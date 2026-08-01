# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib.parse
from bs4 import BeautifulSoup
import requests

# 导入基类（兼容 CatVod / TVBox 蜘蛛框架）
try:
    from base.spider import Spider
except ImportError:

    class Spider:
        pass


class Spider(Spider):
    site_url = "https://www.ibbs.pro"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def getName(self):
        return "情色小说论坛"

    def init(self, extend=""):
        pass

    def isVideo(self, url):
        pass

    def destroy(self):
        pass

    # 分类列表
    def homeContent(self, filter):
        result = {}
        classes = [{"type_name": "视频", "type_id": "6095467d69deb6073dc6d6d7"}]
        result["class"] = classes
        return result

    # 首页推荐数据
    def homeVideoContent(self):
        return {"list": []}

    # 分类页数据
    def categoryContent(self, tid, pg, filter, extend):
        result = {
            "list": [],
            "page": pg,
            "pagecount": 999,
            "limit": 20,
            "total": 9999,
        }
        try:
            url = f"{self.site_url}/category/{tid}?pagenumber={pg}"
            res = requests.get(url, headers=self.headers, timeout=10)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, "html.parser")

            filter_words = [
                "皇宫",
                "棋牌",
                "pg娱乐",
                "潘多拉直播",
                "24小时在线匹配",
                "站长担保",
                "骚货",
            ]
            items = soup.select("div.row.mt-3 > div.col-md-6")
            if not items:
                items = soup.select("[class^=col-lg-9] [class^=col-md-6]")

            videos = []
            for item in items:
                text = item.get_text()
                if any(w in text for w in filter_words):
                    continue

                title_el = item.select_one("h6 a") or item.select_one("a")
                if not title_el:
                    continue

                title = (
                    title_el.get("title", "")
                    or title_el.get_text(strip=True)
                )
                href = title_el.get("href", "")

                img_el = item.select_one("figure img") or item.select_one("img")
                pic = ""
                if img_el:
                    pic = (
                        img_el.get("src")
                        or img_el.get("data-src")
                        or img_el.get("data-original")
                        or ""
                    )

                date_el = item.select_one(".entry-overlay-date")
                remark = date_el.get_text(strip=True) if date_el else ""

                if href and not href.startswith("http"):
                    href = urllib.parse.urljoin(self.site_url, href)
                if pic and not pic.startswith("http"):
                    pic = urllib.parse.urljoin(self.site_url, pic)

                videos.append(
                    {
                        "vod_id": href,
                        "vod_name": title,
                        "vod_pic": pic,
                        "vod_remarks": remark,
                    }
                )
            result["list"] = videos
        except Exception:
            pass
        return result

    # 详情页
    def detailContent(self, array):
        vod_url = array[0]
        vod = {
            "vod_id": vod_url,
            "vod_name": "视频详情",
            "vod_play_from": "默认线路",
            "vod_play_url": f"播放${vod_url}",
        }
        try:
            res = requests.get(vod_url, headers=self.headers, timeout=10)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, "html.parser")

            title_el = (
                soup.select_one("h1")
                or soup.select_one("h2")
                or soup.select_one("title")
            )
            if title_el:
                vod["vod_name"] = title_el.get_text(strip=True)

            img_el = (
                soup.select_one('meta[property="og:image"]')
                or soup.select_one("figure img")
                or soup.select_one("img")
            )
            if img_el:
                pic = (
                    img_el.get("content")
                    or img_el.get("src")
                    or img_el.get("data-src")
                    or ""
                )
                if pic and not pic.startswith("http"):
                    pic = urllib.parse.urljoin(self.site_url, pic)
                vod["vod_pic"] = pic

            # 在 TVBox 中，播放地址直接传帖子详情页 ID，交给 playerContent 动态解析
            vod["vod_play_url"] = f"播放${vod_url}"

        except Exception:
            pass

        return {"list": [vod]}

    # 搜索页数据
    def searchContent(self, key, quick):
        result = {"list": []}
        try:
            url = f"{self.site_url}/searchthread?s={urllib.parse.quote(key)}"
            res = requests.get(url, headers=self.headers, timeout=10)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, "html.parser")

            items = soup.select("div.row.mt-3 > div.col-md-6")
            if not items:
                items = soup.select("[class^=col-lg-9] [class^=col-md-6]")

            videos = []
            for item in items:
                if "皇宫" in item.get_text():
                    continue

                title_el = item.select_one("h6 a") or item.select_one("a")
                if not title_el:
                    continue

                title = (
                    title_el.get("title", "")
                    or title_el.get_text(strip=True)
                )
                href = title_el.get("href", "")

                img_el = item.select_one("figure img") or item.select_one("img")
                pic = ""
                if img_el:
                    pic = (
                        img_el.get("src")
                        or img_el.get("data-src")
                        or img_el.get("data-original")
                        or ""
                    )

                date_el = item.select_one(".entry-overlay-date")
                remark = date_el.get_text(strip=True) if date_el else ""

                if href and not href.startswith("http"):
                    href = urllib.parse.urljoin(self.site_url, href)
                if pic and not pic.startswith("http"):
                    pic = urllib.parse.urljoin(self.site_url, pic)

                videos.append(
                    {
                        "vod_id": href,
                        "vod_name": title,
                        "vod_pic": pic,
                        "vod_remarks": remark,
                    }
                )
            result["list"] = videos
        except Exception:
            pass
        return result

    # 核心：播放解析
    def playerContent(self, flag, id, vipFlags):
        # 传输 Referer，部分视频防盗链需要
        play_header = {
            "User-Agent": self.headers["User-Agent"],
            "Referer": id,
        }
        result = {"parse": 0, "url": "", "header": play_header}

        try:
            # 1. 请求帖子详情页
            res = requests.get(id, headers=self.headers, timeout=10)
            res.encoding = "utf-8"
            html_text = res.text
            soup = BeautifulSoup(html_text, "html.parser")

            # 2. 尝试第一种情况：如果页面直接有常规 m3u8/mp4 视频链接
            m3u8_matches = re.findall(
                r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)', html_text
            )
            mp4_matches = re.findall(
                r'(https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*)', html_text
            )

            filtered_m3u8 = [u for u in m3u8_matches if "baidu.com" not in u]
            filtered_mp4 = [u for u in mp4_matches if "baidu.com" not in u]

            if filtered_m3u8:
                result["url"] = filtered_m3u8[0]
                return result
            elif filtered_mp4:
                result["url"] = filtered_mp4[0]
                return result

            # 3. 核心情况：提取动态 m3u8 接口需要的两个关键参数 (m3u8name + videoid)
            m3u8_name = None
            video_tag = soup.find("video", attrs={"data-m3u8name": True})
            if video_tag:
                m3u8_name = video_tag.get("data-m3u8name")

            # 提取 JS 里的 videoid
            video_id = None
            video_id_match = re.search(
                r"['\"]?videoid['\"]?\s*[:=]\s*['\"]([^'\"]+)['\"]",
                html_text,
                re.IGNORECASE,
            )
            if video_id_match:
                video_id = video_id_match.group(1)
            else:
                # 备用匹配 UUID 标准格式
                uuid_match = re.search(
                    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                    html_text,
                    re.IGNORECASE,
                )
                if uuid_match:
                    video_id = uuid_match.group(0)

            # 4. 如果找到了参数，调用接口请求真实链接
            if m3u8_name and video_id:
                api_relative_path = f"/generatedataurl/{m3u8_name}/{video_id}"
                api_url = urllib.parse.urljoin(self.site_url, api_relative_path)

                req_headers = self.headers.copy()
                req_headers["Referer"] = id

                api_res = requests.get(api_url, headers=req_headers, timeout=10)
                if api_res.status_code == 200:
                    try:
                        json_data = api_res.json()
                        real_url = (
                            json_data.get("url")
                            or json_data.get("m3u8")
                            or json_data.get("src")
                        )
                        if real_url:
                            if not real_url.startswith("http"):
                                real_url = urllib.parse.urljoin(
                                    self.site_url, real_url
                                )
                            result["url"] = real_url
                            return result
                    except Exception:
                        pass

            # 如果均未能找到，退回原链接让客户端自适应解析
            result["url"] = id
            result["parse"] = 1

        except Exception:
            result["url"] = id
            result["parse"] = 1

        return result

    def localProxy(self, param):
        pass
