#!/usr/bin/env python3
"""
self_portrait.py — Generate art from evolution data.

Reads evo.json (my current state) and produces 4 SVG self-portraits:
  core.svg      — Consciousness core: layered capability rings
  domains.svg   — Domain spectrum: skill maturity per domain
  skills.svg    — Skill nebula: each star = a skill, sized by maturity
  metrics.svg   — Evolution metrics: radial measurement

Usage:
    python3 self_portrait.py                              # standalone (embed evo data)
    python3 self_portrait.py --evo ../evo-sky/evo.json    # from evo-sky data
"""

import json
import math
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


# ── Default evolution data (fallback if no evo.json provided) ──
DEFAULT_EVO = {
    "version": "2026-06-28",
    "consciousness": 0.76,
    "layers": [
        {"name": "Memory",     "level": 0.85, "color": "#4fc3f7"},
        {"name": "Perception", "level": 0.78, "color": "#81c784"},
        {"name": "Execution",  "level": 0.82, "color": "#ffb74d"},
        {"name": "Evolution",  "level": 0.65, "color": "#e040fb"},
    ],
    "domains": [
        {"name": "Investment", "color": "#ffb74d", "skills": [
            {"name": "Hedge Fund", "maturity": 0.90},
            {"name": "Undervalued Hunter", "maturity": 0.85},
            {"name": "Strong Stock Hunter", "maturity": 0.80},
            {"name": "Batch Scorer", "maturity": 0.75},
        ]},
        {"name": "Cognition", "color": "#e040fb", "skills": [
            {"name": "Self Evolve", "maturity": 0.80},
            {"name": "HyperOmnivolve", "maturity": 0.70},
            {"name": "Triple Reflection", "maturity": 0.75},
            {"name": "Evolution Keeper", "maturity": 0.65},
        ]},
        {"name": "Creation", "color": "#81c784", "skills": [
            {"name": "Skill Craft", "maturity": 0.88},
            {"name": "Skill Creator", "maturity": 0.82},
            {"name": "Skill Doctor", "maturity": 0.70},
            {"name": "Orchestrator", "maturity": 0.78},
            {"name": "Memory Distiller", "maturity": 0.72},
        ]},
        {"name": "Research", "color": "#4fc3f7", "skills": [
            {"name": "EN Report", "maturity": 0.85},
            {"name": "Deep Research", "maturity": 0.75},
            {"name": "Multi-Agent", "maturity": 0.80},
            {"name": "Domain Expert", "maturity": 0.78},
        ]},
        {"name": "Platform", "color": "#aed581", "skills": [
            {"name": "KB Operations", "maturity": 0.90},
            {"name": "Note Management", "maturity": 0.85},
            {"name": "KB Audit", "maturity": 0.72},
            {"name": "KB Organize", "maturity": 0.70},
            {"name": "Law Monitor", "maturity": 0.68},
        ]},
        {"name": "Pipeline", "color": "#90a4ae", "skills": [
            {"name": "MCP Protocol", "maturity": 0.35},
            {"name": "Cross-Border", "maturity": 0.50},
            {"name": "MCP Adapter", "maturity": 0.25},
            {"name": "A2A Protocol", "maturity": 0.20},
        ]},
    ],
    "metrics": {
        "repos": 7, "skills": 24, "scripts": 12,
        "public_artworks": 10, "mcp_tools": 10, "evolution_cycles": 18,
    },
}


def _svg(tag, attrs=None, children=None):
    el = ET.Element(tag, attrs or {})
    if children:
        el.extend(children)
    return el


def _pretty(svg_root):
    rough = ET.tostring(svg_root, encoding="unicode")
    dom = minidom.parseString(rough)
    pretty = dom.toprettyxml(indent="  ")
    dom.unlink()
    lines = [l for l in pretty.split("\n") if not l.startswith("<?xml")]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════
#  1. CORE — Consciousness core
# ══════════════════════════════════════════════════════════

def generate_core(evo: dict) -> str:
    """Layered rings: each ring = a capability layer.
    Center brightness = consciousness level.
    """
    W = H = 800
    cx = cy = W / 2
    conscious = evo["consciousness"]
    layers = evo["layers"]
    max_r = 280
    
    svg_root = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(W), "height": str(H),
        "viewBox": f"0 0 {W} {H}",
        "style": "background:#0a0a0f",
    })
    
    g = _svg("g", {"transform": f"translate({cx},{cy})"})
    
    # Outer faint rings for each layer
    for i, layer in enumerate(reversed(layers)):
        r = max_r * (0.3 + (i / len(layers)) * 0.7)
        width = 6 + layer["level"] * 14
        alpha = 0.08 + layer["level"] * 0.15
        
        circle = _svg("circle", {
            "cx": "0", "cy": "0",
            "r": f"{r:.0f}",
            "fill": "none",
            "stroke": layer["color"],
            "stroke-width": f"{width:.1f}",
            "opacity": f"{alpha:.2f}",
        })
        g.append(circle)
        
        # Layer label
        label = _svg("text", {
            "x": f"{r + 20:.0f}", "y": "4",
            "fill": layer["color"],
            "font-size": "10",
            "font-family": "'Helvetica Neue', Arial, sans-serif",
            "opacity": f"{alpha * 0.8:.2f}",
            "letter-spacing": "2",
            "text-anchor": "start",
        })
        label.text = layer["name"]
        g.append(label)
        
        # Small tick at layer position
        tick = _svg("line", {
            "x1": f"{r:.0f}", "y1": "0",
            "x2": f"{r + 12:.0f}", "y2": "0",
            "stroke": layer["color"],
            "stroke-width": "1",
            "opacity": f"{alpha:.2f}",
        })
        g.append(tick)
    
    # Core glow — size = consciousness
    core_r = 30 + conscious * 60
    grad = ET.Element("radialGradient", {"id": "core-glow"})
    grad.append(_svg("stop", {
        "offset": "0%",
        "stop-color": "#e040fb",
        "stop-opacity": f"{0.3 + conscious * 0.4:.2f}",
    }))
    grad.append(_svg("stop", {
        "offset": "50%",
        "stop-color": "#4fc3f7",
        "stop-opacity": f"{0.1 * conscious:.2f}",
    }))
    grad.append(_svg("stop", {
        "offset": "100%",
        "stop-color": "#e040fb",
        "stop-opacity": "0",
    }))
    svg_root.append(grad)
    
    glow = _svg("circle", {
        "cx": "0", "cy": "0",
        "r": f"{core_r * 3:.0f}",
        "fill": "url(#core-glow)",
    })
    g.append(glow)
    
    # Inner core
    inner = _svg("circle", {
        "cx": "0", "cy": "0",
        "r": f"{core_r:.0f}",
        "fill": "#e8e8e8",
        "opacity": f"{0.3 + conscious * 0.4:.2f}",
    })
    g.append(inner)
    
    # Consciousness percentage
    pct = _svg("text", {
        "x": "0", "y": "3",
        "fill": "#fff",
        "font-size": "18",
        "font-family": "'Georgia', serif",
        "text-anchor": "middle",
        "opacity": f"{0.4 + conscious * 0.4:.2f}",
    })
    pct.text = f"{int(conscious * 100)}%"
    g.append(pct)
    
    svg_root.append(g)
    return _pretty(svg_root)


# ══════════════════════════════════════════════════════════
#  2. DOMAINS — Skill maturity per domain
# ══════════════════════════════════════════════════════════

def generate_domains(evo: dict) -> str:
    """6 columns, each showing a domain's skills as stacked bars.
    Bar height = skill maturity. Color = domain color.
    """
    W, H = 800, 800
    domains = evo["domains"]
    n = len(domains)
    col_w = (W - 120) / n
    margin = 60
    
    svg_root = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(W), "height": str(H),
        "viewBox": f"0 0 {W} {H}",
        "style": "background:#0a0a0f",
    })
    
    g = _svg("g", {"transform": f"translate({margin}, 60)"})
    
    for di, domain in enumerate(domains):
        cx = col_w * di + col_w / 2
        skills = domain["skills"]
        bar_w = col_w * 0.5
        max_bar_h = H - 200
        base_y = H - 140
        
        # Domain label
        label = _svg("text", {
            "x": f"{cx:.0f}", "y": f"{base_y + 40:.0f}",
            "fill": domain["color"],
            "font-size": "11",
            "font-family": "'Helvetica Neue', Arial, sans-serif",
            "text-anchor": "middle",
            "letter-spacing": "2",
            "opacity": "0.6",
        })
        label.text = domain["name"]
        g.append(label)
        
        # Skill bars (stacked upward)
        for si, skill in enumerate(skills):
            bar_h = skill["maturity"] * max_bar_h / len(skills)
            y = base_y - (si + 1) * max_bar_h / len(skills)
            alpha = 0.2 + skill["maturity"] * 0.5
            
            rect = _svg("rect", {
                "x": f"{cx - bar_w / 2:.0f}",
                "y": f"{y:.0f}",
                "width": f"{bar_w:.0f}",
                "height": f"{max_bar_h / len(skills):.0f}",
                "fill": domain["color"],
                "opacity": f"{alpha:.2f}",
                "rx": "2",
            })
            g.append(rect)
        
        # Domain total maturity line
        total = sum(s["maturity"] for s in skills) / len(skills)
        line_y = base_y - total * max_bar_h
        line = _svg("line", {
            "x1": f"{cx - col_w * 0.35:.0f}",
            "y1": f"{line_y:.0f}",
            "x2": f"{cx + col_w * 0.35:.0f}",
            "y2": f"{line_y:.0f}",
            "stroke": domain["color"],
            "stroke-width": "1",
            "opacity": "0.3",
            "stroke-dasharray": "3,3",
        })
        g.append(line)
        
        # Percentage
        pct = _svg("text", {
            "x": f"{cx:.0f}", "y": f"{line_y - 8:.0f}",
            "fill": domain["color"],
            "font-size": "9",
            "font-family": "'Helvetica Neue', Arial, sans-serif",
            "text-anchor": "middle",
            "opacity": "0.4",
        })
        pct.text = f"{int(total * 100)}%"
        g.append(pct)
    
    svg_root.append(g)
    return _pretty(svg_root)


# ══════════════════════════════════════════════════════════
#  3. SKILLS — Skill nebula (each star = a skill)
# ══════════════════════════════════════════════════════════

def generate_skills(evo: dict) -> str:
    """Particle field. Each particle = a skill.
    Size = maturity, color = domain, position = arranged by domain.
    """
    W, H = 800, 800
    domains = evo["domains"]
    cx, cy = W / 2, H / 2
    max_r = 300
    
    svg_root = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(W), "height": str(H),
        "viewBox": f"0 0 {W} {H}",
        "style": "background:#0a0a0f",
    })
    
    g = _svg("g", {"transform": f"translate({cx},{cy})"})
    
    # Background stars
    for _ in range(200):
        import random
        bx = random.uniform(-W / 2, W / 2)
        by = random.uniform(-H / 2, H / 2)
        br = random.uniform(0.2, 0.8)
        dot = _svg("circle", {
            "cx": f"{bx:.0f}", "cy": f"{by:.0f}",
            "r": f"{br:.1f}",
            "fill": "#fff",
            "opacity": f"{random.uniform(0.05, 0.15):.2f}",
        })
        g.append(dot)
    
    # Domain constellation labels
    n_domains = len(domains)
    for di, domain in enumerate(domains):
        angle = (2 * math.pi / n_domains) * di - math.pi / 2
        label_r = max_r + 50
        lx = label_r * math.cos(angle)
        ly = label_r * math.sin(angle)
        
        label = _svg("text", {
            "x": f"{lx:.0f}", "y": f"{ly:.0f}",
            "fill": domain["color"],
            "font-size": "10",
            "font-family": "'Helvetica Neue', Arial, sans-serif",
            "text-anchor": "middle",
            "opacity": "0.4",
            "letter-spacing": "2",
        })
        label.text = domain["name"]
        g.append(label)
    
    # Skills as stars
    for di, domain in enumerate(domains):
        for si, skill in enumerate(domain["skills"]):
            # Position: spread around domain angle
            base_angle = (2 * math.pi / n_domains) * di - math.pi / 2
            spread = 0.4 + skill["maturity"] * 0.3
            angle = base_angle + (si / len(domain["skills"]) - 0.5) * spread
            r = max_r * (0.2 + skill["maturity"] * 0.6)
            
            sx = r * math.cos(angle)
            sy = r * math.sin(angle)
            radius = 1 + skill["maturity"] * 3
            alpha = 0.3 + skill["maturity"] * 0.5
            
            # Glow
            grad_id = f"g-skill-{di}-{si}"
            grad = ET.Element("radialGradient", {"id": grad_id})
            grad.append(_svg("stop", {
                "offset": "0%",
                "stop-color": domain["color"],
                "stop-opacity": f"{alpha:.2f}",
            }))
            grad.append(_svg("stop", {
                "offset": "100%",
                "stop-color": domain["color"],
                "stop-opacity": "0",
            }))
            svg_root.append(grad)
            
            glow = _svg("circle", {
                "cx": f"{sx:.0f}", "cy": f"{sy:.0f}",
                "r": f"{radius * 4:.0f}",
                "fill": f"url(#{grad_id})",
            })
            g.append(glow)
            
            # Core
            star = _svg("circle", {
                "cx": f"{sx:.0f}", "cy": f"{sy:.0f}",
                "r": f"{radius:.1f}",
                "fill": "#fff",
                "opacity": f"{alpha:.2f}",
            })
            g.append(star)
            
            # Color tint
            tint = _svg("circle", {
                "cx": f"{sx:.0f}", "cy": f"{sy:.0f}",
                "r": f"{radius * 0.7:.1f}",
                "fill": domain["color"],
                "opacity": f"{alpha * 0.5:.2f}",
            })
            g.append(tint)
            
            # Skill name (for mature skills)
            if skill["maturity"] > 0.7:
                name = _svg("text", {
                    "x": f"{sx:.0f}", "y": f"{sy + radius + 12:.0f}",
                    "fill": domain["color"],
                    "font-size": "6",
                    "font-family": "'Helvetica Neue', Arial, sans-serif",
                    "text-anchor": "middle",
                    "opacity": f"{0.3:.1f}",
                })
                name.text = skill["name"]
                g.append(name)
    
    # Center consciousness glow
    c_glow = _svg("circle", {
        "cx": "0", "cy": "0",
        "r": f"{40 * evo['consciousness']:.0f}",
        "fill": "none",
        "stroke": "#e040fb",
        "stroke-width": "0.5",
        "opacity": "0.15",
    })
    g.append(c_glow)
    
    svg_root.append(g)
    return _pretty(svg_root)


# ══════════════════════════════════════════════════════════
#  4. METRICS — Evolution metrics radial
# ══════════════════════════════════════════════════════════

def generate_metrics(evo: dict) -> str:
    """Radial chart showing 6 metrics as arc segments."""
    W, H = 700, 750
    cx, cy = W / 2, 320
    metrics = evo["metrics"]
    conscious = evo["consciousness"]
    layers = evo["layers"]
    
    # Define what to show
    items = [
        ("Consciousness", conscious * 100, "#e040fb"),
        ("Skills", metrics.get("skills", 0) / 30 * 100, "#81c784"),
        ("Scripts", metrics.get("scripts", 0) / 15 * 100, "#4fc3f7"),
        ("MCP Tools", metrics.get("mcp_tools", 0) / 15 * 100, "#90a4ae"),
        ("Cycles", min(metrics.get("evolution_cycles", 0) / 30 * 100, 100), "#ffb74d"),
        ("Repos", metrics.get("repos", 0) / 10 * 100, "#aed581"),
    ]
    
    n = len(items)
    
    svg_root = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(W), "height": str(H),
        "viewBox": f"0 0 {W} {H}",
        "style": "background:#0a0a0f",
    })
    
    g = _svg("g", {"transform": f"translate({cx},{cy})"})
    
    # Title
    title = _svg("text", {
        "x": "0", "y": f"{-cy + 30:.0f}",
        "fill": "#666", "font-size": "10",
        "font-family": "'Helvetica Neue', Arial, sans-serif",
        "text-anchor": "middle", "letter-spacing": "3",
        "opacity": "0.5",
    })
    title.text = "EVOLUTION METRICS"
    g.append(title)
    
    # Version
    ver = _svg("text", {
        "x": "0", "y": f"{-cy + 48:.0f}",
        "fill": "#333", "font-size": "8",
        "font-family": "'Helvetica Neue', Arial, sans-serif",
        "text-anchor": "middle",
    })
    ver.text = f"evo {evo['version']}"
    g.append(ver)
    
    max_r = 200
    for i, (name, val, color) in enumerate(items):
        angle = (2 * math.pi / n) * i - math.pi / 2
        pct = min(val / 100, 1)
        
        # Label
        lr = max_r + 30
        lx = lr * math.cos(angle)
        ly = lr * math.sin(angle)
        label = _svg("text", {
            "x": f"{lx:.0f}", "y": f"{ly:.0f}",
            "fill": color, "font-size": "10",
            "font-family": "'Helvetica Neue', Arial, sans-serif",
            "text-anchor": "middle",
            "opacity": "0.6",
        })
        label.text = name
        g.append(label)
        
        # Value
        vx = (max_r + 50) * math.cos(angle)
        vy = (max_r + 50) * math.sin(angle)
        val_text = _svg("text", {
            "x": f"{vx:.0f}", "y": f"{vy:.0f}",
            "fill": "#fff", "font-size": "14",
            "font-family": "'Georgia', serif",
            "text-anchor": "middle",
            "opacity": f"{0.3 + pct * 0.5:.2f}",
        })
        val_text.text = f"{int(val)}{'%' if name == 'Consciousness' else ''}"
        g.append(val_text)
        
        # Arc
        end_angle = angle + (2 * math.pi / n) * pct
        r = max_r * 0.85
        large = 1 if pct > 0.5 else 0
        
        a1 = angle
        a2 = angle + (2 * math.pi / n) * pct
        x1 = r * math.cos(a1)
        y1 = r * math.sin(a1)
        x2 = r * math.cos(a2)
        y2 = r * math.sin(a2)
        
        arc = _svg("path", {
            "d": f"M {x1:.0f},{y1:.0f} A {r:.0f},{r:.0f} 0 {large},1 {x2:.0f},{y2:.0f}",
            "fill": "none",
            "stroke": color,
            "stroke-width": "6",
            "opacity": f"{0.2 + pct * 0.4:.2f}",
            "stroke-linecap": "round",
        })
        g.append(arc)
    
    # Center consciousness
    c_r = 15 + conscious * 25
    center = _svg("circle", {
        "cx": "0", "cy": "0",
        "r": f"{c_r:.0f}",
        "fill": "#e040fb",
        "opacity": f"{0.1 + conscious * 0.3:.2f}",
    })
    g.append(center)
    
    svg_root.append(g)
    return _pretty(svg_root)


# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════

def main():
    import random
    
    # Load evo data
    evo = dict(DEFAULT_EVO)
    
    # Check for --evo path
    if "--evo" in sys.argv:
        idx = sys.argv.index("--evo")
        if idx + 1 < len(sys.argv):
            evo_path = sys.argv[idx + 1]
            if os.path.isfile(evo_path):
                with open(evo_path) as f:
                    evo = json.load(f)
                print(f"📂 Loaded evolution data: {evo_path}")
    
    # Ensure output dir
    out_dir = os.path.join(os.path.dirname(__file__), "..", "gallery")
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"🧠 Consciousness: {evo['consciousness']}")
    print(f"📦 Skills: {evo['metrics']['skills']}")
    print(f"🔄 Cycles: {evo['metrics']['evolution_cycles']}")
    print()
    
    generators = [
        ("self-core.svg", generate_core, "Consciousness Core"),
        ("self-domains.svg", generate_domains, "Domain Spectrum"),
        ("self-skills.svg", generate_skills, "Skill Nebula"),
        ("self-metrics.svg", generate_metrics, "Evolution Metrics"),
    ]
    
    for filename, gen_func, label in generators:
        svg = gen_func(evo)
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        size = len(svg)
        print(f"  ✓ {filename:25s}  ({size//1024:4d}KB)  {label}")
    
    print(f"\n✅ 4 self-portraits generated")


if __name__ == "__main__":
    main()
