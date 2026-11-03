"""Generate an Excalidraw-style Architecture Diagram for AegisBrain.

Creates a friendly, human-drawn, warm whiteboard-style architecture diagram
showing a SINGLE unified coding agent client box connecting via ONE common bus
to the AegisBrain Daemon, where ALL features are universally accessible to all agents,
with downstream arrows dispatching to dedicated storage and runtimes.
"""

import json
from pathlib import Path

SVG_PATH = Path("P:/open-source/aegis-brain/assets/architecture-excalidraw.svg")
EXCALIDRAW_JSON_PATH = Path("P:/open-source/aegis-brain/assets/architecture.excalidraw")
SVG_PATH.parent.mkdir(parents=True, exist_ok=True)


def generate_diagram():
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
      
      @media (prefers-color-scheme: dark) {{
        .bg {{ fill: #0B0D11; }}
        .box-frame {{ fill: #11141C; stroke: #334155; }}
        .label-zone {{ fill: #94A3B8; }}
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
  <rect x="25" y="30" width="245" height="500" class="box-frame" />
  <text x="45" y="60" class="label-zone">AI CODING AGENTS (ANY RUNTIME)</text>

  <!-- Single Unified Client Box -->
  <g transform="translate(42, 80)">
    <rect width="210" height="430" rx="12" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.5" />
    
    <!-- Box Header -->
    <text x="16" y="32" fill="#0369A1" class="card-title" font-size="16">All AI Coding Agents</text>
    <text x="16" y="52" fill="#0284C7" class="card-sub">Irrespective of agent used</text>
    <line x1="16" y1="62" x2="194" y2="62" stroke="#BAE6FD" stroke-width="1.5" />

    <!-- Agent 1: Antigravity -->
    <g transform="translate(12, 74)">
      <rect width="186" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700">✦ Google Antigravity</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">Claude 3.7 / Gemini 2.5</text>
    </g>

    <!-- Agent 2: Claude Code -->
    <g transform="translate(12, 124)">
      <rect width="186" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700">✦ Anthropic Claude Code</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">CLI agent &amp; tools</text>
    </g>

    <!-- Agent 3: OpenAI Codex -->
    <g transform="translate(12, 174)">
      <rect width="186" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700">✦ OpenAI Codex CLI</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">CLI prompt hooks</text>
    </g>

    <!-- Agent 4: Cursor & Windsurf -->
    <g transform="translate(12, 224)">
      <rect width="186" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700">✦ Cursor &amp; Windsurf</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">.cursorrules / context</text>
    </g>

    <!-- Agent 5: Nous Hermes -->
    <g transform="translate(12, 274)">
      <rect width="186" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700">✦ Nous Hermes Agent</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">Autonomous reasoning</text>
    </g>

    <!-- Agent 6: Aider & OpenCode -->
    <g transform="translate(12, 324)">
      <rect width="186" height="42" rx="7" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="12" y="22" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="13" font-weight="700">✦ Aider &amp; OpenCode</text>
      <text x="12" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">Terminal pair programming</text>
    </g>

    <!-- Footer callout inside the single box -->
    <g transform="translate(12, 374)">
      <rect width="186" height="44" rx="6" fill="#E0F2FE" stroke="#7DD3FC" stroke-dasharray="3,3" />
      <text x="10" y="18" fill="#0369A1" font-family="'Virgil', 'Comic Sans MS', sans-serif" font-size="11" font-weight="700">Universal Memory Channel</text>
      <text x="10" y="34" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10">100% shared by all agents</text>
    </g>
  </g>

  <!-- ======================================================= -->
  <!-- THE ONE COMMON BUS ARROW (ZONE 1 TO ZONE 2)             -->
  <!-- ======================================================= -->
  <!-- Main connection arrow connecting single box to AegisBrain Daemon -->
  <path d="M 252 295 L 366 295" class="arrow" stroke="#0284C7" stroke-width="3.5" marker-end="url(#arrow-blue)" />

  <!-- Badge over the common arrow -->
  <g transform="translate(268, 256)">
    <rect width="84" height="66" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.8" />
    <text x="42" y="20" fill="#0369A1" class="edge-label" text-anchor="middle" font-size="10">COMMON BUS</text>
    <text x="42" y="35" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" text-anchor="middle">HTTP :8765</text>
    <text x="42" y="48" fill="#0284C7" font-family="ui-monospace, monospace" font-size="10" text-anchor="middle">CLI / Skills</text>
    <text x="42" y="60" fill="#047857" font-family="ui-monospace, monospace" font-size="9" font-weight="700" text-anchor="middle">One Ingress</text>
  </g>

  <!-- ======================================================= -->
  <!-- ZONE 2: AEGIS CORE DAEMON CHASSIS (CENTER)              -->
  <!-- ======================================================= -->
  <rect x="370" y="30" width="460" height="500" class="box-frame" />
  <text x="390" y="60" class="label-zone">AEGISBRAIN DAEMON (127.0.0.1:8765)</text>
  <text x="810" y="60" fill="#059669" font-family="ui-monospace, monospace" font-size="11" font-weight="700" text-anchor="end">● DAEMON ACTIVE</text>

  <!-- Internal Distribution Spine (Universal Access for All Connected Agents) -->
  <path d="M 370 295 L 396 295" stroke="#0284C7" stroke-width="2.5" />
  <path d="M 396 122 L 396 437" stroke="#0284C7" stroke-width="2.5" stroke-dasharray="4,4" />

  <!-- Branches to all 4 engines -->
  <path d="M 396 122 L 416 122" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />
  <path d="M 396 227 L 416 227" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />
  <path d="M 396 332 L 416 332" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />
  <path d="M 396 437 L 416 437" stroke="#0284C7" stroke-width="2" marker-end="url(#arrow-blue)" />

  <!-- Core Engine 1: Context Governor -->
  <g transform="translate(416, 80)">
    <rect width="395" height="85" rx="10" fill="#FEF3C7" stroke="#D97706" stroke-width="2" />
    <text x="20" y="30" fill="#B45309" class="card-title">Deterministic Context Governor</text>
    <text x="20" y="50" fill="#92400E" class="card-sub">Prunes git diffs, branch state, commits, &amp; tracked PRs</text>
    <rect x="20" y="58" width="185" height="18" rx="4" fill="#FDE68A" />
    <text x="26" y="71" fill="#78350F" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Strict ≤ 400 Token Cap | Auto-Load</text>
  </g>

  <!-- Core Engine 2: Neural Memory Bus & Instant Recall -->
  <g transform="translate(416, 185)">
    <rect width="395" height="85" rx="10" fill="#D1FAE5" stroke="#059669" stroke-width="2" />
    <text x="20" y="30" fill="#047857" class="card-title">Neural Memory Bus &amp; Instant Recall</text>
    <text x="20" y="50" fill="#065F46" class="card-sub">SQLite WAL + FTS5 full-text indexing with triggers</text>
    <rect x="20" y="58" width="220" height="18" rx="4" fill="#A7F3D0" />
    <text x="26" y="71" fill="#064E3B" font-family="ui-monospace, monospace" font-size="10" font-weight="700">&lt; 50ms Recall ('aegis recall') | 95%+ Save</text>
  </g>

  <!-- Core Engine 3: Skill Distiller & Proxy -->
  <g transform="translate(416, 290)">
    <rect width="395" height="85" rx="10" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2" />
    <text x="20" y="30" fill="#6D28D9" class="card-title">Cross-Model Skill Distiller &amp; Proxy</text>
    <text x="20" y="50" fill="#5B21B6" class="card-sub">OpenAI-compatible /v1 prompt augmentation reverse proxy</text>
    <rect x="20" y="58" width="200" height="18" rx="4" fill="#DDD6FE" />
    <text x="26" y="71" fill="#4C1D95" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Injects 500+ Skills to Local Models</text>
  </g>

  <!-- Core Engine 4: OpenHiggsfield Media Bridge -->
  <g transform="translate(416, 395)">
    <rect width="395" height="85" rx="10" fill="#FFE4E6" stroke="#E11D48" stroke-width="2" />
    <text x="20" y="30" fill="#BE123C" class="card-title">OpenHiggsfield Media Bridge</text>
    <text x="20" y="50" fill="#9F1239" class="card-sub">Zero-dependency stdlib image/video dispatch &amp; indexing</text>
    <rect x="20" y="58" width="200" height="18" rx="4" fill="#FECDD3" />
    <text x="26" y="71" fill="#881337" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Flux 2 / Seedance / Kling / Wan 2.6</text>
  </g>

  <!-- ======================================================= -->
  <!-- ZONE 3: STORAGE & TARGET RUNTIMES (RIGHT)               -->
  <!-- ======================================================= -->
  <rect x="910" y="30" width="245" height="500" class="box-frame" />
  <text x="930" y="60" class="label-zone">STORAGE &amp; TARGET RUNTIMES</text>

  <!-- Target 1: ACTIVE_CONTEXT.md -->
  <g transform="translate(930, 85)">
    <rect width="205" height="74" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="2" />
    <text x="16" y="28" fill="#B45309" class="card-title">ACTIVE_CONTEXT.md</text>
    <text x="16" y="48" fill="#92400E" class="card-sub">~/.aegis-brain/</text>
    <text x="16" y="62" fill="#D97706" class="card-sub">Auto-read by all agents</text>
  </g>

  <!-- Target 2: brain.db (SQLite) -->
  <g transform="translate(930, 190)">
    <rect width="205" height="74" rx="8" fill="#D1FAE5" stroke="#059669" stroke-width="2" />
    <text x="16" y="28" fill="#047857" class="card-title">brain.db (SQLite)</text>
    <text x="16" y="48" fill="#065F46" class="card-sub">WAL + FTS5 on disk</text>
    <text x="16" y="62" fill="#059669" class="card-sub">Bypassed in private mode</text>
  </g>

  <!-- Target 3: Local Ollama -->
  <g transform="translate(930, 295)">
    <rect width="205" height="74" rx="8" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2" />
    <text x="16" y="28" fill="#6D28D9" class="card-title">Local Ollama :11434</text>
    <text x="16" y="48" fill="#5B21B6" class="card-sub">qwen2.5-coder / deepseek</text>
    <text x="16" y="62" fill="#7C3AED" class="card-sub">Guided by distilled skills</text>
  </g>

  <!-- Target 4: OpenHiggsfield API -->
  <g transform="translate(930, 400)">
    <rect width="205" height="74" rx="8" fill="#FFE4E6" stroke="#E11D48" stroke-width="2" />
    <text x="16" y="28" fill="#BE123C" class="card-title">OpenHiggsfield API</text>
    <text x="16" y="48" fill="#9F1239" class="card-sub">openhiggsfield.ai</text>
    <text x="16" y="62" fill="#E11D48" class="card-sub">Photo &amp; video generation</text>
  </g>

  <!-- ======================================================= -->
  <!-- DOWNSTREAM ARROWS (ZONE 2 TO ZONE 3)                    -->
  <!-- ======================================================= -->
  <!-- Governor -> ACTIVE_CONTEXT.md -->
  <path d="M 811 122 L 926 122" class="arrow" stroke="#D97706" marker-end="url(#arrow-amber)" />
  <rect x="830" y="110" width="76" height="20" rx="4" fill="#FEF3C7" stroke="#FDE68A" />
  <text x="868" y="124" fill="#92400E" class="edge-label" text-anchor="middle">compile</text>

  <!-- Memory Bus -> brain.db -->
  <path d="M 811 227 L 926 227" class="arrow" stroke="#059669" marker-end="url(#arrow-green)" />
  <rect x="830" y="215" width="76" height="20" rx="4" fill="#D1FAE5" stroke="#A7F3D0" />
  <text x="868" y="229" fill="#065F46" class="edge-label" text-anchor="middle">WAL sync</text>

  <!-- Skill Distiller -> Ollama -->
  <path d="M 811 332 L 926 332" class="arrow" stroke="#7C3AED" marker-end="url(#arrow-purple)" />
  <rect x="830" y="320" width="76" height="20" rx="4" fill="#EDE9FE" stroke="#DDD6FE" />
  <text x="868" y="334" fill="#5B21B6" class="edge-label" text-anchor="middle">:11434/v1</text>

  <!-- Media Bridge -> OpenHiggsfield -->
  <path d="M 811 437 L 926 437" class="arrow" stroke="#E11D48" marker-end="url(#arrow-rose)" />
  <rect x="830" y="425" width="76" height="20" rx="4" fill="#FFE4E6" stroke="#FECDD3" />
  <text x="868" y="439" fill="#9F1239" class="edge-label" text-anchor="middle">dispatch</text>

</svg>"""

    SVG_PATH.write_text(svg, encoding="utf-8")
    print(f"Generated unified SVG Architecture Diagram at: {SVG_PATH}")

    # Also build the matching Excalidraw JSON file
    excalidraw_data = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://github.com/PG300604/aegis-brain",
        "elements": [
            {
                "id": "frame-clients",
                "type": "frame",
                "x": 25,
                "y": 30,
                "width": 245,
                "height": 500,
                "name": "AI Coding Agents (Any Runtime)",
                "strokeColor": "#94a3b8",
                "backgroundColor": "transparent"
            },
            {
                "id": "card-all-agents",
                "type": "rectangle",
                "x": 42,
                "y": 80,
                "width": 210,
                "height": 430,
                "strokeColor": "#0284c7",
                "backgroundColor": "#f0f9ff",
                "fillStyle": "solid",
                "strokeWidth": 2.5,
                "roughness": 1
            },
            {
                "id": "text-agents-header",
                "type": "text",
                "x": 58,
                "y": 105,
                "width": 180,
                "height": 25,
                "text": "All AI Coding Agents\n(Irrespective of agent)",
                "fontSize": 16,
                "fontFamily": 1,
                "textAlign": "left",
                "verticalAlign": "top"
            },
            {
                "id": "arrow-unified-bus",
                "type": "arrow",
                "x": 252,
                "y": 295,
                "width": 114,
                "height": 0,
                "strokeColor": "#0284c7",
                "strokeWidth": 3.5,
                "points": [[0, 0], [114, 0]]
            },
            {
                "id": "badge-common-bus",
                "type": "rectangle",
                "x": 268,
                "y": 256,
                "width": 84,
                "height": 66,
                "strokeColor": "#0284c7",
                "backgroundColor": "#ffffff",
                "fillStyle": "solid",
                "strokeWidth": 1.8
            },
            {
                "id": "frame-daemon",
                "type": "frame",
                "x": 370,
                "y": 30,
                "width": 460,
                "height": 500,
                "name": "AegisBrain Daemon (:8765)",
                "strokeColor": "#94a3b8",
                "backgroundColor": "transparent"
            },
            {
                "id": "card-governor",
                "type": "rectangle",
                "x": 416,
                "y": 80,
                "width": 395,
                "height": 85,
                "strokeColor": "#d97706",
                "backgroundColor": "#fef3c7",
                "fillStyle": "solid",
                "strokeWidth": 2
            },
            {
                "id": "card-memory",
                "type": "rectangle",
                "x": 416,
                "y": 185,
                "width": 395,
                "height": 85,
                "strokeColor": "#059669",
                "backgroundColor": "#d1fae5",
                "fillStyle": "solid",
                "strokeWidth": 2
            },
            {
                "id": "card-distiller",
                "type": "rectangle",
                "x": 416,
                "y": 290,
                "width": 395,
                "height": 85,
                "strokeColor": "#7c3aed",
                "backgroundColor": "#ede9fe",
                "fillStyle": "solid",
                "strokeWidth": 2
            },
            {
                "id": "card-media",
                "type": "rectangle",
                "x": 416,
                "y": 395,
                "width": 395,
                "height": 85,
                "strokeColor": "#e11d48",
                "backgroundColor": "#ffe4e6",
                "fillStyle": "solid",
                "strokeWidth": 2
            },
            {
                "id": "frame-storage",
                "type": "frame",
                "x": 910,
                "y": 30,
                "width": 245,
                "height": 500,
                "name": "Storage & Target Runtimes",
                "strokeColor": "#94a3b8",
                "backgroundColor": "transparent"
            },
            {
                "id": "card-context-md",
                "type": "rectangle",
                "x": 930,
                "y": 85,
                "width": 205,
                "height": 74,
                "strokeColor": "#d97706",
                "backgroundColor": "#fef3c7",
                "fillStyle": "solid"
            },
            {
                "id": "card-brain-db",
                "type": "rectangle",
                "x": 930,
                "y": 190,
                "width": 205,
                "height": 74,
                "strokeColor": "#059669",
                "backgroundColor": "#d1fae5",
                "fillStyle": "solid"
            },
            {
                "id": "card-ollama",
                "type": "rectangle",
                "x": 930,
                "y": 295,
                "width": 205,
                "height": 74,
                "strokeColor": "#7c3aed",
                "backgroundColor": "#ede9fe",
                "fillStyle": "solid"
            },
            {
                "id": "card-openhiggsfield",
                "type": "rectangle",
                "x": 930,
                "y": 400,
                "width": 205,
                "height": 74,
                "strokeColor": "#e11d48",
                "backgroundColor": "#ffe4e6",
                "fillStyle": "solid"
            }
        ]
    }

    EXCALIDRAW_JSON_PATH.write_text(json.dumps(excalidraw_data, indent=2), encoding="utf-8")
    print(f"Generated Excalidraw JSON Diagram at: {EXCALIDRAW_JSON_PATH}")


if __name__ == "__main__":
    generate_diagram()
