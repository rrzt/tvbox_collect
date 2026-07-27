# coding=utf-8
# fmt: off
# type: ignore
"""
91porna 影视源 (drpy/TVBox 格式)

说明:
  1. 适用于 drpy / TVBox 的 Python 爬虫源
  2. 包含首页分类、分类列表分页、视频详情解析以及播放地址提取
  3. 内置多重请求后备方案（requests / requests(verify=False) / urllib）
"""

import re
import json
import urllib.parse
import urllib.request

# ======================== 配置 ========================

BASE_URL = "https://91porna.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

HEADERS = {
    "User-Agent": UA,
    "Referer": BASE_URL + "/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 分类配置 (可根据 91porna 实际导航栏进行调整)
CATEGORIES = [
    {"name": "最近更新", "tid": "latest"},
    {"name": "最多浏览", "tid": "viewed"},
    {"name": "最多收藏", "tid": "favorite"},
    {"name": "长视频", "tid": "long"},
    {"name": "高清", "tid": "hd"},
]


# ======================== 工具函数 ========================

def _fetch(url, timeout=15):
    """发起 HTTP GET 请求 - 优先 requests, 失败则用 urllib 后备"""
    # 方式1: requests (verify=True)
    try:
        import requests
        resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=True, allow_redirects=True)
        resp.encoding = 'utf-8'
        if resp.text and len(resp.text) > 50:
            return resp.text
    except Exception:
        pass

    # 方式2: requests (verify=False, SSL 宽松)
    try:
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=False, allow_redirects=True)
        resp.encoding = 'utf-8'
        if resp.text and len(resp.text) > 50:
            return resp.text
    except Exception:
        pass

    # 方式3: urllib 后备
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read()
            for enc in ['utf-8', 'gbk', 'latin-1']:
                try:
                    return data.decode(enc)
                except Exception:
                    continue
    except Exception:
        pass

    return ""


def _parse_video_items(html):
    """从 HTML 中解析视频列表项"""
    videos = []
    
    # 适配常见结构：匹配带链接、标题、封面及时长/备注的视频卡片
    item_pattern = re.compile(
        r'<div[^>]*class="[^"]*well[^"]*"[^>]*>.*?'
        r'href="([^"]*view_video\.php\?[^"]+)"[^>]*>.*?'
        r'src="([^"]*)"[^>]*title="([^"]*)"',
        re.DOTALL
    )
    
    matches = item_pattern.findall(html)
    for href, cover, title in matches:
        # 提取视频唯一标识（如 view_video.php?viewkey=xxxx）
        parsed_url = urllib.parse.urlparse(href)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        viewkey = query_params.get("viewkey", [""])[0]
        
        if not viewkey:
            # 备用：直接正则提取 viewkey
            vk_match = re.search(r'viewkey=([a-zA-Z0-9]+)', href)
            if vk_match:
                viewkey = vk_match.group(1)
        
        if not viewkey:
            continue
            
        videos.append({
            "vod_id": viewkey,
            "vod_name": title.strip(),
            "vod_pic": cover.strip(),
            "vod_remarks": "",
        })
        
    # 如果标准 well 没匹配到，尝试通用列表正则后备
    if not videos:
        general_pattern = re.compile(
            r'<a[^>]*href="([^"]*view_video\.php\?viewkey=[^"]+)"[^>]*>.*?'
            r'(?:src="([^"]*)"|data-src="([^"]*)").*?'
            r'title="([^"]*)"',
            re.DOTALL
        )
        seen = set()
        for href, src1, src2, title in general_pattern.findall(html):
            cover = src1 or src2 or ""
            vk_match = re.search(r'viewkey=([a-zA-Z0-9]+)', href)
            if not vk_match:
                continue
            viewkey = vk_match.group(1)
            if viewkey in seen:
                continue
            seen.add(viewkey)
            
            videos.append({
                "vod_id": viewkey,
                "vod_name": title.strip(),
                "vod_pic": cover.strip(),
                "vod_remarks": "",
            })
            
    return videos


def _build_list_url(tid, pg):
    """根据分类和页码构建列表 URL"""
    page_str = f"&page={pg}" if pg > 1 else ""
    
    if tid == "latest":
        return f"{BASE_URL}/index.php?c=index&a=idx{page_str}"
    elif tid == "viewed":
        return f"{BASE_URL}/v.php?category=top&viewtype=basic{page_str}"
    elif tid == "favorite":
        return f"{BASE_URL}/v.php?category=most_favour&viewtype=basic{page_str}"
    elif tid == "long":
        return f"{BASE_URL}/v.php?category=long&viewtype=basic{page_str}"
    elif tid == "hd":
        return f"{BASE_URL}/v.php?category=hd&viewtype=basic{page_str}"
    else:
        return f"{BASE_URL}/v.php?category={tid}&viewtype=basic{page_str}"


# ======================== Spider 类 ========================

class Spider:
    
    def init(self, extend=""):
        self.extend = extend
        return ""
    
    def getName(self):
        return "91porna"
    
    def isVideoFormat(self, url):
        return False
    
    def manualVideoCheck(self):
        return False
    
    def homeContent(self, filter):
        classes = []
        for cat in CATEGORIES:
            classes.append({"type_name": cat["name"], "type_id": cat["tid"]})
        
        result = {"class": classes, "list": []}
        try:
            html = _fetch(f"{BASE_URL}/")
            result["list"] = _parse_video_items(html)
        except Exception:
            pass
        return result
    
    def homeVideoContent(self):
        try:
            html = _fetch(f"{BASE_URL}/")
            return {"list": _parse_video_items(html)}
        except Exception:
            return {"list": []}
    
    def categoryContent(self, tid, pg, filter, extend):
        page = int(pg) if pg else 1
        result = {
            "list": [],
            "page": page,
            "pagecount": 999,
            "limit": 20,
            "total": 999,
        }
        
        try:
            target_url = _build_list_url(tid, page)
            html = _fetch(target_url)
            result["list"] = _parse_video_items(html)
            if not result["list"]:
                result["pagecount"] = page - 1
        except Exception:
            pass
        
        return result
    
    def detailContent(self, ids):
        viewkey = ids[0] if ids else ""
        result = {
            "list": [{
                "vod_id": viewkey,
                "vod_name": viewkey,
                "vod_pic": "",
                "vod_play_from": "91porna",
                "vod_play_url": "",
            }]
        }
        
        try:
            detail_url = f"{BASE_URL}/view_video.php?viewkey={viewkey}"
            html = _fetch(detail_url)
            
            if html and len(html) > 100:
                # 提取标题
                title_match = re.search(r'<h4[^>]*class="[^"]*text-muted[^"]*"[^>]*>([^<]+)</h4>|<title>([^<]+)</title>', html)
                title = ""
                if title_match:
                    title = (title_match.group(1) or title_match.group(2) or "").strip()
                    title = title.replace("- 91porna", "").strip()
                if not title:
                    title = viewkey
                
                # 提取封面
                cover_match = re.search(r'poster="([^"]+)"|src="([^"]+\.(?:jpg|png))"', html)
                cover = ""
                if cover_match:
                    cover = cover_match.group(1) or cover_match.group(2) or ""
                
                # 提取视频直链或 m3u8 地址
                play_url = ""
                src_match = re.search(r'<source\s+src="([^"]+)"', html)
                if src_match:
                    play_url = src_match.group(1)
                else:
                    # 尝试从 js 变量中提取视频地址
                    js_src = re.search(r'video_url\s*=\s*["\']([^"\']+)["\']', html)
                    if js_src:
                        play_url = js_src.group(1)
                
                result["list"][0]["vod_name"] = title
                result["list"][0]["vod_pic"] = cover
                result["list"][0]["vod_play_from"] = "91porna"
                result["list"][0]["vod_play_url"] = f"播放${play_url}" if play_url else f"播放$https://91porna.com/view_video.php?viewkey={viewkey}"
            else:
                result["list"][0]["vod_play_url"] = f"播放$https://91porna.com/view_video.php?viewkey={viewkey}"
        except Exception:
            pass
            
        return result
    
    def searchContent(self, key, quick):
        result = {"list": []}
        try:
            search_url = f"{BASE_URL}/search.php?search_type=videos&search_query={urllib.parse.quote(key)}"
            html = _fetch(search_url)
            if html:
                result["list"] = _parse_video_items(html)
        except Exception:
            pass
        return result
    
    def playerContent(self, flag, id, vipFlags):
        return {
            "parse": 0,
            "playUrl": "",
            "url": id,
            "header": json.dumps({
                "User-Agent": UA,
                "Referer": BASE_URL + "/",
            }),
        }
    
    def localProxy(self, param):
        return {}
    
    def destroy(self):
        return ""
