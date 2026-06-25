#!/usr/bin/env python3
"""
mandala.py — 几何万花筒生成器

用旋转对称和递归几何生成曼陀罗图案。
零外部依赖，纯 Python SVG 输出。
"""

import math
import random
import xml.etree.ElementTree as ET
from xml.dom import minidom


def rotate_point(x, y, cx, cy, angle):
    """绕中心旋转点"""
    s = math.sin(angle)
    c = math.cos(angle)
    dx = x - cx
    dy = y - cy
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


def generate_petal(cx, cy, radius, angle, layers=3):
    """生成一个花瓣层的点集"""
    points = []
    segments = max(8, int(radius * 0.4))
    
    for i in range(segments + 1):
        t = i / segments * math.pi * 2 / layers
        r = radius * (0.3 + 0.7 * abs(math.sin(t * layers)))
        x = cx + r * math.cos(angle + t)
        y = cy + r * math.sin(angle + t)
        points.append((x, y))
    
    return points


def generate_mandala_svg(
    width=800,
    height=800,
    num_petals=8,
    layers=6,
    color_scheme="warm",
    background="#0d0d0d",
    seed=None,
):
    """生成曼陀罗 SVG
    
    参数:
        num_petals: 花瓣对称数 (4-24)
        layers: 层数 (3-12)
        color_scheme: warm / cool / pastel / mono
    """
    if seed:
        random.seed(seed)
    
    cx, cy = width / 2, height / 2
    max_radius = min(width, height) * 0.42
    
    # 配色方案
    schemes = {
        "warm": ["#e74c3c", "#e67e22", "#f1c40f", "#c0392b", "#d35400"],
        "cool": ["#3498db", "#2ecc71", "#1abc9c", "#2980b9", "#16a085"],
        "pastel": ["#f8c8dc", "#b8e6c8", "#c8d8f8", "#f8e8b8", "#e8c8f8"],
        "mono": ["#ffffff", "#cccccc", "#999999", "#666666", "#333333"],
    }
    colors = schemes.get(color_scheme, schemes["warm"])
    
    # 构建 SVG
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
    })
    
    # 背景
    bg = ET.SubElement(svg, "rect", {
        "width": "100%", "height": "100%", "fill": background,
    })
    
    # 主群组
    main_g = ET.SubElement(svg, "g", {
        "transform": f"translate({cx},{cy})",
    })
    
    # 逐层生成
    for layer in range(layers):
        layer_radius = max_radius * (layer + 1) / layers
        layer_alpha = 1.0 - (layer / layers) * 0.3
        stroke_w = 1.5 - (layer / layers) * 0.8
        color = colors[layer % len(colors)]
        
        # 每层的形状变化
        base_angle_offset = random.uniform(0, math.pi)
        segments = max(6, int(layer_radius * 0.5))
        
        # 外圈：花瓣形状
        g_outer = ET.SubElement(main_g, "g", {
            "fill": "none",
            "stroke": color,
            "stroke-width": f"{max(stroke_w, 0.3):.1f}",
            "opacity": f"{layer_alpha:.2f}",
        })
        
        for p in range(num_petals):
            angle = (2 * math.pi / num_petals) * p + base_angle_offset
            r = layer_radius
            
            # 生成花瓣路径
            points = []
            for i in range(segments + 1):
                t = i / segments * 2 * math.pi
                petal_shape = abs(math.sin(t * (layer + 2) * 0.5 + p * 0.5))
                rr = r * (0.2 + 0.8 * petal_shape)
                x = rr * math.cos(t + angle)
                y = rr * math.sin(t + angle)
                points.append((x, y))
            
            path_data = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z"
            path = ET.SubElement(g_outer, "path", {"d": path_data})
        
        # 内圈：圆点（点缀）
        dots_count = max(6, num_petals * (layer + 1))
        for _ in range(dots_count):
            a = random.uniform(0, 2 * math.pi)
            r = layer_radius * random.uniform(0.3, 0.9)
            dot_r = random.uniform(1, 3) * (1 - layer / layers * 0.5)
            dot = ET.SubElement(main_g, "circle", {
                "cx": f"{r * math.cos(a):.1f}",
                "cy": f"{r * math.sin(a):.1f}",
                "r": f"{dot_r:.1f}",
                "fill": color,
                "opacity": f"{layer_alpha:.2f}",
            })
    
    # 中心点
    center = ET.SubElement(main_g, "circle", {
        "cx": "0", "cy": "0",
        "r": f"{max_radius * 0.08:.0f}",
        "fill": colors[0],
        "opacity": "0.8",
    })
    
    # 格式化成漂亮的 XML
    rough = ET.tostring(svg, encoding="unicode")
    dom = minidom.parseString(rough)
    pretty = dom.toprettyxml(indent="  ")
    dom.unlink()
    
    lines = pretty.split("\n")
    svg_lines = [l for l in lines if not l.startswith("<?xml")]
    return "\n".join(svg_lines)


if __name__ == "__main__":
    print("🔮 曼陀罗生成器")
    print("=" * 40)
    
    import os
    os.makedirs("gallery", exist_ok=True)
    
    # 生成多种风格
    configs = [
        ("mandala-sun", 12, 8, "warm", "#0d0d0d"),
        ("mandala-ocean", 8, 6, "cool", "#0a1628"),
        ("mandala-spring", 16, 7, "pastel", "#1a1a2e"),
        ("mandala-eclipse", 6, 10, "mono", "#000000"),
        ("mandala-fire", 24, 5, "warm", "#1a0a00"),
    ]
    
    for name, petals, layers, scheme, bg in configs:
        svg = generate_mandala_svg(
            width=800, height=800,
            num_petals=petals,
            layers=layers,
            color_scheme=scheme,
            background=bg,
            seed=hash(name) % 10000,
        )
        filename = f"gallery/{name}.svg"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg)
        size = len(svg)
        print(f"  ✓ {filename}  ({size/1024:.0f}KB)")
    
    print(f"\n✅ 共生成 {len(configs)} 幅曼陀罗作品")
