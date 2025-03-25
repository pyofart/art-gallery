#!/bin/bash
set -e

# 自动暂存未提交的更改（避免干扰）
git stash save -u "Auto stash before auto_push"  # 保存所有更改（包括未跟踪的文件）

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

# 合并远程更改（变基）
git pull origin main --rebase

# 恢复之前暂存的更改（在脚本结束时）
git stash pop

echo "自动化推送完成"