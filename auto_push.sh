#!/bin/bash
set -e

# 生成新图片
python generate_art.py
echo "图片生成完成"

# 检查文件存在性
if [ ! -f "art.png" ]; then
  echo "错误：未找到 art.png 文件"
  exit 1
fi

# Git 操作
git add art.png
git commit -m "Update art $(date +%s)"
git pull origin main --rebase  # 合并远程更改
git push origin main