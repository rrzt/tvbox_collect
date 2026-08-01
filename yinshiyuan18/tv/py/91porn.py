# coding: utf-8
import re
import sys
import urllib.parse
import requests
import json
from pyquery import PyQuery as pq
import time

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        self.name = '91pron'
        self.host = 'https://0708.fs708.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 15; 2407FRK8EC Build/AP3A.240617.008; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36',
            'Origin': self.host.rstrip('/'),
            'Referer': self.host,
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.cookies = {'language': 'cn_CN', 'over18': '1'}
        self.class_map = {
            '最新': 'watch',
            '91原创': 'ori',
            '当前最热': 'hot',
            '本月最热': 'top',
            '10分钟以上': 'long',
            '20分钟以上': 'longer',
            '本月收藏': 'tf',
            '最近加精': 'rf',
            '高清': 'hd',
            '每月最热': 'top_m',  # 优化：转换为内部标识，在 categoryContent 中独立处理参数
            '本月讨论': 'md',
            '收藏最多': 'mf'
        }

    def getName(self):
        return self.name

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        return any(ext in (url or '') for ext in ['.m3u8', '.mp4', '.ts'])

    def manualVideoCheck(self):
        return False

    def _abs_href(self, href):
        if not href:
            return ''
        if href.startswith('http'):
            return href
        return f"{self.host.rstrip('/')}/{href.lstrip('/')}"

    def _parse_video_items(self, data):
        vlist = []
        # 优化：放宽选择器，兼容各种响应式网格及卡片容器
        for item in data('.well.well-sm.videos-text-align, div[class*="col-xs-12"][class*="col-sm"]').items():
            try:
                title_elem = item('span[class="video-title title-truncate m-t-5"], .video-title')
                title = title_elem.text().strip()
                if not title:
                    continue
                pic_elem = item('img')
                pic = pic_elem.attr('src') or pic_elem.attr('data-original') or ''
                pic = self._abs_href(pic) if pic else ''
                
                a_elem = item('a')
                href = self._abs_href(a_elem.attr('href'))
                
                duration = item('.duration').text().strip() or '未知'
                
                if href:
                    # 去重处理，避免响应式导致同一视频重复抓取
                    if not any(v['vod_id'] == href for v in vlist):
                        vlist.append({
                            'vod_id': href,
                            'vod_name': title,
                            'vod_pic': pic,
                            'vod_remarks': duration
                        })
            except:
                continue
        return vlist

    def _parse_pagecount(self, data):
        try:
            nums = [int(m.group(1)) for a in data('a').items() 
                    if (m := re.search(r'[?&]page=(\d+)', a.attr('href') or ''))]
            if nums:
                return max(nums)
            page_nums = [int(a.text().strip()) 
                         for a in data('.pagination li a, .pagingnav a').items() 
                         if a.text().strip().isdigit()]
            return max(page_nums) if page_nums else 1
        except:
            return 1

    def homeContent(self, filter):
        result = {'class': [{'type_name': k, 'type_id': v} for k, v in self.class_map.items()]}
        try:
            html = self._fetch(f"{self.host}index.php").text
            result['list'] = self._parse_video_items(pq(html))
        except:
            result['list'] = []
        return result

    def homeVideoContent(self):
        return []

    def categoryContent(self, tid, pg, filter, extend):
        pg = int(pg or 1)
        try:
            # 优化：处理带特殊参数的分类（如每月最热需要 &m=-1）
            if tid == 'top_m':
                url = f"{self.host}v.php?category=top&m=-1&viewtype=basic&page={pg}"
            else:
                url = f"{self.host}v.php?category={tid}&viewtype=basic&page={pg}"
                
            html = self._fetch(url).text
            data = pq(html)
            return {
                'list': self._parse_video_items(data),
                'page': pg,
                'pagecount': self._parse_pagecount(data),
                'limit': 24,
                'total': 999999
            }
        except:
            return {'list': [], 'page': pg, 'pagecount': 1, 'limit': 0, 'total': 0}

    def _extract_vid(self, text):
        patterns = [
            r'viewkey=([a-zA-Z0-9]+)',
            r'/viewvideo\.php\?.*viewkey=([a-zA-Z0-9]+)',
            r'VID["\']?\s*[:=]\s*["\']?([a-zA-Z0-9]+)',
            r'/ev\.php\?VID=([a-zA-Z0-9]+)'
        ]
        for pattern in patterns:
            if m := re.search(pattern, text):
                return m.group(1)
        return None

    def _get_ev_url(self, html, detail_url):
        if m := re.search(r'<textarea[^>]*>\s*(https?://[^<]+/ev\.php\?VID=[^<\s]+)', html, re.I):
            return m.group(1).strip()
        if matches := re.findall(r'(https?://[^"\'\s<>]+/ev\.php\?VID=[a-zA-Z0-9]+)', html, re.I):
            return matches[0]
        if vid := self._extract_vid(html) or self._extract_vid(detail_url):
            return f"{self.host}ev.php?VID={vid}"
        return None

    def _get_mp4_url(self, ev_url):
        try:
            resp = self._fetch(ev_url, headers={**self.headers, 'Referer': self.host}, timeout=10)
            if resp.status_code != 200:
                return None
            html = resp.text
            if m := re.search(r'<source\s+src="([^"]+)"\s+type="video/mp4"', html, re.I):
                return m.group(1).strip().replace('&amp;', '&')
            if matches := re.findall(r'https?://[^"\'\s<>]*cdn77[^"\'\s<>]*\.mp4\?secure=[^"\'\s<>&]+', html):
                return matches[0].replace('&amp;', '&')
            if all_mp4 := re.findall(r'https?://[^"\'\s<>]+\.mp4[^"\'\s<>]*', html):
                for url in sorted(all_mp4, key=len, reverse=True):
                    if 'cdn77' in url and 'secure=' in url and len(url) > 150:
                        return url.replace('&amp;', '&')
                for url in all_mp4:
                    if 'cdn77' in url and len(url) > 100:
                        return url.replace('&amp;', '&')
            if m_src := re.search(r'src\s*:\s*["\'](https?://[^"\']+\.mp4[^"\']*)["\']', html, re.I):
                return m_src.group(1).replace('&amp;', '&')
            return None
        except:
            return None

    def detailContent(self, ids):
        if not ids or not ids[0]:
            return {'list': []}
        vod_id = ids[0].strip()
        detail_url = vod_id if vod_id.startswith('http') else f"{self.host.rstrip('/')}/{vod_id.lstrip('/')}"
        try:
            html = self._fetch(detail_url).text
        except:
            return {'list': []}
        
        ev_url = self._get_ev_url(html, detail_url)
        mp4_url = self._get_mp4_url(ev_url) if ev_url else None
        video_url = mp4_url if (mp4_url and 'secure=' in mp4_url) else (ev_url or detail_url)
        
        data = pq(html)
        title = data('title').text().strip().split('Chinese homemade video')[0].strip() or '未知标题'
        pic = (data('meta[property="og:image"]').attr('content') or
               data('.video-pic img, img.img-responsive').attr('src') or '')
        pic = self._abs_href(pic) if pic else ''
        
        director = '飞鱼'
        views = '未知'
        duration = '未知'
        
        # 优化：通过正则直接在整页匹配时长与热度，防止因为容器类名变动而失效
        if m_dur := re.search(r'\d{2}:\d{2}:\d{2}|\d{2}:\d{2}', html):
            duration = m_dur.group(0)
            
        main_box = data('div[class*="col-md-8"], .col-xs-12')
        for span in main_box.find('span.info').items():
            txt = span.text()
            if '热度' in txt or '观看' in txt:
                if m := re.search(r'[\d]+', span.parent().text().strip()):
                    views = m.group(0)

        remarks = f"{duration} | 观看:{views}" if views != '未知' else duration
        
        return {'list': [{
            'vod_id': vod_id,
            'vod_name': title,
            'vod_pic': pic,
            'vod_play_from': '飞鱼',
            'vod_play_url': f'高清${video_url}',
            'vod_director': director,
            'vod_remarks': remarks,
            'vod_content': title
        }]}

    def searchContent(self, key, quick, pg=1):
        pg = int(pg or 1)
        if not key or not key.strip():
            return {'list': [], 'page': pg, 'pagecount': 1, 'limit': 0, 'total': 0}
        try:
            encoded_key = urllib.parse.quote(key.strip())
            url = f"{self.host}search_result.php?search_id={encoded_key}&search_type=search_videos&min_duration=&page={pg}"
            
            html = self._fetch(url).text
            data = pq(html)
            vlist = self._parse_video_items(data)
            
            if not vlist:
                return {'list': [], 'page': pg, 'pagecount': 1, 'limit': 0, 'total': 0}
                
            return {
                'list': vlist,
                'page': pg,
                'pagecount': self._parse_pagecount(data) or (pg + 1),
                'limit': len(vlist),
                'total': 999999
            }
        except:
            return {'list': [], 'page': pg, 'pagecount': 1, 'limit': 0, 'total': 0}

    def playerContent(self, flag, id, vipFlags):
        parsed = urllib.parse.urlparse(id if id.startswith('http') else self.host)
        headers = {
            **self.headers,
            'Origin': f"{parsed.scheme}://{parsed.netloc}",
            'Referer': self.host
        }
        return {
            'parse': 0 if self.isVideoFormat(id) else 1,
            'url': id,
            'header': headers
        }

    def localProxy(self, param):
        return [404, 'text/plain', '']

    def _fetch(self, url, params=None, headers=None, timeout=15):
        for i in range(2):
            try:
                resp = requests.get(
                    url,
                    headers=headers or self.headers,
                    cookies=self.cookies,
                    timeout=timeout,
                    allow_redirects=True,
                    params=params or {},
                    verify=False
                )
                if resp.status_code in (200, 301, 302):
                    resp.encoding = resp.apparent_encoding or 'utf-8'
                    return resp
            except:
                if i < 1:
                    time.sleep(0.5)
        return type('obj', (object,), {
            'text': '', 'status_code': 404, 'headers': {},
            'content': b'', 'url': url, 'json': lambda: {}
        })()
