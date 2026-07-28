const fs = require("fs");
const axios = require("axios");

const ARRAY_FIELDS = ["sites", "lives", "flags", "parses", "rules", "ads"];

// ------------------------------
// 自动获取 Wex 最新 spider
// ------------------------------
async function getWexSpider() {
  try {
    const url = "https://9280.kstore.space/newwex.json";
    const res = await axios.get(url, { timeout: 10000 });
    if (res.data && res.data.spider) {
      console.log("🕷️ 已获取最新 Wex spider:", res.data.spider);
      return res.data.spider;
    }
  } catch (e) {
    console.error("❌ 获取 Wex spider 失败:", e);
  }
  return null;
}

// ------------------------------
// 自动获取 Fish 最新 spider
// ------------------------------
async function getFishSpider() {
  try {
    const url = "https://6800.kstore.vip/fish.json";
    const res = await axios.get(url, { timeout: 10000 });

    // 兼容服务器返回 JSON 对象或 JSON 字符串
    const data =
      typeof res.data === "string"
        ? JSON.parse(res.data)
        : res.data;

    if (data && data.spider) {
      console.log("🐟 已获取最新 Fish spider:", data.spider);
      return data.spider;
    }

    console.error("❌ Fish 配置中未找到 spider 字段");
  } catch (e) {
    console.error("❌ 获取 Fish spider 失败:", e.message || e);
  }

  return null;
}

// ------------------------------
//  合并数组逻辑（保持原样）
// ------------------------------
function mergeArrays(apiArr, editedArr, keyName) {
  if (!Array.isArray(editedArr)) return apiArr;

  const editedMap = new Map();
  for (const item of editedArr) {
    if (!item || !item[keyName]) continue;
    editedMap.set(item[keyName], item);
  }

  const result = [];

  for (const apiItem of apiArr) {
    const k = apiItem[keyName];
    const editedItem = editedMap.get(k);

    if (!editedItem) {
      result.push(apiItem);
      continue;
    }

    if (editedItem.delete === true) continue;

    const { delete: _del, ...pure } = editedItem;
    result.push(pure);
    editedMap.delete(k);
  }

  for (const [_, item] of editedMap) {
    if (item.delete === true) continue;
    const { delete: _del, ...pure } = item;
    result.push(pure);
  }

  return result;
}

// ------------------------------
// 深度合并
// ------------------------------
function deepMerge(api, edited) {
  const result = JSON.parse(JSON.stringify(api));

  for (const key in edited) {
    const value = edited[key];

    if (ARRAY_FIELDS.includes(key) && Array.isArray(value)) {
      const keyName = key === "sites" ? "key" : "name";
      result[key] = mergeArrays(api[key] || [], value, keyName);
      continue;
    }

    if (typeof value === "object" && value !== null && !Array.isArray(value)) {
      result[key] = deepMerge(api[key] || {}, value);
      continue;
    }

    result[key] = value;
  }

  return result;
}

// ------------------------------
// 主流程
// ------------------------------
(async () => {
  try {
    const api = JSON.parse(fs.readFileSync("天神IY.txt", "utf8"));
    const edited = JSON.parse(fs.readFileSync("edited.json", "utf8"));

    // 先合并
    const merged = deepMerge(api, edited);

    // 同时获取最新 Wex 和 Fish spider
const [wexSpider, fishSpider] = await Promise.all([
  getWexSpider(),
  getFishSpider()
]);

    // ------------------------------
    // 为指定站点注入对应 jar/ext
    // ------------------------------

if (merged.sites && Array.isArray(merged.sites)) {
  merged.sites = merged.sites.map(site => {
    // 为 csp_SportKaFeiGuard 注入 Wex spider
    if (site.api === "csp_SportKaFeiGuard" && wexSpider) {
      console.log(`✨ 为 ${site.key} 注入最新 Wex spider`);

      return {
        ...site,
        jar: wexSpider,
        ext: "https://9280.kstore.space/newwex.json"
      };
    }

    // 为 csp_ALLLive 和 csp_FishConfig 注入 Fish spider
if (
  (site.api === "csp_ALLLive" || site.api === "csp_FishConfig") &&
  fishSpider
) {
  console.log(`🐟 为 ${site.key}（${site.api}）注入最新 Fish spider`);

  return {
    ...site,
    jar: fishSpider,
    ext: "https://6800.kstore.vip/fish.json"
  };
}

return site;

  });
}

    // 写入最终接口
    fs.writeFileSync("iy_merged.json", JSON.stringify(merged, null, 2), "utf8");

    console.log("🎉 合并完成：已为指定站点注入spider");

  } catch (e) {
    console.error("❌ 合并失败");
    console.error(e);
    process.exit(1);
  }
})();
