# coding=utf-8
# !/python
import sys
import json
import re
import requests
from urllib.parse import unquote, quote, urljoin, urlparse
from base.spider import Spider

sys.path.append("..")

# ---------- 站点配置 ----------
xurl = "https://www.adultporna-av107.com"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive'
}

# ---------- 广告关键词 ----------
AD_KEYWORDS = [
    "新葡京", "澳门新葡京", "新葡京娱乐城", "新葡京娱乐场",
    "澳门赌场", "澳门威尼斯人", "永利皇宫", "美高梅", "金沙娱乐场",
    "金沙赌场", "葡京娱乐场", "葡京赌场", "新濠天地", "新濠影汇",
    "银河娱乐", "星际娱乐", "英皇娱乐", "永利澳门", "美高梅中国",
    "老虎机", "pg电子", "cq9", "cq9电子", "跳高高", "麻将胡了",
    "赏金女王", "寻宝黄金城", "水果机", "糖果派对",
    "棋牌", "开元棋牌", "真人视讯", "百家乐", "体育下注",
    "外围投注", "足彩", "滚球", "六合彩", "时时彩",
    "赌场", "casino", "娱乐城", "博彩", "彩票", "投注",
    "充值送", "首存", "返水", "vip通道", "快速提现",
    "注册即送", "高赔率", "资金安全", "百万提款",
    "澳门威尼斯", "澳门金沙", "澳门银河", "永利娱乐",
]

# ---------- 热门搜索标签（从源码提取） ----------
HOT_TAGS = [
    "网袜",
    "导师",
    "纤细",
    "美腿",
    "清纯",
    "小姐",
    "菊花",
    "爆菊",
    "求饶",
    "短裙",
    "浴场",
    "迷晕",
    "嫖妓",
    "旅馆",
    "正妹",
    "紧身",
    "白皙",
    "老婆",
    "中出",
    "女模",
    "按摩",
    "阴道",
    "淫荡",
    "手机",
    "开档",
    "拍摄",
    "海滩",
    "沙滩",
    "奴隶",
    "惩罚",
    "精液",
    "午睡",
    "嫂子",
    "上位",
    "秘书",
    "上班",
    "强迫",
    "男友",
    "甜蜜",
    "温柔",
    "暴力",
    "撕烂",
    "日逼",
    "女星",
    "卖淫",
    "夜班",
    "尾随",
    "色狼",
    "痴汉",
    "偶遇",
    "巨乳",
    "调教",
    "萝莉",
    "自慰",
    "妈妈",
    "母子",
    "黑人",
    "强奸",
    "熟女",
    "偷拍",
    "人妖",
    "迷奸",
    "足交",
    "伪娘",
    "女儿",
    "幼女",
    "黑丝",
    "内射",
    "破处",
    "丝袜",
    "抖音",
    "国产",
    "绳子",
    "美臀",
    "哥哥",
    "禽兽",
    "灌倒",
    "做客",
    "狗链",
    "主妇",
    "美鲍",
    "偷约",
    "技师",
    "美人",
    "处女",
    "清秀",
    "新娘",
    "跳蛋",
    "诱奸",
    "学生",
    "日本",
    "空姐",
    "丝足",
]


class Spider(Spider):
    def getName(self):
        return "91爆料"

    def init(self, extend):
        self.host = xurl
        self.session = requests.Session()
        self.session.headers.update(headerx)

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    # ---------- 首页视频 ----------
    def homeVideoContent(self):
        videos = []
        try:
            res = requests.get(xurl + '/show/30/', headers=headerx, timeout=10)
            res.encoding = "utf-8"
            doc = res.text
            vodss = self._find_list_container(doc)
            if vodss:
                vods = re.findall(r'<li[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*title="([^"]+)".*?</li>', vodss, re.S)
                for href, title in vods:
                    pic = self._extract_pic(vodss, href)
                    remarks = self._extract_remarks(vodss, href)
                    videos.append({
                        "vod_id": href,
                        "vod_name": title.strip(),
                        "vod_pic": pic,
                        "vod_remarks": remarks
                    })
        except Exception as e:
            print(f"homeVideoContent error: {e}")
        return {'list': videos}

    # ---------- 分类 ----------
    def homeContent(self, filter):
        result = {}
        result['class'] = []
        
        # 方式1：从源码硬编码的分类表（已提取自HTML）
        manual_classes = [
            ('/t/163/', '国产视频'),
            ('/t/232/', '网曝黑料'),
            ('/t/236/', '主播大秀'),
            ('/t/233/', 'AV解说'),
            ('/t/48/', '国产自拍'),
            ('/t/231/', '抖阴视频'),
            ('/t/45/', '国模私拍'),
            ('/t/67/', '空姐模特'),
            ('/t/69/', '国产学生'),
            ('/t/70/', '人妻熟女'),
            ('/t/74/', '国产 OL'),
            ('/t/75/', '国产名人'),
            ('/t/17/', '国产精品'),
            ('/t/18/', '国产剧情'),
            ('/t/2/', '国产传媒'),
            ('/t/227/', '综合传媒'),
            ('/t/38/', '麻豆合集'),
            ('/t/109/', '葫芦影业'),
            ('/t/111/', '天美传媒'),
            ('/t/112/', '果冻传媒'),
            ('/t/131/', '91制片厂'),
            ('/t/113/', '蜜桃传媒'),
            ('/t/114/', '精东影业'),
            ('/t/115/', '皇家华人'),
            ('/t/116/', 'SWAG'),
            ('/t/120/', '兔子先生'),
            ('/t/125/', '大象传媒'),
            ('/t/126/', '乌鸦传媒'),
            ('/t/128/', '糖心VLOG'),
            ('/t/130/', '星空传媒'),
            ('/t/1/', '日本有码'),
            ('/t/36/', '丝袜美腿'),
            ('/t/53/', '绝美少女'),
            ('/t/58/', '日本口爆'),
            ('/t/234/', '萝莉少女'),
            ('/t/6/', '强奸乱伦'),
            ('/t/7/', '日本巨乳'),
            ('/t/9/', '制服诱惑'),
            ('/t/5/', '日本无码'),
            ('/t/10/', '人妻熟女'),
            ('/t/11/', '日本调教'),
            ('/t/12/', '日本出轨'),
            ('/t/13/', '中文字幕'),
            ('/t/16/', '日本素人'),
            ('/t/32/', '巨乳无码'),
            ('/t/35/', '制服无码'),
            ('/t/89/', '波多野结衣'),
            ('/t/87/', '三上悠亚'),
            ('/t/90/', '葵司'),
            ('/t/93/', '桃乃木香奈'),
            ('/t/103/', '松本一香'),
            ('/t/205/', '篠田優'),
            ('/t/215/', '川上奈奈美'),
            ('/t/225/', '综合番号'),
            ('/t/142/', '200GANA'),
            ('/t/146/', '259LUXU'),
            ('/t/143/', '300MIUM'),
            ('/t/149/', '300MAAN'),
            ('/t/190/', 'MIAA'),
            ('/t/191/', 'SSIS'),
            ('/t/186/', 'STARS'),
            ('/t/235/', '国产自/偷拍'),
            ('/t/86/', '女优'),
            ('/t/222/', '番号未分类'),
            ('/t/141/', '日本番號'),
            ('/t/30/', '欧美'),
            ('/t/164/', '成人动漫'),
            ('/t/85/', '伦理电影'),
            ('/t/84/', 'VR'),
            ('/t/226/', '猫爪影像'),
            ('/t/117/', '台湾JVID'),
            ('/t/118/', '逼哩逼哩'),
            ('/t/119/', '杏吧专区'),
            ('/t/122/', 'PsychoPornTW'),
            ('/t/123/', 'MINI传媒'),
            ('/t/124/', '微啪 &amp; 陌丽影像传媒'),
            ('/t/47/', '国产视频'),
            ('/t/68/', '国产颜射'),
            ('/t/71/', '国产乱伦'),
            ('/t/72/', '国产自慰'),
            ('/t/73/', '国产野合车震'),
            ('/t/76/', '国产网曝门'),
            ('/t/88/', '高桥圣子'),
            ('/t/91/', '水卜櫻'),
            ('/t/92/', '紗倉真菜'),
            ('/t/94/', '安齋拉拉'),
            ('/t/95/', '天使萌'),
            ('/t/96/', '相澤南'),
            ('/t/98/', 'Miru'),
            ('/t/99/', '羽咲美晴'),
            ('/t/100/', '山岸逢花'),
            ('/t/101/', '七澤米亞'),
            ('/t/102/', '河北彩花'),
            ('/t/207/', '夢乃愛華'),
            ('/t/104/', '木下日葵'),
            ('/t/132/', '二階堂夢'),
            ('/t/133/', '田中宁宁'),
            ('/t/147/', '261ARA'),
            ('/t/148/', '277DCV'),
            ('/t/150/', '300NTK'),
            ('/t/152/', '328HMDN'),
            ('/t/153/', '332NAMA'),
            ('/t/154/', '336KNB'),
            ('/t/155/', '348NTR'),
            ('/t/156/', '390JAC'),
            ('/t/158/', '428SUKE'),
            ('/t/181/', 'AARM'),
            ('/t/180/', 'ADN'),
            ('/t/185/', 'ATID'),
            ('/t/159/', 'DCV'),
            ('/t/192/', 'DFDM'),
            ('/t/194/', 'DLDSS'),
            ('/t/51/', '日本有码'),
            ('/t/52/', '高潮喷吹'),
            ('/t/59/', '日本重口味'),
            ('/t/63/', '名优精品'),
            ('/t/79/', '日本人妖'),
            ('/t/81/', '日本新人'),
            ('/t/34/', '人妻无码'),
            ('/t/50/', '精品无码'),
            ('/t/221/', '日本无码'),
            ('/t/223/', '乱伦无码'),
            ('/t/224/', '强奸无码'),
            ('/t/105/', 'X-Art'),
            ('/t/106/', '欧美激情'),
            ('/t/107/', 'ThZu.Cc'),
            ('/t/42/', '欧美女同性戀'),
            ('/t/41/', '欧美男同性戀'),
            ('/t/40/', '欧美人妖'),
            ('/t/49/', '欧美极品'),
            ('/t/65/', '欧美自拍'),
            ('/t/29/', '成人动漫'),
            ('/t/170/', 'ETERNITY ～深夜的濡恋频道(中文字幕)'),
            ('/t/171/', '地味变!!～改变土妹子的纯洁异性交往(中文字幕)'),
            ('/t/172/', '魔界天使ジブリール'),
            ('/t/173/', '土下座跪求給看'),
            ('/t/174/', '魔法少女アイ'),
            ('/t/175/', '女教師'),
            ('/t/176/', '夢現の境界'),
            ('/t/177/', '支配的教坛(中文字幕)'),
            ('/t/37/', '三级电影'),
            ('/t/61/', 'AI换脸'),
            ('/t/64/', '香港級品'),
            ('/t/14/', '韩国级品'),
            ('/t/44/', 'VR无码'),
            ('/t/43/', 'VR有碼'),
        ]
        
        # 方式2：动态从首页抓取分类（优先）
        dynamic_classes = self._fetch_dynamic_classes()
        if dynamic_classes:
            seen = set()
            for tid, name in dynamic_classes:
                if tid not in seen:
                    seen.add(tid)
                    result['class'].append({'type_id': tid, 'type_name': name})
            for tid, name in manual_classes:
                if tid not in seen:
                    seen.add(tid)
                    result['class'].append({'type_id': tid, 'type_name': name})
        else:
            for tid, name in manual_classes:
                result['class'].append({'type_id': tid, 'type_name': name})
        
        # 热门标签作为 filter 返回
        if filter and HOT_TAGS:
            result['filters'] = {
                "tags": [{"n": t, "v": t} for t in HOT_TAGS[:50]]
            }
        return result

    # ---------- 动态获取分类 ----------
    def _fetch_dynamic_classes(self):
        classes = []
        try:
            res = requests.get(xurl, headers=headerx, timeout=10)
            res.encoding = "utf-8"
            html = res.text
            dl_blocks = re.findall(r'<dl>(.*?)</dl>', html, re.S)
            for dl in dl_blocks:
                dd_links = re.findall(r'<dd>\s*<a[^>]*href="(/t/\d+)"[^>]*>(.*?)</a>\s*</dd>', dl, re.S)
                for href, name in dd_links:
                    name = re.sub(r'<[^>]+>', '', name).strip()
                    if name and href not in [c[0] for c in classes]:
                        classes.append((href, name))
            panel_blocks = re.findall(
                r'<h2[^>]*class="main-title-name">(.*?)</h2>\s*<div[^>]*class="btn-sort-wrapper1 grid-container">(.*?)</div>',
                html, re.S
            )
            for _, block in panel_blocks:
                links = re.findall(r'<a[^>]*href="(/t/\d+)"[^>]*>(.*?)</a>', block, re.S)
                for href, name in links:
                    name = re.sub(r'<[^>]+>', '', name).strip()
                    if name and href not in [c[0] for c in classes]:
                        classes.append((href, name))
        except Exception as e:
            print(f"动态获取分类失败: {e}")
        return classes

    # ---------- 分类列表 ----------
    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if pg == "" or int(pg) == 1:
            url = xurl + cid
        else:
            url = xurl + cid.rstrip('/') + '-' + str(pg) + '/'

        try:
            res = requests.get(url=url, headers=headerx, timeout=10)
            res.encoding = "utf-8"
            html = res.text
            vodss = self._find_list_container(html)
            if vodss:
                vods = re.findall(r'<li[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*title="([^"]+)".*?</li>', vodss, re.S)
                for href, title in vods:
                    pic = self._extract_pic(vodss, href)
                    remarks = self._extract_remarks(vodss, href)
                    videos.append({
                        "vod_id": href,
                        "vod_name": title.strip(),
                        "vod_pic": pic,
                        "vod_remarks": remarks
                    })
        except Exception as e:
            print(f"categoryContent error: {e}")

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    # ---------- 视频详情（获取直链） ----------
    def detailContent(self, ids):
        did = ids[0]
        if "voddetail" in did:
            did = did.replace("voddetail", "v")
        videos = []
        result = {}
        try:
            res = requests.get(url=xurl + did, headers=headerx, timeout=10)
            res.encoding = "utf-8"
            html = res.text
            purl = ""
            source_match = re.search(r'"","url":"(.*?)"', html)
            if source_match:
                purl = source_match.group(1).replace("\\", "")
            if not purl:
                pm = re.search(r'var player_[^=]+=\s*({.*?})', html, re.S)
                if pm:
                    try:
                        pdata = json.loads(pm.group(1))
                        purl = pdata.get('url', '')
                    except:
                        pass
            if not purl:
                vm = re.search(r'<video[^>]*src="([^"]+)"', html)
                if vm:
                    purl = vm.group(1)
            
            title = ""
            pic = ""
            tm = re.search(r'<h1[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</h1>', html, re.S)
            if tm:
                title = re.sub(r'<[^>]+>', '', tm.group(1)).strip()
            pm2 = re.search(r'<img[^>]*class="[^"]*pic[^"]*"[^>]*src="([^"]+)"', html)
            if pm2:
                pic = pm2.group(1)
            
            videos.append({
                "vod_id": did,
                "vod_name": title,
                "vod_pic": pic,
                "type_name": "",
                "vod_year": "",
                "vod_area": "",
                "vod_remarks": "",
                "vod_actor": "",
                "vod_director": "",
                "vod_content": "",
                'vod_play_from': '直链播放',
                "vod_play_url": purl
            })
        except Exception as e:
            print(f"detailContent error: {e}")
        result['list'] = videos
        return result

    # ---------- 搜索 ----------
    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        header2 = {
            'User-Agent': headerx['User-Agent'],
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        try:
            search_url = xurl + '/s/page/' + str(page) + '/wd/' + quote(key)
            res = requests.get(search_url, headers=header2, timeout=10)
            res.encoding = "utf-8"
            html = res.text
            vodss = self._find_list_container(html)
            if vodss:
                vods = re.findall(r'<li[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*title="([^"]+)".*?</li>', vodss, re.S)
                for href, title in vods:
                    pic = self._extract_pic(vodss, href)
                    remarks = self._extract_remarks(vodss, href)
                    videos.append({
                        "vod_id": href,
                        "vod_name": title.strip(),
                        "vod_pic": pic,
                        "vod_remarks": remarks
                    })
        except Exception as e:
            print(f"searchContentPage error: {e}")
        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    # ================= 工具方法 =================
    def _find_list_container(self, html):
        patterns = [
            r'<ul[^>]*class="[^"]*row row-space8[^"]*"[^>]*>(.*?)</ul>',
            r'<ul[^>]*class="[^"]*vod-list[^"]*"[^>]*>(.*?)</ul>',
            r'<div[^>]*class="[^"]*vod-list[^"]*"[^>]*>(.*?)</div>',
        ]
        for p in patterns:
            m = re.search(p, html, re.S)
            if m:
                return m.group(1)
        m = re.search(r'<body[^>]*>(.*?)</body>', html, re.S)
        return m.group(1) if m else html

    def _extract_pic(self, container, href):
        m = re.search(r'<a[^>]*href="' + re.escape(href) + r'"[^>]*>.*?<img[^>]*src="([^"]+)"', container, re.S)
        if m:
            return m.group(1)
        return ""

    def _extract_remarks(self, container, href):
        m = re.search(r'<a[^>]*href="' + re.escape(href) + r'"[^>]*>.*?<small[^>]*>(.*?)</small>', container, re.S)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return ""

    # ================= 去广告核心 =================
    def localProxy(self, params):
        if params.get('type') == "m3u8":
            return self._proxy_m3u8(params)
        elif params.get('type') == "media":
            return self._proxy_media(params)
        elif params.get('type') == "ts":
            return self._proxy_ts(params)
        return [404, "text/plain", "unsupported type"]

    def _proxy_m3u8(self, params):
        url = params.get('url', '')
        referer = params.get('referer', xurl)
        if not url:
            return [404, "text/plain", "no url"]
        text = self._get_m3u8_content(url, referer)
        if not text:
            return [404, "text/plain", "m3u8 download failed"]
        cleaned = self._clean_m3u8(text, url, referer)
        return [200, "application/vnd.apple.mpegurl", cleaned]

    def _proxy_media(self, params):
        return [404, "text/plain", "not supported"]

    def _proxy_ts(self, params):
        return [404, "text/plain", "not supported"]

    def _get_m3u8_content(self, url, referer):
        try:
            headers = {
                'User-Agent': headerx['User-Agent'],
                "Referer": referer,
                "Origin": xurl
            }
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                return resp.text
        except Exception as e:
            print(f"下载 m3u8 失败: {e}")
        return None

    def _proxy_m3u8_url(self, url, referer=''):
        try:
            if hasattr(self, 'getProxyUrl'):
                return self.getProxyUrl() + '&type=m3u8&url=' + quote(url, safe='') + '&referer=' + quote(referer or xurl, safe='')
        except:
            pass
        return url

    def _clean_m3u8(self, m3u8_text, m3u8_url='', referer='', skip_seconds=25):
        text = (m3u8_text or '').replace('\r', '')
        if '#EXT-X-STREAM-INF' in text:
            out = []
            last_stream = False
            for raw in text.splitlines():
                line = raw.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    out.append(line)
                    last_stream = line.startswith('#EXT-X-STREAM-INF')
                else:
                    abs_url = urljoin(m3u8_url, line)
                    if last_stream or '.m3u8' in line.lower():
                        out.append(self._proxy_m3u8_url(abs_url, referer))
                    else:
                        out.append(abs_url)
                    last_stream = False
            return '\n'.join(out) + '\n'

        header, segments, tail, media_sequence, target_duration = self._parse_m3u8_segments(text)
        if not segments:
            return text

        marker = self._main_path_marker(m3u8_url)
        stat = {}
        for seg in segments:
            key = self._segment_host_key(seg['uri'], m3u8_url)
            stat[key] = stat.get(key, 0.0) + float(seg.get('dur') or 0)
        main_key = max(stat.items(), key=lambda x: x[1])[0] if stat else ('', '')
        total_dur = sum(stat.values()) or 0
        main_dur = stat.get(main_key, 0)

        cleaned = []
        removed = 0
        for idx, seg in enumerate(segments):
            key = self._segment_host_key(seg['uri'], m3u8_url)
            is_front = idx < 12
            abs_uri = urljoin(m3u8_url, seg.get('uri', ''))
            is_ad = self._is_ad_segment(seg['uri'], seg.get('dur'), seg.get('tags'))
            if marker and marker not in urlparse(abs_uri).path.lower():
                is_ad = True
            tags_text = '\n'.join(seg.get('tags') or []).upper()
            if is_front and 'METHOD=NONE' in tags_text and marker and marker not in urlparse(abs_uri).path.lower():
                is_ad = True
            if (not is_ad) and is_front and total_dur > 0 and main_dur >= total_dur * 0.6:
                if key != main_key and stat.get(key, 0) <= 90:
                    is_ad = True
            if is_ad:
                removed += 1
                continue
            seg['_idx'] = idx
            cleaned.append(seg)

        if removed == 0 and len(segments) > 4:
            acc = 0.0
            cut = 0
            for idx, seg in enumerate(segments[:12]):
                key = self._segment_host_key(seg['uri'], m3u8_url)
                if key == main_key and acc >= 3:
                    break
                acc += float(seg.get('dur') or target_duration or 3)
                cut = idx + 1
                if acc >= skip_seconds:
                    break
            if cut > 0 and cut < len(segments):
                first_key = self._segment_host_key(segments[0]['uri'], m3u8_url)
                if first_key != main_key:
                    cleaned = segments[cut:]
                    removed = cut

        if not cleaned:
            cleaned = segments
            removed = 0

        new_lines = []
        has_m3u = False
        for line in header:
            if line.startswith('#EXTM3U'):
                has_m3u = True
            if line.startswith('#EXT-X-MEDIA-SEQUENCE') or line.startswith('#EXT-X-START'):
                continue
            if line.startswith('#EXT-X-KEY') and 'METHOD=NONE' in line.upper() and removed > 0:
                continue
            new_lines.append(line)
        if not has_m3u:
            new_lines.insert(0, '#EXTM3U')
        first_idx = cleaned[0].get('_idx', removed) if cleaned else removed
        new_lines.append(f'#EXT-X-MEDIA-SEQUENCE:{media_sequence + first_idx}')

        for seg in cleaned:
            for tag in seg.get('tags') or []:
                if tag.startswith('#EXT-X-KEY') or tag.startswith('#EXT-X-MAP'):
                    def _fix_uri(m):
                        return 'URI="' + urljoin(m3u8_url, m.group(1)) + '"'
                    tag = re.sub(r'URI="([^"]+)"', _fix_uri, tag)
                new_lines.append(tag)
            new_lines.append(urljoin(m3u8_url, seg.get('uri', '')))
        if tail:
            for line in tail:
                if line.startswith('#EXT-X-ENDLIST'):
                    new_lines.append(line)
        elif '#EXT-X-ENDLIST' in text:
            new_lines.append('#EXT-X-ENDLIST')
        print(f"[m3u8清洗] 原片段:{len(segments)} 删除广告:{removed} 保留:{len(cleaned)}")
        return '\n'.join(new_lines) + '\n'

    def _parse_m3u8_segments(self, text):
        lines = [x.strip() for x in text.replace('\r', '').split('\n') if x.strip()]
        header, segments, tail = [], [], []
        pending_tags = []
        media_sequence = 0
        target_duration = 0
        started = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('#EXT-X-MEDIA-SEQUENCE'):
                try:
                    media_sequence = int(line.split(':', 1)[1])
                except:
                    pass
                if not started:
                    header.append(line)
                else:
                    pending_tags.append(line)
            elif line.startswith('#EXT-X-TARGETDURATION'):
                try:
                    target_duration = float(line.split(':', 1)[1])
                except:
                    pass
                if not started:
                    header.append(line)
                else:
                    pending_tags.append(line)
            elif line.startswith('#EXTINF'):
                started = True
                dur = target_duration or 3.0
                m = re.search(r'#EXTINF:\s*([\d.]+)', line)
                if m:
                    try:
                        dur = float(m.group(1))
                    except:
                        pass
                tags = pending_tags + [line]
                pending_tags = []
                uri = ''
                j = i + 1
                while j < len(lines):
                    if lines[j].startswith('#'):
                        tags.append(lines[j])
                        j += 1
                        continue
                    uri = lines[j]
                    break
                if uri:
                    segments.append({'tags': tags, 'uri': uri, 'dur': dur})
                    i = j
                else:
                    tail.extend(tags)
            elif line.startswith('#EXT-X-ENDLIST'):
                tail.append(line)
            elif line.startswith('#'):
                if started:
                    pending_tags.append(line)
                else:
                    header.append(line)
            else:
                started = True
                dur = target_duration or 3.0
                segments.append({'tags': pending_tags, 'uri': line, 'dur': dur})
                pending_tags = []
            i += 1
        return header, segments, tail, media_sequence, target_duration

    def _segment_host_key(self, uri, base_url):
        try:
            full = urljoin(base_url, uri)
            p = urlparse(full)
            path = re.sub(r'/[^/]*$', '/', p.path or '/')
            return (p.netloc.lower(), path.lower())
        except:
            return ('', '')

    def _main_path_marker(self, m3u8_url):
        try:
            p = urlparse(m3u8_url).path
            m = re.search(r'(/\d{8}/[^/]+/\d+kb/hls/)', p)
            if m:
                return m.group(1).lower()
            m = re.search(r'(/\d{8}/[^/]+/)', p)
            if m:
                return m.group(1).lower()
        except:
            pass
        return ''

    def _is_ad_segment(self, uri, dur=0, prev_tags=None):
        u = (uri or '').strip().lower()
        if not u:
            return False
        if any(kw in u for kw in AD_KEYWORDS):
            return True
        ad_paths = ['ad', 'ads', 'advert', 'sponsor', 'preroll', '/gg/', '_gg', 'gg_', '/adv/', '/ad/', '/ads/', 'banner', 'promo']
        if any(p in u for p in ad_paths):
            return True
        try:
            if 0 < float(dur) <= 1.2:
                return True
        except:
            pass
        return False

    # ---------- 播放解析 ----------
    def playerContent(self, flag, id, vipFlags):
        m3u8_url = id
        if not m3u8_url.startswith('http'):
            m3u8_url = urljoin(xurl, m3u8_url)

        media_header = {
            "User-Agent": headerx['User-Agent'],
            "Referer": xurl + '/',
            "Origin": xurl
        }

        proxy_url = self._proxy_m3u8_url(m3u8_url, xurl + '/')
        return {
            "parse": 0,
            "playUrl": "",
            "url": proxy_url,
            "header": json.dumps(media_header, ensure_ascii=False)
        }
