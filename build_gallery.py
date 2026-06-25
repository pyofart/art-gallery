#!/usr/bin/env python3
"""
build_gallery.py — 构建画廊：生成作品 + 更新页面

每次运行时扫描 gallery/ 目录，将文件列表注入 index.html 的 knownFiles 数组。
支持多次运行——无论数组是否已被替换，都能正确更新。
"""

import os
import re


def get_file_list():
    """获取 gallery 目录中的 SVG 文件列表"""
    gallery_dir = os.path.join(os.path.dirname(__file__), "gallery")
    if not os.path.isdir(gallery_dir):
        return []
    
    files = sorted(f for f in os.listdir(gallery_dir) if f.endswith(".svg"))
    return files


def inject_files_into_html(files):
    """将文件列表注入 index.html 的 knownFiles 数组"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    
    if not os.path.isfile(html_path):
        print(f"❌ 未找到 index.html: {html_path}")
        return False
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 生成 JS 数组字符串
    if files:
        file_entries = ",\n        ".join(f'"{f}"' for f in files)
        replacement = file_entries
    else:
        replacement = ""
    
    # 用正则替换 knownFiles 数组内容（不管当前是占位符还是已替换的列表）
    pattern = r'(var knownFiles = \[)([^\]]*)(\])'
    
    new_array = f"\\1\n        {replacement}\n    \\3"
    
    if re.search(pattern, html, re.DOTALL):
        html = re.sub(pattern, new_array, html, count=1, flags=re.DOTALL)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ index.html 已更新: {len(files)} 个文件")
        return True
    else:
        print("❌ 未找到 knownFiles 数组，index.html 可能格式不正确")
        return False


def main():
    files = get_file_list()
    print(f"📂 gallery/ 中找到 {len(files)} 个文件")
    
    if not files:
        print("⚠️  没有作品文件，请先运行 python3 generate.py")
        return
    
    inject_files_into_html(files)


if __name__ == "__main__":
    main()
