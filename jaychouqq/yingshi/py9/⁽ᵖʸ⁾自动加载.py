# -*- coding: utf-8 -*-
"""
TVBox 本地 Py 爬虫聚合源
========================
功能: 扫描指定目录下的 .py 爬虫文件，在 TVBox 中以频道形式展示，
      并在初始化时自动保存 py.json 到指定路径。
使用: 将本文件放入 TVBox 配置中，type=3，api 指向本文件路径即可。
"""
import os
import json
import base64
from base.spider import Spider


class Spider(Spider):
    # ==========================================================================
    # 📂 【配置区】在这里修改扫描目录和 JSON 保存路径
    # ==========================================================================
    PY_DIR    = "/storage/emulated/0/tvbox/py"
    SAVE_PATH = "/storage/emulated/0/tvbox/py.json"
    # ==========================================================================

    def __init__(self):
        super().__init__()
        self.inited = False
        # cache["categories"]: 首页频道列表
        # cache["file_index"]: 映射频道 ID 到文件路径
        self.cache = {"categories": [], "file_index": {}}

    def getName(self):
        return "本地Py爬虫聚合源"

    # ==========================================================================
    # 🚀 【核心初始化】扫描 py 文件 + 自动保存 JSON 配置
    # ==========================================================================
    def init(self, extend):
        if self.inited:
            return

        self._scan_py_files()
        self._save_config_json()
        self.inited = True

    def _scan_py_files(self):
        """递归扫描 PY_DIR，收集所有 .py 爬虫文件"""
        sites = []
        self_path = os.path.abspath(__file__)

        if not os.path.isdir(self.PY_DIR):
            self.cache["categories"] = sites
            return

        for root, dirs, files in os.walk(self.PY_DIR):
            for f in sorted(files):
                if not f.endswith(".py"):
                    continue
                full_path = os.path.join(root, f)
                if os.path.abspath(full_path) == self_path:
                    continue  # 排除自身

                file_name = f[:-3]  # 去掉 .py 后缀
                rel_path  = os.path.relpath(full_path, self.PY_DIR)
                folder_part = os.path.dirname(rel_path)

                if folder_part:
                    # 子文件夹里的 py 文件 → 不显示文件夹名
                    name_part = file_name
                else:
                    # py 根目录里直接有的 py 文件 → 显示文件夹名在前
                    folder_name = os.path.basename(self.PY_DIR)
                    name_part = f"{file_name}"

                # Base64 编码 tid，供 TVBox 内部传递
                tid = base64.b64encode(f"PY|{full_path}".encode()).decode()
                sites.append({
                    "type_id": tid,
                    "type_name": name_part,
                    # 排序键: 根目录文件排前面，然后按名称排序
                    "sk": (0 if not folder_part else 1, name_part)
                })
                self.cache["file_index"][tid] = full_path

        self.cache["categories"] = sorted(sites, key=lambda x: x["sk"])

    def _build_api(self, f_path):
        """用 PY_DIR 变量拼接 api 路径（不带 file:// 前缀）"""
        rel = os.path.relpath(f_path, self.PY_DIR)
        return f"./py/{rel}"

    def _save_config_json(self):
        """将扫描结果保存为 TVBox 可用的 config.json"""
        config = {
            "spider": "./spider.jar",
            "sites": []
        }
        for cat in self.cache["categories"]:
            f_path = self.cache["file_index"].get(cat["type_id"], "")
            if not f_path:
                continue
            config["sites"].append({
                "key": f"{cat['type_name']}",
                "name": f"⁽ᵖʸ⁾{cat['type_name']}",
                "type": 3,
                "searchable": 1,
                "quickSearch": 1,
                "api": self._build_api(f_path)
            })

        # 确保保存目录存在
        save_dir = os.path.dirname(self.SAVE_PATH)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        with open(self.SAVE_PATH, "w", encoding="utf-8") as fp:
            json.dump(config, fp, ensure_ascii=False, indent=2)

    # ==========================================================================
    # 📺 【TVBox 标准接口】
    # ==========================================================================
    def homeContent(self, filter):
        """返回首页频道列表"""
        return {"class": self.cache["categories"]}

    def categoryContent(self, tid, pg, filter, ext):
        """返回指定频道下的条目列表"""
        if str(pg) != "1":
            return {"list": []}

        f_path = self.cache["file_index"].get(tid, "")
        if not f_path or not os.path.exists(f_path):
            return {"list": []}

        f_base = os.path.basename(f_path).rsplit('.', 1)[0]
        v_id = base64.b64encode(f"PY|{f_path}".encode()).decode()

        return {"list": [{
            "vod_id": v_id,
            "vod_name": f_base,
            "vod_pic": "",
            "vod_remarks": self._build_api(f_path)
        }]}

    def detailContent(self, array):
        """返回详情页，展示爬虫配置信息"""
        try:
            v_id_raw = str(array[0])
            # Base64 补齐
            v_id_raw += "=" * ((4 - len(v_id_raw) % 4) % 4)
            raw_decoded = base64.b64decode(v_id_raw).decode('utf-8', errors='ignore')

            # 解析 ID: 格式为 "PY|文件路径"
            if raw_decoded.startswith("PY|"):
                f_path = raw_decoded[3:]
            else:
                f_path = raw_decoded

            if not os.path.exists(f_path):
                return {"list": [{"vod_name": "文件不存在", "vod_content": f"路径不存在: {f_path}"}]}

            f_base = os.path.basename(f_path).rsplit('.', 1)[0]

            # 构建 TVBox 站点配置信息
            site_info = {
                "key": f"py_{f_base}",
                "name": f_base,
                "type": 3,
                "searchable": 1,
                "quickSearch": 1,
                "api": self._build_api(f_path)
            }
            info_text = json.dumps(site_info, ensure_ascii=False, indent=2)

            # 再次保存 JSON 配置（确保最新）
            self._save_config_json()

            return {"list": [{
                "vod_name": f_base,
                "vod_pic": "",
                "vod_play_from": "配置信息",
                "vod_play_url": f"查看配置${f_path}",
                "vod_content": (
                    f"✅ 配置已自动保存到: {self.SAVE_PATH}\n\n"
                    f"站点配置详情:\n{info_text}\n\n"
                    f"文件路径: {f_path}"
                )
            }]}
        except Exception as e:
            return {"list": [{"vod_name": "解析错误", "vod_content": f"错误详情: {str(e)}"}]}

    def searchContent(self, key, quick):
        """本地搜索 py 文件"""
        res = []
        for tid, f_path in self.cache["file_index"].items():
            f_base = os.path.basename(f_path).rsplit('.', 1)[0]
            if key.lower() in f_base.lower():
                v_id = base64.b64encode(f"PY|{f_path}".encode()).decode()
                res.append({
                    "vod_id": v_id,
                    "vod_name": f_base,
                    "vod_pic": "",
                    "vod_remarks": self._build_api(f_path)
                })
        return {"list": res}

    def playerContent(self, flag, id, vipFlags):
        """播放接口（本源无实际播放内容，仅返回路径）"""
        url = id.split('$')[-1] if '$' in id else id
        return {"url": url, "header": {}, "parse": 0}

    def destroy(self):
        """资源释放"""
        return "destroy"
