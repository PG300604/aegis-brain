"""Generate an Excalidraw-style Architecture Diagram for AegisBrain.

Creates a friendly, human-drawn, warm whiteboard-style architecture diagram
with organic pastel shapes, curved connectors, and clean typographic labels.
"""

from pathlib import Path

OUTPUT_PATH = Path("P:/open-source/aegis-brain/assets/architecture-excalidraw.svg")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def generate_svg():
    width = 1160
    height = 540

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      .bg {{ fill: #FFFFFF; }}
      .box-frame {{ stroke: #94A3B8; stroke-width: 1.8; stroke-dasharray: 6,6; fill: #F8FAFC; rx: 14; }}
      .label-zone {{ font-family: 'Virgil', 'Comic Sans MS', 'Caveat', -apple-system, sans-serif; font-size: 13px; font-weight: 700; fill: #64748B; letter-spacing: 1px; }}
      .card-title {{ font-family: 'Virgil', 'Comic Sans MS', -apple-system, sans-serif; font-size: 15px; font-weight: 700; }}
      .card-sub {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; font-weight: 500; opacity: 0.85; }}
      .edge-label {{ font-family: 'Virgil', 'Comic Sans MS', -apple-system, sans-serif; font-size: 11px; font-weight: 600; }}
      .arrow {{ stroke-width: 2; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
      
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

  <!-- ========================================== -->
  <!-- ZONE 1: AI CODING AGENTS (LEFT COLUMN)      -->
  <!-- ========================================== -->
  <rect x="30" y="30" width="220" height="480" class="box-frame" />
  <text x="50" y="60" class="label-zone">AI CODING AGENTS</text>

  <!-- Agent Card 1: Antigravity -->
  <g transform="translate(50, 80)">
    <rect width="180" height="64" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" />
    <text x="18" y="28" fill="#0369A1" class="card-title">Google Antigravity</text>
    <text x="18" y="46" fill="#0284C7" class="card-sub">Claude 3.7 / Gemini 2.5</text>
  </g>

  <!-- Agent Card 2: Claude Code -->
  <g transform="translate(50, 160)">
    <rect width="180" height="64" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" />
    <text x="18" y="28" fill="#0369A1" class="card-title">Anthropic Claude Code</text>
    <text x="18" y="46" fill="#0284C7" class="card-sub">CLI agent &amp; tools</text>
  </g>

  <!-- Agent Card 3: OpenAI Codex & Cursor -->
  <g transform="translate(50, 240)">
    <rect width="180" height="64" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" />
    <text x="18" y="28" fill="#0369A1" class="card-title">Codex &amp; Cursor</text>
    <text x="18" y="46" fill="#0284C7" class="card-sub">IDE prompt hooks</text>
  </g>

  <!-- Agent Card 4: Hermes Agent -->
  <g transform="translate(50, 320)">
    <rect width="180" height="64" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" />
    <text x="18" y="28" fill="#0369A1" class="card-title">Nous Hermes Agent</text>
    <text x="18" y="46" fill="#0284C7" class="card-sub">Thinking &amp; fallbacks</text>
  </g>

  <!-- Agent Card 5: Aider & Terminal -->
  <g transform="translate(50, 400)">
    <rect width="180" height="64" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" />
    <text x="18" y="28" fill="#0369A1" class="card-title">Aider &amp; OpenCode</text>
    <text x="18" y="46" fill="#0284C7" class="card-sub">Terminal coding agents</text>
  </g>

  <!-- ========================================== -->
  <!-- ZONE 2: AEGIS CORE DAEMON (CENTER COLUMN)  -->
  <!-- ========================================== -->
  <rect x="350" y="30" width="450" height="480" class="box-frame" />
  <text x="370" y="60" class="label-zone">AEGISBRAIN DAEMON (127.0.0.1:8765)</text>

  <!-- Core Module 1: Context Governor -->
  <g transform="translate(370, 80)">
    <rect width="410" height="85" rx="10" fill="#FEF3C7" stroke="#D97706" stroke-width="2" />
    <text x="22" y="32" fill="#B45309" class="card-title">Deterministic Context Governor</text>
    <text x="22" y="52" fill="#92400E" class="card-sub">Prunes git diffs, commits, &amp; tracked PRs</text>
    <rect x="22" y="60" width="160" height="18" rx="4" fill="#FDE68A" />
    <text x="28" y="73" fill="#78350F" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Strict ≤ 400 Token Cap</text>
  </g>

  <!-- Core Module 2: Neural Memory Bus -->
  <g transform="translate(370, 185)">
    <rect width="410" height="85" rx="10" fill="#D1FAE5" stroke="#059669" stroke-width="2" />
    <text x="22" y="32" fill="#047857" class="card-title">Neural Memory Bus (SQLite 3)</text>
    <text x="22" y="52" fill="#065F46" class="card-sub">WAL Mode + FTS5 Synchronized Triggers</text>
    <rect x="22" y="60" width="180" height="18" rx="4" fill="#A7F3D0" />
    <text x="28" y="73" fill="#064E3B" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Sub-0.5ms Memory Recall</text>
  </g>

  <!-- Core Module 3: Skill Distiller & Proxy -->
  <g transform="translate(370, 290)">
    <rect width="410" height="85" rx="10" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2" />
    <text x="22" y="32" fill="#6D28D9" class="card-title">Cross-Model Skill Distiller</text>
    <text x="22" y="52" fill="#5B21B6" class="card-sub">OpenAI-compatible /v1 prompt augmentation proxy</text>
    <rect x="22" y="60" width="195" height="18" rx="4" fill="#DDD6FE" />
    <text x="28" y="73" fill="#4C1D95" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Injects 500+ Skills to Ollama</text>
  </g>

  <!-- Core Module 4: OpenHiggsfield Media Bridge -->
  <g transform="translate(370, 395)">
    <rect width="410" height="85" rx="10" fill="#FFE4E6" stroke="#E11D48" stroke-width="2" />
    <text x="22" y="32" fill="#BE123C" class="card-title">OpenHiggsfield Media Bridge</text>
    <text x="22" y="52" fill="#9F1239" class="card-sub">Stdlib image/video dispatch &amp; metadata indexing</text>
    <rect x="22" y="60" width="195" height="18" rx="4" fill="#FECDD3" />
    <text x="28" y="73" fill="#881337" font-family="ui-monospace, monospace" font-size="10" font-weight="700">Flux 2 / Seedance / Kling</text>
  </g>

  <!-- ========================================== -->
  <!-- ZONE 3: STORAGE & RUNTIMES (RIGHT COLUMN)  -->
  <!-- ========================================== -->
  <rect x="890" y="30" width="240" height="480" class="box-frame" />
  <text x="910" y="60" class="label-zone">LOCAL STORAGE &amp; MODELS</text>

  <!-- Target 1: ACTIVE_CONTEXT.md -->
  <g transform="translate(910, 85)">
    <rect width="200" height="74" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="2" />
    <text x="16" y="30" fill="#B45309" class="card-title">ACTIVE_CONTEXT.md</text>
    <text x="16" y="50" fill="#92400E" class="card-sub">~/.aegis-brain/</text>
    <text x="16" y="64" fill="#D97706" class="card-sub">Auto-read by agents</text>
  </g>

  <!-- Target 2: brain.db -->
  <g transform="translate(910, 190)">
    <rect width="200" height="74" rx="8" fill="#D1FAE5" stroke="#059669" stroke-width="2" />
    <text x="16" y="30" fill="#047857" class="card-title">brain.db (SQLite)</text>
    <text x="16" y="50" fill="#065F46" class="card-sub">WAL + FTS5 on disk</text>
    <text x="16" y="64" fill="#059669" class="card-sub">Bypassed in private mode</text>
  </g>

  <!-- Target 3: Local Ollama -->
  <g transform="translate(910, 295)">
    <rect width="200" height="74" rx="8" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2" />
    <text x="16" y="30" fill="#6D28D9" class="card-title">Local Ollama :11434</text>
    <text x="16" y="50" fill="#5B21B6" class="card-sub">qwen2.5-coder / deepseek</text>
    <text x="16" y="64" fill="#7C3AED" class="card-sub">Guided by distilled skills</text>
  </g>

  <!-- Target 4: OpenHiggsfield API -->
  <g transform="translate(910, 400)">
    <rect width="200" height="74" rx="8" fill="#FFE4E6" stroke="#E11D48" stroke-width="2" />
    <text x="16" y="30" fill="#BE123C" class="card-title">OpenHiggsfield API</text>
    <text x="16" y="50" fill="#9F1239" class="card-sub">openhiggsfield.ai</text>
    <text x="16" y="64" fill="#E11D48" class="card-sub">Photo &amp; video generation</text>
  </g>

  <!-- ========================================== -->
  <!-- HAND-DRAWN CONNECTING ARROWS               -->
  <!-- ========================================== -->
  <!-- Agents -> Aegis Daemon (Zone 1 to Zone 2) -->
  <path d="M 230 112 C 290 112, 310 115, 360 115" class="arrow" stroke="#0284C7" marker-end="url(#arrow-blue)" />
  <path d="M 230 192 C 290 192, 310 220, 360 220" class="arrow" stroke="#0284C7" marker-end="url(#arrow-blue)" />
  <path d="M 230 272 C 290 272, 310 320, 360 320" class="arrow" stroke="#0284C7" marker-end="url(#arrow-blue)" />
  <path d="M 230 352 C 290 352, 310 330, 360 330" class="arrow" stroke="#0284C7" marker-end="url(#arrow-blue)" />
  <path d="M 230 432 C 290 432, 310 430, 360 430" class="arrow" stroke="#0284C7" marker-end="url(#arrow-blue)" />

  <rect x="250" y="240" width="80" height="22" rx="4" fill="#F0F9FF" stroke="#BAE6FD" />
  <text x="290" y="255" fill="#0284C7" class="edge-label" text-anchor="middle">HTTP / CLI</text>

  <!-- Zone 2 to Zone 3 (Daemon to Targets) -->
  <!-- Governor -> ACTIVE_CONTEXT.md -->
  <path d="M 780 122 C 830 122, 860 122, 900 122" class="arrow" stroke="#D97706" marker-end="url(#arrow-amber)" />
  <rect x="800" y="110" width="76" height="20" rx="4" fill="#FEF3C7" stroke="#FDE68A" />
  <text x="838" y="124" fill="#92400E" class="edge-label" text-anchor="middle">compile</text>

  <!-- Memory Bus -> brain.db -->
  <path d="M 780 227 C 830 227, 860 227, 900 227" class="arrow" stroke="#059669" marker-end="url(#arrow-green)" />
  <rect x="800" y="215" width="76" height="20" rx="4" fill="#D1FAE5" stroke="#A7F3D0" />
  <text x="838" y="229" fill="#065F46" class="edge-label" text-anchor="middle">WAL sync</text>

  <!-- Skill Distiller -> Ollama -->
  <path d="M 780 332 C 830 332, 860 332, 900 332" class="arrow" stroke="#7C3AED" marker-end="url(#arrow-purple)" />
  <rect x="800" y="320" width="76" height="20" rx="4" fill="#EDE9FE" stroke="#DDD6FE" />
  <text x="838" y="334" fill="#5B21B6" class="edge-label" text-anchor="middle">:11434/v1</text>

  <!-- Media Bridge -> OpenHiggsfield -->
  <path d="M 780 437 C 830 437, 860 437, 900 437" class="arrow" stroke="#E11D48" marker-end="url(#arrow-rose)" />
  <rect x="800" y="425" width="76" height="20" rx="4" fill="#FFE4E6" stroke="#FECDD3" />
  <text x="838" y="439" fill="#9F1239" class="edge-label" text-anchor="middle">dispatch</text>

</svg>"""

    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Generated Excalidraw-style Architecture Diagram at: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_svg()
