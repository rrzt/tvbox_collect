# -*- coding: utf-8 -*-
import os
import sys
import json

PY_DIR = "/storage/emulated/0/VodPlus/小百合/py"

def build_sites():
    sites = []
    self_path = os.path.abspath(__file__)  # 当前脚本的绝对路径

    # 递归遍历 PY_DIR 下所有子目录
    for root, dirs, files in os.walk(PY_DIR):
        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            full_path = os.path.join(root, f)
            if os.path.abspath(full_path) == self_path:
                continue  # 排除自身

            file_name = f[:-3]  # 去掉 .py 后缀
            rel_path = os.path.relpath(full_path, PY_DIR)
            folder_part = os.path.dirname(rel_path)

            if folder_part:
                # 子文件夹里的 py 文件 → 不显示文件夹名
                name_part = file_name
            else:
# py 文件夹里直接有的 py 文件 → 显示文件夹名在前
                folder_name = os.path.basename(PY_DIR)
                name_part = folder_name + '☞' + file_name

            sites.append({
                "key": f"py_{name_part}",
                "name": name_part,
                "type": 3,
                "searchable": 1,
                "quickSearch": 1,
                "api": f"file://{full_path}"
            })
    return sites

CONFIG = {
    "spider": "",
    "sites": build_sites()
}
