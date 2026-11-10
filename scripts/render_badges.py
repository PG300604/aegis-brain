"""Render transparent motion graphics badge overlays for the video."""

import subprocess
from pathlib import Path

OUT_DIR = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/master_edit/badges")
OUT_DIR.mkdir(parents=True, exist_ok=True)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

BADGES = [
    {
        "id": "badge_preflight",
        "tag": "⚡ ZERO-UI PRE-FLIGHT",
        "title": "Sub-Second Session Briefing",
        "metric": "< 400 Tokens • 18.2ms Query • 0 Amnesia",
        "color": "cyan",
        "border": "#0EA5E9",
        "glow": "rgba(14, 165, 233, 0.4)",
    },
    {
        "id": "badge_recall",
        "tag": "🧠 SUB-SECOND NEURAL MEMORY",
        "title": "SQLite FTS5 Porter Stemmer",
        "metric": "18.2ms Recall vs 60,420 Token JSONL Crawl",
        "color": "cyan",
        "border": "#0EA5E9",
        "glow": "rgba(14, 165, 233, 0.4)",
    },
    {
        "id": "badge_triad",
        "tag": "🤖 3-TIER MULTI-AGENT HIERARCHY",
        "title": "Dynamic Token Arbitrage Mode",
        "metric": "Tier 1 Manager ➔ Tier 2 Subagent ➔ Tier 3 Hermes CLI",
        "color": "yellow",
        "border": "#EAB308",
        "glow": "rgba(234, 179, 8, 0.4)",
    },
    {
        "id": "badge_quality_gate",
        "tag": "🛡️ 4-STAGE ARCHITECTURE GATE",
        "title": "Karpathy Simplicity & AST Defense",
        "metric": "Zero Over-Engineering • Unslop • Flaw Coaching",
        "color": "purple",
        "border": "#A855F7",
        "glow": "rgba(168, 85, 247, 0.4)",
    },
    {
        "id": "badge_pytest",
        "tag": "✅ 11/11 UNIT TESTS PASSED (0.72s)",
        "title": "Quality Certification & WAL Commit",
        "metric": "92.4% Frontier Tokens Saved ($0.00 Cost)",
        "color": "green",
        "border": "#10B981",
        "glow": "rgba(16, 185, 129, 0.4)",
    },
    {
        "id": "badge_standalone",
        "tag": "🔍 STANDALONE TERMINAL TOOLS",
        "title": "Cross-Assistant Memory & Audit",
        "metric": "aegis recall & aegis challenge (VERIFIED_SOUND)",
        "color": "cyan",
        "border": "#0EA5E9",
        "glow": "rgba(14, 165, 233, 0.4)",
    },
    {
        "id": "badge_rollback",
        "tag": "⏪ ZERO-RESIDUE ROLLBACK",
        "title": "1-Click Snapshot Restore Engine",
        "metric": "Restored 8 Files with SHA-256 Verification",
        "color": "green",
        "border": "#10B981",
        "glow": "rgba(16, 185, 129, 0.4)",
    },
]

def render_badge_html(b):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: transparent;
    width: 650px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  .badge-container {{
    background: rgba(8, 12, 22, 0.92);
    border: 1.5px solid {b['border']};
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 25px {b['glow']};
    backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 16px 24px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: 100%;
  }}
  .badge-tag {{
    font-size: 13px;
    font-weight: 800;
    color: {b['border']};
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}
  .badge-title {{
    font-size: 20px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.3px;
  }}
  .badge-metric {{
    font-size: 14px;
    color: #94A3B8;
    font-weight: 600;
    font-family: ui-monospace, monospace;
  }}
</style>
</head>
<body>
  <div class="badge-container">
    <div class="badge-tag">{b['tag']}</div>
    <div class="badge-title">{b['title']}</div>
    <div class="badge-metric">{b['metric']}</div>
  </div>
</body>
</html>
"""

def generate_all_badges():
    for b in BADGES:
        html_file = OUT_DIR / f"{b['id']}.html"
        png_file = OUT_DIR / f"{b['id']}.png"
        html_file.write_text(render_badge_html(b), encoding="utf-8")
        
        subprocess.run([
            EDGE_PATH,
            "--headless=new",
            "--disable-gpu",
            "--default-background-color=00000000",
            "--window-size=650,140",
            f"--screenshot={png_file.resolve()}",
            html_file.as_uri()
        ], check=True)
        print(f"Generated badge: {png_file.name}")

if __name__ == "__main__":
    generate_all_badges()
