import requests
import json
import re
from urllib.parse import urlparse, parse_qs

class DouyinCollectionSpider:
    def __init__(self):
        # 请求头，替换成你浏览器抓包的Cookie
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.douyin.com/",
            "Cookie": "这里粘贴你浏览器登录抖音后的完整Cookie"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_collection_id(self, collection_url: str) -> str:
        """从合集链接提取合集ID"""
        # 格式示例：https://www.douyin.com/collection/7566889922334444141/
        if "collection/" in collection_url:
            match = re.search(r"collection/(\d+)", collection_url)
            if match:
                return match.group(1)
        # 短链接解析（可选，需额外重定向处理）
        parsed = urlparse(collection_url)
        params = parse_qs(parsed.query)
        if "itemIds" in params:
            return params["itemIds"][0]
        raise Exception("合集链接解析失败，请检查链接格式")

    def fetch_collection_all_videos(self, collection_id: str):
        """获取合集全部视频列表"""
        base_api = "https://www.douyin.com/aweme/v1/collection/video/list/"
        all_videos = []
        max_cursor = 0
        has_more = True

        while has_more:
            params = {
                "collection_id": collection_id,
                "max_cursor": max_cursor,
                "count": 20,  # 单次拉取数量
                "version_code": "170000"
            }
            resp = self.session.get(base_api, params=params, timeout=15)
            if resp.status_code != 200:
                print(f"接口请求失败，状态码：{resp.status_code}")
                break
            data = resp.json()
            video_list = data.get("aweme_list", [])
            if not video_list:
                break
            # 解析单条视频信息
            for aweme in video_list:
                video_info = {
                    "视频ID": aweme.get("aweme_id"),
                    "标题": aweme.get("desc"),
                    "作者昵称": aweme.get("author", {}).get("nickname"),
                    "作者UID": aweme.get("author", {}).get("uid"),
                    "发布时间": aweme.get("create_time"),
                    "封面图": aweme.get("video", {}).get("cover", {}).get("url_list", [])[0] if aweme.get("video") else "",
                    "无水印播放地址": aweme.get("video", {}).get("play_addr", {}).get("url_list", [])[0] if aweme.get("video") else "",
                    "点赞数": aweme.get("statistics", {}).get("digg_count"),
                    "评论数": aweme.get("statistics", {}).get("comment_count"),
                    "分享数": aweme.get("statistics", {}).get("share_count")
                }
                all_videos.append(video_info)
            # 分页判断
            has_more = data.get("has_more", 0) == 1
            max_cursor = data.get("max_cursor", 0)
            print(f"已获取 {len(all_videos)} 条视频，继续加载下一页...")
        return all_videos

    def save_to_json(self, video_list, save_name="抖音合集数据.json"):
        """保存合集数据到本地JSON文件"""
        with open(save_name, "w", encoding="utf-8") as f:
            json.dump(video_list, f, ensure_ascii=False, indent=2)
        print(f"数据已保存至 {save_name}，共 {len(video_list)} 条视频")

if __name__ == "__main__":
    spider = DouyinCollectionSpider()
    # 替换为你的抖音合集链接
    collection_url = "https://www.douyin.com/collection/合集数字ID/"
    try:
        cid = spider.get_collection_id(collection_url)
        video_data = spider.fetch_collection_all_videos(cid)
        spider.save_to_json(video_data)
    except Exception as e:
        print(f"运行异常：{str(e)}")
