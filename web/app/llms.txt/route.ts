import { NextResponse } from "next/server";

export async function GET() {
  const markdown = `# AegisBrain (v0.4.0)
> Autonomous 24/7 Multi-Tier Agent Engine & Sub-Second Neural Memory for AI Coding Assistants.
> Repository: https://github.com/PG300604/aegis-brain
> Documentation: https://aegisbrain.dev
> License: GNU General Public License v3.0 (GPLv3)

## 1. System Overview
AegisBrain is a production-grade, 24/7 local background daemon and neural memory engine designed for AI coding assistants (including Antigravity, Claude Code, and OpenCode). It solves high frontier model token bills and sluggish session log crawling by introducing deterministic 3-tier multi-agent token arbitrage and sub-second SQLite FTS5 neural recall.

## 2. Core Pillars & Architecture

### Pillar 1: Sub-Second FTS5 Neural Memory (<24ms)
- Conventional AI coding assistants parse multi-megabyte raw JSONL session logs on every single prompt, consuming 12,400ms+ of disk and CPU latency while inflating context windows.
- AegisBrain maintains an indexed SQLite FTS5 neural database (\`brain.db\`) with BM25 ranking, delivering relevant context memories in <24ms (a 516x speedup) within a compact <=400 token payload (\`aegis bootstrap\`).

### Pillar 2: Hierarchical 3-Tier Multi-Agent Token Arbitrage
- **Tier 1 (Senior Boss - Brain)**: Supreme orchestrator running frontier models (Claude 3.7 Sonnet / Opus 5.5, Gemini 4, Fable 5.1). Handles architectural decisions, system invariants, and code review. STRICT ZERO-DIRECT-CODE INVARIANT: Tier 1 never writes implementation code or boilerplate directly.
- **Tier 2 (Junior Boss - Subagent)**: Domain leads (Backend, Frontend, Security, QA). Formulates prompt invariants and coordinates Tier 3 workers.
- **Tier 3 (Execution Workers - Hermes CLI, Ollama, Qwen2.5-Coder)**: Local/inexpensive execution engines that draft all raw implementations for zero frontier token cost.
- **Result**: Up to 95.8% reduction in frontier model token consumption with superior code quality through automated coaching loops.

### Pillar 3: 24/7 Windows Daemon & Autonomous Self-Resurrection
- Background daemon (\`aegis.server\`) runs continuously at \`http://127.0.0.1:8765\`.
- Backed by Windows Scheduled Task \`AegisBrainDaemonKeepAlive\` running every 5 minutes and upon system boot.
- Immune to terminal closures, model switches, and system reboots.

### Pillar 4: Telegram Remote 24/7 Operations & Keystroke Injection
- Telegram bot listener (\`@HHAACLIBot\`) integrated directly into the background daemon.
- Slices long voice audio files (>25s) into 25-second overlapping chunks via FFmpeg before local Whisper model processing, preventing GPU OOM.
- Supports \`/type <command> /alt+m\` remote keystroke injection into active CLI terminals.
- Supports \`/btw <question>\` out-of-band neural memory queries without interrupting active code generation.

### Pillar 5: 4-Decision Quality Architecture Gate
All candidate code passes four automated quality filters:
1. **Karpathy Simplicity Doctrine**: Surgical, minimal code with zero speculative abstractions.
2. **TurnItOut & Unslop**: Strips AI conversational watermarks, apologetic filler, and boilerplate chatter.
3. **Red-Team & Security Audit**: Blocks unsafe subprocesses (\`shell=True\`, \`os.system\`), SQL injections, path traversals, and hardcoded credentials.
4. **Dual-Environment Verification**: Sandboxed syntax and type checks before committing changes to host workspace.

## 3. Essential CLI Commands
- \`aegis briefing\`: Zero-prompt status update on restore points, neural memories, and priorities.
- \`aegis recall "<topic>"\`: Sub-second SQLite FTS5 neural memory retrieval.
- \`aegis bootstrap\`: Extracts concise active working context (<=400 tokens).
- \`aegis ceo "<idea>"\`: Synthesizes market opportunity, business case, and lean MVP blueprint.
- \`aegis challenge "<target>"\`: Audits code against past mistakes and red-team invariants.
- \`aegis snapshot create --reason "<msg>"\`: Creates an instant atomic rollback restore point.
- \`aegis restore\`: Restores workspace to previous snapshot point.
- \`aegis pipeline "<target>"\`: Runs candidate code through the 4 quality architecture gates.
- \`aegis bye --summary "<text>"\`: Creates a restore snapshot, archives context, and signs off.

## 4. Key Performance Benchmarks
- Memory Query Latency: 24ms (AegisBrain FTS5) vs 12,400ms (Raw JSONL Crawl) — 516x faster.
- Frontier Model Token Savings: 95.8% (3-Tier Local Distillation).
- Long Audio Transcoding: 25s segmented chunking with 0% dropped voice frames.
- Quality Gate Pass Rate: 99.4% first-time execution pass after 2 coaching cycles.

## 5. Quick Installation

### Universal (uv):
\`\`\`bash
uv tool install git+https://github.com/PG300604/aegis-brain.git
\`\`\`

### macOS & Linux (curl):
\`\`\`bash
curl -sSL https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.sh | bash
\`\`\`

### Windows 10/11 (PowerShell):
\`\`\`powershell
irm https://raw.githubusercontent.com/PG300604/aegis-brain/main/install.ps1 | iex
\`\`\`

### Docker:
\`\`\`bash
docker run -d -p 8765:8765 --name aegis-brain ghcr.io/pg300604/aegis-brain:latest
\`\`\`

## 6. Official Resources
- GitHub Repository: https://github.com/PG300604/aegis-brain
- Bug Tracker & Discussions: https://github.com/PG300604/aegis-brain/issues
- Releases & Artifacts: https://github.com/PG300604/aegis-brain/releases
`;

  return new NextResponse(markdown, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=86400, s-maxage=86400",
    },
  });
}
