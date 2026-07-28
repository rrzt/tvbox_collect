const fs = require("fs");
const path = require("path");

// 去除注释和 BOM
function removeComments(str) {
  str = str.replace(/\/\*[\s\S]*?\*\//g, "");
  str = str.replace(/(^|[^:])\/\/.*$/gm, "$1");
  return str;
}
function removeBOM(str) {
  return str.charCodeAt(0) === 0xFEFF ? str.slice(1) : str;
}

/**
 * ⭐【改动 1】：优先识别 ZIP 解压后的固定目录 “缘起【天神IY】”
 * ⭐【改动 2】：如果不存在，则寻找唯一的非隐藏目录
 */
function findExtractedFolder() {
  const EXPECTED = "缘起【天神IY】";

  // 优先使用固定目录名
  if (fs.existsSync(EXPECTED) && fs.statSync(EXPECTED).isDirectory()) {
    return EXPECTED;
  }

  // fallback：寻找唯一的非隐藏目录
  const dirs = fs.readdirSync(".").filter(d =>
    fs.statSync(d).isDirectory() && !d.startsWith(".")
  );

  if (dirs.length === 1) {
    return dirs[0];
  }

  return null;
}

/**
 * ⭐【改动 3】：递归查找 api.json（保持不变）
 */
function findApiJson(dir) {
  const entries = fs.readdirSync(dir);
  for (const e of entries) {
    const full = path.join(dir, e);
    const stat = fs.statSync(full);

    if (stat.isDirectory()) {
      const found = findApiJson(full);
      if (found) return found;
    } else if (e === "api.json") {
      return full;
    }
  }
  return null;
}

// 修复相对路径
function fixPaths(obj) {
  if (typeof obj === "string") {
    if (obj.startsWith("./")) {
      return `https://gh-proxy.com/https://raw.githubusercontent.com/IY-CPU/IY/main/${obj.slice(2)}`;
    }
    if (obj.startsWith("../")) {
      return `https://gh-proxy.com/https://raw.githubusercontent.com/IY-CPU/IY/main/lib/${obj.slice(3)}`;
    }
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map(fixPaths);
  }
  if (typeof obj === "object" && obj !== null) {
    const res = {};
    for (const [k, v] of Object.entries(obj)) {
      res[k] = fixPaths(v);
    }
    return res;
  }
  return obj;
}

try {
  // 1) 自动识别解压文件夹
  const root = findExtractedFolder();
  if (!root) {
    console.error("❌ 未找到解压后的文件夹（未检测到“缘起【天神IY】”）");
    process.exit(1);
  }
  console.log("📁 解压目录:", root);

  // 2) 查找 api.json
  const apiPath = findApiJson(root);
  if (!apiPath) {
    console.error("❌ 未找到 api.json（已递归搜索所有子目录）");
    process.exit(1);
  }
  console.log("🔍 找到 api.json:", apiPath);

  // 3) 去除注释和 BOM
  let raw = fs.readFileSync(apiPath, "utf8");
  raw = removeBOM(removeComments(raw));
  const parsed = JSON.parse(raw);

  // 4) 修复路径
  const fixed = fixPaths(parsed);

  // 5) 输出
  fs.writeFileSync("天神IY.txt", JSON.stringify(fixed, null, 2), "utf8");
  console.log("✅ 成功生成 天神IY.txt");

} catch (e) {
  console.error("❌ 解析失败");
  console.error(e);
  process.exit(1);
}
