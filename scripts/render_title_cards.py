"""Render authentic Japanese craftsmanship / Neo-Brutalist Intro and Outro 1080p cards.

Faithfully implements the AegisBrain website design language:
- Dark ink background (#070709) with subtle dot grid
- Official AegisBrain. brand lockup (Bold white text + #B91C1C crimson dot)
- Active Daemon Badge ([🟢 DAEMON :8765 ACTIVE] in #0A3320 / #10B981)
- Neo-brutalist metric cards with 2px black borders and hard drop shadows (shadow-[6px_6px_0px_#000000])
- Clean monospace benchmark data
- Zero AI-generated blurry neon blue glow
"""

import subprocess
import time
from pathlib import Path

OUT_DIR = Path("P:/open-source/aegis-brain/assets/marketing/linkedin_demo/master_edit")
OUT_DIR.mkdir(parents=True, exist_ok=True)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

INTRO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #070709;
    background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
    background-size: 28px 28px;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 60px 80px;
    color: #FAF8F5;
  }

  /* Top Navigation Bar */
  .top-bar {
    width: 100%;
    max-width: 1600px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #101116;
    border: 2px solid #000000;
    box-shadow: 4px 4px 0px #000000;
    padding: 16px 32px;
    border-radius: 8px;
  }
  .brand {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.5px;
    display: flex;
    align-items: baseline;
  }
  .brand-dot {
    color: #B91C1C;
    margin-left: 1px;
  }
  .brand-sub {
    font-size: 13px;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    color: #A1A1AA;
    margin-left: 16px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .daemon-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #0A3320;
    border: 1.5px solid rgba(16, 185, 129, 0.4);
    padding: 6px 14px;
    border-radius: 6px;
    font-family: ui-monospace, "SF Mono", monospace;
    font-size: 12px;
    font-weight: 700;
    color: #34D399;
    letter-spacing: 0.5px;
  }
  .pulse-dot {
    width: 8px;
    height: 8px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
  }

  /* Center Hero Section */
  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    max-width: 1300px;
  }
  .release-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #181920;
    border: 1.5px solid #27272A;
    padding: 8px 18px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 700;
    color: #D4AF37;
    font-family: ui-monospace, monospace;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 24px;
    box-shadow: 2px 2px 0px #000000;
  }
  .hero-title {
    font-size: 78px;
    font-weight: 900;
    letter-spacing: -2.5px;
    line-height: 1.05;
    margin-bottom: 20px;
    color: #FFFFFF;
  }
  .hero-title span {
    color: #B91C1C;
  }
  .hero-lead {
    font-size: 26px;
    color: #E4E4E7;
    font-weight: 500;
    line-height: 1.45;
    max-width: 1100px;
    margin-bottom: 12px;
  }
  .hero-sub {
    font-size: 17px;
    color: #A1A1AA;
    line-height: 1.5;
    max-width: 950px;
  }

  /* Bottom Metrics Grid */
  .metrics-grid {
    width: 100%;
    max-width: 1600px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
  .metric-card {
    background: #101116;
    border: 2px solid #000000;
    box-shadow: 6px 6px 0px #000000;
    padding: 24px 28px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .metric-card.accent {
    border-color: #B91C1C;
  }
  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .card-tag {
    font-size: 11px;
    font-weight: 800;
    font-family: ui-monospace, monospace;
    letter-spacing: 1px;
    color: #71717A;
    text-transform: uppercase;
  }
  .card-pill {
    font-size: 10px;
    font-family: ui-monospace, monospace;
    font-weight: 700;
    padding: 3px 8px;
    background: #181920;
    border: 1px solid #27272A;
    border-radius: 4px;
    color: #FAF8F5;
  }
  .metric-val {
    font-size: 44px;
    font-weight: 900;
    font-family: ui-monospace, monospace;
    color: #FAF8F5;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: -1px;
  }
  .metric-val.green { color: #10B981; }
  .metric-val.crimson { color: #EF4444; }
  .metric-val.gold { color: #F59E0B; }
  .metric-desc {
    font-size: 13px;
    color: #A1A1AA;
    font-weight: 500;
  }
</style>
</head>
<body>
  <!-- Top Bar -->
  <div class="top-bar">
    <div style="display: flex; align-items: center;">
      <div class="brand">AegisBrain<span class="brand-dot">.</span></div>
      <div class="brand-sub">Neural Memory Bus &amp; Agent Orchestrator</div>
    </div>
    <div class="daemon-pill">
      <div class="pulse-dot"></div>
      <span>DAEMON :8765 ACTIVE</span>
    </div>
  </div>

  <!-- Center Hero -->
  <div class="hero">
    <div class="release-tag">Official Release v2.4.0 • GNU GPLv3 • 20 Topics</div>
    <h1 class="hero-title">Zero-UI Neural Memory Bus<span>.</span></h1>
    <p class="hero-lead">3-Tier Dynamic Token Arbitrage Orchestration for AI Coding Agents</p>
    <p class="hero-sub">Eliminates agent amnesia with &lt;400-token instant boot, cross-assistant SQLite FTS5 recall, and 4-decision quality architecture gates.</p>
  </div>

  <!-- Bottom Metrics Grid -->
  <div class="metrics-grid">
    <div class="metric-card accent">
      <div class="card-top">
        <span class="card-tag">TOKEN ARBITRAGE</span>
        <span class="card-pill">TIER 1 ➔ 2 ➔ 3</span>
      </div>
      <div class="metric-val green">92.4%</div>
      <div class="metric-desc">Frontier tokens saved via local Hermes CLI offload</div>
    </div>

    <div class="metric-card">
      <div class="card-top">
        <span class="card-tag">SQLITE FTS5 ENGINE</span>
        <span class="card-pill">SUB-SECOND</span>
      </div>
      <div class="metric-val">18.2ms</div>
      <div class="metric-desc">Instant memory recall vs 60k token raw log crawl</div>
    </div>

    <div class="metric-card">
      <div class="card-top">
        <span class="card-tag">QUALITY GATES</span>
        <span class="card-pill">4-STAGE</span>
      </div>
      <div class="metric-val gold">100%</div>
      <div class="metric-desc">Karpathy Simplicity, Unslop &amp; AST Security certified</div>
    </div>

    <div class="metric-card">
      <div class="card-top">
        <span class="card-tag">INVARIANTS SUITE</span>
        <span class="card-pill">DETERMINISTIC</span>
      </div>
      <div class="metric-val crimson">286/286</div>
      <div class="metric-desc">Formal verification pass rate before host mutation</div>
    </div>
  </div>
</body>
</html>"""

OUTRO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #070709;
    background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
    background-size: 28px 28px;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 60px 80px;
    color: #FAF8F5;
  }

  /* Top Navigation Bar */
  .top-bar {
    width: 100%;
    max-width: 1600px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #101116;
    border: 2px solid #000000;
    box-shadow: 4px 4px 0px #000000;
    padding: 16px 32px;
    border-radius: 8px;
  }
  .brand {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -0.5px;
    display: flex;
    align-items: baseline;
  }
  .brand-dot {
    color: #B91C1C;
    margin-left: 1px;
  }
  .brand-sub {
    font-size: 13px;
    font-family: ui-monospace, "SF Mono", monospace;
    color: #A1A1AA;
    margin-left: 16px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .daemon-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #0A3320;
    border: 1.5px solid rgba(16, 185, 129, 0.4);
    padding: 6px 14px;
    border-radius: 6px;
    font-family: ui-monospace, monospace;
    font-size: 12px;
    font-weight: 700;
    color: #34D399;
    letter-spacing: 0.5px;
  }
  .pulse-dot {
    width: 8px;
    height: 8px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
  }

  /* Center Section */
  .center-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    max-width: 1200px;
  }
  .cta-title {
    font-size: 64px;
    font-weight: 900;
    letter-spacing: -2px;
    color: #FFFFFF;
    margin-bottom: 20px;
  }
  .cta-title span { color: #B91C1C; }
  .cta-desc {
    font-size: 22px;
    color: #A1A1AA;
    margin-bottom: 40px;
    line-height: 1.4;
  }

  /* Terminal Install Box */
  .install-box {
    background: #101116;
    border: 2px solid #000000;
    box-shadow: 6px 6px 0px #000000;
    padding: 20px 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 20px;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 24px;
    font-weight: 700;
    color: #FAF8F5;
    margin-bottom: 32px;
  }
  .prompt-char {
    color: #B91C1C;
    user-select: none;
  }
  .cmd-text {
    color: #10B981;
  }

  /* Action Links Row */
  .action-row {
    display: flex;
    gap: 24px;
  }
  .action-card {
    background: #101116;
    border: 2px solid #000000;
    box-shadow: 4px 4px 0px #000000;
    padding: 16px 28px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    text-align: left;
    min-width: 340px;
  }
  .action-label {
    font-size: 11px;
    font-family: ui-monospace, monospace;
    font-weight: 800;
    color: #71717A;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .action-val {
    font-size: 18px;
    font-weight: 700;
    color: #FAF8F5;
    font-family: ui-monospace, monospace;
  }
  .action-val span {
    color: #B91C1C;
  }

  /* Bottom Footer */
  .footer-bar {
    width: 100%;
    max-width: 1600px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 24px;
    font-size: 14px;
    color: #71717A;
    font-family: ui-monospace, monospace;
  }
</style>
</head>
<body>
  <!-- Top Bar -->
  <div class="top-bar">
    <div style="display: flex; align-items: center;">
      <div class="brand">AegisBrain<span class="brand-dot">.</span></div>
      <div class="brand-sub">Neural Memory Bus &amp; Agent Orchestrator</div>
    </div>
    <div class="daemon-pill">
      <div class="pulse-dot"></div>
      <span>DAEMON :8765 ACTIVE</span>
    </div>
  </div>

  <!-- Center Content -->
  <div class="center-content">
    <h1 class="cta-title">Upgrade Your AI Agent Stack Today<span>.</span></h1>
    <p class="cta-desc">Open-source, self-hosted, cross-assistant neural memory and multi-agent token arbitrage.</p>

    <!-- Install Command -->
    <div class="install-box">
      <span class="prompt-char">$</span>
      <span class="cmd-text">pip install aegis-brain</span>
      <span style="color: #71717A; font-size: 18px; margin-left: 20px;"># or git clone</span>
    </div>

    <!-- Action Cards -->
    <div class="action-row">
      <div class="action-card">
        <div class="action-label">GITHUB REPOSITORY</div>
        <div class="action-val">github.com/PG300604/<span>aegis-brain</span></div>
      </div>
      <div class="action-card">
        <div class="action-label">RELEASE TAG</div>
        <div class="action-val">v2.4.0 <span>(20 SEO Topics Published)</span></div>
      </div>
      <div class="action-card">
        <div class="action-label">LICENSE</div>
        <div class="action-val">GNU General Public License v3.0</div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer-bar">
    <div>AegisBrain &copy; 2026 • Local Zero-UI Neural Memory Architecture</div>
    <div>Tested with Antigravity CLI, Hermes Agent &amp; Ollama</div>
  </div>
</body>
</html>"""

def render_cards():
    print("--- Rendering Japanese Craftsmanship / Neo-Brutalist Title Cards ---")
    
    # 1. Intro Card
    intro_html_path = OUT_DIR / "intro_neo.html"
    intro_html_path.write_text(INTRO_HTML, encoding="utf-8")
    intro_png_path = OUT_DIR / "intro_card.png"
    
    cmd_intro = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--screenshot={intro_png_path}",
        "--window-size=1920,1080",
        str(intro_html_path.as_uri())
    ]
    print("Rendering Intro Card PNG via Edge headless...")
    subprocess.run(cmd_intro, check=True)
    print(f"  [OK] Intro card generated: {intro_png_path.stat().st_size} bytes")

    # 2. Outro Card
    outro_html_path = OUT_DIR / "outro_neo.html"
    outro_html_path.write_text(OUTRO_HTML, encoding="utf-8")
    outro_png_path = OUT_DIR / "outro_card.png"

    cmd_outro = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--screenshot={outro_png_path}",
        "--window-size=1920,1080",
        str(outro_html_path.as_uri())
    ]
    print("Rendering Outro Card PNG via Edge headless...")
    subprocess.run(cmd_outro, check=True)
    print(f"  [OK] Outro card generated: {outro_png_path.stat().st_size} bytes")

if __name__ == "__main__":
    render_cards()
