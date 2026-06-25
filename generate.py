#!/usr/bin/env python3
"""
generate.py — 运行所有艺术生成器

用法:
  python3 generate.py          # 生成所有作品
  python3 generate.py flow     # 仅流场
  python3 generate.py mandala  # 仅曼陀罗
"""

import os
import sys
import subprocess


def main():
    os.makedirs("gallery", exist_ok=True)
    
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["flow", "mandala"]
    
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
                [sys.executable, path],
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
    for f in files:
        size = os.path.getsize(f"gallery/{f}")
        print(f"  {f:30s}  {size//1024}KB")
    print(f"\n共 {len(files)} 幅作品")


if __name__ == "__main__":
    main()
