import base64
import hashlib
import hmac
import html
import json
import os
import re
import time
from urllib.parse import urlencode

import requests
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

try:
    from base.spider import Spider as BaseSpider
except Exception:
    class BaseSpider:
        pass


class Spider(BaseSpider):
    BASE_URL = "http://43.254.106.169:8167"
    DEVICE_ID = os.urandom(8).hex()
    APP_SIGNATURE = "5F:4A:CC:15:90:58:90:3F:23:88:46:6C:AC:94:01:82:CB:02:0D:AB:49:22:1D:E4:5E:BC:B5:9B:81:29:E5:7A"
    DEFAULT_ACCESS_TOKEN = "10cb267048f8a3442788607fdcbe9b61a72d317ee902f84d2c58d648a9a384a9"
    CHALLENGE_HMAC_KEY = b"e7ed978ee3b971daebe0a8fe6fd3b1f9b0f3da3bafbc91f54da73920df72bf23"
    PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt3JQLXON9M0vBRoiSaKTuxDRnccbNCJHaNA5hM8Ejcq2jnBDxKv7IcSz8fc3WBtQ1EbQ4O3s3xG/dQqc4GMRUjdtC3vNPljLWE3VKakvqj7FH4eiujugK2JQpZniyJipfRqy5w1pUwQVVAQQbK8/RK8gUHZ/zkonGovOr5dnpwAJBrYBjVjiEuS7ZTjaTxcykfmKybqs+bZEJqATBU6LfykaEl6Egn7td1H+OJzbA+XXqwhXhgA8waukNggcsBURJncWKJL4jB+b2Ypv5rfabf6N9q/4xI1nTjFhXp9nnh/mJjZ+7AwN6n3su7riHXtT2yKrljQlrqQEPAV1+7HV7wIDAQAB
-----END PUBLIC KEY-----
"""

    def getName(self):
        return "四叶草（公开版）"

    def init(self, extend=""):
        self.http = requests.Session()
        self.timeout = 15
        config = extend if isinstance(extend, dict) else {}
        if isinstance(extend, str) and extend.strip().startswith("{"):
            try:
                config = json.loads(extend)
            except Exception:
                config = {}
        self.access_token = str(
            config.get("access_token")
            or os.environ.get("ZHUIYI_ACCESS_TOKEN")
            or getattr(self.__class__, "DEFAULT_ACCESS_TOKEN", "")
            or ""
        )
        self.refresh_token = str(
            config.get("refresh_token")
            or os.environ.get("ZHUIYI_REFRESH_TOKEN")
            or ""
        )
        self.session_aes_key = b""
        self.session_hmac_key = b""
        self.session_expires_at = 0
        self.session_auth_token = ""
        self.categories = []
        self.category_filters = {}
        self.categories_expires_at = 0

    def _ensure_init(self):
        if not hasattr(self, "http"):
            self.init("")

    @staticmethod
    def _compact(value):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    @staticmethod
    def _clean(value):
        text = html.unescape(html.unescape(str(value or "")))
        text = re.sub(r"<[^>]*>", " ", text)
        return re.sub(r"\s+", " ", text).strip().replace("$", " ").replace("#", " ")

    @staticmethod
    def _pic(value):
        url = html.unescape(html.unescape(str(value or "").strip()))
        matches = list(re.finditer(r"https?://", url, re.I))
        if len(matches) > 1:
            url = url[matches[-1].start():]
        if url.startswith("//"):
            return "https:" + url
        return url if re.match(r"^https?://", url, re.I) else ""

    def _base_headers(self, auth_token=""):
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) NOX/1.0 Mobile/15E148 Safari/604.1",
            "X-Device-Id": "a7aa66aebec84bc0",
            "X-App-Package": "com.cscblh.ycv",
            "X-App-Signature": self.APP_SIGNATURE,
            "X-App-Version-Code": "3",
            "X-App-Version-Name": "2.7.0",
        }
        if auth_token:
            headers["Authorization"] = "Bearer " + auth_token
        return headers

    @staticmethod
    def _jwt_exp(token):
        try:
            part = str(token).split(".")[1]
            payload = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
            return int(payload.get("exp") or 0)
        except Exception:
            return 0

    @staticmethod
    def _gcm_encrypt(key, plain):
        iv = os.urandom(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
        encrypted, tag = cipher.encrypt_and_digest(plain)
        return iv + encrypted + tag

    @staticmethod
    def _gcm_decrypt(key, payload):
        cipher = AES.new(key, AES.MODE_GCM, nonce=payload[:12], mac_len=16)
        return cipher.decrypt_and_verify(payload[12:-16], payload[-16:])

    def _create_session(self, auth_token=""):
        headers = self._base_headers(auth_token)
        response = self.http.get(
            self.BASE_URL + "/api/captcha/rotate/init",
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        challenge = response.json()["data"]["id"]
        challenge_response = hmac.new(
            self.CHALLENGE_HMAC_KEY,
            f"{challenge}|{self.DEVICE_ID}".encode(),
            hashlib.sha256,
        ).hexdigest()
        temp_key = os.urandom(32)
        request_key = os.urandom(32)
        plain = self._compact(
            {
                "temp_key": base64.b64encode(temp_key).decode(),
                "device_id": self.DEVICE_ID,
                "challenge": challenge,
                "challenge_response": challenge_response,
            }
        ).encode()
        encrypted_key = PKCS1_OAEP.new(
            RSA.import_key(self.PUBLIC_KEY_PEM), hashAlgo=SHA256
        ).encrypt(request_key)
        data = "|".join(
            (
                base64.b64encode(encrypted_key).decode(),
                base64.b64encode(self._gcm_encrypt(request_key, plain)).decode(),
            )
        )
        response = self.http.post(
            self.BASE_URL + "/api/sync/preferences",
            headers={**headers, "Content-Type": "application/json"},
            data=self._compact({"data": data}).encode(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        session = json.loads(
            self._gcm_decrypt(temp_key, base64.b64decode(response.json()["data"]))
        )
        self.session_aes_key = base64.b64decode(session["aes_key"])
        self.session_hmac_key = base64.b64decode(session["hmac_key"])
        self.session_expires_at = int(session["expires_at"])
        self.session_auth_token = auth_token

    def _refresh_tokens(self):
        if not self.refresh_token:
            return False
        result = self._business_once(
            "POST",
            "/api/auth/refresh",
            {"refresh_token": self.refresh_token},
            authenticated=False,
        )
        if result.get("code") != 0 or not isinstance(result.get("data"), dict):
            return False
        data = result["data"]
        self.access_token = str(data.get("access_token") or "")
        self.refresh_token = str(data.get("refresh_token") or self.refresh_token)
        self.session_aes_key = b""
        self.session_hmac_key = b""
        self.session_expires_at = 0
        self.session_auth_token = ""
        return bool(self.access_token)

    def _ensure_access_token(self):
        if self.access_token and self._jwt_exp(self.access_token) > time.time() + 60:
            return
        if self.refresh_token:
            try:
                if self._refresh_tokens():
                    return
            except Exception:
                pass
        self.access_token = ""
        self.refresh_token = ""

    def _ensure_session(self, force=False, authenticated=True):
        self._ensure_init()
        if authenticated:
            self._ensure_access_token()
        auth_token = self.access_token if authenticated else ""
        if (
            force
            or not self.session_aes_key
            or time.time() >= self.session_expires_at - 20
            or self.session_auth_token != auth_token
        ):
            self._create_session(auth_token)

    def _business_once(self, method, target, body="", authenticated=True):
        self._ensure_session(authenticated=authenticated)
        path, _, query = target.partition("?")
        signed_headers = {
            "X-App-Package": "com.recall.app",
            "X-App-Signature": self.APP_SIGNATURE,
            "X-App-Version-Code": "56",
            "X-App-Version-Name": "5.6.0",
        }
        if authenticated and self.access_token:
            signed_headers["Authorization"] = "Bearer " + self.access_token
        body_text = body if isinstance(body, str) else self._compact(body)
        if method.upper() != "GET":
            signed_headers["Content-Type"] = "application/json"
        plain = self._compact(
            {
                "method": method.upper(),
                "path": path,
                "query": query,
                "headers": signed_headers,
                "body": body_text,
            }
        ).encode()
        bundle = base64.b64encode(
            self._gcm_encrypt(self.session_aes_key, plain)
        ).decode()
        timestamp = str(int(time.time() * 1000))
        trace = base64.b64encode(os.urandom(16)).decode()
        token = hmac.new(
            self.session_hmac_key,
            f"{bundle}{timestamp}{trace}".encode(),
            hashlib.sha256,
        ).hexdigest()
        response = self.http.post(
            self.BASE_URL + "/api/sync/push",
            headers={
                "User-Agent": self._base_headers()["User-Agent"],
                "X-Req-Ts": timestamp,
                "X-Req-Id": self.DEVICE_ID,
                "X-Req-Trace": trace,
                "X-Req-Token": token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            data=self._compact({"bundle": bundle}).encode(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        envelope = response.json()
        if "bundle" not in envelope:
            return envelope
        return json.loads(
            self._gcm_decrypt(
                self.session_aes_key, base64.b64decode(envelope["bundle"])
            )
        )

    def _api(self, method, target, body=""):
        last = None
        for attempt in range(2):
            unauthorized = False
            try:
                result = self._business_once(method, target, body)
                if result.get("code") == 0:
                    return result.get("data")
                last = RuntimeError(result.get("msg") or "API 请求失败")
            except Exception as error:
                last = error
                unauthorized = (
                    isinstance(error, requests.HTTPError)
                    and error.response is not None
                    and error.response.status_code == 401
                )
            self.session_aes_key = b""
            self.session_hmac_key = b""
            self.session_expires_at = 0
            self.session_auth_token = ""
            if attempt == 0:
                if unauthorized and self.refresh_token:
                    self.access_token = ""
                    try:
                        self._refresh_tokens()
                    except Exception:
                        pass
                self._ensure_session(force=True)
        raise last or RuntimeError("API 请求失败")

    def _vod(self, item):
        return {
            "vod_id": str(item.get("vod_id") or item.get("id") or ""),
            "vod_name": self._clean(item.get("vod_name") or item.get("name")),
            "vod_pic": self._pic(
                item.get("image_url")
                or item.get("vod_pic")
                or item.get("banner_url")
                or item.get("pic")
            ),
            "vod_remarks": self._clean(item.get("vod_remarks") or item.get("remarks")),
        }

    @staticmethod
    def _page(data, fallback_page=1):
        page = int(data.get("page") or fallback_page)
        limit = int(data.get("limit") or 20)
        total = int(data.get("total") or 0)
        pagecount = max(page, (total + limit - 1) // limit if total else page)
        return page, pagecount, limit, total

    @staticmethod
    def _filter_values(values):
        result = [{"n": "全部", "v": ""}]
        result.extend({"n": str(value), "v": str(value)} for value in values or [])
        return result

    def _load_categories(self):
        if self.categories and time.time() < self.categories_expires_at:
            return
        data = self._api("GET", "/api/categories") or []
        self.categories = [
            {"type_id": str(item.get("type_id")), "type_name": self._clean(item.get("type_name"))}
            for item in data
            if item.get("type_id") is not None
        ]
        filters = {}
        names = {"areas": "地区", "classes": "类型", "years": "年份"}
        for item in data:
            groups = []
            for key in ("areas", "classes", "years"):
                values = (item.get("filters") or {}).get(key) or []
                if values:
                    groups.append(
                        {
                            "key": key,
                            "name": names[key],
                            "init": "",
                            "value": self._filter_values(values),
                        }
                    )
            filters[str(item.get("type_id"))] = groups
        self.category_filters = filters
        self.categories_expires_at = time.time() + 600

    def homeContent(self, filter):
        try:
            self._load_categories()
            data = self._api("GET", "/api/category?type=0&page=1&limit=20") or {}
            return {
                "class": self.categories,
                "list": [self._vod(item) for item in data.get("list") or []],
                "filters": self.category_filters if filter else {},
            }
        except Exception:
            return {"class": self.categories, "list": [], "filters": self.category_filters if filter else {}}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            page = int(pg or 1)
            params = {"type": str(tid), "page": str(page), "limit": "20"}
            for key in ("areas", "classes", "years"):
                value = str((extend or {}).get(key) or "")
                if value:
                    params[key] = value
            data = self._api("GET", "/api/category?" + urlencode(params)) or {}
            current, pages, limit, total = self._page(data, page)
            return {
                "page": current,
                "pagecount": pages,
                "limit": limit,
                "total": total,
                "list": [self._vod(item) for item in data.get("list") or []],
            }
        except Exception:
            return {"page": int(pg or 1), "pagecount": int(pg or 1), "limit": 20, "total": 0, "list": []}

    @staticmethod
    def _encode_play(payload):
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    @staticmethod
    def _decode_play(value):
        text = str(value or "")
        return json.loads(base64.urlsafe_b64decode(text + "=" * (-len(text) % 4)))

    def detailContent(self, ids):
        try:
            vod_id = str(ids[0] if isinstance(ids, (list, tuple)) else ids or "")
            info = self._api("GET", "/api/videos/" + vod_id) or {}
            enabled = [item for item in info.get("play_sources") or [] if int(item.get("is_disabled") or 0) == 0 and item.get("episodes")]
            sources = enabled
            play_from, play_url = [], []
            for source in sources:
                headers = source.get("headers") if isinstance(source.get("headers"), dict) else {}
                referer = headers.get("Referer") or headers.get("referer") or ""
                episodes = []
                for episode in source.get("episodes") or []:
                    payload = self._encode_play(
                        {
                            "u": str(episode.get("url") or ""),
                            "s": str(source.get("source_code") or ""),
                            "r": str(referer),
                            "h": headers,
                        }
                    )
                    episodes.append(f"{self._clean(episode.get('name') or '播放')}${payload}")
                if episodes:
                    play_from.append(self._clean(source.get("source_name") or source.get("source_code") or "线路"))
                    play_url.append("#".join(episodes))
            vod = self._vod(info)
            vod.update(
                {
                    "vod_year": self._clean(info.get("vod_year")),
                    "vod_area": self._clean(info.get("vod_area")),
                    "vod_class": self._clean(info.get("vod_class")),
                    "vod_actor": self._clean(info.get("vod_actor")),
                    "vod_director": self._clean(info.get("vod_director")),
                    "vod_content": self._clean(info.get("vod_blurb")),
                    "vod_play_from": "$$$".join(play_from),
                    "vod_play_url": "$$$".join(play_url),
                }
            )
            return {"list": [vod]} if vod.get("vod_id") else {"list": []}
        except Exception:
            return {"list": []}

    def searchContent(self, key, quick, pg="1"):
        try:
            page = int(pg or 1)
            params = {"keyword": str(key or ""), "page": str(page), "limit": "20"}
            data = self._api("GET", "/api/search?" + urlencode(params)) or {}
            current, pages, limit, total = self._page(data, page)
            return {
                "page": current,
                "pagecount": pages,
                "limit": limit,
                "total": total,
                "list": [self._vod(item) for item in data.get("list") or []],
            }
        except Exception:
            return {"page": int(pg or 1), "pagecount": int(pg or 1), "limit": 20, "total": 0, "list": []}

    def playerContent(self, flag, id, vipFlags):
        try:
            payload = self._decode_play(id)
            data = self._api(
                "POST",
                "/api/videos/parse-url",
                {
                    "url": payload.get("u") or "",
                    "source_code": payload.get("s") or "",
                    "referer": payload.get("r") or "",
                },
            ) or {}
            url = str(data.get("parsed_url") or data.get("original_url") or "")
            headers = data.get("headers") if isinstance(data.get("headers"), dict) else payload.get("h") or {}
            return {"parse": 0, "url": url, "header": headers}
        except Exception:
            return {"parse": 0, "url": str(id or "") if str(id or "").startswith("http") else "", "header": {}}
