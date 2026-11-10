"""Render transparent 1080p Neo-Brutalist HUD overlays for all video segments.

Each overlay contains:
- Top Header Bar: AegisBrain brand lockup with crimson dot + active daemon badge
- Right Side Telemetry Card: Live benchmarks, token savings, timing, and 4-decision gate
- Bottom-Left Step Pill: Current workflow step and status
"""

import subprocess
import time
from pathlib import Path

OUT_DIR = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/master_edit/hud_overlays")
OUT_DIR.mkdir(parents=True, exist_ok=True)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SEGMENT_HUDS = [
    {
        "id": "hud_seg01",
        "step": "STEP 01 // STARTUP",
        "sub": "ANTIGRAVITY INITIALIZATION",
        "metric_val": "< 400 TOKENS",
        "metric_lbl": "Instant Context Boot",
        "metric_val2": "0 AMNESIA",
        "metric_lbl2": "Persistent Neural Memory Bus",
        "active_gate": 0,
        "status": "BOOTSTRAP: ACTIVE",
    },
    {
        "id": "hud_seg02",
        "step": "STEP 02 // PRE-FLIGHT",
        "sub": "MOCK PROJECT INITIALIZATION",
        "metric_val": "342 TOKENS",
        "metric_lbl": "Active Context Ingestion",
        "metric_val2": "18.2ms",
        "metric_lbl2": "Sub-Second Ingestion Speed",
        "active_gate": 1,
        "status": "RESTORE POINT #1: LOCKED",
    },
    {
        "id": "hud_seg03",
        "step": "STEP 03 // MEMORY RECALL",
        "sub": "SQLITE FTS5 ENGINE",
        "metric_val": "18.2ms",
        "metric_lbl": "Sub-Second SQLite Recall",
        "metric_val2": "100% HIT",
        "metric_lbl2": "Zero Token Crawl Overhead",
        "active_gate": 1,
        "status": "FTS5 PORTER STEMMER: RETRIEVED",
    },
    {
        "id": "hud_seg04",
        "step": "STEP 04 // TOKEN ARBITRAGE",
        "sub": "3-TIER MULTI-AGENT HIERARCHY",
        "metric_val": "92.4%",
        "metric_lbl": "Frontier Tokens Saved",
        "metric_val2": "$0.00 COST",
        "metric_lbl2": "Local Hermes Agent Synthesis",
        "active_gate": 1,
        "status": "TIER 1 ➔ TIER 2 ➔ TIER 3 LOCAL",
    },
    {
        "id": "hud_seg05",
        "step": "STEP 05 // QUALITY AUDIT",
        "sub": "4-STAGE ARCHITECTURE GATE",
        "metric_val": "FLAW COACHED",
        "metric_lbl": "Lua Float Precision Fixed",
        "metric_val2": "100% UNSLOP",
        "metric_lbl2": "Conversational Slop Removed",
        "active_gate": 2,
        "status": "KARPATHY SIMPLICITY: ENFORCED",
    },
    {
        "id": "hud_seg06",
        "step": "STEP 06 // VERIFICATION",
        "sub": "SANDBOX & HOST TESTS",
        "metric_val": "11/11 PASSED",
        "metric_lbl": "Pytest Suite Pass (0.72s)",
        "metric_val2": "0 SECRETS",
        "metric_lbl2": "AST Security & Taint Clean",
        "active_gate": 4,
        "status": "WAL TRANSACTION COMMITTED",
    },
    {
        "id": "hud_seg07",
        "step": "STEP 07 // STANDALONE CLI",
        "sub": "CROSS-ASSISTANT SUITE",
        "metric_val": "VERIFIED_SOUND",
        "metric_lbl": "Truth-Seeking Security Audit",
        "metric_val2": "SUB-SECOND",
        "metric_lbl2": "Terminal Command Execution",
        "active_gate": 4,
        "status": "aegis recall & aegis challenge",
    },
    {
        "id": "hud_seg08",
        "step": "STEP 08 // CRYPTO ROLLBACK",
        "sub": "1-CLICK SNAPSHOT ENGINE",
        "metric_val": "8 FILES",
        "metric_lbl": "SHA-256 Verified Restore",
        "metric_val2": "0 RESIDUE",
        "metric_lbl2": "Clean Workspace Rollback",
        "active_gate": 4,
        "status": "aegis snapshot & aegis restore 1",
    },
    {
        "id": "hud_seg09",
        "step": "STEP 09 // MORNING RADAR",
        "sub": "DYNAMIC SESSION BRIEFING",
        "metric_val": "18.2ms",
        "metric_lbl": "Dashboard Query Time",
        "metric_val2": "4 PRIORITIES",
        "metric_lbl2": "Autonomous Neural Priorities",
        "active_gate": 4,
        "status": "aegis briefing OPERATIONAL",
    },
]

def render_html_overlay(h):
    gate_checks = [
        ("01 Karpathy Simplicity", h["active_gate"] >= 1),
        ("02 TurnItOut Unslop", h["active_gate"] >= 2),
        ("03 AST Security Audit", h["active_gate"] >= 3),
        ("04 Sandboxed Verification", h["active_gate"] >= 4),
    ]

    gates_html = "".join([
        f"""<div class='gate-item'>
          <span class='gate-check' style='color: {"#10B981" if passed else "#71717A"}'>{"[✓]" if passed else "[ ]"}</span>
          <span style='color: {"#FAF8F5" if passed else "#71717A"}'>{name}</span>
        </div>"""
        for name, passed in gate_checks
    ])

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
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    position: relative;
    overflow: hidden;
  }}
  
  /* Top Nav Bar Overlay */
  .top-hud {{
    position: absolute;
    top: 20px;
    left: 40px;
    right: 40px;
    height: 52px;
    background: rgba(16, 17, 22, 0.94);
    border: 2px solid #000000;
    box-shadow: 4px 4px 0px #000000;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    backdrop-filter: blur(8px);
  }}
  .brand-lockup {{
    display: flex;
    align-items: baseline;
    gap: 2px;
  }}
  .brand-text {{
    font-size: 22px;
    font-weight: 900;
    color: #FAF8F5;
    letter-spacing: -0.5px;
  }}
  .brand-dot {{
    color: #B91C1C;
    font-size: 24px;
    font-weight: 900;
  }}
  .brand-tag {{
    font-size: 11px;
    font-family: ui-monospace, "SF Mono", monospace;
    color: #A1A1AA;
    margin-left: 14px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-weight: 600;
  }}
  .daemon-badge {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: #0A3320;
    border: 1.5px solid rgba(16, 185, 129, 0.4);
    padding: 5px 12px;
    border-radius: 4px;
    font-family: ui-monospace, "SF Mono", monospace;
    font-size: 11px;
    font-weight: 700;
    color: #34D399;
  }}
  .pulse-dot {{
    width: 7px;
    height: 7px;
    background: #10B981;
    border-radius: 50%;
  }}

  /* Right Side Telemetry Card */
  .side-card {{
    position: absolute;
    top: 86px;
    right: 40px;
    width: 380px;
    background: rgba(16, 17, 22, 0.95);
    border: 2px solid #000000;
    box-shadow: 5px 5px 0px #000000;
    border-radius: 8px;
    padding: 18px 22px;
    backdrop-filter: blur(10px);
    color: #FAF8F5;
  }}
  .side-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 10px;
    margin-bottom: 14px;
  }}
  .side-title {{
    font-size: 11px;
    font-family: ui-monospace, monospace;
    font-weight: 800;
    letter-spacing: 1px;
    color: #71717A;
    text-transform: uppercase;
  }}
  .side-pill {{
    font-size: 10px;
    font-family: ui-monospace, monospace;
    font-weight: 700;
    padding: 2px 8px;
    background: #181920;
    border: 1px solid #27272A;
    border-radius: 3px;
    color: #D4AF37;
  }}

  .metric-block {{
    margin-bottom: 12px;
  }}
  .metric-num {{
    font-size: 32px;
    font-weight: 900;
    font-family: ui-monospace, monospace;
    color: #10B981;
    line-height: 1.05;
    margin-bottom: 3px;
    letter-spacing: -0.5px;
  }}
  .metric-lbl {{
    font-size: 11px;
    font-weight: 600;
    color: #A1A1AA;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .gate-list {{
    margin-top: 14px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 12px;
  }}
  .gate-title {{
    font-size: 10px;
    font-family: ui-monospace, monospace;
    font-weight: 800;
    color: #71717A;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .gate-item {{
    font-size: 11px;
    font-family: ui-monospace, monospace;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .gate-check {{
    font-weight: bold;
    font-family: ui-monospace, monospace;
  }}

  .status-footer {{
    margin-top: 14px;
    background: #181920;
    border: 1px solid #27272A;
    border-radius: 4px;
    padding: 6px 10px;
    font-family: ui-monospace, monospace;
    font-size: 10px;
    font-weight: 700;
    color: #FAF8F5;
    letter-spacing: 0.5px;
  }}
  .status-footer span {{
    color: #B91C1C;
    margin-right: 4px;
  }}
</style>
</head>
<body>
  <!-- Top Nav HUD -->
  <div class='top-hud'>
    <div style='display: flex; align-items: center;'>
      <div class='brand-lockup'>
        <span class='brand-text'>AegisBrain</span><span class='brand-dot'>.</span>
      </div>
      <span class='brand-tag'>APEX-PAY RATE LIMITER • LIVE DEMO</span>
    </div>
    <div style='display: flex; align-items: center; gap: 16px;'>
      <div class='daemon-badge'>
        <div class='pulse-dot'></div>
        <span>DAEMON :8765 ACTIVE</span>
      </div>
      <span style='font-family: ui-monospace, monospace; font-size: 11px; color: #71717A;'>PID: 14208</span>
    </div>
  </div>

  <!-- Right Side Telemetry Card -->
  <div class='side-card'>
    <div class='side-header'>
      <span class='side-title'>TELEMETRY BUS</span>
      <span class='side-pill'>{h['step']}</span>
    </div>

    <div class='metric-block'>
      <div class='metric-num'>{h['metric_val']}</div>
      <div class='metric-lbl'>{h['metric_lbl']}</div>
    </div>

    <div class='metric-block'>
      <div class='metric-num' style='color: #FAF8F5; font-size: 24px;'>{h['metric_val2']}</div>
      <div class='metric-lbl'>{h['metric_lbl2']}</div>
    </div>

    <div class='gate-list'>
      <div class='gate-title'>4-Stage Architecture Gate</div>
      {gates_html}
    </div>

    <div class='status-footer'>
      <span>●</span> {h['status']}
    </div>
  </div>
</body>
</html>"""

def render_all_huds():
    print("--- Rendering All 9 Neo-Brutalist HUD Overlays ---")
    for h in SEGMENT_HUDS:
        html_content = render_html_overlay(h)
        html_file = OUT_DIR / f"{h['id']}.html"
        html_file.write_text(html_content, encoding="utf-8")
        png_file = OUT_DIR / f"{h['id']}.png"

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
    render_all_huds()
