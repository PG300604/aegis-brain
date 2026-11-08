"""Generate authentic Data Professor style hand-drawn infographics for AegisBrain.

Follows the visual language of:
- Chanin Nantasenamat (Data Professor)
- AntV Infographic framework principles
- Warm sketchpad paper (#FDFBF7), organic charcoal strokes (#22252A), soft pastel marker highlights
"""

import math
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

FONT_IMPORT = """<![CDATA[
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&amp;family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
    
    .paper-bg { fill: #FDFBF7; }
    .ink { stroke: #22252A; stroke-linecap: round; stroke-linejoin: round; }
    .text-title { font-family: 'Patrick Hand', 'Caveat', 'Comic Sans MS', cursive, sans-serif; font-size: 26px; font-weight: 700; fill: #22252A; }
    .text-subtitle { font-family: 'Patrick Hand', 'Caveat', 'Comic Sans MS', cursive, sans-serif; font-size: 15px; fill: #52525B; }
    .text-heading { font-family: 'Patrick Hand', 'Caveat', 'Comic Sans MS', cursive, sans-serif; font-size: 18px; font-weight: 700; fill: #22252A; }
    .text-body { font-family: 'Patrick Hand', 'Caveat', 'Comic Sans MS', cursive, sans-serif; font-size: 14px; fill: #27272A; }
    .text-badge { font-family: 'Patrick Hand', 'Caveat', 'Comic Sans MS', cursive, sans-serif; font-size: 13px; font-weight: 700; }
    .text-mono { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; }
    .text-metric { font-family: 'Patrick Hand', 'Caveat', 'Comic Sans MS', cursive, sans-serif; font-size: 46px; font-weight: 700; }
]]>"""

def svg_header(width, height):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <defs>
    <style>{FONT_IMPORT}
    </style>
    <filter id="sketch-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="3" dy="4" stdDeviation="0" flood-color="#22252A" flood-opacity="0.15" />
    </filter>
  </defs>

  <!-- Warm Sketchpad Canvas Card -->
  <rect width="{width}" height="{height}" rx="20" class="paper-bg ink" stroke="#22252A" stroke-width="3" />
"""

def ribbon_banner(cx, y, w, h, title, subtitle=None):
    hw = w / 2
    x1 = cx - hw
    x2 = cx + hw
    fold = 24
    tail_w = 40
    
    lt = f"""
    <!-- Left Ribbon Tail -->
    <path d="M {x1} {y+8} L {x1-tail_w} {y+8} L {x1-tail_w+16} {y+h/2} L {x1-tail_w} {y+h-6} L {x1} {y+h-6} Z" 
          fill="#BAE6FD" stroke="#22252A" stroke-width="2.6" stroke-linejoin="round" />
    <!-- Left Fold Shadow Triangle -->
    <polygon points="{x1},{y+h-6} {x1},{y+h+12} {x1+fold},{y+h-6}" fill="#0284C7" stroke="#22252A" stroke-width="2" />
    """
    
    rt = f"""
    <!-- Right Ribbon Tail -->
    <path d="M {x2} {y+8} L {x2+tail_w} {y+8} L {x2+tail_w-16} {y+h/2} L {x2+tail_w} {y+h-6} L {x2} {y+h-6} Z" 
          fill="#BAE6FD" stroke="#22252A" stroke-width="2.6" stroke-linejoin="round" />
    <!-- Right Fold Shadow Triangle -->
    <polygon points="{x2},{y+h-6} {x2},{y+h+12} {x2-fold},{y+h-6}" fill="#0284C7" stroke="#22252A" stroke-width="2" />
    """
    
    main = f"""
    <!-- Main Center Banner -->
    <rect x="{x1}" y="{y}" width="{w}" height="{h}" rx="6" fill="#F0F9FF" stroke="#22252A" stroke-width="2.8" filter="url(#sketch-shadow)" />
    <!-- Inner Accent Line -->
    <rect x="{x1+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="4" fill="none" stroke="#BAE6FD" stroke-width="1.8" />
    <text x="{cx}" y="{y + (28 if subtitle else h/2 + 8)}" text-anchor="middle" class="text-title" fill="#0369A1">{title}</text>
    """
    if subtitle:
        main += f"""<text x="{cx}" y="{y+50}" text-anchor="middle" class="text-subtitle" fill="#475569">{subtitle}</text>"""
        
    return lt + rt + main

def cylinder_3d(cx, cy, rx, ry, h, fill_top, fill_body, label, sublabel=None):
    # Generous text spacing strictly between top ellipse bottom (cy + ry + 1.4) and body bottom
    label_y = cy + ry + 22
    sublabel_y = cy + ry + 39
    return f"""
    <g>
      <!-- Cylinder Shadow -->
      <ellipse cx="{cx+3}" cy="{cy+h+3}" rx="{rx}" ry="{ry}" fill="#E2E8F0" opacity="0.6" />
      
      <!-- Cylinder Body -->
      <path d="M {cx-rx} {cy} L {cx-rx} {cy+h} A {rx} {ry} 0 0 0 {cx+rx} {cy+h} L {cx+rx} {cy} Z" 
            fill="{fill_body}" stroke="#22252A" stroke-width="2.8" stroke-linejoin="round" />
      
      <!-- Cylinder Bottom Highlight Curve -->
      <path d="M {cx-rx+4} {cy+h-2} A {rx-4} {ry-2} 0 0 0 {cx+rx-4} {cy+h-2}" 
            fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.6" />
            
      <!-- Cylinder Top Ellipse -->
      <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill_top}" stroke="#22252A" stroke-width="2.8" />
      
      <!-- Highlight Reflection on Top -->
      <path d="M {cx-rx/2} {cy-ry/3} A {rx/2} {ry/2} 0 0 1 {cx+rx/3} {cy-ry/3}" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" />
      
      <!-- Labels positioned cleanly inside cylinder body with generous breathing room -->
      <text x="{cx}" y="{label_y}" text-anchor="middle" class="text-heading" font-size="14.5">{label}</text>
      {f'<text x="{cx}" y="{sublabel_y}" text-anchor="middle" class="text-body" font-size="11.5" fill="#52525B">{sublabel}</text>' if sublabel else ''}
    </g>
    """

def isometric_cube(x, y, s, fill_top, fill_left, fill_right, label=""):
    dx = s * 0.866
    dy = s * 0.5
    h = s
    
    top = f"{x},{y} {x+dx},{y+dy} {x},{y+2*dy} {x-dx},{y+dy}"
    left = f"{x-dx},{y+dy} {x},{y+2*dy} {x},{y+2*dy+h} {x-dx},{y+dy+h}"
    right = f"{x},{y+2*dy} {x+dx},{y+dy} {x+dx},{y+dy+h} {x},{y+2*dy+h}"
    
    return f"""
    <g>
      <!-- Shadow -->
      <polygon points="{x-dx+4},{y+dy+h+4} {x},{y+2*dy+h+6} {x+dx+4},{y+dy+h+4} {x},{y+2*dy+h+12}" fill="#CBD5E1" opacity="0.7" />
      <!-- Left Face -->
      <polygon points="{left}" fill="{fill_left}" stroke="#22252A" stroke-width="2.6" stroke-linejoin="round" />
      <!-- Right Face -->
      <polygon points="{right}" fill="{fill_right}" stroke="#22252A" stroke-width="2.6" stroke-linejoin="round" />
      <!-- Top Face -->
      <polygon points="{top}" fill="{fill_top}" stroke="#22252A" stroke-width="2.6" stroke-linejoin="round" />
      {f'<text x="{x}" y="{y+2*dy+h+24}" text-anchor="middle" class="text-heading">{label}</text>' if label else ''}
    </g>
    """

def hand_badge(x, y, w, h, fill_color, text, text_color="#22252A"):
    return f"""
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill_color}" stroke="#22252A" stroke-width="2.2" filter="url(#sketch-shadow)" />
      <text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" class="text-badge" fill="{text_color}">{text}</text>
    </g>
    """

def hand_arrow(x1, y1, x2, y2, label=None, label_side="right", color="#22252A", curve_dx=15):
    mx = (x1 + x2) / 2 + curve_dx
    my = (y1 + y2) / 2
    
    angle = math.atan2(y2 - my, x2 - mx)
    arrow_len = 12
    a1_x = x2 - arrow_len * math.cos(angle - math.pi/6)
    a1_y = y2 - arrow_len * math.sin(angle - math.pi/6)
    a2_x = x2 - arrow_len * math.cos(angle + math.pi/6)
    a2_y = y2 - arrow_len * math.sin(angle + math.pi/6)
    
    path = f"""
    <path d="M {x1} {y1} Q {mx} {my} {x2} {y2}" fill="none" stroke="{color}" stroke-width="2.6" stroke-linecap="round" />
    <polygon points="{x2},{y2} {a1_x},{a1_y} {a2_x},{a2_y}" fill="{color}" stroke="{color}" stroke-width="1" />
    """
    if label:
        lx = mx + (18 if label_side == "right" else -18)
        anchor = "start" if label_side == "right" else "end"
        path += f"""<text x="{lx}" y="{my+4}" text-anchor="{anchor}" class="text-body" fill="#3F3F46">{label}</text>"""
    return path

def footer_signature(y, width=1000):
    return f"""
    <!-- Clean Brand Signature -->
    <g transform="translate(40, {y})">
      <text x="0" y="24" class="text-heading" fill="#22252A">AegisBrain Autonomous Architecture</text>
      
      <g transform="translate(0, 34)">
        <rect x="0" y="0" width="60" height="26" rx="4" fill="#0284C7" stroke="#22252A" stroke-width="2" />
        <text x="30" y="18" text-anchor="middle" font-family="'Patrick Hand', cursive" font-weight="700" font-size="14" fill="#FFFFFF">AEGIS</text>
        
        <rect x="64" y="0" width="64" height="26" rx="4" fill="#22252A" stroke="#22252A" stroke-width="2" />
        <text x="96" y="18" text-anchor="middle" font-family="'Patrick Hand', cursive" font-weight="700" font-size="14" fill="#FFFFFF">BRAIN</text>
      </g>
      
      <text x="{width-80}" y="44" text-anchor="end" class="text-mono" font-size="12" fill="#71717A">github.com/PG300604/aegis-brain</text>
    </g>
    """


# ==========================================
# 1. UNIFIED ARCHITECTURE INFOGRAPHIC
# ==========================================
def build_unified_architecture():
    w, h = 1000, 1380
    svg = svg_header(w, h)
    
    # 1. Header Ribbon
    svg += ribbon_banner(500, 30, 740, 68, "AEGISBRAIN AUTONOMOUS ARCHITECTURE", 
                         "Deterministic Token Arbitrage, Neural FTS5 Memory &amp; 3-Tier Execution")
    
    # 2. Stage 1: Raw Session Logs & Transcripts
    svg += hand_badge(360, 125, 280, 36, "#FEF08A", "Raw Session Logs &amp; Transcripts")
    svg += cylinder_3d(500, 185, 90, 14, 76, "#FEF9C3", "#FEF08A", "transcript.jsonl", "Multi-MB Unstructured")
    
    # Exploratory Data Analysis Pill & Callouts
    svg += hand_arrow(595, 205, 715, 205, curve_dx=0)
    svg += hand_badge(715, 185, 230, 36, "#FED7AA", "Deterministic AST Parsing")
    svg += hand_arrow(830, 225, 780, 260, curve_dx=0)
    svg += hand_arrow(830, 225, 880, 260, curve_dx=0)
    svg += hand_badge(725, 265, 105, 30, "#E9D5FF", "AST Tree")
    svg += hand_badge(840, 265, 115, 30, "#BBF7D0", "Call Graph")
    
    # Downward Processing Arrows with annotations
    svg += hand_arrow(500, 276, 500, 350, curve_dx=0)
    svg += """
    <g transform="translate(525, 290)">
      <text x="0" y="0" class="text-body" fill="#22252A">↓ 1. Privacy Scrubbing (Zero Secret Leakage)</text>
      <text x="0" y="20" class="text-body" fill="#22252A">↓ 2. Conversational Slop &amp; Filler Pruning</text>
      <text x="0" y="40" class="text-body" fill="#22252A">↓ 3. Deterministic AST &amp; Event Chunking</text>
    </g>
    """
    
    # 3. Stage 2: Pre-processed Neural Memory (brain.db)
    svg += hand_badge(360, 355, 280, 36, "#E9D5FF", "Pre-Processed Neural Index")
    svg += cylinder_3d(500, 420, 100, 14, 76, "#F3E8FF", "#E9D5FF", "SQLite WAL + FTS5", "brain.db (Sub-Second Recall)")
    
    # Zoom-in lines to Fast Semantic Table on the left
    svg += f"""
    <!-- Table Zoom Projection Lines -->
    <path d="M 395 440 L 350 370" stroke="#8B5CF6" stroke-width="1.8" stroke-dasharray="4,4" />
    <path d="M 395 485 L 350 540" stroke="#8B5CF6" stroke-width="1.8" stroke-dasharray="4,4" />
    
    <!-- Fast Semantic Token Retrieval Matrix Table -->
    <g transform="translate(40, 360)">
      <rect x="0" y="0" width="300" height="185" rx="10" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Table Header -->
      <rect x="0" y="0" width="300" height="32" rx="10" fill="#FEF08A" stroke="#22252A" stroke-width="2.2" />
      <text x="150" y="22" text-anchor="middle" class="text-heading" fill="#22252A">Active Context Retrieval Matrix</text>
      
      <!-- Column Headers -->
      <rect x="0" y="32" width="55" height="26" fill="#FED7AA" stroke="#22252A" stroke-width="1.4" />
      <text x="27" y="50" text-anchor="middle" class="text-mono">T_ID</text>
      
      <rect x="55" y="32" width="60" height="26" fill="#FED7AA" stroke="#22252A" stroke-width="1.4" />
      <text x="85" y="50" text-anchor="middle" class="text-mono">Score</text>
      
      <rect x="115" y="32" width="115" height="26" fill="#FED7AA" stroke="#22252A" stroke-width="1.4" />
      <text x="172" y="50" text-anchor="middle" class="text-mono">Source</text>
      
      <rect x="230" y="32" width="70" height="26" fill="#E9D5FF" stroke="#22252A" stroke-width="1.4" />
      <text x="265" y="50" text-anchor="middle" class="text-mono">≤ 400 t</text>
      
      <!-- Row 1 -->
      <rect x="0" y="58" width="55" height="26" fill="#FFFFFF" stroke="#22252A" stroke-width="1" />
      <text x="27" y="76" text-anchor="middle" class="text-mono">T01</text>
      <rect x="55" y="58" width="60" height="26" fill="#FFFFFF" stroke="#22252A" stroke-width="1" />
      <text x="85" y="76" text-anchor="middle" class="text-mono">0.99</text>
      <rect x="115" y="58" width="115" height="26" fill="#FFFFFF" stroke="#22252A" stroke-width="1" />
      <text x="172" y="76" text-anchor="middle" class="text-mono">FTS5 Memory</text>
      <rect x="230" y="58" width="70" height="26" fill="#BBF7D0" stroke="#22252A" stroke-width="1" />
      <text x="265" y="76" text-anchor="middle" class="text-mono">42 t</text>
      
      <!-- Row 2 -->
      <rect x="0" y="84" width="55" height="26" fill="#FAF7F0" stroke="#22252A" stroke-width="1" />
      <text x="27" y="102" text-anchor="middle" class="text-mono">T02</text>
      <rect x="55" y="84" width="60" height="26" fill="#FAF7F0" stroke="#22252A" stroke-width="1" />
      <text x="85" y="102" text-anchor="middle" class="text-mono">0.95</text>
      <rect x="115" y="84" width="115" height="26" fill="#FAF7F0" stroke="#22252A" stroke-width="1" />
      <text x="172" y="102" text-anchor="middle" class="text-mono">Invariants</text>
      <rect x="230" y="84" width="70" height="26" fill="#BBF7D0" stroke="#22252A" stroke-width="1" />
      <text x="265" y="102" text-anchor="middle" class="text-mono">68 t</text>
      
      <!-- Row 3 -->
      <rect x="0" y="110" width="55" height="26" fill="#FFFFFF" stroke="#22252A" stroke-width="1" />
      <text x="27" y="128" text-anchor="middle" class="text-mono">T03</text>
      <rect x="55" y="110" width="60" height="26" fill="#FFFFFF" stroke="#22252A" stroke-width="1" />
      <text x="85" y="128" text-anchor="middle" class="text-mono">0.91</text>
      <rect x="115" y="110" width="115" height="26" fill="#FFFFFF" stroke="#22252A" stroke-width="1" />
      <text x="172" y="128" text-anchor="middle" class="text-mono">AST Symbols</text>
      <rect x="230" y="110" width="70" height="26" fill="#BBF7D0" stroke="#22252A" stroke-width="1" />
      <text x="265" y="128" text-anchor="middle" class="text-mono">75 t</text>
      
      <!-- Row 4 -->
      <rect x="0" y="136" width="55" height="26" fill="#FAF7F0" stroke="#22252A" stroke-width="1" />
      <text x="27" y="154" text-anchor="middle" class="text-mono">T04</text>
      <rect x="55" y="136" width="60" height="26" fill="#FAF7F0" stroke="#22252A" stroke-width="1" />
      <text x="85" y="154" text-anchor="middle" class="text-mono">0.88</text>
      <rect x="115" y="136" width="115" height="26" fill="#FAF7F0" stroke="#22252A" stroke-width="1" />
      <text x="172" y="154" text-anchor="middle" class="text-mono">Confidence</text>
      <rect x="230" y="136" width="70" height="26" fill="#BBF7D0" stroke="#22252A" stroke-width="1" />
      <text x="265" y="154" text-anchor="middle" class="text-mono">55 t</text>
      
      <!-- Table Footer Pill -->
      <rect x="10" y="165" width="280" height="16" rx="8" fill="#BBF7D0" />
      <text x="150" y="177" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">Pinned Active Context: 240 Tokens Total</text>
    </g>
    """
    
    # 4. Stage 3: Severity Scoring & 3-Tier Hierarchy Routing
    svg += hand_badge(340, 520, 320, 36, "#FED7AA", "Autonomous Severity Scoring &amp; Task Routing")
    
    # 3-Way Split Arrows
    svg += hand_arrow(430, 560, 180, 625, curve_dx=-15)
    svg += hand_arrow(500, 560, 500, 625, curve_dx=0)
    svg += hand_arrow(570, 560, 820, 625, curve_dx=15)
    
    # Tier 1 (Left): Frontier Manager
    svg += hand_badge(60, 630, 240, 34, "#FEF08A", "Tier 1: Senior Boss (Brain)")
    svg += isometric_cube(180, 680, 40, "#FEF08A", "#EAB308", "#CA8A04")
    svg += """
    <g transform="translate(60, 770)">
      <rect x="0" y="0" width="240" height="100" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2.2" />
      <text x="120" y="24" text-anchor="middle" class="text-heading" font-size="15" fill="#0369A1">Fable 5.1 / Opus 5.5 / Gemini 4 / Argon</text>
      <text x="120" y="46" text-anchor="middle" class="text-body">• High Cognition Architecture</text>
      <text x="120" y="66" text-anchor="middle" class="text-body">• Invariants &amp; Sign-off</text>
      <rect x="15" y="74" width="210" height="20" rx="4" fill="#BBF7D0" stroke="#15803D" stroke-width="1.2" />
      <text x="120" y="88" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">ZERO DIRECT CODE (0 Tokens)</text>
    </g>
    """
    
    # Tier 2 (Middle): Domain Subagents
    svg += hand_badge(380, 625, 240, 34, "#BAE6FD", "Tier 2: Junior Bosses (Leads)")
    svg += isometric_cube(500, 675, 40, "#BAE6FD", "#38BDF8", "#0284C7")
    svg += """
    <g transform="translate(380, 765)">
      <rect x="0" y="0" width="240" height="100" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2.2" />
      <text x="120" y="24" text-anchor="middle" class="text-heading" fill="#0369A1">Domain Specialists</text>
      <text x="120" y="46" text-anchor="middle" class="text-body">• Backend &amp; Frontend Leads</text>
      <text x="120" y="66" text-anchor="middle" class="text-body">• Security &amp; QA Auditors</text>
      <rect x="15" y="74" width="210" height="20" rx="4" fill="#E0F2FE" stroke="#0284C7" stroke-width="1.2" />
      <text x="120" y="88" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#0284C7">Worker Coaching Loops</text>
    </g>
    """
    
    # Tier 3 (Right): Execution Workers
    svg += hand_badge(700, 625, 240, 34, "#FED7AA", "Tier 3: Execution Workers")
    svg += isometric_cube(820, 675, 40, "#FED7AA", "#FB923C", "#EA580C")
    svg += """
    <g transform="translate(700, 765)">
      <rect x="0" y="0" width="240" height="100" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2.2" />
      <text x="120" y="24" text-anchor="middle" class="text-heading" fill="#C2410C">Hermes / Ollama / OpenCode</text>
      <text x="120" y="46" text-anchor="middle" class="text-body">• 100% Raw Code Implementation</text>
      <text x="120" y="66" text-anchor="middle" class="text-body">• Fast Parallel Drafts &amp; Tests</text>
      <rect x="15" y="74" width="210" height="20" rx="4" fill="#BBF7D0" stroke="#15803D" stroke-width="1.2" />
      <text x="120" y="88" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">FREE LOCAL TOKENS ($0.00)</text>
    </g>
    """
    
    # 5. Stage 4: 4-Decision Quality Architecture Gate
    svg += hand_arrow(500, 875, 500, 930, label="Candidate Code Filter", label_side="right")
    
    svg += """
    <!-- 4-Decision Quality Architecture Gate Card -->
    <g transform="translate(60, 935)">
      <rect x="0" y="0" width="880" height="210" rx="14" fill="#FEF9C3" stroke="#22252A" stroke-width="2.8" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon on Gate -->
      <rect x="260" y="-16" width="360" height="36" rx="18" fill="#EAB308" stroke="#22252A" stroke-width="2.4" />
      <text x="440" y="8" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="18" font-weight="700" fill="#FFFFFF">4-Decision Quality Architecture Gate</text>
      
      <!-- 4 Pillars Grid -->
      <g transform="translate(27, 36)">
        <!-- Gate 1: Karpathy Simplicity -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2" />
          <rect x="0" y="0" width="195" height="28" rx="8" fill="#BBF7D0" stroke="#22252A" stroke-width="1.6" />
          <text x="97" y="19" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700">1. Simplicity</text>
          <text x="97" y="48" text-anchor="middle" class="text-mono" font-size="11">Karpathy Doctrine</text>
          <text x="14" y="70" class="text-body" font-size="12">• Minimal lines of diff</text>
          <text x="14" y="90" class="text-body" font-size="12">• Zero speculative bloat</text>
          <text x="14" y="110" class="text-body" font-size="12">• Standard library first</text>
          <text x="14" y="130" class="text-body" font-size="12">• 50-line rewrite rule</text>
        </g>
        
        <!-- Gate 2: Unslop / TurnItOut -->
        <g transform="translate(210, 0)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2" />
          <rect x="0" y="0" width="195" height="28" rx="8" fill="#BAE6FD" stroke="#22252A" stroke-width="1.6" />
          <text x="97" y="19" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700">2. Unslop Master</text>
          <text x="97" y="48" text-anchor="middle" class="text-mono" font-size="11">TurnItOut Engine</text>
          <text x="14" y="70" class="text-body" font-size="12">• Strip conversational slop</text>
          <text x="14" y="90" class="text-body" font-size="12">• No polite preambles</text>
          <text x="14" y="110" class="text-body" font-size="12">• Zero sycophancy filler</text>
          <text x="14" y="130" class="text-body" font-size="12">• Pure executable code</text>
        </g>
        
        <!-- Gate 3: Red-Team Security -->
        <g transform="translate(420, 0)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2" />
          <rect x="0" y="0" width="195" height="28" rx="8" fill="#FECDD3" stroke="#22252A" stroke-width="1.6" />
          <text x="97" y="19" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700">3. Red-Team</text>
          <text x="97" y="48" text-anchor="middle" class="text-mono" font-size="11">Security Audit</text>
          <text x="14" y="70" class="text-body" font-size="12">• Block shell=True execution</text>
          <text x="14" y="90" class="text-body" font-size="12">• No hardcoded credentials</text>
          <text x="14" y="110" class="text-body" font-size="12">• Path traversal guards</text>
          <text x="14" y="130" class="text-body" font-size="12">• GitGuardian secret scan</text>
        </g>
        
        <!-- Gate 4: Dual-Env Verification -->
        <g transform="translate(630, 0)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="2" />
          <rect x="0" y="0" width="195" height="28" rx="8" fill="#E9D5FF" stroke="#22252A" stroke-width="1.6" />
          <text x="97" y="19" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700">4. Dual-Env Test</text>
          <text x="97" y="48" text-anchor="middle" class="text-mono" font-size="11">Verification Gate</text>
          <text x="14" y="70" class="text-body" font-size="12">• Isolated sandbox check</text>
          <text x="14" y="90" class="text-body" font-size="12">• Host pytest test suite</text>
          <text x="14" y="110" class="text-body" font-size="12">• 100% tests pass check</text>
          <text x="14" y="130" class="text-body" font-size="12">• Zero residue cleanup</text>
        </g>
      </g>
    </g>
    """
    
    # 6. Out of Gate Actions: Passing vs Error Coaching Loop
    svg += hand_arrow(360, 1150, 360, 1215, label="100% Tests Pass", label_side="left", color="#15803D")
    svg += hand_badge(230, 1220, 260, 36, "#BBF7D0", "Verified Clean Git Commit", "#15803D")
    
    # Coaching Feedback Loop (Curved cleanly on the outside, zero text crossing)
    svg += """
    <!-- Autonomous Coaching Feedback Loop -->
    <path d="M 945 1040 Q 995 925 945 815" fill="none" stroke="#EA580C" stroke-width="2.6" stroke-dasharray="6,4" />
    <polygon points="940,815 952,809 952,821" fill="#EA580C" stroke="#EA580C" />
    <g transform="translate(895, 875)">
      <rect x="0" y="0" width="88" height="46" rx="6" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.6" filter="url(#sketch-shadow)" />
      <text x="44" y="18" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="11" font-weight="700" fill="#EA580C">Flaw Detected?</text>
      <text x="44" y="32" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="10" fill="#7C2D12">Auto-Coaching Loop</text>
    </g>
    """
    
    # Side Floating Feature Badges
    svg += hand_badge(40, 1275, 285, 34, "#BAE6FD", "24/7 Mobile Bridge (@HHAACLIBot)", "#0369A1")
    svg += hand_badge(355, 1275, 285, 34, "#BBF7D0", "Deterministic Code Quality Gate", "#15803D")
    svg += hand_badge(675, 1275, 285, 34, "#FEF08A", "Sub-Second Recall (24ms)", "#854D0E")
    
    # Footer Signature
    svg += footer_signature(1320, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-unified-architecture.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# 2. SPEED BENCHMARKS INFOGRAPHIC
# ==========================================
def build_speed_benchmarks():
    w, h = 1040, 770
    svg = svg_header(w, h)
    
    # Header Ribbon
    svg += ribbon_banner(520, 30, 780, 68, "EMPIRICAL SPEED &amp; BENCHMARK REPORT", 
                         "AegisBrain SQLite WAL + FTS5 vs. Traditional Raw Log Crawling")
    
    card_y = 125
    card_w = 295
    card_h = 475
    
    # ---------------- Card 1: Speed & Latency ----------------
    x1 = 40
    svg += f"""
    <g transform="translate({x1}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="12" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Badge -->
      <rect x="25" y="-14" width="245" height="30" rx="15" fill="#BBF7D0" stroke="#22252A" stroke-width="2" />
      <text x="147" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700" fill="#15803D">SPEED &amp; RETRIEVAL LATENCY</text>
      
      <!-- Hand-Drawn Analog Stopwatches -->
      <g transform="translate(25, 45)">
        <!-- Stopwatch 1: Traditional -->
        <g transform="translate(10, 0)">
          <rect x="30" y="-8" width="10" height="8" rx="2" fill="#E2E8F0" stroke="#22252A" stroke-width="1.8" />
          <circle cx="35" cy="35" r="32" fill="#FEE2E2" stroke="#22252A" stroke-width="2.4" />
          <!-- Subtle motion lines on outer left margin only -->
          <path d="M 2 20 Q -6 15 -2 5" fill="none" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round" />
          <path d="M -2 32 Q -10 30 -6 18" fill="none" stroke="#EF4444" stroke-width="1.8" stroke-linecap="round" />
          <line x1="35" y1="35" x2="58" y2="22" stroke="#DC2626" stroke-width="2.6" stroke-linecap="round" />
          <circle cx="35" cy="35" r="3" fill="#22252A" />
          <text x="35" y="80" text-anchor="middle" class="text-heading" font-size="18" fill="#DC2626">12,400 ms</text>
          <text x="35" y="96" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#7F1D1D">Traditional Crawl</text>
        </g>
        
        <!-- Stopwatch 2: AegisBrain -->
        <g transform="translate(160, 0)">
          <rect x="30" y="-8" width="10" height="8" rx="2" fill="#E2E8F0" stroke="#22252A" stroke-width="1.8" />
          <circle cx="35" cy="35" r="32" fill="#DCFCE7" stroke="#22252A" stroke-width="2.4" />
          <line x1="35" y1="35" x2="35" y2="10" stroke="#16A34A" stroke-width="2.6" stroke-linecap="round" />
          <circle cx="35" cy="35" r="3" fill="#22252A" />
          <text x="62" y="16" font-size="15" fill="#16A34A">★</text>
          <text x="35" y="80" text-anchor="middle" class="text-heading" font-size="18" fill="#16A34A">24 ms</text>
          <text x="35" y="96" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#14532D">AegisBrain FTS5</text>
        </g>
      </g>
      
      <!-- Big Handwritten Stat -->
      <g transform="translate(147, 185)">
        <rect x="-110" y="-30" width="220" height="52" rx="26" fill="#FEF08A" stroke="#22252A" stroke-width="2" />
        <text x="0" y="8" text-anchor="middle" class="text-metric" fill="#854D0E">516x</text>
      </g>
      <text x="147" y="232" text-anchor="middle" class="text-heading" fill="#0369A1">FASTER RECALL</text>
      
      <!-- Hand-Drawn Comparison Bar Chart -->
      <g transform="translate(30, 255)">
        <text x="0" y="0" class="text-body" font-size="13">Traditional Crawl:</text>
        <rect x="0" y="8" width="235" height="20" rx="4" fill="#FCA5A5" stroke="#22252A" stroke-width="1.6" />
        <text x="225" y="23" text-anchor="end" class="text-mono" font-size="11" fill="#7F1D1D">12,400 ms (12.4s)</text>
        
        <text x="0" y="48" class="text-body" font-size="13">AegisBrain FTS5:</text>
        <rect x="0" y="56" width="30" height="20" rx="4" fill="#86EFAC" stroke="#22252A" stroke-width="1.6" />
        <text x="40" y="71" class="text-mono" font-size="11" fill="#14532D">24 ms (0.024s)</text>
      </g>
      
      <!-- Note & Badge -->
      <g transform="translate(18, 365)">
        <rect x="0" y="0" width="260" height="55" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.4" />
        <text x="130" y="22" text-anchor="middle" class="text-body" font-size="12">Instant SQLite FTS5 index lookup</text>
        <text x="130" y="40" text-anchor="middle" class="text-body" font-size="12">vs scanning multi-MB logs on disk</text>
      </g>
      
      <rect x="40" y="435" width="215" height="26" rx="13" fill="#BBF7D0" stroke="#15803D" stroke-width="1.4" />
      <text x="147" y="452" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">Sub-Second Response Guarantee</text>
    </g>
    """
    
    # ---------------- Card 2: Token Arbitrage ----------------
    x2 = 372
    svg += f"""
    <g transform="translate({x2}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="12" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Badge -->
      <rect x="25" y="-14" width="245" height="30" rx="15" fill="#FEF08A" stroke="#22252A" stroke-width="2" />
      <text x="147" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700" fill="#854D0E">TOKEN ARBITRAGE &amp; COST</text>
      
      <!-- Hand-Drawn Battery Illustrations -->
      <g transform="translate(45, 45)">
        <!-- Battery 1: Traditional -->
        <g transform="translate(15, 0)">
          <rect x="24" y="-6" width="12" height="6" rx="2" fill="#22252A" />
          <rect x="10" y="0" width="40" height="60" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="2.2" />
          <rect x="14" y="45" width="32" height="11" rx="3" fill="#EF4444" />
          <path d="M 30 15 L 24 30 L 34 30 L 26 44" fill="none" stroke="#DC2626" stroke-width="2" />
          <text x="30" y="80" text-anchor="middle" class="text-heading" fill="#DC2626">52,000 t</text>
          <text x="30" y="96" text-anchor="middle" class="text-mono" font-size="10" fill="#7F1D1D">Context Bloat</text>
        </g>
        
        <!-- Battery 2: AegisBrain -->
        <g transform="translate(130, 0)">
          <rect x="24" y="-6" width="12" height="6" rx="2" fill="#22252A" />
          <rect x="10" y="0" width="40" height="60" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="2.2" />
          <rect x="14" y="4" width="32" height="52" rx="3" fill="#22C55E" />
          <path d="M 22 30 L 28 36 L 38 22" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" />
          <text x="30" y="80" text-anchor="middle" class="text-heading" fill="#16A34A">240 t</text>
          <text x="30" y="96" text-anchor="middle" class="text-mono" font-size="10" fill="#14532D">Pinned Budget</text>
        </g>
      </g>
      
      <!-- Big Handwritten Stat -->
      <g transform="translate(147, 185)">
        <rect x="-110" y="-30" width="220" height="52" rx="26" fill="#BBF7D0" stroke="#22252A" stroke-width="2" />
        <text x="0" y="8" text-anchor="middle" class="text-metric" fill="#15803D">99.5%</text>
      </g>
      <text x="147" y="232" text-anchor="middle" class="text-heading" fill="#0369A1">TOKEN REDUCTION</text>
      
      <!-- Hand-Drawn Comparison Bar Chart -->
      <g transform="translate(30, 255)">
        <text x="0" y="0" class="text-body" font-size="13">Traditional Resend:</text>
        <rect x="0" y="8" width="235" height="20" rx="4" fill="#FCA5A5" stroke="#22252A" stroke-width="1.6" />
        <text x="225" y="23" text-anchor="end" class="text-mono" font-size="11" fill="#7F1D1D">52,000 tokens/req</text>
        
        <text x="0" y="48" class="text-body" font-size="13">AegisBrain Neural Pin:</text>
        <rect x="0" y="56" width="30" height="20" rx="4" fill="#86EFAC" stroke="#22252A" stroke-width="1.6" />
        <text x="40" y="71" class="text-mono" font-size="11" fill="#14532D">240 tokens/req</text>
      </g>
      
      <!-- Note & Badge -->
      <g transform="translate(18, 365)">
        <rect x="0" y="0" width="260" height="55" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.4" />
        <text x="130" y="22" text-anchor="middle" class="text-body" font-size="12">Working context pinned ≤ 400 t</text>
        <text x="130" y="40" text-anchor="middle" class="text-body" font-size="12">Zero runaway frontier API cost</text>
      </g>
      
      <rect x="40" y="435" width="215" height="26" rx="13" fill="#FEF08A" stroke="#854D0E" stroke-width="1.4" />
      <text x="147" y="452" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#854D0E">Zero Frontier Token Waste</text>
    </g>
    """
    
    # ---------------- Card 3: Hardware Footprint ----------------
    x3 = 705
    svg += f"""
    <g transform="translate({x3}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="12" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Badge -->
      <rect x="25" y="-14" width="245" height="30" rx="15" fill="#E9D5FF" stroke="#22252A" stroke-width="2" />
      <text x="147" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700" fill="#6B21A8">HARDWARE &amp; RAM FOOTPRINT</text>
      
      <!-- Hand-Drawn Balance Scale (Raised to give ample clearance above stat box) -->
      <g transform="translate(45, 25)">
        <polygon points="100,35 85,58 115,58" fill="#CBD5E1" stroke="#22252A" stroke-width="2.2" />
        <line x1="20" y1="50" x2="180" y2="18" stroke="#22252A" stroke-width="3" stroke-linecap="round" />
        
        <!-- Left Pan (Dumbbell) -->
        <line x1="20" y1="50" x2="20" y2="58" stroke="#22252A" stroke-width="1.6" />
        <rect x="5" y="58" width="30" height="12" rx="4" fill="#64748B" stroke="#22252A" stroke-width="1.8" />
        <text x="20" y="82" text-anchor="middle" class="text-heading" font-size="14" fill="#DC2626">&gt; 1.2 GB</text>
        <text x="20" y="94" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="11" fill="#7F1D1D">RAM Bloat</text>
        
        <!-- Right Pan (Feather) -->
        <line x1="180" y1="18" x2="180" y2="26" stroke="#22252A" stroke-width="1.6" />
        <path d="M 170 20 Q 185 8 195 22 Q 185 28 170 20" fill="#BAE6FD" stroke="#0284C7" stroke-width="1.6" />
        <line x1="170" y1="20" x2="195" y2="22" stroke="#0284C7" stroke-width="1.2" />
        <text x="180" y="50" text-anchor="middle" class="text-heading" font-size="14" fill="#16A34A">&lt; 25 MB</text>
        <text x="180" y="62" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="11" fill="#14532D">RAM Light</text>
      </g>
      
      <!-- Big Handwritten Stat -->
      <g transform="translate(147, 185)">
        <rect x="-110" y="-30" width="220" height="52" rx="26" fill="#BAE6FD" stroke="#22252A" stroke-width="2" />
        <text x="0" y="8" text-anchor="middle" class="text-metric" fill="#0369A1">48x</text>
      </g>
      <text x="147" y="232" text-anchor="middle" class="text-heading" fill="#0369A1">LIGHTER FOOTPRINT</text>
      
      <!-- Hand-Drawn Comparison Bar Chart -->
      <g transform="translate(30, 255)">
        <text x="0" y="0" class="text-body" font-size="13">In-Memory Transcript Scan:</text>
        <rect x="0" y="8" width="235" height="20" rx="4" fill="#FCA5A5" stroke="#22252A" stroke-width="1.6" />
        <text x="225" y="23" text-anchor="end" class="text-mono" font-size="11" fill="#7F1D1D">&gt; 1,200 MB RAM</text>
        
        <text x="0" y="48" class="text-body" font-size="13">AegisBrain Embedded SQLite:</text>
        <rect x="0" y="56" width="30" height="20" rx="4" fill="#86EFAC" stroke="#22252A" stroke-width="1.6" />
        <text x="40" y="71" class="text-mono" font-size="11" fill="#14532D">&lt; 25 MB RAM</text>
      </g>
      
      <!-- Note & Badge -->
      <g transform="translate(18, 365)">
        <rect x="0" y="0" width="260" height="55" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.4" />
        <text x="130" y="22" text-anchor="middle" class="text-body" font-size="12">Embedded C SQLite WAL engine</text>
        <text x="130" y="40" text-anchor="middle" class="text-body" font-size="12">Zero background RAM daemon bloat</text>
      </g>
      
      <rect x="40" y="435" width="215" height="26" rx="13" fill="#E9D5FF" stroke="#6B21A8" stroke-width="1.4" />
      <text x="147" y="452" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#6B21A8">Zero Background RAM Bloat</text>
    </g>
    """
    
    # ---------------- Bottom 4 Feature Badges ----------------
    by = 620
    bw = 220
    bh = 34
    svg += hand_badge(40, by, bw, bh, "#BBF7D0", "Zero External Dependencies", "#15803D")
    svg += hand_badge(285, by, bw, bh, "#BAE6FD", "Sub-Second FTS5 Retrieval", "#0369A1")
    svg += hand_badge(530, by, bw, bh, "#FEF08A", "Deterministic SQLite WAL", "#854D0E")
    svg += hand_badge(775, by, bw, bh, "#FED7AA", "Zero-Direct-Code Arbitrage", "#C2410C")
    
    # Footer Signature
    svg += footer_signature(680, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-speed-benchmarks.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# 3. LEARNING CURVE INFOGRAPHIC
# ==========================================
def build_learning_curve():
    w, h = 1040, 830
    svg = svg_header(w, h)
    
    # Colorful Block Letters at Top
    letters = [
        ('A', '#F43F5E', '#FFE4E6'),
        ('E', '#F97316', '#FFEDD5'),
        ('G', '#F59E0B', '#FEF3C7'),
        ('I', '#EAB308', '#FEF9C3'),
        ('S', '#22C55E', '#DCFCE7'),
        ('B', '#10B981', '#D1FAE5'),
        ('R', '#06B6D4', '#CFFAFE'),
        ('A', '#0EA5E9', '#E0F2FE'),
        ('I', '#8B5CF6', '#EDE9FE'),
        ('N', '#A855F7', '#F3E8FF')
    ]
    
    start_x = 295
    box_w = 42
    box_h = 46
    gap = 4
    
    svg += """<!-- Top Block Letters -->\n<g transform="translate(0, 30)">\n"""
    for idx, (char, text_col, bg_col) in enumerate(letters):
        bx = start_x + idx * (box_w + gap)
        svg += f"""
        <g transform="translate({bx}, 0)">
          <rect x="2" y="2" width="{box_w}" height="{box_h}" rx="6" fill="#22252A" opacity="0.15" />
          <rect x="0" y="0" width="{box_w}" height="{box_h}" rx="6" fill="{bg_col}" stroke="#22252A" stroke-width="2.4" />
          <text x="{box_w/2}" y="{box_h/2+8}" text-anchor="middle" font-family="'Patrick Hand', 'Comic Sans MS', cursive" font-size="28" font-weight="700" fill="{text_col}">{char}</text>
        </g>
        """
    svg += "</g>\n"
    
    # Subtitle Ribbon Under Block Letters
    svg += """
    <g transform="translate(520, 110)">
      <text x="0" y="0" text-anchor="middle" class="text-heading" font-size="24" fill="#22252A">CONTEXT RETENTION &amp; TOKEN BURN CURVE</text>
      <text x="0" y="22" text-anchor="middle" class="text-subtitle" fill="#52525B">Deterministic Token Arbitrage vs. Traditional Context Bloat</text>
    </g>
    """
    
    # Coordinate Axes
    ox = 140
    oy = 610
    ax_len_x = 810
    ax_len_y = 450
    
    svg += f"""
    <!-- Hand-Drawn Coordinate Axes -->
    <g>
      <!-- X-Axis -->
      <line x1="{ox}" y1="{oy}" x2="{ox+ax_len_x}" y2="{oy}" stroke="#22252A" stroke-width="3.2" stroke-linecap="round" />
      <polygon points="{ox+ax_len_x},{oy} {ox+ax_len_x-14},{oy-6} {ox+ax_len_x-14},{oy+6}" fill="#22252A" />
      
      <!-- X-Axis Title Placed Cleanly Below Callout Boxes -->
      <text x="{ox+ax_len_x/2}" y="730" text-anchor="middle" class="text-heading" font-size="20" fill="#22252A">CONVERSATION DEPTH / SESSION TURNS →</text>
      
      <!-- Y-Axis -->
      <line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-ax_len_y}" stroke="#22252A" stroke-width="3.2" stroke-linecap="round" />
      <polygon points="{ox},{oy-ax_len_y} {ox-6},{oy-ax_len_y+14} {ox+6},{oy-ax_len_y+14}" fill="#22252A" />
      
      <!-- Rotated Y-Axis Label (Pushed further left with generous margin) -->
      <text transform="translate({ox-50}, {oy-ax_len_y/2}) rotate(-90)" text-anchor="middle" class="text-heading" font-size="18" fill="#22252A">CONTEXT PRESSURE / TOKEN BURN</text>
    </g>
    """
    
    # Curve 1: Traditional Unbounded Context Bloat
    svg += f"""
    <!-- Curve 1: Traditional Context Bloat -->
    <path d="M {ox} 580 Q 320 540 480 390 T 750 220 T 870 170" fill="none" stroke="#FCA5A5" stroke-width="12" stroke-linecap="round" opacity="0.6" />
    <path d="M {ox} 580 Q 320 540 480 390 T 750 220 T 870 170" fill="none" stroke="#DC2626" stroke-width="3.6" stroke-linecap="round" />
    
    <!-- End dots -->
    <circle cx="875" cy="168" r="4" fill="#DC2626" />
    <circle cx="887" cy="166" r="4" fill="#DC2626" />
    <circle cx="899" cy="164" r="4" fill="#DC2626" />
    
    <!-- Traditional Callout Box 1 (Raised well above the red curve) -->
    <g transform="translate(195, 315)">
      <rect x="0" y="0" width="200" height="58" rx="8" fill="#FFEDD5" stroke="#EA580C" stroke-width="2.2" filter="url(#sketch-shadow)" />
      <text x="100" y="24" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#9A3412">Turn 5 to 10 Slowdown:</text>
      <text x="100" y="42" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#7C2D12">Full transcript re-read latency</text>
      <path d="M 100 58 Q 110 85 125 110" fill="none" stroke="#EA580C" stroke-width="2" />
      <polygon points="125,110 115,106 120,99" fill="#EA580C" />
    </g>
    
    <!-- Traditional Callout Box 2 (Steep rise) -->
    <g transform="translate(420, 240)">
      <rect x="0" y="0" width="220" height="70" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="2.2" filter="url(#sketch-shadow)" />
      <text x="110" y="24" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#991B1B">Turn 20+ Explosion:</text>
      <text x="110" y="42" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#7F1D1D">60k+ tokens resent every prompt</text>
      <text x="110" y="58" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#B91C1C">Frontier token costs skyrocket!</text>
      <path d="M 110 70 Q 115 85 125 100" fill="none" stroke="#DC2626" stroke-width="2" />
      <polygon points="125,100 117,95 121,90" fill="#DC2626" />
    </g>
    
    <!-- Traditional Callout Box 3 (Top peak) -->
    <g transform="translate(720, 115)">
      <rect x="0" y="0" width="230" height="75" rx="8" fill="#FFE4E6" stroke="#E11D48" stroke-width="2.2" filter="url(#sketch-shadow)" />
      <text x="115" y="24" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700" fill="#9F1239">Context Overflow Crash:</text>
      <text x="115" y="44" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#881337">Hallucinations begin, rules</text>
      <text x="115" y="60" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#881337">forgotten, model degrades</text>
      <path d="M 115 75 Q 120 85 130 95" fill="none" stroke="#E11D48" stroke-width="2" />
      <polygon points="130,95 122,90 126,85" fill="#E11D48" />
    </g>
    """
    
    # Curve 2: AegisBrain Pinned Active Context (<= 400 Tokens)
    svg += f"""
    <!-- Curve 2: AegisBrain Pinned Active Context -->
    <rect x="{ox}" y="565" width="{ax_len_x}" height="45" fill="#DCFCE7" opacity="0.4" />
    
    <line x1="{ox}" y1="575" x2="{ox+ax_len_x}" y2="575" stroke="#86EFAC" stroke-width="12" stroke-linecap="round" />
    <line x1="{ox}" y1="575" x2="{ox+ax_len_x}" y2="575" stroke="#16A34A" stroke-width="3.6" stroke-linecap="round" />
    
    <!-- AegisBrain Callout Box 1 (Left) -->
    <g transform="translate(170, 635)">
      <rect x="0" y="0" width="300" height="58" rx="8" fill="#DCFCE7" stroke="#16A34A" stroke-width="2.2" filter="url(#sketch-shadow)" />
      <text x="150" y="24" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700" fill="#14532D">Turn 1 to Turn 1,000+ Pinned:</text>
      <text x="150" y="44" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#166534">Active working context strictly pinned ≤ 400 t</text>
      <path d="M 150 0 Q 150 -15 150 -58" fill="none" stroke="#16A34A" stroke-width="2" />
      <polygon points="150,-58 145,-48 155,-48" fill="#16A34A" />
    </g>
    
    <!-- AegisBrain Callout Box 2 (Right) -->
    <g transform="translate(530, 635)">
      <rect x="0" y="0" width="340" height="58" rx="8" fill="#DCFCE7" stroke="#16A34A" stroke-width="2.2" filter="url(#sketch-shadow)" />
      <text x="170" y="24" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="14" font-weight="700" fill="#14532D">SQLite WAL + FTS5 Neural Index:</text>
      <text x="170" y="44" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#166534">Recalls exact relevant facts in 24ms with 0 bloat</text>
      <path d="M 170 0 Q 170 -15 170 -58" fill="none" stroke="#16A34A" stroke-width="2" />
      <polygon points="170,-58 165,-48 175,-48" fill="#16A34A" />
    </g>
    """
    
    # Footer Signature
    svg += footer_signature(770, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-learning-curve.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# 4. HIERARCHY PYRAMID INFOGRAPHIC
# ==========================================
def build_hierarchy_pyramid():
    w, h = 1040, 870
    svg = svg_header(w, h)
    
    # Header Ribbon
    svg += ribbon_banner(520, 30, 780, 68, "3-TIER MULTI-AGENT HIERARCHY", 
                         "Strict Token Arbitrage Architecture &amp; Autonomous Error-Reduction Coaching Loop")
    
    # ---------------- Tier 1: Senior Boss (Brain) ----------------
    t1_y = 125
    t1_w = 700
    t1_h = 155
    t1_x = (w - t1_w) / 2
    
    svg += f"""
    <!-- Tier 1 Card: Senior Boss -->
    <g transform="translate({t1_x}, {t1_y})">
      <rect x="0" y="0" width="{t1_w}" height="{t1_h}" rx="14" fill="#FFFBEB" stroke="#22252A" stroke-width="2.8" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="180" y="-14" width="340" height="30" rx="15" fill="#FEF08A" stroke="#22252A" stroke-width="2" />
      <text x="350" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="15" font-weight="700" fill="#854D0E">TIER 1: SENIOR BOSS (THE BRAIN)</text>
      
      <!-- Isometric Gold Cube & Crown Icon on Left -->
      <g transform="translate(65, 40)">
        {isometric_cube(0, 0, 32, "#FEF08A", "#EAB308", "#CA8A04")}
        <text x="0" y="-12" text-anchor="middle" font-size="22">👑</text>
      </g>
      
      <!-- Details -->
      <g transform="translate(145, 32)">
        <text x="0" y="16" class="text-heading" font-size="17" fill="#0369A1">Models: Fable 5.1 / Opus 5.5 / Gemini 4 / Argon</text>
        <text x="0" y="38" class="text-body">• High Cognition, System Architecture &amp; Strategy</text>
        <text x="0" y="58" class="text-body">• Invariants Definition, Error Detection &amp; Final Production Sign-off</text>
        
        <!-- Mandatory Invariant Badge -->
        <rect x="0" y="70" width="460" height="26" rx="13" fill="#BBF7D0" stroke="#15803D" stroke-width="1.4" />
        <text x="230" y="87" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">MANDATORY INVARIANT: ZERO DIRECT CODE GENERATED (0 Tokens)</text>
      </g>
    </g>
    """
    
    # Downward Arrow 1
    svg += hand_arrow(440, t1_y + t1_h, 440, t1_y + t1_h + 55, 
                      label="1. Decomposes tasks into strict invariants &amp; coaching rules", label_side="right", curve_dx=0)
    
    # ---------------- Tier 2: Junior Bosses (Domain Leads) ----------------
    t2_y = 335
    t2_w = 820
    t2_h = 165
    t2_x = (w - t2_w) / 2
    
    svg += f"""
    <!-- Tier 2 Card: Junior Bosses -->
    <g transform="translate({t2_x}, {t2_y})">
      <rect x="0" y="0" width="{t2_w}" height="{t2_h}" rx="14" fill="#F0F9FF" stroke="#22252A" stroke-width="2.8" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="240" y="-14" width="340" height="30" rx="15" fill="#BAE6FD" stroke="#22252A" stroke-width="2" />
      <text x="410" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="15" font-weight="700" fill="#0369A1">TIER 2: JUNIOR BOSSES (DOMAIN LEADS)</text>
      
      <!-- 3 Domain Specialists Modules -->
      <g transform="translate(35, 32)">
        <!-- Module 1: Backend Lead -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="235" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="235" height="24" rx="8" fill="#E0F2FE" stroke="#22252A" stroke-width="1.4" />
          <text x="117" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700">Backend &amp; DB Lead</text>
          <text x="12" y="42" class="text-body" font-size="12">• Schema contracts</text>
          <text x="12" y="60" class="text-body" font-size="12">• Formats worker prompts</text>
          <text x="12" y="78" class="text-body" font-size="12">• SQLite FTS5 neural index</text>
          <text x="12" y="96" class="text-body" font-size="12">• AST graph navigation</text>
        </g>
        
        <!-- Module 2: Frontend & Design Lead -->
        <g transform="translate(255, 0)">
          <rect x="0" y="0" width="235" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="235" height="24" rx="8" fill="#FEF08A" stroke="#22252A" stroke-width="1.4" />
          <text x="117" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700">UI-UX Design Lead</text>
          <text x="12" y="42" class="text-body" font-size="12">• UI UX Pro Max tokens</text>
          <text x="12" y="60" class="text-body" font-size="12">• Motion &amp; GSAP tiers</text>
          <text x="12" y="78" class="text-body" font-size="12">• Sketch &amp; vector styles</text>
          <text x="12" y="96" class="text-body" font-size="12">• Accessibility compliance</text>
        </g>
        
        <!-- Module 3: Security & QA Lead -->
        <g transform="translate(510, 0)">
          <rect x="0" y="0" width="235" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="235" height="24" rx="8" fill="#FECDD3" stroke="#22252A" stroke-width="1.4" />
          <text x="117" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700">Security &amp; QA Auditor</text>
          <text x="12" y="42" class="text-body" font-size="12">• 4-Decision Quality Gate</text>
          <text x="12" y="60" class="text-body" font-size="12">• Red-Team vulnerability scan</text>
          <text x="12" y="78" class="text-body" font-size="12">• GitGuardian secret audit</text>
          <text x="12" y="96" class="text-body" font-size="12">• Dual-env pytest testing</text>
        </g>
      </g>
    </g>
    """
    
    # Downward Arrow 2
    svg += hand_arrow(440, t2_y + t2_h, 440, t2_y + t2_h + 55, 
                      label="2. Dispatches CLI worker commands (hermes, ollama, opencode)", label_side="right", curve_dx=0)
    
    # ---------------- Tier 3: Execution Workers (Muscle) ----------------
    t3_y = 555
    t3_w = 940
    t3_h = 165
    t3_x = (w - t3_w) / 2
    
    svg += f"""
    <!-- Tier 3 Card: Execution Workers -->
    <g transform="translate({t3_x}, {t3_y})">
      <rect x="0" y="0" width="{t3_w}" height="{t3_h}" rx="14" fill="#F0FDF4" stroke="#22252A" stroke-width="2.8" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="280" y="-14" width="380" height="30" rx="15" fill="#BBF7D0" stroke="#22252A" stroke-width="2" />
      <text x="470" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="15" font-weight="700" fill="#15803D">TIER 3: EXECUTION WORKERS (THE MUSCLE)</text>
      
      <!-- 4 Fast Parallel Workers -->
      <g transform="translate(30, 32)">
        <!-- Worker 1: Hermes CLI -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="205" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="205" height="24" rx="8" fill="#FED7AA" stroke="#22252A" stroke-width="1.4" />
          <text x="102" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#9A3412">Hermes CLI</text>
          <text x="12" y="44" class="text-body" font-size="12">• Primary code engine</text>
          <text x="12" y="64" class="text-body" font-size="12">• hermes chat -q</text>
          <text x="12" y="84" class="text-body" font-size="12">• Rapid CLI execution</text>
          <text x="12" y="104" class="text-mono" font-size="10" fill="#15803D">✓ 100% Free Tokens</text>
        </g>
        
        <!-- Worker 2: Ollama Local MoE -->
        <g transform="translate(225, 0)">
          <rect x="0" y="0" width="205" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="205" height="24" rx="8" fill="#E9D5FF" stroke="#22252A" stroke-width="1.4" />
          <text x="102" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#6B21A8">Ollama (qwen2.5)</text>
          <text x="12" y="44" class="text-body" font-size="12">• Local MoE worker</text>
          <text x="12" y="64" class="text-body" font-size="12">• 100% Offline execution</text>
          <text x="12" y="84" class="text-body" font-size="12">• Zero data egress</text>
          <text x="12" y="104" class="text-mono" font-size="10" fill="#15803D">✓ 100% Free Tokens</text>
        </g>
        
        <!-- Worker 3: Claude Code CLI / Codex -->
        <g transform="translate(450, 0)">
          <rect x="0" y="0" width="205" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="205" height="24" rx="8" fill="#BAE6FD" stroke="#22252A" stroke-width="1.4" />
          <text x="102" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#0369A1">Claude Code / Codex</text>
          <text x="12" y="44" class="text-body" font-size="12">• Surgical diffs</text>
          <text x="12" y="64" class="text-body" font-size="12">• Terminal refactoring</text>
          <text x="12" y="84" class="text-body" font-size="12">• Git commit drafting</text>
          <text x="12" y="104" class="text-mono" font-size="10" fill="#15803D">✓ Token Arbitrage</text>
        </g>
        
        <!-- Worker 4: OpenCode Engine -->
        <g transform="translate(675, 0)">
          <rect x="0" y="0" width="205" height="115" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="205" height="24" rx="8" fill="#BBF7D0" stroke="#22252A" stroke-width="1.4" />
          <text x="102" y="17" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#15803D">OpenCode Engine</text>
          <text x="12" y="44" class="text-body" font-size="12">• Multi-model fallbacks</text>
          <text x="12" y="64" class="text-body" font-size="12">• Autonomous task worker</text>
          <text x="12" y="84" class="text-body" font-size="12">• Pytest generator</text>
          <text x="12" y="104" class="text-mono" font-size="10" fill="#15803D">✓ 100% Free Tokens</text>
        </g>
      </g>
    </g>
    """
    
    # Autonomous Coaching Feedback Loop (Right Side)
    svg += """
    <!-- Autonomous Coaching Feedback Loop Curve -->
    <path d="M 945 610 Q 995 500 995 420 Q 995 360 895 360" fill="none" stroke="#EA580C" stroke-width="3" stroke-dasharray="6,4" />
    <polygon points="895,360 907,354 907,366" fill="#EA580C" stroke="#EA580C" />
    
    <g transform="translate(930, 480)">
      <rect x="-40" y="-30" width="95" height="60" rx="8" fill="#FFF7ED" stroke="#EA580C" stroke-width="2" filter="url(#sketch-shadow)" />
      <text x="7" y="-10" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#EA580C">Loop Until 0</text>
      <text x="7" y="6" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#9A3412">Errors &amp; 100%</text>
      <text x="7" y="22" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" fill="#9A3412">Tests Pass!</text>
    </g>
    """
    
    # Bottom Badge
    svg += hand_badge(240, 740, 560, 36, "#FEF08A", "Continuous Learning Curve Persisted in brain.db (agent_confidence)", "#854D0E")
    
    # Footer Signature
    svg += footer_signature(795, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-hierarchy-pyramid.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# 5. MOBILE PIPELINE INFOGRAPHIC
# ==========================================
def build_mobile_pipeline():
    w, h = 1040, 800
    svg = svg_header(w, h)
    
    # Header Ribbon
    svg += ribbon_banner(520, 30, 780, 68, "24/7 MOBILE DAEMON &amp; VOICE PIPELINE", 
                         "Telegram Remote Operations • Sub-30s Audio Chunks • Win32 Process Shield")
    
    card_y = 125
    card_w = 225
    card_h = 490
    
    # ---------------- Stage 1: Smartphone UI ----------------
    x1 = 25
    svg += f"""
    <!-- Stage 1: Smartphone UI -->
    <g transform="translate({x1}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="16" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Badge -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#BAE6FD" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#0369A1">1. Telegram Mobile Bridge</text>
      
      <!-- Smartphone Silhouette -->
      <g transform="translate(20, 28)">
        <rect x="0" y="0" width="185" height="370" rx="20" fill="#FFFFFF" stroke="#22252A" stroke-width="2.6" />
        <rect x="67" y="8" width="50" height="6" rx="3" fill="#22252A" />
        
        <!-- Chat Header -->
        <rect x="6" y="22" width="173" height="28" rx="6" fill="#0284C7" />
        <text x="92" y="40" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#FFFFFF">@HHAACLIBot (24/7)</text>
        
        <!-- Speech Bubble 1: Voice Note -->
        <g transform="translate(12, 60)">
          <rect x="0" y="0" width="160" height="65" rx="10" fill="#E0F2FE" stroke="#0284C7" stroke-width="1.4" />
          <text x="10" y="20" font-size="18">🎙</text>
          <text x="32" y="20" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#0369A1">Voice Note (2:45)</text>
          <path d="M 12 45 L 18 35 L 24 50 L 30 30 L 36 55 L 42 35 L 48 50 L 54 38 L 60 48 L 66 32 L 72 52 L 78 40 L 84 46 L 90 35 L 96 52 L 102 42 L 108 48 L 114 36 L 120 45 L 140 45" 
                fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" />
        </g>
        
        <!-- Speech Bubble 2: /btw query -->
        <g transform="translate(12, 135)">
          <rect x="0" y="0" width="160" height="48" rx="10" fill="#FEF3C7" stroke="#D97706" stroke-width="1.4" />
          <text x="10" y="20" class="text-mono" font-size="11" fill="#B45309">/btw status</text>
          <text x="10" y="38" font-family="'Patrick Hand', cursive" font-size="11" fill="#78350F">In-flight memory query</text>
        </g>
        
        <!-- Speech Bubble 3: /type interrupt -->
        <g transform="translate(12, 195)">
          <rect x="0" y="0" width="160" height="52" rx="10" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.4" />
          <text x="10" y="20" class="text-mono" font-size="11" fill="#15803D">/type fix bug /alt+m</text>
          <text x="10" y="38" font-family="'Patrick Hand', cursive" font-size="11" fill="#14532D">Live session interrupt</text>
        </g>
        
        <line x1="67" y1="358" x2="117" y2="358" stroke="#94A3B8" stroke-width="3" stroke-linecap="round" />
      </g>
      
      <!-- Bottom Badge -->
      <rect x="15" y="445" width="195" height="26" rx="13" fill="#BAE6FD" stroke="#0284C7" stroke-width="1.4" />
      <text x="112" y="462" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#0369A1">Remote Hands-Free Ops</text>
    </g>
    """
    
    # Arrow 1 -> 2
    svg += hand_arrow(x1 + card_w, card_y + card_h/2 - 50, x1 + card_w + 30, card_y + card_h/2 - 50, curve_dx=0)
    
    # ---------------- Stage 2: 24/7 Daemon KeepAlive ----------------
    x2 = 280
    svg += f"""
    <!-- Stage 2: 24/7 Daemon KeepAlive -->
    <g transform="translate({x2}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="16" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Badge -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#FEF08A" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#854D0E">2. 24/7 Daemon KeepAlive</text>
      
      <!-- Cylinder Database -->
      <g transform="translate(112, 55)">
        {cylinder_3d(0, 0, 65, 13, 72, "#FEF9C3", "#FEF08A", "aegis.server", "127.0.0.1:8765")}
      </g>
      
      <!-- Bullet Points Box -->
      <g transform="translate(15, 165)">
        <rect x="0" y="0" width="195" height="225" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
        <text x="12" y="26" class="text-heading" font-size="14" fill="#0369A1">Windows Scheduled Task</text>
        <text x="12" y="46" class="text-body" font-size="12">• AegisBrainKeepAlive</text>
        <text x="12" y="66" class="text-body" font-size="12">• Runs every 5 mins silently</text>
        
        <text x="12" y="96" class="text-heading" font-size="14" fill="#0369A1">Zero Disruption</text>
        <text x="12" y="116" class="text-body" font-size="12">• Survives account switch</text>
        <text x="12" y="136" class="text-body" font-size="12">• Survives terminal close</text>
        <text x="12" y="156" class="text-body" font-size="12">• Survives PC reboots</text>
        
        <text x="12" y="186" class="text-body" font-size="12">• Async inbox queue</text>
        <text x="12" y="206" class="text-body" font-size="12">• SQLite telegram_inbox</text>
      </g>
      
      <!-- Bottom Badge -->
      <rect x="15" y="445" width="195" height="26" rx="13" fill="#FEF08A" stroke="#854D0E" stroke-width="1.4" />
      <text x="112" y="462" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#854D0E">Self-Resurrecting Daemon</text>
    </g>
    """
    
    # Arrow 2 -> 3
    svg += hand_arrow(x2 + card_w, card_y + card_h/2 - 50, x2 + card_w + 30, card_y + card_h/2 - 50, curve_dx=0)
    
    # ---------------- Stage 3: FFmpeg Stream Chunker ----------------
    x3 = 535
    svg += f"""
    <!-- Stage 3: FFmpeg Audio Stream Chunker -->
    <g transform="translate({x3}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="16" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Badge -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#FED7AA" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#C2410C">3. FFmpeg Sub-30s Audio</text>
      
      <!-- Hand-Drawn Audio Slices Diagram -->
      <g transform="translate(15, 30)">
        <rect x="0" y="0" width="195" height="155" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
        <text x="97" y="22" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#C2410C">30-Second Audio Slices</text>
        
        <!-- Slice 1 -->
        <g transform="translate(12, 34)">
          <rect x="0" y="0" width="171" height="32" rx="4" fill="#FFEDD5" stroke="#EA580C" stroke-width="1.2" />
          <text x="8" y="20" class="text-mono" font-size="10">chunk_001.wav [0:00-0:30]</text>
        </g>
        
        <!-- Slice 2 -->
        <g transform="translate(12, 72)">
          <rect x="0" y="0" width="171" height="32" rx="4" fill="#FFEDD5" stroke="#EA580C" stroke-width="1.2" />
          <text x="8" y="20" class="text-mono" font-size="10">chunk_002.wav [0:30-1:00]</text>
        </g>
        
        <!-- Slice 3 -->
        <g transform="translate(12, 110)">
          <rect x="0" y="0" width="171" height="32" rx="4" fill="#FFEDD5" stroke="#EA580C" stroke-width="1.2" />
          <text x="8" y="20" class="text-mono" font-size="10">chunk_003.wav [1:00-1:30]</text>
        </g>
      </g>
      
      <!-- Why This Matters Callout Box (Cleanly wrapped lines) -->
      <g transform="translate(15, 205)">
        <rect x="0" y="0" width="195" height="185" rx="8" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.8" />
        <text x="12" y="24" class="text-heading" font-size="13" fill="#9A3412">Why Chunk Audio?</text>
        <text x="12" y="44" class="text-body" font-size="11">• Prevents Whisper OOM crashes</text>
        <text x="12" y="62" class="text-body" font-size="11">• Eliminates hallucination loops</text>
        <text x="12" y="80" class="text-body" font-size="11">• Deterministic segmentation</text>
        <text x="12" y="98" class="text-body" font-size="11">• Sub-30s audio chunks</text>
        <text x="12" y="116" class="text-body" font-size="11">• 16kHz mono WAV format</text>
        <text x="12" y="134" class="text-body" font-size="11">• Zero speech truncation</text>
      </g>
      
      <!-- Bottom Badge -->
      <rect x="15" y="445" width="195" height="26" rx="13" fill="#FED7AA" stroke="#C2410C" stroke-width="1.4" />
      <text x="112" y="462" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#C2410C">Zero Hallucination Audio</text>
    </g>
    """
    
    # Arrow 3 -> 4
    svg += hand_arrow(x3 + card_w, card_y + card_h/2 - 50, x3 + card_w + 30, card_y + card_h/2 - 50, curve_dx=0)
    
    # ---------------- Stage 4: Whisper Greedy STT & Win32 Shield ----------------
    x4 = 790
    svg += f"""
    <!-- Stage 4: Whisper Greedy STT & Process Shield -->
    <g transform="translate({x4}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="16" fill="#FAF7F0" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Badge -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#E9D5FF" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#6B21A8">4. Whisper &amp; Win32 Shield</text>
      
      <!-- Whisper Greedy Decoding Box -->
      <g transform="translate(15, 28)">
        <rect x="0" y="0" width="195" height="160" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
        <text x="12" y="24" class="text-heading" font-size="14" fill="#6B21A8">Whisper Greedy Flags</text>
        
        <rect x="8" y="34" width="179" height="24" rx="4" fill="#F3E8FF" stroke="#A855F7" stroke-width="1" />
        <text x="14" y="50" class="text-mono" font-size="9" fill="#581C87">condition_on_prev=False</text>
        
        <rect x="8" y="64" width="179" height="24" rx="4" fill="#F3E8FF" stroke="#A855F7" stroke-width="1" />
        <text x="14" y="80" class="text-mono" font-size="9" fill="#581C87">temperature=0 (Greedy)</text>
        
        <rect x="8" y="94" width="179" height="24" rx="4" fill="#F3E8FF" stroke="#A855F7" stroke-width="1" />
        <text x="14" y="110" class="text-mono" font-size="9" fill="#581C87">beam_size=1 (Fast)</text>
        
        <text x="12" y="136" class="text-body" font-size="11">• Local whisper.exe execution</text>
        <text x="12" y="152" class="text-body" font-size="11">• 100% Deterministic STT</text>
      </g>
      
      <!-- Win32 Process-Tree Shield Box -->
      <g transform="translate(15, 205)">
        <rect x="0" y="0" width="195" height="185" rx="8" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.8" />
        <text x="12" y="24" class="text-heading" font-size="14" fill="#15803D">Win32 Process Shield</text>
        
        <!-- Shield Icon with Padlock -->
        <g transform="translate(97, 60)">
          <path d="M 0 -18 L 18 -10 L 18 10 Q 18 25 0 32 Q -18 25 -18 10 L -18 -10 Z" fill="#DCFCE7" stroke="#16A34A" stroke-width="2" />
          <circle cx="0" cy="5" r="4" fill="#15803D" />
          <line x1="0" y1="9" x2="0" y2="15" stroke="#15803D" stroke-width="2" />
        </g>
        
        <rect x="8" y="105" width="179" height="24" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1" />
        <text x="14" y="121" class="text-mono" font-size="9" fill="#14532D">taskkill /PID &lt;pid&gt; /T /F</text>
        
        <text x="12" y="145" class="text-body" font-size="11">• Win32 Job Objects</text>
        <text x="12" y="162" class="text-body" font-size="11">• Deep process reaping</text>
        <text x="12" y="178" class="text-body" font-size="11" font-weight="700" fill="#15803D">✓ 0 Orphan Processes</text>
      </g>
      
      <!-- Bottom Badge -->
      <rect x="15" y="445" width="195" height="26" rx="13" fill="#E9D5FF" stroke="#6B21A8" stroke-width="1.4" />
      <text x="112" y="462" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#6B21A8">Clean Win32 Lifecycle</text>
    </g>
    """
    
    # Bottom Wide Summary Banner
    svg += hand_badge(60, 640, 920, 38, "#BBF7D0", 
                      "Voice notes converted into validated prompts &amp; executed autonomously while away from desk!", "#15803D")
    
    # Footer Signature
    svg += footer_signature(720, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-mobile-pipeline.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# 6. UNIVERSAL AGENT INTERCHANGEABILITY INFOGRAPHIC
# ==========================================
def build_universal_agents():
    w, h = 1040, 720
    svg = svg_header(w, h)
    
    # Header Ribbon
    svg += ribbon_banner(520, 30, 840, 68, "UNIVERSAL AGENT INTERCHANGEABILITY PROTOCOL", 
                         "Standardized UniversalAgentEnvelope • Zero Tool Lock-In • Any Model as Boss or Worker")
    
    # ---------------- Row 1: Tier 1 Senior Boss Candidates ----------------
    svg += """
    <!-- Row 1: Tier 1 Boss Candidates -->
    <g transform="translate(40, 120)">
      <rect x="0" y="0" width="960" height="120" rx="14" fill="#FFFBEB" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="230" y="-14" width="500" height="28" rx="14" fill="#FEF08A" stroke="#22252A" stroke-width="2" />
      <text x="480" y="5" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#854D0E">TIER 1: SENIOR BOSS (COGNITION &amp; ARCHITECTURE) — SELECT ANY TOOL</text>
      
      <!-- 4 Boss Tool Candidates -->
      <g transform="translate(25, 28)">
        <!-- Boss 1: OpenCode -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#EDE9FE" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#6B21A8">OpenCode CLI</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Model: opus-5.5 / gpt-6-astra</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Cognition &amp; Planning</text>
        </g>
        
        <!-- Boss 2: OpenAI Codex -->
        <g transform="translate(232, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#EDE9FE" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#6B21A8">OpenAI Codex</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Model: codex-5.4 / fable-5.1</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Strategic Architecture</text>
        </g>
        
        <!-- Boss 3: Google Antigravity -->
        <g transform="translate(464, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#EDE9FE" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#6B21A8">Google Antigravity</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Model: gemini-4 / argon</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Autonomous Senior Boss</text>
        </g>
        
        <!-- Boss 4: Claude Code CLI -->
        <g transform="translate(696, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#EDE9FE" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#6B21A8">Claude Code CLI</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Model: opus-5.5 / claude-4</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Invariants &amp; Sign-Off</text>
        </g>
      </g>
    </g>
    """
    
    # Connecting Dual Side Arrows 1 -> Bus (Leaves center title ribbon completely unobstructed)
    svg += hand_arrow(200, 240, 200, 275, curve_dx=0)
    svg += hand_arrow(840, 240, 840, 275, curve_dx=0)
    
    # ---------------- Row 2: Standardized Execution Bus ----------------
    svg += """
    <!-- Row 2: Standardized Execution Protocol Bus -->
    <g transform="translate(40, 275)">
      <rect x="0" y="0" width="960" height="115" rx="14" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.6" stroke-dasharray="6,4" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="250" y="-14" width="460" height="28" rx="14" fill="#BAE6FD" stroke="#22252A" stroke-width="2" />
      <text x="480" y="5" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#0369A1">STANDARDIZED EXECUTION PROTOCOL (UniversalAgentEnvelope)</text>
      
      <!-- 4 Protocol Stages -->
      <g transform="translate(25, 26)">
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="215" height="66" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.6" />
          <text x="10" y="24" class="text-heading" font-size="13" fill="#0284C7">1. Normalized Payload</text>
          <text x="10" y="44" class="text-body" font-size="11" fill="#475569">Unified JSON schema</text>
          <text x="10" y="58" class="text-body" font-size="11" fill="#475569">across all agent runners</text>
        </g>
        
        <g transform="translate(232, 0)">
          <rect x="0" y="0" width="215" height="66" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.6" />
          <text x="10" y="24" class="text-heading" font-size="13" fill="#D97706">2. Quality Verification</text>
          <text x="10" y="44" class="text-body" font-size="11" fill="#475569">4-Gate architectural check</text>
          <text x="10" y="58" class="text-body" font-size="11" fill="#475569">Karpathy + Security + Test</text>
        </g>
        
        <g transform="translate(464, 0)">
          <rect x="0" y="0" width="215" height="66" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.6" />
          <text x="10" y="24" class="text-heading" font-size="13" fill="#7C3AED">3. Worker Coaching</text>
          <text x="10" y="44" class="text-body" font-size="11" fill="#475569">Targeted correction loop</text>
          <text x="10" y="58" class="text-body" font-size="11" fill="#475569">Error feedback dossiers</text>
        </g>
        
        <g transform="translate(696, 0)">
          <rect x="0" y="0" width="215" height="66" rx="6" fill="#FFFFFF" stroke="#22252A" stroke-width="1.6" />
          <text x="10" y="24" class="text-heading" font-size="13" fill="#15803D">4. Executive Sign-Off</text>
          <text x="10" y="44" class="text-body" font-size="11" fill="#475569">Verified git commit</text>
          <text x="10" y="58" class="text-body" font-size="11" fill="#475569">Production-grade delivery</text>
        </g>
      </g>
    </g>
    """
    
    # Connecting Dual Side Arrows Bus -> 3 (Leaves center title ribbon completely unobstructed)
    svg += hand_arrow(200, 390, 200, 425, curve_dx=0)
    svg += hand_arrow(840, 390, 840, 425, curve_dx=0)
    
    # ---------------- Row 3: Tier 3 Worker Candidates ----------------
    svg += """
    <!-- Row 3: Tier 3 Worker Candidates -->
    <g transform="translate(40, 425)">
      <rect x="0" y="0" width="960" height="120" rx="14" fill="#F0FDF4" stroke="#22252A" stroke-width="2.6" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon (Unobstructed Center Placement) -->
      <rect x="200" y="-14" width="560" height="28" rx="14" fill="#BBF7D0" stroke="#22252A" stroke-width="2" />
      <text x="480" y="5" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">TIER 3: WORKER CANDIDATES (100% RAW CODE &amp; TESTS) — FREE LOCAL TOKENS</text>
      
      <!-- 4 Worker Candidates -->
      <g transform="translate(25, 28)">
        <!-- Worker 1: Hermes CLI -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#FED7AA" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#9A3412">Hermes CLI</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Command: hermes chat -q</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Fast Boilerplate Drafts</text>
        </g>
        
        <!-- Worker 2: Ollama Local MoE -->
        <g transform="translate(232, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#E9D5FF" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#6B21A8">Ollama (qwen2.5)</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Model: qwen2.5-coder:7b</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ 100% Free Offline Tokens</text>
        </g>
        
        <!-- Worker 3: OpenCode Engine -->
        <g transform="translate(464, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#BBF7D0" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#15803D">OpenCode Engine</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Command: opencode run</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Autonomous Subagent</text>
        </g>
        
        <!-- Worker 4: Claude Code / Codex -->
        <g transform="translate(696, 0)">
          <rect x="0" y="0" width="215" height="72" rx="8" fill="#FFFFFF" stroke="#22252A" stroke-width="1.8" />
          <rect x="0" y="0" width="215" height="22" rx="8" fill="#BAE6FD" stroke="#22252A" stroke-width="1.2" />
          <text x="107" y="16" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="13" font-weight="700" fill="#0369A1">Claude Code / Codex</text>
          <text x="12" y="42" class="text-mono" font-size="10" fill="#4B5563">Command: claude -p / codex</text>
          <text x="12" y="60" class="text-body" font-size="11" fill="#15803D">✓ Surgical Diff Execution</text>
        </g>
      </g>
    </g>
    """
    
    # Bottom Badges
    svg += hand_badge(50, 575, 290, 34, "#BAE6FD", "Standardized JSON Payload Envelope", "#0369A1")
    svg += hand_badge(375, 575, 290, 34, "#BBF7D0", "Zero Vendor Lock-In Guarantee", "#15803D")
    svg += hand_badge(700, 575, 290, 34, "#FEF08A", "Dynamic Token &amp; Latency Arbitrage", "#854D0E")
    
    # Footer Signature
    svg += footer_signature(635, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-universal-agents.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# 7. 4-DECISION QUALITY ARCHITECTURE GATE INFOGRAPHIC
# ==========================================
def build_quality_gate():
    w, h = 1040, 720
    svg = svg_header(w, h)
    
    # Header Ribbon
    svg += ribbon_banner(520, 30, 840, 68, "4-DECISION QUALITY ARCHITECTURE GATE", 
                         "Candidate Code Filter • Zero AI Slop in Git • Red-Team Security &amp; Dual-Env Verification")
    
    # Subtitle Note
    svg += """
    <text x="520" y="115" text-anchor="middle" class="text-subtitle" fill="#52525B">
      Every worker candidate draft must pass all 4 gates before reaching senior models or git
    </text>
    """
    
    card_y = 135
    card_w = 225
    card_h = 390
    
    # ---------------- Gate 1: Surgical Simplicity ----------------
    x1 = 35
    svg += f"""
    <!-- Gate 1: Surgical Simplicity -->
    <g transform="translate({x1}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="14" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.4" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#BBF7D0" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12.5" font-weight="700" fill="#15803D">1. Surgical Simplicity</text>
      
      <text x="112" y="36" text-anchor="middle" class="text-heading" font-size="15" fill="#1E40AF">Karpathy Doctrine</text>
      <line x1="25" y1="46" x2="200" y2="46" stroke="#93C5FD" stroke-width="1.6" />
      
      <g transform="translate(14, 60)">
        <text x="0" y="0" class="text-body" font-size="12">• Minimal lines of diff</text>
        <text x="0" y="24" class="text-body" font-size="12">• Standard library first</text>
        <text x="0" y="48" class="text-body" font-size="12">• Zero speculative code</text>
        <text x="0" y="72" class="text-body" font-size="12">• Zero unreachable wrappers</text>
        <text x="0" y="96" class="text-body" font-size="12">• Touch only what is broken</text>
        <text x="0" y="120" class="text-body" font-size="12">• Clean up created orphans</text>
        <text x="0" y="148" class="text-body" font-size="12" font-weight="700" fill="#1E40AF">50-Line Rewrite Rule:</text>
        <text x="0" y="168" class="text-body" font-size="11" fill="#4B5563">If 200 lines could easily be 50,</text>
        <text x="0" y="184" class="text-body" font-size="11" fill="#4B5563">rewrite immediately.</text>
      </g>
      
      <rect x="25" y="340" width="175" height="26" rx="13" fill="#BBF7D0" stroke="#15803D" stroke-width="1.4" />
      <text x="112" y="357" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#15803D">Zero Over-Engineering</text>
    </g>
    """
    
    # Arrow 1 -> 2
    svg += hand_arrow(x1 + card_w, card_y + card_h/2 - 20, x1 + card_w + 25, card_y + card_h/2 - 20, curve_dx=0)
    
    # ---------------- Gate 2: Unslop Master ----------------
    x2 = 285
    svg += f"""
    <!-- Gate 2: Unslop Master -->
    <g transform="translate({x2}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="14" fill="#FAF5FF" stroke="#7C3AED" stroke-width="2.4" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#E9D5FF" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12.5" font-weight="700" fill="#6B21A8">2. Unslop Master</text>
      
      <text x="112" y="36" text-anchor="middle" class="text-heading" font-size="15" fill="#5B21B6">TurnItOut Engine</text>
      <line x1="25" y1="46" x2="200" y2="46" stroke="#D8B4FE" stroke-width="1.6" />
      
      <g transform="translate(14, 60)">
        <text x="0" y="0" class="text-body" font-size="12">• Strips conversational slop</text>
        <text x="0" y="24" class="text-body" font-size="12">• Removes "Certainly!", "Here is"</text>
        <text x="0" y="48" class="text-body" font-size="12">• Prunes polite preambles</text>
        <text x="0" y="72" class="text-body" font-size="12">• Removes chatty comments</text>
        <text x="0" y="96" class="text-body" font-size="12">• Eliminates sycophancy filler</text>
        <text x="0" y="120" class="text-body" font-size="12">• Pure executable code</text>
        <text x="0" y="148" class="text-body" font-size="12" font-weight="700" fill="#5B21B6">Zero Slop Guarantee:</text>
        <text x="0" y="168" class="text-body" font-size="11" fill="#4B5563">Zero AI watermarks or slop</text>
        <text x="0" y="184" class="text-body" font-size="11" fill="#4B5563">ever committed into git.</text>
      </g>
      
      <rect x="25" y="340" width="175" height="26" rx="13" fill="#E9D5FF" stroke="#6B21A8" stroke-width="1.4" />
      <text x="112" y="357" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#6B21A8">Human-Grade Code</text>
    </g>
    """
    
    # Arrow 2 -> 3
    svg += hand_arrow(x2 + card_w, card_y + card_h/2 - 20, x2 + card_w + 25, card_y + card_h/2 - 20, curve_dx=0)
    
    # ---------------- Gate 3: Red-Team Security ----------------
    x3 = 535
    svg += f"""
    <!-- Gate 3: Red-Team Security -->
    <g transform="translate({x3}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="14" fill="#FFF1F2" stroke="#E11D48" stroke-width="2.4" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#FECDD3" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12.5" font-weight="700" fill="#9F1239">3. Red-Team Security</text>
      
      <text x="112" y="36" text-anchor="middle" class="text-heading" font-size="15" fill="#9F1239">Vulnerability Guard</text>
      <line x1="25" y1="46" x2="200" y2="46" stroke="#FDA4AF" stroke-width="1.6" />
      
      <g transform="translate(14, 60)">
        <text x="0" y="0" class="text-body" font-size="12">• Blocks shell=True execution</text>
        <text x="0" y="24" class="text-body" font-size="12">• Blocks os.system() payloads</text>
        <text x="0" y="48" class="text-body" font-size="12">• Path traversal prevention</text>
        <text x="0" y="72" class="text-body" font-size="12">• GitGuardian secret scanner</text>
        <text x="0" y="96" class="text-body" font-size="12">• Injection vulnerability audit</text>
        <text x="0" y="120" class="text-body" font-size="12">• Host perimeter protection</text>
        <text x="0" y="148" class="text-body" font-size="12" font-weight="700" fill="#9F1239">Hard Boundary Defense:</text>
        <text x="0" y="168" class="text-body" font-size="11" fill="#4B5563">Blocks unverified network</text>
        <text x="0" y="184" class="text-body" font-size="11" fill="#4B5563">calls &amp; privilege elevation.</text>
      </g>
      
      <rect x="25" y="340" width="175" height="26" rx="13" fill="#FECDD3" stroke="#9F1239" stroke-width="1.4" />
      <text x="112" y="357" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#9F1239">Strict Perimeter Safety</text>
    </g>
    """
    
    # Arrow 3 -> 4
    svg += hand_arrow(x3 + card_w, card_y + card_h/2 - 20, x3 + card_w + 25, card_y + card_h/2 - 20, curve_dx=0)
    
    # ---------------- Gate 4: Dual-Env Verification ----------------
    x4 = 785
    svg += f"""
    <!-- Gate 4: Dual-Env Verification -->
    <g transform="translate({x4}, {card_y})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="14" fill="#ECFDF5" stroke="#059669" stroke-width="2.4" filter="url(#sketch-shadow)" />
      
      <!-- Top Title Ribbon -->
      <rect x="10" y="-14" width="205" height="28" rx="8" fill="#BBF7D0" stroke="#22252A" stroke-width="2" />
      <text x="112" y="4" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12.5" font-weight="700" fill="#15803D">4. Dual-Env Verification</text>
      
      <text x="112" y="36" text-anchor="middle" class="text-heading" font-size="15" fill="#065F46">Deterministic Check</text>
      <line x1="25" y1="46" x2="200" y2="46" stroke="#6EE7B7" stroke-width="1.6" />
      
      <g transform="translate(14, 60)">
        <text x="0" y="0" class="text-body" font-size="12">• AST syntax compilation</text>
        <text x="0" y="24" class="text-body" font-size="12">• Isolated sandbox dry-run</text>
        <text x="0" y="48" class="text-body" font-size="12">• Local host test execution</text>
        <text x="0" y="72" class="text-body" font-size="12">• 100% pytest pass check</text>
        <text x="0" y="96" class="text-body" font-size="12">• Zero runtime/syntax errors</text>
        <text x="0" y="120" class="text-body" font-size="12">• Zero state residue</text>
        <text x="0" y="148" class="text-body" font-size="12" font-weight="700" fill="#065F46">Dual-Env Invariant:</text>
        <text x="0" y="168" class="text-body" font-size="11" fill="#4B5563">Sandbox dry-run first,</text>
        <text x="0" y="184" class="text-body" font-size="11" fill="#4B5563">local verification second.</text>
      </g>
      
      <rect x="25" y="340" width="175" height="26" rx="13" fill="#BBF7D0" stroke="#059669" stroke-width="1.4" />
      <text x="112" y="357" text-anchor="middle" font-family="'Patrick Hand', cursive" font-size="12" font-weight="700" fill="#059669">Verified Production Safe</text>
    </g>
    """
    
    # ---------------- Out of Gate Actions ----------------
    svg += hand_arrow(260, card_y + card_h, 260, card_y + card_h + 40, label="100% Tests Pass", label_side="left", color="#15803D")
    svg += hand_badge(140, 580, 270, 36, "#BBF7D0", "✓ Verified Clean Git Commit", "#15803D")
    
    svg += hand_arrow(780, card_y + card_h, 780, card_y + card_h + 40, label="Flaw Detected?", label_side="right", color="#EA580C")
    svg += hand_badge(630, 580, 290, 36, "#FED7AA", "✕ Autonomous Coaching Loop", "#C2410C")
    
    # Footer Signature
    svg += footer_signature(640, w)
    svg += "</svg>"
    
    output_path = ASSETS_DIR / "infographic-quality-gate.svg"
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path} ({len(svg)} bytes)")


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    build_unified_architecture()
    build_speed_benchmarks()
    build_learning_curve()
    build_hierarchy_pyramid()
    build_mobile_pipeline()
    build_universal_agents()
    build_quality_gate()
    print("All 7 educational hand-drawn infographics generated successfully.")
