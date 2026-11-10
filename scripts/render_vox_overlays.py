"""Render authentic Vox-style documentary evidence overlays (Huashu Art Motion Y2 Vox).

Design elements from huashu-art-motion/references/动画语法/y2_vox.md:
- Editorial tape badge: dark label (#171716) with crimson dot (#B8433F) and white monospace text
- Yellow highlighter line (rgba(218, 207, 8, 0.55)) with multiply blending
- Hand-drawn red marker loop (#B8433F) circling key numbers and verification passes
- Index evidence note card with torn edge, monospace metrics, and subtitle descriptions
- Zero AI neon slop: authentic investigative documentary aesthetic
"""

import subprocess
from pathlib import Path

OUT_DIR = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/master_edit/vox_overlays")
OUT_DIR.mkdir(parents=True, exist_ok=True)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SEGMENTS_VOX = [
    {
        "id": "vox_seg01",
        "tag": "DOC 01 · CONTEXT BOOTSTRAP",
        "metric": "< 400 TOKENS",
        "desc": "Autonomous session boot vs 60k token raw log crawl",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg02",
        "tag": "DOC 02 · ZERO-UI PRE-FLIGHT",
        "metric": "18.2ms INGESTION",
        "desc": "Active session radar, restore point #1 and priorities loaded",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg03",
        "tag": "DOC 03 · SQLITE FTS5 RECALL",
        "metric": "18.2ms vs 60,420 TOKENS",
        "desc": "Retrieves verified rate limiter invariants with zero token crawl",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg04",
        "tag": "DOC 04 · TOKEN ARBITRAGE HIERARCHY",
        "metric": "92.4% TOKENS SAVED",
        "desc": "Tier 1 Boss delegates boilerplate to Tier 3 Hermes CLI on local GPU",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg05",
        "tag": "DOC 05 · 4-STAGE ARCHITECTURE GATE",
        "metric": "FLAW COACHED & FIXED",
        "desc": "Caught Lua float precision issue • 100% Unslop & Karpathy simplicity",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg06",
        "tag": "DOC 06 · TEST & AST SECURITY",
        "metric": "11/11 PASSED (0.72s)",
        "desc": "All unit tests pass • AST security scanner certifies 0 secrets",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg07",
        "tag": "DOC 07 · STANDALONE TERMINAL SUITE",
        "metric": "VERIFIED_SOUND",
        "desc": "aegis recall & aegis challenge truth-seeking AST audit in PowerShell",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg08",
        "tag": "DOC 08 · CRYPTO SNAPSHOT ROLLBACK",
        "metric": "8 FILES RESTORED",
        "desc": "1-click snapshot restore rolls back workspace with zero residual dirt",
        "hl_box": None,
        "red_loop": None,
    },
    {
        "id": "vox_seg09",
        "tag": "DOC 09 · MORNING RADAR BRIEFING",
        "metric": "18.2ms DASHBOARD",
        "desc": "Complete morning briefing table: completed tasks, news radar & priorities",
        "hl_box": None,
        "red_loop": None,
    },
]

def render_vox_html(item):
    hl_html = ""
    if item["hl_box"]:
        b = item["hl_box"]
        hl_html = f"""<div style='position: absolute; left: {b["x"]}px; top: {b["y"]}px; width: {b["w"]}px; height: {b["h"]}px; background: rgba(218, 207, 8, 0.40); mix-blend-mode: multiply; border-radius: 3px; pointer-events: none;'></div>"""

    loop_html = ""
    if item["red_loop"]:
        l = item["red_loop"]
        loop_html = f"""<div style='position: absolute; left: {l["x"]}px; top: {l["y"]}px; width: {l["w"]}px; height: {l["h"]}px; border: 3.5px solid #B8433F; border-radius: 52% 48% 50% 48% / 46% 54% 46% 54%; transform: rotate(-1.5deg); pointer-events: none; box-shadow: 0 0 3px rgba(184, 67, 63, 0.4);'></div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1920px;
    height: 1080px;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    position: relative;
    overflow: hidden;
  }}

  /* Vox Tape Badge in top-left corner */
  .tape-badge {{
    position: absolute;
    top: 40px;
    left: 48px;
    background: #171716;
    color: #EEEDED;
    padding: 9px 20px;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    gap: 10px;
    border-radius: 2px;
  }}
  .tape-dot {{
    width: 8px;
    height: 8px;
    background: #B8433F;
    border-radius: 50%;
  }}

  /* Top Right Status Pill */
  .status-tag {{
    position: absolute;
    top: 40px;
    right: 48px;
    background: #F6F4EE;
    color: #171716;
    border: 1px solid #D8D4C8;
    padding: 8px 18px;
    border-radius: 4px;
    font-family: ui-monospace, monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3);
  }}

  /* Bottom-Right Evidence Index Card */
  .note-card {{
    position: absolute;
    bottom: 64px;
    right: 55px;
    background: #F6F4EE;
    color: #171716;
    border-left: 4px solid #B8433F;
    padding: 14px 22px;
    border-radius: 4px;
    font-family: ui-monospace, monospace;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    max-width: 440px;
  }}
  .note-num {{
    font-size: 22px;
    font-weight: 900;
    color: #B8433F;
    margin-bottom: 3px;
    letter-spacing: -0.5px;
  }}
  .note-sub {{
    font-size: 11px;
    color: #4B5563;
    font-weight: 600;
    line-height: 1.4;
  }}
</style>
</head>
<body>
  <div class='tape-badge'>
    <div class='tape-dot'></div>
    <span>{item['tag']}</span>
  </div>

  <div class='status-tag'>
    <span>EVIDENCE VERIFIED · AEGIS-BRAIN</span>
  </div>

  {hl_html}
  {loop_html}

  <div class='note-card'>
    <div class='note-num'>{item['metric']}</div>
    <div class='note-sub'>{item['desc']}</div>
  </div>
</body>
</html>"""

def render_all_vox():
    print("--- Rendering All 9 Vox Documentary Evidence Overlays ---")
    for v in SEGMENTS_VOX:
        html = render_vox_html(v)
        html_file = OUT_DIR / f"{v['id']}.html"
        html_file.write_text(html, encoding="utf-8")
        png_file = OUT_DIR / f"{v['id']}.png"

        cmd = [
            EDGE_PATH,
            "--headless",
            "--disable-gpu",
            f"--screenshot={png_file}",
            "--window-size=1920,1080",
            "--default-background-color=00000000",
            str(html_file.as_uri())
        ]
        res = subprocess.run(cmd, capture_output=True)
        if png_file.exists() and png_file.stat().st_size > 1000:
            print(f"  [OK] Rendered {png_file.name}: {png_file.stat().st_size:,} bytes")
        else:
            print(f"  [FAIL] Failed {png_file.name}: {res.stderr.decode(errors='ignore')[:200]}")

if __name__ == "__main__":
    render_all_vox()
