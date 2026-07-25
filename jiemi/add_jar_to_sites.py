import hashlib
import json
import os

INPUT_JSON = "tvbox_config.json"
OUTPUT_JSON = "tvbox_modified.json"
LOCAL_SPIDER_FILE = "aowu.png"  # 直接引用 download_spider.py 下载好的本地文件

JAR_KEY = "jar"
BASE_JAR_URL = (
    "https://down.nigx.cn/raw.githubusercontent.com/woshishiq1/jiemi/main/aowu.png"
)


def get_local_file_md5(file_path: str) -> str | None:
    """直接计算本地下载好的 aowu.png 的 MD5，避免网络拉取失败"""
    if not os.path.exists(file_path):
        print(f"[!] 本地未找到 {file_path}，无法计算 MD5")
        return None

    try:
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5_hash.update(chunk)

        calculated_md5 = md5_hash.hexdigest()
        print(f"[+] 本地 {file_path} MD5 计算成功: {calculated_md5}")
        return calculated_md5
    except Exception as e:
        print(f"[!] 计算本地 MD5 失败: {e}")
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

    # 1. 优先读取本地 aowu.png 的 MD5 并拼接 URL
    file_md5 = get_local_file_md5(LOCAL_SPIDER_FILE)
    if file_md5:
        final_jar_value = f"{BASE_JAR_URL};md5;{file_md5}"
    else:
        final_jar_value = BASE_JAR_URL

    print(f"\n[+] 准备注入的完整 Jar 地址 → {final_jar_value}")

    # 2. 同步更新顶级 spider 链接
    config_data["spider"] = final_jar_value
    print("[+] 已同步更新顶级 spider 链接")

    updated_count = 0
    skipped_count = 0

    # 3. 遍历 sites 进行注入
    for site in sites_list:
        if isinstance(site, dict):
            site_name = site.get("name", "未知站点")
            current_jar = site.get(JAR_KEY)

            # 已有有效 jar 地址则跳过
            if (
                current_jar
                and isinstance(current_jar, str)
                and current_jar.strip()
            ):
                print(f"[~] 跳过已有 Jar 的站点: {site_name}")
                skipped_count += 1
                continue

            # 没有 jar 或为空 -> 注入带有 MD5 的新地址
            site[JAR_KEY] = final_jar_value
            print(f"[+] 已为站点注入 Jar: {site_name}")
            updated_count += 1

    if updated_count == 0 and skipped_count == 0:
        print("[-] sites 列表为空或格式异常")
        return

    # 4. 保存写出新 JSON
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
