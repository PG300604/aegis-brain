"""Render marketing screenshots, high-res PNG infographics, terminal screens,
and generate a high-frame-rate terminal demo video using FFmpeg.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
ASSETS_DIR = REPO_ROOT / "assets"
MARKETING_DIR = ASSETS_DIR / "marketing"
MARKETING_DIR.mkdir(parents=True, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def capture_screenshot(source_path: Path, output_png: Path, width: int = 1280, height: int = 800) -> bool:
    """Uses headless Edge to render an SVG or HTML file into a high-res PNG screenshot."""
    url = source_path.as_uri()
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={output_png.resolve()}",
        url,
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=15)
        if output_png.exists() and output_png.stat().st_size > 1000:
            print(f"  [OK] Rendered: {output_png.name} ({output_png.stat().st_size:,} bytes)")
            return True
        else:
            print(f"  [FAIL] Failed to generate {output_png.name}: {res.stderr.decode(errors='ignore')[:200]}")
            return False
    except Exception as exc:
        print(f"  [ERR] {output_png.name}: {exc}")
        return False


def render_all_svg_infographics():
    print("\n--- 1. Rendering SVG Infographics & Benchmark Cards to PNG ---")
    svgs = [
        ("infographic-speed-benchmarks.svg", "infographic-speed-benchmarks.png", 1120, 680),
        ("infographic-unified-architecture.svg", "infographic-unified-architecture.png", 1120, 800),
        ("infographic-hierarchy-pyramid.svg", "infographic-hierarchy-pyramid.png", 1120, 720),
        ("infographic-quality-gate.svg", "infographic-quality-gate.png", 1120, 720),
        ("infographic-universal-agents.svg", "infographic-universal-agents.png", 1120, 720),
        ("infographic-learning-curve.svg", "infographic-learning-curve.png", 1120, 700),
        ("benchmarks-visual.svg", "benchmarks-visual.png", 1120, 560),
        ("universal-agent-matrix.svg", "universal-agent-matrix.png", 1120, 720),
    ]

    for svg_name, png_name, w, h in svgs:
        src = ASSETS_DIR / svg_name
        if src.exists():
            dest = MARKETING_DIR / png_name
            capture_screenshot(src, dest, w, h)
        else:
            print(f"  [SKIP] Missing source: {svg_name}")


if __name__ == "__main__":
    render_all_svg_infographics()
