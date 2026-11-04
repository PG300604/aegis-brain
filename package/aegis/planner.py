"""Interactive Suggestion Panel & Multi-Tier Clarification Gate for AegisBrain.

Implements Matt Pocock's structured alignment protocol:
- Prevents token wastage and repeated refactors from blind guessing.
- Evaluates task ambiguity and generates targeted clarification questions
  between User <-> Manager and Manager <-> Worker before code synthesis.
- After complex tasks or when choices exist, generates a structured Suggestion Panel
  presenting 3-4 distinct paths with explicit trade-offs, resource footprints, and pros/cons.
- Gates autonomous multi-step execution until the user or manager model aligns on the exact path.
"""

import re
from typing import List, Dict, Any, Optional


def evaluate_task_ambiguity(prompt: str) -> Dict[str, Any]:
    """Analyze prompt for missing architectural invariants or underspecified constraints."""
    clean = prompt.lower().strip()
    ambiguities = []

    # Check for missing persistence/storage specification
    if any(k in clean for k in ("store", "save", "database", "persist", "cache", "data")) and not any(k in clean for k in ("sqlite", "postgres", "redis", "json", "memory", "file", "disk")):
        ambiguities.append({
            "dimension": "Storage Backend",
            "question": "Which storage mechanism should be prioritized?",
            "options": [
                "(Recommended) SQLite with WAL mode (Zero-dependency, sub-millisecond, local on-device)",
                "Local JSON/File buffer (Simplest, transparent plain text)",
                "External Postgres / Redis (Requires running background service)",
            ]
        })

    # Check for missing interface/protocol specification
    if any(k in clean for k in ("api", "endpoint", "service", "route")) and not any(k in clean for k in ("rest", "json", "http", "graphql", "rpc")):
        ambiguities.append({
            "dimension": "API Protocol",
            "question": "What interface protocol should the service expose?",
            "options": [
                "(Recommended) Lightweight HTTP JSON REST (Standard library first, zero bloat)",
                "CLI interactive command (Terminal-native, instant testing)",
                "Async WebSocket event streaming (Real-time state push)",
            ]
        })

    # Check for error recovery / fallback specification
    if any(k in clean for k in ("download", "fetch", "network", "remote", "install", "stream")) and not any(k in clean for k in ("retry", "timeout", "fallback", "offline")):
        ambiguities.append({
            "dimension": "Failure Mode & Resilience",
            "question": "How should network timeouts or offline conditions be handled?",
            "options": [
                "(Recommended) Offline Queue with Telegram alert (Never blocks user, resumes on desk presence)",
                "Immediate graceful fail with diagnostic error message",
                "Exponential backoff retry (3 attempts with 2s jitter)",
            ]
        })

    is_ambiguous = len(ambiguities) > 0
    return {
        "is_ambiguous": is_ambiguous,
        "ambiguity_score": round(len(ambiguities) * 0.33, 2),
        "questions": ambiguities,
    }


def format_clarification_gate(prompt: str, ambiguity_data: Optional[Dict[str, Any]] = None) -> str:
    """Format an interactive Clarification Gate for the user or between Manager & Worker."""
    if ambiguity_data is None:
        ambiguity_data = evaluate_task_ambiguity(prompt)

    if not ambiguity_data["is_ambiguous"]:
        return ""

    lines = [
        "❓ *AegisBrain Matt Pocock Clarification Gate*",
        "• *Objective:* Zero communication gap & zero token wastage from blind hallucination.",
        "• *Status:* Detected underspecified architectural details before code synthesis.",
        ""
    ]

    for idx, q in enumerate(ambiguity_data["questions"], 1):
        lines.append(f"**[{idx}] {q['dimension']}:** {q['question']}")
        for opt in q["options"]:
            lines.append(f"   • {opt}")
        lines.append("")

    lines.append("💬 *How to proceed:* Confirm your choices (e.g. `1A, 2A`) or reply with your preference to proceed.")
    return "\n".join(lines)


def format_suggestion_panel(
    task_title: str,
    suggestions: List[Dict[str, Any]],
    recommended_index: int = 0,
) -> str:
    """Format an interactive Suggestion Panel with trade-offs and recommendations."""
    lines = [
        f"🧭 *AegisBrain Suggestion Panel: {task_title}*",
        "Select the next path forward to execute safely with zero token wastage:\n",
    ]

    for idx, s in enumerate(suggestions, 1):
        is_rec = (idx - 1) == recommended_index
        rec_badge = " 🌟 *(Recommended)*" if is_rec else ""
        title = s.get("title", f"Option {idx}")
        desc = s.get("description", "")
        pros = s.get("pros", [])
        cons = s.get("cons", [])
        token_impact = s.get("token_impact", "Minimal")
        resource_cost = s.get("resource_cost", "Low RAM")

        lines.append(f"**[{idx}] {title}**{rec_badge}")
        if desc:
            lines.append(f"   • *Strategy:* {desc}")
        if pros:
            lines.append(f"   • *Pros:* {'; '.join(pros)}")
        if cons:
            lines.append(f"   • *Cons / Trade-offs:* {'; '.join(cons)}")
        lines.append(f"   • *Footprint:* {token_impact} tokens | {resource_cost}")
        lines.append("")

    lines.append("💬 *How to proceed:* Reply with your preferred option number (e.g. `1` or `2`) or type `/type <choice>` from Telegram.")
    return "\n".join(lines)


def create_default_suggestions_for_task(task_type: str) -> List[Dict[str, Any]]:
    """Generate default contextual suggestions based on detected task category."""
    clean_type = task_type.lower()

    if "model" in clean_type or "llm" in clean_type or "orchestrat" in clean_type or "moe" in clean_type:
        return [
            {
                "title": "Lightweight MoE Tier (~7.5GB RAM Cap, Offloaded to Drive P:)",
                "description": "Reverse-engineered FreeToken architecture with dynamic LRU expert caching. Deep multi-token reasoning.",
                "pros": ["Massive MoE capacity on RTX 3050", "Windows & VM RAM protected", "Zero cloud tokens"],
                "cons": ["Moderate throughput (~18 tok/s) due to PCIe offload"],
                "token_impact": "Zero Cloud Tokens",
                "resource_cost": "7.5 GB RAM Cap | Disk P: Storage",
            },
            {
                "title": "Ultra-Light Qwen 2.5 Coder Synthesis (<4GB RAM)",
                "description": "Fast surgical edits using quantized 7B coder. Ideal when 8GB VM and browser tabs are heavily loaded.",
                "pros": ["Highest local generation speed (32 tok/s)", "Lowest memory footprint (3.2 GB)"],
                "cons": ["Slightly narrower context reasoning than full MoE"],
                "token_impact": "Zero Cloud Tokens",
                "resource_cost": "3.2 GB local RAM",
            },
            {
                "title": "Frontier Manager Arbitrage (Gemini 3.8 / Claude 3.7)",
                "description": "Frontier boss sets invariants and reviews local draft. Keeps proprietary code local while saving 80% tokens.",
                "pros": ["Highest architectural rigor", "Zero host RAM spike", "Continuous distillation learning"],
                "cons": ["Requires network connectivity for manager review"],
                "token_impact": "Low (~150 manager tokens)",
                "resource_cost": "1.5 GB host RAM",
            },
        ]

    elif "ui" in clean_type or "frontend" in clean_type or "web" in clean_type:
        return [
            {
                "title": "Modern Dark Mode with GSAP Natural Motion",
                "description": "Slate-950 canvas, crisp typography tokens, accessible contrast, 250ms eased transitions.",
                "pros": ["Aligned with user taste profile", "High responsive polish", "Zero UI slop"],
                "cons": ["Requires GSAP animation script import"],
                "token_impact": "Minimal",
                "resource_cost": "Lightweight client-side",
            },
            {
                "title": "Minimal Pure Tailwind / CSS Clean State",
                "description": "Zero external JS animation dependencies, pure semantic CSS transitions.",
                "pros": ["Ultra-fast load times", "Zero bundle overhead"],
                "cons": ["Less expressive interactive motion"],
                "token_impact": "Minimal",
                "resource_cost": "Lowest bundle size",
            },
        ]

    else:
        return [
            {
                "title": "Surgical Karpathy-Style Implementation",
                "description": "Touch only the essential files, minimal diff, verifiable unit tests.",
                "pros": ["Zero regression risk", "Cleanest git diff", "Fastest review cycle"],
                "cons": ["No speculative helper abstractions"],
                "token_impact": "Minimal",
                "resource_cost": "Zero extra dependencies",
            },
            {
                "title": "Architectural Decoupling with Extended Test Matrix",
                "description": "Extract modular service interfaces and add comprehensive regression suites.",
                "pros": ["Highest long-term extensibility"],
                "cons": ["More lines of code", "Takes longer to verify"],
                "token_impact": "Moderate",
                "resource_cost": "Minimal",
            },
        ]
