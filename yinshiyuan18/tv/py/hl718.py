import sys,json,re,requests,threading,socket
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import quote,unquote
sys.path.append('..')
from base.spider import Spider as _BaseSpider

_proxy_port=0
_proxy_started=False
_proxy_session=None

def _start_proxy():
    global _proxy_port,_proxy_started,_proxy_session
    if _proxy_started:return
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('127.0.0.1',0))
    _proxy_port=s.getsockname()[1]
    s.close()
    _proxy_session=requests.Session()
    _proxy_session.verify=False
    threading.Thread(target=lambda:HTTPServer(('127.0.0.1',_proxy_port),_ProxyHandler).serve_forever(),daemon=True).start()
    _proxy_started=True

class _ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self,format,*args):pass
    def do_GET(self):
        url=unquote(self.path.lstrip('/'))
        if not url or not url.startswith('http'):
            self.send_response(404);self.end_headers();return
        try:
            r=_proxy_session.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','Referer':'https://www.hl718.com/'},timeout=15)
            data=r.content
            ct=r.headers.get('Content-Type','')
            # webp 转 jpg（纯 Python，无外部依赖）
            if 'webp' in ct or url.endswith('.webp'):
                converted=self._webp_to_jpeg(data)
                if converted:
                    data=converted
                    ct='image/jpeg'
            self.send_response(200)
            self.send_header('Content-Type',ct)
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Content-Length',str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except:
            self.send_response(404);self.end_headers()
    def _webp_to_jpeg(self,data):
        """webp→jpg 转换（优先 Pillow，备用 ffmpeg）"""
        # 方法1: Pillow
        try:
            from PIL import Image
            from io import BytesIO
            img=Image.open(BytesIO(data))
            if img.mode in ('RGBA','P'):
                img=img.convert('RGB')
            buf=BytesIO()
            img.save(buf,format='JPEG',quality=85)
            return buf.getvalue()
        except ImportError:
            pass
        except:
            pass
        # 方法2: ffmpeg（处理 RGBA→RGB）
        try:
            import subprocess,tempfile,os
            with tempfile.NamedTemporaryFile(suffix='.webp',delete=False) as f:
                f.write(data)
                webp_path=f.name
            jpg_path=webp_path.replace('.webp','.jpg')
            subprocess.run(['ffmpeg','-y','-i',webp_path,'-vf','format=yuvj420p','-q:v','2',jpg_path],capture_output=True,timeout=10)
            if os.path.exists(jpg_path):
                with open(jpg_path,'rb') as f:result=f.read()
                os.unlink(jpg_path)
                os.unlink(webp_path)
                return result
            os.unlink(webp_path)
        except:pass
        return None

class Spider(_BaseSpider):
    def getName(self):return "黑料718"
    def isVideoFormat(self,url):
        if not url:return False
        if url.startswith(('novel://','text://','pics://','book_','comic_')):return False
        return '.mp4' in url or '.m3u8' in url or '.ts' in url
    def manualVideoCheck(self):return False
    def destroy(self):pass
    def localProxy(self,param):return None

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','Referer':'https://www.hl718.com/'}
    host='https://www.hl718.com'
    cdn='https://pass.saxinx.cn'
    cat_map={
        'daily-gossip':'每日黑料','top-stories':'黑料热榜','entertainment-news':'娱乐黑料',
        'celebrity-scandals':'明星黑料','hljh':'黑料精华','wanghuang':'网黄合集',
        'internet-celebrities':'网红吃瓜','model-photos':'福利姬料','daily-contest':'每日大赛',
        'trending-news':'社会吃瓜','contrast-reveal':'反差婊们','zsll':'真实乱伦','AICG':'AI短剧成人'
    }

    def init(self,extend=""):
        _start_proxy()
        self.session=requests.Session()
        self.session.verify=False

    def _get(self,url):
        r=self.session.get(url,headers=self.headers,timeout=15)
        r.encoding=r.apparent_encoding
        return r.text

    def _clean_pic(self,pic):
        """图片通过代理访问（webp 转 jpg）"""
        if not pic:return ''
        if pic.startswith('http'):return f'http://127.0.0.1:{_proxy_port}/{pic}'
        if pic.startswith('/'):return f'http://127.0.0.1:{_proxy_port}/{self.cdn}{pic}'
        return f'http://127.0.0.1:{_proxy_port}/{self.cdn}/{pic}'

    def _parse_list(self,html):
        items=[]
        for block in re.finditer(r'<article[^>]*>(.*?)</article>',html,re.S):
            b=block.group(1)
            pid_m=re.search(r'archives/(\d+)',b)
            if not pid_m:continue
            pid=pid_m.group(1)
            title_m=re.search(r'<h2[^>]*>(.*?)</h2>',b,re.S)
            if not title_m:continue
            title=re.sub(r'<[^>]+>','',title_m.group(1)).strip()
            title=re.sub(r'\s*(热搜\s*HOT|HOT)\s*','',title).strip()
            if len(title)<3 or '蟹老板' in title or '赞助' in title:continue
            # 封面图
            pic=''
            pic_m=re.search(r'data-pic="([^"]+)"',b)
            if pic_m:pic=pic_m.group(1).strip()
            if not pic:
                pic_m=re.search(r'meta itemprop="image" content="([^"]+)"',b)
                if pic_m:pic=pic_m.group(1).strip()
            img=self._clean_pic(pic)
            items.append({"vod_id":pid,"vod_name":title,"vod_pic":img})
        return items

    def homeContent(self,filter):
        try:
            cats=[{'type_id':k,'type_name':v} for k,v in self.cat_map.items()]
            return {"class":cats,"list":[],"filters":{}}
        except:
            return {"class":[],"filters":{},"list":[],"page":1,"pagecount":1}

    def homeVideoContent(self):
        try:
            html=self._get(self.host)
            return {"list":self._parse_list(html)[:20]}
        except:
            return {"list":[]}

    def categoryContent(self,tid,pg,filter,extend):
        try:
            page=int(pg) if pg else 1
            url=f"{self.host}/category/{tid}/" if page==1 else f"{self.host}/category/{tid}/page/{page}/"
            html=self._get(url)
            # 解析分页
            page_section=re.search(r'<(?:ol|ul|div)[^>]*class="[^"]*(?:pagination|page-navigator|pager)[^"]*"[^>]*>(.*?)</(?:ol|ul|div)>',html,re.S)
            max_page=page
            if page_section:
                nums=re.findall(r'<a[^>]*>\s*(\d+)\s*</a>',page_section.group(1))
                if nums:max_page=max(int(n) for n in nums)
            return {"page":page,"pagecount":max_page,"list":self._parse_list(html)}
        except:
            return {"page":int(pg) if pg else 1,"pagecount":1,"list":[]}

    def detailContent(self,ids):
        try:
            id=ids[0]
            html=self._get(f"{self.host}/archives/{id}")
            title_m=re.search(r'<h1[^>]*class="post-title[^"]*"[^>]*>(.*?)</h1>',html,re.S)
            title=re.sub(r'<[^>]+>','',title_m.group(1)).strip() if title_m else ''
            post_m=re.search(r'<div class="post-content"[^>]*>(.*?)</article>',html,re.S)
            post=post_m.group(1) if post_m else ''

            # 提取图片
            img_urls=[]
            for m in re.finditer(r"data-pic=['\"]([^'\"]+)['\"]",post):
                u=m.group(1).strip()
                if u and '/XPic/' not in u and '/images/' not in u and 'banner' not in u.lower():
                    img_urls.append(self._clean_pic(u))

            # 提取视频
            video_url=''
            dp=re.search(r"data-config='([^']+)'",html)
            if dp:
                config_str=dp.group(1).replace('&quot;','"').replace('&amp;','&')
                u2=re.search(r'"url2":"((?:[^"\\]|\\.)*)"',config_str)
                if u2:
                    raw=u2.group(1).replace('\\/','/')
                    if raw and raw.startswith('http'):video_url=raw
                if not video_url:
                    u1=re.search(r'"url":"((?:[^"\\]|\\.)*)"',config_str)
                    if u1:
                        raw=u1.group(1).replace('\\/','/')
                        if raw and raw.startswith('http'):video_url=raw

            # 封面图：取第一张内容图
            pic=img_urls[0] if img_urls else self._clean_pic('/usr/themes/Mirages/images/logo.webp')

            # 构建播放信息
            from_names=[]
            ep_parts=[]
            if img_urls:
                from_names.append('图文')
                ep_parts.append(f'图片$pics://{"&&".join(img_urls)}')
            if video_url:
                from_names.append('视频')
                ep_parts.append(f'播放${video_url}')

            if from_names:
                vod={"vod_id":id,"vod_name":title,"vod_remarks":"","vod_pic":pic,"vod_content":title[:500],"vod_play_from":"$$$".join(from_names),"vod_play_url":"$$$".join(ep_parts)}
            else:
                c=re.sub(r'<[^>]+>',' ',post).strip()[:500]
                vod={"vod_id":id,"vod_name":title,"vod_remarks":"","vod_pic":pic,"vod_content":c,"vod_play_from":"文字","vod_play_url":f"阅读${c[:300]}"}
            return {"list":[vod]}
        except:
            return {"list":[]}

    def searchContent(self,key,quick,pg="1"):
        try:
            page=int(pg) if pg else 1
            url=f"{self.host}/search/{quote(key)}/" if page==1 else f"{self.host}/search/{quote(key)}/page/{page}/"
            html=self._get(url)
            return {"list":self._parse_list(html),"page":page}
        except:
            return {"list":[],"page":int(pg) if pg else 1}

    def playerContent(self,flag,id,vipFlags):
        try:
            if flag=='图文' or id.startswith('pics://'):
                return {"parse":0,"playUrl":"","url":id.replace('图片',''),"header":self.headers,"position":"0"}
            if flag=='视频' or '播放' in id:
                url=id.replace('播放','')
                if '$$$' in url:url=url.split('$$$')[-1]
                return {"parse":0,"url":url,"header":self.headers,"position":"0"}
            if flag=='文字' or '阅读' in id:
                content=id.replace('阅读','')
                if '$$$' in content:content=content.split('$$$')[-1]
                nj=json.dumps({"title":content[:50],"content":content},ensure_ascii=False)
                return {"parse":0,"url":f"novel://{nj}","header":"","vod_player":"书","position":"0"}
            if id.startswith('pics://'):
                return {"parse":0,"playUrl":"","url":id,"header":self.headers,"position":"0"}
            if id.startswith('http'):
                return {"parse":0,"url":id,"header":self.headers,"position":"0"}
            return {"parse":0,"url":id,"header":self.headers,"position":"0"}
        except:
            return {"parse":0,"url":"","position":"0"}
