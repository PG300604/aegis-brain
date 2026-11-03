"""Generate 3D Axonometric Architecture Diagram for AegisBrain.

Uses 2:1 dimetric projection iso(x, y, z) = (x - y + OX, (x + y)/2 - z + OY)
to render an exploded isometric architectural diagram with true 3D slabs,
recessed processor cavities, and isometric bus routing.
"""

import math
from pathlib import Path

OUTPUT_PATH = Path("P:/open-source/aegis-brain/assets/architecture-3d.svg")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

WIDTH = 1200
HEIGHT = 720
OX = 600
OY = 180


def iso(x: float, y: float, z: float):
    """2:1 dimetric projection."""
    px = OX + (x - y)
    py = OY + (x + y) * 0.5 - z
    return round(px, 2), round(py, 2)


def make_prism(x: float, y: float, z: float, w: float, d: float, h: float,
               top_fill: str, left_fill: str, right_fill: str, stroke: str = "rgba(255,255,255,0.12)"):
    """Render a 3D isometric box/slab."""
    # 8 vertices
    p000 = iso(x, y, z)
    p100 = iso(x + w, y, z)
    p110 = iso(x + w, y + d, z)
    p010 = iso(x, y + d, z)

    p001 = iso(x, y, z + h)
    p101 = iso(x + w, y, z + h)
    p111 = iso(x + w, y + d, z + h)
    p011 = iso(x, y + d, z + h)

    # Top face (p001, p101, p111, p011)
    top_d = f"M {p001[0]} {p001[1]} L {p101[0]} {p101[1]} L {p111[0]} {p111[1]} L {p011[0]} {p011[1]} Z"
    # Left face (front-left in 2:1 projection: x+w, y to y+d -> p100, p110, p111, p101)
    # Wait, in x-y: increasing y moves DOWN-LEFT (+x-y -> negative x, positive y)
    # increasing x moves DOWN-RIGHT (+x-y -> positive x, positive y)
    # So Front-Right face: from x0 to x1 at y1 (p010 -> p110 -> p111 -> p011)
    # Front-Left face: from y0 to y1 at x1 (p100 -> p110 -> p111 -> p101)
    # Actually:
    # (x, y+d) is front-left. (x+w, y+d) is bottom corner. (x+w, y) is front-right.
    # Left face (y = y+d edge along x from 0 to w): p010 -> p110 -> p111 -> p011
    # Right face (x = x+w edge along y from 0 to d): p100 -> p110 -> p111 -> p101

    left_d = f"M {p010[0]} {p010[1]} L {p110[0]} {p110[1]} L {p111[0]} {p111[1]} L {p011[0]} {p011[1]} Z"
    right_d = f"M {p100[0]} {p100[1]} L {p110[0]} {p110[1]} L {p111[0]} {p111[1]} L {p101[0]} {p101[1]} Z"

    return f"""
    <g class="prism">
      <path d="{left_d}" fill="{left_fill}" stroke="{stroke}" stroke-width="1" />
      <path d="{right_d}" fill="{right_fill}" stroke="{stroke}" stroke-width="1" />
      <path d="{top_d}" fill="{top_fill}" stroke="{stroke}" stroke-width="1" />
    </g>"""


def build_svg():
    elements = []

    # 1. Background Grid & Lighting
    elements.append(f"""
    <rect width="{WIDTH}" height="{HEIGHT}" fill="#08090D" />
    <!-- Subtle Coordinate Grid -->
    <defs>
      <pattern id="isoGrid" width="60" height="30" patternUnits="userSpaceOnUse">
        <path d="M 0 15 L 30 0 L 60 15 L 30 30 Z" fill="none" stroke="rgba(255, 255, 255, 0.02)" stroke-width="1" />
      </pattern>
      <linearGradient id="chassisGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E2330" />
        <stop offset="100%" stop-color="#121620" />
      </linearGradient>
      <linearGradient id="chipGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#242B3D" />
        <stop offset="100%" stop-color="#171C28" />
      </linearGradient>
      <radialGradient id="ambientGlow" cx="50%" cy="45%" r="60%">
        <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.08" />
        <stop offset="100%" stop-color="#08090D" stop-opacity="0" />
      </radialGradient>
    </defs>
    <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#isoGrid)" />
    <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#ambientGlow)" />
    <rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" fill="none" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1" />
    """)

    # LAYER 0: Bottom Floor (Storage & Runtimes, z = -120)
    # Slabs for: Local SQLite WAL, ACTIVE_CONTEXT.md, Local Ollama, OpenHiggsfield
    z_floor = -130
    elements.append(f"<!-- Tier 3: Execution & Storage Floor (z={z_floor}) -->")
    # Base Floor Plate
    elements.append(make_prism(
        x=-340, y=-220, z=z_floor, w=680, d=440, h=12,
        top_fill="#0F1219", left_fill="#0A0C11", right_fill="#0D0F16",
        stroke="rgba(255, 255, 255, 0.07)"
    ))

    # Modules on Floor Plate
    floor_nodes = [
        (-280, -160, 220, 120, "brain.db", "SQLite WAL + FTS5", "#10B981", "PERSISTENT MEMORY"),
        (60, -160, 220, 120, "ACTIVE_CONTEXT.md", "Deterministic ≤400t", "#38BDF8", "GOVERNOR CACHE"),
        (-280, 20, 220, 120, "Local Ollama :11434", "Qwen / DeepSeek / Llama", "#F59E0B", "INFERENCE RUNTIME"),
        (60, 20, 220, 120, "OpenHiggsfield", "Flux 2 / Seedance / Kling", "#818CF8", "MEDIA GENERATION"),
    ]

    for fx, fy, fw, fd, ftitle, fsub, faccent, ftag in floor_nodes:
        elements.append(make_prism(
            x=fx, y=fy, z=z_floor+12, w=fw, d=fd, h=20,
            top_fill="#161B26", left_fill="#0E121B", right_fill="#121622",
            stroke="rgba(255,255,255,0.1)"
        ))
        # Top face text
        tx, ty = iso(fx + fw/2, fy + fd/2, z_floor + 32)
        elements.append(f"""
        <g transform="translate({tx}, {ty})">
          <circle cx="-65" cy="-8" r="3" fill="{faccent}" />
          <text x="-55" y="-5" fill="{faccent}" font-family="ui-monospace, Consolas, monospace" font-size="9" font-weight="700" letter-spacing="1">{ftag}</text>
          <text x="0" y="10" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="600" text-anchor="middle">{ftitle}</text>
          <text x="0" y="24" fill="#94A3B8" font-family="ui-monospace, Consolas, monospace" font-size="10" text-anchor="middle">{fsub}</text>
        </g>
        """)

    # LAYER 1: AegisBrain 3D Core Chassis (z = 40)
    z_core = 40
    elements.append(f"<!-- Tier 2: AegisBrain Chassis (z={z_core}) -->")
    # Main Daemon Floating Slab
    elements.append(make_prism(
        x=-300, y=-190, z=z_core, w=600, d=380, h=24,
        top_fill="url(#chassisGrad)", left_fill="#0E121A", right_fill="#141924",
        stroke="rgba(56, 189, 248, 0.28)"
    ))

    # Core Coprocessor Chips on Top of Daemon
    chips = [
        (-260, -150, 240, 140, "Context Governor", "≤400 Token Pruning", "#38BDF8", "TOKEN BUDGET"),
        (20, -150, 240, 140, "Neural Memory Bus", "FTS5 Virtual Triggers", "#10B981", "SUB-MS WAL"),
        (-260, 20, 240, 130, "Skill Distiller", "Ollama Proxy :8765/v1", "#F59E0B", "PROMPT AUGMENT"),
        (20, 20, 240, 130, "Media Bridge", "OpenHiggsfield Dispatch", "#818CF8", "IMAGE / VIDEO"),
    ]

    for cx, cy, cw, cd, ctitle, csub, caccent, ctag in chips:
        elements.append(make_prism(
            x=cx, y=cy, z=z_core+24, w=cw, d=cd, h=16,
            top_fill="url(#chipGrad)", left_fill="#0F131C", right_fill="#181E2B",
            stroke="rgba(255,255,255,0.12)"
        ))
        tx, ty = iso(cx + cw/2, cy + cd/2, z_core + 40)
        elements.append(f"""
        <g transform="translate({tx}, {ty})">
          <rect x="-60" y="-18" width="120" height="15" rx="3" fill="rgba(255,255,255,0.04)" stroke="{caccent}" stroke-width="0.8" />
          <text x="0" y="-7" fill="{caccent}" font-family="ui-monospace, Consolas, monospace" font-size="8.5" font-weight="700" letter-spacing="1" text-anchor="middle">{ctag}</text>
          <text x="0" y="8" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" text-anchor="middle">{ctitle}</text>
          <text x="0" y="22" fill="#94A3B8" font-family="ui-monospace, Consolas, monospace" font-size="10" text-anchor="middle">{csub}</text>
        </g>
        """)

    # Chassis Identification Plate
    plate_x, plate_y = iso(-300, -190, z_core + 24)
    elements.append(f"""
    <g transform="translate({plate_x + 80}, {plate_y - 20})">
      <text x="0" y="0" fill="#38BDF8" font-family="ui-monospace, Consolas, monospace" font-size="11" font-weight="800" letter-spacing="2">AEGIS_CORE_DAEMON // 127.0.0.1:8765</text>
    </g>
    """)

    # LAYER 2: Client Agents Tier (z = 210)
    z_client = 210
    elements.append(f"<!-- Tier 1: Agent Clients (z={z_client}) -->")

    client_nodes = [
        (-260, -150, 110, 80, "Antigravity", "Claude / Gemini"),
        (-130, -150, 110, 80, "Hermes", "Thinking Agents"),
        (20, -150, 110, 80, "OpenCode", "Agent Swarms"),
        (150, -150, 110, 80, "Terminal CLI", "Aider / Scripts"),
    ]

    for cx, cy, cw, cd, ctitle, csub in client_nodes:
        elements.append(make_prism(
            x=cx, y=cy, z=z_client, w=cw, d=cd, h=14,
            top_fill="#1E293B", left_fill="#0F172A", right_fill="#141E33",
            stroke="rgba(56, 189, 248, 0.4)"
        ))
        tx, ty = iso(cx + cw/2, cy + cd/2, z_client + 14)
        elements.append(f"""
        <g transform="translate({tx}, {ty})">
          <text x="0" y="0" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" text-anchor="middle">{ctitle}</text>
          <text x="0" y="14" fill="#94A3B8" font-family="ui-monospace, Consolas, monospace" font-size="9" text-anchor="middle">{csub}</text>
        </g>
        """)

    # BUS CONNECTORS: Laser Bus Routing between Tiers
    # From Tier 1 (Clients) to Tier 2 (Daemon)
    for cx, cy, cw, cd, _, _ in client_nodes:
        x_src, y_src = iso(cx + cw/2, cy + cd/2, z_client)
        x_dst, y_dst = iso(cx + cw/2, cy + cd/2, z_core + 40)
        elements.append(f"""
        <path d="M {x_src} {y_src} L {x_dst} {y_dst}" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
        <circle cx="{x_src}" cy="{y_src}" r="2.5" fill="#38BDF8" />
        <circle cx="{x_dst}" cy="{y_dst}" r="2.5" fill="#38BDF8" />
        """)

    # From Tier 2 (Daemon) to Tier 3 (Floor Targets)
    down_routes = [
        ((-260 + 120, -150 + 70, z_core), (60 + 110, -160 + 60, z_floor + 32), "#38BDF8"),  # Governor -> ACTIVE_CONTEXT
        ((20 + 120, -150 + 70, z_core), (-280 + 110, -160 + 60, z_floor + 32), "#10B981"),   # Memory Bus -> brain.db
        ((-260 + 120, 20 + 65, z_core), (-280 + 110, 20 + 60, z_floor + 32), "#F59E0B"),    # Distiller -> Ollama
        ((20 + 120, 20 + 65, z_core), (60 + 110, 20 + 60, z_floor + 32), "#818CF8"),        # Media Bridge -> OpenHiggsfield
    ]

    for (x1, y1, z1), (x2, y2, z2), color in down_routes:
        p_start = iso(x1, y1, z1)
        p_end = iso(x2, y2, z2)
        elements.append(f"""
        <path d="M {p_start[0]} {p_start[1]} L {p_end[0]} {p_end[1]}" stroke="{color}" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.75" />
        <circle cx="{p_start[0]}" cy="{p_start[1]}" r="3" fill="{color}" />
        <circle cx="{p_end[0]}" cy="{p_end[1]}" r="3" fill="{color}" />
        """)

    # Header Legend & Branding in Corner
    elements.append(f"""
    <g transform="translate(60, 60)">
      <text x="0" y="0" fill="#38BDF8" font-family="ui-monospace, Consolas, monospace" font-size="11" font-weight="700" letter-spacing="2">SYSTEM TOPOLOGY // 3D DIMETRIC PROJECTION</text>
      <text x="0" y="24" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="22" font-weight="800">AegisBrain Architectural Bus</text>
      <text x="0" y="44" fill="#64748B" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13">Hardware-accelerated context governor and persistent SQLite memory</text>
    </g>

    <!-- Bottom Specs Pill Bar -->
    <g transform="translate(60, {HEIGHT - 50})">
      <rect x="0" y="0" width="1080" height="32" rx="6" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.08)" stroke-width="1" />
      <text x="20" y="20" fill="#64748B" font-family="ui-monospace, Consolas, monospace" font-size="11">ENGINE: <tspan fill="#E2E8F0">Python 3 Stdlib</tspan></text>
      <text x="220" y="20" fill="#64748B" font-family="ui-monospace, Consolas, monospace" font-size="11">STORAGE: <tspan fill="#10B981">SQLite 3 WAL + FTS5</tspan></text>
      <text x="440" y="20" fill="#64748B" font-family="ui-monospace, Consolas, monospace" font-size="11">TOKEN CAP: <tspan fill="#38BDF8">≤ 400t Deterministic</tspan></text>
      <text x="680" y="20" fill="#64748B" font-family="ui-monospace, Consolas, monospace" font-size="11">PROMPT PROXY: <tspan fill="#F59E0B">127.0.0.1:8765/v1</tspan></text>
      <text x="910" y="20" fill="#64748B" font-family="ui-monospace, Consolas, monospace" font-size="11">CREATIVE: <tspan fill="#818CF8">OpenHiggsfield</tspan></text>
    </g>
    """)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="100%">
{''.join(elements)}
</svg>"""

    OUTPUT_PATH.write_text(svg_content, encoding="utf-8")
    print(f"Generated 3D Axonometric Architecture Diagram at: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_svg()
