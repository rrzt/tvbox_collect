# coding=utf-8
#!/usr/bin/python
import sys, re, base64, json, requests, time, threading, random
from base.spider import Spider
from datetime import datetime, timedelta
from urllib.parse import quote, urlparse
from urllib3.util.retry import Retry
sys.path.append('..')

class Spider(Spider):
    def init(self, extend="{}"):
        origin = 'https://zh.stripchat.com'
        self.host = origin
        self.Doppiocdn = "doppiocdn.org"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:153.0) Gecko/20100101 Firefox/153.0"
        self.headers = {'Origin': origin, 'Referer': f"{origin}/", 'User-Agent': user_agent, "Accept-Language": "zh,en;q=0.5"}
        self.stripchat_preferredVideoCodec = "H265"
        self.stripchat_key = "YzWScuyQRGAGcxx1KIJmiQ7BY9Vi35ftwLqUOVO8uoo="
        self.stripchat_pkey = "Fq6m2TO2ZeBkRPm9"
        self.stripchat_play='0 0'
        self.search_headers = self.headers.copy()
        self.danmu_cache = {}
        self.danmu_seen = {}
        self.danmu_threads = {}
        self.danmu_lock = threading.Lock()
        self.danmu_refreshed = set()
        self.danmu_refresh_ts = {}
        self.create_session_with_retry()

    def getName(self): return "StripChat弹幕版"
    def isVideoFormat(self, url): pass
    def manualVideoCheck(self): pass
    def destroy(self): pass
    def homeVideoContent(self): pass
    def normalize_username_for_hdstream(self, username): return username.replace('-', '_').lower()

    def homeContent(self, filter):
        CLASSES = [{'type_name': '女主播g', 'type_id': 'girls'}, {'type_name': '情侣c', 'type_id': 'couples'}, {'type_name': '男主播m', 'type_id': 'men'}, {'type_name': '跨性别t', 'type_id': 'trans'}]
        VALUE = [{'n': '中国', 'v': 'tagLanguageChinese'}, {'n': '亚洲', 'v': 'ethnicityAsian'}, {'n': '白人', 'v': 'ethnicityWhite'}, {'n': '拉丁', 'v': 'ethnicityLatino'}, {'n': '混血', 'v': 'ethnicityMultiracial'}, {'n': '印度', 'v': 'ethnicityIndian'}, {'n': '阿拉伯', 'v': 'ethnicityMiddleEastern'}, {'n': '黑人', 'v': 'ethnicityEbony'}]
        VALUE_MEN = [{'n': '情侣', 'v': 'sexGayCouples'}, {'n': '直男', 'v': 'orientationStraight'}]
        TIDS = ('girls', 'couples', 'men', 'trans')
        filters = {tid: [{'key': 'tag', 'value': VALUE_MEN + VALUE if tid == 'men' else VALUE}] for tid in TIDS}
        return {'class': CLASSES, 'filters': filters}

    def categoryContent(self, tid, pg, filter, extend):
        limit = 60
        offset = limit * (int(pg) - 1)
        url = f"{self.host}/api/front/models?improveTs=false&removeShows=false&limit={limit}&offset={offset}&primaryTag={tid}&sortBy=stripRanking&rcmGrp=A&rbCnGr=true&prxCnGr=false&nic=false"
        if isinstance(extend, dict) and 'tag' in extend: url += f'&filterGroupTags=[["{extend["tag"]}"]]'
        rsp = self.session_get(url).json()
        videos = [{"vod_id": str(v['username']), "vod_name": f"{self.country_code_to_flag(str(v['country']))}{v['username']}", "vod_pic": f"https://img.{self.Doppiocdn}/snapshot/{v['id']}/{v['snapshotTimestamp']}", "vod_remarks": "" if v.get('status') == "public" else "🎫"} for v in rsp.get('models', [])]
        total = int(rsp.get('filteredCount', 0))
        return {"list": videos, "page": pg, "pagecount": (total + limit - 1) // limit, "limit": limit, "total": total}

    def detailContent(self, array):
        username = array[0]
        try:
            rsp = self.session_get(f"{self.host}/api/front/v2/models/username/{username}/cam").json()
            info, user = rsp['cam'], rsp['user']['user']
            uid, isLive = str(user['id']), user['isLive']
            oldName = self.stripchat_play.rsplit(' ', 1)[-1]
            if username != oldName:
                timestp = int(time.time())
                self.stripchat_play = f"0 {timestp} {username}"
            flag = self.country_code_to_flag(str(user['country']).strip())
            remark = "🔴 直播中" if isLive else "⚫ 已下播"
            show = info.get('show') or info.get('groupShowAnnouncement')
            if show:
                startAt = show.get('createdAt') or show.get('startAt')
                if startAt: remark = f"🎫 始于 {(datetime.strptime(startAt, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=8)).strftime('%m月%d日 %H:%M')}"
            director = f"{flag}{username}"
            return {'list': [{"vod_id": username, "vod_name": str(info.get('topic') or username)[:80], "vod_pic": str(user.get('avatarUrl') or ''), "vod_director": director, "vod_remarks": remark, 'vod_play_from': 'StripChat$$$LemonCams', 'vod_play_url': f"{uid}${uid}$$${uid}$lemon_{uid}"}]}
        except Exception as e:
            self.log(f"详情失败 {username}: {e}")
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        if int(pg) > 1: return {}
        tags = {'G': 'girls', 'C': 'couples', 'M': 'men', 'T': 'trans'}
        parts = key.split(maxsplit=1)
        tag, key = (tags.get(parts[0].upper()), parts[1].strip()) if len(parts) > 1 and parts[0].upper() in tags else ('girls', key.strip())
        rsp = self.session_get(f"{self.host}/api/front/v4/models/search/group/username?query={quote(key)}&limit=900&primaryTag={tag}").json()
        return {'list': [{"vod_id": str(u['username']), "vod_name": f"{self.country_code_to_flag(str(u['country']))}{u['username']}", "vod_pic": f"https://img.{self.Doppiocdn}/snapshot/{u['id']}/{u['snapshotTimestamp']}", "vod_remarks": "" if u['status'] == "public" else "🎫"} for u in rsp.get('models', []) if u.get('isLive')]}

    def playerContent(self, flag, id, vipFlags):
        if str(id).startswith('lemon'):
            sid = str(id).split('_', 1)[1]
            self.start_danmu(sid)
            rsp = self.session_get(f"https://edge-hls.growcdnssedge.com/hls/{sid}/master/{sid}_auto.m3u8?playlistType=lowLatency").text
            lines = rsp.strip().split('\n')
            urls = []
            for i, line in enumerate(lines):
                if '#EXT-X-STREAM-INF' in line and i + 1 < len(lines):
                    qn_start = line.find('NAME="')+6
                    qn = line[qn_start:line.find('"', qn_start)] if qn_start > 5 else 'auto'
                    urls.extend([qn, lines[i + 1].strip()])
            lemon_headers = {'User-Agent': self.headers.get('User-Agent'), 'Origin': 'https://www.lemoncams.com', 'Referer': 'https://www.lemoncams.com/'}
            return {"url": urls, "parse": '0', "header": lemon_headers, "danmaku": f"{self.getProxyUrl()}&type=danmu&room={sid}"}

        try:
            sid = str(id)
            self.start_danmu(sid)
            rsp = self.session_get(f"https://edge-hls.{self.Doppiocdn}/hls/{sid}/master/{sid}_auto.m3u8?playlistType=lowLatency").text
            lines = rsp.strip().split('\n')
            psch, pkey, urls = 'v2', self.stripchat_pkey, []
            for i, line in enumerate(lines):
                if '#EXT-X-STREAM-INF' in line and i + 1 < len(lines):
                    qn_start = line.find('NAME="')+6
                    qn = line[qn_start:line.find('"', qn_start)] if qn_start > 5 else 'auto'
                    full_url = f"{lines[i+1]}&psch={psch}&pkey={pkey}&preferredVideoCodec={self.stripchat_preferredVideoCodec}"
                    urls.extend([qn, f"{self.getProxyUrl()}&url={quote(full_url)}"])
            headers = self.headers.copy(); headers.pop('Accept-Language', None)
            return {"url": urls, "parse": '0', "header": headers, "danmaku": f"{self.getProxyUrl()}&type=danmu&room={sid}"}
        except Exception as e:
            self.log(f"播放失败 {id}: {e}")
            return {"url": [], "parse": 0}

    def update_vod(self, username):
        try:
            content_data = self.detailContent([username]).get('list')[0]
            payload = {"json": json.dumps(content_data, ensure_ascii=False)}
            self.post("http://127.0.0.1:9978/action?do=refresh&type=vod", data=payload)
        except Exception as e:
            self.log(f"刷新详情失败: {e}")

    def localProxy(self, param):
        type = param.get('type', '')
        if type == 'danmu': return self.proxy_danmu(str(param.get('room', '')))
        if type == 'danmu_debug': return [200, 'application/json', json.dumps(self.danmu_debug(), ensure_ascii=False)]
        url = param.get('url', '')
        if type == 'rec_img':
            data = self.session_get(url, self.search_headers)
            return [200, 'application/octet-stream', data.content]
        rsp = self.session_get(url)
        oldCode, oldtmp, username = self.stripchat_play.rsplit(' ')
        timestp = int(time.time())
        is_time_up = (timestp - 10) > int(oldtmp)
        is_code_changed = (int(oldCode) != 0 and rsp.status_code != int(oldCode))
        if is_time_up or is_code_changed:
            self.stripchat_play = f"{rsp.status_code} {timestp} {username}"
            self.log('计划更新')
            self.update_vod(username)
            if is_code_changed:
                self.log('code变更')
                self.post("http://127.0.0.1:9978/action?do=refresh&type=player")
                return [404, "text/plain", ""]
        if rsp.status_code == 403: rsp = self.session_get(re.sub(r'(_\d+p\d*)?\.m3u8', '_160p_blurred.m3u8', url))
        if rsp.status_code != 200: return [404, "text/plain", ""]
        data = self.process_m3u8(rsp.text) if "#EXT-X-MOUFLON:URI:" in rsp.text else rsp.text
        return [200, "application/vnd.apple.mpegur", data]

    # ===================== 轻量弹幕：HTTP轮询 + FongMi do=danmaku =====================
    def start_danmu(self, room_id):
        try:
            room_id = str(room_id)
            if not room_id: return
            with self.danmu_lock:
                self.danmu_cache.setdefault(room_id, [])
                self.danmu_seen.setdefault(room_id, set())
                t = self.danmu_threads.get(room_id)
                if t and t.is_alive(): return
                t = threading.Thread(target=self._danmu_poll_worker, args=(room_id,), daemon=True)
                self.danmu_threads[room_id] = t
                t.start()
                self.log(f"弹幕线程启动: {room_id}")
        except Exception as e: self.log(f"弹幕线程启动失败: {e}")

    def _danmu_poll_worker(self, room_id):
        first = True
        while True:
            try:
                added = self.fetch_chat_once(room_id, push_live=not first)
                if first:
                    self.refresh_danmaku(room_id)
                    first = False
                time.sleep(4 if added else 6)
            except Exception as e:
                self.log(f"弹幕轮询异常 {room_id}: {e}")
                time.sleep(8)

    def fetch_chat_once(self, room_id, push_live=False):
        url = f"{self.host}/api/front/v2/models/{room_id}/chat?source=regular&uniq={int(time.time()*1000)}"
        r = self.session_get(url, headers=self.json_headers())
        if r.status_code != 200: return 0
        try: data = r.json()
        except Exception: return 0
        arr = data.get('messages') if isinstance(data, dict) else []
        if not isinstance(arr, list): return 0
        added, new_items = 0, []
        with self.danmu_lock:
            cache = self.danmu_cache.setdefault(room_id, [])
            seen = self.danmu_seen.setdefault(room_id, set())
            for raw in arr[-100:]:
                mid = str(raw.get('id') or raw.get('createdAt') or json.dumps(raw, ensure_ascii=False)[:80])
                if mid in seen: continue
                item = self.normalize_chat_message(raw)
                if not item: continue
                item['room'] = room_id
                seen.add(mid); cache.append(item)
                if len(cache) > 500: del cache[:-500]
                new_items.append(item); added += 1
        if added:
            self.log(f"弹幕轮询更新: {room_id} +{added}")
            if push_live:
                for item in new_items[-30:]:
                    self.send_live_danmaku(item)
                    time.sleep(0.15)
        return added

    def normalize_chat_message(self, msg):
        try:
            if not isinstance(msg, dict): return None
            details = msg.get('details') or {}
            text = msg.get('text') or msg.get('message') or msg.get('content') or msg.get('body') or ''
            if not text and isinstance(details, dict): text = details.get('body') or details.get('message') or details.get('text') or ''
            if isinstance(text, dict): text = text.get('text') or text.get('body') or ''
            tp = msg.get('type') or ''
            if not text and tp == 'tip':
                amount = details.get('amount') or details.get('tokens') or '' if isinstance(details, dict) else ''
                text = f"打赏 {amount}" if amount else '打赏'
            if not text and tp == 'lovense': text = 'Lovense互动'
            ud = msg.get('userData') or msg.get('user') or msg.get('sender') or {}
            user = ''
            if isinstance(ud, dict): user = ud.get('username') or ud.get('name') or ud.get('login') or ''
            elif isinstance(ud, str): user = ud
            if not user: user = msg.get('username') or msg.get('userName') or ''
            text, user = str(text).strip(), str(user).strip()
            if not text: return None
            return {'time': int(time.time()), 'user': user[:32], 'text': text[:120]}
        except Exception as e:
            self.log(f"弹幕解析失败: {e}")
            return None

    def send_live_danmaku(self, item):
        try:
            text = str(item.get('text', '')).strip(); user = str(item.get('user', '')).strip()
            if not text: return
            show = (f"{user}: {text}" if user else text)[:80]
            ok = self.call_local_action(f"do=danmaku&text={quote(show)}", f"实时弹幕发送: {show}")
            if not ok:
                self.log("实时弹幕 action 未确认")
        except Exception as e: self.log(f"实时弹幕发送失败: {e}")

    def refresh_danmaku(self, room_id, force=False):
        try:
            room_id = str(room_id)
            now = int(time.time())
            last = int(self.danmu_refresh_ts.get(room_id, 0))
            if not force and room_id in self.danmu_refreshed: return
            if force and now - last < 3: return
            self.danmu_refreshed.add(room_id)
            self.danmu_refresh_ts[room_id] = now
            danmaku_url = f"{self.getProxyUrl()}&type=danmu&room={quote(room_id)}&t={now}"
            self.call_local_action(f"do=refresh&type=danmaku&path={quote(danmaku_url)}", f"已通知播放器刷新弹幕: {room_id}")
        except Exception as e: self.log(f"刷新弹幕失败: {e}")

    def get_action_bases(self):
        bases = []
        try:
            p = urlparse(self.getProxyUrl())
            if p.scheme and p.netloc: bases.append(f"{p.scheme}://{p.netloc}")
        except Exception: pass
        for b in ["http://127.0.0.1:9978", "http://127.0.0.1:9979"]:
            if b not in bases: bases.append(b)
        return bases

    def call_local_action(self, query, log_name=''):
        last_err = ''
        for base in self.get_action_bases():
            url = f"{base}/action?{query}"
            try:
                self.fetch(url)
                if log_name: self.log(log_name)
                return True
            except Exception as e:
                last_err = str(e)
                try:
                    requests.get(url, timeout=2)
                    if log_name: self.log(log_name)
                    return True
                except Exception as e2: last_err = str(e2)
        if log_name: self.log(f"{log_name}失败: {last_err}")
        return False

    def proxy_danmu(self, room_id):
        try:
            room_id = str(room_id)
            with self.danmu_lock: items = list(self.danmu_cache.get(room_id, []))
            xml = ['<?xml version="1.0" encoding="UTF-8"?>','<i>','\t<chatserver>chat.stripchat.local</chatserver>','\t<chatid>88888888</chatid>','\t<mission>0</mission>','\t<maxlimit>99999</maxlimit>','\t<state>0</state>','\t<real_name>0</real_name>','\t<source>stripchat</source>']
            if items: xml.append(f'\t<d p="0,5,25,16711680,0">共有{len(items)}条弹幕来袭！！！</d>')
            for i, item in enumerate(items[-200:]):
                text = self.xml_escape((str(item.get('user','')) + ': ' if item.get('user') else '') + str(item.get('text','')))
                color = '16777215' if random.random() > 0.1 else str(random.randint(0, 0xFFFFFF))
                xml.append(f'\t<d p="{round(i*2.0,1)},1,25,{color},0">{text}</d>')
            xml.append('</i>')
            self.log(f"弹幕XML输出: {room_id} {len(items)}条")
            return [200, 'text/xml', '\n'.join(xml)]
        except Exception as e:
            self.log(f"弹幕输出失败: {e}")
            return [200, 'text/xml', '<?xml version="1.0" encoding="UTF-8"?><i></i>']

    def danmu_debug(self):
        with self.danmu_lock:
            return {'rooms': {k: len(v) for k, v in self.danmu_cache.items()}, 'threads': {k: (t.is_alive() if t else False) for k,t in self.danmu_threads.items()}}

    def xml_escape(self, text):
        text = str(text or '')
        return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

    def json_headers(self):
        h = self.headers.copy(); h.update({'Accept': 'application/json, text/plain, */*', 'Referer': self.host + '/'})
        return h

    URL_PATTERN = re.compile(r'https://media-hls\.doppiocdn\.\w+/b-hls-\d+/media\.mp4')
    def process_m3u8(self, content):
        lines = content.strip().split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-MOUFLON:URI:') and i + 1 < len(lines) and 'media.mp4' in lines[i+1]:
                mouflon = line.split(':', 2)[2].strip()
                encrypted = re.sub(r'(_part\d+)?\.mp4$', '', mouflon).rsplit('_', 2)[1]
                lines[i+1] = self.URL_PATTERN.sub(mouflon.replace(encrypted, self._decode(encrypted[::-1], self.stripchat_key)), lines[i+1])
        return '\n'.join(lines)

    def country_code_to_flag(self, code):
        return ''.join(chr(ord(c.upper()) - ord('A') + 0x1F1E6) for c in code) if len(code) == 2 and code.isalpha() else code

    def _decode(self, encrypted_b64: str, key_b64: str) -> str:
        missing_padding = len(encrypted_b64) % 4
        if missing_padding: encrypted_b64 += '=' * (4 - missing_padding)
        key_bytes = base64.b64decode(key_b64)
        encrypted = base64.b64decode(encrypted_b64)
        decrypted = bytearray(len(encrypted))
        for i in range(len(encrypted)): decrypted[i] = encrypted[i] ^ (key_bytes[i % len(key_bytes)] & 0xFF)
        return decrypted.decode('utf-8')

    def create_session_with_retry(self):
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504], raise_on_status=False)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100, pool_block=False)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def session_get(self, url, headers=None, stream=False): return self.session.get(url, headers = self.headers if headers is None else headers, timeout=5, stream=stream, allow_redirects = True)