# -*- coding: utf-8 -*-
# //@name:豆瓣导航
# //@id:douban_meta_wish
# //@version:2

import json
import math
import re
import threading
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, urlencode

import requests
from lxml import html
from requests.adapters import HTTPAdapter

from base.spider import Spider as BaseSpider


class Spider(BaseSpider):
    name = "豆瓣导航"
    host = "https://m.douban.com"
    backend_parse = False
    category_mode = False
    categoryMode = False

    API = "https://m.douban.com/rexxar/api/v2"
    MOVIE = "https://movie.douban.com"
    ACTION_PREFIX = "douban-wish:add:"
    ERROR_PREFIX = "douban-error:"
    FILTER_CACHE_KEY = "douban_meta_wish_filters_v4_navigation"

    CATEGORIES = (
        ("hotmovie", "热门电影"),
        ("hottv", "热门剧集"),
        ("hotzy", "热门综艺"),
        ("movielist", "电影榜单"),
        ("tvlist", "电视榜单"),
        ("moviefilter", "电影筛选"),
        ("tvfilter", "电视筛选"),
        ("anime", "动漫"),
        ("wishlist", "豆瓣想看"),
    )

    MOVIE_LISTS = (
        ("实时热门电影", "movie_real_time_hotest"),
        ("一周口碑电影榜", "movie_weekly_best"),
        ("豆瓣电影Top250", "top250"),
    )
    TV_LISTS = (
        ("实时热门剧集", "tv_real_time_hotest"),
        ("华语口碑剧集榜", "tv_chinese_best_weekly"),
        ("全球口碑剧集榜", "tv_global_best_weekly"),
        ("国内口碑综艺榜", "show_chinese_best_weekly"),
        ("国外口碑综艺榜", "show_global_best_weekly"),
    )
    AREAS = ("中国大陆", "中国香港", "中国台湾", "美国", "英国", "日本", "韩国", "法国", "德国", "印度", "泰国")
    MOVIE_TYPES = ("剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "犯罪", "惊悚", "恐怖", "纪录片", "短片")
    TV_TYPES = ("电视剧", "综艺")
    SERIES_TYPES = ("国产剧", "港剧", "台剧", "日剧", "韩剧", "美剧", "英剧")
    SHOW_TYPES = ("真人秀", "脱口秀", "音乐", "喜剧", "旅行", "竞技")
    TV_GENRES = ("剧情", "喜剧", "爱情", "悬疑", "动画", "武侠", "古装", "家庭", "犯罪", "科幻", "恐怖", "历史", "战争", "动作", "冒险", "传记", "奇幻", "惊悚", "灾难", "歌舞", "音乐")
    TAGS = ("经典", "热门", "高分", "青春", "家庭", "治愈", "女性", "成长", "历史", "战争", "奇幻", "冒险", "推理", "人性", "真实事件改编")
    PLATFORMS = ("Netflix", "HBO", "Disney+", "BBC", "NHK", "TVB", "爱奇艺", "腾讯视频", "优酷", "芒果TV")
    SORTS = (("综合排序", "T"), ("近期热度", "U"), ("首映/首播时间", "R"), ("高分优先", "S"))
    ANIME_SORTS = (("热度", "U"), ("更新时间", "R"), ("评分", "S"))
    ANIME_REGIONS = {
        "cn": "中国大陆",
        "jp": "日本",
        "kr": "韩国",
        "us": "美国",
    }
    LEGACY_ANIME_REGIONS = {
        "anime_cn": "中国大陆",
        "anime_jp": "日本",
        "anime_kr": "韩国",
        "anime_us": "美国",
    }
    ANIME_GENRES = ("热血", "冒险", "奇幻", "科幻", "校园", "治愈", "搞笑", "恋爱", "悬疑", "运动", "音乐", "历史", "机战", "推理")
    ANIME_FORMATS = ("TV动画", "剧场版", "OVA", "网络动画", "动画短片")

    def __init__(self):
        try:
            super().__init__()
        except Exception:
            pass
        self.timeout = 15
        self.cache_ttl = 180
        self.list_cache_ttl = 120
        self.collection_cache_ttl = 300
        self.detail_cache_ttl = 86400
        self.wishlist_cache_ttl = 20
        self.top250_cache_ttl = 21600
        self.stale_ttl = 86400
        self.cache_max_entries = 256
        self.failure_ttl = 60
        self.filter_cache_ttl = 21600
        self.dynamic_filters = True
        self.persistent_filter_cache = True
        self.image_headers = True
        self.verify_tls = True
        self.trust_env = True
        self.proxy = ""
        self.cookie = ""
        self.ck = ""
        self.user_id = ""
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
        self._session = None
        self._cache = OrderedDict()
        self._failures = {}
        self._cache_lock = threading.RLock()
        self._filters = None
        self._filters_at = 0
        self._reset_session()

    def getName(self):
        return self.name

    def init(self, extend=""):
        config = self._parse_config(extend)
        self.timeout = self._bounded_int(config.get("timeout"), 15, 5, 45)
        self.cache_ttl = self._bounded_int(config.get("cache_ttl"), 180, 0, 3600)
        self.list_cache_ttl = self._bounded_int(config.get("list_cache_ttl"), 120, 10, 1800)
        self.collection_cache_ttl = self._bounded_int(config.get("collection_cache_ttl"), 300, 30, 3600)
        self.detail_cache_ttl = self._bounded_int(config.get("detail_cache_ttl"), 86400, 300, 604800)
        self.wishlist_cache_ttl = self._bounded_int(config.get("wishlist_cache_ttl"), 20, 5, 300)
        self.top250_cache_ttl = self._bounded_int(config.get("top250_cache_ttl"), 21600, 300, 86400)
        self.stale_ttl = self._bounded_int(config.get("stale_ttl"), 86400, 300, 604800)
        self.cache_max_entries = self._bounded_int(config.get("cache_max_entries"), 256, 32, 1024)
        self.failure_ttl = self._bounded_int(config.get("failure_ttl"), 60, 10, 600)
        self.filter_cache_ttl = self._bounded_int(config.get("filter_cache_ttl"), 21600, 300, 86400)
        self.dynamic_filters = self._bool_value(config.get("dynamic_filters"), True)
        self.persistent_filter_cache = self._bool_value(config.get("persistent_filter_cache"), True)
        self.image_headers = self._bool_value(config.get("image_headers"), True)
        self.verify_tls = self._bool_value(config.get("verify_tls"), True)
        self.trust_env = self._bool_value(config.get("trust_env"), True)
        self.proxy = str(config.get("proxy") or "").strip()
        self.cookie = str(config.get("cookie") or "").strip()
        self.user_id = str(config.get("user_id") or "").strip().strip("/")
        self.ck = str(config.get("ck") or self._cookie_value(self.cookie, "ck") or "").strip()
        ua = str(config.get("user_agent") or "").strip()
        if ua:
            self.user_agent = ua
        with self._cache_lock:
            self._cache.clear()
        self._failures.clear()
        self._filters = None
        self._filters_at = 0
        self._reset_session()
        if not self.user_id and self.cookie:
            self._resolve_user_id()

    def destroy(self):
        if self._session is not None:
            try:
                self._session.close()
            except Exception:
                pass

    def homeContent(self, filter=False):
        result = {"class": [{"type_id": key, "type_name": name} for key, name in self.CATEGORIES]}
        if filter:
            result["filters"] = self._get_filters()
        return result

    def homeVideoContent(self):
        try:
            params = {"start": 0, "count": 30, "updated_at": "", "items_only": 1, "for_mobile": 1}
            data = self._get_json(self.API + "/subject_collection/subject_real_time_hotest/items", params=params, ttl=self.list_cache_ttl)
            items = self._parse_collection_items(data)
            if items:
                return {"list": items}
            raise RuntimeError("实时热门列表为空")
        except Exception as primary:
            try:
                fallback = self._category_media("movie", 1, {"sort": "U"})
                if fallback.get("list"):
                    return {"list": fallback["list"]}
            except Exception:
                pass
            return {"list": [self._error_card("首页载入失败", primary)]}

    def categoryContent(self, tid, pg, filter=False, extend=None):
        page = self._positive_int(pg, 1)
        ext = self._parse_extend(extend)
        try:
            if tid == "hotmovie":
                return self._category_media("movie", page, ext)
            if tid == "hottv":
                return self._category_media("tv", page, ext)
            if tid == "hotzy":
                return self._category_media("show", page, ext)
            if tid == "movielist":
                return self._category_movie_list(page, self._value(ext, "1", "movie_real_time_hotest"), ext)
            if tid == "tvlist":
                return self._category_collection(page, self._value(ext, "1", "tv_real_time_hotest"), ext)
            if tid == "moviefilter":
                return self._category_recommend("movie", page, ext)
            if tid == "tvfilter":
                return self._category_recommend("tv", page, ext)
            if tid == "anime":
                region_key = self._value(ext, "region", "cn")
                return self._category_anime(self.ANIME_REGIONS.get(region_key, "中国大陆"), page, ext)
            if tid in self.LEGACY_ANIME_REGIONS:
                return self._category_anime(self.LEGACY_ANIME_REGIONS[tid], page, ext)
            if tid == "wishlist":
                return self._category_wishlist(page)
            return self._page_result([], page, page, 0, 20)
        except Exception as exc:
            return self._page_result([self._error_card("分类载入失败", exc)], page, page, 1, 20)

    def detailContent(self, ids):
        subject_id = self._first_id(ids)
        if subject_id.startswith("atvp_detail:"):
            subject_id = subject_id[len("atvp_detail:"):]
        if subject_id.startswith(self.ERROR_PREFIX):
            text = subject_id[len(self.ERROR_PREFIX):]
            return {"list": [{"vod_id": subject_id, "vod_name": "豆瓣错误", "vod_content": text}]}
        subject_id = self._subject_id(subject_id)
        if not subject_id:
            return {"list": []}
        try:
            data = self._get_json(self.API + "/subject/" + subject_id, params={"for_mobile": 1}, ttl=self.detail_cache_ttl)
            rating = self._rating(data)
            title = str(data.get("title") or "")
            original = str(data.get("original_title") or "")
            names = title if not original or original == title else title + " / " + original
            content = str(data.get("intro") or data.get("card_subtitle") or "").strip()
            honors = self._names(data.get("honor_infos"), "title", 3)
            if honors:
                content = (content + "\n\n榜单：" + honors).strip()
            vod = {
                "vod_id": subject_id,
                "vod_name": names,
                "vod_pic": self._image(self._pic(data, large=True)),
                "type_name": ", ".join(data.get("genres") or []),
                "vod_year": str(data.get("year") or ""),
                "vod_area": ", ".join(data.get("countries") or []),
                "vod_remarks": self._detail_remark(data, rating),
                "vod_actor": self._names(data.get("actors"), "name", 12),
                "vod_director": self._names(data.get("directors"), "name", 6),
                "vod_content": content,
                "vod_play_from": "",
                "vod_play_url": "",
            }
            return {"list": [vod]}
        except Exception as exc:
            return {"list": [self._error_card("详情载入失败", exc, subject_id)]}

    def searchContent(self, key, quick=False, pg="1"):
        return {"list": []}

    def playerContent(self, flag, id, vipFlags=None):
        return {
            "parse": 0,
            "jx": 0,
            "playUrl": "",
            "url": "",
            "header": {},
            "msg": "豆瓣仅提供影视资料，请使用详情页的全局搜索查找播放源",
        }

    def localProxy(self, param):
        return [404, "text/plain; charset=utf-8", "not found"]

    def action(self, action):
        value = str(action or "")
        if not value.startswith(self.ACTION_PREFIX):
            return json.dumps({"msg": "不支持的豆瓣操作"}, ensure_ascii=False)
        subject_id = self._subject_id(value[len(self.ACTION_PREFIX):])
        if not subject_id:
            return json.dumps({"msg": "豆瓣条目编号无效"}, ensure_ascii=False)
        if not self.cookie or not self.ck:
            return json.dumps({"msg": "未配置豆瓣 Cookie/ck，无法加入想看"}, ensure_ascii=False)
        try:
            url = self.MOVIE + "/j/subject/%s/interest" % subject_id
            headers = {
                "Referer": self.MOVIE + "/subject/%s/" % subject_id,
                "X-Requested-With": "XMLHttpRequest",
            }
            data = {"interest": "wish", "ck": self.ck, "tags": "", "comment": "", "privacy": "public"}
            response = self._session.post(url, headers=headers, data=data, timeout=self.timeout, verify=self.verify_tls)
            payload = self._json_response(response)
            if response.status_code == 200 and str(payload.get("r", "0")) == "0":
                self._drop_cache_prefix("wishlist:")
                return json.dumps({"msg": "已加入豆瓣想看"}, ensure_ascii=False)
            if response.status_code in (401, 403) or str(payload.get("code", "")) == "403":
                message = "豆瓣登录已失效，请更新 Cookie/ck"
            else:
                message = str(payload.get("msg") or payload.get("error") or "豆瓣未确认收藏成功")
            return json.dumps({"msg": message}, ensure_ascii=False)
        except Exception as exc:
            return json.dumps({"msg": "加入想看失败：%s" % self._short_error(exc)}, ensure_ascii=False)

    def _category_search_subjects(self, kind, page, tag, ext):
        limit = 50
        params = {"type": kind, "tag": tag or "热门", "page_limit": limit, "page_start": (page - 1) * limit}
        data = self._get_json(self.MOVIE + "/j/search_subjects", params=params, ttl=self.list_cache_ttl)
        items = []
        for raw in data.get("subjects") or []:
            items.append(self._subject_card(raw, ext))
        pagecount = page + 1 if len(items) >= limit else page
        return self._page_result(items, page, pagecount, pagecount * limit, limit)

    def _category_media(self, media, page, ext):
        limit = 20
        sort = self._value(ext, "sort", "U")
        if sort not in {item[1] for item in self.ANIME_SORTS}:
            sort = "U"
        area = self._value(ext, "area", "")
        year = self._value(ext, "year", "")
        genre = self._value(ext, "type" if media == "movie" else "genre", "")
        platform = self._value(ext, "platform", "")
        tag = self._value(ext, "tag", "")
        if media == "movie":
            endpoint = "movie"
            selected = {"类型": genre, "地区": area}
            expected_type = "movie"
            tags = [genre, area, year, tag]
        else:
            endpoint = "tv"
            form = "电视剧" if media == "tv" else "综艺"
            selected = {"类型": genre, "形式": form, "地区": area}
            expected_type = "tv"
            tags = [form, genre, area, year, platform, tag]
        params = {
            "refresh": 0,
            "start": (page - 1) * limit,
            "count": limit,
            "selected_categories": json.dumps(selected, ensure_ascii=False, separators=(",", ":")),
            "uncollect": "false",
            "sort": sort,
            "tags": ",".join([item for item in tags if item]),
        }
        data = self._get_json(self.API + "/%s/recommend" % endpoint, params=params, ttl=self.list_cache_ttl)
        items = []
        for raw in data.get("items") or []:
            raw_type = str(raw.get("type") or "")
            if raw_type and raw_type != expected_type:
                continue
            items.append(self._collection_card(raw, ext))
        total = self._positive_int(data.get("total"), 0)
        pagecount = int(math.ceil(float(total) / limit)) if total else page + (1 if len(items) >= limit else 0)
        return self._page_result(items, page, max(page, pagecount), total or pagecount * limit, limit)

    def _category_hot_show(self, page, scope, ext):
        if page > 1:
            return self._page_result([], page, 1, 0, 50)
        params = {"start": 0, "count": 50, "updated_at": "", "items_only": 1, "for_mobile": 1}
        data = self._get_json(self.API + "/subject_collection/show_hot/items", params=params, ttl=self.list_cache_ttl)
        items = []
        for raw in data.get("subject_collection_items") or []:
            subtitle = str(raw.get("card_subtitle") or "")
            if scope == "zy_cn" and "中国" not in subtitle:
                continue
            if scope == "zy_other" and "中国" in subtitle:
                continue
            items.append(self._collection_card(raw, ext))
        return self._page_result(items, 1, 1, len(items), 50)

    def _category_movie_list(self, page, collection, ext):
        if collection == "top250":
            return self._category_top250(page, ext)
        return self._category_collection(page, collection, ext)

    def _category_collection(self, page, collection, ext):
        limit = 50
        params = {"start": (page - 1) * limit, "count": limit, "updated_at": "", "items_only": 1, "for_mobile": 1}
        data = self._get_json(self.API + "/subject_collection/%s/items" % quote(collection, safe=""), params=params, ttl=self.collection_cache_ttl)
        items = [self._collection_card(raw, ext) for raw in data.get("subject_collection_items") or []]
        total = self._positive_int(data.get("total"), len(items))
        pagecount = max(page, int(math.ceil(float(total) / limit))) if total else page
        return self._page_result(items, page, pagecount, total, limit)

    def _category_top250(self, page, ext):
        limit = 25
        if page > 10:
            return self._page_result([], page, 10, 250, limit)
        text = self._get_text(self.MOVIE + "/top250", params={"start": (page - 1) * limit}, ttl=self.top250_cache_ttl)
        doc = html.fromstring(text)
        items = []
        nodes = doc.xpath("//div[contains(@class,'article')]//ol[contains(@class,'grid_view')]/li")
        for node in nodes:
            href = self._xpath_text(node, ".//div[contains(@class,'pic')]/a/@href")
            subject_id = self._subject_id(href)
            if not subject_id:
                continue
            title = self._xpath_text(node, ".//div[contains(@class,'hd')]//span[contains(@class,'title')][1]")
            pic = self._xpath_text(node, ".//div[contains(@class,'pic')]//img/@src")
            score = self._xpath_text(node, ".//span[contains(@class,'rating_num')]")
            card = {"vod_id": subject_id, "vod_name": title, "vod_pic": self._image(pic), "vod_remarks": (score + "分") if score else "Top250"}
            items.append(card)
        return self._page_result(items, page, 10, 250, limit)

    def _category_recommend(self, kind, page, ext):
        limit = 20
        if kind == "movie":
            type_value = self._value(ext, "1", "")
            area = self._value(ext, "2", "")
            tags = [type_value, area, self._value(ext, "3", ""), self._value(ext, "4", "")]
            selected = {"类型": type_value, "地区": area}
            sort = self._value(ext, "5", "U")
        else:
            form = self._value(ext, "1", "")
            series = self._value(ext, "2", "")
            show = self._value(ext, "3", "")
            area = self._value(ext, "4", "")
            subtype = series if form == "电视剧" else show if form == "综艺" else ""
            tags = [subtype or form, area, self._value(ext, "5", ""), self._value(ext, "6", ""), self._value(ext, "7", "")]
            selected = {"类型": subtype, "形式": form, "地区": area}
            sort = self._value(ext, "8", "U")
        params = {
            "refresh": 0,
            "start": (page - 1) * limit,
            "count": limit,
            "selected_categories": json.dumps(selected, ensure_ascii=False, separators=(",", ":")),
            "uncollect": "false",
            "sort": sort,
            "tags": ",".join([item for item in tags if item]),
        }
        data = self._get_json(self.API + "/%s/recommend" % kind, params=params, ttl=self.list_cache_ttl)
        items = []
        for raw in data.get("items") or []:
            if raw.get("type") and raw.get("type") != kind:
                continue
            items.append(self._collection_card(raw, ext))
        total = self._positive_int(data.get("total"), 0)
        pagecount = int(math.ceil(float(total) / limit)) if total else page + (1 if len(items) >= limit else 0)
        return self._page_result(items, page, max(page, pagecount), total or pagecount * limit, limit)

    def _category_wishlist(self, page):
        user_id = self.user_id or self._resolve_user_id()
        if not user_id:
            message = "请在 ext 中配置 user_id；写回想看还需 cookie，ck 可从 Cookie 自动读取"
            return self._page_result([self._error_card("豆瓣想看未配置", message)], page, page, 1, 15)
        start = (page - 1) * 15
        url = self.MOVIE + "/people/%s/wish" % quote(user_id, safe="")
        cache_key = "wishlist:%s:%s" % (user_id, page)
        text = self._get_text(url, params={"start": start, "sort": "time", "rating": "all", "filter": "all", "mode": "grid"}, custom_key=cache_key, ttl=self.wishlist_cache_ttl)
        doc = html.fromstring(text)
        items = []
        nodes = doc.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' grid-view ')]//div[contains(concat(' ',normalize-space(@class),' '),' item ')]")
        for node in nodes:
            href = self._xpath_text(node, ".//li[contains(@class,'title')]/a/@href")
            subject_id = self._subject_id(href)
            if not subject_id:
                continue
            title = self._xpath_text(node, ".//li[contains(@class,'title')]//em") or self._xpath_text(node, ".//img/@alt")
            pic = self._xpath_text(node, ".//img/@src")
            date = self._xpath_text(node, ".//span[contains(@class,'date')]")
            intro = self._xpath_text(node, ".//li[contains(@class,'intro')]")
            remark = date or (intro[:24] if intro else "想看")
            items.append({"vod_id": subject_id, "vod_name": title, "vod_pic": self._image(pic), "vod_remarks": remark})
        title_text = self._xpath_text(doc, "//title")
        match = re.search(r"\((\d+)\)", title_text)
        total = int(match.group(1)) if match else start + len(items)
        pagecount = max(page, int(math.ceil(float(total) / 15))) if total else page
        return self._page_result(items, page, pagecount, total, 15)

    def _category_anime(self, region, page, ext):
        kind = self._value(ext, "kind", "tv")
        if kind not in ("tv", "movie"):
            kind = "tv"
        sort = self._value(ext, "sort", "U")
        if sort not in {item[1] for item in self.ANIME_SORTS}:
            sort = "U"
        year = self._value(ext, "year", "")
        genre = self._value(ext, "genre", "")
        format_tag = self._value(ext, "format", "")
        limit = 20
        if kind == "movie":
            selected = {"类型": "动画", "地区": region}
        else:
            selected = {"类型": "动画", "形式": "电视剧", "地区": region}
        tags = ["动画", region, year, genre, format_tag]
        params = {
            "refresh": 0,
            "start": (page - 1) * limit,
            "count": limit,
            "selected_categories": json.dumps(selected, ensure_ascii=False, separators=(",", ":")),
            "uncollect": "false",
            "sort": sort,
            "tags": ",".join([item for item in tags if item]),
        }
        data = self._get_json(self.API + "/%s/recommend" % kind, params=params, ttl=self.list_cache_ttl)
        items = []
        for raw in data.get("items") or []:
            raw_type = str(raw.get("type") or "")
            if raw_type and raw_type != kind:
                continue
            items.append(self._collection_card(raw, ext))
        total = self._positive_int(data.get("total"), 0)
        pagecount = int(math.ceil(float(total) / limit)) if total else page + (1 if len(items) >= limit else 0)
        return self._page_result(items, page, max(page, pagecount), total or pagecount * limit, limit)

    def _parse_collection_items(self, data):
        return [self._collection_card(raw, {}) for raw in data.get("subject_collection_items") or []]

    def _subject_card(self, raw, ext):
        score = str(raw.get("rate") or "").strip()
        card = {
            "vod_id": str(raw.get("id") or ""),
            "vod_name": str(raw.get("title") or ""),
            "vod_pic": self._image(str(raw.get("cover") or "")),
            "vod_remarks": (score + "分") if score and score != "0" else "暂无评分",
        }
        return card

    def _collection_card(self, raw, ext):
        rating = self._rating(raw)
        honor = self._names(raw.get("honor_infos"), "title", 1)
        remark = (rating + "分") if rating else "暂无评分"
        if honor:
            remark += " " + honor
        card = {
            "vod_id": str(raw.get("id") or ""),
            "vod_name": str(raw.get("title") or ""),
            "vod_pic": self._image(self._pic(raw)),
            "vod_remarks": remark,
        }
        return card

    def _get_filters(self):
        now = time.time()
        if self._filters is not None and now - self._filters_at < self.filter_cache_ttl:
            return self._filters
        persisted = self._load_persistent_filters()
        if persisted is not None:
            self._filters = persisted
            self._filters_at = now
            return persisted
        filters = self._base_filters()
        if self.dynamic_filters:
            self._merge_dynamic_filters(filters)
        self._filters = filters
        self._filters_at = now
        self._save_persistent_filters(filters)
        return filters

    def _load_persistent_filters(self):
        if not self.persistent_filter_cache:
            return None
        getter = getattr(self, "getCache", None)
        if not callable(getter):
            return None
        try:
            value = getter(self.FILTER_CACHE_KEY)
            if not isinstance(value, dict):
                return None
            filters = value.get("filters")
            if not isinstance(filters, dict):
                return None
            required = {item[0] for item in self.CATEGORIES}
            if not required.issubset(set(filters)):
                return None
            return filters
        except Exception:
            return None

    def _save_persistent_filters(self, filters):
        if not self.persistent_filter_cache:
            return
        setter = getattr(self, "setCache", None)
        if not callable(setter):
            return
        try:
            setter(self.FILTER_CACHE_KEY, {
                "expiresAt": int(time.time() + self.filter_cache_ttl),
                "filters": filters,
            })
        except Exception:
            pass

    def _base_filters(self):
        years = [str(year) for year in range(time.localtime().tm_year, 1979, -1)]
        hot_movie = [
            self._filter("sort", "排序", self.ANIME_SORTS),
            self._filter("type", "类型", [("全部类型", "")] + [(v, v) for v in self.MOVIE_TYPES]),
            self._filter("area", "地区", [("全部地区", "")] + [(v, v) for v in self.AREAS]),
            self._filter("year", "年代", [("全部年代", "")] + [(v, v) for v in years]),
            self._filter("tag", "标签", [("全部标签", "")] + [(v, v) for v in self.TAGS]),
        ]
        hot_tv = [
            self._filter("sort", "排序", self.ANIME_SORTS),
            self._filter("genre", "题材", [("全部题材", "")] + [(v, v) for v in self.TV_GENRES]),
            self._filter("area", "地区", [("全部地区", "")] + [(v, v) for v in self.AREAS]),
            self._filter("year", "年代", [("全部年代", "")] + [(v, v) for v in years]),
            self._filter("platform", "平台", [("全部平台", "")] + [(v, v) for v in self.PLATFORMS]),
            self._filter("tag", "标签", [("全部标签", "")] + [(v, v) for v in self.TAGS]),
        ]
        hot_show = [
            self._filter("sort", "排序", self.ANIME_SORTS),
            self._filter("genre", "类型", [("全部类型", "")] + [(v, v) for v in self.SHOW_TYPES]),
            self._filter("area", "地区", [("全部地区", "")] + [(v, v) for v in self.AREAS]),
            self._filter("year", "年代", [("全部年代", "")] + [(v, v) for v in years]),
            self._filter("platform", "平台", [("全部平台", "")] + [(v, v) for v in self.PLATFORMS]),
        ]
        return {
            "hotmovie": hot_movie,
            "hottv": hot_tv,
            "hotzy": hot_show,
            "movielist": [self._filter("1", "榜单", self.MOVIE_LISTS)],
            "tvlist": [self._filter("1", "榜单", self.TV_LISTS)],
            "moviefilter": [
                self._filter("5", "排序", self.SORTS),
                self._filter("1", "类型", [("全部类型", "")] + [(v, v) for v in self.MOVIE_TYPES]),
                self._filter("2", "地区", [("全部地区", "")] + [(v, v) for v in self.AREAS]),
                self._filter("3", "年代", [("全部年代", "")] + [(v, v) for v in years]),
                self._filter("4", "标签", [("全部标签", "")] + [(v, v) for v in self.TAGS]),
            ],
            "tvfilter": [
                self._filter("8", "排序", self.SORTS),
                self._filter("1", "类型", [("全部类型", "")] + [(v, v) for v in self.TV_TYPES]),
                self._filter("2", "电视剧", [("全部剧集", "")] + [(v, v) for v in self.SERIES_TYPES]),
                self._filter("3", "综艺", [("全部综艺", "")] + [(v, v) for v in self.SHOW_TYPES]),
                self._filter("4", "地区", [("全部地区", "")] + [(v, v) for v in self.AREAS]),
                self._filter("5", "年代", [("全部年代", "")] + [(v, v) for v in years]),
                self._filter("6", "平台", [("全部平台", "")] + [(v, v) for v in self.PLATFORMS]),
                self._filter("7", "标签", [("全部标签", "")] + [(v, v) for v in self.TAGS]),
            ],
            "anime": self._anime_filters(years),
            "wishlist": [],
        }

    def _anime_filters(self, years):
        return [
            self._filter("sort", "排序", self.ANIME_SORTS),
            self._filter("region", "地区", (("国漫", "cn"), ("日漫", "jp"), ("韩漫", "kr"), ("美漫", "us"))),
            self._filter("kind", "内容", (("动画剧集", "tv"), ("动画电影", "movie"))),
            self._filter("year", "年代", [("全部年代", "")] + [(v, v) for v in years]),
            self._filter("genre", "题材", [("全部题材", "")] + [(v, v) for v in self.ANIME_GENRES]),
            self._filter("format", "形式", [("全部形式", "")] + [(v, v) for v in self.ANIME_FORMATS]),
        ]

    def _merge_dynamic_filters(self, filters):
        jobs = {
            "movie_meta": (self.API + "/movie/recommend", {}),
            "tv_meta": (self.API + "/tv/recommend", {}),
        }
        results = {}
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(self._get_json, url, params, self.filter_cache_ttl): key for key, (url, params) in jobs.items()}
                for future in as_completed(futures):
                    try:
                        results[futures[future]] = future.result()
                    except Exception:
                        pass
        except Exception:
            return
        self._merge_recommend_meta(filters.get("moviefilter"), results.get("movie_meta"), False)
        self._merge_recommend_meta(filters.get("tvfilter"), results.get("tv_meta"), True)

    def _merge_recommend_meta(self, target, data, is_tv):
        if not target or not isinstance(data, dict):
            return
        categories = data.get("recommend_categories") or []
        try:
            if is_tv:
                type_data = categories[0].get("data") or []
                if type_data:
                    tags = type_data[0].get("tags") or []
                    values = []
                    for item in tags[1:]:
                        name = str(item).replace("全部剧集", "电视剧").replace("全部综艺", "综艺")
                        values.append((name, name))
                    if values:
                        self._set_filter_values(target, "1", [("全部类型", "")] + values)
                if len(categories) > 1:
                    areas = categories[1].get("data") or []
                    values = [(str(v.get("text")), str(v.get("text"))) for v in areas[1:] if v.get("text")]
                    if values:
                        self._set_filter_values(target, "4", [("全部地区", "")] + values)
            else:
                for index in (0, 1):
                    values = []
                    for item in (categories[index].get("data") or [])[1:]:
                        if item.get("text"):
                            values.append((str(item["text"]), str(item["text"])))
                    if values:
                        self._set_filter_values(target, "1" if index == 0 else "2", [("全部" + ("类型" if index == 0 else "地区"), "")] + values)
            sorts = [(str(v.get("text")), str(v.get("name"))) for v in data.get("sorts") or [] if v.get("text") and v.get("name")]
            if sorts:
                self._set_filter_values(target, "8" if is_tv else "5", sorts)
        except Exception:
            return

    def _set_filter_values(self, filters, key, pairs):
        for item in filters or []:
            if str(item.get("key")) == str(key):
                item["value"] = self._values(pairs)
                return

    def _get_json(self, url, params=None, ttl=None):
        key = "json:" + url + "?" + urlencode(sorted((params or {}).items()), doseq=True)
        ttl = self.cache_ttl if ttl is None else ttl
        cached = self._cache_get(key, ttl)
        if cached is not None:
            return cached
        stale = self._cache_get(key, self.stale_ttl, allow_expired=True)
        if self._has_cached_failure(key) and stale is not None:
            return stale
        self._raise_cached_failure(key)
        try:
            response = self._session.get(url, params=params, timeout=self.timeout, verify=self.verify_tls)
            payload = self._json_response(response)
            if response.status_code != 200:
                raise RuntimeError("HTTP %s" % response.status_code)
            self._cache_set(key, payload)
            self._failures.pop(key, None)
            return payload
        except Exception as exc:
            self._remember_failure(key, exc)
            if stale is not None:
                return stale
            raise

    def _get_text(self, url, params=None, custom_key="", ttl=None):
        key = custom_key or ("text:" + url + "?" + urlencode(sorted((params or {}).items()), doseq=True))
        ttl = self.cache_ttl if ttl is None else ttl
        cached = self._cache_get(key, ttl)
        if cached is not None:
            return cached
        stale = self._cache_get(key, self.stale_ttl, allow_expired=True)
        if self._has_cached_failure(key) and stale is not None:
            return stale
        self._raise_cached_failure(key)
        try:
            response = self._session.get(url, params=params, timeout=self.timeout, verify=self.verify_tls)
            if response.status_code != 200:
                raise RuntimeError("HTTP %s" % response.status_code)
            text = response.text
            if len(text) < 500:
                raise RuntimeError("页面内容异常短")
            self._cache_set(key, text)
            self._failures.pop(key, None)
            return text
        except Exception as exc:
            self._remember_failure(key, exc)
            if stale is not None:
                return stale
            raise

    def _json_response(self, response):
        try:
            value = response.json()
            return value if isinstance(value, dict) else {"data": value}
        except Exception:
            if response.status_code != 200:
                return {"error": "HTTP %s" % response.status_code}
            raise RuntimeError("上游返回了非 JSON 内容")

    def _reset_session(self):
        if self._session is not None:
            try:
                self._session.close()
            except Exception:
                pass
        session = requests.Session()
        session.trust_env = self.trust_env
        session.headers.update({"User-Agent": self.user_agent, "Referer": self.host + "/", "Accept": "application/json,text/html;q=0.9,*/*;q=0.8"})
        if self.cookie:
            session.headers["Cookie"] = self.cookie
        if self.proxy:
            session.proxies.update({"http": self.proxy, "https": self.proxy})
        try:
            from requests.packages.urllib3.util.retry import Retry
            retry = Retry(total=2, connect=2, read=2, status=2, backoff_factor=0.35, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset(("GET",)))
            adapter = HTTPAdapter(max_retries=retry, pool_connections=8, pool_maxsize=8)
        except TypeError:
            adapter = HTTPAdapter(max_retries=2, pool_connections=8, pool_maxsize=8)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        self._session = session

    def _resolve_user_id(self):
        if self.user_id:
            return self.user_id
        if not self.cookie:
            return ""
        try:
            response = self._session.get("https://www.douban.com/mine/", timeout=self.timeout, verify=self.verify_tls, allow_redirects=True)
            match = re.search(r"/people/([^/?#]+)/?", response.url)
            if not match:
                match = re.search(r"https?://www\.douban\.com/people/([^/?#]+)/?", response.text)
            if match:
                self.user_id = match.group(1)
        except Exception:
            pass
        return self.user_id

    def _parse_config(self, extend):
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
            nested = self._parse_config(data)
            merged = dict(value)
            merged.update(nested)
            return merged
        return dict(value)

    def _parse_extend(self, extend):
        if isinstance(extend, dict):
            return extend
        if isinstance(extend, str):
            text = extend.strip()
            if not text:
                return {}
            try:
                value = json.loads(text)
                return value if isinstance(value, dict) else {}
            except Exception:
                return {}
        return {}

    def _cache_get(self, key, ttl, allow_expired=False):
        with self._cache_lock:
            item = self._cache.get(key)
            if not item:
                return None
            created, value = item
            age = time.time() - created
            if age > ttl:
                if not allow_expired and age > self.stale_ttl:
                    self._cache.pop(key, None)
                return value if allow_expired and age <= self.stale_ttl else None
            self._cache.move_to_end(key)
            return value

    def _cache_set(self, key, value):
        if self.cache_ttl <= 0:
            return
        with self._cache_lock:
            self._cache[key] = (time.time(), value)
            self._cache.move_to_end(key)
            while len(self._cache) > self.cache_max_entries:
                self._cache.popitem(last=False)

    def _drop_cache_prefix(self, prefix):
        with self._cache_lock:
            for key in list(self._cache):
                if key.startswith(prefix):
                    self._cache.pop(key, None)

    def _remember_failure(self, key, exc):
        self._failures[key] = (time.time(), self._short_error(exc))

    def _raise_cached_failure(self, key):
        item = self._failures.get(key)
        if not item:
            return
        created, message = item
        if time.time() - created <= self.failure_ttl:
            raise RuntimeError(message)
        self._failures.pop(key, None)

    def _has_cached_failure(self, key):
        item = self._failures.get(key)
        if not item:
            return False
        if time.time() - item[0] <= self.failure_ttl:
            return True
        self._failures.pop(key, None)
        return False

    def _page_result(self, items, page, pagecount, total, limit):
        return {"list": items, "page": page, "pagecount": max(page, pagecount), "limit": limit, "total": total}

    def _error_card(self, title, exc, subject_id=""):
        message = self._short_error(exc)
        identity = self.ERROR_PREFIX + quote(message[:180], safe="")
        return {"vod_id": subject_id or identity, "vod_name": title, "vod_pic": "", "vod_remarks": message, "vod_content": message}

    def _detail_remark(self, data, rating):
        parts = []
        if rating:
            parts.append(rating + "分")
        parts.extend([str(v) for v in data.get("durations") or []][:1])
        episode_count = self._positive_int(data.get("episodes_count"), 0)
        if episode_count:
            parts.append("%s集" % episode_count)
        return " / ".join(parts)

    def _image(self, url):
        value = str(url or "").strip()
        if not value or not self.image_headers or "doubanio.com" not in value:
            return value
        return value + "@Referer=https://m.douban.com/@User-Agent=" + self.user_agent

    @staticmethod
    def _pic(data, large=False):
        pic = data.get("pic") or {}
        if isinstance(pic, dict):
            return str(pic.get("large" if large else "normal") or pic.get("normal") or pic.get("large") or "")
        return str(data.get("cover_url") or data.get("cover") or "")

    @staticmethod
    def _rating(data):
        rating = data.get("rating")
        if isinstance(rating, dict):
            value = rating.get("value")
        else:
            value = data.get("rate")
        if value in (None, "", 0, "0"):
            return ""
        return str(value)

    @staticmethod
    def _names(items, key, limit):
        values = []
        for item in items or []:
            value = item.get(key) if isinstance(item, dict) else item
            if value:
                values.append(str(value))
            if len(values) >= limit:
                break
        return ", ".join(values)

    @staticmethod
    def _xpath_text(node, xpath):
        try:
            values = node.xpath(xpath)
            if not values:
                return ""
            value = values[0]
            if hasattr(value, "text_content"):
                value = value.text_content()
            return " ".join(str(value).split())
        except Exception:
            return ""

    @staticmethod
    def _subject_id(value):
        match = re.search(r"(?:subject/)?(\d{3,})", str(value or ""))
        return match.group(1) if match else ""

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
    def _cookie_value(cookie, name):
        match = re.search(r"(?:^|;\s*)%s=([^;]*)" % re.escape(name), str(cookie or ""))
        return match.group(1) if match else ""

    @staticmethod
    def _value(data, key, default=""):
        if not isinstance(data, dict):
            return default
        value = data.get(key)
        if value is None and str(key).isdigit():
            value = data.get(int(key))
        return default if value is None else str(value)

    @staticmethod
    def _filter(key, name, pairs):
        return {"key": key, "name": name, "value": Spider._values(pairs)}

    @staticmethod
    def _values(pairs):
        result = []
        seen = set()
        for name, value in pairs:
            marker = str(value)
            if marker in seen:
                continue
            seen.add(marker)
            result.append({"n": str(name), "v": marker})
        return result

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
    def _short_error(exc):
        text = str(exc or "未知错误").strip().replace("\r", " ").replace("\n", " ")
        return text[:220] or "未知错误"
