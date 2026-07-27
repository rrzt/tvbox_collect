var WidgetMetadata = {
  id: "jable_capyplayer",
  title: "Jable",
  description: "Jable CapyPlayer 规范版，支持热门、最新、中文字幕、女优、玩法、剧情、搜索与播放解析。",
  author: "Minis",
  version: "3.0.3",
  site: "https://jable.tv",
  icon: "https://jable.tv/favicon.ico",
  modules: [
    {
      id: "hot",
      title: "热门",
      type: "media_list",
      functionName: "loadPage",
      cacheDuration: 3600,
      timeoutSeconds: 30,
      params: [
        {
          name: "url",
          title: "列表地址",
          type: "constant",
          value: "https://jable.tv/hot/?mode=async&function=get_block&block_id=list_videos_common_videos_list"
        },
        {
          name: "sort_by",
          title: "排序",
          type: "enum",
          value: "video_viewed_today",
          enumOptions: [
            { title: "今日热门", value: "video_viewed_today" },
            { title: "本周热门", value: "video_viewed_week" },
            { title: "本月热门", value: "video_viewed_month" },
            { title: "所有时间", value: "video_viewed" }
          ]
        },
        { name: "from", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "latest",
      title: "最新",
      type: "media_list",
      functionName: "loadPage",
      cacheDuration: 3600,
      timeoutSeconds: 30,
      params: [
        {
          name: "url",
          title: "列表地址",
          type: "constant",
          value: "https://jable.tv/new-release/?mode=async&function=get_block&block_id=list_videos_common_videos_list"
        },
        {
          name: "sort_by",
          title: "排序",
          type: "enum",
          value: "latest-updates",
          enumOptions: [
            { title: "最新发布", value: "latest-updates" },
            { title: "最多观看", value: "video_viewed" },
            { title: "最多收藏", value: "most_favourited" }
          ]
        },
        { name: "from", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "subtitle",
      title: "中文",
      type: "media_list",
      functionName: "loadPage",
      cacheDuration: 3600,
      timeoutSeconds: 30,
      params: [
        {
          name: "url",
          title: "列表地址",
          type: "constant",
          value: "https://jable.tv/categories/chinese-subtitle/?mode=async&function=get_block&block_id=list_videos_common_videos_list"
        },
        {
          name: "sort_by",
          title: "排序",
          type: "enum",
          value: "post_date",
          enumOptions: [
            { title: "最近更新", value: "post_date" },
            { title: "最多观看", value: "video_viewed" },
            { title: "最多收藏", value: "most_favourited" }
          ]
        },
        { name: "from", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "actress",
      title: "女优",
      type: "media_list",
      functionName: "loadPage",
      cacheDuration: 3600,
      timeoutSeconds: 30,
      params: [
        {
          name: "url",
          title: "选择女优",
          type: "enum",
          value: "https://jable.tv/s1/models/yua-mikami/?mode=async&function=get_block&block_id=list_videos_common_videos_list",
          enumOptions: [
            { title: "三上悠亚", value: "https://jable.tv/s1/models/yua-mikami/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "枫可怜", value: "https://jable.tv/models/86b2f23f95cc485af79fe847c5b9de8d/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "小野夕子", value: "https://jable.tv/models/2958338aa4f78c0afb071e2b8a6b5f1b/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "大槻响", value: "https://jable.tv/models/hibiki-otsuki/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "藤森里穗", value: "https://jable.tv/models/riho-fujimori/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "JULIA", value: "https://jable.tv/models/julia/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "明里紬", value: "https://jable.tv/models/tsumugi-akari/?mode=async&function=get_block&block_id=list_videos_common_videos_list" },
            { title: "桃乃木香奈", value: "https://jable.tv/models/momonogi-kana/?mode=async&function=get_block&block_id=list_videos_common_videos_list" }
          ]
        },
        {
          name: "sort_by",
          title: "排序",
          type: "enum",
          value: "post_date",
          enumOptions: [
            { title: "最近更新", value: "post_date" },
            { title: "最多观看", value: "video_viewed" },
            { title: "最多收藏", value: "most_favourited" }
          ]
        },
        { name: "from", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "playstyle",
      title: "玩法",
      type: "media_list",
      functionName: "loadTagPage",
      cacheDuration: 3600,
      timeoutSeconds: 30,
      params: [
        {
          name: "url",
          title: "玩法标签",
          type: "enum",
          value: "https://jable.tv/tags/outdoor/",
          enumOptions: [
            { title: "露出", value: "https://jable.tv/tags/outdoor/" },
            { title: "集團進犯", value: "https://jable.tv/tags/gang-intrusion/" },
            { title: "進犯", value: "https://jable.tv/tags/intrusion/" },
            { title: "調教", value: "https://jable.tv/tags/tune/" },
            { title: "綑綁", value: "https://jable.tv/tags/bondage/" },
            { title: "瞬間插入", value: "https://jable.tv/tags/quickie/" },
            { title: "痴漢", value: "https://jable.tv/tags/chikan/" },
            { title: "痴女", value: "https://jable.tv/tags/chizyo/" },
            { title: "男M", value: "https://jable.tv/tags/masochism-guy/" },
            { title: "泥醉", value: "https://jable.tv/tags/crapulence/" },
            { title: "泡姬", value: "https://jable.tv/tags/soapland/" },
            { title: "母乳", value: "https://jable.tv/tags/breast-milk/" },
            { title: "放尿", value: "https://jable.tv/tags/piss/" },
            { title: "按摩", value: "https://jable.tv/tags/massage/" },
            { title: "多P", value: "https://jable.tv/tags/groupsex/" },
            { title: "刑具", value: "https://jable.tv/tags/grip/" },
            { title: "凌辱", value: "https://jable.tv/tags/insult/" },
            { title: "一日十回", value: "https://jable.tv/tags/10-times-a-day/" },
            { title: "3P", value: "https://jable.tv/tags/3p/" }
          ]
        },
        {
          name: "sort_by",
          title: "排序",
          type: "enum",
          value: "post_date",
          enumOptions: [
            { title: "最近更新", value: "post_date" },
            { title: "最多观看", value: "video_viewed" },
            { title: "最多收藏", value: "most_favourited" }
          ]
        },
        { name: "from", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "story",
      title: "劇情",
      type: "media_list",
      functionName: "loadTagPage",
      cacheDuration: 3600,
      timeoutSeconds: 30,
      params: [
        {
          name: "url",
          title: "劇情标签",
          type: "enum",
          value: "https://jable.tv/tags/black/",
          enumOptions: [
            { title: "黑人", value: "https://jable.tv/tags/black/" },
            { title: "醜男", value: "https://jable.tv/tags/ugly-man/" },
            { title: "誘惑", value: "https://jable.tv/tags/temptation/" },
            { title: "親屬", value: "https://jable.tv/tags/kinship/" },
            { title: "童貞", value: "https://jable.tv/tags/virginity/" },
            { title: "時間停止", value: "https://jable.tv/tags/time-stop/" },
            { title: "復仇", value: "https://jable.tv/tags/avenge/" },
            { title: "年齡差", value: "https://jable.tv/tags/age-difference/" },
            { title: "巨漢", value: "https://jable.tv/tags/giant/" },
            { title: "媚藥", value: "https://jable.tv/tags/love-potion/" },
            { title: "夫目前犯", value: "https://jable.tv/tags/sex-beside-husband/" },
            { title: "出軌", value: "https://jable.tv/tags/affair/" },
            { title: "催眠", value: "https://jable.tv/tags/hypnosis/" },
            { title: "偷拍", value: "https://jable.tv/tags/private-cam/" },
            { title: "下雨天", value: "https://jable.tv/tags/rainy-day/" },
            { title: "NTR", value: "https://jable.tv/tags/ntr/" },
            { title: "風俗娘", value: "https://jable.tv/tags/club-hostess-and-sex-worker/" },
            { title: "醫生", value: "https://jable.tv/tags/doctor/" },
            { title: "逃犯", value: "https://jable.tv/tags/fugitive/" },
            { title: "護士", value: "https://jable.tv/tags/nurse/" },
            { title: "老師", value: "https://jable.tv/tags/teacher/" },
            { title: "空姐", value: "https://jable.tv/tags/flight-attendant/" },
            { title: "球隊經理", value: "https://jable.tv/tags/team-manager/" },
            { title: "未亡人", value: "https://jable.tv/tags/widow/" },
            { title: "搜查官", value: "https://jable.tv/tags/detective/" },
            { title: "情侶", value: "https://jable.tv/tags/couple/" },
            { title: "家政婦", value: "https://jable.tv/tags/housewife/" },
            { title: "家庭教師", value: "https://jable.tv/tags/private-teacher/" },
            { title: "偶像", value: "https://jable.tv/tags/idol/" },
            { title: "人妻", value: "https://jable.tv/tags/wife/" },
            { title: "主播", value: "https://jable.tv/tags/female-anchor/" },
            { title: "OL", value: "https://jable.tv/tags/ol/" },
            { title: "魔鏡號", value: "https://jable.tv/tags/magic-mirror/" },
            { title: "電車", value: "https://jable.tv/tags/tram/" },
            { title: "處女", value: "https://jable.tv/tags/first-night/" },
            { title: "監獄", value: "https://jable.tv/tags/prison/" },
            { title: "溫泉", value: "https://jable.tv/tags/hot-spring/" },
            { title: "洗浴場", value: "https://jable.tv/tags/bathing-place/" },
            { title: "泳池", value: "https://jable.tv/tags/swimming-pool/" },
            { title: "汽車", value: "https://jable.tv/tags/car/" },
            { title: "廁所", value: "https://jable.tv/tags/toilet/" },
            { title: "學校", value: "https://jable.tv/tags/school/" },
            { title: "圖書館", value: "https://jable.tv/tags/library/" },
            { title: "健身房", value: "https://jable.tv/tags/gym-room/" },
            { title: "便利店", value: "https://jable.tv/tags/store/" },
            { title: "錄像", value: "https://jable.tv/tags/video-recording/" },
            { title: "處女作/引退作", value: "https://jable.tv/tags/debut-retires/" },
            { title: "綜藝", value: "https://jable.tv/tags/variety-show/" },
            { title: "節日主題", value: "https://jable.tv/tags/festival/" },
            { title: "感謝祭", value: "https://jable.tv/tags/thanksgiving/" },
            { title: "4小時以上", value: "https://jable.tv/tags/more-than-4-hours/" }
          ]
        },
        {
          name: "sort_by",
          title: "排序",
          type: "enum",
          value: "post_date",
          enumOptions: [
            { title: "最近更新", value: "post_date" },
            { title: "最多观看", value: "video_viewed" },
            { title: "最多收藏", value: "most_favourited" }
          ]
        },
        { name: "from", title: "页码", type: "page", value: "1" }
      ]
    },
    // {
    //   id: "search_module",
    //   title: "网站搜索",
    //   type: "media_list",
    //   functionName: "searchVideos",
    //   cacheDuration: 300,
    //   timeoutSeconds: 30,
    //   params: [
    //     { name: "keyword", title: "关键词", type: "string", value: "" },
    //     {
    //       name: "sort_by",
    //       title: "排序",
    //       type: "enum",
    //       value: "post_date",
    //       enumOptions: [
    //         { title: "最多观看", value: "video_viewed" },
    //         { title: "近期最佳", value: "post_date_and_popularity" },
    //         { title: "最近更新", value: "post_date" },
    //         { title: "最多收藏", value: "most_favourited" }
    //       ]
    //     },
    //     { name: "from", title: "页码", type: "page", value: "1" }
    //   ]
    // }
  ],
  search: {
    title: "搜索",
    functionName: "searchVideos",
    params: [
      { name: "keyword", title: "关键词", type: "string", value: "" },
      { name: "page", title: "页码", type: "page", value: "1" }
    ]
  }
};

var JABLE_HEADERS = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  "Referer": "https://jable.tv/"
};

function ensureArray(v) {
  return Array.isArray(v) ? v : [];
}

function safeText(v) {
  return String(v || "").replace(/\s+/g, " ").trim();
}

function absoluteUrl(url) {
  if (!url) return "";
  if (url.indexOf("http://") === 0 || url.indexOf("https://") === 0) return url;
  return new URL(url, "https://jable.tv").toString();
}

async function fetchHtmlByBrowser(url) {
  if (typeof fetch !== "function") return "";

  try {
    var response = await fetch(url, {
      method: "GET",
      credentials: "include",
      cache: "no-store"
    });
    if (!response || !response.ok) return "";
    return await response.text();
  } catch (e) {
    return "";
  }
}

async function fetchHtml(url) {
  var browserHtml = await fetchHtmlByBrowser(url);
  if (browserHtml) return browserHtml;

  var response = await Widget.http.get(url, { headers: JABLE_HEADERS, timeout: 30000 });
  return String(response.data || "");
}

function mapJableItem(item) {
  return {
    id: String(item.id || item.link || item.title),
    title: safeText(item.title || ""),
    posterUrl: absoluteUrl(item.cover || ""),
    backdropUrl: absoluteUrl(item.cover || ""),
    description: item.duration ? ("时长: " + item.duration) : "",
    mediaType: "movie",
    link: absoluteUrl(item.link || "")
  };
}

function parseJableList(htmlContent) {
  var docId = Widget.dom.parse(htmlContent);
  try {
    var itemNodes = Widget.dom.select(docId, ".video-img-box");
    var results = [];
    var seen = {};

    for (var i = 0; i < itemNodes.length; i++) {
      var node = itemNodes[i];
      var linkNode = Widget.dom.select(node, ".title a")[0];
      if (!linkNode) continue;
      var href = absoluteUrl((linkNode.attributes && linkNode.attributes.href) || "");
      if (!href || seen[href]) continue;
      seen[href] = true;

      var imgNode = Widget.dom.select(node, "img")[0];
      var durationNode = Widget.dom.select(node, ".absolute-bottom-right .label")[0];
      results.push(mapJableItem({
        id: href,
        title: linkNode.text || "",
        link: href,
        cover: imgNode ? ((imgNode.attributes && (imgNode.attributes["data-src"] || imgNode.attributes.src || imgNode.attributes["data-original"])) || "") : "",
        duration: durationNode ? (durationNode.text || "") : ""
      }));
    }

    return results;
  } finally {
    Widget.dom.remove(docId);
  }
}

async function loadPage(params) {
  params = params || {};
  var url = String(params.url || "");
  if (!url) return [];
  if (params.sort_by) url += "&sort_by=" + encodeURIComponent(params.sort_by);
  if (params.from) url += "&from=" + encodeURIComponent(params.from);
  try {
    var html = await fetchHtml(url);
    return ensureArray(parseJableList(html));
  } catch (e) {
    console.error("jable loadPage error", e && e.message ? e.message : e);
    return [];
  }
}

async function loadTagPage(params) {
  params = params || {};
  var url = String(params.url || "");
  if (!url) return [];
  if (params.sort_by) {
    if (url.indexOf("?") >= 0) url += "&sort_by=" + encodeURIComponent(params.sort_by);
    else url += "?sort_by=" + encodeURIComponent(params.sort_by);
  }
  if (params.from && String(params.from) !== "1") {
    if (url.indexOf("?") >= 0) url += "&from=" + encodeURIComponent(params.from);
    else url += "?from=" + encodeURIComponent(params.from);
  }
  try {
    var html = await fetchHtml(url);
    return ensureArray(parseJableList(html));
  } catch (e) {
    console.error("jable loadTagPage error", e && e.message ? e.message : e);
    return [];
  }
}

async function searchVideos(params) {
  params = params || {};
  var keyword = encodeURIComponent(params.keyword || "");
  if (!keyword) return [];
  var url = "https://jable.tv/search/" + keyword + "/?mode=async&function=get_block&block_id=list_videos_videos_list_search_result&q=" + keyword;
  if (params.sort_by) url += "&sort_by=" + encodeURIComponent(params.sort_by);
  if (params.from) url += "&from=" + encodeURIComponent(params.from);
  try {
    var html = await fetchHtml(url);
    return ensureArray(parseJableList(html));
  } catch (e) {
    console.error("jable searchVideos error", e && e.message ? e.message : e);
    return [];
  }
}

async function loadDetail(link) {
  try {
    var html = await fetchHtmlByBrowser(link);
    if (!html) {
      var response = await Widget.http.get(link, { headers: JABLE_HEADERS, timeout: 30000 });
      html = String(response.data || "");
    }
    var hlsUrl = "";

    var key = "var hlsUrl = '";
    var idx = html.indexOf(key);
    if (idx >= 0) {
      var start = idx + key.length;
      var end = html.indexOf("'", start);
      if (end > start) hlsUrl = html.slice(start, end);
    }

    if (!hlsUrl) {
      key = 'var hlsUrl = "';
      idx = html.indexOf(key);
      if (idx >= 0) {
        start = idx + key.length;
        end = html.indexOf('"', start);
        if (end > start) hlsUrl = html.slice(start, end);
      }
    }

    if (!hlsUrl) {
      var marker = '.m3u8';
      var m3u8Index = html.indexOf(marker);
      if (m3u8Index > 0) {
        var begin = html.lastIndexOf('https://', m3u8Index);
        if (begin < 0) begin = html.lastIndexOf('http://', m3u8Index);
        if (begin >= 0) hlsUrl = html.slice(begin, m3u8Index + marker.length);
      }
    }

    if (!hlsUrl) {
      var sourceKey = '<source';
      var sourceIdx = html.indexOf(sourceKey);
      while (sourceIdx >= 0) {
        var srcIdx = html.indexOf('src="', sourceIdx);
        if (srcIdx < 0) srcIdx = html.indexOf("src='", sourceIdx);
        if (srcIdx >= 0) {
          var quote = html[srcIdx + 4];
          var srcStart = srcIdx + 5;
          var srcEnd = html.indexOf(quote, srcStart);
          var candidate = srcEnd > srcStart ? html.slice(srcStart, srcEnd) : '';
          if (candidate.indexOf('.m3u8') >= 0) {
            hlsUrl = candidate;
            break;
          }
        }
        sourceIdx = html.indexOf(sourceKey, sourceIdx + sourceKey.length);
      }
    }

    if (!hlsUrl) {
      return { title: "无法获取有效的播放地址" };
    }

    hlsUrl = hlsUrl.split('\\/').join('/');

    var docId = Widget.dom.parse(html);
    try {
      var title = "";
      var metaTitle = Widget.dom.select(docId, 'meta[property="og:title"]')[0];
      if (metaTitle && metaTitle.attributes && metaTitle.attributes.content) title = metaTitle.attributes.content;
      if (!title) {
        var titleNode = Widget.dom.select(docId, "title")[0];
        title = titleNode ? safeText(titleNode.text) : "Jable";
      }
      var poster = "";
      var metaImage = Widget.dom.select(docId, 'meta[property="og:image"]')[0];
      if (metaImage && metaImage.attributes && metaImage.attributes.content) poster = absoluteUrl(metaImage.attributes.content);
      return {
        title: title || "Jable",
        posterUrl: poster,
        backdropUrl: poster,
        videoUrl: hlsUrl,
        playerType: "ijk",
        headers: {
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
          "Referer": link,
          "Origin": "https://jable.tv"
        },
        customHeaders: {
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
          "Referer": link,
          "Origin": "https://jable.tv"
        }
      };
    } finally {
      Widget.dom.remove(docId);
    }
  } catch (e) {
    console.error("jable loadDetail error", e && e.message ? e.message : e);
    return { title: "请求错误" };
  }
}
