#!/usr/bin/env python3
"""
generate.py — 运行所有艺术生成器

用法:
  python3 generate.py                    # 生成所有作品（随机种子）
  python3 generate.py --seed 42          # 用指定种子生成
  python3 generate.py --date 2026-06-25  # 用日期作为种子
  python3 generate.py --all              # 同默认，生成所有系列
  python3 generate.py flow               # 仅流场
  python3 generate.py mandala            # 仅曼陀罗
"""

import os
import sys
import subprocess
import hashlib
import argparse


def date_to_seed(date_str):
    """将日期字符串转为整数种子"""
    return int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)


def main():
    os.makedirs("gallery", exist_ok=True)
    
    parser = argparse.ArgumentParser(description="Art Gallery Generator")
    parser.add_argument("targets", nargs="*", default=["flow", "mandala"],
                       help="要运行的生成器 (flow, mandala)")
    parser.add_argument("--seed", type=int, default=None,
                       help="随机种子（整数）")
    parser.add_argument("--date", type=str, default=None,
                       help="日期字符串，如 2026-06-25")
    parser.add_argument("--all", action="store_true",
                       help="运行所有生成器")
    
    args = parser.parse_args()
    
    # 确定种子
    seed = args.seed
    if args.date:
        seed = date_to_seed(args.date)
        print(f"📅 日期种子: {args.date} → seed={seed}")
    elif seed is not None:
        print(f"🎯 指定种子: {seed}")
    else:
        import time
        seed = int(time.time())
        print(f"🎲 随机种子: {seed}")
    
    # 确定目标
    if args.all or (not args.targets and not args.seed and not args.date):
        targets = ["flow", "mandala"]
    else:
        targets = args.targets if args.targets else ["flow", "mandala"]
    
    generators = {
        "flow": ("generators/flow_field.py", "🌊 流场艺术"),
        "mandala": ("generators/mandala.py", "🔮 曼陀罗"),
    }
    
    for key in targets:
        if key in generators:
            path, label = generators[key]
            print(f"\n{label}")
            print("-" * 30)
            result = subprocess.run(
                [sys.executable, path, "--seed", str(seed)],
                capture_output=True, text=True,
                cwd=os.path.dirname(os.path.abspath(__file__)) or ".",
            )
            print(result.stdout)
            if result.stderr:
                print("ERR:", result.stderr)
        else:
            print(f"未知生成器: {key}")
    
    # 列出所有作品
    print("\n📂 作品集总览")
    print("=" * 40)
    files = sorted(os.listdir("gallery"))
    total = 0
    for f in files:
        size = os.path.getsize(f"gallery/{f}")
        total += size
        print(f"  {f:35s}  {size//1024:4d}KB")
    print(f"\n共 {len(files)} 幅作品，总计 {total//1024}KB")
    
    # 更新画廊页面
    print("\n🖼️  构建画廊页面...")
    result = subprocess.run(
        [sys.executable, "build_gallery.py"],
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.stderr:
        print("ERR:", result.stderr)


if __name__ == "__main__":
    main()
