"""AegisBrain Emergency Token Reserve Guard.

Enforces strict token preservation:
1. Reserves the final 10% of token budget strictly for mission-critical operations
   (e.g. Spring AI project, Final Year Project, production outages).
2. If remaining context/token budget <= 10.0%, non-essential processes, background tasks,
   and conversational generation are HALTED immediately.
3. Only unlocks when explicitly flagged with priority keywords:
   ['spring ai', 'final year', 'fyp', 'important', 'critical', 'emergency'].
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple

from aegis.config import get_aegis_dir

logger = logging.getLogger(__name__)

DEFAULT_PRIORITY_KEYWORDS = [
    "spring ai",
    "final year",
    "fyp",
    "important",
    "critical",
    "emergency",
    "urgent",
    "priority",
    "production",
]

DEFAULT_EMERGENCY_CAP_PCT = 10.0


def get_token_guard_config() -> dict:
    cfg_file = get_aegis_dir() / "config.json"
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("token_guard", {})
        except Exception:
            pass
    return {}


def save_token_guard_config(cap_pct: float = DEFAULT_EMERGENCY_CAP_PCT, keywords: Optional[List[str]] = None) -> None:
    cfg_file = get_aegis_dir() / "config.json"
    cfg_file.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    data["token_guard"] = {
        "emergency_cap_pct": cap_pct,
        "priority_keywords": keywords or DEFAULT_PRIORITY_KEYWORDS,
        "enforced": True,
    }
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def is_priority_task(task_text: str, custom_keywords: Optional[List[str]] = None) -> bool:
    """Check if task matches user-authorized emergency/priority exceptions."""
    keywords = custom_keywords or DEFAULT_PRIORITY_KEYWORDS
    lower = task_text.lower()
    return any(kw in lower for kw in keywords)


def check_token_emergency_lock(
    remaining_pct: float,
    task_description: str,
    explicit_override: bool = False
) -> Tuple[bool, str]:
    """Evaluate whether the request is allowed to run under token budget.
    
    Returns:
        (allowed: bool, message: str)
    """
    cfg = get_token_guard_config()
    cap = cfg.get("emergency_cap_pct", DEFAULT_EMERGENCY_CAP_PCT)
    keywords = cfg.get("priority_keywords", DEFAULT_PRIORITY_KEYWORDS)

    if remaining_pct > cap:
        return True, f"Token budget normal ({remaining_pct:.1f}% remaining > {cap:.1f}% cap)"

    # Within the final 10% emergency reserve
    if explicit_override or is_priority_task(task_description, keywords):
        logger.warning(
            "🚨 Emergency token reserve UNLOCKED for priority task: '%s' (Budget: %.1f%% left)",
            task_description, remaining_pct
        )
        return True, f"🚨 Emergency 10% token reserve unlocked for priority task ('{task_description}')"

    err_msg = (
        f"🛑 EMERGENCY TOKEN CAP TRIGGERED: Token headroom is below {cap:.1f}% ({remaining_pct:.1f}% remaining). "
        "All routine background tasks, sprawling scrapes, and boilerplate drafts are PAUSED. "
        "The remaining 10% is reserved exclusively for Spring AI, Final Year Project, or explicitly marked critical work. "
        "To reclaim context, run `/compact` or explicitly flag your request with 'IMPORTANT:'."
    )
    return False, err_msg
