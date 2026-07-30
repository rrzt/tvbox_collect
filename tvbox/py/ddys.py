#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, json, requests
from urllib.parse import quote
try:
    from lxml import etree
except Exception:
    etree = None
from base.spider import Spider

BADIMG = ("logo", "loading", "nopic", "no-pic", "static/")


class Spider(Spider):
    def getName(self): return "低端影视"

    def init(self, extend=""):
        self.host = "https://www.ddys.run"
        try: ext = json.loads(extend) if str(extend).strip().startswith("{") else {}
        except Exception: ext = {}
        if ext.get("host"): self.host = ext["host"].rstrip("/")
        self.headers = {"User-Agent": ext.get("ua", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"), "Referer": self.host + "/", "Accept-Language": "zh-CN,zh;q=0.9", "Cookie": ext.get("cookie", "pageLogin=ok")}
        self.listFmt = ext.get("listFmt", "")
        self.categories = [{"type_id": "dianying", "type_name": "电影"}, {"type_id": "juji", "type_name": "剧集"}, {"type_id": "dongman", "type_name": "动漫"}]

    def _fix(self, u):
        if not u: return ""
        if u.startswith("//"): return "https:" + u
        if u.startswith("/"): return self.host + u
        return u

    def _get(self, path):
        url = path if path.startswith("http") else self.host + path
        try:
            r = requests.get(url, headers=self.headers, timeout=15); r.encoding = "utf-8"
            if r.status_code >= 400: print("[WARN] status=%s url=%s" % (r.status_code, url)); return None
            return r.text
        except requests.exceptions.Timeout: print("[ERROR] 请求超时: %s" % url)
        except requests.exceptions.ConnectionError: print("[ERROR] 连接错误: %s" % url)
        except Exception as e: print("[ERROR] 请求失败: %s, %s" % (url, str(e)))
        return None

    def _post(self, path, data):
        try:
            r = requests.post(self.host + path, data=data, headers=self.headers, timeout=15); r.encoding = "utf-8"; return r.text
        except Exception as e: print("[ERROR] POST失败: %s, %s" % (path, str(e))); return None

    def _img(self, node):
        for at in ("data-original", "data-src", "data-echo", "src"):
            for v in node.xpath('.//@%s' % at):
                if v and re.search(r'\.(jpg|jpeg|png|webp|avif)', v) and not any(b in v for b in BADIMG): return v
        return ""

    def _parse_list(self, html):
        if not html: return []
        if etree is None:
            print("[WARN] lxml 不可用，降级为正则解析")
            out, seen = [], set()
            for slug, title in re.findall(r'href="/video/([^"]+)\.html"[^>]*title="([^"]*)"', html):
                if slug in seen: continue
                seen.add(slug); out.append({"vod_id": slug, "vod_name": title, "vod_pic": ""})
            return out
        tree = etree.HTML(html); results, seen = [], set()
        items = tree.xpath('//a[contains(@class,"stui-vodlist__thumb") and contains(@href,"/video/")]') or tree.xpath('//div[contains(@class,"stui-vodlist__box")]//a[contains(@href,"/video/")]') or tree.xpath('//a[contains(@href,"/video/") and @title]')
        for it in items:
            try:
                m = re.search(r'/video/([^/.]+)\.html', it.get("href", ""))
                if not m or m.group(1) in seen: continue
                name = (it.get("title") or "".join(it.xpath('.//img/@alt')[:1])).strip()
                if not name: continue
                seen.add(m.group(1))
                note = "".join(it.xpath('.//span[contains(@class,"pic-text")]//text()')).strip()
                results.append({"vod_id": m.group(1), "vod_name": name, "vod_pic": self._fix(self._img(it)), "vod_remarks": note})
            except Exception: continue
        return results

    def _dcount(self, sep):
        try: return len(re.findall(r'/list/[a-z0-9]+(%s*)\.html' % re.escape(sep), self._home)[0])
        except Exception: return 11

    def homeContent(self, filter):
        self._home = self._get("/") or ""
        fl = {}
        return {"class": self.categories, "list": self._parse_list(self._home), "filters": fl}

    def homeVideoContent(self): return {"list": self._parse_list(self._get("/"))}

    def categoryContent(self, tid, pg, filter, extend):
        pg = str(pg or "1")
        cands = ["/list/%s-%s----------.html" % (tid, pg), "/list/%s----------%s-.html" % (tid, pg), "/list/%s-----------.html?page=%s" % (tid, pg)]
        if self.listFmt: cands = [self.listFmt % (tid, pg)]
        lst = []
        for c in cands:
            lst = self._parse_list(self._get(c))
            if lst:
                self.listFmt = c.replace(tid, "%s", 1).replace("-%s-" % pg, "-%s-", 1).replace("%s-" % pg + "-", "%s--", 1) if not self.listFmt else self.listFmt
                self.listFmt = c.split(tid, 1)[0] + "%s" + c.split(tid, 1)[1].replace(pg, "%s", 1)
                break
        return {"page": int(pg), "pagecount": int(pg) + 1 if lst else int(pg), "limit": 48, "total": 999999, "list": lst}

    def searchContent(self, key, quick, pg="1"):
        pg = str(pg or "1")
        lst = self._parse_list(self._get("/search/-------------.html?wd=%s&page=%s" % (quote(key), pg)))
        if not lst:
            lst = self._parse_list(self._post("/search/-------------.html", {"wd": key}))
        if not lst:
            lst = self._parse_list(self._get("/vodsearch/-------------.html?wd=%s" % quote(key)))
        return {"list": lst, "page": int(pg)}

    def detailContent(self, ids):
        slug = str(ids[0])
        html = self._get("/video/%s.html" % slug)
        if not html or etree is None: return {"list": []}
        tree = etree.HTML(html)
        text = "\n".join(x.strip() for x in tree.xpath('//text()') if x.strip())
        pic = self._img(tree) or "".join(tree.xpath('//img[contains(@class,"lazyload")]/@data-original')[:1])
        vod = {"vod_id": slug,
               "vod_name": ("".join(tree.xpath('//h1//text()')).strip() or "".join(tree.xpath('//div[contains(@class,"stui-content__detail")]//h1/text()')).strip()),
               "vod_pic": self._fix(pic),
               "vod_year": self._field(text, "年份"), "vod_area": self._field(text, "地区"),
               "type_name": self._field(text, "分类") or self._field(text, "类型"),
               "vod_lang": self._field(text, "语言"),
               "vod_actor": self._field(text, "主演"), "vod_director": self._field(text, "导演"),
               "vod_remarks": self._field(text, "备注") or self._field(text, "状态"),
               "vod_content": re.sub(r'\s+', ' ', "".join(tree.xpath('//span[contains(@class,"detail-content")]//text() | //div[contains(@class,"detail")]//span[contains(@class,"content")]//text()'))).strip()}
        froms, urls = [], []
        heads = tree.xpath('//div[contains(@class,"stui-pannel__head") or contains(@class,"playlist")]//h3/text() | //div[contains(@class,"stui-vodlist__head")]//h3/text()')
        lists = tree.xpath('//ul[contains(@class,"stui-content__playlist") or contains(@class,"stui-content__list") or contains(@class,"content__playlist")]')
        for i, ul in enumerate(lists):
            eps = []
            for a in ul.xpath('.//a'):
                nm = ("".join(a.xpath('.//text()')).strip() or a.get("title", "")).strip()
                lk = a.get("href", "")
                if not nm or not lk: continue
                eps.append(nm.replace("$", "").replace("#", "") + "$" + self._fix(lk))
            if eps:
                froms.append(heads[i].strip() if i < len(heads) else "线路%d" % (i + 1))
                urls.append("#".join(eps))
        vod["vod_play_from"] = "$$$".join(froms) if froms else "低端影视"
        vod["vod_play_url"] = "$$$".join(urls) if urls else ("正片$%s/video/%s.html" % (self.host, slug))
        return {"list": [vod]}

    def _field(self, text, key):
        m = re.search(r'%s\s*[:：]\s*([^\n]{1,200})' % key, text)
        return m.group(1).strip(" \u3000|/") if m else ""

    def playerContent(self, flag, id, vipFlags):
        pid = id if id.startswith("http") else self._fix(id)
        html = self._get(pid) or ""
        url = ""
        for p in [r'var\s+player_\w*\s*=\s*(\{.*?\})\s*[<;]', r'"url"\s*:\s*"([^"]+)"', r'var\s+now\s*=\s*["\']([^"\']+)["\']', r'url:\s*["\']([^"\']+\.(?:m3u8|mp4)[^"\']*)["\']', r'(https?://[^\s"\'\\<>]+\.(?:m3u8|mp4)[^\s"\'\\<>]*)']:
            m = re.search(p, html.replace("\\/", "/"), re.S)
            if not m: continue
            val = m.group(1)
            if val.startswith("{"):
                try: val = json.loads(val).get("url", "")
                except Exception:
                    m2 = re.search(r'"url"\s*:\s*"([^"]+)"', val); val = m2.group(1).replace("\\/", "/") if m2 else ""
            if val: url = self._fix(val); break
        if not url: return {"parse": 1, "url": pid, "header": self.headers}
        return {"parse": 0, "url": url, "header": {"User-Agent": self.headers["User-Agent"], "Referer": self.host + "/"}}
