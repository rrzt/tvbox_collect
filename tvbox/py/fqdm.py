# -*- coding: utf-8 -*-
# TVBox Python Spider for https://www.fqdm.cc
# 适用于 FongMi 版本

import requests
import re
import json
from urllib.parse import urljoin, quote

class Spider:
    def __init__(self):
        self.siteUrl = "https://www.fqdm.cc"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": self.siteUrl
        }

    # ---------- 必需接口 ----------
    def getDependence(self):
        return ""

    def init(self, ext=""):
        pass

    def homeContent(self, filter=None):
        categories = self._getCategories()
        html = self._fetch(self.siteUrl)
        videos = self._parseVideoList(html)
        return json.dumps({"class": categories, "list": videos}, ensure_ascii=False)

    def homeVideoContent(self, filter=None):
        html = self._fetch(self.siteUrl)
        videos = self._parseVideoList(html)
        return json.dumps({"list": videos}, ensure_ascii=False)

    def categoryContent(self, tid, pg, filter=False, extend=""):
        url = f"{self.siteUrl}/vodshow/{tid}--------{pg}---/"
        html = self._fetch(url)
        videos = self._parseVideoList(html)
        pagecount = self._getPageCount(html) or 999
        return json.dumps({
            "page": pg,
            "pagecount": pagecount,
            "limit": 24,
            "total": pagecount * 24,
            "list": videos
        }, ensure_ascii=False)

    def detailContent(self, ids):
        vid = ids[0]
        html = self._fetch(f"{self.siteUrl}/voddetail/{vid}.html")
        name = self._extract(html, r'<h2[^>]*>([^<]+)</h2>')
        pic = self._extract(html, r'data-original="([^"]*)"')
        if not pic:
            pic = self._extract(html, r'<img[^>]*src="([^"]*)"')
        if pic:
            pic = urljoin(self.siteUrl, pic)
        desc = self._extract(html, r'class="content"[^>]*>([\s\S]*?)</div>')
        if not desc:
            desc = self._extract(html, r'class="info"[^>]*>([\s\S]*?)</div>')
        play_url = self._parsePlayList(html)
        vod = {
            "vod_id": vid,
            "vod_name": name.strip() if name else "",
            "vod_pic": pic or "",
            "vod_content": desc.strip() if desc else "",
            "vod_play_from": "fqdm",
            "vod_play_url": play_url
        }
        return json.dumps({"list": [vod]}, ensure_ascii=False)

    def searchContent(self, key, quick=False):
        url = f"{self.siteUrl}/vodsearch/-------------.html?wd={quote(key)}"
        html = self._fetch(url)
        videos = self._parseVideoList(html)
        return json.dumps({"list": videos}, ensure_ascii=False)

    def playerContent(self, flag, ids, vipFlags=None):
        if not ids.startswith("http"):
            playUrl = urljoin(self.siteUrl, ids)
        else:
            playUrl = ids
        html = self._fetch(playUrl)
        real_url = ""
        # 尝试匹配苹果 CMS 播放器对象
        player_json = self._extract(html, r'player_\w+\s*=\s*({[\s\S]*?});')
        if player_json:
            try:
                data = json.loads(player_json)
                real_url = data.get("url") or data.get("url_next", "")
            except:
                pass
        if not real_url:
            real_url = self._extract(html, r'<video[^>]*src="([^"]*)"')
        if not real_url:
            iframe_src = self._extract(html, r'<iframe[^>]*src="([^"]*)"')
            if iframe_src:
                iframe_url = iframe_src if iframe_src.startswith("http") else urljoin(self.siteUrl, iframe_src)
                return self.playerContent(flag, iframe_url)
        if real_url and not real_url.startswith("http"):
            real_url = urljoin(self.siteUrl, real_url)
        return json.dumps({"url": real_url}, ensure_ascii=False)

    # ---------- 辅助方法 ----------
    def _fetch(self, url):
        resp = requests.get(url, headers=self.headers, timeout=15)
        resp.encoding = "utf-8"
        return resp.text

    def _getCategories(self):
        html = self._fetch(self.siteUrl)
        categories = []
        seen = set()
        # 标准格式：<a href="/vodshow/1--------/...">动漫</a>
        for cid, name in re.findall(r'<a[^>]*href="/vodshow/(\d+)[^"]*"[^>]*>([^<]+)</a>', html):
            if cid not in seen:
                seen.add(cid)
                categories.append({"type_id": cid, "type_name": name.strip()})
        if not categories:
            # 松散匹配
            for cid, name in re.findall(r'href="/vodshow/(\d+)[^"]*"[^>]*>([^<]+)<', html):
                if cid not in seen:
                    seen.add(cid)
                    categories.append({"type_id": cid, "type_name": name.strip()})
        if not categories:
            categories = [{"type_id": "1", "type_name": "动漫"}]
        return categories

    def _parseVideoList(self, html):
        # 找到所有包含 voddetail/数字.html 的 <a> 标签块
        a_blocks = re.findall(r'<a[^>]*href="/voddetail/(\d+)\.html"[^>]*>([\s\S]*?)</a>', html)
        if not a_blocks:
            # 备用：可能结构较乱，只匹配至下一个 <a 或换行
            a_blocks = re.findall(r'<a[^>]*href="/voddetail/(\d+)\.html"[^>]*>(.*?)</a>', html, re.DOTALL)
        videos = []
        for vid, content in a_blocks:
            # 标题
            title = ""
            title_match = re.search(r'title="([^"]*)"', content)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # 去除 HTML 标签取纯文本
                text = re.sub(r'<[^>]+>', '', content).strip()
                if text:
                    title = text
            # 图片
            pic_url = ""
            pic_match = re.search(r'data-original="([^"]*)"', content)
            if not pic_match:
                pic_match = re.search(r'<img[^>]*src="([^"]*)"', content)
            if pic_match:
                pic_url = pic_match.group(1)
                if not pic_url.startswith(("http://", "https://")):
                    pic_url = urljoin(self.siteUrl, pic_url)
            if pic_url:
                videos.append({
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": pic_url,
                    "vod_remarks": ""
                })
            else:
                # 即使没有图片也加入，避免漏掉
                videos.append({
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": "",
                    "vod_remarks": ""
                })
        return videos

    def _parsePlayList(self, html):
        items = re.findall(r'<a[^>]*href="(/vodplay/[^"]+)"[^>]*>([^<]+)</a>', html)
        if not items:
            items = re.findall(r'href="(/vodplay/[^"]+)"[^>]*>([^<]+)<', html)
        episodes = []
        for path, name in items:
            full_url = urljoin(self.siteUrl, path)
            episodes.append(f"{name.strip()}${full_url}")
        return "#".join(episodes)

    def _getPageCount(self, html):
        import math
        total_match = re.search(r'共(\d+)条', html)
        if total_match:
            total = int(total_match.group(1))
            return math.ceil(total / 24)
        return None

    @staticmethod
    def _extract(html, pattern):
        m = re.search(pattern, html, re.DOTALL)
        return m.group(1).strip() if m else ""