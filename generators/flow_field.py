#!/usr/bin/env python3
"""
flow_field.py — 流场线画生成器

用数学噪声函数驱动粒子在矢量场中流动，
生成有机形态的线条画。零外部依赖，纯 Python。
"""

import math
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom


def noise(x, y, seed=42):
    """简易伪随机噪声函数（无需外部库）"""
    n = math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453
    return n - math.floor(n)


def smooth_noise(x, y, seed=42):
    """双线性插值噪声"""
    ix, iy = int(x), int(y)
    fx, fy = x - ix, y - iy
    
    n00 = noise(ix, iy, seed)
    n10 = noise(ix + 1, iy, seed)
    n01 = noise(ix, iy + 1, seed)
    n11 = noise(ix + 1, iy + 1, seed)
    
    ux = fx * fx * (3 - 2 * fx)
    uy = fy * fy * (3 - 2 * fy)
    
    nx0 = n00 + (n10 - n00) * ux
    nx1 = n01 + (n11 - n01) * ux
    return nx0 + (nx1 - nx0) * uy


def fbm(x, y, octaves=3, seed=42):
    """分形布朗运动 - 多层噪声叠加"""
    value = 0
    amplitude = 1
    frequency = 1
    max_val = 0
    for _ in range(octaves):
        value += amplitude * smooth_noise(x * frequency, y * frequency, seed)
        max_val += amplitude
        amplitude *= 0.5
        frequency *= 2
    return value / max_val


def angle_at(x, y, seed=42):
    """流场中某点的角度（用噪声驱动）"""
    # 用两层噪声产生平滑变化的角度场
    a = fbm(x * 0.02, y * 0.02, octaves=4, seed=seed) * 2 * math.pi
    b = fbm(x * 0.01 + 100, y * 0.01 + 100, octaves=2, seed=seed + 1) * math.pi
    return a + b


class FlowField:
    """流场：定义粒子运动的矢量场"""
    
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.seed = seed or random.randint(0, 9999)
    
    def angle(self, x, y):
        return angle_at(x, y, seed=self.seed)
    
    def generate_lines(self, num_particles=2000, max_steps=200, step_size=3.0):
        """从随机起点追踪粒子路径，生成线条"""
        lines = []
        
        for p in range(num_particles):
            # 随机起点
            sx = random.uniform(0, self.width)
            sy = random.uniform(0, self.height)
            
            points = [(sx, sy)]
            x, y = sx, sy
            
            for _ in range(max_steps):
                theta = self.angle(x, y)
                dx = math.cos(theta) * step_size
                dy = math.sin(theta) * step_size
                x += dx
                y += dy
                
                # 边界检查
                if x < 0 or x > self.width or y < 0 or y > self.height:
                    break
                
                points.append((x, y))
            
            if len(points) > 10:
                lines.append(points)
        
        return lines


def line_to_svg_path(points):
    """将点集转换为 SVG path d 属性"""
    if not points:
        return ""
    parts = [f"M {points[0][0]:.1f},{points[0][1]:.1f}"]
    for p in points[1:]:
        parts.append(f"L {p[0]:.1f},{p[1]:.1f}")
    return " ".join(parts)


def generate_flow_field_svg(
    width=800,
    height=800,
    num_particles=2000,
    max_steps=200,
    stroke_width=0.5,
    color="#2c3e50",
    background="#fafafa",
    seed=None,
):
    """生成完整的流场 SVG 文件
    
    返回 SVG 字符串
    """
    field = FlowField(width, height, seed=seed)
    lines = field.generate_lines(
        num_particles=num_particles,
        max_steps=max_steps,
        step_size=3.0,
    )
    
    # 构建 SVG
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
    })
    
    # 背景
    bg = ET.SubElement(svg, "rect", {
        "width": "100%",
        "height": "100%",
        "fill": background,
    })
    svg.append(bg)
    
    # 路径（按长度从短到长排序，让短线条在底层）
    lines.sort(key=len)
    
    # 渐变透明度：越长的线越淡，增加深度感
    g = ET.SubElement(svg, "g", {
        "fill": "none",
        "stroke": color,
        "stroke-width": str(stroke_width),
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
    })
    
    for i, points in enumerate(lines):
        path_data = line_to_svg_path(points)
        opacity = 0.15 + (len(points) / 200) * 0.85
        path = ET.SubElement(g, "path", {
            "d": path_data,
            "opacity": f"{min(opacity, 0.9):.2f}",
        })
    
    # 格式化为漂亮的 XML
    rough = ET.tostring(svg, encoding="unicode")
    dom = minidom.parseString(rough)
    pretty = dom.toprettyxml(indent="  ")
    dom.unlink()
    
    # 去掉 XML 声明
    lines = pretty.split("\n")
    svg_lines = [l for l in lines if not l.startswith("<?xml")]
    return "\n".join(svg_lines)


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Flow Field Generator")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()
    
    base_seed = args.seed
    print(f"🌊 流场艺术生成器 (seed={base_seed})")
    print("=" * 40)
    
    # 种子决定色彩倾向和画风
    random.seed(base_seed)
    
    # 色彩池 — 从 15 种配色中根据种子选 5 种
    color_pool = [
        ("flow-ocean", "#1a5276", "#eaf2f8", 0.6),
        ("flow-sunset", "#e74c3c", "#fdf2e9", 0.5),
        ("flow-forest", "#1e8449", "#e8f8f5", 0.6),
        ("flow-midnight", "#2c3e50", "#f8f9fa", 0.5),
        ("flow-gold", "#d4a017", "#fef9e7", 0.4),
        ("flow-aurora", "#6c3483", "#f5eef8", 0.5),
        ("flow-teal", "#0e6655", "#e8f8f5", 0.6),
        ("flow-coral", "#cb4335", "#fdedec", 0.5),
        ("flow-steel", "#566573", "#f4f6f7", 0.4),
        ("flow-lavender", "#7d3c98", "#f4ecf7", 0.5),
        ("flow-peach", "#e67e22", "#fef5e7", 0.5),
        ("flow-jade", "#148f77", "#e8f6f3", 0.5),
        ("flow-rouge", "#922b21", "#fdedec", 0.6),
        ("flow-sky", "#2e86c1", "#eaf2f8", 0.4),
        ("flow-charcoal", "#424949", "#fdfefe", 0.4),
    ]
    
    # 种子决定粒子流动形态（不同种子→不同流场走向）
    random.shuffle(color_pool)
    palettes = color_pool[:5]
    
    for i, (name, color, bg, width) in enumerate(palettes):
        # 每幅画用不同的子种子，但都与基础种子相关
        sub_seed = base_seed * 10 + i
        # 粒子数也随种子微调
        particles = 600 + (base_seed % 5) * 100 + i * 30
        
        svg = generate_flow_field_svg(
            width=800,
            height=800,
            num_particles=int(particles),
            max_steps=100 + (base_seed % 10) * 5,
            stroke_width=width,
            color=color,
            background=bg,
            seed=sub_seed,
        )
        filename = f"gallery/{name}.svg"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg)
        size = len(svg)
        print(f"  ✓ {filename}  ({size/1024:.0f}KB)")
    
    print(f"\n✅ 共生成 {len(palettes)} 幅流场艺术作品 (seed={base_seed})")
