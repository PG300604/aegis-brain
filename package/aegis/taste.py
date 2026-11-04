"""User Taste & Aesthetic Persona Engine for AegisBrain.

Maintains a living profile of the user's communication style, coding philosophy,
UI/UX aesthetics, and creative workflow preferences. Automatically injected into
AegisBrain active context so all agents (Antigravity, Hermes, OpenCode) execute
with the user's exact taste and high-standards without repetitive prompting.
"""

import json
from pathlib import Path
from typing import Dict, Any

from .config import get_aegis_dir


def get_taste_path() -> Path:
    return get_aegis_dir() / "taste.json"


DEFAULT_TASTE_PROFILE: Dict[str, Any] = {
    "user_name": "Priyanshu",
    "persona": "Systems Engineer, Open-Source Innovator & AI Architect",
    "communication": {
        "style": "Conversational, visionary, high-velocity, and direct",
        "tone": "Confident, objective, and solution-focused",
        "guidelines": [
            "Never use apologetic or fluffy filler ('I apologize for...', 'Sure, I would love to help...')",
            "Present 3-4 structured options with pros/cons when choices exist (Matt Pocock protocol)",
            "Always provide verifiable success criteria before executing multi-step tasks",
            "Format outputs cleanly with GitHub-style markdown, structured headings, and clickable file links",
        ],
    },
    "coding_philosophy": {
        "core_doctrine": "Andrej Karpathy Guidelines & Surgical Simplicity",
        "rules": [
            "Minimum code that solves the problem — zero speculative abstractions",
            "Surgical edits: touch only what must change; clean up only own orphans; preserve existing comments",
            "Standard library first: avoid adding heavy external dependencies when stdlib suffices",
            "Local data privacy: keep code and proprietary context on-device whenever possible",
            "Multi-model token arbitrage: let frontier models govern/audit while local workers generate code",
        ],
    },
    "ui_ux_taste": {
        "style": "Modern Dark Mode & Neo-Minimalism",
        "typography": "Crisp sans-serif (Inter, Geist) with monospaced accents (JetBrains Mono)",
        "color_palette": "Deep neutral canvas (slate-950/zinc-900), subtle borders (zinc-800), vibrant accent highlights",
        "motion": "Tight, natural easing (200-350ms duration) using GSAP / Anime.js motion principles",
        "anti_patterns": ["Zero visual slop", "No generic AI template layouts", "No sluggish heavy animations"],
    },
    "creative_and_video": {
        "engine": "OpenMontage, Remotion & Hyperframes",
        "pacing": "Dynamic, high-retention, and rhythmically synced to audio cues",
        "overlays": "Minimalist typography cards, accessible contrast, clean lower-thirds",
    },
    "hardware_discipline": {
        "total_ram_budget": "16 GB RAM with Intel i5-12500H and RTX 3050 (4GB VRAM)",
        "multitasking_protection": "Always preserve memory headroom for 8GB VM, 5-6 Brave tabs, Spotify, and IDEs",
        "model_selection": "Auto-size local models (1.5B under load, 7B Q4 balanced) to prevent system freeze",
    },
}


def load_taste_profile() -> Dict[str, Any]:
    """Load user taste profile or initialize with defaults."""
    p = get_taste_path()
    if p.exists():
        try:
            loaded = json.loads(p.read_text(encoding="utf-8"))
            base = dict(DEFAULT_TASTE_PROFILE)
            base.update(loaded)
            return base
        except Exception:
            pass
    return dict(DEFAULT_TASTE_PROFILE)


def save_taste_profile(profile: Dict[str, Any]) -> None:
    """Save user taste profile to ~/.aegis-brain/taste.json."""
    p = get_taste_path()
    p.write_text(json.dumps(profile, indent=2), encoding="utf-8")


def update_taste_facet(domain: str, key: str, value: Any) -> bool:
    """Update a specific facet of the user's taste profile."""
    prof = load_taste_profile()
    if domain in prof and isinstance(prof[domain], dict):
        prof[domain][key] = value
        save_taste_profile(prof)
        return True
    return False


def format_taste_prompt() -> str:
    """Compact prompt segment for agent bootstrapping and ACTIVE_CONTEXT.md."""
    prof = load_taste_profile()
    comm = prof["communication"]
    code = prof["coding_philosophy"]
    ui = prof["ui_ux_taste"]
    hw = prof["hardware_discipline"]

    lines = [
        "### 🎨 User Taste & Aesthetic Standards (Enforced)",
        f"- **User Style:** {comm['style']} ({comm['tone']})",
        f"- **Code Doctrine:** {code['core_doctrine']} — Minimum code, surgical diffs, no speculative bloat.",
        f"- **UI/UX Aesthetic:** {ui['style']} | Typography: {ui['typography']} | Motion: {ui['motion']}",
        f"- **Hardware Headroom:** {hw['multitasking_protection']}.",
        "- **Clarification Gate:** Present 3-4 structured options with pros/cons before executing ambiguous plans.",
    ]
    return "\n".join(lines)


def format_taste_display() -> str:
    """Detailed visual representation of user taste for CLI and Telegram."""
    prof = load_taste_profile()
    lines = [
        f"🎨 *AegisBrain Taste & Persona Profile ({prof['user_name']})*",
        f"• *Persona:* {prof['persona']}",
        "",
        "🗣️ *Communication & Presentation:*",
        f"• *Tone & Style:* {prof['communication']['style']} ({prof['communication']['tone']})",
        *[f"  - {g}" for g in prof["communication"]["guidelines"]],
        "",
        "💻 *Coding Doctrine:*",
        f"• *Core:* {prof['coding_philosophy']['core_doctrine']}",
        *[f"  - {r}" for r in prof["coding_philosophy"]["rules"]],
        "",
        "✨ *Design & Creative Aesthetic:*",
        f"• *UI Style:* {prof['ui_ux_taste']['style']} (Font: {prof['ui_ux_taste']['typography']})",
        f"• *Motion:* {prof['ui_ux_taste']['motion']}",
        f"• *Video Stack:* {prof['creative_and_video']['engine']} ({prof['creative_and_video']['pacing']})",
        "",
        "🛡️ *Hardware Discipline:*",
        f"• *Hardware Budget:* {prof['hardware_discipline']['total_ram_budget']}",
        f"• *Multitasking Rule:* {prof['hardware_discipline']['multitasking_protection']}",
    ]
    return "\n".join(lines)
