"""Render Explainroo-inspired Explainer Title Cards (Intro and Outro).

Implements Explainroo's editorial / product-launch design principles:
- Clear, confident question-first layout
- High-contrast, clean typography (Inter / SF Pro Display)
- Step progression and big concrete numbers
- Subtle warm studio canvas (#0E0F12) with refined borders (#262833)
- Zero AI neon slop or blurry glowing halos
"""

import subprocess
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
    background-color: #0E0F14;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 70px 100px;
    color: #F4F4F6;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .brand-chip {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #171821;
    border: 1px solid #2B2D3C;
    padding: 10px 22px;
    border-radius: 8px;
  }
  .brand-name {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #FFFFFF;
  }
  .brand-dot {
    color: #E11D48;
  }
  .brand-pill {
    font-size: 11px;
    font-family: ui-monospace, monospace;
    color: #94A3B8;
    background: #232532;
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .release-tag {
    font-family: ui-monospace, monospace;
    font-size: 13px;
    font-weight: 700;
    color: #10B981;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 8px 18px;
    border-radius: 6px;
  }

  /* Center Question Hero */
  .hero-box {
    max-width: 1350px;
  }
  .question-tag {
    font-family: ui-monospace, monospace;
    font-size: 14px;
    font-weight: 800;
    color: #F59E0B;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .hero-heading {
    font-size: 68px;
    font-weight: 900;
    line-height: 1.12;
    letter-spacing: -2px;
    color: #FFFFFF;
    margin-bottom: 24px;
  }
  .hero-heading span {
    color: #E11D48;
  }
  .hero-desc {
    font-size: 24px;
    color: #94A3B8;
    line-height: 1.45;
    max-width: 1100px;
    font-weight: 400;
  }

  /* Bottom Numbers Bar (explainroo bigNumber) */
  .stats-row {
    display: flex;
    gap: 32px;
    border-top: 1px solid #232532;
    padding-top: 40px;
  }
  .stat-card {
    background: #171821;
    border: 1px solid #262835;
    padding: 24px 32px;
    border-radius: 10px;
    flex: 1;
  }
  .stat-num {
    font-size: 42px;
    font-weight: 900;
    font-family: ui-monospace, monospace;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 8px;
  }
  .stat-num.accent { color: #10B981; }
  .stat-num.red { color: #E11D48; }
  .stat-num.amber { color: #F59E0B; }
  .stat-lbl {
    font-size: 14px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
</style>
</head>
<body>
  <!-- Header -->
  <div class="header">
    <div class="brand-chip">
      <span class="brand-name">AegisBrain<span class="brand-dot">.</span></span>
      <span class="brand-pill">Architecture Explainer</span>
    </div>
    <div class="release-tag">Official Release v2.4.0 • GNU GPLv3</div>
  </div>

  <!-- Hero Question -->
  <div class="hero-box">
    <div class="question-tag">▶ The Coding Agent Dilemma</div>
    <h1 class="hero-heading">How do you eliminate agent amnesia and stop burning expensive frontier tokens<span>?</span></h1>
    <p class="hero-desc">Watch how AegisBrain pairs a sub-second SQLite FTS5 memory bus with a 3-tier multi-agent hierarchy to save 92.4% of API tokens on real-world engineering tasks.</p>
  </div>

  <!-- Explainer Big Numbers -->
  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-num accent">92.4%</div>
      <div class="stat-lbl">Token Arbitrage Cost Savings</div>
    </div>
    <div class="stat-card">
      <div class="stat-num amber">18.2ms</div>
      <div class="stat-lbl">SQLite FTS5 Sub-Second Recall</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">&lt; 400</div>
      <div class="stat-lbl">Token Instant Context Boot</div>
    </div>
    <div class="stat-card">
      <div class="stat-num red">286/286</div>
      <div class="stat-lbl">Invariants Passed Deterministically</div>
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
    background-color: #0E0F14;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 70px 100px;
    color: #F4F4F6;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .brand-chip {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #171821;
    border: 1px solid #2B2D3C;
    padding: 10px 22px;
    border-radius: 8px;
  }
  .brand-name {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #FFFFFF;
  }
  .brand-dot { color: #E11D48; }
  .badge-open {
    font-family: ui-monospace, monospace;
    font-size: 13px;
    font-weight: 700;
    color: #10B981;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 8px 18px;
    border-radius: 6px;
  }

  /* Center Content */
  .center-box {
    max-width: 1350px;
  }
  .summary-tag {
    font-family: ui-monospace, monospace;
    font-size: 14px;
    font-weight: 800;
    color: #10B981;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
  }
  .outro-heading {
    font-size: 64px;
    font-weight: 900;
    line-height: 1.15;
    letter-spacing: -2px;
    color: #FFFFFF;
    margin-bottom: 28px;
  }
  .outro-heading span { color: #E11D48; }

  /* Install Terminal Box */
  .cmd-box {
    background: #171821;
    border: 1px solid #2B2D3C;
    padding: 22px 36px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    gap: 20px;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
  }
  .cmd-prompt { color: #E11D48; }
  .cmd-text { color: #10B981; }
  .cmd-comment { color: #64748B; font-size: 18px; margin-left: 16px; }

  /* Takeaways Grid (explainroo takeaways) */
  .takeaways-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  .takeaway-card {
    background: #171821;
    border: 1px solid #262835;
    padding: 20px 24px;
    border-radius: 8px;
  }
  .takeaway-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 8px;
  }
  .check-icon {
    color: #10B981;
    font-weight: 900;
    font-size: 18px;
  }
  .takeaway-desc {
    font-size: 13px;
    color: #94A3B8;
    line-height: 1.45;
  }

  /* Footer */
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #232532;
    padding-top: 24px;
    font-size: 14px;
    color: #64748B;
    font-family: ui-monospace, monospace;
  }
  .footer a {
    color: #F4F4F6;
    text-decoration: none;
    font-weight: bold;
  }
  .footer a span { color: #E11D48; }
</style>
</head>
<body>
  <!-- Header -->
  <div class="header">
    <div class="brand-chip">
      <span class="brand-name">AegisBrain<span class="brand-dot">.</span></span>
      <span class="brand-pill">Open Source</span>
    </div>
    <div class="badge-open">Free &amp; Open Source • GNU GPLv3</div>
  </div>

  <!-- Center Content -->
  <div class="center-box">
    <div class="summary-tag">✓ Ready For Production</div>
    <h1 class="outro-heading">Add Neural Memory &amp; Token Arbitrage to Your Coding Agents<span>.</span></h1>

    <!-- Terminal Command -->
    <div class="cmd-box">
      <span class="cmd-prompt">$</span>
      <span class="cmd-text">pip install aegis-brain</span>
      <span class="cmd-comment"># works with Antigravity, Hermes &amp; Ollama</span>
    </div>

    <!-- 3 Takeaway Cards -->
    <div class="takeaways-grid">
      <div class="takeaway-card">
        <div class="takeaway-header"><span class="check-icon">✓</span> Zero-UI Neural Memory</div>
        <div class="takeaway-desc">SQLite FTS5 Porter Stemmer delivers sub-second recall (&lt;18.2ms) without multi-megabyte JSONL crawls.</div>
      </div>
      <div class="takeaway-card">
        <div class="takeaway-header"><span class="check-icon">✓</span> 3-Tier Multi-Agent Triad</div>
        <div class="takeaway-desc">Frontier Manager dictates strict invariants while local GPU workers synthesize code at 0 API cost.</div>
      </div>
      <div class="takeaway-card">
        <div class="takeaway-header"><span class="check-icon">✓</span> 4-Decision Quality Gates</div>
        <div class="takeaway-desc">Enforces Karpathy Simplicity, scrubs conversational slop, and guarantees 100% AST security.</div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <div>GitHub: <a href="https://github.com/PG300604/aegis-brain">github.com/PG300604/<span>aegis-brain</span></a></div>
    <div>Official Release: <strong>v2.4.0 (20 Topics Configured)</strong></div>
  </div>
</body>
</html>"""

def render_explainroo_cards():
    print("--- Rendering Explainroo-Style Explainer Title Cards ---")
    
    # 1. Intro Card
    intro_html_path = OUT_DIR / "intro_explainroo.html"
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
    print("Rendering Explainroo Intro Card PNG...")
    subprocess.run(cmd_intro, check=True)
    print(f"  [OK] Intro card generated: {intro_png_path.stat().st_size:,} bytes")

    # 2. Outro Card
    outro_html_path = OUT_DIR / "outro_explainroo.html"
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
    print("Rendering Explainroo Outro Card PNG...")
    subprocess.run(cmd_outro, check=True)
    print(f"  [OK] Outro card generated: {outro_png_path.stat().st_size:,} bytes")

if __name__ == "__main__":
    render_explainroo_cards()
