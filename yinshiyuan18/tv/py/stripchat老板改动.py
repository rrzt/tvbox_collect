# coding=utf-8
# !/usr/bin/python
import sys
import requests
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):

    def init(self, extend="{}"):
        self.host='https://zh.stripol.com/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
        }

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    def homeContent(self, filter):
        result = {}
        classes = [{'type_name': '女主播', 'type_id': 'girls'}, {'type_name': '情侣', 'type_id': 'couples'}, {'type_name': '男主播', 'type_id': 'men'}, {'type_name': '跨性别', 'type_id': 'trans'}]
        filters = {}
        value = [{'n': '新主播', 'v': 'autoTagNew'},
{'n': '推荐', 'v': 'recommended'},
{"v":"fuckMachine","n":"炮机"},
{'n': '青年', 'v': 'ageTeen'},
{'n': 'VR', 'v': 'autoTagVr'},
{'n': '亚洲人', 'v': 'ethnicityAsian'},
{'n': '🇨🇳中国', 'v': 'tagLanguageChinese'}, {'n': '🇯🇵日本', 'v': 'tagLanguageJapanese'}, {'n': '🇰🇷韩国', 'v': 'tagLanguageKorean'}, {'n': '🇻🇳越南', 'v': 'tagLanguageVietnamese'},{"v":"tagLanguageUkrainian","n":"🇺🇦乌克兰"},
{"v":"tagLanguageRussianSpeaking","n":"🇷🇺俄罗斯"},
{"v":"tagLanguageUSModels","n":"🇺🇸美国"},
{"v":"tagLanguageColombian","n":"🇨🇴哥伦比亚"},
{"v":"tagLanguageGermanSpeaking","n":"🇩🇪德国"},
{"v":"tagLanguageFrench","n":"🇫🇷法国"},
{"v":"tagLanguageUKModels","n":"🇬🇧英国"},
{"v":"tagLanguageCanadian","n":"🇨🇦加拿大"},
{"v":"tagLanguageMexican","n":"🇲🇽墨西哥"},
{"v":"ethnicityIndian","n":"🇮🇳印度"},
{"v":"tagLanguageVenezuelan","n":"🇻🇪委内瑞拉"},
{"v":"tagLanguageRomanian","n":"🇷🇴罗马尼亚"},
{"v":"tagLanguageAfrican","n":"🌍非洲"},
{"v":"tagLanguageSpanishSpeaking","n":"🇪🇸西班牙"},
{"v":"ethnicityMiddleEastern","n":"🇸🇦🇦🇪阿拉伯"},
{"v":"tagLanguageKenyan","n":"🇰🇪肯尼亚"},
{"v":"tagLanguageSouthAfrican","n":"🇿🇦南非"},
{"v":"tagLanguageBrazilian","n":"🇧🇷巴西"},
{"v":"tagLanguageThai","n":"🇹🇭泰国"},
{"v":"tagLanguageItalian","n":"🇮🇹意大利"},
{'n': '亚洲', 'v': 'ethnicityAsian'}, {'n': '白人', 'v': 'ethnicityWhite'}, {'n': '拉丁', 'v': 'ethnicityLatino'}, {'n': '混血', 'v': 'ethnicityMultiracial'}, {'n': '印度', 'v': 'ethnicityIndian'}, {'n': '阿拉伯', 'v': 'ethnicityMiddleEastern'}, {'n': '黑人', 'v': 'ethnicityEbony'},{'n': '✨新主播', 'v': 'autoTagNew'},{'n': 'VR直播', 'v': 'autoTagVr'},{'n': '18+', 'v': 'ageTeen'},{'n': '鲜嫩青年22+', 'v': 'ageYoung'},{'n': '学生', 'v': 'subcultureStudent'},{'n': '口交', 'v': 'doBlowjob'},{'n': '深喉', 'v': 'doDeepThroat'},{'n': '恋足', 'v': 'doFootFetish'},{'n': '互动玩具', 'v': 'autoTagInteractiveToy'},{'n': '自慰', 'v': 'doMasturbation'},{'n': '肛交', 'v': 'doAnal'},{'n': '潮吹', 'v': 'doSquirt'},{'n': '狗式', 'v': 'doDoggyStyle'},{'n': 'Cosplay', 'v': 'doCosplay'},{'n': 'RolePlay', 'v': 'doRolePlay'}]
        value_gay = [{'n': '情侣', 'v': 'sexGayCouples'}, {'n': '直男', 'v': 'orientationStraight'}]
        for tid in ['girls', 'couples', 'men', 'trans']:
            c_value = value[:]
            if tid == 'men':
                c_value += value_gay
            filters[tid] = [{'key': 'tag', 'value': c_value}]
        result['class'] = classes
        result['filters'] = filters
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        limit = 60
        offset = limit * (int(pg) - 1)
        domain = f"{self.host}api/front/models?improveTs=false&removeShows=false&limit={limit}&offset={offset}&primaryTag={tid}&sortBy=viewersRating&rcmGrp=A&rbCnGr=true&prxCnGr=false&nic=false"
        
        if 'tag' in extend:
            domain += "&filterGroupTags=%5B%5B%22" + extend['tag'] + "%22%5D%5D"
        
        rsp = requests.get(domain, headers=self.headers).json()
        vodList = rsp.get('models', [])
        videos = []
        
        for vod in vodList:
            username = str(vod.get('username', '')).strip()
            id = str(vod.get('id', ''))
            stamp = vod.get('snapshotTimestamp')
            
            # 在线人数
            viewers = vod.get('viewersCount', 0)
            viewers_str = f"{viewers}人在看" if viewers > 0 else ""
            
            # 标签
            tags = vod.get('tags', [])
            tag_str = " | ".join([str(t) for t in tags[:3]]) if tags else ""
            
            # ==================== 加强版 groupShowType 判断 ====================
            group_type = vod.get('groupShowType')
            
            # 转为字符串并清理
            g = str(group_type).strip() if group_type is not None else ""
            
            if g == "" or g.lower() == "none" or g.lower() == "null":
                show_type = "免费直播"
            elif g.lower() == "ticket":
                show_type = "🎫个人购票表演中"
            elif g.lower() == "perminute" or g.lower() == "per_minute":
                show_type = "🎫团体购票表演中"
            else:
                # 其他任何非空值都视为买票表演
                show_type = "🎫收费表演中"
            # =================================================================
            
            # 组合副标题
            remarks = [item for item in [tag_str, viewers_str, show_type] if item]
            
            videos.append({
                "vod_id": username,
                "vod_name": username,
                "vod_pic": f"https://img.doppiocdn.net/thumbs/{stamp}/{id}" if stamp and id else "",
                "vod_remarks": " | ".join(remarks)
            })
        
        total = int(rsp.get('filteredCount', 0))
        result = {
            'list': videos,
            'page': int(pg),
            'pagecount': (total + limit - 1) // limit,
            'limit': limit,
            'total': total
        }
        return result

    def detailContent(self, array):
        username = array[0]
        domain = f"{self.host}api/front/v2/models/username/{username}/cam"
        rsp = requests.get(domain, headers=self.headers).json()
        info = rsp['cam']
        user = rsp['user']['user']
        id = str(user['id'])
        vod = {
            "vod_id": id,
            "vod_name": str(info['topic']).strip(), 
            "vod_pic": str(user['avatarUrl']),
            "vod_director": username,
            "vod_area": str(user['country']),
             "vod_actor": username,          # 作者（演员），与导演相同
        "vod_content": f"{self.host}{username}#长按复制到浏览器观看",     # 简介内容为链接
            'vod_play_from': '飞鱼在线',
            'vod_play_url': f"高清播放${id}"
        }
        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick, pg="1"):
        pass

    def playerContent(self, flag, id, vipFlags):
        domain = f"https://edge-hls.growcdnssedge.com/hls/{id}/master/{id}_auto.m3u8?playlistType=lowLatency"
        rsp = requests.get(domain, headers=self.headers).text
        lines = rsp.strip().split('\n')
        psch = ''
        pkey = ''
        url = []
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-MOUFLON:'):
                parts = line.split(':')
                if len(parts) >= 4:
                    psch = parts[2]
                    pkey = parts[3]
            if '#EXT-X-STREAM-INF' in line:
                name_start = line.find('NAME="') + 6
                name_end = line.find('"', name_start)
                qn = line[name_start:name_end]
                # URL在下一行
                url_base = lines[i + 1]
                # 组合最终的URL，并加上psch和pkey参数
                full_url = f"{url_base}&psch={psch}&pkey={pkey}"
                # 将画质和URL添加到列表中
                url.append(qn)
                url.append(full_url)
        result = {}
        result["url"] = url
        result["parse"] = '0'
        result["contentType"] = ''
        result["header"] = self.headers
        return result

    def localProxy(self, param):
        pass
