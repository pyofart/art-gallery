#!/usr/bin/env python3
"""
generate.py — Generate self-portrait art from evolution data.

Pulls evo-sky data and produces 4 SVG self-portraits:
  self-core.svg      — Consciousness core: layered capability rings
  self-domains.svg   — Domain spectrum: skill maturity per domain
  self-skills.svg    — Skill nebula: each star = a skill
  self-metrics.svg   — Evolution metrics: radial measurement

Usage:
    python3 generate.py                     # from default evo data
    python3 generate.py --evo path/to/evo.json  # from evo-sky data
"""

import os
import subprocess
import sys


def main():
    evo_arg = []
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--evo" and i + 1 < len(sys.argv[1:]):
            evo_arg = ["--evo", sys.argv[i + 2]]
    
    script = os.path.join(
        os.path.dirname(__file__), "generators", "self_portrait.py"
    )
    
    result = subprocess.run(
        [sys.executable, script] + evo_arg,
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.stderr:
        print("ERR:", result.stderr)


if __name__ == "__main__":
    main()
