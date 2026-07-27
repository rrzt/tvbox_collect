# -*- coding: utf-8 -*-
import json
import re
import requests
from bs4 import BeautifulSoup

# 尝试导入 TVBox/CatVod 框架基类，如果不在 TVBox 运行环境中则定义模拟基类
try:
    from spider import Spider as BaseSpider
except ImportError:
    class BaseSpider:
        pass

class PornLuluSpider(BaseSpider):

    def getName(self):
        return "pornlulu"

    def init(self, extend=""):
        self.site_url = "https://www.pornlulu.net"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; 2407FRK8EC Build/AP3A.240617.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36",
            "Origin": self.site_url,
            "Referer": f"{self.site_url}/"
        }
        # 创建 requests Session 保持会话
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch(self, url, headers=None):
        """兼容 TVBox 框架的 fetch 请求方法"""
        try:
            req_headers = self.headers.copy()
            if headers:
                req_headers.update(headers)
            response = self.session.get(url, headers=req_headers, timeout=10)
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            print(f"[Error] Fetch url failed ({url}): {e}")
            return None

    def isVideoFormat(self, url):
        return True

    def manualVideoCheck(self):
        return False

    def action(self, action):
        return ""

    def homeContent(self, filter):
        result = {}
        classes = []
        
        # 请求主页，动态获取导航分类
        rsp = self.fetch(self.site_url)
        if rsp and rsp.text:
            soup = BeautifulSoup(rsp.text, 'html.parser')
            # 寻找 ul#w5 或 ul#w4 节点
            ul_cate = soup.find("ul", id="w5") or soup.find("ul", id="w4")
            if ul_cate:
                li_list = ul_cate.find_all("li")
                for li in li_list:
                    a_tag = li.find("a")
                    if not a_tag:
                        continue
                    
                    p_tag = li.find("p")
                    cate_title = p_tag.get_text(strip=True) if p_tag else a_tag.get_text(strip=True)
                    cate_href = a_tag.get("href", "").strip()
                    
                    # 过滤无效或首页重复链接
                    if cate_href and cate_title and cate_href != "/" and cate_href != self.site_url:
                        cate_id = cate_href.replace(self.site_url, "").strip("/")
                        classes.append({
                            "type_id": cate_id,
                            "type_name": cate_title
                        })

        # 兜底默认分类
        if not classes:
            classes = [
                {"type_id": "videos", "type_name": "全部视频"},
                {"type_id": "folder-0-0-H", "type_name": "博主"}
            ]

        result['class'] = classes
        
        # 筛选配置
        filters = {}
        for item in classes:
            filters[item['type_id']] = [
                {
                    "key": "by",
                    "name": "排序",
                    "value": [
                        {"n": "最新", "v": "newest"},
                        {"n": "推荐", "v": "promoted"},
                        {"n": "热门🔥", "v": "hottest"},
                        {"n": "最多点赞👍", "v": "mostlike"}
                    ]
                }
            ]

        if filter:
            result['filters'] = filters
            
        return result

    def homeVideoContent(self):
        return self.categoryContent("videos", "1", False, {})

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        videos = []
        
        # 构建分类 URL
        tid_clean = tid.strip('/')
        if tid_clean.startswith("http"):
            url = tid_clean
        elif "folder-" in tid_clean:
            url = f"{self.site_url}/{tid_clean}/"
        else:
            url = f"{self.site_url}/{tid_clean}?page={pg}"

        # 拼接排序筛选参数
        if extend and "by" in extend and extend['by']:
            sep = "&" if "?" in url else "?"
            url += f"{sep}by={extend['by']}"

        rsp = self.fetch(url)
        if not rsp or not rsp.text:
            return {"list": [], "page": int(pg), "pagecount": 0, "limit": 0, "total": 0}

        soup = BeautifulSoup(rsp.text, 'html.parser')
        
        # 提取列表卡片
        container = soup.find(id="videos")
        cards = container.select(".card") if container else soup.select(".card")

        for card in cards:
            img_tag = card.find("img")
            a_tag = card.find("a")
            
            if not a_tag:
                continue

            pic = ""
            if img_tag:
                pic = img_tag.get("data-src") or img_tag.get("data-original") or img_tag.get("src") or ""

            title = img_tag.get("alt", "").strip() if (img_tag and img_tag.get("alt")) else a_tag.get_text(strip=True)
            href = a_tag.get("href", "").strip()

            if not href or href == "#" or href.startswith("javascript:"):
                continue

            if href.startswith("/"):
                href = self.site_url + href
            elif not href.startswith("http"):
                href = f"{self.site_url}/{href}"

            videos.append({
                "vod_id": href,
                "vod_name": title,
                "vod_pic": pic,
                "vod_remarks": ""
            })

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = int(pg) + 1
        result['limit'] = len(videos)
        result['total'] = 9999
        return result

    def detailContent(self, array):
        if not array:
            return {}

        vod_id = array[0]
        rsp = self.fetch(vod_id)
        if not rsp or not rsp.text:
            return {}

        soup = BeautifulSoup(rsp.text, 'html.parser')
        
        # 提取标题
        title = ""
        img_tag = soup.find("img")
        if img_tag and img_tag.get("alt"):
            title = img_tag.get("alt").strip()

        # 提取演员/博主
        actor_list = []
        meta_div = soup.find("div", class_="video-meta")
        if meta_div:
            actors = meta_div.find_all("a")
            actor_list = [a.get_text(strip=True) for a in actors]
        actor = " / ".join(actor_list)

        # 提取类型
        type_div = soup.find("div", attrs={"style": re.compile(r"margin-bottom:\s*16px;?")})
        type_name = type_div.get_text(strip=True) if type_div else ""

        # 提取播放链接
        play_url = ""
        widget_div = soup.find(id="videojs-widget")
        if widget_div:
            source_tag = widget_div.find("source")
            if source_tag and source_tag.get("src"):
                play_url = source_tag.get("src")

        vod_play_from = "PornLulu"
        vod_play_url = f"高清${play_url if play_url else vod_id}"

        vod = {
            "vod_id": vod_id,
            "vod_name": title if title else "未知影片",
            "vod_pic": "",
            "type_name": type_name,
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": actor,
            "vod_director": "",
            "vod_content": title,
            "vod_play_from": vod_play_from,
            "vod_play_url": vod_play_url
        }

        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        url = f"{self.site_url}/q/{key}?category_id=&page={pg}"
        rsp = self.fetch(url)
        
        videos = []
        if rsp and rsp.text:
            soup = BeautifulSoup(rsp.text, 'html.parser')
            container = soup.find(id="videos")
            cards = container.select(".card") if container else soup.select(".card")

            for card in cards:
                img_tag = card.find("img")
                a_tag = card.find("a")
                
                if not a_tag:
                    continue

                pic = ""
                if img_tag:
                    pic = img_tag.get("data-src") or img_tag.get("data-original") or img_tag.get("src") or ""

                title = img_tag.get("alt", "").strip() if (img_tag and img_tag.get("alt")) else a_tag.get_text(strip=True)
                href = a_tag.get("href", "").strip()

                if not href or href == "#" or href.startswith("javascript:"):
                    continue

                if href.startswith("/"):
                    href = self.site_url + href
                elif not href.startswith("http"):
                    href = f"{self.site_url}/{href}"

                videos.append({
                    "vod_id": href,
                    "vod_name": title,
                    "vod_pic": pic,
                    "vod_remarks": ""
                })

        return {
            "list": videos,
            "page": int(pg)
        }

    def playerContent(self, flag, id, vipFlags):
        headers = {
            "User-Agent": self.headers["User-Agent"],
            "Referer": self.site_url,
            "Origin": self.site_url
        }
        return {
            "parse": 0,
            "url": id,
            "header": headers
        }

    def localProxy(self, param):
        return [200, "video/MP2T", ""]


# 本地直接运行测试程序入口
if __name__ == "__main__":
    spider = PornLuluSpider()
    spider.init()

    print("=== 测试 1: 获取首页分类 (homeContent) ===")
    home_res = spider.homeContent(filter=True)
    print(json.dumps(home_res, ensure_ascii=False, indent=2))

    print("\n=== 测试 2: 获取分类列表数据 (categoryContent) ===")
    cat_res = spider.categoryContent("videos", "1", False, {})
    print(f"解析获得视频数量: {len(cat_res.get('list', []))}")
    if cat_res.get('list'):
        first_vod = cat_res['list'][0]
        print("第1条视频数据:", json.dumps(first_vod, ensure_ascii=False, indent=2))

        print("\n=== 测试 3: 获取视频详情页 (detailContent) ===")
        detail_res = spider.detailContent([first_vod['vod_id']])
        print(json.dumps(detail_res, ensure_ascii=False, indent=2))