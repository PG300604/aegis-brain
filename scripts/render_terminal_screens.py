"""Generate crisp terminal screenshots and simulation frames for AegisBrain."""

import html
import subprocess
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
MARKETING_DIR = REPO_ROOT / "assets" / "marketing"
TEMPLATES_DIR = REPO_ROOT / "scratch" / "terminal_templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def create_terminal_html(title: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #090B0E;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    padding: 24px;
  }}
  .window {{
    width: 1080px;
    background: #0D1117;
    border-radius: 12px;
    border: 1px solid #30363D;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 40px rgba(56, 189, 248, 0.08);
    overflow: hidden;
  }}
  .titlebar {{
    background: #161B22;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #30363D;
  }}
  .dots {{
    display: flex;
    gap: 8px;
    margin-right: 16px;
  }}
  .dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}
  .dot.red {{ background: #FF5F56; }}
  .dot.yellow {{ background: #FFBD2E; }}
  .dot.green {{ background: #27C93F; }}
  .window-title {{
    color: #8B949E;
    font-size: 13px;
    font-weight: 500;
    flex-grow: 1;
    text-align: center;
    padding-right: 50px;
  }}
  .terminal-body {{
    padding: 24px 28px;
    color: #E6EDF3;
    font-size: 13.5px;
    line-height: 1.55;
    white-space: pre;
  }}
  .cyan {{ color: #38BDF8; font-weight: bold; }}
  .yellow {{ color: #FBBF24; font-weight: bold; }}
  .green {{ color: #34D399; font-weight: bold; }}
  .red {{ color: #F87171; font-weight: bold; }}
  .magenta {{ color: #C084FC; font-weight: bold; }}
  .gray {{ color: #6E7681; }}
  .white {{ color: #F0F6FC; }}
  .bold {{ font-weight: bold; }}
  .box-border {{ color: #0EA5E9; }}
  .box-border-yellow {{ color: #EAB308; }}
  .box-border-magenta {{ color: #A855F7; }}
  .box-border-green {{ color: #10B981; }}
  .pill {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
  }}
  .pill-green {{ background: #064E3B; color: #34D399; border: 1px solid #059669; }}
  .pill-cyan {{ background: #0C4A6E; color: #38BDF8; border: 1px solid #0284C7; }}
  .pill-yellow {{ background: #713F12; color: #FDE047; border: 1px solid #CA8A04; }}
  .cursor {{
    display: inline-block;
    width: 8px;
    height: 15px;
    background: #38BDF8;
    vertical-align: middle;
    animation: blink 1s infinite;
  }}
  @keyframes blink {{
    0%, 49% {{ opacity: 1; }}
    50%, 100% {{ opacity: 0; }}
  }}
</style>
</head>
<body>
  <div class="window">
    <div class="titlebar">
      <div class="dots">
        <div class="dot red"></div>
        <div class="dot yellow"></div>
        <div class="dot green"></div>
      </div>
      <div class="window-title">{title}</div>
    </div>
    <div class="terminal-body">{body_html}</div>
  </div>
</body>
</html>
"""


def generate_screens():
    # Screen 1: Node.js Style Colored Installer
    screen1_content = """<span class="gray">PS C:\\Users\\priya&gt;</span> <span class="white bold">curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | powershell</span>

<span class="cyan">  █████╗ ███████╗ ██████╗ ██╗███████╗    ██████╗ ██████╗  █████╗ ██╗███╗   ██╗</span>
<span class="cyan"> ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║</span>
<span class="yellow"> ███████║█████╗  ██║  ███╗██║███████╗    ██████╔╝██████╔╝███████║██║██╔██╗ ██║</span>
<span class="yellow"> ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║</span>
<span class="red"> ██║  ██║███████╗╚██████╔╝██║███████║    ██████╔╝██║  ██║██║  ██║██║██║ ╚████║</span>
<span class="red"> ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝</span>
<span class="gray">         [ 24/7 AUTONOMOUS NEURAL MEMORY & 3-TIER AGENT ORCHESTRATOR ]</span>
<span class="gray">                               Version 2.4.0 (GPLv3)</span>

<span class="box-border">┌────────────────────────────────────────────────────────────────────────┐</span>
<span class="box-border">│</span>  <span class="cyan bold">STEP 1 of 4: License Agreement &amp; Terms of Service</span>                     <span class="box-border">│</span>
<span class="box-border">└────────────────────────────────────────────────────────────────────────┘</span>
<span class="gray">┌────────────────────────────────────────────────────────────────────────┐</span>
<span class="gray">│</span>  License: GNU General Public License v3.0 (GPL-3.0-or-later)           <span class="gray">│</span>
<span class="gray">│</span>  Author: Priyanshu Ghosh (@PG300604) | github.com/PG300604/aegis-brain  <span class="gray">│</span>
<span class="gray">│</span>                                                                        <span class="gray">│</span>
<span class="gray">│</span>  Core Commitments: 100% Local Neural Memory • Zero Exfiltration         <span class="gray">│</span>
<span class="gray">│</span>  Subprocess Boundary: Workers (Hermes/Ollama) execute via isolated OS  <span class="gray">│</span>
<span class="gray">│</span>  Pre-mutation snapshots created automatically before file edits.       <span class="gray">│</span>
<span class="gray">└────────────────────────────────────────────────────────────────────────┘</span>
 <span class="green">[✓] Terms accepted.</span>

<span class="box-border-yellow">┌────────────────────────────────────────────────────────────────────────┐</span>
<span class="box-border-yellow">│</span>  <span class="yellow bold">STEP 2 of 4: Select Agent Execution Strategy</span>                          <span class="box-border-yellow">│</span>
<span class="box-border-yellow">└────────────────────────────────────────────────────────────────────────┘</span>
<span class="gray">┌────────────────────────────────────────────────────────────────────────┐</span>
<span class="gray">│</span>  Choose how Antigravity CLI &amp; AegisBrain should triage coding tasks:   <span class="gray">│</span>
<span class="gray">│</span>                                                                        <span class="gray">│</span>
<span class="gray">│</span>  <span class="white bold">[1] Arbitrage Mode</span> <span class="green bold">(Recommended - 85%+ Token Savings):</span>               <span class="gray">│</span>
<span class="gray">│</span>      Senior Boss serves as Brain only. Delegates substantial tasks to  <span class="gray">│</span>
<span class="gray">│</span>      Tier 2 Subagents + Tier 3 Local Workers (Hermes, Ollama MoE).     <span class="gray">│</span>
<span class="gray">│</span>                                                                        <span class="gray">│</span>
<span class="gray">│</span>  <span class="white bold">[2] Fast Direct Mode:</span>                                                 <span class="gray">│</span>
<span class="gray">│</span>      Frontier Manager writes code directly for rapid prototyping.      <span class="gray">│</span>
<span class="gray">└────────────────────────────────────────────────────────────────────────┘</span>
 <span class="green">[✓] Configured: Dynamic Arbitrage Mode (3-Tier Token Saving)</span>

<span class="box-border-green">┌────────────────────────────────────────────────────────────────────────┐</span>
<span class="box-border-green">│</span>  <span class="green bold">STEP 4 of 4: Installation &amp; Restore Point Reflex</span>                      <span class="box-border-green">│</span>
<span class="box-border-green">└────────────────────────────────────────────────────────────────────────┘</span>
 <span class="cyan">[1/6]</span> Creating automated pre-install restore point snapshot...
       <span class="green">[OK]</span> Snapshot saved: <span class="white">1794302583_pre_install</span> (8 files archived)
 <span class="cyan">[2/6]</span> Initializing local neural memory bus (<span class="white">brain.db</span> WAL mode)...
 <span class="cyan">[3/6]</span> Setting up zero-elevation background autostart daemon (Port 8765)...
 <span class="cyan">[4/6]</span> Registering global '<span class="white bold">aegis</span>' CLI command shim...
 <span class="cyan">[5/6]</span> Auto-linking companion skills across Antigravity, Claude, Codex...
 <span class="cyan">[6/6]</span> Injecting autonomous engineering directives &amp; FTS5 memory hooks...

<span class="green bold">════════════════════════════════════════════════════════════════════════</span>
<span class="green bold"> [✓] AegisBrain v2.4.0 successfully installed and operational!</span>
<span class="green bold">════════════════════════════════════════════════════════════════════════</span>
  • Execution Mode:  <span class="white bold">ARBITRAGE (85%+ Token Savings via 3-Tier Hierarchy)</span>
  • Instant Recall:  <span class="cyan">aegis recall &lt;topic&gt;</span> (&lt;25ms sub-second retrieval)
  • Daemon Status:   <span class="green">http://127.0.0.1:8765/status (24/7 background service)</span>"""

    # Screen 2: 3-Tier Multi-Agent Triage in Action
    screen2_content = """<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis triage "Build distributed JWT token refresh rotation engine with Redis caching"</span>

<span class="cyan bold">⚡ [AegisBrain 3-Tier Dynamic Workload Triage]</span>
  • Incoming Task:        <span class="white">"Build distributed JWT token refresh rotation engine..."</span>
  • Task Severity Score:  <span class="yellow bold">0.82 / 1.0 (High Severity - Architecture + Security)</span>
  • Hardware Headroom:    <span class="green bold">5.38 GB RAM Free • CPU 12% • Thermals Normal</span>
  • Token Cost Forecast:  <span class="magenta bold">~12,400 Frontier Tokens ($0.037) vs 0 Local Tokens ($0.000)</span>
  • Triage Decision:      <span class="green bold">PARALLEL_SUBAGENTS (3-Tier Token Arbitrage Mode)</span>

<span class="box-border">┌────────────────────────────────────────────────────────────────────────┐</span>
<span class="box-border">│</span>  <span class="cyan bold">HIERARCHICAL MULTI-AGENT EXECUTION TRACE</span>                              <span class="box-border">│</span>
<span class="box-border">└────────────────────────────────────────────────────────────────────────┘</span>
 <span class="white bold">Tier 1 Senior Boss (Antigravity Main Brain):</span>
   ↳ Formulates strict invariants &amp; architectural specification (Karpathy Simplicity).
   ↳ Spawns <span class="cyan bold">Tier 2 Junior Boss</span> (`invoke_subagent` -> Security &amp; Auth Subagent).

 <span class="cyan bold">Tier 2 Junior Boss (Security Subagent):</span>
   ↳ Assesses task requirements &amp; drafts worker execution prompt.
   ↳ Dispatches directive to <span class="yellow bold">Tier 3 Execution Worker CLI</span> via `run_command`:
     <span class="gray">&gt; hermes chat -q "Implement JwtRotationService with atomic redis SETNX..."</span>

 <span class="yellow bold">Tier 3 Execution Worker (Hermes CLI / Qwen2.5-Coder):</span>
   ↳ Generating raw candidate draft using 100% local tokens (0 frontier cost)...
   ↳ Produced 148 lines of surgical Python JWT rotation logic &amp; unit tests.

 <span class="magenta bold">Tier 2 Quality Architecture Audit (4-Gate Verification):</span>
   <span class="green">[✓] Gate 1: Karpathy Simplicity Doctrine</span>  - Zero unnecessary layers, 148 lines.
   <span class="green">[✓] Gate 2: Ponytail / TurnItOut Unslop</span>   - All AI conversational watermarks stripped.
   <span class="green">[✓] Gate 3: Red-Team Security Audit</span>       - AST verified: 0 injection sinks, timing-safe compare.
   <span class="green">[✓] Gate 4: Dual-Environment Verification</span> - Isolated sandbox: PASS • Local test: PASS (8/8 tests).

 <span class="white bold">Tier 1 Senior Boss Sign-off:</span>
   ↳ Verified and committed to workspace.
   ↳ Neural memory WAL commit recorded to <span class="white">brain.db</span> in <span class="green bold">18.4ms</span>.
   ↳ <span class="green bold">Token Arbitrage Result: 92.4% Frontier Tokens Saved (12,400 -&gt; 940 tokens)</span>"""

    # Screen 3: aegis briefing
    screen3_content = """<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis briefing</span>

<span class="cyan bold">🛡️  AEGISBRAIN MORNING BRIEFING &amp; COGNITIVE SYNC</span>
<span class="gray">────────────────────────────────────────────────────────────────────────</span>
 <span class="white bold">System Snapshot:</span>        <span class="green">1794302583_pre_install</span> (Verified intact, rollback ready)
 <span class="white bold">Daemon KeepAlive:</span>       <span class="green">ONLINE (http://127.0.0.1:8765) • Uptime: 48h 12m</span>
 <span class="white bold">Hardware Resource:</span>      <span class="green">5.38 GB RAM Free (Healthy) • CPU 8%</span>
 <span class="white bold">Execution Strategy:</span>     <span class="cyan bold">ARBITRAGE MODE (Active)</span>

 <span class="yellow bold">Recent Neural Milestones (from brain.db WAL):</span>
  [1] <span class="white">React 19.3.1 Security Patch:</span> RSC RCE vulnerability patched &amp; deployed to Vercel.
  [2] <span class="white">License Compliance Audit:</span> 100% GPLv3 compliant, zero upstream conflicts.
  [3] <span class="white">Interactive Installer:</span> Node.js-style 4-panel wizard with license acceptance.

 <span class="magenta bold">Community Tech Radar (LocalLLaMA &amp; HackerNews Trends):</span>
  • <span class="white">Qwen 2.5 Coder 32B-Instruct:</span> SOTA local coding model with 128k context.
  • <span class="white">DeepSeek-V3 MoE Architecture:</span> Multi-head latent attention benchmarks released.
  • <span class="white">Hermes-3 Llama-3.1 8B:</span> Uncensored agentic steering tool use standard.

 <span class="cyan bold">Today's Prioritized Directives:</span>
  <span class="green">[1]</span> Promotional launch on r/LocalLLaMA and X with verified empirical benchmarks.
  <span class="green">[2]</span> Distribute terminal demo video &amp; infographic assets to community repositories.
  <span class="green">[3]</span> Verify Telegram Bot listener (@HHAACLIBot) background message ingestion.<span class="cursor"></span>"""

    # Screen 4: aegis recall (sub-25ms FTS5)
    screen4_content = """<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis recall "JWT rotation"</span>

<span class="cyan bold">🔍 [Sub-Second FTS5 Neural Recall]</span>
<span class="gray">Target: "JWT rotation" • Query Engine: SQLite FTS5 Porter Stemmer</span>

<span class="green bold">[Record #1] (Rank: -14.28 • Query Latency: 18.2ms • Cost: 0 Frontier Tokens)</span>
  • Title:      <span class="white bold">Distributed JWT Session Rotation &amp; Redis Setnx Lock</span>
  • Category:   <span class="yellow">ARCHITECTURE / SECURITY</span>
  • Decision:   Rotated tokens using atomic Redis SETNX with 60-second grace period.
  • Invariants: Constant-time HMAC comparison (hmac.compare_digest) to prevent timing attacks.
  • Rationale:  Prevents double-refresh race conditions across multi-node microservices.
  • Code Anchor: <span class="cyan">package/aegis/auth/jwt_rotation.py#L42-L88</span>
  • Tags:       <span class="gray">["jwt", "security", "redis", "token-rotation", "session-vault"]</span>

<span class="green bold">[Record #2] (Rank: -9.14 • Query Latency: 21.0ms)</span>
  • Title:      <span class="white bold">Red-Team Security Gate Audit Checklist</span>
  • Category:   <span class="yellow">SECURITY_AUDIT</span>
  • Decision:   Enforce timing-safe secret comparisons and block unsanitized JWT claims.

<span class="gray">────────────────────────────────────────────────────────────────────────</span>
 <span class="white bold">Benchmark Comparison:</span>
  • <span class="green bold">AegisBrain FTS5 Recall:  18.2 ms (82 tokens injected)</span>
  • Raw JSONL Log Crawling:  9,420 ms (52,400 tokens crawled - 99.8% slower)
  • <span class="cyan bold">Net Savings: 52,318 tokens saved &amp; 517x faster response</span><span class="cursor"></span>"""

    screens = [
        ("screenshot-01-installer.html", "screenshot-01-installer.png", "AegisBrain Universal Installer v2.4.0 (Windows Terminal)", screen1_content, 1140, 780),
        ("screenshot-02-subagent-triage.html", "screenshot-02-subagent-triage.png", "AegisBrain 3-Tier Multi-Agent Workload Triage", screen2_content, 1140, 720),
        ("screenshot-03-briefing.html", "screenshot-03-briefing.png", "AegisBrain Zero-Prompt Autonomous Morning Briefing", screen3_content, 1140, 680),
        ("screenshot-04-fts5-recall.html", "screenshot-04-fts5-recall.png", "AegisBrain Sub-Second Neural Memory Recall (18.2ms)", screen4_content, 1140, 620),
    ]

    print("\n--- 2. Generating Terminal Screens and PNG Screenshots ---")
    for html_name, png_name, title, body, w, h in screens:
        html_file = TEMPLATES_DIR / html_name
        png_file = MARKETING_DIR / png_name
        html_content = create_terminal_html(title, body)
        html_file.write_text(html_content, encoding="utf-8")

        # Capture screenshot with msedge
        cmd = [
            EDGE_PATH,
            "--headless=new",
            "--disable-gpu",
            f"--window-size={w},{h}",
            f"--screenshot={png_file.resolve()}",
            html_file.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=15)
        if png_file.exists():
            print(f"  [OK] Rendered Terminal Screen: {png_name} ({png_file.stat().st_size:,} bytes)")
        else:
            print(f"  [FAIL] Failed: {png_name}")


if __name__ == "__main__":
    generate_screens()
