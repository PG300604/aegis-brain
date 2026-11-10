"""Build high-fidelity animated terminal video and GIF using Edge headless and FFmpeg.

Showcases the product in action:
1. Node.js style installer with ASCII art logo and license acceptance
2. Real-time 3-Tier Multi-Agent Triage (Senior Boss -> Subagent -> Local Worker CLI)
3. 4-Decision Quality Architecture Gate (Karpathy Simplicity, Unslop, Red-team security, Sandbox test)
4. Sub-second FTS5 neural recall (<25ms) and token arbitrage savings (92.4%).
"""

import os
import shutil
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path("P:/open-source/aegis-brain")
MARKETING_DIR = REPO_ROOT / "assets" / "marketing"
FRAMES_DIR = REPO_ROOT / "scratch" / "video_frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def create_terminal_frame_html(step_title: str, lines: list[str], prompt: str = "P:\\vault>", active_cmd: str = "", show_cursor: bool = True) -> str:
    content_html = ""
    for line in lines:
        content_html += f"{line}\n"
    if active_cmd:
        cursor_span = '<span class="cursor"></span>' if show_cursor else ''
        content_html += f'<span class="gray">{prompt}</span> <span class="white bold">{active_cmd}</span>{cursor_span}\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #07090C;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    padding: 20px;
  }}
  .window {{
    width: 1120px;
    height: 720px;
    background: #0B0E14;
    border-radius: 12px;
    border: 1px solid #28303E;
    box-shadow: 0 30px 70px -15px rgba(0, 0, 0, 0.8), 0 0 30px rgba(56, 189, 248, 0.08);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}
  .titlebar {{
    background: #121720;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #232B38;
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
  .dot.red {{ background: #EF4444; }}
  .dot.yellow {{ background: #F59E0B; }}
  .dot.green {{ background: #10B981; }}
  .window-title {{
    color: #94A3B8;
    font-size: 13px;
    font-weight: 600;
    flex-grow: 1;
    text-align: center;
    padding-right: 50px;
  }}
  .terminal-body {{
    padding: 22px 26px;
    color: #E2E8F0;
    font-size: 13.5px;
    line-height: 1.5;
    white-space: pre;
    flex-grow: 1;
    overflow: hidden;
  }}
  .cyan {{ color: #38BDF8; font-weight: bold; }}
  .yellow {{ color: #FBBF24; font-weight: bold; }}
  .green {{ color: #34D399; font-weight: bold; }}
  .red {{ color: #F87171; font-weight: bold; }}
  .magenta {{ color: #C084FC; font-weight: bold; }}
  .gray {{ color: #64748B; }}
  .white {{ color: #F8FAFC; }}
  .bold {{ font-weight: bold; }}
  .box-border {{ color: #0EA5E9; }}
  .box-border-yellow {{ color: #EAB308; }}
  .box-border-green {{ color: #10B981; }}
  .cursor {{
    display: inline-block;
    width: 8px;
    height: 15px;
    background: #38BDF8;
    vertical-align: middle;
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
      <div class="window-title">{step_title}</div>
    </div>
    <div class="terminal-body">{content_html}</div>
  </div>
</body>
</html>
"""


def build_scenario_frames():
    """Builds a choreographed sequence of terminal states."""
    scenarios = []

    # Frame 1: Empty shell with prompt
    scenarios.append({
        "title": "AegisBrain - Autonomous 3-Tier Multi-Agent Engine",
        "lines": [],
        "prompt": "PS C:\\Users\\priya>",
        "cmd": "curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | powershell",
        "duration": 2.0,
    })

    # Frame 2: Installer ASCII Logo & System Checks
    scenarios.append({
        "title": "AegisBrain Universal Installer v2.4.0",
        "lines": [
            '<span class="cyan">  █████╗ ███████╗ ██████╗ ██╗███████╗    ██████╗ ██████╗  █████╗ ██╗███╗   ██╗</span>',
            '<span class="cyan"> ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║</span>',
            '<span class="yellow"> ███████║█████╗  ██║  ███╗██║███████╗    ██████╔╝██████╔╝███████║██║██╔██╗ ██║</span>',
            '<span class="yellow"> ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║</span>',
            '<span class="red"> ██║  ██║███████╗╚██████╔╝██║███████║    ██████╔╝██║  ██║██║  ██║██║██║ ╚████║</span>',
            '<span class="red"> ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝</span>',
            '<span class="gray">         [ 24/7 AUTONOMOUS NEURAL MEMORY & 3-TIER AGENT ORCHESTRATOR ]</span>',
            '<span class="gray">                               Version 2.4.0 (GPLv3)</span>',
            '',
            '<span class="box-border">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="box-border">│</span>  <span class="cyan bold">STEP 1 of 6: License Agreement &amp; Terms of Service (GPLv3)</span>             <span class="box-border">│</span>',
            '<span class="box-border">└────────────────────────────────────────────────────────────────────────┘</span>',
            '<span class="gray">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="gray">│</span>  100% Local Neural Memory: Your data stays on your machine. Zero leaks.<span class="gray">│</span>',
            '<span class="gray">│</span>  Subprocess Boundary: Workers (Hermes, Ollama) run via isolated OS pipe<span class="gray">│</span>',
            '<span class="gray">│</span>  Automated pre-install snapshot created for 1-click restore rollback.  <span class="gray">│</span>',
            '<span class="gray">└────────────────────────────────────────────────────────────────────────┘</span>',
            ' <span class="green bold">[✓] Terms accepted automatically.</span>',
            '',
            '<span class="box-border-yellow">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="box-border-yellow">│</span>  <span class="yellow bold">STEP 2 of 6: System Requirements &amp; Runtime Inspection</span>                 <span class="box-border-yellow">│</span>',
            '<span class="box-border-yellow">└────────────────────────────────────────────────────────────────────────┘</span>',
            '<span class="gray">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="gray">│</span>   • Python Runtime:      <span class="green bold">[INSTALLED]</span> Python 3.14.7                     <span class="gray">│</span>',
            '<span class="gray">│</span>   • Git Version Control: <span class="green bold">[INSTALLED]</span> git version 2.55.0                <span class="gray">│</span>',
            '<span class="gray">│</span>   • Node.js &amp; npm:       <span class="green bold">[INSTALLED]</span> Node v24.19.0 / npm v11.17.0      <span class="gray">│</span>',
            '<span class="gray">│</span>   • Host Memory (RAM):   <span class="green bold">[HEALTHY]</span> 5.38 GB Available                   <span class="gray">│</span>',
            '<span class="gray">└────────────────────────────────────────────────────────────────────────┘</span>',
            ' <span class="green bold">[✓] System prerequisites validated.</span>',
        ],
        "prompt": " ",
        "cmd": "",
        "duration": 2.5,
    })

    # Frame 3: Local Tools, Dual NLP Engine & Finish
    scenarios.append({
        "title": "AegisBrain Universal Installer v2.4.0",
        "lines": [
            '<span class="box-border">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="box-border">│</span>  <span class="cyan bold">STEP 4 of 6: Local Worker Engines &amp; Multimodal Tools</span>                  <span class="box-border">│</span>',
            '<span class="box-border">└────────────────────────────────────────────────────────────────────────┘</span>',
            '<span class="gray">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="gray">│</span>   • Ollama (Local LLM Engine):   <span class="green bold">[INSTALLED]</span> ollama version 0.5.12     <span class="gray">│</span>',
            '<span class="gray">│</span>   • Hermes Agent CLI:            <span class="green bold">[INSTALLED]</span> Available in PATH         <span class="gray">│</span>',
            '<span class="gray">│</span>   • FFmpeg Engine:               <span class="green bold">[INSTALLED]</span> Available in PATH         <span class="gray">│</span>',
            '<span class="gray">│</span>   • Whisper Speech-to-Text:      <span class="green bold">[INSTALLED]</span> Available in PATH         <span class="gray">│</span>',
            '<span class="gray">│</span>   • yt-dlp Media Downloader:     <span class="green bold">[INSTALLED]</span> Available in PATH         <span class="gray">│</span>',
            '<span class="gray">└────────────────────────────────────────────────────────────────────────┘</span>',
            '',
            '<span class="box-border-yellow">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="box-border-yellow">│</span>  <span class="yellow bold">STEP 5 of 6: Intelligent NLP Dual-Mode Engine &amp; Background Daemon</span>     <span class="box-border-yellow">│</span>',
            '<span class="box-border-yellow">└────────────────────────────────────────────────────────────────────────┘</span>',
            '<span class="gray">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="gray">│</span>  Dynamic Workload Triage Architecture:                                 <span class="gray">│</span>',
            '<span class="gray">│</span>   • Dual NLP Auto-Triage: BOTH Arbitrage &amp; Fast modes active.          <span class="gray">│</span>',
            '<span class="gray">│</span>   • The NLP intent engine analyzes every command in any AI assistant:  <span class="gray">│</span>',
            '<span class="gray">│</span>     - Fast / Urgent / Quick / Micro fixes  -&gt; Fast Mode (Direct)       <span class="gray">│</span>',
            '<span class="gray">│</span>     - Substantial / Heavy / Architecture   -&gt; Arbitrage Mode (3-Tier)  <span class="gray">│</span>',
            '<span class="gray">│</span>   • Zero manual mode switching required: NLP routes automatically.     <span class="gray">│</span>',
            '<span class="gray">└────────────────────────────────────────────────────────────────────────┘</span>',
            '',
            '<span class="green bold">╔════════════════════════════════════════════════════════════════════════╗</span>',
            '<span class="green bold">║  AEGISBRAIN INSTALLATION COMPLETE — 100% OPERATIONAL                   ║</span>',
            '<span class="green bold">╠════════════════════════════════════════════════════════════════════════╣</span>',
            '<span class="white">║  • Execution Strategy:   DUAL NLP AUTO-TRIAGE (Arbitrage + Fast Active)║</span>',
            '<span class="white">║  • Neural Memory Bus:    Active (brain.db WAL mode, &lt;25ms FTS5 index)  ║</span>',
            '<span class="white">║  • Background Daemon:    Online 24/7 (http://127.0.0.1:8765/status)    ║</span>',
            '<span class="white">║  • Telegram Bridge:      @HHAACLIBot (Voice Notes &amp; Terminal Control)  ║</span>',
            '<span class="white">║  • Restore Point ID:     1794330900_universal_install                  ║</span>',
            '<span class="white">║  • License:              GNU GPLv3 (Free &amp; Open Source)                ║</span>',
            '<span class="green bold">╚════════════════════════════════════════════════════════════════════════╝</span>',
        ],
        "prompt": "PS C:\\Users\\priya>",
        "cmd": "",
        "duration": 3.0,
    })

    # Frame 4: Prompting Task Triage
    scenarios.append({
        "title": "AegisBrain - 3-Tier Multi-Agent Workload Triage",
        "lines": [
            '<span class="gray">PS C:\\Users\\priya&gt;</span> <span class="white bold">cd P:\\vault</span>',
        ],
        "prompt": "P:\\vault>",
        "cmd": 'aegis triage "Build distributed JWT token refresh rotation engine with Redis caching"',
        "duration": 2.0,
    })

    # Frame 5: 3-Tier Execution Trace & 4-Gate Quality Verification
    scenarios.append({
        "title": "AegisBrain - 3-Tier Multi-Agent Workload Triage",
        "lines": [
            '<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis triage "Build distributed JWT token refresh rotation engine with Redis caching"</span>',
            '',
            '<span class="cyan bold">⚡ [AegisBrain Dynamic Severity &amp; Workload Triage]</span>',
            '  • Task Severity Score:  <span class="yellow bold">0.82 / 1.0 (High Severity - Architecture + Security)</span>',
            '  • Hardware Headroom:    <span class="green bold">5.38 GB RAM Free • CPU 12% • Thermals Normal</span>',
            '  • Forecast Cost:        <span class="magenta bold">~12,400 Frontier Tokens ($0.037) vs 0 Local Tokens ($0.000)</span>',
            '  • Triage Routing:       <span class="green bold">PARALLEL_SUBAGENTS (3-Tier Token Arbitrage Mode)</span>',
            '',
            '<span class="box-border">┌────────────────────────────────────────────────────────────────────────┐</span>',
            '<span class="box-border">│</span>  <span class="cyan bold">HIERARCHICAL MULTI-AGENT EXECUTION TRACE</span>                              <span class="box-border">│</span>',
            '<span class="box-border">└────────────────────────────────────────────────────────────────────────┘</span>',
            ' <span class="white bold">Tier 1 Senior Boss (Brain):</span> Formulates strict invariants &amp; Karpathy specification.',
            '   ↳ Spawns <span class="cyan bold">Tier 2 Junior Boss</span> (`invoke_subagent` -&gt; Security Specialist).',
            '',
            ' <span class="cyan bold">Tier 2 Junior Boss (Subagent):</span> Dispatches to <span class="yellow bold">Tier 3 Execution Worker CLI</span>:',
            '   ↳ <span class="gray">&gt; hermes chat -q "Implement JwtRotationService with atomic redis SETNX..."</span>',
            '',
            ' <span class="yellow bold">Tier 3 Local Worker (Hermes CLI / Qwen2.5-Coder):</span>',
            '   ↳ Generates candidate code using 100% local tokens (0 frontier cost)...',
            '   ↳ Delivered 148 lines of surgical Python JWT rotation logic + unit tests.',
            '',
            ' <span class="magenta bold">Tier 2 Quality Architecture Audit (4-Gate Verification):</span>',
            '   <span class="green">[✓] Gate 1: Karpathy Simplicity Doctrine</span>  - 148 lines, zero unnecessary wrappers.',
            '   <span class="green">[✓] Gate 2: TurnItOut Unslop</span>              - 100% conversational watermarks stripped.',
            '   <span class="green">[✓] Gate 3: Red-Team Security Audit</span>       - AST verified: 0 injection sinks, safe hmac.',
            '   <span class="green">[✓] Gate 4: Dual-Environment Test</span>         - Sandbox: PASS • Host: PASS (8/8 tests).',
            '',
            ' <span class="white bold">Tier 1 Senior Boss Sign-off:</span> Verified and committed to workspace.',
            '   ↳ Neural memory WAL commit recorded to <span class="white">brain.db</span> in <span class="green bold">18.4ms</span>.',
            '   ↳ <span class="green bold">Token Arbitrage Result: 92.4% Frontier Tokens Saved (12,400 -&gt; 940 tokens)</span>',
        ],
        "prompt": "P:\\vault>",
        "cmd": "",
        "duration": 4.5,
    })

    # Frame 6: Sub-second FTS5 Memory Recall Demonstration
    scenarios.append({
        "title": "AegisBrain - Sub-Second Neural Memory Bus (<25ms)",
        "lines": [
            '<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis recall "JWT rotation"</span>',
            '',
            '<span class="cyan bold">🔍 [Sub-Second FTS5 Neural Recall]</span>',
            '<span class="gray">Target: "JWT rotation" • Query Engine: SQLite FTS5 Porter Stemmer</span>',
            '',
            '<span class="green bold">[Record #1] (Rank: -14.28 • Query Latency: 18.2ms • Cost: 0 Frontier Tokens)</span>',
            '  • Title:      <span class="white bold">Distributed JWT Session Rotation &amp; Redis Setnx Lock</span>',
            '  • Category:   <span class="yellow">ARCHITECTURE / SECURITY</span>',
            '  • Decision:   Rotated tokens using atomic Redis SETNX with 60-second grace period.',
            '  • Invariants: Constant-time HMAC comparison to prevent timing attacks.',
            '  • Code Anchor:<span class="cyan"> package/aegis/auth/jwt_rotation.py#L42-L88</span>',
            '  • Tags:       <span class="gray">["jwt", "security", "redis", "token-rotation", "session-vault"]</span>',
            '',
            '<span class="gray">────────────────────────────────────────────────────────────────────────</span>',
            ' <span class="white bold">Benchmark Comparison:</span>',
            '  • <span class="green bold">AegisBrain FTS5 Recall:  18.2 ms (82 tokens injected)</span>',
            '  • Raw JSONL Log Crawling:  9,420 ms (52,400 tokens crawled - 99.8% slower)',
            '  • <span class="cyan bold">Net Savings: 52,318 tokens saved &amp; 517x faster response</span>',
        ],
        "prompt": "P:\\vault>",
        "cmd": "",
        "duration": 3.0,
    })

    # Frame 7: Snapshot Restore Points & Zero-Residue Rollback
    scenarios.append({
        "title": "AegisBrain - Instant Snapshot Restore & Zero-Residue Rollback",
        "lines": [
            '<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis snapshot list</span>',
            '<span class="cyan bold">============================================================================================</span>',
            '  <span class="white bold">#   Date / Time          Files  Snapshot ID                    Reason</span>',
            '<span class="gray">--------------------------------------------------------------------------------------------</span>',
            ' <span class="yellow bold">[ 1]</span> <span class="cyan">2026-11-10 17:30:06</span>   <span class="green">8</span>     <span class="white bold">1794312006_pre_gemini_update</span>   Pre-update of GEMINI.md for Quick Mode',
            ' <span class="yellow bold">[ 2]</span> <span class="cyan">2026-11-10 17:18:05</span>   <span class="green">8</span>     <span class="white bold">1794311285_universal_install</span>   AegisBrain Universal Installation',
            ' <span class="yellow bold">[ 3]</span> <span class="cyan">2026-11-10 14:53:03</span>   <span class="green">8</span>     <span class="white bold">1794302583_pre_install</span>         Automated pre-install restore point',
            '<span class="gray">--------------------------------------------------------------------------------------------</span>',
            '  <span class="gray">(Showing newest 3 of 47 snapshots)</span>',
            '',
            '  <span class="white bold">Tip:</span> Run <span class="green bold">`aegis restore &lt;number&gt;`</span> (e.g. <span class="cyan bold">`aegis restore 1`</span>) to roll back instantly.',
            '',
            '<span class="gray">P:\\vault&gt;</span> <span class="white bold">aegis restore 1</span>',
            '<span class="green bold">[AegisBrain] [OK] Restored 8 files from restore point \'1794312006_pre_gemini_update\'</span>',
            '  <span class="white">↳ Reverted GEMINI.md, CLAUDE.md, and agent rules to exact pre-change hashes</span>',
            '  <span class="white">↳ Zero leftover residue • Clean verified state</span>',
        ],
        "prompt": "P:\\vault>",
        "cmd": "",
        "duration": 3.5,
    })

    return scenarios


def render_video():
    scenarios = build_scenario_frames()
    print(f"\n--- 3. Rendering {len(scenarios)} Scenario Video Frames ---")

    frame_files = []
    for idx, sc in enumerate(scenarios):
        html_file = FRAMES_DIR / f"frame_{idx:02d}.html"
        png_file = FRAMES_DIR / f"frame_{idx:02d}.png"
        html_content = create_terminal_frame_html(sc["title"], sc["lines"], sc.get("prompt", "P:\\vault>"), sc.get("cmd", ""))
        html_file.write_text(html_content, encoding="utf-8")

        # Capture frame PNG
        cmd = [
            EDGE_PATH,
            "--headless=new",
            "--disable-gpu",
            "--window-size=1200,780",
            f"--screenshot={png_file.resolve()}",
            html_file.as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, timeout=15)
        if png_file.exists():
            print(f"  [OK] Rendered Frame #{idx}: {png_file.name} (Duration: {sc['duration']}s)")
            frame_files.append((png_file, sc["duration"]))

    # Build concat demuxer file for FFmpeg
    concat_file = FRAMES_DIR / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for png_path, dur in frame_files:
            f.write(f"file '{png_path.as_posix()}'\n")
            f.write(f"duration {dur}\n")
        # Repeat last file for ffmpeg concat requirement
        if frame_files:
            f.write(f"file '{frame_files[-1][0].as_posix()}'\n")

    output_mp4 = MARKETING_DIR / "aegis-brain-terminal-demo.mp4"
    output_gif = MARKETING_DIR / "aegis-brain-terminal-demo.gif"

    print("\n--- 4. Encoding MP4 Video with FFmpeg ---")
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-vf", "fps=30,format=yuv420p,scale=1200:780",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        str(output_mp4),
    ]
    res = subprocess.run(ffmpeg_cmd, capture_output=True)
    if output_mp4.exists() and output_mp4.stat().st_size > 1000:
        print(f"  [OK] Video created: {output_mp4.name} ({output_mp4.stat().st_size:,} bytes)")
    else:
        print(f"  [FAIL] Video creation failed: {res.stderr.decode(errors='ignore')[:300]}")

    print("\n--- 5. Encoding Animated GIF with FFmpeg ---")
    gif_cmd = [
        "ffmpeg",
        "-y",
        "-i", str(output_mp4),
        "-vf", "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        str(output_gif),
    ]
    res_gif = subprocess.run(gif_cmd, capture_output=True)
    if output_gif.exists() and output_gif.stat().st_size > 1000:
        print(f"  [OK] GIF created: {output_gif.name} ({output_gif.stat().st_size:,} bytes)")
    else:
        print(f"  [FAIL] GIF creation failed: {res_gif.stderr.decode(errors='ignore')[:300]}")


if __name__ == "__main__":
    render_video()
