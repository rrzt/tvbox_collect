function rouOption(title, value) {
  return { title: title, value: value || title };
}

var ROU_SORT_OPTIONS = [
  rouOption("最新发布", "createdAt"),
  rouOption("最多播放", "viewCount"),
  rouOption("最多点赞", "likeCount"),
  rouOption("最长时长", "duration"),
  rouOption("最近更新", "updatedAt")
];

var ROU_CNAV_OPTIONS = [
  rouOption("全部 国产AV", "國產AV"),
  rouOption("糖心Vlog"),
  rouOption("蜜桃影像傳媒"),
  rouOption("香蕉視頻傳媒"),
  rouOption("星空無限傳媒"),
  rouOption("天美傳媒"),
  rouOption("精東影業"),
  rouOption("杏吧傳媒"),
  rouOption("91製片廠"),
  rouOption("皇家華人"),
  rouOption("起點傳媒"),
  rouOption("大象傳媒"),
  rouOption("果凍傳媒"),
  rouOption("蘿莉社"),
  rouOption("ED Mosaic"),
  rouOption("兔子先生"),
  rouOption("扣扣傳媒"),
  rouOption("SA國際傳媒"),
  rouOption("愛神傳媒"),
  rouOption("性視界傳媒"),
  rouOption("PsychopornTW"),
  rouOption("拍攝花絮"),
  rouOption("抖陰"),
  rouOption("91茄子"),
  rouOption("絕對領域傳媒"),
  rouOption("烏托邦傳媒"),
  rouOption("紅斯燈影像"),
  rouOption("草莓視頻"),
  rouOption("渡邊傳媒"),
  rouOption("葫蘆影業"),
  rouOption("樂播傳媒"),
  rouOption("Pussy Hunter"),
  rouOption("麻麻傳媒"),
  rouOption("三只狼傳媒"),
  rouOption("萝莉原创"),
  rouOption("辣椒原創"),
  rouOption("MisAV"),
  rouOption("SWAG@daisybaby"),
  rouOption("冠希傳媒"),
  rouOption("微密圈傳媒"),
  rouOption("愛妃傳媒"),
  rouOption("天美影院"),
  rouOption("西瓜影視"),
  rouOption("肉肉傳媒"),
  rouOption("烏鴉傳媒"),
  rouOption("日出文化"),
  rouOption("鯨魚傳媒"),
  rouOption("國產AV劇情"),
  rouOption("SWAG@cartiernn"),
  rouOption("TWAV"),
  rouOption("Mini傳媒"),
  rouOption("桃花源"),
  rouOption("叮叮映畫"),
  rouOption("蜜桃視頻"),
  rouOption("O-STAR"),
  rouOption("開心鬼傳媒"),
  rouOption("葵心娛樂"),
  rouOption("愛污傳媒")
];

var ROU_MADOU_OPTIONS = [
  rouOption("全部 麻豆传媒", "麻豆傳媒"),
  rouOption("愛豆傳媒"),
  rouOption("MD"),
  rouOption("MDX"),
  rouOption("麻豆US"),
  rouOption("MSD"),
  rouOption("MCY"),
  rouOption("MKY"),
  rouOption("MPG"),
  rouOption("FLIXKO"),
  rouOption("貓爪影像"),
  rouOption("國產麻豆AV節目"),
  rouOption("麻豆女神微愛視頻"),
  rouOption("麻豆番外"),
  rouOption("麻豆三十天特別企劃"),
  rouOption("麻豆導演系列"),
  rouOption("情趣K歌房"),
  rouOption("MDWP"),
  rouOption("突襲女優家"),
  rouOption("麻豆女優"),
  rouOption("麻豆達人秀"),
  rouOption("澀會"),
  rouOption("MDS"),
  rouOption("MDSR"),
  rouOption("麻豆女神微愛影片"),
  rouOption("MDL"),
  rouOption("MAN"),
  rouOption("MSM"),
  rouOption("MDHT"),
  rouOption("MDAG"),
  rouOption("MS"),
  rouOption("MSG"),
  rouOption("MDJ"),
  rouOption("MDM"),
  rouOption("MXJ"),
  rouOption("MDD"),
  rouOption("MLT")
];

var ROU_ONLYFANS_OPTIONS = [
  rouOption("全部 OnlyFans", "OnlyFans"),
  rouOption("fansly"),
  rouOption("tangbo_hu"),
  rouOption("HongKongDoll"),
  rouOption("BunnyMiffy"),
  rouOption("Nana_Taipei"),
  rouOption("qiobnxingcai"),
  rouOption("suchanghub"),
  rouOption("ssrpeach"),
  rouOption("nicolove.cc"),
  rouOption("Miuzxc"),
  rouOption("kitty2002102"),
  rouOption("kittyxkum"),
  rouOption("yui_xin_tw"),
  rouOption("juneliu"),
  rouOption("YuZuKitty"),
  rouOption("jeenzen"),
  rouOption("monmon_tw"),
  rouOption("applecptv"),
  rouOption("andmlove"),
  rouOption("Loliiiiipop99"),
  rouOption("daintywilder"),
  rouOption("ZZZ666"),
  rouOption("aixiaixi"),
  rouOption("ChiChibae"),
  rouOption("blazeconjure3"),
  rouOption("moremore618"),
  rouOption("bdollairi"),
  rouOption("olive_emmm"),
  rouOption("chocoletmilkk"),
  rouOption("SLRabbit"),
  rouOption("Xreindeers"),
  rouOption("Carla Grace")
];

var ROU_TANHUA_OPTIONS = [
  rouOption("全部 探花", "探花"),
  rouOption("91沈先生"),
  rouOption("探花精選400"),
  rouOption("小寶尋花"),
  rouOption("91lisa"),
  rouOption("調教小景甜"),
  rouOption("午夜尋花"),
  rouOption("91鳳鳴鳥唱"),
  rouOption("大神精選"),
  rouOption("AVOVE直播"),
  rouOption("91貓先生"),
  rouOption("千人斬探花"),
  rouOption("全國探花"),
  rouOption("91Fans"),
  rouOption("七天探花"),
  rouOption("9總全國探花"),
  rouOption("91大神@LovELolita7"),
  rouOption("18歲母狗無限高潮"),
  rouOption("鴨哥探花"),
  rouOption("錘子探花"),
  rouOption("探花合集"),
  rouOption("91不見星空"),
  rouOption("早期東莞ISO桑拿系列"),
  rouOption("91康先生"),
  rouOption("肉オナホ"),
  rouOption("91大神唐伯虎"),
  rouOption("韋小寶"),
  rouOption("91風流哥全集"),
  rouOption("91蜜桃的合集"),
  rouOption("換妻探花"),
  rouOption("小陳頭星選"),
  rouOption("91大神括約肌大叔"),
  rouOption("情侶自拍"),
  rouOption("探花精選"),
  rouOption("91呆哥"),
  rouOption("mmmn753"),
  rouOption("楊導撩妹"),
  rouOption("歌廳探花陳先生"),
  rouOption("91美女涵菱"),
  rouOption("太子探花"),
  rouOption("小馬尋花"),
  rouOption("91唐哥"),
  rouOption("jimmybiiig"),
  rouOption("91天堂原創"),
  rouOption("小飛探花"),
  rouOption("王子哥專啪學生妹"),
  rouOption("文軒探花"),
  rouOption("偉哥尋歡"),
  rouOption("大草莓寶貝"),
  rouOption("探花女下海直播"),
  rouOption("91天堂系列"),
  rouOption("91大神胖Kyo"),
  rouOption("攝影師果哥出品"),
  rouOption("莞式選妃"),
  rouOption("catman"),
  rouOption("90w粉"),
  rouOption("探花大神"),
  rouOption("91原創達人@多乙丶"),
  rouOption("91大黃鴨"),
  rouOption("小東全國尋妹"),
  rouOption("91Dr哥"),
  rouOption("大熊探花"),
  rouOption("91約妹達人"),
  rouOption("91大神揚風"),
  rouOption("91愛絲小仙女思妍"),
  rouOption("探花郎李尋歡"),
  rouOption("91新晉大神sweattt"),
  rouOption("91新人GD超模（現改名69DD）"),
  rouOption("91大神jinx"),
  rouOption("91sex哥"),
  rouOption("175車模"),
  rouOption("東莞探花"),
  rouOption("嫖嫖sex探花"),
  rouOption("秀人網模特")
];

var ROU_SELFIE_OPTIONS = [
  rouOption("全部 自拍流出", "自拍流出"),
  rouOption("中國"),
  rouOption("台灣"),
  rouOption("twitter"),
  rouOption("主播"),
  rouOption("韓國"),
  rouOption("絲襪"),
  rouOption("多P"),
  rouOption("素人"),
  rouOption("偷拍"),
  rouOption("情侶自拍"),
  rouOption("91Fans"),
  rouOption("91天堂原創"),
  rouOption("大神精選"),
  rouOption("糖心Vlog")
];

var WidgetMetadata = {
  id: "rou_video",
  title: "肉视频",
  description: "rou.video 分类、排序、搜索与播放解析组件",
  author: "Evil",
  version: "1.2.5",
  site: "https://rou.video",
  icon: "https://rou.video/favicon.ico",
  modules: [
    // {
    //   id: "search",
    //   title: "站内搜索",
    //   type: "media_list",
    //   functionName: "searchVideos",
    //   cacheDuration: 300,
    //   timeoutSeconds: 30,
    //   params: [
    //     {
    //       name: "keyword",
    //       title: "搜索关键词",
    //       type: "input",
    //       description: "输入搜索关键词（标题、标签、演员/创作者等）",
    //       value: ""
    //     },
    //     { name: "page", title: "页码", type: "page", description: "页码", value: "1" }
    //   ]
    // },
    {
      id: "home_sections",
      title: "首页精选",
      type: "media_list",
      functionName: "loadSectionVideos",
      cacheDuration: 1800,
      timeoutSeconds: 30,
      params: [
        {
          name: "section",
          title: "分区",
          type: "enum",
          value: "latestVideos",
          enumOptions: [
            { title: "最新更新", value: "latestVideos" },
            { title: "热门 91", value: "hot91" },
            { title: "热门 自拍流出", value: "hotSelfie" },
            { title: "热门 国产AV视频", value: "hotCNAV" },
            { title: "日榜 91", value: "dailyHot91" },
            { title: "日榜 自拍流出", value: "dailyHotSelfie" },
            { title: "日榜 国产AV视频", value: "dailyHotCNAV" },
            { title: "日榜 OnlyFans", value: "dailyOnlyFans" },
            { title: "日榜 日本区", value: "dailyJV" }
          ]
        }
      ]
    },
    {
      id: "cnav",
      title: "国产AV",
      type: "media_list",
      functionName: "loadTagVideos",
      cacheDuration: 1800,
      timeoutSeconds: 30,
      params: [
        { name: "tag", title: "子模块", type: "enum", value: "國產AV", enumOptions: ROU_CNAV_OPTIONS },
        { name: "order", title: "排序", type: "enum", value: "createdAt", enumOptions: ROU_SORT_OPTIONS },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "madou",
      title: "麻豆传媒",
      type: "media_list",
      functionName: "loadTagVideos",
      cacheDuration: 1800,
      timeoutSeconds: 30,
      params: [
        { name: "tag", title: "子模块", type: "enum", value: "麻豆傳媒", enumOptions: ROU_MADOU_OPTIONS },
        { name: "order", title: "排序", type: "enum", value: "createdAt", enumOptions: ROU_SORT_OPTIONS },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "onlyfans",
      title: "OnlyFans",
      type: "media_list",
      functionName: "loadTagVideos",
      cacheDuration: 1800,
      timeoutSeconds: 30,
      params: [
        { name: "tag", title: "子模块", type: "enum", value: "OnlyFans", enumOptions: ROU_ONLYFANS_OPTIONS },
        { name: "order", title: "排序", type: "enum", value: "createdAt", enumOptions: ROU_SORT_OPTIONS },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "tanhua",
      title: "探花",
      type: "media_list",
      functionName: "loadTagVideos",
      cacheDuration: 1800,
      timeoutSeconds: 30,
      params: [
        { name: "tag", title: "子模块", type: "enum", value: "探花", enumOptions: ROU_TANHUA_OPTIONS },
        { name: "order", title: "排序", type: "enum", value: "createdAt", enumOptions: ROU_SORT_OPTIONS },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "selfie",
      title: "自拍流出",
      type: "media_list",
      functionName: "loadTagVideos",
      cacheDuration: 1800,
      timeoutSeconds: 30,
      params: [
        { name: "tag", title: "子模块", type: "enum", value: "自拍流出", enumOptions: ROU_SELFIE_OPTIONS },
        { name: "order", title: "排序", type: "enum", value: "createdAt", enumOptions: ROU_SORT_OPTIONS },
        { name: "page", title: "页码", type: "page", value: "1" }
      ]
    },
    {
      id: "loadResource",
      title: "肉视频播放源",
      description: "根据当前影片返回 MDK 标准化与 MPV 原始播放线路",
      functionName: "loadResource",
      type: "stream",
      cacheDuration: 0,
      timeoutSeconds: 45,
      retryCount: 0,
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
        description: "输入搜索关键词（标题、标签、演员/创作者等）",
        value: ""
      },
      { name: "page", title: "页码", type: "page", description: "页码", value: "1" }
    ]
  }
};

var ROU_SITE = "https://rou.video";
var ROU_IMAGE_PROXY = "https://external-content.duckduckgo.com/iu/";
var ROU_RESOURCE_LINKS = {};
var ROU_HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
  "Referer": ROU_SITE + "/"
};

function ensureArray(v) {
  return Array.isArray(v) ? v : [];
}

function text(v) {
  return String(v == null ? "" : v).replace(/\s+/g, " ").trim();
}

function stripRouLineSuffix(value) {
  return text(value).replace(/\s*·\s*(?:MDK\s*标准化线路|MPV\s*原始线路)\s*$/i, "").trim();
}

function normalizeRouMatchTitle(value) {
  return stripRouLineSuffix(value)
    .toLowerCase()
    .replace(/\s+/g, "")
    .replace(/[·•:：,，。!！?？"'“”‘’()（）\[\]【】{}<>《》_\-.\/\\|~～]/g, "");
}

function rouTitleHash(value) {
  value = String(value || "");
  var hash = 2166136261;
  for (var i = 0; i < value.length; i++) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul ? Math.imul(hash, 16777619) : ((hash * 16777619) | 0);
  }
  return (hash >>> 0).toString(16);
}

function rouResourceStorageKey(title) {
  var normalized = normalizeRouMatchTitle(title);
  return normalized ? ("rou.resource.link." + rouTitleHash(normalized) + "." + normalized.length) : "";
}

function rememberRouResourceLink(title, link) {
  var key = rouResourceStorageKey(title);
  link = text(link);
  if (!key || !/^https?:\/\//i.test(link)) return;

  ROU_RESOURCE_LINKS[key] = link;
  try {
    if (Widget.storage && typeof Widget.storage.set === "function") {
      Widget.storage.set(key, link);
    }
  } catch (e) {
    console.log("[rou.video] resource link cache write failed: " + (e && e.message ? e.message : e));
  }
}

function getRememberedRouResourceLink(title) {
  var key = rouResourceStorageKey(title);
  if (!key) return "";
  if (ROU_RESOURCE_LINKS[key]) return ROU_RESOURCE_LINKS[key];

  try {
    if (Widget.storage && typeof Widget.storage.get === "function") {
      var stored = text(Widget.storage.get(key, ""));
      if (/^https?:\/\//i.test(stored)) {
        ROU_RESOURCE_LINKS[key] = stored;
        return stored;
      }
    }
  } catch (e) {
    console.log("[rou.video] resource link cache read failed: " + (e && e.message ? e.message : e));
  }
  return "";
}

function utf8BytesToString(bytes) {
  var result = "";
  var i = 0;

  while (i < bytes.length) {
    var first = bytes[i++] & 255;
    var codePoint = first;

    if (first >= 240 && i + 2 < bytes.length) {
      codePoint = ((first & 7) << 18) |
        ((bytes[i++] & 63) << 12) |
        ((bytes[i++] & 63) << 6) |
        (bytes[i++] & 63);
    } else if (first >= 224 && i + 1 < bytes.length) {
      codePoint = ((first & 15) << 12) |
        ((bytes[i++] & 63) << 6) |
        (bytes[i++] & 63);
    } else if (first >= 192 && i < bytes.length) {
      codePoint = ((first & 31) << 6) | (bytes[i++] & 63);
    }

    if (codePoint > 65535) {
      codePoint -= 65536;
      result += String.fromCharCode(55296 + (codePoint >> 10));
      result += String.fromCharCode(56320 + (codePoint & 1023));
    } else {
      result += String.fromCharCode(codePoint);
    }
  }

  return result;
}

function responseBodyToString(data) {
  if (typeof data === "string") return data;
  if (data == null) return "";

  var bytes = null;
  if (Array.isArray(data)) {
    bytes = data;
  } else if (typeof Uint8Array !== "undefined" && data instanceof Uint8Array) {
    bytes = data;
  } else if (typeof ArrayBuffer !== "undefined" && data instanceof ArrayBuffer) {
    bytes = new Uint8Array(data);
  } else if (data && data.buffer && typeof Uint8Array !== "undefined") {
    try {
      bytes = new Uint8Array(data.buffer, data.byteOffset || 0, data.byteLength || data.length);
    } catch (e) {
      bytes = null;
    }
  }

  return bytes ? utf8BytesToString(bytes) : String(data);
}

function proxyCoverUrl(url) {
  url = absoluteUrl(url);
  if (!/^https?:\/\//i.test(url)) return url;
  if (url.indexOf(ROU_IMAGE_PROXY) === 0) return url;
  return ROU_IMAGE_PROXY + "?u=" + encodeURIComponent(url) + "&f=1&nofb=1";
}

function absoluteUrl(url) {
  url = text(url);
  if (!url) return "";
  if (url.indexOf("//") === 0) return "https:" + url;
  if (/^https?:\/\//i.test(url)) return url;
  if (url.charAt(0) === "/") return ROU_SITE + url;
  return ROU_SITE + "/" + url;
}

function formatDuration(seconds) {
  seconds = Number(seconds || 0);
  if (!isFinite(seconds) || seconds <= 0) return "";
  seconds = Math.round(seconds);
  var h = Math.floor(seconds / 3600);
  var m = Math.floor((seconds % 3600) / 60);
  var s = seconds % 60;
  function pad(n) { return n < 10 ? "0" + n : String(n); }
  return h > 0 ? (h + ":" + pad(m) + ":" + pad(s)) : (pad(m) + ":" + pad(s));
}

function formatCount(value) {
  var n = Number(value || 0);
  if (!isFinite(n) || n <= 0) return "";
  if (n >= 100000000) return (n / 100000000).toFixed(1).replace(/\.0$/, "") + "亿";
  if (n >= 10000) return (n / 10000).toFixed(1).replace(/\.0$/, "") + "万";
  return String(Math.round(n));
}

function createPlaceholderItem(message) {
  return {
    id: "placeholder",
    type: "placeholder",
    title: "提示",
    description: text(message || "暂无内容"),
    posterPath: "",
    backdropPath: "",
    mediaType: "movie",
    duration: 0,
    durationText: "",
    previewUrl: "",
    videoUrl: "",
    url: "",
    playUrl: "",
    link: "",
    playerType: "none"
  };
}

function base64ToBytes(input) {
  var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var clean = String(input || "").replace(/[^A-Za-z0-9+/=]/g, "");
  var bytes = [];
  var buffer = 0;
  var bits = 0;

  for (var i = 0; i < clean.length; i++) {
    var c = clean.charAt(i);
    if (c === "=") break;
    var value = chars.indexOf(c);
    if (value < 0) continue;
    buffer = (buffer << 6) | value;
    bits += 6;
    if (bits >= 8) {
      bits -= 8;
      bytes.push((buffer >> bits) & 255);
    }
  }

  return bytes;
}

function decodeRouVideoPayload(ev) {
  if (!ev || !ev.d) return {};
  var key = Number(ev.k || 0);
  var bytes = base64ToBytes(ev.d);
  var text = "";

  for (var i = 0; i < bytes.length; i++) {
    text += String.fromCharCode((bytes[i] - key + 256) & 255);
  }

  try {
    return JSON.parse(text);
  } catch (e) {
    return {};
  }
}

function extractNextData(html) {
  var match = String(html || "").match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/i);
  if (!match) return {};
  try {
    var raw = JSON.parse(match[1]);
    return (raw && raw.props && raw.props.pageProps) ? raw.props.pageProps : {};
  } catch (e) {
    return {};
  }
}

async function requestTextWithRetry(url, headers, timeout, validator, label, maxAttempts) {
  var lastError = null;
  var attempts = Math.max(1, parseInt(maxAttempts, 10) || 2);

  for (var attempt = 1; attempt <= attempts; attempt++) {
    try {
      var resp = await Widget.http.get(url, {
        headers: headers || {},
        allow_redirects: true,
        timeout: timeout
      });
      var status = Number(resp && resp.status || 0);
      var body = responseBodyToString(resp && resp.data);

      if (!resp || resp.ok === false || status >= 400) {
        throw new Error((label || "request") + " HTTP " + status);
      }
      if (!body || (validator && !validator(body))) {
        throw new Error((label || "request") + " response validation failed");
      }
      return body;
    } catch (e) {
      lastError = e;
      console.log("[rou.video] " + (label || "request") + " attempt " + attempt + " failed: " + (e && e.message ? e.message : e));
    }
  }

  throw lastError || new Error((label || "request") + " failed");
}

function fetchHtmlWithOptions(url, timeout, attempts, label) {
  return requestTextWithRetry(url, ROU_HEADERS, timeout || 8000, function (body) {
    return body.indexOf("__NEXT_DATA__") >= 0;
  }, label || "html", attempts || 2);
}

function fetchHtml(url) {
  return fetchHtmlWithOptions(url, 8000, 2, "html");
}

function getPlayHeaders(referer) {
  return {
    "User-Agent": ROU_HEADERS["User-Agent"],
    "Accept": "application/vnd.apple.mpegurl,application/x-mpegURL,video/*,*/*",
    "Referer": referer || ROU_SITE + "/",
    "Origin": ROU_SITE
  };
}

function normalizeRouVideoUrl(url) {
  url = text(url);
  if (!url) return "";
  return url.replace(/\/index\.jpg(?=([?#]|$))/i, "/index.m3u8");
}

function parseRouHlsAttributeList(attributeText) {
  var attributes = {};
  var source = String(attributeText || "");
  var token = "";
  var quoted = false;

  for (var i = 0; i <= source.length; i++) {
    var ch = i < source.length ? source.charAt(i) : ",";
    if (ch === '"' && source.charAt(i - 1) !== "\\") {
      quoted = !quoted;
      token += ch;
      continue;
    }
    if (ch === "," && !quoted) {
      var part = token.trim();
      token = "";
      if (!part) continue;
      var equalsIndex = part.indexOf("=");
      if (equalsIndex <= 0) continue;
      var key = part.slice(0, equalsIndex).trim().toUpperCase();
      var value = part.slice(equalsIndex + 1).trim();
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

function positiveRouNumber(value) {
  var result = parseInt(String(value || ""), 10);
  return isFinite(result) && result > 0 ? result : 0;
}

function parseRouHlsResolution(value, uri) {
  var width = 0;
  var height = 0;
  var declared = String(value || "").match(/(\d{2,5})\s*x\s*(\d{2,5})/i);
  if (declared) {
    width = positiveRouNumber(declared[1]);
    height = positiveRouNumber(declared[2]);
  }

  var pathText = String(uri || "");
  if (!width || !height) {
    var pathResolution = pathText.match(/(?:^|[\/_\-.])(\d{2,5})x(\d{2,5})(?:[\/_\-.]|$)/i);
    if (pathResolution) {
      width = positiveRouNumber(pathResolution[1]);
      height = positiveRouNumber(pathResolution[2]);
    }
  }
  if (!height) {
    var heightOnly = pathText.match(/(?:^|[\/_\-.])(\d{3,4})p(?:[\/_\-.]|$)/i);
    if (heightOnly) {
      height = positiveRouNumber(heightOnly[1]);
      width = height ? Math.round(height * 16 / 9) : 0;
    }
  }
  return { width: width, height: height, pixels: width && height ? width * height : 0 };
}

function resolveRouHlsUrl(uri, playlistUrl) {
  var value = text(uri);
  var base = text(playlistUrl);
  if (!value) return "";
  if (/^https?:\/\//i.test(value)) return normalizeRouVideoUrl(value);
  if (/^\/\//.test(value)) return normalizeRouVideoUrl("https:" + value);
  try {
    if (typeof URL !== "undefined") return normalizeRouVideoUrl(new URL(value, base).toString());
  } catch (e) {}

  var cleanBase = base.replace(/[?#].*$/, "");
  var originMatch = cleanBase.match(/^(https?:\/\/[^/]+)/i);
  if (value.charAt(0) === "/" && originMatch) return normalizeRouVideoUrl(originMatch[1] + value);
  var slashIndex = cleanBase.lastIndexOf("/");
  var directory = slashIndex >= 0 ? cleanBase.slice(0, slashIndex + 1) : cleanBase + "/";
  return normalizeRouVideoUrl(directory + value.replace(/^\.\//, ""));
}

function parseRouMasterVariants(masterText, playlistUrl) {
  var lines = String(masterText || "").split(/\r?\n/);
  var variants = [];
  for (var i = 0; i < lines.length; i++) {
    var line = String(lines[i] || "").trim();
    if (!/^#EXT-X-STREAM-INF\s*:/i.test(line)) continue;
    var attrs = parseRouHlsAttributeList(line.slice(line.indexOf(":") + 1));
    var uri = "";
    var uriIndex = i + 1;
    while (uriIndex < lines.length) {
      var candidate = String(lines[uriIndex] || "").trim();
      if (!candidate || candidate.charAt(0) === "#") {
        uriIndex++;
        continue;
      }
      uri = candidate;
      break;
    }
    if (!uri) continue;

    var resolution = parseRouHlsResolution(attrs.RESOLUTION, uri);
    var averageBandwidth = positiveRouNumber(attrs["AVERAGE-BANDWIDTH"]);
    var peakBandwidth = positiveRouNumber(attrs.BANDWIDTH);
    variants.push({
      url: resolveRouHlsUrl(uri, playlistUrl),
      uri: uri,
      codecs: String(attrs.CODECS || ""),
      resolution: String(attrs.RESOLUTION || ""),
      width: resolution.width,
      height: resolution.height,
      pixels: resolution.pixels,
      bandwidth: averageBandwidth || peakBandwidth,
      peakBandwidth: peakBandwidth,
      frameRate: parseFloat(String(attrs["FRAME-RATE"] || "0")) || 0,
      order: variants.length
    });
    i = uriIndex;
  }
  return variants;
}

function selectRouHighestQualityVariant(masterText, playlistUrl) {
  var variants = parseRouMasterVariants(masterText, playlistUrl);
  if (!variants.length) return null;
  variants.sort(function (left, right) {
    var fields = ["pixels", "height", "width", "bandwidth", "peakBandwidth", "frameRate", "order"];
    for (var i = 0; i < fields.length; i++) {
      var difference = Number(right[fields[i]] || 0) - Number(left[fields[i]] || 0);
      if (difference) return difference;
    }
    return 0;
  });
  return variants[0];
}

function classifyRouCodecString(codecs) {
  var value = String(codecs || "").toLowerCase();
  if (/(^|[,\s])(hvc1|hev1|hevc|h265|av01|av1|vp09|vp9|dvhe|dvh1)(?:\.|[,\s]|$)/i.test(value)) return "modern";
  if (/(^|[,\s])(avc1|avc3|h264)(?:\.|[,\s]|$)/i.test(value)) return "avc";
  return "unknown";
}

function firstRouMediaSegmentUrl(playlist, playlistUrl) {
  var lines = String(playlist || "").split(/\r?\n/);
  var expectSegment = false;
  for (var i = 0; i < lines.length; i++) {
    var line = String(lines[i] || "").trim();
    if (/^#EXTINF:/i.test(line)) {
      expectSegment = true;
      continue;
    }
    if (!line || line.charAt(0) === "#") continue;
    if (expectSegment) return resolveRouHlsUrl(line, playlistUrl);
    expectSegment = false;
  }
  return "";
}

function responseBodyToBytes(data) {
  if (data == null) return [];
  if (Array.isArray(data)) return data;
  if (typeof Uint8Array !== "undefined" && data instanceof Uint8Array) return data;
  if (typeof ArrayBuffer !== "undefined" && data instanceof ArrayBuffer) return new Uint8Array(data);
  if (data && data.buffer && typeof Uint8Array !== "undefined") {
    try {
      return new Uint8Array(data.buffer, data.byteOffset || 0, data.byteLength || data.length);
    } catch (e) {}
  }
  var source = String(data || "");
  var bytes = [];
  var limit = Math.min(source.length, 131072);
  for (var i = 0; i < limit; i++) bytes.push(source.charCodeAt(i) & 255);
  return bytes;
}

function inspectRouTsCodec(bytes) {
  bytes = responseBodyToBytes(bytes);
  var syncOffset = -1;
  for (var offset = 0; offset < 188 && offset + 376 < bytes.length; offset++) {
    if (bytes[offset] === 71 && bytes[offset + 188] === 71 && bytes[offset + 376] === 71) {
      syncOffset = offset;
      break;
    }
  }
  if (syncOffset < 0) return { family: "unknown", streamTypes: [] };

  var pmtPid = -1;
  var streamTypes = [];
  for (var packet = syncOffset; packet + 188 <= bytes.length; packet += 188) {
    if (bytes[packet] !== 71) continue;
    var payloadStart = (bytes[packet + 1] & 64) !== 0;
    var pid = ((bytes[packet + 1] & 31) << 8) | bytes[packet + 2];
    var adaptation = (bytes[packet + 3] >> 4) & 3;
    if (adaptation === 0 || adaptation === 2) continue;
    var cursor = packet + 4;
    if (adaptation === 3) cursor += 1 + bytes[cursor];
    if (cursor >= packet + 188) continue;
    if (payloadStart) cursor += 1 + bytes[cursor];
    if (cursor + 12 >= packet + 188) continue;

    if (pid === 0 && bytes[cursor] === 0) {
      var patLength = ((bytes[cursor + 1] & 15) << 8) | bytes[cursor + 2];
      var patEnd = Math.min(cursor + 3 + patLength - 4, packet + 188);
      for (var pat = cursor + 8; pat + 3 < patEnd; pat += 4) {
        var program = (bytes[pat] << 8) | bytes[pat + 1];
        if (program) {
          pmtPid = ((bytes[pat + 2] & 31) << 8) | bytes[pat + 3];
          break;
        }
      }
    } else if (pid === pmtPid && bytes[cursor] === 2) {
      var pmtLength = ((bytes[cursor + 1] & 15) << 8) | bytes[cursor + 2];
      var programInfoLength = ((bytes[cursor + 10] & 15) << 8) | bytes[cursor + 11];
      var pmtEnd = Math.min(cursor + 3 + pmtLength - 4, packet + 188);
      for (var stream = cursor + 12 + programInfoLength; stream + 4 < pmtEnd;) {
        var streamType = bytes[stream];
        var infoLength = ((bytes[stream + 3] & 15) << 8) | bytes[stream + 4];
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

async function probeRouSegmentCodec(segmentUrl, referer, timeout) {
  var headers = getPlayHeaders(referer);
  headers.Range = "bytes=0-65535";
  var response = await Widget.http.get(segmentUrl, {
    headers: headers,
    allow_redirects: true,
    timeout: Math.max(2000, Math.min(Number(timeout || 3500), 4500))
  });
  var status = Number(response && response.status || 0);
  if (!response || response.ok === false || status >= 400) throw new Error("segment probe HTTP " + status);
  return inspectRouTsCodec(response.data);
}
function stringToUtf8Bytes(input) {
  input = String(input || "");
  var bytes = [];

  for (var i = 0; i < input.length; i++) {
    var codePoint = input.charCodeAt(i);
    if (codePoint >= 55296 && codePoint <= 56319 && i + 1 < input.length) {
      var next = input.charCodeAt(i + 1);
      if (next >= 56320 && next <= 57343) {
        codePoint = 65536 + ((codePoint - 55296) << 10) + (next - 56320);
        i++;
      }
    }

    if (codePoint <= 127) {
      bytes.push(codePoint);
    } else if (codePoint <= 2047) {
      bytes.push(192 | (codePoint >> 6));
      bytes.push(128 | (codePoint & 63));
    } else if (codePoint <= 65535) {
      bytes.push(224 | (codePoint >> 12));
      bytes.push(128 | ((codePoint >> 6) & 63));
      bytes.push(128 | (codePoint & 63));
    } else {
      bytes.push(240 | (codePoint >> 18));
      bytes.push(128 | ((codePoint >> 12) & 63));
      bytes.push(128 | ((codePoint >> 6) & 63));
      bytes.push(128 | (codePoint & 63));
    }
  }

  return bytes;
}

function bytesToBase64(bytes) {
  var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var result = "";

  for (var i = 0; i < bytes.length; i += 3) {
    var a = bytes[i] & 255;
    var hasB = i + 1 < bytes.length;
    var hasC = i + 2 < bytes.length;
    var b = hasB ? (bytes[i + 1] & 255) : 0;
    var c = hasC ? (bytes[i + 2] & 255) : 0;
    var value = (a << 16) | (b << 8) | c;

    result += chars.charAt((value >> 18) & 63);
    result += chars.charAt((value >> 12) & 63);
    result += hasB ? chars.charAt((value >> 6) & 63) : "=";
    result += hasC ? chars.charAt(value & 63) : "=";
  }

  return result;
}

function rewriteRouPlaylistForMdk(playlist) {
  var lines = String(playlist || "").replace(/^\uFEFF/, "").replace(/\r\n/g, "\n").split("\n");
  var expectSegment = false;
  var rewritten = 0;
  for (var i = 0; i < lines.length; i++) {
    var trimmed = lines[i].trim();
    if (/^#EXTINF:/i.test(trimmed)) {
      expectSegment = true;
      continue;
    }
    if (!trimmed || trimmed.charAt(0) === "#") continue;
    if (expectSegment && /^https?:\/\//i.test(trimmed) && /\.jpg(?=([?#]|$))/i.test(trimmed)) {
      lines[i] = lines[i].replace(/\.jpg(?=([?#]|$))/i, ".ts");
      rewritten++;
    }
    expectSegment = false;
  }
  if (!/^\s*#EXTM3U/i.test(lines.join("\n")) || rewritten < 1) return null;
  return { body: lines.join("\n"), segmentCount: rewritten };
}

function createMdkPlaylistDataUrl(playlist) {
  var normalized = rewriteRouPlaylistForMdk(playlist);
  if (!normalized) return null;
  if (normalized.body.length > 800000) throw new Error("playlist is too large for inline transport");
  return {
    url: "data:application/vnd.apple.mpegurl;base64," + bytesToBase64(stringToUtf8Bytes(normalized.body)),
    segmentCount: normalized.segmentCount
  };
}

async function buildMdkPlaylistDataUrl(videoUrl, referer, timeout, attempts) {
  var playlist = await requestTextWithRetry(videoUrl, getPlayHeaders(referer), timeout || 6000, function (body) {
    return /^\s*#EXTM3U/i.test(body);
  }, "playlist", attempts || 2);
  var result = createMdkPlaylistDataUrl(playlist);
  if (!result) throw new Error("playlist has no disguised MPEG-TS segments");
  return result;
}

async function resolveRouPlaybackPlan(videoUrl, referer, timeout, attempts) {
  var originalUrl = normalizeRouVideoUrl(videoUrl);
  var playlistTimeout = Math.max(3000, Math.min(Number(timeout || 5000), 5500));
  var playlistAttempts = Math.max(1, Math.min(parseInt(attempts, 10) || 1, 2));
  var initialPlaylist = await requestTextWithRetry(originalUrl, getPlayHeaders(referer), playlistTimeout, function (body) {
    return /^\s*#EXTM3U/i.test(body);
  }, "playlist-inspection", playlistAttempts);
  var selected = selectRouHighestQualityVariant(initialPlaylist, originalUrl);
  var rawUrl = selected && selected.url ? selected.url : originalUrl;
  var mediaPlaylist = selected ? "" : initialPlaylist;

  if (selected) {
    try {
      mediaPlaylist = await requestTextWithRetry(rawUrl, getPlayHeaders(referer), playlistTimeout, function (body) {
        return /^\s*#EXTM3U/i.test(body) && !/#EXT-X-STREAM-INF/i.test(body);
      }, "selected-playlist", 1);
    } catch (selectedError) {
      console.log("[rou.video] selected playlist inspection failed: " + (selectedError && selectedError.message ? selectedError.message : selectedError));
    }
  }

  var codecFamily = classifyRouCodecString(selected && selected.codecs);
  var streamTypes = [];
  var segmentUrl = mediaPlaylist ? firstRouMediaSegmentUrl(mediaPlaylist, rawUrl) : "";
  if (codecFamily === "unknown" && segmentUrl) {
    try {
      var codecProbe = await probeRouSegmentCodec(segmentUrl, referer, Math.min(4000, playlistTimeout));
      codecFamily = codecProbe.family;
      streamTypes = codecProbe.streamTypes;
    } catch (probeError) {
      console.log("[rou.video] segment codec probe failed: " + (probeError && probeError.message ? probeError.message : probeError));
    }
  }

  var mdkPlaylist = codecFamily === "modern" || !mediaPlaylist ? null : createMdkPlaylistDataUrl(mediaPlaylist);
  var rawPlayerType = codecFamily === "avc" && mediaPlaylist && !mdkPlaylist ? "ijk" : "system";
  var resolution = selected && (selected.resolution || (selected.width && selected.height ? selected.width + "x" + selected.height : ""));
  console.log("[rou.video] selected quality=" + (resolution || "single") + " codec=" + codecFamily + " engine=" + (mdkPlaylist && codecFamily === "avc" ? "MDK" : rawPlayerType));
  return {
    rawUrl: rawUrl,
    rawPlayerType: rawPlayerType,
    codecFamily: codecFamily,
    codecs: selected ? selected.codecs : "",
    resolution: resolution || "",
    bandwidth: selected ? selected.bandwidth : 0,
    streamTypes: streamTypes,
    mdkPlaylist: mdkPlaylist
  };
}
function buildVideoItem(item) {
  item = item || {};
  var id = text(item.id || item.vid || item.nameZh || item.name);
  var title = text(item.nameZh || item.name || item.title || id);
  var cover = proxyCoverUrl(item.coverImageUrl || "");
  var tags = ensureArray(item.tagsZh && item.tagsZh.length ? item.tagsZh : item.tags);
  var durationText = formatDuration(item.duration);
  var detailUrl = item.id ? (ROU_SITE + "/v/" + encodeURIComponent(item.id)) : absoluteUrl(item.ref || "");
  var desc = [];

  if (item.vid) desc.push("编号: " + text(item.vid));
  if (durationText) desc.push("时长: " + durationText);
  if (item.viewCount != null) desc.push("播放: " + formatCount(item.viewCount));
  if (tags.length) desc.push("标签: " + tags.slice(0, 4).join(" / "));
  if (item.ref) desc.push("来源: " + text(item.ref));

  return {
    id: id || detailUrl || title,
    type: "movie",
    title: title || id || "肉视频",
    description: desc.join("\n"),
    posterPath: cover,
    backdropPath: cover,
    mediaType: "movie",
    duration: Math.round(Number(item.duration || 0)) || 0,
    durationText: durationText,
    previewUrl: "",
    videoUrl: "",
    url: "",
    playUrl: "",
    link: detailUrl,
    detailUrl: detailUrl,
    playerType: "none"
  };
}

function mapList(items) {
  return ensureArray(items).map(buildVideoItem);
}

async function loadHomeData() {
  var html = await fetchHtml(ROU_SITE + "/home");
  return extractNextData(html);
}

async function loadSectionVideos(params) {
  params = params || {};
  var section = text(params.section || "latestVideos");
  var data = await loadHomeData();
  var list = ensureArray(data[section]);

  if (!list.length) {
    return [createPlaceholderItem("未找到该分区内容")];
  }

  return mapList(list);
}

function buildTagUrl(tag, order, page) {
  tag = text(tag || "自拍流出");
  order = text(order || "createdAt");
  page = parseInt(page, 10) || 1;
  var url = ROU_SITE + "/t/" + encodeURIComponent(tag) + "?order=" + encodeURIComponent(order);
  url += "&page=" + encodeURIComponent(page);
  return url;
}

async function loadTagVideos(params) {
  params = params || {};
  var tag = text(params.tag || params.category || "自拍流出");
  var order = text(params.order || params.sort || "createdAt");
  var page = parseInt(params.page, 10) || 1;
  var html = await fetchHtml(buildTagUrl(tag, order, page));
  var data = extractNextData(html);
  var list = ensureArray(data.videos);

  if (!list.length) {
    return [createPlaceholderItem("未找到「" + tag + "」相关内容")];
  }

  return mapList(list);
}

async function searchVideos(params) {
  params = params || {};
  var keyword = text(params.keyword || params.query || params.q || "");
  var page = parseInt(params.page, 10) || 1;
  if (!keyword) return [createPlaceholderItem("请输入搜索关键词")];

  var url = ROU_SITE + "/search?q=" + encodeURIComponent(keyword) + "&t=&sort=&page=" + encodeURIComponent(page);

  var html = await fetchHtml(url);
  var data = extractNextData(html);
  var list = ensureArray(data.videos);

  if (!list.length) {
    return [createPlaceholderItem("未找到与「" + keyword + "」相关的内容")];
  }

  return mapList(list);
}

async function loadDetail(link) {
  try {
    var requestProfile = arguments.length > 1 && arguments[1] ? arguments[1] : {};
    var detailLink = link;
    if (detailLink && typeof detailLink === "object") {
      detailLink = detailLink.detailUrl || detailLink.link || detailLink.id || "";
    }
    detailLink = text(detailLink);
    if (!detailLink) return createPlaceholderItem("\u7f3a\u5c11\u8be6\u60c5\u94fe\u63a5");

    var html = await fetchHtmlWithOptions(
      detailLink,
      Number(requestProfile.htmlTimeout || 8000),
      Number(requestProfile.htmlAttempts || 2),
      "detail"
    );
    var data = extractNextData(html);
    var video = data.video || {};
    var item = buildVideoItem(video);
    rememberRouResourceLink(item.title, detailLink);
    var payload = decodeRouVideoPayload(data.ev);
    var videoUrl = normalizeRouVideoUrl(payload.videoUrl || "");
    if (!videoUrl) throw new Error("video URL not found");

    var detailBase = {
      id: item.id,
      type: "detail",
      title: item.title,
      description: item.description || "\u6682\u65e0\u7b80\u4ecb",
      posterPath: item.posterPath,
      backdropPath: item.backdropPath,
      mediaType: "movie",
      duration: item.duration,
      durationText: item.durationText,
      previewUrl: text(payload.thumbVTTUrl || ""),
      link: "",
      detailUrl: ""
    };

    try {
      var playback = await resolveRouPlaybackPlan(
        videoUrl,
        detailLink,
        Number(requestProfile.playlistTimeout || 6000),
        Number(requestProfile.playlistAttempts || 2)
      );
      videoUrl = playback.rawUrl || videoUrl;
      var playHeaders = getPlayHeaders(detailLink);
      var rawLine = Object.assign({}, detailBase, {
        id: item.id + ":raw",
        title: item.title,
        description: (item.description || "\u6682\u65e0\u7b80\u4ecb") + "\n\u7ebf\u8def: Auto/MPV \u539f\u59cb HLS",
        videoUrl: videoUrl,
        url: videoUrl,
        playUrl: videoUrl,
        playerType: playback.rawPlayerType || "system",
        customHeaders: playHeaders,
        headers: playHeaders
      });
      var mdkLine = playback.mdkPlaylist ? Object.assign({}, detailBase, {
        id: item.id + ":mdk",
        title: item.title,
        description: (item.description || "\u6682\u65e0\u7b80\u4ecb") + "\n\u7ebf\u8def: MDK \u6807\u51c6\u5316\uff08" + playback.mdkPlaylist.segmentCount + " \u4e2a TS \u5206\u7247\uff09",
        videoUrl: playback.mdkPlaylist.url,
        url: playback.mdkPlaylist.url,
        playUrl: playback.mdkPlaylist.url,
        playerType: "ijk",
        customHeaders: playHeaders,
        headers: playHeaders
      }) : null;

      if (mdkLine && playback.codecFamily === "avc") return [mdkLine, rawLine];
      if (mdkLine && playback.codecFamily === "unknown") return [rawLine, mdkLine];
      return [rawLine];
    } catch (playlistError) {
      console.log("[rou.video] playback inspection failed: " + (playlistError && playlistError.message ? playlistError.message : playlistError));
      var fallbackHeaders = getPlayHeaders(detailLink);
      return Object.assign({}, detailBase, {
        videoUrl: videoUrl,
        url: videoUrl,
        playUrl: videoUrl,
        playerType: "system",
        customHeaders: fallbackHeaders,
        headers: fallbackHeaders
      });
    }
  } catch (e) {
    console.error("[rou.video] loadDetail failed", e && e.message ? e.message : e);
    return {
      id: text(link) || "detail",
      type: "detail",
      title: "\u8089\u89c6\u9891",
      description: "\u8be6\u60c5\u9875\u89e3\u6790\u5931\u8d25",
      posterPath: "",
      backdropPath: "",
      mediaType: "movie",
      duration: 0,
      durationText: "",
      previewUrl: "",
      videoUrl: "",
      url: "",
      playUrl: "",
      playerType: "none",
      link: ""
    };
  }
}
function scoreRouResourceCandidate(item, targetTitle) {
  var candidate = normalizeRouMatchTitle(item && item.title);
  var target = normalizeRouMatchTitle(targetTitle);
  if (!candidate || !target) return 0;
  if (candidate === target) return 100000;
  if (candidate.indexOf(target) >= 0 || target.indexOf(candidate) >= 0) {
    return 50000 - Math.abs(candidate.length - target.length);
  }
  return 0;
}

async function findRouResourceItem(title) {
  title = stripRouLineSuffix(title);
  if (!title) return null;

  var remembered = getRememberedRouResourceLink(title);
  if (remembered) {
    return { title: title, link: remembered, detailUrl: remembered };
  }

  var url = ROU_SITE + "/search?q=" + encodeURIComponent(title) + "&t=&sort=&page=1";
  var html = await requestTextWithRetry(url, ROU_HEADERS, 6000, function (body) {
    return body.indexOf("__NEXT_DATA__") >= 0;
  }, "resource-search", 1);
  var data = extractNextData(html);
  var candidates = mapList(ensureArray(data.videos)).filter(function (item) {
    return item && item.link;
  });
  var best = null;
  var bestScore = 0;

  for (var i = 0; i < candidates.length; i++) {
    var score = scoreRouResourceCandidate(candidates[i], title);
    if (score > bestScore) {
      bestScore = score;
      best = candidates[i];
    }
  }

  if (bestScore >= 50000 && best) {
    rememberRouResourceLink(best.title || title, best.link);
    return best;
  }
  return null;
}

async function loadResource(params) {
  params = params || {};
  var rawTitle = params.seriesName || params.title || params.name || params.episodeName || "";
  var title = stripRouLineSuffix(rawTitle);
  if (!title) return [];

  try {
    var matched = await findRouResourceItem(title);
    if (!matched || !matched.link) return [];

    var detail = await loadDetail(matched.link, {
      htmlTimeout: 6000,
      htmlAttempts: 1,
      playlistTimeout: 5000,
      playlistAttempts: 2
    });
    var lines = Array.isArray(detail)
      ? detail
      : (detail && Array.isArray(detail.playSources) && detail.playSources.length
        ? detail.playSources
        : [detail]);
    var resources = [];

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i] || {};
      var url = String(line.videoUrl || line.url || "");
      if (!url) continue;
      var isMdk = /:mdk$/i.test(String(line.id || "")) || /MDK\s*标准化线路/i.test(String(line.title || ""));
      var name = isMdk ? "肉视频 MDK 标准化" : "肉视频 MPV 原始";
      resources.push({
        name: name,
        description: "匹配: " + (matched.title || title) + "\n线路: " + (isMdk ? "标准 TS 清单" : "原始伪装 HLS"),
        url: url
      });
    }

    return resources;
  } catch (e) {
    console.error("[rou.video] loadResource failed", e && e.message ? e.message : e);
    return [];
  }
}
