"""Generate an Excalidraw-style Architecture Diagram for AegisBrain.

Creates a friendly, human-drawn, warm whiteboard-style architecture diagram
showing a SINGLE unified coding agent client box connecting via ONE common bus
to the AegisBrain Daemon, where ALL features are universally accessible to all agents,
with downstream arrows dispatching to dedicated storage and runtimes.
"""

import json
from pathlib import Path

OUTPUT_UNIFIED = Path("P:/open-source/aegis-brain/assets/architecture-unified.svg")
OUTPUT_LEGACY = Path("P:/open-source/aegis-brain/assets/architecture-excalidraw.svg")
OUTPUT_JSON = Path("P:/open-source/aegis-brain/assets/architecture.excalidraw")


def build_diagram():
    width = 1180
    height = 560

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: #FFFFFF; }}
      .box-frame {{ stroke: #94A3B8; stroke-width: 1.8; stroke-dasharray: 6,6; fill: #F8FAFC; rx: 14; }}
      .label-zone {{ font-family: 'Virgil', 'Comic Sans MS', 'Caveat', -apple-system, sans-serif; font-size: 13px; font-weight: 700; fill: #64748B; letter-spacing: 1px; }}
      .card-title {{ font-family: 'Virgil', 'Comic Sans MS', -apple-system, sans-serif; font-size: 15px; font-weight: 700; }}
      .card-sub {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; font-weight: 500; opacity: 0.85; }}
      .edge-label {{ font-family: 'Virgil', 'Comic Sans MS', -apple-system, sans-serif; font-size: 11px; font-weight: 700; }}
      .arrow {{ stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
      
      /* Dark mode support */
      @media (prefers-color-scheme: dark) {{
        .bg {{ fill: #0B0D11; }}
        .box-frame {{ fill: #11141C; stroke: #334155; }}
        .label-zone {{ fill: #94A3B8; }}
        .dark-client-bg {{ fill: #0C1E33 !important; stroke: #0284C7 !important; }}
        .dark-pill-bg {{ fill: #16263D !important; stroke: #1E3A5F !important; }}
        .dark-pill-title {{ fill: #38BDF8 !important; }}
        .dark-pill-sub {{ fill: #94A3B8 !important; }}
        .dark-engine-amber {{ fill: #241A0B !important; stroke: #D97706 !important; }}
        .dark-engine-emerald {{ fill: #0A261A !important; stroke: #059669 !important; }}
        .dark-engine-violet {{ fill: #1D1536 !important; stroke: #7C3AED !important; }}
        .dark-engine-rose {{ fill: #2C0F17 !important; stroke: #E11D48 !important; }}
        .text-dark {{ fill: #F8FAFC !important; }}
      }}
    </style>

    <!-- Arrow Markers -->
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#0284C7" />
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#D97706" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#7C3AED" />
    </marker>
    <marker id="arrow-rose" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#E11D48" />
    </marker>
  </defs>

  <!-- Background Base -->
  <rect width="{width}" height="{height}" class="bg" rx="12" />

  <!-- ======================================================= -->
  <!-- ZONE 1: SINGLE UNIFIED AI CODING AGENT BOX (LEFT)       -->
  <!-- ======================================================= -->
  <rect x="25" y="30" width="255" height="500" class="box-frame" />
  <text x="45" y="60" class="label-zone">AI CODING AGENTS (ANY RUNTIME)</text>

  <!-- Single Unified Client Box -->
  <g transform="translate(42, 80)">
    <rect width="221" height="430" rx="12" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.5" class="dark-client-bg" />
    
    <!-- Box Header -->
    <text x="16" y="32" fill="#0369A1" class="card-title text-dark" font-size="16">All AI Coding Agents</text>
    <text x="16" y="52" fill="#0284C7" class="card-sub dark-pill-sub">Irrespective of agent used</text>
    <line x1="16" y1="62" x2="205" y2="62" stroke="#BAE6FD" stroke-width="1.5" />

    <!-- Agent 1: Antigravity -->
    <g transform="translate(12, 74)">
      <rect width="197" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" class="dark-pill-bg" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700" class="dark-pill-title">✦ Google Antigravity</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">Claude 3.7 / Gemini 2.5</text>
    </g>

    <!-- Agent 2: Claude Code -->
    <g transform="translate(12, 124)">
      <rect width="197" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" class="dark-pill-bg" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700" class="dark-pill-title">✦ Anthropic Claude Code</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">CLI agent &amp; tools</text>
    </g>

    <!-- Agent 3: OpenAI Codex -->
    <g transform="translate(12, 174)">
      <rect width="197" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" class="dark-pill-bg" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700" class="dark-pill-title">✦ OpenAI Codex CLI</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">CLI prompt hooks</text>
    </g>

    <!-- Agent 4: Cursor & Windsurf -->
    <g transform="translate(12, 224)">
      <rect width="197" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" class="dark-pill-bg" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700" class="dark-pill-title">✦ Cursor &amp; Windsurf</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">.cursorrules / context</text>
    </g>

    <!-- Agent 5: Nous Hermes -->
    <g transform="translate(12, 274)">
      <rect width="197" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" class="dark-pill-bg" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700" class="dark-pill-title">✦ Nous Hermes Agent</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">Autonomous reasoning</text>
    </g>

    <!-- Agent 6: Aider & OpenCode -->
    <g transform="translate(12, 324)">
      <rect width="197" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" class="dark-pill-bg" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700" class="dark-pill-title">✦ Aider &amp; OpenCode</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">Terminal pair programming</text>
    </g>

    <!-- Footer callout inside the single box -->
    <g transform="translate(12, 374)">
      <rect width="197" height="44" rx="6" fill="#E0F2FE" stroke="#7DD3FC" stroke-dasharray="3,3" class="dark-pill-bg" />
      <text x="10" y="18" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="11" font-weight="700" class="dark-pill-title">Universal Memory Channel</text>
      <text x="10" y="34" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" class="dark-pill-sub">100% shared by all agents</text>
    </g>
  </g>

  <!-- ======================================================= -->
  <!-- THE ONE COMMON BUS ARROW (ZONE 1 TO ZONE 2)             -->
  <!-- ======================================================= -->
  <!-- Main connection arrow connecting single box to AegisBrain Daemon -->
  <path d="M 263 295 L 376 295" class="arrow" stroke="#0284C7" stroke-width="3.5" marker-end="url(#arrow-blue)" />

  <!-- Badge over the common arrow -->
  <g transform="translate(278, 256)">
    <rect width="86" height="66" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.8" class="dark-pill-bg" />
    <text x="43" y="20" fill="#0369A1" class="edge-label dark-pill-title" text-anchor="middle" font-size="10">COMMON BUS</text>
    <text x="43" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" text-anchor="middle" class="dark-pill-sub">HTTP :8765</text>
    <text x="43" y="48" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" text-anchor="middle" class="dark-pill-sub">CLI / Skills</text>
    <text x="43" y="60" fill="#047857" font-family="ui-monospace, monospace" font-size="9" font-weight="700" text-anchor="middle">One Ingress</text>
  </g>

  <!-- ======================================================= -->
  <!-- ZONE 2: AEGIS CORE DAEMON CHASSIS (CENTER)              -->
  <!-- ======================================================= -->
  <rect x="380" y="30" width="465" height="500" class="box-frame" />
  <text x="400" y="60" class="label-zone">AEGISBRAIN DAEMON (127.0.0.1:8765)</text>
  <text x="825" y="60" fill="#059669" font-family="ui-monospace, monospace" font-size="11" font-weight="700" text-anchor="end">● DAEMON ACTIVE</text>

  <!-- Internal Distribution Spine (Universal Access for All Connected Agents) -->
  <path d="M 380 295 L 406 295" stroke="#0284C7" stroke-width="2.5" />
  <path d="M 406 122 L 406 437" stroke="#0284C7" stroke-width="2.5" stroke-dasharray="4,4" />

  <!-- Branches to all 4 engines -->
  <path d="M 406 122 L 426 122" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />
  <path d="M 406 227 L 426 227" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />
  <path d="M 406 332 L 426 332" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />
  <path d="M 406 437 L 426 437" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />

  <!-- Core Engine 1: Context Governor -->
  <g transform="translate(426, 80)">
    <rect width="400" height="85" rx="10" fill="#FEF3C7" stroke="#D97706" stroke-width="2" class="dark-engine-amber" />
    <text x="20" y="30" fill="#B45309" class="card-title text-dark">Deterministic Context Governor</text>
    <text x="20" y="50" fill="#92400E" class="card-sub text-dark">Prunes git diffs, branch state, commits, &amp; tracked PRs</text>
    <rect x="20" y="58" width="185" height="18" rx="4" fill="#FDE68A" />
    <text x="26" y="71" fill="#78350F" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Strict ≤ 400 Token Cap | Auto-Load</text>
  </g>

  <!-- Core Engine 2: Neural Memory Bus & Instant Recall -->
  <g transform="translate(426, 185)">
    <rect width="400" height="85" rx="10" fill="#D1FAE5" stroke="#059669" stroke-width="2" class="dark-engine-emerald" />
    <text x="20" y="30" fill="#047857" class="card-title text-dark">Neural Memory Bus &amp; Instant Recall</text>
    <text x="20" y="50" fill="#065F46" class="card-sub text-dark">SQLite WAL + FTS5 full-text indexing with triggers</text>
    <rect x="20" y="58" width="220" height="18" rx="4" fill="#A7F3D0" />
    <text x="26" y="71" fill="#064E3B" font-family="ui-monospace, monospace" font-size="10" font-weight="700">&lt; 50ms Recall ('aegis recall') | 95%+ Save</text>
  </g>

  <!-- Core Engine 3: Skill Distiller & Proxy -->
  <g transform="translate(426, 290)">
    <rect width="400" height="85" rx="10" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2" class="dark-engine-violet" />
    <text x="20" y="30" fill="#6D28D9" class="card-title text-dark">Cross-Model Skill Distiller &amp; Proxy</text>
    <text x="20" y="50" fill="#5B21B6" class="card-sub text-dark">OpenAI-compatible /v1 prompt augmentation reverse proxy</text>
    <rect x="20" y="58" width="200" height="18" rx="4" fill="#DDD6FE" />
    <text x="26" y="71" fill="#4C1D95" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Injects 500+ Skills to Local Models</text>
  </g>

  <!-- Core Engine 4: OpenHiggsfield Media Bridge -->
  <g transform="translate(426, 395)">
    <rect width="400" height="85" rx="10" fill="#FFE4E6" stroke="#E11D48" stroke-width="2" class="dark-engine-rose" />
    <text x="20" y="30" fill="#BE123C" class="card-title text-dark">OpenHiggsfield Media Bridge</text>
    <text x="20" y="50" fill="#9F1239" class="card-sub text-dark">Zero-dependency stdlib image/video dispatch &amp; indexing</text>
    <rect x="20" y="58" width="200" height="18" rx="4" fill="#FECDD3" />
    <text x="26" y="71" fill="#881337" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Flux 2 / Seedance / Kling / Wan 2.6</text>
  </g>

  <!-- ======================================================= -->
  <!-- ZONE 3: STORAGE & TARGET RUNTIMES (RIGHT)               -->
  <!-- ======================================================= -->
  <rect x="915" y="30" width="240" height="500" class="box-frame" />
  <text x="935" y="60" class="label-zone">STORAGE &amp; TARGET RUNTIMES</text>

  <!-- Target 1: ACTIVE_CONTEXT.md -->
  <g transform="translate(935, 85)">
    <rect width="200" height="74" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="2" class="dark-engine-amber" />
    <text x="16" y="28" fill="#B45309" class="card-title text-dark">ACTIVE_CONTEXT.md</text>
    <text x="16" y="48" fill="#92400E" class="card-sub text-dark">~/.aegis-brain/</text>
    <text x="16" y="62" fill="#D97706" class="card-sub text-dark">Auto-read by all agents</text>
  </g>

  <!-- Target 2: brain.db (SQLite) -->
  <g transform="translate(935, 190)">
    <rect width="200" height="74" rx="8" fill="#D1FAE5" stroke="#059669" stroke-width="2" class="dark-engine-emerald" />
    <text x="16" y="28" fill="#047857" class="card-title text-dark">brain.db (SQLite)</text>
    <text x="16" y="48" fill="#065F46" class="card-sub text-dark">WAL + FTS5 on disk</text>
    <text x="16" y="62" fill="#059669" class="card-sub text-dark">Bypassed in private mode</text>
  </g>

  <!-- Target 3: Local Ollama -->
  <g transform="translate(935, 295)">
    <rect width="200" height="74" rx="8" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2" class="dark-engine-violet" />
    <text x="16" y="28" fill="#6D28D9" class="card-title text-dark">Local Ollama :11434</text>
    <text x="16" y="48" fill="#5B21B6" class="card-sub text-dark">qwen2.5-coder / deepseek</text>
    <text x="16" y="62" fill="#7C3AED" class="card-sub text-dark">Guided by distilled skills</text>
  </g>

  <!-- Target 4: OpenHiggsfield API -->
  <g transform="translate(935, 400)">
    <rect width="200" height="74" rx="8" fill="#FFE4E6" stroke="#E11D48" stroke-width="2" class="dark-engine-rose" />
    <text x="16" y="28" fill="#BE123C" class="card-title text-dark">OpenHiggsfield API</text>
    <text x="16" y="48" fill="#9F1239" class="card-sub text-dark">openhiggsfield.ai</text>
    <text x="16" y="62" fill="#E11D48" class="card-sub text-dark">Photo &amp; video generation</text>
  </g>

  <!-- ======================================================= -->
  <!-- DOWNSTREAM ARROWS (ZONE 2 TO ZONE 3)                    -->
  <!-- ======================================================= -->
  <!-- Governor -> ACTIVE_CONTEXT.md -->
  <path d="M 826 122 L 931 122" class="arrow" stroke="#D97706" marker-end="url(#arrow-amber)" />
  <rect x="846" y="110" width="74" height="20" rx="4" fill="#FEF3C7" stroke="#FDE68A" class="dark-engine-amber" />
  <text x="883" y="124" fill="#92400E" class="edge-label text-dark" text-anchor="middle">compile</text>

  <!-- Memory Bus -> brain.db -->
  <path d="M 826 227 L 931 227" class="arrow" stroke="#059669" marker-end="url(#arrow-green)" />
  <rect x="846" y="215" width="74" height="20" rx="4" fill="#D1FAE5" stroke="#A7F3D0" class="dark-engine-emerald" />
  <text x="883" y="229" fill="#065F46" class="edge-label text-dark" text-anchor="middle">WAL sync</text>

  <!-- Skill Distiller -> Ollama -->
  <path d="M 826 332 L 931 332" class="arrow" stroke="#7C3AED" marker-end="url(#arrow-purple)" />
  <rect x="846" y="320" width="74" height="20" rx="4" fill="#EDE9FE" stroke="#DDD6FE" class="dark-engine-violet" />
  <text x="883" y="334" fill="#5B21B6" class="edge-label text-dark" text-anchor="middle">:11434/v1</text>

  <!-- Media Bridge -> OpenHiggsfield -->
  <path d="M 826 437 L 931 437" class="arrow" stroke="#E11D48" marker-end="url(#arrow-rose)" />
  <rect x="846" y="425" width="74" height="20" rx="4" fill="#FFE4E6" stroke="#FECDD3" class="dark-engine-rose" />
  <text x="883" y="439" fill="#9F1239" class="edge-label text-dark" text-anchor="middle">dispatch</text>

</svg>"""

    OUTPUT_UNIFIED.write_text(svg, encoding="utf-8")
    OUTPUT_LEGACY.write_text(svg, encoding="utf-8")
    print(f"Written SVG to {OUTPUT_UNIFIED} and {OUTPUT_LEGACY}")


if __name__ == "__main__":
    build_diagram()
