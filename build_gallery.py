#!/usr/bin/env python3
"""
build_gallery.py — 构建画廊：生成作品 + 更新页面

在 generate.py 之后运行，将 gallery/ 中的文件列表注入 index.html
这样画廊页面始终显示当前存在的作品。
"""

import os
import sys


def get_file_list():
    """获取 gallery 目录中的 SVG 文件列表"""
    gallery_dir = os.path.join(os.path.dirname(__file__), "gallery")
    if not os.path.isdir(gallery_dir):
        return []
    
    files = sorted(f for f in os.listdir(gallery_dir) if f.endswith(".svg"))
    return files


def inject_files_into_html(files):
    """将文件列表注入 index.html 的 {%FILES%} 占位符"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    
    if not os.path.isfile(html_path):
        print(f"❌ 未找到 index.html: {html_path}")
        return False
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 生成 JS 数组
    file_array = ",\n        ".join(f'"{f}"' for f in files)
    replacement = file_array if file_array else ""
    
    if "{%FILES%}" not in html:
        print("❌ index.html 中未找到 {%FILES%} 占位符")
        return False
    
    html = html.replace("{%FILES%}", replacement)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ index.html 已更新: {len(files)} 个文件")
    return True


def main():
    files = get_file_list()
    print(f"📂 gallery/ 中找到 {len(files)} 个文件")
    
    if not files:
        print("⚠️  没有作品文件，请先运行 python3 generate.py")
        return
    
    inject_files_into_html(files)


if __name__ == "__main__":
    main()
