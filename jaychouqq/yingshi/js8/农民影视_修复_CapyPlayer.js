const SITE = "https://vip.wwgz.cn:5200";
const PLAYER_SITE = "https://api.nmvod.me:520";

const UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Mobile/15E148 Safari/604.1";

const PLAY_API = PLAYER_SITE + "/player/?url=";

const PLAY_HEADERS = {
  "User-Agent": UA,
  "Referer": PLAYER_SITE + "/"
};
const CACHE_TTL = 5 * 60 * 1000;

var __cache = {};

var WidgetMetadata = {
  id: "nongmin_vod_capyplayer",
  title: "农民影视",
  description: "农民影视分类浏览与搜索播放源",
  version: "1.3.19",
  requiredVersion: "0.0.1",
  modules: [
    {
      id: "movies",
      title: "电影",
      description: "农民影视电影分类",
      functionName: "loadCategory",
      type: "media_list",
      cacheDuration: 120,
      timeoutSeconds: 15,
      retryCount: 0,
      params: [
        { name: "categoryId", title: "分类", type: "constant", value: "1" },
        {
          name: "type",
          title: "类型",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "1" },
            { title: "动作片", value: "5" },
            { title: "喜剧片", value: "6" },
            { title: "爱情片", value: "7" },
            { title: "科幻片", value: "8" },
            { title: "恐怖片", value: "9" },
            { title: "剧情片", value: "10" },
            { title: "战争片", value: "11" },
            { title: "惊悚片", value: "12" },
            { title: "奇幻片", value: "13" }
          ],
          value: "1"
        },
        {
          name: "area",
          title: "地区",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "" },
            { title: "大陆", value: "大陆" },
            { title: "香港", value: "香港" },
            { title: "台湾", value: "台湾" },
            { title: "美国", value: "美国" },
            { title: "日本", value: "日本" },
            { title: "韩国", value: "韩国" },
            { title: "印度", value: "印度" },
            { title: "泰国", value: "泰国" },
            { title: "英国", value: "英国" },
            { title: "法国", value: "法国" },
            { title: "加拿大", value: "加拿大" },
            { title: "西班牙", value: "西班牙" },
            { title: "俄罗斯", value: "俄罗斯" },
            { title: "其他", value: "其他" }
          ],
          value: ""
        },
        {
          name: "year",
          title: "年份",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "0" },
            { title: "2026", value: "2026" },
            { title: "2025", value: "2025" },
            { title: "2024", value: "2024" },
            { title: "2023", value: "2023" },
            { title: "2022", value: "2022" },
            { title: "2021", value: "2021" },
            { title: "2020", value: "2020" },
            { title: "2019", value: "2019" },
            { title: "2018", value: "2018" },
            { title: "2017", value: "2017" },
            { title: "2016", value: "2016" },
            { title: "2015", value: "2015" },
            { title: "2014", value: "2014" },
            { title: "2013", value: "2013" },
            { title: "2012", value: "2012" },
            { title: "2011", value: "2011" },
            { title: "2010", value: "2010" },
            { title: "2009~2000", value: "2009~2000" }
          ],
          value: "0"
        },
        {
          name: "sort",
          title: "排序",
          type: "enum",
          enumOptions: [
            { title: "时间", value: "time" },
            { title: "人气", value: "hits" },
            { title: "评分", value: "score" }
          ],
          value: "time"
        },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "series",
      title: "连续剧",
      description: "农民影视连续剧分类",
      functionName: "loadCategory",
      type: "media_list",
      cacheDuration: 120,
      timeoutSeconds: 15,
      retryCount: 0,
      params: [
        { name: "categoryId", title: "分类", type: "constant", value: "2" },
        {
          name: "type",
          title: "类型",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "2" },
            { title: "国产剧", value: "12" },
            { title: "港台泰", value: "13" },
            { title: "日韩剧", value: "14" },
            { title: "欧美剧", value: "15" }
          ],
          value: "2"
        },
        {
          name: "area",
          title: "地区",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "" },
            { title: "大陆", value: "大陆" },
            { title: "香港", value: "香港" },
            { title: "台湾", value: "台湾" },
            { title: "美国", value: "美国" },
            { title: "日本", value: "日本" },
            { title: "韩国", value: "韩国" },
            { title: "印度", value: "印度" },
            { title: "泰国", value: "泰国" },
            { title: "英国", value: "英国" },
            { title: "法国", value: "法国" },
            { title: "加拿大", value: "加拿大" },
            { title: "西班牙", value: "西班牙" },
            { title: "俄罗斯", value: "俄罗斯" },
            { title: "其他", value: "其他" }
          ],
          value: ""
        },
        {
          name: "year",
          title: "年份",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "0" },
            { title: "2026", value: "2026" },
            { title: "2025", value: "2025" },
            { title: "2024", value: "2024" },
            { title: "2023", value: "2023" },
            { title: "2022", value: "2022" },
            { title: "2021", value: "2021" },
            { title: "2020", value: "2020" },
            { title: "2019", value: "2019" },
            { title: "2018", value: "2018" },
            { title: "2017", value: "2017" },
            { title: "2016", value: "2016" },
            { title: "2015", value: "2015" },
            { title: "2014", value: "2014" },
            { title: "2013", value: "2013" },
            { title: "2012", value: "2012" },
            { title: "2011", value: "2011" },
            { title: "2010", value: "2010" }
          ],
          value: "0"
        },
        {
          name: "sort",
          title: "排序",
          type: "enum",
          enumOptions: [
            { title: "时间", value: "time" },
            { title: "人气", value: "hits" },
            { title: "评分", value: "score" }
          ],
          value: "time"
        },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "variety",
      title: "综艺",
      description: "农民影视综艺分类",
      functionName: "loadCategory",
      type: "media_list",
      cacheDuration: 120,
      timeoutSeconds: 15,
      retryCount: 0,
      params: [
        { name: "categoryId", title: "分类", type: "constant", value: "3" },
        {
          name: "area",
          title: "地区",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "" },
            { title: "大陆", value: "大陆" },
            { title: "香港", value: "香港" },
            { title: "台湾", value: "台湾" },
            { title: "美国", value: "美国" },
            { title: "日本", value: "日本" },
            { title: "韩国", value: "韩国" },
            { title: "印度", value: "印度" },
            { title: "泰国", value: "泰国" },
            { title: "英国", value: "英国" },
            { title: "法国", value: "法国" },
            { title: "加拿大", value: "加拿大" },
            { title: "西班牙", value: "西班牙" },
            { title: "俄罗斯", value: "俄罗斯" },
            { title: "其他", value: "其他" }
          ],
          value: ""
        },
        {
          name: "year",
          title: "年份",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "0" },
            { title: "2026", value: "2026" },
            { title: "2025", value: "2025" },
            { title: "2024", value: "2024" },
            { title: "2023", value: "2023" },
            { title: "2022", value: "2022" },
            { title: "2021", value: "2021" },
            { title: "2020", value: "2020" },
            { title: "2019", value: "2019" },
            { title: "2018", value: "2018" },
            { title: "2017", value: "2017" },
            { title: "2016", value: "2016" },
            { title: "2015", value: "2015" },
            { title: "2014", value: "2014" },
            { title: "2013", value: "2013" },
            { title: "2012", value: "2012" },
            { title: "2011", value: "2011" },
            { title: "2010", value: "2010" }
          ],
          value: "0"
        },
        {
          name: "sort",
          title: "排序",
          type: "enum",
          enumOptions: [
            { title: "时间", value: "time" },
            { title: "人气", value: "hits" },
            { title: "评分", value: "score" }
          ],
          value: "time"
        },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "anime",
      title: "动漫",
      description: "农民影视动漫分类",
      functionName: "loadCategory",
      type: "media_list",
      cacheDuration: 120,
      timeoutSeconds: 15,
      retryCount: 0,
      params: [
        { name: "categoryId", title: "分类", type: "constant", value: "4" },
        {
          name: "area",
          title: "地区",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "" },
            { title: "大陆", value: "大陆" },
            { title: "香港", value: "香港" },
            { title: "台湾", value: "台湾" },
            { title: "美国", value: "美国" },
            { title: "日本", value: "日本" },
            { title: "韩国", value: "韩国" },
            { title: "印度", value: "印度" },
            { title: "泰国", value: "泰国" },
            { title: "英国", value: "英国" },
            { title: "法国", value: "法国" },
            { title: "加拿大", value: "加拿大" },
            { title: "西班牙", value: "西班牙" },
            { title: "俄罗斯", value: "俄罗斯" },
            { title: "其他", value: "其他" }
          ],
          value: ""
        },
        {
          name: "year",
          title: "年份",
          type: "enum",
          enumOptions: [
            { title: "全部", value: "0" },
            { title: "2026", value: "2026" },
            { title: "2025", value: "2025" },
            { title: "2024", value: "2024" },
            { title: "2023", value: "2023" },
            { title: "2022", value: "2022" },
            { title: "2021", value: "2021" },
            { title: "2020", value: "2020" },
            { title: "2019", value: "2019" },
            { title: "2018", value: "2018" },
            { title: "2017", value: "2017" },
            { title: "2016", value: "2016" },
            { title: "2015", value: "2015" },
            { title: "2014", value: "2014" },
            { title: "2013", value: "2013" },
            { title: "2012", value: "2012" },
            { title: "2011", value: "2011" },
            { title: "2010", value: "2010" }
          ],
          value: "0"
        },
        {
          name: "sort",
          title: "排序",
          type: "enum",
          enumOptions: [
            { title: "时间", value: "time" },
            { title: "人气", value: "hits" },
            { title: "评分", value: "score" }
          ],
          value: "time"
        },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "short_drama",
      title: "短剧",
      description: "农民影视短剧分类",
      functionName: "loadCategory",
      type: "media_list",
      cacheDuration: 120,
      timeoutSeconds: 15,
      retryCount: 0,
      params: [
        { name: "categoryId", title: "分类", type: "constant", value: "26" },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "loadResource",
      title: "农民影视播放源",
      description: "根据当前影片返回农民影视播放源",
      functionName: "loadResource",
      type: "stream",
      params: []
    }
  ],
  search: {
    title: "搜索",
    functionName: "searchVideos",
    params: [
      {
        name: "keyword",
        title: "搜索关键词",
        type: "input",
        description: "输入影片名称",
        value: ""
      },
      { name: "page", title: "页码", type: "page", description: "页码", value: "1" }
    ]
  }
};

const NONGMIN_CATEGORY_IDS = {
  movies: "1",
  series: "2",
  variety: "3",
  anime: "4",
  short_drama: "26"
};

function categoryValue(value, fallback) {
  const text = String(value == null ? "" : value).trim();
  return text || fallback;
}

function categoryUrl(params) {
  params = params || {};
  const categoryId = categoryValue(params.categoryId, "1");
  const listId = categoryValue(params.type, categoryId);
  const page = Math.max(1, toInt(params.page, 1));
  const year = categoryValue(params.year, "0");
  const sort = categoryValue(params.sort, "time");
  const area = String(params.area == null ? "" : params.area);
  return SITE + "/vod-list-id-" + encodeURIComponent(listId)
    + "-pg-" + page
    + "-order--by-" + encodeURIComponent(sort)
    + "-class-0"
    + "-year-" + encodeURIComponent(year)
    + "-letter--area-" + encodeURIComponent(area)
    + "-lang-.html";
}

async function loadCategory(params) {
  const url = categoryUrl(params);
  console.log("[nongmin] category request: " + url);
  const res = await httpGet(url);
  const cards = parseSearchResults((res && res.data) || "");
  console.log("[nongmin] category parsed items=" + cards.length);
  return cards.map(function (item) {
    const mediaType = String(params && params.categoryId) === "1" ? "movie" : "tv";
    return {
      id: item.url,
      type: mediaType,
      title: item.rawTitle,
      name: item.rawTitle,
      posterPath: item.cover || "",
      description: item.remark || "",
      mediaType: mediaType,
      link: item.url,
      detailUrl: item.url
    };
  });
}

async function loadDetail(link) {
  let originalLink = link;
  let itemTitle = "";
  if (link && typeof link === "object") {
    originalLink = link.detailUrl || link.link || link.id || link.url || "";
    itemTitle = String(link.title || link.name || "").trim();
  }
  const url = String(originalLink || "").trim();
  if (!url) return {};

  const playlist = await loadPlaylist(url);
  const profiles = await buildNongminPlaybackProfiles(playlist || [], url);
  if (!profiles.length) return {};

  const maxTrackCount = profiles.reduce(function (count, profile) {
    return Math.max(count, profile && profile.group && profile.group.tracks ? profile.group.tracks.length : 0);
  }, 0);
  const isSeries = maxTrackCount > 1 || profiles.some(function (profile) {
    return looksLikeSeriesGroup(profile.group);
  });

  if (isSeries) {
    const episodeItems = await resolveNongminSeriesEpisodes(url, profiles);
    if (!episodeItems.length) return {};

    return {
      id: url,
      type: "detail",
      title: itemTitle,
      mediaType: "tv",
      seasonCount: 1,
      episodeCount: episodeItems.length,
      currentSeason: 1,
      currentEpisode: 1,
      currentSeasonId: url + "#s1",
      currentEpisodeId: episodeItems[0].id,
      currentEpisodeName: episodeItems[0].title,
      seasons: [
        {
          id: url + "#s1",
          seasonNumber: 1,
          title: "第1季",
          episodeCount: episodeItems.length,
          episodes: episodeItems
        }
      ],
      episodeItems: episodeItems,
      episodes: episodeItems,
      episode_items: episodeItems,
      seasonItems: [
        {
          id: url + "#s1",
          seasonNumber: 1,
          title: "第1季",
          episodeCount: episodeItems.length,
          episodes: episodeItems
        }
      ],
      season_items: [
        {
          id: url + "#s1",
          seasonNumber: 1,
          title: "第1季",
          episodeCount: episodeItems.length,
          episodes: episodeItems
        }
      ],
      link: url
    };
  }

  const movie = await resolveNongminMoviePlan(url, profiles);
  if (!movie || !movie.url) return {};

  return {
    id: url,
    type: "detail",
    title: itemTitle,
    mediaType: "movie",
    videoUrl: movie.url,
    video_url: movie.url,
    url: movie.url,
    playUrl: movie.url,
    playerType: movie.playerType || "system",
    sourceName: movie.sourceName || "",
    quality: formatNongminQuality(movie),
    link: url
  };
}

async function searchVideos(params) {
  params = params || {};
  const keyword = String(params.keyword || params.text || params.title || "").trim();
  const page = Math.max(1, toInt(params.page, 1));
  if (!keyword || page > 1) return [];

  const results = await searchSite(keyword);
  const typedResults = await Promise.all(results.map(async function (item) {
    let mediaType = "movie";
    let episodeCount = 0;

    try {
      const playlist = await loadPlaylist(item.url);
      const group = pickBestGroup(playlist || []);
      if (looksLikeSeriesGroup(group)) {
        mediaType = "tv";
        episodeCount = group.tracks.length;
      }
    } catch (error) {
      console.log("[nongmin-search] classify error=" + String(error && error.message || error));
    }

    return {
      item: item,
      mediaType: mediaType,
      episodeCount: episodeCount
    };
  }));

  return typedResults.map(function (entry) {
    const item = entry.item;
    const mediaType = entry.mediaType;
    const result = {
      id: item.url,
      type: mediaType,
      title: item.rawTitle,
      name: item.rawTitle,
      posterPath: item.cover || "",
      description: item.remark || "",
      mediaType: mediaType,
      seasonCount: mediaType === "tv" ? 1 : undefined,
      episodeCount: mediaType === "tv" ? entry.episodeCount : undefined,
      currentSeason: mediaType === "tv" ? 1 : undefined,
      currentEpisode: mediaType === "tv" ? 1 : undefined,
      link: item.url,
      detailUrl: item.url
    };

    return result;
  });
}

function toInt(v, d) {
  const n = parseInt(v, 10);
  return isNaN(n) ? d || 0 : n;
}

function nowMs() {
  return typeof Date.now === "function" ? Date.now() : new Date().getTime();
}

function makeCacheKey(parts) {
  return parts.map(p => String(p || "")).join("||");
}

function cacheGet(key) {
  const item = __cache[key];
  if (!item) return undefined;
  if (nowMs() - item.time > CACHE_TTL) {
    delete __cache[key];
    return undefined;
  }
  return item.value;
}

function cacheSet(key, value) {
  __cache[key] = { time: nowMs(), value: value };
  return value;
}

function pad2(n) {
  n = parseInt(n, 10);
  if (isNaN(n)) return "";
  return n < 10 ? "0" + n : String(n);
}

function buildHeaders(url, extra) {
  return Object.assign({ "User-Agent": UA }, extra || {});
}

async function httpGet(url, extra) {
  const headers = buildHeaders(url, extra);

  if (typeof fetch === "function") {
    console.log("[nongmin] GET transport=fetch");
    const response = await fetch(url, {
      method: "GET",
      headers: headers,
      credentials: "include",
      cache: "no-store"
    });
    const data = typeof response.text === "function"
      ? await response.text()
      : String(response.data || "");
    console.log("[nongmin] GET fetch status=" + response.status + " bytes=" + data.length);
    if (response.ok === false) {
      throw new Error("http get " + response.status + ": " + url);
    }
    return { data: data, status: response.status };
  }

  console.log("[nongmin] GET transport=Widget.http");
  const response = await Widget.http.get(url, { headers: headers, timeout: 15000 });
  console.log("[nongmin] GET Widget.http bytes=" + String((response && response.data) || "").length);
  return response;
}

async function httpPost(url, body, extra) {
  const headers = buildHeaders(
    url,
    Object.assign({ "Content-Type": "application/x-www-form-urlencoded" }, extra || {})
  );

  if (typeof fetch === "function") {
    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: body,
      credentials: "include",
      cache: "no-store"
    });
    const data = typeof response.text === "function"
      ? await response.text()
      : String(response.data || "");
    if (response.ok === false) {
      throw new Error("http post " + response.status + ": " + url);
    }
    return { data: data, status: response.status };
  }

  return await Widget.http.post(url, body, { headers: headers, timeout: 15000 });
}

function isBadHref(url) {
  url = String(url || "").trim();

  if (!url) return true;
  if (url === "#") return true;
  if (/^javascript:/i.test(url)) return true;
  if (/^void/i.test(url)) return true;

  return false;
}

function absoluteUrl(url) {
  url = String(url || "").trim();

  if (isBadHref(url)) return "";
  if (/^https?:\/\//i.test(url)) return url;

  if (!url.startsWith("/")) url = "/" + url;

  return SITE + url;
}

function htmlDecode(text) {
  return String(text || "")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#34;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&nbsp;/g, " ");
}

function stripTags(text) {
  return String(text || "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeName(text) {
  return String(text || "")
    .replace(/\s+/g, "")
    .replace(/[：:·・,，.。!！?？\-—_'’"“”()（）\[\]【】]/g, "")
    .toLowerCase();
}

function stripTitleMeta(text) {
  return String(text || "")
    .replace(/[\(（][^\)）]*[\)）]/g, "")
    .replace(/第[0-9一二两三四五六七八九十百零〇]+季/g, "")
    .replace(/season\s*\d+/ig, "")
    .replace(/\bs\d{1,2}\b/ig, "")
    .trim();
}

const CN_NUM_MAP = {
  "零": 0,
  "〇": 0,
  "一": 1,
  "二": 2,
  "两": 2,
  "三": 3,
  "四": 4,
  "五": 5,
  "六": 6,
  "七": 7,
  "八": 8,
  "九": 9
};

function cnToNum(s) {
  s = String(s || "").trim();

  if (!s) return 0;
  if (/^\d+$/.test(s)) return parseInt(s, 10);

  if (s === "十") return 10;

  let total = 0;
  s = s.replace(/^[零〇]+/, "");
  if (!s) return total;

  if (s.indexOf("百") >= 0) {
    const arr = s.split("百");
    const h = CN_NUM_MAP[arr[0]] || 1;
    total += h * 100;
    s = (arr[1] || "").replace(/^[零〇]+/, "");
  }

  if (s.indexOf("十") >= 0) {
    const arr = s.split("十");
    const t = arr[0] ? CN_NUM_MAP[arr[0]] || 0 : 1;
    const u = arr[1] ? CN_NUM_MAP[arr[1]] || 0 : 0;
    total += t * 10 + u;
    return total;
  }

  if (s && CN_NUM_MAP[s] != null) return total + CN_NUM_MAP[s];

  return total;
}

function extractEpisodeNumber(text) {
  const s = String(text || "");

  let m = s.match(/第\s*([0-9一二两三四五六七八九十百零〇]+)\s*[集话期]/);
  if (m) return cnToNum(m[1]);

  m = s.match(/(?:EP|E|episode)\s*0*(\d{1,4})/i);
  if (m) return parseInt(m[1], 10);

  m = s.match(/(?:^|[^\d])0*(\d{1,4})(?:$|[^\d])/);
  if (m) return parseInt(m[1], 10);

  return 0;
}

function getWantedEpisode(params) {
  params = params || {};

  let n = 0;

  // 最优先：明确集数字段
  n =
    toInt(params.episode, 0) ||
    toInt(params.episodeNumber, 0) ||
    toInt(params.episodeNo, 0) ||
    toInt(params.episodeNum, 0) ||
    toInt(params.ep, 0) ||
    toInt(params.epNumber, 0) ||
    toInt(params.number, 0) ||
    toInt(params.currentEpisode, 0);

  if (n > 0) return n;

  // episodeIndex 通常是 0 基：第 5 集 = 4
  if (params.episodeIndex !== undefined && params.episodeIndex !== null) {
    const idx = toInt(params.episodeIndex, -1);
    if (idx >= 0) return idx + 1;
  }

  if (params.epIndex !== undefined && params.epIndex !== null) {
    const idx = toInt(params.epIndex, -1);
    if (idx >= 0) return idx + 1;
  }

  // 从文字字段提取
  n =
    extractEpisodeNumber(params.episodeName) ||
    extractEpisodeNumber(params.episodeTitle) ||
    extractEpisodeNumber(params.name) ||
    extractEpisodeNumber(params.subtitle);

  if (n > 0) return n;

  return 0;
}

function parseSearchResults(html) {
  html = String(html || "");

  // Category pages contain navigation <li> elements before the actual card list.
  const listMarker = html.indexOf("globalPicList");
  if (listMarker >= 0) {
    const listStart = html.indexOf("<ul", listMarker);
    const listEnd = html.indexOf("</ul>", listStart);
    if (listStart >= 0 && listEnd > listStart) {
      html = html.slice(listStart, listEnd + 5);
    }
  }

  const out = [];
  const liReg = /<li[\s\S]*?<\/li>/gi;
  let li;

  while ((li = liReg.exec(html))) {
    const item = li[0];

    let href = "";
    let title = "";
    let cover = "";
    let remark = "";

    let m;

    m = item.match(/<a[^>]+href=["']([^"']+)["'][^>]*>/i);
    if (m) href = htmlDecode(m[1]);

    m = item.match(/<[^>]+class=["'][^"']*sTit[^"']*["'][^>]*>([\s\S]*?)<\/[^>]+>/i);
    if (m) title = stripTags(htmlDecode(m[1]));

    if (!title) {
      m = item.match(/title=["']([^"']+)["']/i);
      if (m) title = htmlDecode(m[1]).trim();
    }

    if (!title) {
      m = item.match(/alt=["']([^"']+)["']/i);
      if (m) title = htmlDecode(m[1]).trim();
    }

    m = item.match(/data-src=["']([^"']+)["']/i);
    if (!m) m = item.match(/src=["']([^"']+)["']/i);
    if (m) cover = htmlDecode(m[1]);

    m = item.match(/<[^>]+class=["'][^"']*sStyle[^"']*["'][^>]*>([\s\S]*?)<\/[^>]+>/i);
    if (!m) m = item.match(/<[^>]+class=["'][^"']*sDes[^"']*["'][^>]*>([\s\S]*?)<\/[^>]+>/i);
    if (m) remark = stripTags(htmlDecode(m[1]));

    const abs = absoluteUrl(href);

    if (abs && title) {
      out.push({
        url: abs,
        rawTitle: title,
        cover: absoluteUrl(cover),
        remark: remark
      });
    }
  }

  if (!out.length) {
    const re = /<a[^>]+href=["']([^"']+)["'][^>]*title=["']([^"']+)["'][^>]*>/ig;
    let m;

    while ((m = re.exec(html))) {
      const href = htmlDecode(m[1]);
      const title = htmlDecode(m[2]).trim();
      const abs = absoluteUrl(href);

      if (abs && title && /vod|detail/i.test(abs)) {
        out.push({
          url: abs,
          rawTitle: title,
          cover: "",
          remark: ""
        });
      }
    }
  }

  return out;
}

function parseMapResults(html) {
  html = String(html || "");

  const out = [];
  const seen = {};
  const re = /<a[^>]+href=["']([^"']*vod-detail-id-\d+\.html)["'][^>]*>([\s\S]*?)<\/a>/gi;
  let m;

  while ((m = re.exec(html))) {
    const url = absoluteUrl(htmlDecode(m[1]));
    const title = stripTags(htmlDecode(m[2])).trim();

    if (!url || !title || seen[url]) continue;
    seen[url] = true;
    out.push({
      url: url,
      rawTitle: title,
      cover: "",
      remark: ""
    });
  }

  return out;
}

async function searchSite(keyword) {
  const cacheKey = makeCacheKey(["search", keyword]);
  const cached = cacheGet(cacheKey);
  if (cached !== undefined) return cached;

  try {
    const url = SITE + "/index.php?m=vod-search";
    const body = "wd=" + encodeURIComponent(keyword);
    const res = await httpPost(url, body);
    const results = parseSearchResults((res && res.data) || "");

    if (results.length) return cacheSet(cacheKey, results);
  } catch (e) {}

  const mapCacheKey = "vod-map-all";
  let all = cacheGet(mapCacheKey);

  if (all === undefined) {
    const mapRes = await httpGet(SITE + "/vod-map.html");
    all = cacheSet(mapCacheKey, parseMapResults((mapRes && mapRes.data) || ""));
  }

  const wantBaseNorm = normalizeName(stripTitleMeta(keyword));
  const results = (all || []).filter(item => scoreResult(item, wantBaseNorm) >= 0);

  return cacheSet(cacheKey, results);
}

function scoreResult(item, wantBaseNorm) {
  const rawBase = stripTitleMeta(item.rawTitle);
  const baseNorm = normalizeName(rawBase);

  if (!baseNorm || !wantBaseNorm) return -1;

  if (baseNorm === wantBaseNorm) return 320;
  if (baseNorm.indexOf(wantBaseNorm) >= 0) return 180;
  if (wantBaseNorm.indexOf(baseNorm) >= 0) return 150;

  return -1;
}

function pickBestResult(results, wantBaseNorm) {
  let best = null;
  let bestScore = -Infinity;

  for (const item of results) {
    const sc = scoreResult(item, wantBaseNorm);

    if (sc > bestScore) {
      bestScore = sc;
      best = item;
    }
  }

  return bestScore >= 0 ? best : null;
}

function parsePlayPageUrls(html) {
  html = String(html || "");

  const urls = [];
  const re = /<a[^>]+href=["']([^"']+)["'][^>]*>/ig;
  let m;

  while ((m = re.exec(html))) {
    const href = htmlDecode(m[1]).trim();

    if (isBadHref(href)) continue;
    if (!/vod[-_]?play|play/i.test(href)) continue;

    const abs = absoluteUrl(href);

    if (abs && urls.indexOf(abs) < 0) {
      urls.push(abs);
    }
  }

  return urls;
}

function parseMacVars(html) {
  const text = String(html || "");

  const fromMatch =
    text.match(/mac_from\s*=\s*'([^']*)'/) ||
    text.match(/mac_from\s*=\s*"([^"]*)"/);

  const urlMatch =
    text.match(/mac_url\s*=\s*'([^']+)'/) ||
    text.match(/mac_url\s*=\s*"([^"]+)"/);

  if (!fromMatch || !urlMatch) return [];

  const fromList = fromMatch[1].split("$$$");
  const urlList = urlMatch[1].split("$$$");

  const groups = [];

  for (let i = 0; i < fromList.length; i++) {
    const sourceName = fromList[i] || "默认线路";
    const eps = String(urlList[i] || "").split("#").filter(Boolean);

    const tracks = [];

    for (let j = 0; j < eps.length; j++) {
      const parts = eps[j].split("$");
      const name = htmlDecode(parts[0] || "第" + (j + 1) + "集");
      const rawUrl = htmlDecode(parts[1] || "");

      if (!rawUrl || isBadHref(rawUrl)) continue;

      const ep = extractEpisodeNumber(name) || j + 1;

      tracks.push({
        name: name,
        episode: ep,
        index: j + 1,
        source: sourceName,
        url: rawUrl
      });
    }

    if (tracks.length) {
      groups.push({
        title: sourceName,
        tracks: tracks
      });
    }
  }

  return groups;
}

async function loadPlaylist(detailUrl) {
  const cacheKey = makeCacheKey(["playlist", detailUrl]);
  const cached = cacheGet(cacheKey);
  if (cached !== undefined) return cached;

  const detailRes = await httpGet(detailUrl);
  const detailHtml = (detailRes && detailRes.data) || "";

  let groups = parseMacVars(detailHtml);
  if (groups && groups.length) return cacheSet(cacheKey, groups);

  const playUrls = parsePlayPageUrls(detailHtml);

  if (!playUrls.length) return [];

  const maxTry = Math.min(playUrls.length, 5);

  for (let i = 0; i < maxTry; i++) {
    try {
      const epRes = await httpGet(playUrls[i]);
      const epHtml = (epRes && epRes.data) || "";

      groups = parseMacVars(epHtml);

      if (groups && groups.length) {
        return cacheSet(cacheKey, groups);
      }
    } catch (e) {}
  }

  return [];
}

function pickBestGroup(groups) {
  if (!groups || !groups.length) return null;

  let best = groups[0];
  let bestCount = best.tracks ? best.tracks.length : 0;

  for (let i = 1; i < groups.length; i++) {
    const count = groups[i].tracks ? groups[i].tracks.length : 0;

    if (count > bestCount) {
      best = groups[i];
      bestCount = count;
    }
  }

  return best;
}

function looksLikeSeriesGroup(group) {
  return !!(
    group &&
    group.tracks &&
    group.tracks.length > 1 &&
    group.tracks.some(function (track) {
      return /第[0-9一二两三四五六七八九十百零〇]+集|S\d{1,2}E\d{1,3}/i.test(String(track.name || ""));
    })
  );
}

async function resolveEpisodeItems(detailUrl, tracks) {
  const list = Array.isArray(tracks) ? tracks : [];
  const resolved = await Promise.all(list.map(async function (track, index) {
    if (!track || !track.url) return null;

    const videoUrl = await resolveDirectUrl(track.url);
    if (!videoUrl) return null;

    const parsedEpisode = extractEpisodeNumber(track.name);
    const episodeNumber = toInt(track.episode, 0) || parsedEpisode || index + 1;
    const episodeTitle = track.name || track.episode || ("第" + pad2(episodeNumber) + "集");

    return {
      id: detailUrl + "#e" + episodeNumber,
      seasonNumber: 1,
      episodeNumber: episodeNumber,
      episode: episodeNumber,
      title: episodeTitle,
      name: episodeTitle,
      videoUrl: videoUrl,
      video_url: videoUrl,
      url: videoUrl
    };
  }));

  return resolved.filter(Boolean);
}

function pickTrack(group, wantEpisode, isMovie) {
  if (!group || !group.tracks || !group.tracks.length) return null;

  const tracks = group.tracks;

  if (isMovie) return tracks[0];

  if (wantEpisode > 0) {
    let tr = tracks.find(t => toInt(t.episode, -1) === wantEpisode);
    if (tr) return tr;

    tr = tracks.find(t => toInt(t.index, -1) === wantEpisode);
    if (tr) return tr;

    tr = tracks.find(t => extractEpisodeNumber(t.name) === wantEpisode);
    if (tr) return tr;
  }

  return tracks[0];
}

function normalizePlayUrl(url) {
  url = String(url || "").trim();

  if (!url) return "";

  url = htmlDecode(url)
    .replace(/\\\//g, "/")
    .replace(/\\\\/g, "\\");

  try {
    if (/^https?%3A%2F%2F/i.test(url)) {
      url = decodeURIComponent(url);
    }
  } catch (e) {}

  if (url.startsWith("//")) {
    url = "https:" + url;
  }

  if (!/^https?:\/\//i.test(url)) {
    return "";
  }

  if (isBadHref(url)) return "";

  return url;
}

function parsePlayerUrl(html) {
  const text = String(html || "");

  let m;

  m = text.match(/var\s+config\s*=\s*(\{[\s\S]*?\})\s*[,;]?/);

  if (m && m[1]) {
    const configString = m[1];

    const urlMatch =
      configString.match(/["']url["']\s*:\s*["']([^"']+)["']/) ||
      configString.match(/url\s*:\s*["']([^"']+)["']/);

    if (urlMatch && urlMatch[1]) {
      const u = normalizePlayUrl(urlMatch[1]);
      if (u) return u;
    }
  }

  m = text.match(/https?:\\?\/\\?\/[^"'<>]+?\.m3u8[^"'<>]*/i);

  if (m && m[0]) {
    const u = normalizePlayUrl(m[0]);
    if (u) return u;
  }

  m =
    text.match(/["']url["']\s*:\s*["']([^"']+)["']/) ||
    text.match(/url\s*:\s*["']([^"']+)["']/);

  if (m && m[1]) {
    const u = normalizePlayUrl(m[1]);
    if (u) return u;
  }

  return "";
}

const NONGMIN_HLS_TIMEOUT_MS = 3200;
const NONGMIN_SEGMENT_TIMEOUT_MS = 2800;
const NONGMIN_EPISODE_TIMEOUT_MS = 2200;
const NONGMIN_EPISODE_BUDGET_MS = 8000;
const NONGMIN_PROBE_CONCURRENCY = 6;

async function mapNongminWithLimit(items, limit, iterator) {
  const source = Array.isArray(items) ? items : [];
  const results = new Array(source.length);
  let cursor = 0;
  const workerCount = Math.max(1, Math.min(toInt(limit, 1), source.length || 1));

  async function worker() {
    while (true) {
      const index = cursor++;
      if (index >= source.length) return;
      results[index] = await iterator(source[index], index);
    }
  }

  const workers = [];
  for (let i = 0; i < workerCount; i++) workers.push(worker());
  await Promise.all(workers);
  return results;
}

function positiveNongminNumber(value) {
  const number = parseInt(String(value || ""), 10);
  return isFinite(number) && number > 0 ? number : 0;
}

function parseNongminHlsAttributes(attributeText) {
  const attributes = {};
  const source = String(attributeText || "");
  let token = "";
  let quoted = false;

  for (let i = 0; i <= source.length; i++) {
    const ch = i < source.length ? source.charAt(i) : ",";
    if (ch === '"' && source.charAt(i - 1) !== "\\") {
      quoted = !quoted;
      token += ch;
      continue;
    }
    if (ch === "," && !quoted) {
      const part = token.trim();
      token = "";
      if (!part) continue;
      const equalsIndex = part.indexOf("=");
      if (equalsIndex <= 0) continue;
      const key = part.slice(0, equalsIndex).trim().toUpperCase();
      let value = part.slice(equalsIndex + 1).trim();
      if (value.length >= 2 && value.charAt(0) === '"' && value.charAt(value.length - 1) === '"') {
        value = value.slice(1, -1).replace(/\\"/g, '"');
      }
      attributes[key] = value;
      continue;
    }
    token += ch;
  }

  return attributes;
}

function parseNongminHlsResolution(value, uri) {
  let width = 0;
  let height = 0;
  const declared = String(value || "").match(/(\d{2,5})\s*x\s*(\d{2,5})/i);
  if (declared) {
    width = positiveNongminNumber(declared[1]);
    height = positiveNongminNumber(declared[2]);
  }

  const pathText = String(uri || "");
  if (!width || !height) {
    const pathResolution = pathText.match(/(?:^|[\/_\-.])(\d{2,5})x(\d{2,5})(?:[\/_\-.]|$)/i);
    if (pathResolution) {
      width = positiveNongminNumber(pathResolution[1]);
      height = positiveNongminNumber(pathResolution[2]);
    }
  }
  if (!height) {
    const heightOnly = pathText.match(/(?:^|[\/_\-.])(\d{3,4})p(?:[\/_\-.]|$)/i);
    if (heightOnly) {
      height = positiveNongminNumber(heightOnly[1]);
      width = height ? Math.round(height * 16 / 9) : 0;
    }
  }

  return {
    width: width,
    height: height,
    pixels: width && height ? width * height : 0
  };
}

function resolveNongminHlsUrl(uri, playlistUrl) {
  const value = String(uri || "").trim();
  const base = String(playlistUrl || "").trim();
  if (!value) return "";
  if (/^https?:\/\//i.test(value)) return normalizePlayUrl(value);
  if (/^\/\//.test(value)) return normalizePlayUrl("https:" + value);

  try {
    if (typeof URL !== "undefined") return normalizePlayUrl(new URL(value, base).toString());
  } catch (e) {}

  const cleanBase = base.replace(/[?#].*$/, "");
  const originMatch = cleanBase.match(/^(https?:\/\/[^/]+)/i);
  if (value.charAt(0) === "/" && originMatch) return normalizePlayUrl(originMatch[1] + value);
  const slashIndex = cleanBase.lastIndexOf("/");
  const directory = slashIndex >= 0 ? cleanBase.slice(0, slashIndex + 1) : cleanBase + "/";
  return normalizePlayUrl(directory + value.replace(/^\.\//, ""));
}

function parseNongminMasterVariants(masterText, playlistUrl) {
  const lines = String(masterText || "").split(/\r?\n/);
  const variants = [];

  for (let i = 0; i < lines.length; i++) {
    const line = String(lines[i] || "").trim();
    if (!/^#EXT-X-STREAM-INF\s*:/i.test(line)) continue;

    const attributes = parseNongminHlsAttributes(line.slice(line.indexOf(":") + 1));
    let uri = "";
    let uriIndex = i + 1;

    while (uriIndex < lines.length) {
      const candidate = String(lines[uriIndex] || "").trim();
      if (!candidate || candidate.charAt(0) === "#") {
        uriIndex++;
        continue;
      }
      uri = candidate;
      break;
    }

    if (!uri) continue;
    const resolution = parseNongminHlsResolution(attributes.RESOLUTION, uri);
    const averageBandwidth = positiveNongminNumber(attributes["AVERAGE-BANDWIDTH"]);
    const peakBandwidth = positiveNongminNumber(attributes.BANDWIDTH);

    variants.push({
      url: resolveNongminHlsUrl(uri, playlistUrl),
      uri: uri,
      codecs: String(attributes.CODECS || ""),
      resolution: String(attributes.RESOLUTION || ""),
      width: resolution.width,
      height: resolution.height,
      pixels: resolution.pixels,
      bandwidth: averageBandwidth || peakBandwidth,
      peakBandwidth: peakBandwidth,
      frameRate: parseFloat(String(attributes["FRAME-RATE"] || "0")) || 0,
      order: variants.length
    });
    i = uriIndex;
  }

  return variants;
}

function compareNongminQuality(left, right) {
  left = left || {};
  right = right || {};
  const fields = ["verified", "pixels", "height", "width", "bandwidth", "peakBandwidth", "frameRate"];

  for (let i = 0; i < fields.length; i++) {
    const field = fields[i];
    const leftValue = field === "verified" ? (left[field] ? 1 : 0) : Number(left[field] || 0);
    const rightValue = field === "verified" ? (right[field] ? 1 : 0) : Number(right[field] || 0);
    const difference = rightValue - leftValue;
    if (difference) return difference;
  }

  return 0;
}

function selectNongminHighestVariant(masterText, playlistUrl) {
  const variants = parseNongminMasterVariants(masterText, playlistUrl);
  if (!variants.length) return null;

  variants.sort(function (left, right) {
    const quality = compareNongminQuality(
      Object.assign({ verified: true }, left),
      Object.assign({ verified: true }, right)
    );
    if (quality) return quality;
    return left.order - right.order;
  });

  return variants[0];
}

function classifyNongminCodec(codecs) {
  const value = String(codecs || "").toLowerCase();
  if (/(^|[,\s])(hvc1|hev1|hevc|h265|av01|av1|vp09|vp9|dvhe|dvh1)(?:\.|[,\s]|$)/i.test(value)) {
    return "modern";
  }
  if (/(^|[,\s])(avc1|avc3|h264)(?:\.|[,\s]|$)/i.test(value)) {
    return "avc";
  }
  return "unknown";
}

function chooseNongminPlayerType(codecFamily) {
  return codecFamily === "avc" ? "ijk" : "system";
}

function firstNongminMediaSegmentUrl(playlist, playlistUrl) {
  const lines = String(playlist || "").split(/\r?\n/);
  let expectSegment = false;

  for (let i = 0; i < lines.length; i++) {
    const line = String(lines[i] || "").trim();
    if (/^#EXTINF:/i.test(line)) {
      expectSegment = true;
      continue;
    }
    if (!line || line.charAt(0) === "#") continue;
    if (expectSegment) return resolveNongminHlsUrl(line, playlistUrl);
    expectSegment = false;
  }

  return "";
}

function nongminResponseBytes(data) {
  if (data == null) return [];
  if (Array.isArray(data)) return data;
  if (typeof Uint8Array !== "undefined" && data instanceof Uint8Array) return data;
  if (typeof ArrayBuffer !== "undefined" && data instanceof ArrayBuffer) return new Uint8Array(data);
  if (data && data.buffer && typeof Uint8Array !== "undefined") {
    try {
      return new Uint8Array(data.buffer, data.byteOffset || 0, data.byteLength || data.length);
    } catch (e) {}
  }

  const source = String(data || "");
  const bytes = [];
  const limit = Math.min(source.length, 131072);
  for (let i = 0; i < limit; i++) bytes.push(source.charCodeAt(i) & 255);
  return bytes;
}

function inspectNongminTsCodec(bytes) {
  bytes = nongminResponseBytes(bytes);
  let syncOffset = -1;

  for (let offset = 0; offset < 188 && offset + 376 < bytes.length; offset++) {
    if (bytes[offset] === 71 && bytes[offset + 188] === 71 && bytes[offset + 376] === 71) {
      syncOffset = offset;
      break;
    }
  }

  if (syncOffset < 0) return { family: "unknown", streamTypes: [] };

  let pmtPid = -1;
  const streamTypes = [];

  for (let packet = syncOffset; packet + 188 <= bytes.length; packet += 188) {
    if (bytes[packet] !== 71) continue;
    const payloadStart = (bytes[packet + 1] & 64) !== 0;
    const pid = ((bytes[packet + 1] & 31) << 8) | bytes[packet + 2];
    const adaptation = (bytes[packet + 3] >> 4) & 3;
    if (adaptation === 0 || adaptation === 2) continue;

    let cursor = packet + 4;
    if (adaptation === 3) cursor += 1 + bytes[cursor];
    if (cursor >= packet + 188) continue;
    if (payloadStart) cursor += 1 + bytes[cursor];
    if (cursor + 12 >= packet + 188) continue;

    if (pid === 0 && bytes[cursor] === 0) {
      const patLength = ((bytes[cursor + 1] & 15) << 8) | bytes[cursor + 2];
      const patEnd = Math.min(cursor + 3 + patLength - 4, packet + 188);
      for (let pat = cursor + 8; pat + 3 < patEnd; pat += 4) {
        const program = (bytes[pat] << 8) | bytes[pat + 1];
        if (program) {
          pmtPid = ((bytes[pat + 2] & 31) << 8) | bytes[pat + 3];
          break;
        }
      }
    } else if (pid === pmtPid && bytes[cursor] === 2) {
      const pmtLength = ((bytes[cursor + 1] & 15) << 8) | bytes[cursor + 2];
      const programInfoLength = ((bytes[cursor + 10] & 15) << 8) | bytes[cursor + 11];
      const pmtEnd = Math.min(cursor + 3 + pmtLength - 4, packet + 188);

      for (let stream = cursor + 12 + programInfoLength; stream + 4 < pmtEnd;) {
        const streamType = bytes[stream];
        const infoLength = ((bytes[stream + 3] & 15) << 8) | bytes[stream + 4];
        if (streamTypes.indexOf(streamType) < 0) streamTypes.push(streamType);
        stream += 5 + infoLength;
      }
      if (streamTypes.length) break;
    }
  }

  if (streamTypes.indexOf(36) >= 0) return { family: "modern", streamTypes: streamTypes };
  if (streamTypes.indexOf(27) >= 0) return { family: "avc", streamTypes: streamTypes };
  return { family: "unknown", streamTypes: streamTypes };
}

function decodeNongminResponseText(data) {
  if (typeof data === "string") return data;
  const bytes = nongminResponseBytes(data);
  if (!bytes.length) return String(data || "");

  if (typeof TextDecoder !== "undefined") {
    try {
      return new TextDecoder("utf-8").decode(bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes));
    } catch (e) {}
  }

  let text = "";
  for (let i = 0; i < bytes.length; i++) text += String.fromCharCode(bytes[i]);
  return text;
}

function getNongminPlaybackHeaders(extra) {
  return Object.assign({
    "User-Agent": UA,
    "Accept": "application/vnd.apple.mpegurl,application/x-mpegURL,video/mp2t,video/*,*/*",
    "Referer": PLAYER_SITE + "/"
  }, extra || {});
}

async function boundedNongminPlaybackGet(url, headers, timeoutMs, binary) {
  const timeout = Math.max(800, Math.min(Number(timeoutMs || NONGMIN_HLS_TIMEOUT_MS), 5000));

  if (typeof Widget !== "undefined" && Widget.http && typeof Widget.http.get === "function") {
    const response = await Widget.http.get(url, {
      headers: headers || {},
      allow_redirects: true,
      timeout: timeout
    });
    const status = Number(response && response.status || 0);
    if (!response || response.ok === false || status >= 400) {
      throw new Error("playback HTTP " + status + ": " + url);
    }
    return response;
  }

  if (typeof fetch !== "function") throw new Error("No playback HTTP transport");

  let timer = null;
  const request = (async function () {
    const response = await fetch(url, {
      method: "GET",
      headers: headers || {},
      cache: "no-store"
    });
    if (response.ok === false) throw new Error("playback HTTP " + response.status + ": " + url);
    let data;
    if (binary && typeof response.arrayBuffer === "function") {
      data = new Uint8Array(await response.arrayBuffer());
    } else {
      data = typeof response.text === "function" ? await response.text() : String(response.data || "");
    }
    return {
      data: data,
      status: response.status,
      ok: response.ok,
      url: response.url || url
    };
  })();

  if (typeof setTimeout !== "function" || typeof Promise.race !== "function") return await request;

  try {
    return await Promise.race([
      request,
      new Promise(function (_, reject) {
        timer = setTimeout(function () {
          reject(new Error("playback timeout after " + timeout + "ms: " + url));
        }, timeout);
      })
    ]);
  } finally {
    if (timer && typeof clearTimeout === "function") clearTimeout(timer);
  }
}

async function fetchNongminHlsText(url, timeoutMs) {
  const response = await boundedNongminPlaybackGet(
    url,
    getNongminPlaybackHeaders(),
    timeoutMs,
    false
  );
  const body = decodeNongminResponseText(response && response.data);
  if (!/^\s*#EXTM3U/i.test(body)) throw new Error("not an HLS playlist: " + url);

  return {
    body: body,
    url: String(response && (response.url || response.finalUrl || response.requestUrl) || url)
  };
}

async function probeNongminSegmentCodec(segmentUrl, timeoutMs) {
  const response = await boundedNongminPlaybackGet(
    segmentUrl,
    getNongminPlaybackHeaders({ "Range": "bytes=0-65535" }),
    Math.min(Number(timeoutMs || NONGMIN_SEGMENT_TIMEOUT_MS), NONGMIN_SEGMENT_TIMEOUT_MS),
    true
  );
  return inspectNongminTsCodec(response && response.data);
}

async function inspectNongminHlsPlan(directUrl, probeCodec, timeoutMs) {
  const timeout = Math.max(900, Math.min(Number(timeoutMs || NONGMIN_HLS_TIMEOUT_MS), NONGMIN_HLS_TIMEOUT_MS));
  let current = await fetchNongminHlsText(directUrl, timeout);
  let finalUrl = current.url || directUrl;
  let mediaBody = current.body;
  let mediaUrl = finalUrl;
  let codecs = "";
  let codecFamily = "unknown";
  const quality = {
    width: 0,
    height: 0,
    pixels: 0,
    bandwidth: 0,
    peakBandwidth: 0,
    frameRate: 0,
    resolution: ""
  };

  for (let depth = 0; depth < 3; depth++) {
    const selected = selectNongminHighestVariant(current.body, current.url || finalUrl);
    if (!selected || !selected.url) {
      mediaBody = current.body;
      mediaUrl = current.url || finalUrl;
      break;
    }

    finalUrl = selected.url;
    if (selected.width) quality.width = selected.width;
    if (selected.height) quality.height = selected.height;
    if (selected.pixels) quality.pixels = selected.pixels;
    if (selected.bandwidth) quality.bandwidth = selected.bandwidth;
    if (selected.peakBandwidth) quality.peakBandwidth = selected.peakBandwidth;
    if (selected.frameRate) quality.frameRate = selected.frameRate;
    if (selected.resolution) quality.resolution = selected.resolution;

    const selectedFamily = classifyNongminCodec(selected.codecs);
    if (selected.codecs) codecs = selected.codecs;
    if (selectedFamily !== "unknown") codecFamily = selectedFamily;

    current = await fetchNongminHlsText(finalUrl, timeout);
    mediaBody = current.body;
    mediaUrl = current.url || finalUrl;
  }

  let streamTypes = [];
  if (codecFamily === "unknown" && probeCodec) {
    const segmentUrl = firstNongminMediaSegmentUrl(mediaBody, mediaUrl);
    if (segmentUrl) {
      const codecProbe = await probeNongminSegmentCodec(segmentUrl, timeout);
      codecFamily = codecProbe.family;
      streamTypes = codecProbe.streamTypes || [];
    }
  }

  return {
    url: finalUrl,
    verified: true,
    playerType: chooseNongminPlayerType(codecFamily),
    codecFamily: codecFamily,
    codecs: codecs,
    streamTypes: streamTypes,
    width: quality.width,
    height: quality.height,
    pixels: quality.pixels,
    bandwidth: quality.bandwidth,
    peakBandwidth: quality.peakBandwidth,
    frameRate: quality.frameRate,
    resolution: quality.resolution
  };
}

function applyNongminProfileFallback(plan, profile) {
  const result = Object.assign({}, plan || {});
  const profilePlan = profile && profile.plan ? profile.plan : null;

  if ((!result.codecFamily || result.codecFamily === "unknown") && profilePlan && profilePlan.codecFamily) {
    result.codecFamily = profilePlan.codecFamily;
    result.codecs = result.codecs || profilePlan.codecs || "";
    result.streamTypes = result.streamTypes && result.streamTypes.length
      ? result.streamTypes
      : (profilePlan.streamTypes || []);
  }

  const qualityFields = ["width", "height", "pixels", "bandwidth", "peakBandwidth", "frameRate", "resolution"];
  for (let i = 0; i < qualityFields.length; i++) {
    const field = qualityFields[i];
    if (!result[field] && profilePlan && profilePlan[field]) result[field] = profilePlan[field];
  }

  result.playerType = chooseNongminPlayerType(result.codecFamily || "unknown");
  result.sourceName = result.sourceName || (profile && profile.group && profile.group.title) || "";
  return result;
}

async function resolveNongminTrackPlan(rawUrl, detailUrl, profile, probeCodec, timeoutMs) {
  const directUrl = await resolveDirectUrl(rawUrl);
  if (!directUrl) return null;

  const fullKey = makeCacheKey(["hls-plan-full", directUrl]);
  const basicKey = makeCacheKey(["hls-plan-basic", directUrl]);
  const fullCached = cacheGet(fullKey);
  if (fullCached !== undefined) return applyNongminProfileFallback(fullCached, profile);

  if (!probeCodec) {
    const basicCached = cacheGet(basicKey);
    if (basicCached !== undefined) return applyNongminProfileFallback(basicCached, profile);
  }

  if (Number(timeoutMs || 0) <= 0) {
    return applyNongminProfileFallback({
      url: directUrl,
      verified: false,
      playerType: "system",
      codecFamily: "unknown",
      codecs: "",
      streamTypes: [],
      width: 0,
      height: 0,
      pixels: 0,
      bandwidth: 0,
      peakBandwidth: 0,
      frameRate: 0,
      resolution: ""
    }, profile);
  }

  try {
    const plan = await inspectNongminHlsPlan(directUrl, !!probeCodec, timeoutMs);
    plan.sourceName = profile && profile.group ? profile.group.title : "";
    cacheSet(basicKey, plan);
    if (probeCodec) cacheSet(fullKey, plan);
    return applyNongminProfileFallback(plan, profile);
  } catch (error) {
    console.log("[nongmin-playback] inspect failed source=" +
      String(profile && profile.group && profile.group.title || "") +
      " error=" + String(error && error.message || error));
    return applyNongminProfileFallback({
      url: directUrl,
      verified: false,
      playerType: "system",
      codecFamily: "unknown",
      codecs: "",
      streamTypes: [],
      width: 0,
      height: 0,
      pixels: 0,
      bandwidth: 0,
      peakBandwidth: 0,
      frameRate: 0,
      resolution: ""
    }, profile);
  }
}

async function buildNongminPlaybackProfiles(groups, detailUrl) {
  const list = (Array.isArray(groups) ? groups : []).filter(function (group) {
    return group && Array.isArray(group.tracks) && group.tracks.length;
  });

  const profiles = await mapNongminWithLimit(list, 3, async function (group, index) {
    const sampleTrack = group.tracks[0];
    const profile = {
      index: index,
      group: group,
      trackCount: group.tracks.length,
      plan: null
    };
    profile.plan = await resolveNongminTrackPlan(
      sampleTrack && sampleTrack.url,
      detailUrl,
      profile,
      true,
      NONGMIN_HLS_TIMEOUT_MS
    );
    return profile;
  });

  return profiles.filter(function (profile) {
    return profile && profile.plan && profile.plan.url;
  }).sort(function (left, right) {
    const quality = compareNongminQuality(left.plan, right.plan);
    if (quality) return quality;
    const countDifference = Number(right.trackCount || 0) - Number(left.trackCount || 0);
    if (countDifference) return countDifference;
    return Number(left.index || 0) - Number(right.index || 0);
  });
}

function nongminTrackEpisodeNumber(track, index) {
  return toInt(track && track.episode, 0) ||
    extractEpisodeNumber(track && track.name) ||
    toInt(track && track.index, 0) ||
    index + 1;
}

function findNongminEpisodeTrack(profile, episodeNumber, referenceIndex) {
  if (!profile || !profile.group || !profile.group.tracks) return null;
  const tracks = profile.group.tracks;

  let track = tracks.find(function (item, index) {
    return nongminTrackEpisodeNumber(item, index) === episodeNumber;
  });
  if (track) return track;

  track = tracks.find(function (item) {
    return toInt(item && item.index, 0) === episodeNumber;
  });
  if (track) return track;

  return referenceIndex >= 0 && referenceIndex < tracks.length ? tracks[referenceIndex] : null;
}

function getNongminReferenceProfile(profiles) {
  let best = null;
  for (let i = 0; i < profiles.length; i++) {
    const profile = profiles[i];
    if (!best || Number(profile.trackCount || 0) > Number(best.trackCount || 0)) best = profile;
  }
  return best;
}

function formatNongminQuality(plan) {
  plan = plan || {};
  if (plan.resolution) return String(plan.resolution);
  if (plan.width && plan.height) return String(plan.width) + "x" + String(plan.height);
  if (plan.height) return String(plan.height) + "p";
  if (plan.bandwidth) return Math.round(Number(plan.bandwidth) / 1000) + "kbps";
  return "未知";
}

function nongminEngineLabel(plan) {
  return plan && plan.playerType === "ijk" ? "MDK" : "Auto";
}

function buildNongminEpisodeItem(detailUrl, track, index, plan) {
  const episodeNumber = nongminTrackEpisodeNumber(track, index);
  const episodeTitle = track && (track.name || track.episode) || ("第" + pad2(episodeNumber) + "集");
  return {
    id: detailUrl + "#e" + episodeNumber + "-" + (index + 1),
    seasonNumber: 1,
    episodeNumber: episodeNumber,
    episode: episodeNumber,
    title: episodeTitle,
    name: episodeTitle,
    videoUrl: plan.url,
    video_url: plan.url,
    url: plan.url,
    playUrl: plan.url,
    playerType: plan.playerType || "system",
    sourceName: plan.sourceName || "",
    quality: formatNongminQuality(plan),
    codecFamily: plan.codecFamily || "unknown"
  };
}

async function resolveNongminSeriesEpisodes(detailUrl, profiles) {
  const reference = getNongminReferenceProfile(profiles);
  const referenceTracks = reference && reference.group && reference.group.tracks
    ? reference.group.tracks
    : [];
  const deadline = nowMs() + NONGMIN_EPISODE_BUDGET_MS;

  const episodes = await mapNongminWithLimit(
    referenceTracks,
    NONGMIN_PROBE_CONCURRENCY,
    async function (referenceTrack, referenceIndex) {
      const episodeNumber = nongminTrackEpisodeNumber(referenceTrack, referenceIndex);
      const candidates = [];

      for (let i = 0; i < profiles.length; i++) {
        const profile = profiles[i];
        const track = findNongminEpisodeTrack(profile, episodeNumber, referenceIndex);
        if (track && track.url) candidates.push({ profile: profile, track: track });
      }

      let fallback = null;
      for (let i = 0; i < candidates.length; i++) {
        const candidate = candidates[i];
        const remaining = deadline - nowMs();
        const timeout = remaining > 500
          ? Math.max(900, Math.min(NONGMIN_EPISODE_TIMEOUT_MS, remaining))
          : 0;
        const plan = await resolveNongminTrackPlan(
          candidate.track.url,
          detailUrl,
          candidate.profile,
          false,
          timeout
        );
        if (!plan || !plan.url) continue;

        const item = buildNongminEpisodeItem(detailUrl, candidate.track, referenceIndex, plan);
        if (!fallback) fallback = item;
        if (plan.verified) return item;
        if (nowMs() >= deadline) return fallback;
      }

      return fallback;
    }
  );

  return episodes.filter(Boolean);
}

async function resolveNongminMoviePlan(detailUrl, profiles) {
  let fallback = null;

  for (let i = 0; i < profiles.length; i++) {
    const profile = profiles[i];
    const track = profile && profile.group && profile.group.tracks && profile.group.tracks[0];
    if (!track || !track.url) continue;

    const plan = profile.plan || await resolveNongminTrackPlan(
      track.url,
      detailUrl,
      profile,
      true,
      NONGMIN_HLS_TIMEOUT_MS
    );
    if (!plan || !plan.url) continue;
    if (!fallback) fallback = plan;
    if (plan.verified) return plan;
  }

  return fallback;
}

async function resolveDirectUrl(rawUrl) {
  rawUrl = String(rawUrl || "").trim();

  if (!rawUrl || isBadHref(rawUrl)) return "";

  const cacheKey = makeCacheKey(["direct", rawUrl]);
  const cached = cacheGet(cacheKey);
  if (cached !== undefined) return cached;

  const normalizedDirect = normalizePlayUrl(rawUrl);
  if (normalizedDirect && /\.m3u8(?:[?#]|$)/i.test(normalizedDirect)) {
    return cacheSet(cacheKey, normalizedDirect);
  }

  const playerUrl = PLAY_API + encodeURIComponent(rawUrl);

  const res = await httpGet(playerUrl, {
    "User-Agent": UA,
    "Referer": SITE + "/",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "iframe"
  });

  const html = (res && res.data) || "";
  const directUrl = parsePlayerUrl(html);

  return directUrl ? cacheSet(cacheKey, directUrl) : "";
}

async function loadResource(params) {
  params = params || {};
  const rawSeries = String(params.seriesName || params.title || "").trim();
  const rawEpisodeName = String(params.episodeName || params.name || "").trim();
  const baseTitle = stripTitleMeta(rawSeries) || rawSeries || rawEpisodeName;

  if (!baseTitle) return [];

  console.log(
    "[nongmin-resource] start title=" + baseTitle +
    " type=" + String(params.type || "") +
    " keys=" + Object.keys(params).join(",")
  );

  try {
    const wantBaseNorm = normalizeName(baseTitle);
    const wantEpisode = getWantedEpisode(params);
    let results = await searchSite(baseTitle);

    if (!results.length && rawSeries && rawSeries !== baseTitle) {
      results = await searchSite(rawSeries);
    }

    console.log("[nongmin-resource] search-count=" + results.length);
    if (!results.length) return [];

    const best = pickBestResult(results, wantBaseNorm);
    if (!best || !best.url) return [];

    const playlist = await loadPlaylist(best.url);
    console.log("[nongmin-resource] group-count=" + (playlist ? playlist.length : 0));
    if (!playlist || !playlist.length) return [];

    const profiles = await buildNongminPlaybackProfiles(playlist, best.url);
    if (!profiles.length) return [];

    const maxTrackCount = profiles.reduce(function (count, profile) {
      return Math.max(count, profile.trackCount || 0);
    }, 0);
    const playlistLooksSeries = maxTrackCount > 1 || profiles.some(function (profile) {
      return looksLikeSeriesGroup(profile.group);
    });

    const resources = [];
    const seen = {};

    function addResource(name, description, plan) {
      if (!plan || !plan.url || seen[plan.url]) return;
      seen[plan.url] = true;
      resources.push({
        name: name,
        description: description,
        url: plan.url,
        playerType: plan.playerType || "system"
      });
    }

    if (!playlistLooksSeries) {
      for (let i = 0; i < profiles.length; i++) {
        const profile = profiles[i];
        const track = profile.group.tracks[0];
        const plan = profile.plan || await resolveNongminTrackPlan(
          track.url,
          best.url,
          profile,
          true,
          NONGMIN_HLS_TIMEOUT_MS
        );
        addResource(
          "农民影视 " + (profile.group.title || ("线路" + (i + 1))),
          [
            "匹配：" + best.rawTitle,
            "线路：" + (profile.group.title || "默认线路"),
            "画质：" + formatNongminQuality(plan),
            "引擎：" + nongminEngineLabel(plan)
          ].join("\n"),
          plan
        );
      }
    } else if (wantEpisode > 0) {
      for (let i = 0; i < profiles.length; i++) {
        const profile = profiles[i];
        const track = findNongminEpisodeTrack(profile, wantEpisode, Math.max(0, wantEpisode - 1));
        if (!track || !track.url) continue;
        const plan = await resolveNongminTrackPlan(
          track.url,
          best.url,
          profile,
          false,
          NONGMIN_EPISODE_TIMEOUT_MS
        );
        addResource(
          "农民影视 E" + pad2(wantEpisode) + " " + (profile.group.title || ("线路" + (i + 1))),
          [
            "匹配：" + best.rawTitle,
            "线路：" + (profile.group.title || "默认线路"),
            "集数：" + (track.name || ("E" + pad2(wantEpisode))),
            "画质：" + formatNongminQuality(plan),
            "引擎：" + nongminEngineLabel(plan)
          ].join("\n"),
          plan
        );
      }
    } else {
      const episodes = await resolveNongminSeriesEpisodes(best.url, profiles);
      for (let i = 0; i < episodes.length; i++) {
        const episode = episodes[i];
        const ep = toInt(episode.episodeNumber, i + 1);
        addResource(
          "农民影视 E" + pad2(ep) + " " + (episode.sourceName || "最佳线路"),
          [
            "匹配：" + best.rawTitle,
            "集数：" + (episode.title || ("E" + pad2(ep))),
            "线路：" + (episode.sourceName || "最佳线路"),
            "画质：" + (episode.quality || "未知"),
            "引擎：" + (episode.playerType === "ijk" ? "MDK" : "Auto")
          ].join("\n"),
          {
            url: episode.videoUrl,
            playerType: episode.playerType
          }
        );
      }
    }

    console.log("[nongmin-resource] direct-count=" + resources.length);
    return resources;
  } catch (error) {
    console.log("[nongmin-resource] error=" + String(error && error.message || error));
    return [];
  }
}
