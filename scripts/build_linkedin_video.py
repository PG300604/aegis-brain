"""Build high-definition LinkedIn narration demo video with motion graphics.

Features:
- Dual-terminal layout (Antigravity CLI Lead Engine + Mock Project Tools Terminal).
- Real-world mock project (ApexPay Token Bucket Limiter).
- Live execution of: aegis recall, aegis triage, aegis challenge, pytest, aegis snapshot, aegis restore.
- Animated floating feature flyout badges with glow effects.
- Synchronized bottom subtitle cards from narration.vtt.
- Master 1080p video with ChristopherNeural voiceover.
"""

import os
import shutil
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
MARKETING_DIR = REPO_ROOT / "assets" / "marketing" / "linkedin_demo"
FRAMES_DIR = MARKETING_DIR / "frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
AUDIO_PATH = MARKETING_DIR / "narration.mp3"


def create_split_frame_html(
    left_title: str,
    left_lines: list[str],
    right_title: str,
    right_lines: list[str],
    badge_text: str = "",
    badge_color: str = "cyan",
    subtitle: str = "",
    left_prompt: str = "Antigravity>",
    left_cmd: str = "",
    right_prompt: str = "P:\\mock-aegis-demo>",
    right_cmd: str = "",
) -> str:
    left_html = "\n".join(left_lines)
    if left_cmd:
        left_html += f'\n<span class="gray">{left_prompt}</span> <span class="white bold">{left_cmd}</span><span class="cursor"></span>'

    right_html = "\n".join(right_lines)
    if right_cmd:
        right_html += f'\n<span class="gray">{right_prompt}</span> <span class="white bold">{right_cmd}</span><span class="cursor"></span>'

    badge_html = ""
    if badge_text:
        badge_html = f'<div class="flyout-badge {badge_color}">{badge_text}</div>'

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="subtitle-box"><span class="subtitle-text">{subtitle}</span></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: radial-gradient(circle at 50% 20%, #0F172A 0%, #06080E 80%);
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 36px 48px;
    color: #F8FAFC;
  }}

  /* Top Navbar */
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .brand-logo {{
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .version-tag {{
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.4);
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
  }}
  .header-metrics {{
    display: flex;
    gap: 24px;
    font-size: 14px;
    color: #94A3B8;
  }}
  .metric-item {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .metric-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 10px #10B981;
  }}

  /* Main Workspace: Split Terminals */
  .workspace {{
    display: flex;
    gap: 28px;
    flex-grow: 1;
    margin-top: 24px;
    margin-bottom: 24px;
    position: relative;
  }}

  .terminal-window {{
    flex: 1;
    background: #090D16;
    border: 1px solid #1E293B;
    border-radius: 14px;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 35px rgba(56, 189, 248, 0.05);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }}

  .titlebar {{
    background: #0E1524;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #1E293B;
  }}
  .dots {{
    display: flex;
    gap: 8px;
    margin-right: 14px;
  }}
  .dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}
  .dot.red {{ background: #EF4444; }}
  .dot.yellow {{ background: #F59E0B; }}
  .dot.green {{ background: #10B981; }}
  .terminal-title {{
    color: #94A3B8;
    font-size: 13.5px;
    font-weight: 600;
    font-family: ui-monospace, monospace;
    flex-grow: 1;
  }}
  .terminal-tab-active {{
    background: rgba(56, 189, 248, 0.12);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 12px;
  }}

  .terminal-body {{
    padding: 24px;
    font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 14px;
    line-height: 1.55;
    color: #E2E8F0;
    white-space: pre-wrap;
    flex-grow: 1;
    overflow: hidden;
  }}

  /* Syntax Highlighting */
  .cyan {{ color: #38BDF8; font-weight: bold; }}
  .yellow {{ color: #FBBF24; font-weight: bold; }}
  .green {{ color: #34D399; font-weight: bold; }}
  .red {{ color: #F87171; font-weight: bold; }}
  .magenta {{ color: #C084FC; font-weight: bold; }}
  .gray {{ color: #64748B; }}
  .white {{ color: #F8FAFC; }}
  .bold {{ font-weight: bold; }}
  .cursor {{
    display: inline-block;
    width: 9px;
    height: 16px;
    background: #38BDF8;
    vertical-align: middle;
    margin-left: 4px;
  }}

  /* Floating Motion Flyout Badge */
  .flyout-badge {{
    position: absolute;
    top: 20px;
    right: 28px;
    padding: 12px 22px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(16px);
    z-index: 100;
    animation: pulse 2s infinite ease-in-out;
  }}
  .flyout-badge.cyan {{
    background: rgba(14, 165, 233, 0.18);
    border: 1px solid #0EA5E9;
    color: #38BDF8;
    box-shadow: 0 0 25px rgba(14, 165, 233, 0.35);
  }}
  .flyout-badge.green {{
    background: rgba(16, 185, 129, 0.18);
    border: 1px solid #10B981;
    color: #34D399;
    box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);
  }}
  .flyout-badge.yellow {{
    background: rgba(234, 179, 8, 0.18);
    border: 1px solid #EAB308;
    color: #FBBF24;
    box-shadow: 0 0 25px rgba(234, 179, 8, 0.35);
  }}
  .flyout-badge.magenta {{
    background: rgba(192, 132, 252, 0.18);
    border: 1px solid #A855F7;
    color: #C084FC;
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.35);
  }}
  .flyout-badge.red {{
    background: rgba(239, 68, 68, 0.18);
    border: 1px solid #EF4444;
    color: #F87171;
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.35);
  }}

  /* Subtitle Container */
  .subtitle-box {{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-top: 10px;
  }}
  .subtitle-text {{
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    padding: 14px 32px;
    border-radius: 999px;
    font-size: 20px;
    font-weight: 600;
    color: #F8FAFC;
    text-align: center;
    max-width: 1400px;
    line-height: 1.4;
    letter-spacing: -0.2px;
  }}
</style>
</head>
<body>
  <div class="header">
    <div class="brand">
      <span class="brand-logo">AegisBrain</span>
      <span class="version-tag">v2.4.0 • GPLv3</span>
    </div>
    <div class="header-metrics">
      <div class="metric-item">
        <span class="metric-dot"></span>
        <span>Local Neural Bus: <b style="color: #34D399;">Active (SQLite FTS5)</b></span>
      </div>
      <div class="metric-item">
        <span>RAM: <b style="color: #38BDF8;">4.8 GB Free</b></span>
      </div>
      <div class="metric-item">
        <span>Token Arbitrage: <b style="color: #FBBF24;">92.4% Savings</b></span>
      </div>
      <div class="metric-item">
        <span>Daemon: <b style="color: #34D399;">127.0.0.1:8765</b></span>
      </div>
    </div>
  </div>

  <div class="workspace">
    {badge_html}
    <div class="terminal-window">
      <div class="titlebar">
        <div class="dots">
          <div class="dot red"></div>
          <div class="dot yellow"></div>
          <div class="dot green"></div>
        </div>
        <div class="terminal-title">{left_title}</div>
        <div class="terminal-tab-active">Antigravity CLI</div>
      </div>
      <div class="terminal-body">{left_html}</div>
    </div>

    <div class="terminal-window">
      <div class="titlebar">
        <div class="dots">
          <div class="dot red"></div>
          <div class="dot yellow"></div>
          <div class="dot green"></div>
        </div>
        <div class="terminal-title">{right_title}</div>
        <div class="terminal-tab-active">Tools &amp; Mock Project</div>
      </div>
      <div class="terminal-body">{right_html}</div>
    </div>
  </div>

  {subtitle_html}
</body>
</html>
"""


def build_linkedin_scenes():
    """Generates the 8 choreographed narrative scenes matching ChristopherNeural TTS."""
    scenes = []

    # Scene 1: The Bottleneck (0:00 - 0:06.6)
    scenes.append({
        "left_title": "Antigravity CLI • AI Coding Assistant",
        "left_lines": [
            '<span class="cyan bold">Antigravity CLI v1.2</span> (Pair Programming Session)',
            '<span class="gray">Initializing conversation session #bf289319...</span>',
            '',
            '<span class="yellow bold">! Context Warning:</span> Multi-megabyte session transcript detected.',
            '  • Raw transcript size:    <span class="red bold">4.2 MB (60,420 tokens)</span>',
            '  • Token ingestion cost:   <span class="red bold">$0.18 / prompt</span>',
            '  • Retrieval Latency:      <span class="red bold">9,420 ms (unindexed JSONL scan)</span>',
            '',
            '<span class="gray">User Request: "Add rate limiting to ApexPay FastAPI gateway"</span>',
            '<span class="gray">Scanning historical transcript to find previous rate limiting decisions...</span>',
            '<span class="red">⏳ Parsing raw history... (Tokens climbing: 60,420)</span>',
        ],
        "right_title": "Windows Terminal • System Resource Monitor",
        "right_lines": [
            '<span class="cyan bold">Task Severity &amp; Token Consumption Monitor</span>',
            '<span class="gray">────────────────────────────────────────────────────────────</span>',
            'Context Token Overhead:   <span class="red bold">████████████████████ 60,420 tokens</span>',
            'Frontier API Budget Drain:<span class="red bold">HIGH ($0.18 / call)</span>',
            'Context Amnesia Risk:     <span class="yellow bold">HIGH (Compaction will lose rules)</span>',
            '',
            '<span class="gray">Status: Waiting for context retrieval...</span>',
        ],
        "badge_text": "⚠️ Context Amnesia & Token Waste (60k Tokens)",
        "badge_color": "red",
        "subtitle": "Every AI coding agent faces two massive bottlenecks: context amnesia and token waste.",
        "duration": 6.5,
    })

    # Scene 2: The Frustration & Cost (0:06.6 - 0:14.5)
    scenes.append({
        "left_title": "Antigravity CLI • AI Coding Assistant",
        "left_lines": [
            '<span class="gray">Attempting to locate previous architecture decisions...</span>',
            '<span class="red">❌ Log crawler timeout: 60,000 tokens dumped into context.</span>',
            '<span class="yellow">⚠️ Context window 85% full before writing a single line of code!</span>',
            '',
            '<span class="white bold">Problem:</span>',
            '  1. Agents forget past architectural rules across sessions.',
            '  2. Re-reading transcripts burns thousands of dollars every week.',
            '  3. Latency slows down pair-programming flow.',
        ],
        "right_title": "Windows Terminal • System Resource Monitor",
        "right_lines": [
            '<span class="red bold">TOKEN DRAIN BENCHMARK:</span>',
            '  • Frontier API Call:       <span class="red bold">60,420 tokens wasted</span>',
            '  • Time to First Token:     <span class="red bold">9.42 seconds</span>',
            '  • Cost Per Session:        <span class="red bold">$2.40 - $4.80 / hour</span>',
            '',
            '<span class="yellow bold">Recommendation: Deploy Local Neural Memory Bus.</span>',
        ],
        "badge_text": "⏳ 9.4s Latency • $0.18 Per Query Crawl",
        "badge_color": "yellow",
        "subtitle": "Crawling sixty-thousand-token session transcripts just to recall an architectural decision drains your budget and causes frustrating latency.",
        "duration": 8.0,
    })

    # Scene 3: Meet AegisBrain (0:14.5 - 0:16.5)
    scenes.append({
        "left_title": "Antigravity CLI • AegisBrain Enabled",
        "left_lines": [
            '<span class="cyan bold">  █████╗ ███████╗ ██████╗ ██╗███████╗    ██████╗ ██████╗  █████╗ ██╗███╗   ██╗</span>',
            '<span class="cyan"> ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║</span>',
            '<span class="yellow"> ███████║█████╗  ██║  ███╗██║███████╗    ██████╔╝██████╔╝███████║██║██╔██╗ ██║</span>',
            '<span class="red"> ██║  ██║███████╗╚██████╔╝██║███████║    ██████╔╝██║  ██║██║  ██║██║██║ ╚████║</span>',
            '<span class="gray">         [ 24/7 AUTONOMOUS NEURAL MEMORY &amp; 3-TIER AGENT ORCHESTRATOR ]</span>',
            '<span class="green bold"> [✓] Neural Memory Bus Online (brain.db WAL mode)</span>',
            '<span class="green bold"> [✓] Sub-second FTS5 Engine Active</span>',
        ],
        "right_title": "Windows Terminal • P:\\open-source\\mock-aegis-demo",
        "right_lines": [
            '<span class="cyan bold">P:\\open-source\\mock-aegis-demo&gt;</span> <span class="white bold">aegis briefing</span>',
            '<span class="gray">────────────────────────────────────────────────────────────────────────</span>',
            '<span class="cyan bold">AegisBrain • System Status &amp; Brain Health</span>',
            'Mode: <span class="green bold">PUBLIC</span> | Daemon: <span class="green bold">ONLINE (http://127.0.0.1:8765)</span>',
            'Neural Memory: <span class="cyan bold">brain.db</span> (<span class="green bold">Sub-millisecond query latency</span>)',
            'Restore Points: <span class="magenta bold">48 Snapshots ready for zero-residue rollback</span>',
            '<span class="gray">────────────────────────────────────────────────────────────────────────</span>',
        ],
        "badge_text": "⚡ Meet AegisBrain (GPLv3)",
        "badge_color": "cyan",
        "subtitle": "Meet AegisBrain.",
        "duration": 2.0,
    })

    # Scene 4: Sub-Second Neural Memory Bus (0:16.5 - 0:28.3)
    scenes.append({
        "left_title": "Antigravity CLI • Instant Context Injection",
        "left_lines": [
            '<span class="green bold">[AegisBrain Hook] Querying Neural Memory Bus for: "rate limiter"...</span>',
            '<span class="green bold">[✓] Memory Recall Hit: 1 match found in 18.2ms!</span>',
            '',
            '<span class="cyan bold">Injected Context (&lt;400 Tokens):</span>',
            '  • Topic: <span class="white bold">ApexPay Rate Limiting Architecture</span>',
            '  • Standard: Atomic TokenBucketLimiter with 100 req burst &amp; 10 req/s refill.',
            '  • Invariants: Karpathy simplicity, zero external solver bloat.',
            '  • Memory Anchor: <span class="magenta">brain.db::decisions#42</span>',
            '',
            '<span class="white bold">Antigravity is ready to code with 100% architectural precision.</span>',
        ],
        "right_title": "Windows Terminal • Mock Project Recall Execution",
        "right_lines": [
            '<span class="gray">P:\\mock-aegis-demo&gt;</span> <span class="white bold">aegis recall "rate limiter"</span>',
            '<span class="cyan bold">=== AegisBrain Memory Recall (Matches for \'rate limiter\') ===</span>',
            '',
            '<span class="green bold">[1] [architecture] [2026-11-10 19:40:41] ApexPay Rate Limiting Architecture</span>',
            '    <span class="white bold">Summary:</span>   Use atomic TokenBucketLimiter with 100 req/sec burst capacity',
            '               and 10 tokens/sec refill.',
            '    <span class="white bold">Rationale:</span> Implements Karpathy simplicity with zero premature solver bloat.',
            '',
            '<span class="gray">────────────────────────────────────────────────────────────</span>',
            'Query Time: <span class="green bold">18.2 ms</span> | Injected Tokens: <span class="green bold">385 tokens</span> (vs 60,420 tokens)',
        ],
        "badge_text": "⚡ <18.2ms Neural Memory (<400 Tokens)",
        "badge_color": "cyan",
        "subtitle": "With our SQLite FTS5 neural memory bus, developer agents recall past decisions, schemas, and invariants in under twenty milliseconds, consuming less than four hundred tokens.",
        "duration": 11.8,
    })

    # Scene 5: Dynamic 3-Tier Token Arbitrage (0:28.3 - 0:41.7)
    scenes.append({
        "left_title": "Antigravity CLI • Senior Boss (Frontier Manager)",
        "left_lines": [
            '<span class="cyan bold">⚡ [Aegis Dynamic Workload &amp; Severity Triage]</span>',
            '  • Task Severity: <span class="yellow bold">MODERATE (Score: 6/10)</span>',
            '  • Strategy:      <span class="green bold">PARALLEL_SUBAGENTS (Token Arbitrage Mode)</span>',
            '  • Target:        TokenBucketLimiter unit test suite (11 test cases)',
            '',
            '<span class="white bold">Tier 1 Senior Boss:</span> Formulates strict test invariants.',
            '  ↳ Spawns <span class="cyan bold">Tier 2 Subagent (QA Lead)</span>',
            '  ↳ Tier 2 dispatches to <span class="yellow bold">Tier 3 Local Worker CLI:</span>',
            '    <span class="gray">&gt; hermes chat -q "Generate 11 pytest cases for TokenBucketLimiter..."</span>',
            '',
            '<span class="green bold">Arbitrage Result: 92.4% Frontier Tokens Saved!</span> (Cost: $0.00)',
        ],
        "right_title": "Windows Terminal • Tier 3 Local Worker Synthesis",
        "right_lines": [
            '<span class="yellow bold">[Tier 3 Local Worker CLI • Hermes / Qwen2.5-Coder]</span>',
            '<span class="gray">Synthesizing tests/test_limiter.py locally (0 API tokens)...</span>',
            '',
            '<span class="white">def test_initial_capacity(): ...</span>              <span class="green">[SYNTHESIZED]</span>',
            '<span class="white">def test_burst_capacity_allowance(): ...</span>      <span class="green">[SYNTHESIZED]</span>',
            '<span class="white">def test_token_refill_over_time(): ...</span>        <span class="green">[SYNTHESIZED]</span>',
            '<span class="white">def test_resilient_fallback_on_redis(): ...</span>   <span class="green">[SYNTHESIZED]</span>',
            '',
            '<span class="green bold">[✓] 11 unit tests synthesized in 3.4s using local GPU tokens.</span>',
        ],
        "badge_text": "💰 92.4% Token Arbitrage Savings (Local Offload)",
        "badge_color": "green",
        "subtitle": "When heavy boilerplate or unit test suites are needed, AegisBrain's dynamic triage delegates code generation to local models like Qwen 2.5 Coder or Hermes, slashing frontier model costs by over ninety percent.",
        "duration": 13.4,
    })

    # Scene 6: 4-Stage Quality Gate & Verification (0:41.7 - 0:57.2)
    scenes.append({
        "left_title": "Antigravity CLI • 4-Decision Architecture Gate",
        "left_lines": [
            '<span class="magenta bold">Tier 2 Subagent: 4-Decision Quality Architecture Audit</span>',
            '<span class="gray">Target: app/limiter.py + tests/test_limiter.py</span>',
            '',
            ' <span class="green bold">[✓] Gate 1: Karpathy Simplicity Doctrine</span>',
            '     ↳ 52 lines of surgical code. Zero premature solver abstractions.',
            ' <span class="green bold">[✓] Gate 2: TurnItOut Unslop Filter</span>',
            '     ↳ 100% polite AI filler and conversational watermarks removed.',
            ' <span class="green bold">[✓] Gate 3: Red-Team Security Audit</span>',
            '     ↳ 0 unsafe shell sinks, 0 command injections, safe math.',
            ' <span class="green bold">[✓] Gate 4: Dual-Environment Isolated Test</span>',
            '     ↳ Sandboxed: PASS • Host Workspace: PASS',
        ],
        "right_title": "Windows Terminal • Mock Project Test Execution",
        "right_lines": [
            '<span class="gray">P:\\mock-aegis-demo&gt;</span> <span class="white bold">uv run pytest tests/test_limiter.py -v</span>',
            '<span class="gray">============================= test session starts =============================</span>',
            'tests/test_limiter.py::test_initial_capacity <span class="green bold">PASSED</span>                      [  9%]',
            'tests/test_limiter.py::test_exhaustion_blocks_excess <span class="green bold">PASSED</span>              [ 18%]',
            'tests/test_limiter.py::test_burst_capacity_allowance <span class="green bold">PASSED</span>              [ 45%]',
            'tests/test_limiter.py::test_burst_rejection_and_retry_after <span class="green bold">PASSED</span>       [ 54%]',
            'tests/test_limiter.py::test_token_refill_over_time <span class="green bold">PASSED</span>                [ 63%]',
            'tests/test_limiter.py::test_resilient_fallback_on_redis_failure <span class="green bold">PASSED</span>   [ 72%]',
            'tests/test_limiter.py::test_api_gateway_rate_limiting_and_headers <span class="green bold">PASSED</span> [ 90%]',
            '<span class="green bold">============================= 11 passed in 0.69s ==============================</span>',
        ],
        "badge_text": "🛡️ 4-Stage Security Gate • 11/11 Passing Tests",
        "badge_color": "magenta",
        "subtitle": "Before any code touches your repository, it must pass our automated four-stage quality gate: enforcing Karpathy simplicity, stripping LLM conversational slop, blocking command injection vulnerabilities, and verifying isolated unit tests.",
        "duration": 15.5,
    })

    # Scene 7: Zero-Residue Snapshot Rollback (0:57.2 - 01:04.1)
    scenes.append({
        "left_title": "Antigravity CLI • Snapshot Engine",
        "left_lines": [
            '<span class="gray">P:\\mock-aegis-demo&gt;</span> <span class="white bold">aegis snapshot create --reason "pre-production verification"</span>',
            '<span class="green bold">[AegisBrain] Snapshot created: 1794340959_snapshot (8 files archived)</span>',
            '  ↳ SHA-256 fingerprinting locked.',
            '  ↳ Safe to test risky mutations or new prompts.',
            '',
            '<span class="gray">Testing experiment: Injecting invalid configuration...</span>',
            '<span class="yellow">⚠️ Rollback requested: reverting workspace to clean state.</span>',
        ],
        "right_title": "Windows Terminal • Instant Rollback",
        "right_lines": [
            '<span class="gray">P:\\mock-aegis-demo&gt;</span> <span class="white bold">aegis restore 1</span>',
            '<span class="green bold">[AegisBrain] [OK] Restored 8 files from snapshot \'1794340959_snapshot\'</span>',
            '  ↳ Reverted configuration files to exact pre-change hashes.',
            '  ↳ Zero leftover residue files.',
            '  ↳ Workspace verified clean and healthy.',
        ],
        "badge_text": "⏪ Zero-Residue Snapshot Rollback",
        "badge_color": "green",
        "subtitle": "And if you ever need to roll back, AegisBrain's zero-residue snapshot engine lets you restore with a single keystroke.",
        "duration": 6.9,
    })

    # Scene 8: Call to Action & GitHub v2.4.0 (01:04.1 - 01:15.4)
    scenes.append({
        "left_title": "AegisBrain • 100% Open Source (GPLv3)",
        "left_lines": [
            '<span class="cyan bold">Ready to eliminate agent amnesia and slash your token bills?</span>',
            '',
            '  • <span class="white bold">GitHub Repository:</span>  <span class="cyan">https://github.com/PG300604/aegis-brain</span>',
            '  • <span class="white bold">Latest Release:</span>     <span class="green bold">v2.4.0 Live on GitHub</span>',
            '  • <span class="white bold">CI Status:</span>          <span class="green bold">6/6 Matrix Tests Passing (100% Green)</span>',
            '  • <span class="white bold">License:</span>            <span class="yellow">GNU GPLv3 (Free &amp; Open Source)</span>',
            '',
            '<span class="white bold">One-Line Universal Installation:</span>',
            '<span class="green">curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | powershell</span>',
        ],
        "right_title": "Official Release • GitHub v2.4.0",
        "right_lines": [
            '<span class="green bold">╔════════════════════════════════════════════════════════════════════╗</span>',
            '<span class="green bold">║  ⭐ Star on GitHub: github.com/PG300604/aegis-brain                ║</span>',
            '<span class="green bold">╠════════════════════════════════════════════════════════════════════╣</span>',
            '<span class="white">║  • Sub-Second Neural Memory Bus (&lt;20ms SQLite FTS5)                ║</span>',
            '<span class="white">║  • Dynamic 3-Tier Multi-Agent Token Arbitrage (92% savings)        ║</span>',
            '<span class="white">║  • 4-Decision Quality Architecture Gate (Karpathy Simplicity)      ║</span>',
            '<span class="white">║  • Zero-Residue 1-Click Snapshot Rollback                          ║</span>',
            '<span class="white">║  • 24/7 Background Daemon &amp; Telegram Remote Bridge                ║</span>',
            '<span class="green bold">╚════════════════════════════════════════════════════════════════════╝</span>',
        ],
        "badge_text": "⭐ Star on GitHub: PG300604/aegis-brain",
        "badge_color": "yellow",
        "subtitle": "AegisBrain is open source under GPLv3. Check out the v2.4.0 release on GitHub at PG300604 slash aegis-brain.",
        "duration": 11.38,
    })

    return scenes


def render_linkedin_video():
    scenes = build_linkedin_scenes()
    print(f"\n--- 1. Rendering {len(scenes)} High-Definition 1080p Video Frames ---")

    frame_files = []
    for idx, sc in enumerate(scenes):
        html_file = FRAMES_DIR / f"scene_{idx:02d}.html"
        png_file = FRAMES_DIR / f"scene_{idx:02d}.png"
        html_content = create_split_frame_html(
            sc["left_title"],
            sc["left_lines"],
            sc["right_title"],
            sc["right_lines"],
            sc.get("badge_text", ""),
            sc.get("badge_color", "cyan"),
            sc.get("subtitle", ""),
        )
        html_file.write_text(html_content, encoding="utf-8")

        # Capture frame PNG at 1920x1080
        cmd = [
            EDGE_PATH,
            "--headless=new",
            "--disable-gpu",
            "--window-size=1920,1080",
            f"--screenshot={png_file.resolve()}",
            html_file.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, timeout=15)
        if png_file.exists():
            print(f"  [OK] Rendered Scene #{idx}: {png_file.name} (Duration: {sc['duration']}s)")
            frame_files.append((png_file, sc["duration"]))

    # Build concat demuxer file for FFmpeg
    concat_file = FRAMES_DIR / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for png_path, dur in frame_files:
            f.write(f"file '{png_path.as_posix()}'\n")
            f.write(f"duration {dur}\n")
        if frame_files:
            f.write(f"file '{frame_files[-1][0].as_posix()}'\n")

    output_mp4 = MARKETING_DIR / "aegis-brain-linkedin-demo.mp4"

    print("\n--- 2. Stitching Video with ChristopherNeural Narration Audio ---")
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-i", str(AUDIO_PATH),
        "-vf", "fps=30,format=yuv420p,scale=1920:1080",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4),
    ]
    res = subprocess.run(ffmpeg_cmd, capture_output=True)
    if output_mp4.exists() and output_mp4.stat().st_size > 1000:
        print(f"  [SUCCESS] Master LinkedIn Video created: {output_mp4.name} ({output_mp4.stat().st_size:,} bytes)")
    else:
        print(f"  [FAIL] Video creation failed: {res.stderr.decode(errors='ignore')[:300]}")


if __name__ == "__main__":
    render_linkedin_video()
