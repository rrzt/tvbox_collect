#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, json, requests
from collections import Counter
from urllib.parse import quote
try:
    from lxml import etree
except Exception:
    etree = None
from base.spider import Spider

# 注意：站点存在 /aiad (AI脱衣/AI换脸类工具) 入口，本源不抓取、不引用、不提供任何访问路径
GENRES = [["动作", "dongzuo"], ["爱情", "aiqing"], ["喜剧", "xiju"], ["科幻", "kehuan"], ["恐怖", "kongbu"],
          ["战争", "zhanzheng"], ["武侠", "wuxia"], ["魔幻", "mohuan"], ["剧情", "juqing"], ["动画", "donghua"],
          ["惊悚", "jingsong"], ["3D", "3D"], ["灾难", "zainan"], ["悬疑", "xuanyi"], ["警匪", "jingfei"],
          ["文艺", "wenyi"], ["青春", "qingchun"], ["冒险", "maoxian"], ["犯罪", "fanzui"], ["纪录", "jilu"],
          ["古装", "guzhuang"], ["奇幻", "qihuan"], ["国语", "guoyu"], ["综艺", "zongyi"], ["历史", "lishi"],
          ["运动", "yundong"], ["原创压制", "yuanchuang"], ["美剧", "meiju"], ["韩剧", "hanju"],
          ["国产电视剧", "guoju"], ["日剧", "riju"], ["英剧", "yingju"], ["德剧", "deju"], ["俄剧", "eju"],
          ["巴剧", "baju"], ["加剧", "jiaju"], ["西剧", "spanish"], ["意大利剧", "yidaliju"], ["泰剧", "taiju"],
          ["港台剧", "gangtaiju"], ["法剧", "faju"], ["澳剧", "aoju"], ["短剧", "duanju"]]
ITEM_RE = re.compile(r'^/([A-Za-z0-9]+)/(\d+)\.htm$')


class Spider(Spider):
    def getName(self): return "雪落影视"

    def init(self, extend=""):
        self.host = "https://v.xl01.eu.cc"
        try: ext = json.loads(extend) if str(extend).strip().startswith("{") else {}
        except Exception: ext = {}
        if ext.get("host"): self.host = ext["host"].rstrip("/")
        self.headers = {"User-Agent": ext.get("ua", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"), "Referer": self.host + "/", "Accept-Language": "zh-CN,zh;q=0.9"}
        if ext.get("cookie"): self.headers["Cookie"] = ext["cookie"]
        self.categories = [{"type_id": "all0", "type_name": "电影"}, {"type_id": "all1", "type_name": "剧集"}] + \
                           [{"type_id": g[1], "type_name": g[0]} for g in GENRES]

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
            body = r.text
            if body and body[0] == "\ufeff": body = body[1:]  # 去除UTF-8 BOM，否则lxml.etree.HTML会报XMLSyntaxError(USC4 little endian)
            return body
        except requests.exceptions.Timeout: print("[ERROR] 请求超时: %s" % url)
        except requests.exceptions.ConnectionError: print("[ERROR] 连接错误: %s" % url)
        except Exception as e: print("[ERROR] 请求失败: %s, %s" % (url, str(e)))
        return None

    def _tree(self, html, tag="页面"):
        if not html: return None
        if etree is None: print("[WARN] lxml 不可用"); return None
        try:
            tree = etree.HTML(html)
        except Exception as e:
            print("[WARN] %s etree解析异常: %s: %s，长度=%d 片段=%r" % (tag, type(e).__name__, e, len(html), html[:80]))
            return None
        if tree is None: print("[WARN] %s etree解析为空，长度=%d 片段=%r" % (tag, len(html), html[:80]))
        return tree

    def _regex_list(self, html):
        out, seen = [], set()
        for m in re.finditer(r'href="([^"]+)"[^>]*title="([^"]*)"', html):
            mm = ITEM_RE.match(m.group(1))
            if not mm or mm.group(0) in seen: continue
            seen.add(mm.group(0))
            out.append({"vod_id": "%s/%s" % (mm.group(1), mm.group(2)), "vod_name": m.group(2), "vod_pic": ""})
        return out

    def _parse_list(self, html):
        if not html: return []
        tree = self._tree(html, "列表") if etree else None
        if tree is None: return self._regex_list(html)
        groups = {}
        for a in tree.xpath('//a[@href]'):
            href = a.get("href", "")
            m = ITEM_RE.match(href.split("?")[0].split("#")[0])
            if not m: continue
            groups.setdefault((m.group(1), m.group(2)), []).append(a)
        results = []
        for (genre, vid), anchors in groups.items():
            name, pic, note = "", "", ""
            for a in anchors:
                if not name:
                    h4 = "".join(a.xpath('.//h4//text()')).strip()
                    if h4: name = h4
                if not pic:
                    for at in ("data-original", "data-src", "src"):
                        v = a.xpath('.//img/@%s' % at)
                        if v and v[0].strip(): pic = v[0]; break
                if not note: note = "".join(a.xpath('.//span//text() | .//em//text()')).strip()
            if not name:
                for a in anchors:
                    cand = (a.xpath('./following-sibling::h4[1]//text()')
                            or a.xpath('./preceding-sibling::h4[1]//text()')
                            or a.xpath('../h4//text()')
                            or a.xpath('../following-sibling::h4[1]//text()')
                            or a.xpath('../preceding-sibling::h4[1]//text()'))
                    if cand: name = "".join(cand).strip(); break
            if not name:
                for a in anchors:
                    if a.get("title"): name = a.get("title").strip(); break
            if not name: continue
            results.append({"vod_id": "%s/%s" % (genre, vid), "vod_name": name,
                             "vod_pic": self._fix(pic), "vod_remarks": note})
        return results

    def _first(self, lst): return lst[0]["vod_id"] if lst else ""

    def _paged(self, base, pg):
        if pg == "1": return self._get(base)
        sep = "&" if "?" in base else "?"
        cands = ["%s" + sep + "page=%s"] + (["%s/page/%s"] if "?" not in base else [])
        first = self._first(self._parse_list(self._get(base)))
        for f in cands:
            html = self._get(f % (base, pg))
            got = self._parse_list(html)
            if got and self._first(got) != first:
                print("[INFO] 分页格式确定: %s" % (f % ("{base}", "{pg}")))
                return html
        print("[WARN] 未能确定分页格式，仅返回首屏")
        return self._get(base)

    def homeContent(self, filter):
        fl = {"all0": [{"key": "area", "name": "地区", "value": [{"n": "全部", "v": ""}, {"n": "中国大陆", "v": "中国大陆"}]}],
              "all1": [{"key": "area", "name": "地区", "value": [{"n": "全部", "v": ""}, {"n": "中国大陆", "v": "中国大陆"}]}]}
        return {"class": self.categories, "list": self._parse_list(self._get("/")), "filters": fl}

    def homeVideoContent(self): return {"list": self._parse_list(self._get("/"))}

    def categoryContent(self, tid, pg, filter, extend):
        pg = str(pg or "1")
        if tid.startswith("all"):
            base = "/s/all?type=%s" % tid[3:]
            area = (extend or {}).get("area", "")
            if area: base += "&area=%s" % quote(area)
        else:
            base = "/s/%s" % tid
        lst = self._parse_list(self._paged(base, pg))
        return {"page": int(pg), "pagecount": int(pg) + 1 if lst else int(pg), "limit": 30, "total": 999999, "list": lst}

    def searchContent(self, key, quick, pg="1"):
        pg = str(pg or "1")
        for p in ["/s/all?wd=%s&page=%s" % (quote(key), pg), "/search?wd=%s&page=%s" % (quote(key), pg)]:
            lst = self._parse_list(self._get(p))
            if lst: return {"list": lst, "page": int(pg)}
        return {"list": [], "page": int(pg)}

    def _field(self, text, key):
        m = re.search(r'%s\s*[:：]\s*([^\n]{1,200})' % key, text)
        return m.group(1).strip(" \u3000|/") if m else ""

    def detailContent(self, ids):
        vid = str(ids[0])
        html = self._get("/%s.htm" % vid)
        tree = self._tree(html, "详情页")
        if tree is None: return {"list": []}
        text = "\n".join(x.strip() for x in tree.xpath('//text()') if x.strip())
        title_line = "".join(tree.xpath('//h1//text()')).strip()
        m = re.match(r'^(.*?)\s*[\(（](\d{4})[\)）]\s*$', title_line)
        name, year = (m.group(1), m.group(2)) if m else (title_line, self._field(text, "年份"))
        rate_m = re.search(r'(\d\.\d)\s*豆瓣评分', text)
        pic = ""
        for v in tree.xpath('//img/@data-original | //img/@src'):
            if v and v.strip(): pic = v; break
        # 该站每个页面的导航菜单会把全部约40个类型链接完整重复渲染，频次相同；
        # 正文里该条目自己标注的"类型"标签会比导航基线多出现1次，据此和导航区分，无需依赖具体的CSS/容器结构
        freq = {}
        for a in tree.xpath('//a[starts-with(@href,"/s/")]'):
            h = a.get("href"); freq[h] = freq.get(h, 0) + 1
        baseline = Counter(freq.values()).most_common(1)[0][0] if freq else 0
        item_genres = [h.split("/s/")[-1] for h, c in freq.items() if c > baseline]
        slug_name = {g[1]: g[0] for g in GENRES}
        type_name = " ".join(slug_name.get(s, s) for s in item_genres) or self._field(text, "类型")
        vod = {"vod_id": vid, "vod_name": name, "vod_pic": self._fix(pic),
               "vod_year": year, "vod_area": self._field(text, "制片国家"),
               "type_name": type_name,
               "vod_director": " ".join(tree.xpath('//a[contains(@href,"/director/")]/text()')),
               "vod_actor": " ".join(tree.xpath('//a[contains(@href,"/performer/")]/text()')),
               "vod_remarks": (rate_m.group(1) + "分") if rate_m else (self._field(text, "集数") and ("共%s集" % self._field(text, "集数"))),
               "vod_content": ""}
        pre = text.split("在线播放", 1)[0] if "在线播放" in text else text
        lines = [l.strip() for l in pre.split("\n") if l.strip()]
        last_label = -1
        for i, l in enumerate(lines):
            if re.match(r'^[\u4e00-\u9fffA-Za-z]{2,8}[:：]', l): last_label = i
        content_lines = lines[last_label + 1:] if last_label >= 0 else lines
        vod["vod_content"] = " ".join(content_lines)[:500]
        eps, seen = [], set()
        for m2 in re.finditer(r'<a[^>]+href="([^"]*?/play/%s-\d+\.htm[^"]*)"[^>]*>([^<]*)</a>' % re.escape(vid.split("/")[-1]), html):
            href, nm = m2.group(1), m2.group(2).strip()
            if not nm or href in seen: continue
            seen.add(href)
            eps.append(nm.replace("$", "").replace("#", "") + "$" + self._fix(href))
        vod["vod_play_from"] = "雪落影视"
        vod["vod_play_url"] = "#".join(eps) if eps else ("播放$%s/play/%s-0.htm" % (self.host, vid.split("/")[-1]))
        return {"list": [vod]}

    def playerContent(self, flag, id, vipFlags):
        pid = id if id.startswith("http") else self._fix(id)
        html = self._get(pid) or ""
        url = ""
        # 专门识别 {"code":0,"data":{"url3":...}} 这种结构（若play页内联嵌入了该JSON）
        # 只取 url3；若 url3 本身是逗号分隔的多个候选地址（如 "url_a,url_b,url_c"），取第一个
        jm = re.search(r'\{"code"\s*:\s*0[^{}]*"data"\s*:\s*(\{[^{}]*\})\}', html.replace("\\/", "/"))
        if jm:
            try:
                data = json.loads(jm.group(1))
                url3 = data.get("url3", "")
                url = url3.split(",")[0].strip() if url3 else ""
            except Exception:
                url = ""
        if not url:
            for p in [r'var\s+player_\w*\s*=\s*(\{.*?\})\s*[<;]', r'"url"\s*:\s*"([^"]+)"', r'var\s+now\s*=\s*["\']([^"\']+)["\']', r'url:\s*["\']([^"\']+\.(?:m3u8|mp4)[^"\']*)["\']', r'(https?://[^\s"\'\\<>]+\.(?:m3u8|mp4)[^\s"\'\\<>]*)']:
                m = re.search(p, html.replace("\\/", "/"), re.S)
                if not m: continue
                val = m.group(1)
                if val.startswith("{"):
                    try:
                        val = json.loads(val).get("url", "")
                    except Exception:
                        m2 = re.search(r'"url"\s*:\s*"([^"]+)"', val)
                        val = m2.group(1).replace("\\/", "/") if m2 else ""
                if val: url = self._fix(val); break
        if not url: return {"parse": 1, "url": pid, "header": self.headers}
        return {"parse": 0, "url": url, "header": {"User-Agent": self.headers["User-Agent"], "Referer": self.host + "/"}}
