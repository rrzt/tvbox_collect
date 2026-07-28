# -*- coding: utf-8 -*-
"""
肉視頻 (rou.video) 爬虫 - 全面修复增强版
修复：视频列表多路提取（Next数据 / HTML卡片 / API接口），增强请求头与反爬策略
"""
import sys
import re
import json
import requests
import urllib3
import time
import random
import html as html_mod
from urllib.parse import quote, urljoin, unquote

urllib3.disable_warnings()
sys.path.append('..')
from base.spider import Spider as BaseSpider


class Spider(BaseSpider):
    host = 'https://rou.video'
    session = requests.Session()
    _debug = True
    _categories = []
    _home_data = None
    _home_html = ''

    AD_TITLE_FILTER = ['广告', '推广', '合作', 'APP', '下载', '注册', '菠菜', '博彩', '棋牌']
    AD_DOMAIN_FILTER = ['doubleclick', 'adservice', 'adsystem', 'adnxs', 'openx', 'casalemedia',
                        'googlesyndication', 'googleads', 'facebook.com/tr', 'statcounter']

    CDN_CANDIDATES = [
        'https://v.rn221.xyz',
        'https://v.rn222.xyz',
        'https://v.rn223.xyz',
        'https://v.rn224.xyz',
        'https://cdn.rou.video',
        'https://stream.rou.video',
        'https://media.rou.video',
        'https://video.rou.video',
        'https://play.rou.video',
        'https://storage.rou.video',
    ]

    def _log(self, msg):
        if self._debug:
            print(f'[rou] {msg}')

    def getName(self):
        return '肉視頻'

    def isVideoFormat(self, url):
        return url and any(ext in url for ext in ['.m3u8', '.mp4', '.ts', '.flv', '.mkv'])

    def manualVideoCheck(self):
        return False

    def destroy(self):
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except:
                pass
            self.session = None

    def localProxy(self, param):
        if not param or not param.startswith('http'):
            return [500, 'text/plain', '']
        try:
            r = self.session.get(param, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': self.host + '/'
            }, timeout=15, stream=True)
            if r.status_code != 200:
                return [r.status_code, 'text/plain', 'error']
            return [200, r.headers.get('Content-Type', 'image/jpeg'), r.content]
        except:
            return [500, 'text/plain', 'error']

    def _get_headers(self, referer=None):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': referer or self.host + '/',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }

    def _fetch(self, url, referer=None, retries=3, timeout=30):
        for attempt in range(retries):
            try:
                if attempt > 0:
                    time.sleep(random.uniform(1.0, 2.5))
                r = self.session.get(url, headers=self._get_headers(referer), timeout=timeout, verify=False)
                r.encoding = 'utf-8'
                if r.status_code == 200:
                    return r.text
                elif r.status_code in [403, 429, 503, 520]:
                    self._log(f'被拦截 [{r.status_code}] 重试 {attempt+1}/{retries}')
                    continue
                else:
                    self._log(f'HTTP {r.status_code} for {url}')
                    return ''
            except requests.exceptions.Timeout:
                self._log(f'超时重试 {attempt+1}/{retries}')
            except Exception as e:
                self._log(f'异常 {e} 重试 {attempt+1}/{retries}')
        return ''

    def _extract_next_data(self, html):
        if not html:
            return None
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass
        match = re.search(r'window\.__NEXT_DATA__\s*=\s*({.+?});?\s*</script>', html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass
        return None

    def _extract_json_ld(self, html):
        results = []
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
            try:
                results.append(json.loads(m.group(1)))
            except:
                pass
        return results

    # ========== 分类提取 ==========
    def _parse_categories_from_home(self, html):
        cats = []
        seen = set()
        # 策略1: 按钮 data-section
        pattern = r'<button[^>]*data-section="([^"]+)"[^>]*>([^<]+)</button>'
        for m in re.finditer(pattern, html):
            section_id = m.group(1)
            name = html_mod.unescape(m.group(2).strip())
            if section_id.startswith('section-') and name not in seen:
                seen.add(name)
                cats.append({'type_id': name, 'type_name': name, 'section': section_id})
        # 策略2: 导航链接 /t/xxx
        if not cats:
            for m in re.finditer(r'href=["\']/(?:t|category|tag)/([^"\'/]+)["\'][^>]*>([^<]+)</a>', html):
                tid = unquote(m.group(1))
                name = html_mod.unescape(m.group(2).strip())
                if name and tid and name not in seen and len(name) < 20:
                    seen.add(name)
                    cats.append({'type_id': tid, 'type_name': name})
        # 策略3: __NEXT_DATA__ 中的 nav/menu
        data = self._extract_next_data(html)
        if data:
            props = data.get('props', {}).get('pageProps', {})
            nav = props.get('nav') or props.get('menu') or props.get('categories') or props.get('tags')
            if isinstance(nav, list):
                for item in nav:
                    if isinstance(item, dict):
                        tid = item.get('id') or item.get('slug') or item.get('name')
                        name = item.get('name') or item.get('title') or tid
                        if tid and name and name not in seen:
                            seen.add(name)
                            cats.append({'type_id': str(tid), 'type_name': str(name)})
                    elif isinstance(item, str):
                        if item not in seen:
                            seen.add(item)
                            cats.append({'type_id': item, 'type_name': item})
        return cats

    def _get_fallback_categories(self):
        return [
            {'type_id': '国产AV', 'type_name': '国产AV'},
            {'type_id': '探花', 'type_name': '探花'},
            {'type_id': '自拍流出', 'type_name': '自拍流出'},
            {'type_id': 'OnlyFans', 'type_name': 'OnlyFans'},
            {'type_id': '日本', 'type_name': '日本'},
            {'type_id': '韩国', 'type_name': '韩国'},
            {'type_id': '欧美', 'type_name': '欧美'},
            {'type_id': '动漫', 'type_name': '动漫'},
            {'type_id': '麻豆', 'type_name': '麻豆'},
            {'type_id': 'JVID', 'type_name': 'JVID'},
            {'type_id': 'SWAG', 'type_name': 'SWAG'},
        ]

    def init(self, extend=''):
        self.session.headers.update(self._get_headers())
        self._home_html = self._fetch(self.host + '/home')
        if not self._home_html:
            self._home_html = self._fetch(self.host + '/')
        self._log(f'首页HTML长度: {len(self._home_html) if self._home_html else 0}')
        if self._home_html:
            if 'video' not in self._home_html.lower():
                self._log('警告：首页HTML中未发现视频关键词，可能被反爬或需JS渲染')
            self._home_data = self._extract_next_data(self._home_html)
            self._categories = self._parse_categories_from_home(self._home_html)
            if not self._categories:
                self._categories = self._get_fallback_categories()
            self._log(f'分类加载完成，共 {len(self._categories)} 个')
        else:
            self._categories = self._get_fallback_categories()
            self._log('首页获取失败，使用硬编码分类')

    # ========== 视频列表转换 ==========
    def _convert_video_items(self, items):
        result = []
        if not items:
            return result
        for item in items:
            if isinstance(item, dict):
                vid = item.get('id') or item.get('vid') or item.get('_id') or item.get('slug')
                if not vid:
                    continue
                name = item.get('name') or item.get('nameZh') or item.get('title') or str(vid)
                pic = item.get('coverImageUrl') or item.get('cover') or item.get('thumb') or item.get('poster') or ''
                remark = ''
                dur = item.get('duration') or item.get('video_duration')
                if dur:
                    try:
                        seconds = int(float(dur))
                        mins = seconds // 60
                        secs = seconds % 60
                        remark = f'{mins}分{secs}秒' if mins > 0 else f'{secs}秒'
                    except:
                        remark = str(dur)
                if any(ad in name for ad in self.AD_TITLE_FILTER):
                    continue
                result.append({
                    'vod_id': str(vid),
                    'vod_name': name,
                    'vod_pic': pic,
                    'vod_remarks': remark
                })
        return result

    # ========== 增强的 HTML 卡片解析 ==========
    def _parse_video_cards_from_html(self, html):
        items = []
        seen = set()

        # 1. JSON-LD 结构化数据
        json_ld = self._extract_json_ld(html)
        for ld in json_ld:
            if isinstance(ld, dict) and ld.get('@type') == 'VideoObject':
                vid = ld.get('@id') or ld.get('url', '').rstrip('/').split('/')[-1]
                name = ld.get('name', vid)
                pic = ld.get('thumbnailUrl', '')
                if vid and vid not in seen:
                    seen.add(vid)
                    items.append({'vod_id': vid, 'vod_name': name, 'vod_pic': pic, 'vod_remarks': ''})

        # 2. 通用卡片匹配：a标签包含 /v/xxx，内部有 img 和标题
        pattern = re.compile(
            r'<a[^>]+href=["\']/(?:v|video|watch)/([^"\'/]+)["\'][^>]*>.*?'
            r'(?:<img[^>]+src=["\']([^"\']+)["\'])?'
            r'.*?(?:<[^>]*>([^<]{2,50})</[^>]*>).*?</a>',
            re.DOTALL | re.IGNORECASE
        )
        for m in pattern.finditer(html):
            vid, pic, name = m.group(1), m.group(2) or '', m.group(3) or ''
            name = re.sub(r'<[^>]+>', '', name).strip()
            if vid and vid not in seen and len(name) > 0:
                seen.add(vid)
                items.append({'vod_id': vid, 'vod_name': name, 'vod_pic': pic, 'vod_remarks': ''})

        # 3. 常见卡片结构：<div class="video-item" ...>
        cards = re.findall(r'<div[^>]*class="[^"]*(?:video|item|card|post)[^"]*"[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL)
        for card in cards:
            vid_m = re.search(r'href=["\']/(?:v|video|watch)/([^"\'/]+)["\']', card)
            pic_m = re.search(r'(?:src|data-src)=["\']([^"\']+)["\']', card)
            name_m = re.search(r'(?:alt|title)=["\']([^"\']+)["\']', card) or re.search(r'<h[1-6][^>]*>([^<]+)</h', card)
            if vid_m and vid_m.group(1) not in seen:
                vid = vid_m.group(1)
                seen.add(vid)
                items.append({
                    'vod_id': vid,
                    'vod_name': name_m.group(1).strip() if name_m else vid,
                    'vod_pic': pic_m.group(1) if pic_m else '',
                    'vod_remarks': ''
                })
        return items

    def _get_video_list_from_data(self, data_key, limit=None):
        if not self._home_data:
            return []
        props = self._home_data.get('props', {}).get('pageProps', {})
        items = props.get(data_key)
        if items is None:
            for key in ['data', 'result', 'results', 'list', 'items', 'videos']:
                if isinstance(props.get(key), list):
                    items = props[key]
                    break
        if not isinstance(items, list):
            return []
        if limit:
            items = items[:limit]
        return self._convert_video_items(items)

    # ========== 新增：API 获取首页视频 ==========
    def _get_home_videos_api(self):
        """尝试直接请求API获取首页视频"""
        api_urls = [
            f'{self.host}/api/home',
            f'{self.host}/api/videos?page=1',
            f'{self.host}/api/index',
            f'{self.host}/api/latest',
        ]
        for api in api_urls:
            resp = self._fetch(api, timeout=10)
            if resp:
                try:
                    data = json.loads(resp)
                    videos = []
                    if isinstance(data, dict):
                        videos = data.get('data') or data.get('list') or data.get('videos') or []
                    elif isinstance(data, list):
                        videos = data
                    if videos:
                        return self._convert_video_items(videos)
                except:
                    pass
        return []

    # ========== 首页 ==========
    def homeContent(self, filter=False):
        try:
            if not self._home_data:
                self.init()
            cats = self._categories
            # 1. Next 数据
            items = self._get_video_list_from_data('latestVideos', limit=20)
            # 2. HTML 卡片解析
            if not items and self._home_html:
                items = self._parse_video_cards_from_html(self._home_html)[:20]
            # 3. API 尝试
            if not items:
                items = self._get_home_videos_api()
            return {'class': cats, 'list': items}
        except Exception as e:
            self._log(f'homeContent 异常: {e}')
            return {'class': self._categories or self._get_fallback_categories(), 'list': []}

    def homeVideoContent(self):
        items = self._get_video_list_from_data('latestVideos', limit=20)
        if not items and self._home_html:
            items = self._parse_video_cards_from_html(self._home_html)[:20]
        if not items:
            items = self._get_home_videos_api()
        return {'list': items}

    # ========== 分类页（增强 API 尝试） ==========
    def categoryContent(self, tid, pg, filter=False, extend=''):
        try:
            page = int(pg) if pg else 1
            cat_name = str(tid)
            # 优先尝试 API
            items = self._get_category_videos_api(cat_name, page)
            if not items:
                # 原有 HTML 解析逻辑
                url = f'{self.host}/t/{quote(cat_name)}'
                if page > 1:
                    url += f'?page={page}'
                html_text = self._fetch(url, referer=self.host)
                if not html_text:
                    return {'list': [], 'page': page, 'pagecount': 1}

                # Next 数据
                data = self._extract_next_data(html_text)
                if data:
                    props = data.get('props', {}).get('pageProps', {})
                    video_list = None
                    for key in ['videos', 'list', 'items', 'results', 'data', 'posts']:
                        if key in props and isinstance(props[key], list):
                            video_list = props[key]
                            break
                    if video_list:
                        items = self._convert_video_items(video_list)

                # HTML 卡片解析
                if not items:
                    items = self._parse_video_cards_from_html(html_text)

            # 分页简单判断
            total_pages = page + 1 if len(items) >= 24 else page
            return {'list': items, 'page': page, 'pagecount': total_pages}
        except Exception as e:
            self._log(f'categoryContent 异常: {e}')
            return {'list': [], 'page': int(pg) if pg else 1, 'pagecount': 1}

    def _get_category_videos_api(self, cat_name, page):
        """尝试从 API 获取分类视频"""
        api_urls = [
            f'{self.host}/api/t/{quote(cat_name)}?page={page}',
            f'{self.host}/api/category/{quote(cat_name)}?page={page}',
            f'{self.host}/api/videos?tag={quote(cat_name)}&page={page}',
            f'{self.host}/api/list?type={quote(cat_name)}&page={page}',
        ]
        for api in api_urls:
            resp = self._fetch(api, timeout=10)
            if resp:
                try:
                    data = json.loads(resp)
                    videos = []
                    if isinstance(data, dict):
                        videos = data.get('videos') or data.get('data') or data.get('list') or data.get('items') or []
                    elif isinstance(data, list):
                        videos = data
                    if videos:
                        return self._convert_video_items(videos)
                except:
                    pass
        return None

    # ========== 详情页（保持原有多路逻辑） ==========
    def detailContent(self, ids):
        try:
            vid = str(ids[0] if isinstance(ids, list) else ids)
            url = f'{self.host}/v/{vid}'
            html_text = self._fetch(url, referer=self.host)
            if not html_text:
                return {'list': [{'vod_id': vid, 'vod_name': '加载失败', 'vod_play_from': '错误', 'vod_play_url': ''}]}

            data = self._extract_next_data(html_text)
            video = None

            # 1. __NEXT_DATA__
            if data:
                props = data.get('props', {}).get('pageProps', {})
                video = props.get('video') or props.get('post') or props.get('item') or props.get('detail')

            # 2. 内联脚本 sources/video 对象
            if not video or not video.get('sources'):
                scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html_text)
                for sc in scripts:
                    # sources 数组
                    for pattern in [
                        r'["\']sources["\']\s*:\s*(\[[^\]]*\])',
                        r'var\s+sources\s*=\s*(\[[^\]]*\])',
                        r'let\s+sources\s*=\s*(\[[^\]]*\])',
                        r'const\s+sources\s*=\s*(\[[^\]]*\])',
                    ]:
                        match = re.search(pattern, sc)
                        if match:
                            try:
                                sources = json.loads(match.group(1))
                                if isinstance(sources, list) and sources:
                                    video = {'sources': sources}
                                    break
                            except:
                                continue
                    if video and video.get('sources'):
                        break

                    # 完整 video 对象
                    for pattern in [
                        r'["\']video["\']\s*:\s*(\{[^}]+\})',
                        r'var\s+video\s*=\s*(\{[^}]+\})',
                    ]:
                        match = re.search(pattern, sc)
                        if match:
                            try:
                                vobj = json.loads(match.group(1))
                                if vobj.get('sources') or vobj.get('playUrl'):
                                    video = vobj
                                    break
                            except:
                                continue
                    if video:
                        break

            # 3. API 尝试
            if not video or not video.get('sources'):
                api_urls = [
                    f'{self.host}/api/video?id={vid}',
                    f'{self.host}/api/play?id={vid}',
                    f'{self.host}/api/getVideo?vid={vid}',
                    f'{self.host}/api/v1/video/{vid}',
                    f'{self.host}/api/video/{vid}',
                    f'{self.host}/api/detail?id={vid}',
                ]
                for api in api_urls:
                    api_resp = self._fetch(api, referer=url, timeout=10)
                    if api_resp:
                        try:
                            api_data = json.loads(api_resp)
                            sources = None
                            if isinstance(api_data, dict):
                                sources = api_data.get('sources')
                                if not sources and 'data' in api_data:
                                    sources = api_data['data'].get('sources') if isinstance(api_data['data'], dict) else None
                                if not sources and 'result' in api_data:
                                    sources = api_data['result'].get('sources') if isinstance(api_data['result'], dict) else None
                                if not sources:
                                    vobj = api_data.get('video') or api_data.get('data', {}).get('video') if isinstance(api_data.get('data'), dict) else None
                                    if vobj:
                                        video = vobj
                                        break
                            if sources:
                                video = {'sources': sources}
                                break
                        except:
                            continue

            title = ''
            pic = ''
            if video and isinstance(video, dict):
                title = video.get('name') or video.get('nameZh') or video.get('title') or vid
                pic = video.get('coverImageUrl') or video.get('cover') or video.get('poster') or ''
            else:
                title = vid
                tmatch = re.search(r'<h1[^>]*>([^<]+)</h1>', html_text) or re.search(r'<title>([^<]+)</title>', html_text)
                if tmatch:
                    title = html_mod.unescape(tmatch.group(1).strip().replace(' - 肉視頻', '').replace(' - rou.video', ''))

            m3u8_urls = []

            # 4. 从 sources 构造
            if video and isinstance(video, dict):
                sources = video.get('sources', [])
                if sources:
                    best = None
                    try:
                        best = max(sources, key=lambda s: int(s.get('resolution', 0) or s.get('height', 0) or 0))
                    except:
                        best = sources[0] if sources else None
                    if best:
                        folder = best.get('folder', '')
                        file_path = best.get('file') or best.get('path', '')
                        if folder:
                            for base in self.CDN_CANDIDATES:
                                m3u8_urls.append(f'{base}/m/{folder}/index.m3u8')
                                m3u8_urls.append(f'{base}/{folder}/index.m3u8')
                                m3u8_urls.append(f'{base}/hls/{folder}/index.m3u8')
                        if file_path:
                            for base in self.CDN_CANDIDATES:
                                if not file_path.startswith('http'):
                                    m3u8_urls.append(f'{base}/{file_path}')
                                else:
                                    m3u8_urls.append(file_path)
                    for s in sources:
                        direct = s.get('url') or s.get('src') or s.get('path') or s.get('file') or s.get('m3u8')
                        if direct:
                            if not direct.startswith('http'):
                                direct = urljoin(self.host, direct)
                            if direct not in m3u8_urls:
                                m3u8_urls.insert(0, direct)

                for key in ['playUrl', 'play_url', 'streamUrl', 'videoUrl', 'm3u8']:
                    play_url = video.get(key)
                    if play_url:
                        if not play_url.startswith('http'):
                            play_url = urljoin(self.host, play_url)
                        if play_url not in m3u8_urls:
                            m3u8_urls.insert(0, play_url)
                        break

            # 5. HTML 内嵌 m3u8/mp4
            direct_abs = re.findall(r'(https?://[^\s"\'<>]+\.(?:m3u8|mp4)[^\s"\'<>]*)', html_text)
            for u in direct_abs:
                if u not in m3u8_urls:
                    m3u8_urls.append(u)
            direct_rel = re.findall(r'["\'](/(?:[^\s"\'<>]+\.(?:m3u8|mp4))[^\s"\'<>]*)["\']', html_text)
            for u in direct_rel:
                full = urljoin(self.host, u)
                if full not in m3u8_urls:
                    m3u8_urls.append(full)

            # 6. <video>/<source> 标签
            for tag in re.findall(r'<(?:video|source)[^>]+src=["\']([^"\']+)["\']', html_text):
                if not tag.startswith('http'):
                    tag = urljoin(self.host, tag)
                if tag not in m3u8_urls:
                    m3u8_urls.append(tag)

            # 7. iframe
            iframe_srcs = re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', html_text)
            for iframe_url in iframe_srcs:
                if iframe_url.startswith('//'):
                    iframe_url = 'https:' + iframe_url
                elif not iframe_url.startswith('http'):
                    iframe_url = urljoin(self.host, iframe_url)
                if any(domain in iframe_url for domain in ['player', 'play', 'embed', 'video']):
                    if iframe_url not in m3u8_urls:
                        m3u8_urls.append(iframe_url)

            # 8. 外部 JS
            js_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html_text)
            for js_url in js_srcs:
                if not js_url.startswith('http'):
                    js_url = urljoin(self.host, js_url)
                if any(lib in js_url for lib in ['jquery', 'bootstrap', 'lodash', 'react', 'vue', 'next']):
                    continue
                js_content = self._fetch(js_url, referer=url, timeout=10)
                if js_content:
                    js_matches = re.findall(r'["\']((?:https?:)?//[^"\']+\.(?:m3u8|mp4)[^"\']*)', js_content)
                    for m in js_matches:
                        if m.startswith('//'):
                            m = 'https:' + m
                        if m not in m3u8_urls:
                            m3u8_urls.append(m)
                    rel_js_matches = re.findall(r'["\'](/(?:[^"\']+\.(?:m3u8|mp4))["\']', js_content)
                    for m in rel_js_matches:
                        full = urljoin(self.host, m)
                        if full not in m3u8_urls:
                            m3u8_urls.append(full)

            # 去重过滤
            seen = set()
            clean = []
            for u in m3u8_urls:
                u = u.replace('\\/', '/').strip()
                if not u.startswith('http'):
                    continue
                if any(ad in u.lower() for ad in self.AD_DOMAIN_FILTER):
                    continue
                if u not in seen:
                    seen.add(u)
                    clean.append(u)

            if not clean:
                return {'list': [{'vod_id': vid, 'vod_name': title, 'vod_pic': pic,
                                  'vod_play_from': '播放', 'vod_play_url': f'播放${url}'}]}

            lines = []
            for idx, addr in enumerate(clean):
                line_name = f'线路{idx+1}'
                if 'iframe' in addr or 'embed' in addr:
                    line_name += '(外链)'
                lines.append(f'{line_name}${addr}')

            play_from = '#'.join(lines)
            play_url = '#'.join(lines)

            return {'list': [{
                'vod_id': vid,
                'vod_name': title,
                'vod_pic': pic,
                'vod_play_from': play_from,
                'vod_play_url': play_url
            }]}
        except Exception as e:
            self._log(f'detailContent 异常: {e}')
            return {'list': [{'vod_id': str(ids[0]), 'vod_name': '错误', 'vod_play_from': '错误', 'vod_play_url': ''}]}

    def playerContent(self, flag, id, vipFlags=None):
        if any(ad in id.lower() for ad in self.AD_DOMAIN_FILTER):
            return {'parse': 0, 'url': '', 'header': {}}
        parse_flag = 1 if ('iframe' in id or 'embed' in id or 'player' in id) else 0
        return {
            'parse': parse_flag,
            'url': id,
            'header': {
                'Referer': self.host,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Origin': self.host,
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        }

    def searchContent(self, key, quick, pg='1'):
        try:
            page = int(pg) if pg else 1
            url = f'{self.host}/search?keyword={quote(key)}&page={page}'
            html_text = self._fetch(url, referer=self.host)
            items = []
            if html_text:
                data = self._extract_next_data(html_text)
                if data:
                    props = data.get('props', {}).get('pageProps', {})
                    results = props.get('results') or props.get('videos') or props.get('list') or props.get('items')
                    if results:
                        items = self._convert_video_items(results)
                if not items:
                    items = self._parse_video_cards_from_html(html_text)
            return {'list': items, 'page': page, 'pagecount': page + 1}
        except Exception as e:
            self._log(f'searchContent 异常: {e}')
            return {'list': [], 'page': 1, 'pagecount': 1}