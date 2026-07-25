import hashlib
import json
import os
import urllib.request

INPUT_JSON = "tvbox_config.json"
OUTPUT_JSON = "tvbox_modified.json"

JAR_KEY = "jar"
# 基础 URL
BASE_JAR_URL = (
    "https://down.nigx.cn/raw.githubusercontent.com/woshishiq1/jiemi/main/aowu.png"
)


def get_remote_file_md5(url: str) -> str | None:
    """下载远程 JAR/图片文件并计算其 MD5 值"""
    print(f"[+] 正在下载并计算文件 MD5: {url}")
    try:
        # 设置 User-Agent 模拟浏览器，防止被某些 CDN 拦截
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        md5_hash = hashlib.md5()
        with urllib.request.urlopen(req, timeout=15) as response:
            # 分块读取，防止大文件占用过大内存
            while chunk := response.read(8192):
                md5_hash.update(chunk)

        calculated_md5 = md5_hash.hexdigest()
        print(f"[+] 获取成功！MD5: {calculated_md5}")
        return calculated_md5
    except Exception as e:
        print(f"[!] 获取远程文件 MD5 失败 ({e})，将回退为无 MD5 模式。")
        return None


def add_jar_to_sites():
    if not os.path.exists(INPUT_JSON):
        print(f"[-] 未找到源文件 {INPUT_JSON}")
        return

    try:
        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"[-] 解析 JSON 失败: {e}")
        return

    sites_list = config_data.get("sites", [])
    if not sites_list or not isinstance(sites_list, list):
        print("[-] 未找到有效的 'sites' 列表。")
        return

    # 1. 计算 MD5 并拼接最终的 URL
    file_md5 = get_remote_file_md5(BASE_JAR_URL)
    if file_md5:
        final_jar_value = f"{BASE_JAR_URL};md5;{file_md5}"
    else:
        final_jar_value = BASE_JAR_URL

    print(f"\n[+] 准备注入的完整 Jar 地址 → {final_jar_value}")

    updated_count = 0
    skipped_count = 0

    # 2. 遍历 sites 进行注入
    for site in sites_list:
        if isinstance(site, dict):
            site_name = site.get("name", "未知站点")
            current_jar = site.get(JAR_KEY)

            # 智能判断：已有有效 jar 地址则跳过
            if (
                current_jar
                and isinstance(current_jar, str)
                and current_jar.strip()
            ):
                print(f"[~] 跳过已有 Jar 的站点: {site_name}")
                skipped_count += 1
                continue

            # 没有 jar 或 jar 为空 → 注入带有 MD5 的地址
            site[JAR_KEY] = final_jar_value
            print(f"[+] 已为站点注入 Jar: {site_name}")
            updated_count += 1

    if updated_count == 0 and skipped_count == 0:
        print("[-] sites 列表为空或格式异常")
        return

    # 3. 保存回写 JSON
    try:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print(f"\n[+] 操作完成！")
        print(f"    • 新增/更新 Jar 的站点: {updated_count} 个")
        print(f"    • 跳过（已有 Jar）的站点: {skipped_count} 个")
        print(f"    • 输出文件: {OUTPUT_JSON}")
    except Exception as e:
        print(f"[-] 保存新 JSON 失败: {e}")


if __name__ == "__main__":
    add_jar_to_sites()
