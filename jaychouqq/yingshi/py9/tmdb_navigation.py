# -*- coding: utf-8 -*-
# //@name:TMDB导航
# //@id:tmdb_navigation
# //@version:1

import json
import re
import threading
import time
from collections import OrderedDict
from urllib.parse import quote, urlencode

import requests
from requests.adapters import HTTPAdapter

from base.spider import Spider as BaseSpider


class Spider(BaseSpider):
    name = "TMDB导航"
    host = "https://www.themoviedb.org"
    backend_parse = False
    category_mode = False
    categoryMode = False

    API = "https://api.themoviedb.org/3"
    IMAGE = "https://image.tmdb.org/t/p/w500"
    NOTICE_PREFIX = "tmdb-nav:notice:"

    CATEGORIES = (
        ("trending", "本周趋势"),
        ("movie_discover", "电影"),
        ("tv_discover", "剧集"),
        ("anime", "动漫"),
        ("movie_popular", "热门电影"),
        ("movie_now", "正在上映"),
        ("movie_upcoming", "即将上映"),
        ("movie_top", "高分电影"),
        ("tv_popular", "热门剧集"),
        ("tv_airing", "今日播出"),
        ("tv_on_air", "正在播出"),
        ("tv_top", "高分剧集"),
    )

    REGION_GROUPS = (
        ("全部地区", ""),
        ("日韩", "JP|KR"),
        ("欧美", "US|GB|FR|DE|ES|IT|CA|AU"),
        ("国产", "CN|HK|TW"),
        ("东南亚", "TH|SG|MY|PH|ID|VN"),
    )
    REGIONS = (
        ("全部地区", ""), ("中国大陆", "CN"), ("中国香港", "HK"),
        ("中国台湾", "TW"), ("日本", "JP"), ("韩国", "KR"),
        ("美国", "US"), ("英国", "GB"), ("法国", "FR"),
        ("德国", "DE"), ("西班牙", "ES"), ("意大利", "IT"),
        ("加拿大", "CA"), ("澳大利亚", "AU"), ("泰国", "TH"),
        ("新加坡", "SG"), ("马来西亚", "MY"), ("菲律宾", "PH"),
        ("印度尼西亚", "ID"), ("越南", "VN"), ("印度", "IN"),
        ("俄罗斯", "RU"), ("巴西", "BR"), ("墨西哥", "MX"),
        ("土耳其", "TR"),
    )
    ANIME_REGIONS = (("国漫", "CN"), ("日漫", "JP"), ("韩漫", "KR"), ("美漫", "US"))
    MOVIE_GENRES = (
        ("全部类型", ""), ("动作", "28"), ("冒险", "12"), ("动画", "16"),
        ("喜剧", "35"), ("犯罪", "80"), ("纪录片", "99"), ("剧情", "18"),
        ("家庭", "10751"), ("奇幻", "14"), ("历史", "36"), ("恐怖", "27"),
        ("音乐", "10402"), ("悬疑", "9648"), ("爱情", "10749"),
        ("科幻", "878"), ("惊悚", "53"), ("战争", "10752"), ("西部", "37"),
    )
    TV_GENRES = (
        ("全部类型", ""), ("动作冒险", "10759"), ("动画", "16"), ("喜剧", "35"),
        ("犯罪", "80"), ("纪录片", "99"), ("剧情", "18"), ("家庭", "10751"),
        ("儿童", "10762"), ("悬疑", "9648"), ("真人秀", "10764"),
        ("科幻奇幻", "10765"), ("肥皂剧", "10766"), ("脱口秀", "10767"),
        ("战争政治", "10768"), ("西部", "37"),
    )
    MOVIE_SORTS = (
        ("热度", "popularity.desc"), ("更新时间", "primary_release_date.desc"),
        ("评分", "vote_average.desc"), ("票房", "revenue.desc"),
    )
    TV_SORTS = (
        ("热度", "popularity.desc"), ("更新时间", "first_air_date.desc"),
        ("评分", "vote_average.desc"),
    )
    LANGUAGES = (
        ("全部语言", ""), ("中文", "zh"), ("日语", "ja"), ("韩语", "ko"),
        ("英语", "en"), ("法语", "fr"), ("德语", "de"), ("西班牙语", "es"),
        ("印地语", "hi"), ("泰语", "th"),
    )
    RATINGS = (("不限评分", ""), ("6分以上", "6"), ("7分以上", "7"), ("8分以上", "8"), ("9分以上", "9"))
    VOTE_COUNTS = (("不限人数", ""), ("20票以上", "20"), ("50票以上", "50"), ("100票以上", "100"), ("500票以上", "500"))
    RUNTIMES = (("不限片长", ""), ("90分钟内", "short"), ("90-120分钟", "medium"), ("120分钟以上", "long"))

    def __init__(self):
        self.api_base = self.API
        self.image_base = self.IMAGE
        self.access_token = ""
        self.api_key = ""
        self.language = "zh-CN"
        self.region = "CN"
        self.timeout = 15
        self.list_cache_ttl = 300
        self.detail_cache_ttl = 21600
        self.stale_ttl = 86400
        self.cache_max_entries = 256
        self.verify_tls = True
        self.trust_env = True
        self.user_agent = "TMDB-Navigation-Spider/1.0"
        self._cache = OrderedDict()
        self._cache_lock = threading.RLock()
        self._session = None
        self._reset_session()

    def getName(self):
        return self.name

    def init(self, extend=""):
        config = self._parse_config(extend)
        self.access_token = self._first(config, "access_token", "accessToken", "readAccessToken", "bearerToken", "token")
        self.api_key = self._first(config, "api_key", "apiKey", "apikey", "tmdbApiKey", "key")
        self.api_base = self._https_base(config.get("api_base") or config.get("apiBase"), self.API)
        self.image_base = self._https_base(config.get("image_base") or config.get("imageBase"), self.IMAGE)
        self.language = str(config.get("language") or "zh-CN").strip() or "zh-CN"
        self.region = str(config.get("region") or "CN").strip().upper() or "CN"
        self.timeout = self._bounded_int(config.get("timeout"), 15, 5, 45)
        self.list_cache_ttl = self._bounded_int(config.get("list_cache_ttl"), 300, 30, 3600)
        self.detail_cache_ttl = self._bounded_int(config.get("detail_cache_ttl"), 21600, 300, 604800)
        self.stale_ttl = self._bounded_int(config.get("stale_ttl"), 86400, 300, 604800)
        self.cache_max_entries = self._bounded_int(config.get("cache_max_entries"), 256, 32, 1024)
        self.verify_tls = self._bool_value(config.get("verify_tls"), True)
        self.trust_env = self._bool_value(config.get("trust_env"), True)
        ua = str(config.get("user_agent") or "").strip()
        if ua:
            self.user_agent = ua
        with self._cache_lock:
            self._cache.clear()
        self._reset_session()

    def destroy(self):
        if self._session is not None:
            try:
                self._session.close()
            except Exception:
                pass

    def homeContent(self, filter=False):
        result = {"class": [{"type_id": key, "type_name": name} for key, name in self.CATEGORIES]}
        if filter:
            result["filters"] = self._filters()
        return result

    def homeVideoContent(self):
        try:
            data = self._api("/trending/all/day", {"page": 1}, self.list_cache_ttl)
            return {"list": self._cards(data.get("results"), "")}
        except Exception as exc:
            return {"list": [self._notice_card("TMDB 导航未就绪", exc)]}

    def categoryContent(self, tid, pg, filter=False, extend=None):
        page = self._positive_int(pg, 1)
        ext = self._parse_extend(extend)
        try:
            if tid == "trending":
                media = self._value(ext, "media", "all")
                if media not in ("all", "movie", "tv"):
                    media = "all"
                window = self._value(ext, "window", "week")
                if window not in ("day", "week"):
                    window = "week"
                return self._list_endpoint("/trending/%s/%s" % (media, window), page, media if media != "all" else "")
            fixed = {
                "movie_popular": ("/movie/popular", "movie"),
                "movie_now": ("/movie/now_playing", "movie"),
                "movie_upcoming": ("/movie/upcoming", "movie"),
                "movie_top": ("/movie/top_rated", "movie"),
                "tv_popular": ("/tv/popular", "tv"),
                "tv_airing": ("/tv/airing_today", "tv"),
                "tv_on_air": ("/tv/on_the_air", "tv"),
                "tv_top": ("/tv/top_rated", "tv"),
            }
            if tid in fixed:
                path, media_type = fixed[tid]
                params = {"region": self._value(ext, "region", self.region)} if media_type == "movie" else {}
                return self._list_endpoint(path, page, media_type, params)
            if tid == "movie_discover":
                return self._discover("movie", page, ext)
            if tid == "tv_discover":
                return self._discover("tv", page, ext)
            if tid == "anime":
                return self._anime(page, ext)
            return self._page_result([], page, page, 0)
        except Exception as exc:
            return self._page_result([self._notice_card("TMDB 分类载入失败", exc)], page, page, 1)

    def detailContent(self, ids):
        media_type, tmdb_id = self._decode_id(self._first_id(ids))
        if not media_type or not tmdb_id:
            return {"list": []}
        try:
            data = self._api("/%s/%s" % (media_type, tmdb_id), {"append_to_response": "credits"}, self.detail_cache_ttl)
            title = self._title(data)
            original = str(data.get("original_title") or data.get("original_name") or "").strip()
            display = title if not original or original == title else title + " / " + original
            credits = data.get("credits") or {}
            cast = [str(item.get("name")) for item in (credits.get("cast") or [])[:12] if item.get("name")]
            crew = credits.get("crew") or []
            directors = [str(item.get("name")) for item in crew if item.get("job") in ("Director", "Creator") and item.get("name")][:6]
            genres = [str(item.get("name")) for item in data.get("genres") or [] if item.get("name")]
            countries = [str(item.get("name")) for item in data.get("production_countries") or [] if item.get("name")]
            if media_type == "tv" and not countries:
                countries = [str(v) for v in data.get("origin_country") or []]
            date = str(data.get("release_date") or data.get("first_air_date") or "")
            remarks = self._remark(data, media_type)
            vod = {
                "vod_id": self._encode_id(media_type, tmdb_id),
                "vod_name": display,
                "vod_pic": self._image(data.get("poster_path") or data.get("backdrop_path")),
                "type_name": ", ".join(genres),
                "vod_year": date[:4],
                "vod_area": ", ".join(countries),
                "vod_remarks": remarks,
                "vod_actor": ", ".join(cast),
                "vod_director": ", ".join(directors),
                "vod_content": str(data.get("overview") or "").strip(),
                "vod_play_from": "",
                "vod_play_url": "",
            }
            return {"list": [vod]}
        except Exception as exc:
            return {"list": [self._notice_card("TMDB 详情载入失败", exc)]}

    def searchContent(self, key, quick=False, pg="1"):
        return {"list": []}

    def playerContent(self, flag, id, vipFlags=None):
        return {
            "parse": 0,
            "jx": 0,
            "playUrl": "",
            "url": "",
            "header": {},
            "msg": "TMDB 仅提供影视资料，请使用全局搜索查找播放源",
        }

    def localProxy(self, param):
        return [404, "text/plain; charset=utf-8", "not found"]

    def action(self, action):
        value = str(action or "")
        if value.startswith(self.NOTICE_PREFIX):
            return json.dumps({"msg": value[len(self.NOTICE_PREFIX):]}, ensure_ascii=False)
        return json.dumps({"msg": "不支持的 TMDB 导航操作"}, ensure_ascii=False)

    def _list_endpoint(self, path, page, media_type, extra=None):
        params = {"page": page}
        params.update(extra or {})
        data = self._api(path, params, self.list_cache_ttl)
        return self._page_from_api(data, page, media_type)

    def _discover(self, media_type, page, ext):
        sort_default = "popularity.desc"
        params = {
            "page": page,
            "sort_by": self._value(ext, "sort", sort_default),
            "with_genres": self._value(ext, "genre", ""),
            "include_adult": "false",
            "include_video": "false",
        }
        country = self._value(ext, "country", "")
        region = country or self._value(ext, "area", "")
        year = self._value(ext, "year", "")
        language = self._value(ext, "language", "")
        rating = self._value(ext, "rating", "")
        vote_count = self._value(ext, "votes", "")
        runtime = self._value(ext, "runtime", "")
        if media_type == "movie":
            if region:
                params["with_origin_country"] = region
            if country:
                params["region"] = country
            if year:
                params["primary_release_year"] = year
        else:
            if region:
                params["with_origin_country"] = region
            if year:
                params["first_air_date_year"] = year
        if language:
            params["with_original_language"] = language
        if rating:
            params["vote_average.gte"] = rating
        if vote_count:
            params["vote_count.gte"] = vote_count
        elif params["sort_by"] == "vote_average.desc":
            params["vote_count.gte"] = 50
        if runtime == "short":
            params["with_runtime.lte"] = 90
        elif runtime == "medium":
            params["with_runtime.gte"] = 90
            params["with_runtime.lte"] = 120
        elif runtime == "long":
            params["with_runtime.gte"] = 120
        data = self._api("/discover/" + media_type, params, self.list_cache_ttl)
        return self._page_from_api(data, page, media_type)

    def _anime(self, page, ext):
        media_type = self._value(ext, "kind", "tv")
        if media_type not in ("movie", "tv"):
            media_type = "tv"
        region = self._value(ext, "region", "JP")
        sort = self._value(ext, "sort", "popularity.desc")
        year = self._value(ext, "year", "")
        params = {
            "page": page,
            "sort_by": sort,
            "with_genres": "16",
            "with_origin_country": region,
            "include_adult": "false",
        }
        if media_type == "movie":
            params["region"] = region
            if year:
                params["primary_release_year"] = year
        elif year:
            params["first_air_date_year"] = year
        if sort == "vote_average.desc":
            params["vote_count.gte"] = 20
        data = self._api("/discover/" + media_type, params, self.list_cache_ttl)
        return self._page_from_api(data, page, media_type)

    def _page_from_api(self, data, page, media_type):
        items = self._cards(data.get("results"), media_type)
        pagecount = self._positive_int(data.get("total_pages"), page)
        total = self._positive_int(data.get("total_results"), len(items))
        return self._page_result(items, page, min(500, max(page, pagecount)), total)

    def _cards(self, items, forced_type):
        result = []
        for raw in items or []:
            media_type = forced_type or str(raw.get("media_type") or "")
            if media_type not in ("movie", "tv"):
                media_type = "movie" if raw.get("title") or raw.get("release_date") else "tv"
            title = self._title(raw)
            tmdb_id = self._positive_int(raw.get("id"), 0)
            if not title or not tmdb_id:
                continue
            result.append({
                "vod_id": self._encode_id(media_type, tmdb_id),
                "vod_name": title,
                "vod_pic": self._image(raw.get("poster_path") or raw.get("backdrop_path")),
                "vod_remarks": self._remark(raw, media_type),
            })
        return result

    def _filters(self):
        years = [("全部年代", "")] + [(str(year), str(year)) for year in range(time.localtime().tm_year + 1, 1979, -1)]
        return {
            "trending": [
                self._filter("media", "内容", (("全部", "all"), ("电影", "movie"), ("剧集", "tv"))),
                self._filter("window", "周期", (("今日", "day"), ("本周", "week"))),
            ],
            "movie_popular": [self._filter("region", "地区", self.REGIONS)],
            "movie_now": [self._filter("region", "地区", self.REGIONS)],
            "movie_upcoming": [self._filter("region", "地区", self.REGIONS)],
            "movie_top": [self._filter("region", "地区", self.REGIONS)],
            "tv_popular": [], "tv_airing": [], "tv_on_air": [], "tv_top": [],
            "movie_discover": [
                self._filter("area", "大区", self.REGION_GROUPS),
                self._filter("country", "国家/地区", self.REGIONS),
                self._filter("sort", "排序", self.MOVIE_SORTS),
                self._filter("genre", "类型", self.MOVIE_GENRES),
                self._filter("year", "年代", years),
                self._filter("language", "原始语言", self.LANGUAGES),
                self._filter("rating", "最低评分", self.RATINGS),
                self._filter("votes", "评分人数", self.VOTE_COUNTS),
                self._filter("runtime", "片长", self.RUNTIMES),
            ],
            "tv_discover": [
                self._filter("area", "大区", self.REGION_GROUPS),
                self._filter("country", "国家/地区", self.REGIONS),
                self._filter("sort", "排序", self.TV_SORTS),
                self._filter("genre", "类型", self.TV_GENRES),
                self._filter("year", "年代", years),
                self._filter("language", "原始语言", self.LANGUAGES),
                self._filter("rating", "最低评分", self.RATINGS),
                self._filter("votes", "评分人数", self.VOTE_COUNTS),
                self._filter("runtime", "单集片长", self.RUNTIMES),
            ],
            "anime": [
                self._filter("sort", "排序", self.TV_SORTS),
                self._filter("region", "地区", self.ANIME_REGIONS),
                self._filter("kind", "内容", (("动画剧集", "tv"), ("动画电影", "movie"))),
                self._filter("year", "年代", years),
            ],
        }

    def _api(self, path, params=None, ttl=None):
        if not self.access_token and not self.api_key:
            raise RuntimeError("请在插件 Extend 配置个人 TMDB access_token 或 api_key")
        query = dict(params or {})
        query.setdefault("language", self.language)
        if not self.access_token:
            query["api_key"] = self.api_key
        cache_query = {key: value for key, value in query.items() if key != "api_key"}
        key = "json:" + path + "?" + urlencode(sorted(cache_query.items()), doseq=True)
        ttl = self.list_cache_ttl if ttl is None else ttl
        cached = self._cache_get(key, ttl)
        if cached is not None:
            return cached
        stale = self._cache_get(key, self.stale_ttl, allow_expired=True)
        try:
            response = self._session.get(self.api_base + path, params=query, timeout=self.timeout, verify=self.verify_tls)
            try:
                data = response.json()
            except Exception:
                raise RuntimeError("TMDB 返回了非 JSON 内容")
            if response.status_code in (401, 403):
                raise RuntimeError("TMDB API 凭据无效或无权访问")
            if response.status_code == 429:
                raise RuntimeError("TMDB API 请求过于频繁，请稍后刷新")
            if response.status_code != 200:
                raise RuntimeError(str(data.get("status_message") or "TMDB HTTP %s" % response.status_code))
            if not isinstance(data, dict):
                raise RuntimeError("TMDB API 响应结构异常")
            self._cache_set(key, data)
            return data
        except Exception:
            if stale is not None:
                return stale
            raise

    def _reset_session(self):
        if self._session is not None:
            try:
                self._session.close()
            except Exception:
                pass
        session = requests.Session()
        session.trust_env = self.trust_env
        session.headers.update({"Accept": "application/json", "User-Agent": self.user_agent})
        if self.access_token:
            session.headers["Authorization"] = "Bearer " + self.access_token
        try:
            from requests.packages.urllib3.util.retry import Retry
            retry = Retry(total=2, connect=2, read=2, status=2, backoff_factor=0.35, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset(("GET",)))
            adapter = HTTPAdapter(max_retries=retry, pool_connections=8, pool_maxsize=8)
        except TypeError:
            adapter = HTTPAdapter(max_retries=2, pool_connections=8, pool_maxsize=8)
        session.mount("https://", adapter)
        self._session = session

    def _cache_get(self, key, ttl, allow_expired=False):
        with self._cache_lock:
            item = self._cache.get(key)
            if not item:
                return None
            created, value = item
            age = time.time() - created
            if age > ttl:
                return value if allow_expired and age <= self.stale_ttl else None
            self._cache.move_to_end(key)
            return value

    def _cache_set(self, key, value):
        with self._cache_lock:
            self._cache[key] = (time.time(), value)
            self._cache.move_to_end(key)
            while len(self._cache) > self.cache_max_entries:
                self._cache.popitem(last=False)

    def _notice_card(self, title, exc):
        message = self._short_error(exc)
        return {
            "vod_id": "tmdb-notice",
            "vod_name": title,
            "vod_pic": "",
            "vod_remarks": message,
            "vod_content": message,
            "action": self.NOTICE_PREFIX + message,
        }

    def _image(self, path):
        value = str(path or "").strip()
        if not value:
            return ""
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return self.image_base.rstrip("/") + "/" + value.lstrip("/")

    def _remark(self, data, media_type):
        parts = []
        vote = data.get("vote_average")
        try:
            score = float(vote or 0)
        except Exception:
            score = 0
        if score > 0:
            parts.append(("%.1f" % score).rstrip("0").rstrip(".") + "分")
        date = str(data.get("release_date") or data.get("first_air_date") or "")
        if date[:4].isdigit():
            parts.append(date[:4])
        parts.append("电影" if media_type == "movie" else "剧集")
        return " / ".join(parts)

    @staticmethod
    def _title(data):
        return str(data.get("title") or data.get("name") or data.get("original_title") or data.get("original_name") or "").strip()

    @staticmethod
    def _encode_id(media_type, tmdb_id):
        return "tmdb:%s:%s" % (media_type, tmdb_id)

    @staticmethod
    def _decode_id(value):
        match = re.match(r"^tmdb:(movie|tv):(\d+)$", str(value or ""))
        return (match.group(1), match.group(2)) if match else ("", "")

    def _first_id(self, ids):
        value = ids
        if isinstance(value, str):
            text = value.strip()
            if text.startswith("["):
                try:
                    value = json.loads(text)
                except Exception:
                    value = text
        if isinstance(value, (list, tuple)):
            return str(value[0]) if value else ""
        return str(value or "")

    @staticmethod
    def _parse_config(extend):
        value = extend
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return {}
            try:
                value = json.loads(text)
            except Exception:
                return {}
        if not isinstance(value, dict):
            return {}
        data = value.get("data")
        if data:
            nested = Spider._parse_config(data)
            merged = dict(value)
            merged.update(nested)
            return merged
        return dict(value)

    @staticmethod
    def _parse_extend(extend):
        if isinstance(extend, dict):
            return extend
        if isinstance(extend, str):
            try:
                value = json.loads(extend.strip() or "{}")
                return value if isinstance(value, dict) else {}
            except Exception:
                return {}
        return {}

    @staticmethod
    def _first(data, *keys):
        for key in keys:
            value = str(data.get(key) or "").strip()
            if value:
                return value
        return ""

    @staticmethod
    def _value(data, key, default=""):
        if not isinstance(data, dict):
            return default
        value = data.get(key)
        return default if value is None else str(value)

    @staticmethod
    def _filter(key, name, pairs):
        return {"key": key, "name": name, "value": [{"n": str(label), "v": str(value)} for label, value in pairs]}

    @staticmethod
    def _page_result(items, page, pagecount, total):
        return {"list": items, "page": page, "pagecount": max(page, pagecount), "limit": 20, "total": total}

    @staticmethod
    def _positive_int(value, default):
        try:
            result = int(value)
            return result if result > 0 else default
        except Exception:
            return default

    @staticmethod
    def _bounded_int(value, default, minimum, maximum):
        try:
            result = int(value)
        except Exception:
            return default
        return max(minimum, min(maximum, result))

    @staticmethod
    def _bool_value(value, default):
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("1", "true", "yes", "on")

    @staticmethod
    def _https_base(value, default):
        text = str(value or default).strip().rstrip("/")
        return text if text.startswith("https://") else default

    @staticmethod
    def _short_error(exc):
        text = str(exc or "未知错误").strip().replace("\r", " ").replace("\n", " ")
        return text[:220] or "未知错误"
