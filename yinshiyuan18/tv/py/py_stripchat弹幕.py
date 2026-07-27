# coding=utf-8
#!/usr/bin/python
import sys, re, base64, json, requests, time, threading, random
from base.spider import Spider
from datetime import datetime, timedelta
from urllib.parse import quote, urlparse
from urllib3.util.retry import Retry
from functools import lru_cache
sys.path.append('..')

class Spider(Spider):
    def init(self, extend="{}"):
        origin = 'https://zh.stripchat.com'
        self.host = origin
        self.Doppiocdn = "doppiocdn.org"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:153.0) Gecko/20100101 Firefox/153.0"
        self.headers = {'Origin': origin, 'Referer': f"{origin}/", 'User-Agent': user_agent, "Accept-Language": "zh,en;q=0.5"}
        self.json_headers = {**self.headers, 'Accept': 'application/json, text/plain, */*'}
        self.stripchat_preferredVideoCodec = "H264" # 可选H264或AV1
        self.stripchat_key = "YzWScuyQRGAGcxx1KIJmiQ7BY9Vi35ftwLqUOVO8uoo="
        self.stripchat_pkey = "Fq6m2TO2ZeBkRPm9"
        self.stripchat_play='0 0'
        self.danmu_cache = {}
        self.danmu_threads = {}
        self.danmu_lock = threading.Lock()
        self.create_session_with_retry()

    def getName(self): return "StripChat"

    def isVideoFormat(self, url): pass

    def manualVideoCheck(self): pass

    def destroy(self): pass

    def homeVideoContent(self): pass

    def datetime_utc8(self, strTime, outFormat):
        return (datetime.strptime(strTime, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=8)).strftime(outFormat)

    def homeContent(self, filter):
        CLASSES = [{'type_name': '女主播', 'type_id': 'girls'}, {'type_name': '情侣', 'type_id': 'couples'}, {'type_name': '男主播', 'type_id': 'men'}, {'type_name': '跨性别', 'type_id': 'trans'}]
        VALUE = [{'n': '中国', 'v': 'tagLanguageChinese'}, {'n': '亚洲', 'v': 'ethnicityAsian'}, {'n': '白人', 'v': 'ethnicityWhite'}, {'n': '拉丁', 'v': 'ethnicityLatino'}, {'n': '混血', 'v': 'ethnicityMultiracial'}, {'n': '印度', 'v': 'ethnicityIndian'}, {'n': '阿拉伯', 'v': 'ethnicityMiddleEastern'}, {'n': '黑人', 'v': 'ethnicityEbony'}]
        VALUE_MEN = [{'n': '情侣', 'v': 'sexGayCouples'}, {'n': '直男', 'v': 'orientationStraight'}]
        TIDS = ('girls', 'couples', 'men', 'trans')
        filters = {tid: [{'key': 'tag', 'value': VALUE_MEN + VALUE if tid == 'men' else VALUE}] for tid in TIDS}
        return {'class': CLASSES, 'filters': filters}

    def categoryContent(self, tid, pg, filter, extend):
        if tid.startswith('search '):
            _, tag, key = tid.split(maxsplit=2)
            rsp = self.session_get(f"{self.host}/api/front/v4/models/search/group/username?query={key}&limit=900&primaryTag={tag}").json()
            return {'list': [{"vod_id": str(u['username']), "vod_name": f"{self.country_code_to_flag(str(u['country']))}{u['username']}", "vod_pic": f"https://img.{self.Doppiocdn}/snapshot/{u['id']}/{u['snapshotTimestamp']}", 'style': {"type": "rect", "ratio": 1.78}, "vod_remarks": "" if u['status'] == "public" else "🎫"} for u in rsp.get('models', []) if u['isLive']], "page": pg, "pagecount": 1}
        limit = 60
        offset = limit * (int(pg) - 1)
        url = f"{self.host}/api/front/models?improveTs=false&removeShows=false&limit={limit}&offset={offset}&primaryTag={tid}&sortBy=stripRanking&rcmGrp=A&rbCnGr=true&prxCnGr=false&nic=false"
        if 'tag' in extend: url += f'&filterGroupTags=[["{extend["tag"]}"]]'
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
                if startAt: remark = f"🎫 始于 {self.datetime_utc8(startAt, '%m月%d日 %H:%M')}"
            director = f"{flag}{username}"
            desc = self.get_danmaku_desc(uid)
            return {'list': [{"vod_id": username, "vod_name": str(info['topic'])[:80], "vod_pic": str(user['avatarUrl']), "vod_director": director, "vod_content": desc, "vod_remarks": remark, 'vod_play_from': 'StripChat$$$LemonCams', 'vod_play_url': f"{uid}${uid}$$${uid}$lemon_{uid}"}]}
        except: return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        if int(pg) > 1: return {}
        return {'list': [{'vod_id': f'search {t["type_id"]} {key}', 'vod_name': t['type_name'], 'vod_tag': 'folder'} for t in self.homeContent(False).get('class', [])]}

    def playerContent(self, flag, id, vipFlags):
        urls = []
        try:
            sid = id.split('_')[-1]
            self.start_danmu(sid)
            if id.startswith('lemon'):
                rsp = self.session_get(f"https://edge-hls.growcdnssedge.com/hls/{sid}/master/{sid}_auto.m3u8?playlistType=lowLatency").text
                lines = rsp.strip().split('\n')
                for i, line in enumerate(lines):
                    if '#EXT-X-STREAM-INF' in line:
                        qn_start = line.find('NAME="')+6
                        qn = line[qn_start:line.find('"', qn_start)]
                        url = lines[i + 1]
                        urls.extend([qn, url])
                headers = {'User-Agent': self.headers.get('User-Agent'), 'Origin': 'https://www.lemoncams.com', 'Referer': 'https://www.lemoncams.com/'}
            else:
                rsp = self.session_get(f"https://edge-hls.{self.Doppiocdn}/hls/{sid}/master/{sid}_auto.m3u8?playlistType=lowLatency").text
                lines = rsp.strip().split('\n')
                psch, pkey, processed = 'v2', self.stripchat_pkey, False
                for i, line in enumerate(lines):
                    if '#EXT-X-STREAM-INF' in line:
                        qn_start = line.find('NAME="')+6
                        qn = line[qn_start:line.find('"', qn_start)]
                        full_url = f"{lines[i+1]}&psch={psch}&pkey={pkey}&preferredVideoCodec={self.stripchat_preferredVideoCodec}"
                        urls.extend([qn, f"{self.getProxyUrl()}&url={quote(full_url)}"])
                headers = {k: v for k, v in self.headers.items() if k != 'Accept-Language'}
            return {"url": urls, "parse": '0', 'position': '0', "header": headers}
        except Exception as e:
            self.log(f"播放失败 {id}: {e}")
            return {"url": urls, "parse": 0}

    def update_vod(self, username):
        try:
            content_data = self.detailContent([username]).get('list')[0]
            payload = {"json": json.dumps(content_data, ensure_ascii=False)}
            self.post("http://127.0.0.1:9978/action?do=refresh&type=vod", data=payload)
        except Exception as e:
            self.log(f"刷新详情失败: {e}")
    
    def localProxy(self, param):
        url, type = param['url'], param.get('type', '')
        if type == 'media':
            data = self.session_get(url, timeout=(5, 15))
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

    URL_PATTERN = re.compile(r'https://media-hls\.doppiocdn\.\w+/b-hls-\d+/media\.mp4')
    MAP_URI_PATTERN = re.compile(r'URI=["\']?(https?://[^\s"\'<>]+)["\']?')
    MOUFLON_TAIL_PATTERN = re.compile(r'(_part\d+)?\.mp4$')
    def process_m3u8(self, content):
        lines = content.strip().split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-MOUFLON:URI:') and 'media.mp4' in lines[i+1]:
                mouflon = line.split(':', 2)[2].strip()
                encrypted = self.MOUFLON_TAIL_PATTERN.sub('', mouflon).rsplit('_', 2)[1]
                new_url= mouflon.replace(encrypted, self._decode(encrypted[::-1], self.stripchat_key))
                proxy_url = f"{self.getProxyUrl()}&type=media&url={quote(new_url)}"
                lines[i+1] = self.URL_PATTERN.sub(proxy_url, lines[i+1])
            elif line.startswith('#EXT-X-MAP:URI'):
                match = self.MAP_URI_PATTERN.search(line)
                if match:
                    original_url = match.group(1)
                    proxy_url = f"{self.getProxyUrl()}&type=media&url={quote(original_url)}"
                    lines[i] = line.replace(original_url, proxy_url)
        return '\n'.join(lines)

    def country_code_to_flag(self, code):
        return ''.join(chr(ord(c.upper()) - ord('A') + 0x1F1E6) for c in code) if len(code) == 2 and code.isalpha() else code

    @staticmethod
    @lru_cache(maxsize=20)
    def _decode(encrypted_b64: str, key_b64: str) -> str:
        encrypted_b64 += '=' * (4 - len(encrypted_b64) % 4)
        key_bytes = base64.b64decode(key_b64)
        encrypted = base64.b64decode(encrypted_b64)
        decrypted = bytearray(len(encrypted))
        for i in range(len(encrypted)):
            decrypted[i] = encrypted[i] ^ (key_bytes[i % len(key_bytes)] & 0xFF)
        return decrypted.decode('utf-8')

    def create_session_with_retry(self):
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[408, 429, 500, 502, 503, 504], raise_on_status=False)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=50, pool_block=False)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def session_get(self, url, headers=None, stream=False, timeout=(3, 5)): return self.session.get(url, headers = self.headers if headers is None else headers, timeout=timeout, stream=stream, allow_redirects = True)

    def start_danmu(self, room_id):
        try:
            entry = self.danmu_threads.get(room_id)
            if entry:
                t, _ = entry
                if t.is_alive():
                    self.log(f"弹幕线程已存在: {room_id}")
                    return
            for rid, (ot, stop_evt) in list(self.danmu_threads.items()):
                if rid == room_id:
                    continue
                if ot.is_alive():
                    self.log(f"正在关闭其他房间弹幕线程: {rid}")
                    stop_evt.set()        # 通知线程停止
                    ot.join(timeout=1.0)  # 等待线程结束（最多1秒）
                    # 从字典中移除（确保不保留死线程）
                    del self.danmu_threads[rid]
            stop_event = threading.Event()
            t = threading.Thread(target=self._danmu_poll_worker, args=(room_id, stop_event), daemon=True)
            self.danmu_threads[room_id] = (t, stop_event)
            t.start()
            self.log(f"弹幕线程启动: {room_id}")
        except Exception as e: self.log(f"弹幕线程启动失败: {e}")

    def _danmu_poll_worker(self, room_id, stop_event):
        while True:
            if self.base_url:
                try:
                    r = self.fetch(f"{self.base_url}/media", timeout=1).json()
                    if not r.get("state", False):
                        stop_event.set()
                except:
                    stop_event.set()
            if stop_event.is_set():
                break
            try:
                self.fetch_chat_once(room_id)
                if stop_event.wait(5):
                    break
            except Exception as e:
                self.log(f"弹幕轮询异常 {room_id}: {e}")
                if stop_event.wait(10):
                    break
        self.log(f"弹幕线程结束: {room_id}")

    def fetch_chat_once(self, room_id):
        url = f"{self.host}/api/front/v2/models/{room_id}/chat?source=regular&uniq={int(time.time()*1000)}"
        r = self.session_get(url, headers=self.json_headers)
        if r.status_code != 200: return 0
        try: data = r.json()
        except Exception: return 0
        arr = data.get('messages') if isinstance(data, dict) else []
        if not isinstance(arr, list): return 0
        newId, newMsg = 0, []
        with self.danmu_lock:
            cache = self.danmu_cache.get(room_id, {})
            oldId = cache.get('id', 0)
            cacheMsg = cache.get('msg', [])
            for raw in reversed(arr):
                id = int(raw.get('id', 0))
                if oldId and id <= oldId:
                    break
                if not newId:
                    newId = id
                item = self.normalize_chat_message(raw)
                if not item: continue
                newMsg.append(item)
            if newId:
                if newMsg:
                    cacheMsg = newMsg + cacheMsg
                    cacheMsg = cacheMsg[:30]
                self.danmu_cache[room_id] = {
                    'id': newId,
                    'msg': cacheMsg
                }
        if oldId:
            for m in reversed(newMsg):
                self.send_live_danmaku(m)
                time.sleep(0.15)

    def replace_emoji(self, text: str) -> str:
        emoji_map = {
            ":heart:": "❤️",
            ":dancing:": "💃",
            ":thumbsup:": "👍",
            ":flower:": "🌹",
            ":lol:": "😄",
            ":flirt:": "😉",
            ":devil:": "😈",
            ":hideeyes:": "🙈",
            ":ask:": "❓",
            ":inlove:": "😍",
            ":tongue:": "😛",
            ":cry:": "😭",
            ":fire:": "🔥",
            ":asking:": "🤔",
            ":wink:": "😉",
            ":ok:": "👌",
            ":shy:": "😳",
            ":angry:": "😡",
            ":facepalm:": "🤦‍♂️",
            ":ass:": "🍑",
        }
        for code, emoji_char in emoji_map.items():
            text = text.replace(code, emoji_char)
        return text

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
                text = f"打赏 {amount} tk" if amount else '打赏'
            if not text and tp == 'lovense': text = 'Lovense互动'
            ud = msg.get('userData') or msg.get('user') or msg.get('sender') or {}
            user = ''
            if isinstance(ud, dict): user = ud.get('username') or ud.get('name') or ud.get('login') or ''
            elif isinstance(ud, str): user = ud
            if not user: user = msg.get('username') or msg.get('userName') or ''
            text, user = str(text).strip(), str(user).strip()
            if not text : return None
            return {'time': msg.get('createdAt'), 'user': user[:32], 'text': self.replace_emoji(text)[:120]}
        except Exception as e:
            self.log(f"弹幕解析失败: {e}")
            return None

    def send_live_danmaku(self, item):
        try:
            text = str(item.get('text', '')).strip(); user = str(item.get('user', '')).strip()
            show = (f"{user}: {text}" if user else text)[:80]
            ok = self.call_local_action(f"do=danmaku&text={quote(show)}", f"实时弹幕发送: {show}")
            if not ok:
                self.log("实时弹幕 action 未确认")
        except Exception as e: self.log(f"实时弹幕发送失败: {e}")

    def get_danmaku_desc(self, room_id):
        cache = self.danmu_cache.get(room_id, {})
        cacheMsg = cache.get('msg', [])
        msg = []
        for item in cacheMsg:
            t = self.datetime_utc8(item.get('time'), '%H:%M')
            text = str(item.get('text', '')).strip(); user = str(item.get('user', '')).strip()
            show = (f"{t} {user}: {text}" if user else f"{t} {text}")
            msg.append(show)
        return '\n'.join(msg)

    def get_action_bases(self):
        bases = []
        try:
            p = urlparse(self.getProxyUrl())
            if p.scheme and p.netloc: bases.append(f"{p.scheme}://{p.netloc}")
        except Exception: pass
        for b in ["http://127.0.0.1:9978", "http://127.0.0.1:9979"]:
            if b not in bases: bases.append(b)
        return bases

    base_url = ''
    def call_local_action(self, query, log_name):
        for base in [self.base_url] if self.base_url else self.get_action_bases():
            try:
                url = f"{base}/action?{query}"
                r = self.fetch(url, timeout=1)
                if r.text.strip() == "OK":
                    self.base_url = base
                    self.log(log_name)
                    return True
            except:
                continue
        self.log(f"失败: {log_name}")
        return False
