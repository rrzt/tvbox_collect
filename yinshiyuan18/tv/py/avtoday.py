#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, json, requests, urllib.parse
from lxml import etree
from base.spider import Spider

class Spider(Spider):
    def getName(self): return "AVToday"
    def init(self, extend=""):
        self.host = "https://avtoday.io"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Referer": self.host + "/chs/index.html"}
        self.categories = [
            {"type_id": "/chs/catalog/中文字幕.html", "type_name": "中文字幕"},
            {"type_id": "/chs/new.html", "type_name": "新片上架"},
            {"type_id": "/chs/hot.html", "type_name": "人气视频"},
            {"type_id": "/chs/no-mosaic.html", "type_name": "无码专区"}
        ]
    def _get(self, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=15)
            r.encoding = r.apparent_encoding or "utf-8"
            return r.text
        except: return None
    def _fix(self, u):
        if not u: return ""
        if u.startswith("//"): return "https:" + u
        if u.startswith("/"): return self.host + u
        return u
    def _parse_list(self, html):
        if not html: return []
        tree = etree.HTML(html); results, seen = [], set()
        cards = tree.xpath('//div[contains(@class,"real-card")]') or tree.xpath('//div[contains(@class,"thumbnail")]')
        for card in cards:
            try:
                a = card.xpath('.//a[contains(@href,"/chs/video/")]')
                if not a: continue
                href = a[0].get("href", "")
                m = re.search(r'/video/([^/]+)\.html', href)
                if not m: continue
                vid = m.group(1)
                if vid in seen: continue
                seen.add(vid)
                img = card.xpath('.//img')
                pic = self._fix(img[0].get("data-src") or img[0].get("data-original") or img[0].get("src", "")) if img else ""
                title = card.get("data-spcode", "") or "".join(card.xpath('.//a[contains(@class,"video-title")]//text()')).strip() or "".join(a[0].xpath('.//text()')).strip() or vid
                results.append({"vod_id": vid, "vod_name": title, "vod_pic": pic})
            except: continue
        if not results:
            for a in tree.xpath('//a[contains(@href,"/chs/video/")]'):
                try:
                    href = a.get("href", "")
                    m = re.search(r'/video/([^/]+)\.html', href)
                    if not m: continue
                    vid = m.group(1)
                    if vid in seen: continue
                    seen.add(vid)
                    img = a.xpath('.//img')
                    pic = self._fix(img[0].get("data-src") or img[0].get("data-original") or img[0].get("src", "")) if img else ""
                    title = "".join(a.xpath('.//text()')).strip() or vid
                    results.append({"vod_id": vid, "vod_name": title, "vod_pic": pic})
                except: continue
        return results
    def homeContent(self, filter):
        html = self._get(self.host + "/chs/index.html")
        return {"class": self.categories, "list": self._parse_list(html) if html else [], "filters": {}}
    def categoryContent(self, tid, pg, filter, extend):
        url = self._fix(tid) if tid.startswith("/") else f"{self.host}/chs/{tid}"
        if int(pg) > 1:
            if "?" in url: url += f"&page={pg}"
            else: url += f"?page={pg}"
        html = self._get(url)
        return {"page": int(pg), "pagecount": 99, "limit": 36, "total": 999, "list": self._parse_list(html) if html else []}
    def detailContent(self, ids):
        result = {"list": []}
        for vid in ids:
            try:
                html = self._get(f"{self.host}/chs/video/{vid}.html")
                if not html: continue
                tree = etree.HTML(html)
                name = "".join(tree.xpath('//h1/text()')).strip() or vid
                pic = self._fix("".join(tree.xpath('//meta[@property="og:image"]/@content')) or "".join(tree.xpath('//div[contains(@class,"video-card")]//img/@src')))
                iframe = tree.xpath('//iframe[contains(@class,"video-frame")]/@src')
                play_url = self._fix(iframe[0]) if iframe else f"{self.host}/player?s={vid}"
                result["list"].append({
                    "vod_id": vid,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_play_from": "AVToday",
                    "vod_play_url": f"在线播放${play_url}"
                })
            except: continue
        return result
    def searchContent(self, key, quick, pg="1"):
        url = f"{self.host}/chs/search?s={urllib.parse.quote(key)}"
        if int(pg) > 1: url += f"&page={pg}"
        html = self._get(url)
        return {"list": self._parse_list(html) if html else [], "page": int(pg)}
    def playerContent(self, flag, id, vipFlags):
        url = self._fix(id)
        if "/player" in url:
            html = self._get(url)
            if html:
                m = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', html) or re.search(r'url\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']', html)
                if m: url = m.group(1)
        return {"parse": 1, "url": url, "header": json.dumps(self.headers)}