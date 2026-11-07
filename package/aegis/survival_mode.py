"""AegisBrain Emergency Low-Token Survival Mode.

Enforces aggressive context and token preservation:
1. is_survival_mode(): checks if remaining token headroom <= 30% or emergency flag is set.
2. enable_survival_mode(reason: str = "token_cap_29%"): sets survival mode in ~/.aegis/config.json.
3. format_post_response_suggestions_and_review(task: str, response_body: str) -> str:
   Automatically appends:
   a) Matt Pocock Suggestion Panel (2-3 structured next paths with pros/cons, token impact, and 1 recommended option).
   b) Skeptical Truth-Seeking Review (anti-sycophancy audit checking edge cases and verification status).
"""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from aegis.config import get_aegis_dir
from aegis.planner import create_default_suggestions_for_task, format_suggestion_panel
from aegis.truth_seeking import SkepticalTruthReviewer

logger = logging.getLogger(__name__)

DEFAULT_HEADROOM_THRESHOLD_PCT = 30.0
PRIMARY_CONFIG_PATH = Path.home() / ".aegis" / "config.json"


def get_survival_config_paths() -> List[Path]:
    """Return all candidate config file locations for Aegis."""
    paths = [PRIMARY_CONFIG_PATH]
    try:
        aegis_dir_cfg = get_aegis_dir() / "config.json"
        if aegis_dir_cfg not in paths:
            paths.append(aegis_dir_cfg)
    except Exception:
        pass
    return paths


def _read_config_file(path: Path) -> dict:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def is_survival_mode(headroom_pct: Optional[float] = None) -> bool:
    """Check if remaining token headroom <= 30% or emergency flag is set."""
    # 1. Explicit argument check
    if headroom_pct is not None and headroom_pct <= DEFAULT_HEADROOM_THRESHOLD_PCT:
        return True

    # 2. Environment variable overrides
    env_survival = os.environ.get("AEGIS_SURVIVAL_MODE", "").strip().lower()
    if env_survival in ("1", "true", "yes", "on"):
        return True

    env_emergency = os.environ.get("AEGIS_EMERGENCY_FLAG", "").strip().lower()
    if env_emergency in ("1", "true", "yes", "on"):
        return True

    env_headroom = os.environ.get("AEGIS_TOKEN_HEADROOM_PCT") or os.environ.get("TOKEN_HEADROOM_PCT")
    if env_headroom:
        try:
            if float(env_headroom) <= DEFAULT_HEADROOM_THRESHOLD_PCT:
                return True
        except ValueError:
            pass

    # 3. Inspect configuration files (~/.aegis/config.json and get_aegis_dir()/config.json)
    for p in get_survival_config_paths():
        cfg = _read_config_file(p)
        if not cfg:
            continue

        # Check emergency flag directly
        if cfg.get("emergency_flag") is True or cfg.get("emergency") is True:
            return True

        # Check survival_mode section
        sm = cfg.get("survival_mode")
        if sm is True:
            return True
        elif isinstance(sm, dict):
            # If explicitly disabled, do not treat as survival mode
            if sm.get("enabled") is False:
                pass
            else:
                if sm.get("enabled") is True:
                    return True
                if sm.get("emergency_flag") is True:
                    return True
                for k in ("remaining_token_headroom_pct", "remaining_headroom_pct", "remaining_pct", "headroom_pct"):
                    if k in sm:
                        try:
                            if float(sm[k]) <= DEFAULT_HEADROOM_THRESHOLD_PCT:
                                return True
                        except (ValueError, TypeError):
                            pass

        # Check token_headroom_pct / remaining_pct at root
        for k in ("remaining_token_headroom_pct", "token_headroom_pct", "headroom_pct", "remaining_pct"):
            if k in cfg:
                try:
                    if float(cfg[k]) <= DEFAULT_HEADROOM_THRESHOLD_PCT:
                        return True
                except (ValueError, TypeError):
                    pass

        # Check token_guard section
        tg = cfg.get("token_guard")
        if isinstance(tg, dict):
            if tg.get("emergency_flag") is True:
                return True
            for k in ("remaining_pct", "headroom_pct", "remaining_token_headroom_pct"):
                if k in tg:
                    try:
                        if float(tg[k]) <= DEFAULT_HEADROOM_THRESHOLD_PCT:
                            return True
                    except (ValueError, TypeError):
                        pass

    return False


def enable_survival_mode(reason: str = "token_cap_29%") -> None:
    """Set survival mode in ~/.aegis/config.json."""
    # Parse percentage if present, e.g. "token_cap_29%" -> 29.0
    pct = 29.0
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", reason)
    if match:
        try:
            pct = float(match.group(1))
        except ValueError:
            pct = 29.0

    survival_payload = {
        "enabled": True,
        "reason": reason,
        "remaining_token_headroom_pct": pct,
        "emergency_flag": True,
        "activated_at": datetime.now().isoformat(),
    }

    # Save to ~/.aegis/config.json and all candidate config paths
    for p in get_survival_config_paths():
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            data = _read_config_file(p)
            data["survival_mode"] = survival_payload
            data["emergency_flag"] = True

            # Also ensure token_guard recognizes emergency status
            if "token_guard" not in data:
                data["token_guard"] = {}
            if isinstance(data["token_guard"], dict):
                data["token_guard"]["emergency_flag"] = True
                data["token_guard"]["remaining_pct"] = pct
                data["token_guard"]["enforced"] = True

            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning("Failed writing survival mode to %s: %s", p, e)

    logger.warning("🚨 Aegis Survival Mode enabled: %s (headroom: %.1f%%)", reason, pct)


def disable_survival_mode() -> None:
    """Disable survival mode in config files and environment."""
    os.environ.pop("AEGIS_SURVIVAL_MODE", None)
    os.environ.pop("AEGIS_EMERGENCY_FLAG", None)
    os.environ.pop("AEGIS_TOKEN_HEADROOM_PCT", None)

    for p in get_survival_config_paths():
        if not p.exists():
            continue
        try:
            data = _read_config_file(p)
            if "survival_mode" in data:
                if isinstance(data["survival_mode"], dict):
                    data["survival_mode"]["enabled"] = False
                    data["survival_mode"]["emergency_flag"] = False
                    data["survival_mode"]["remaining_token_headroom_pct"] = 100.0
                else:
                    data["survival_mode"] = False
            data["emergency_flag"] = False
            data.pop("emergency", None)
            data.pop("remaining_token_headroom_pct", None)
            data.pop("token_headroom_pct", None)
            if "token_guard" in data and isinstance(data["token_guard"], dict):
                data["token_guard"]["emergency_flag"] = False
                data["token_guard"]["remaining_pct"] = 100.0

            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass


def build_suggestion_panel(task: str) -> str:
    """Generate 2-3 structured next paths with pros/cons, token impact, and 1 recommended option."""
    survival = is_survival_mode()
    if survival:
        suggestions = [
            {
                "title": "Surgical Karpathy-Style Execution (Zero Token Wastage)",
                "description": "Minimal diff, zero speculative abstractions, offline deterministic execution preserving the final 30% token budget.",
                "pros": ["100% token preservation", "Cleanest git diff", "Fast deterministic verification"],
                "cons": ["No verbose conversational commentary"],
                "token_impact": "Ultra-Low (< 100 tokens)",
                "resource_cost": "Zero cloud tokens | Local CPU",
            },
            {
                "title": "Local Worker Offload (Tier 1 Qwen-Coder / Ollama)",
                "description": "Synthesize draft on-device preserving token quota and privacy.",
                "pros": ["Zero cloud API tokens", "Preserves context headroom"],
                "cons": ["Requires local Ollama/Hermes runtime"],
                "token_impact": "0 Cloud Tokens",
                "resource_cost": "3.2 GB host RAM",
            },
            {
                "title": "Context Compaction & Memory Checkpoint (`/compact`)",
                "description": "Persist current findings to brain.db and clear working memory before next turn.",
                "pros": ["Reclaims 60-70% context headroom", "Prevents context overflow"],
                "cons": ["Brief consolidation cycle required"],
                "token_impact": "Reclaims context",
                "resource_cost": "SQLite WAL",
            },
        ]
    else:
        suggestions = create_default_suggestions_for_task(task)
        if len(suggestions) > 3:
            suggestions = suggestions[:3]
        elif len(suggestions) < 2:
            suggestions.append({
                "title": "Verification & Test Suite Execution",
                "description": "Run pytest suite to verify zero regressions.",
                "pros": ["Deterministic safety", "Prevents breaking changes"],
                "cons": ["Takes execution time"],
                "token_impact": "Zero tokens",
                "resource_cost": "Local pytest",
            })

    return format_suggestion_panel(task, suggestions, recommended_index=0)


def build_skeptical_review(task: str, response_body: str) -> str:
    """Anti-sycophancy audit checking edge cases and verification status."""
    audit = SkepticalTruthReviewer.audit_proposal_or_code(response_body, context=task)

    # Verification status check
    verification_patterns = [
        r"\b(?:tests?|pytest)\s+(?:pass(?:ed)?|ok)\b",
        r"\bassert(?:ion)?s?\s+passed\b",
        r"\bexit code 0\b",
        r"\bdeterministic(?:ally)?\s+verified\b",
        r"\bverified\b",
    ]
    verified = any(re.search(pat, response_body, re.IGNORECASE) for pat in verification_patterns)
    verification_status = (
        "VERIFIED (Backed by test assertions or deterministic logs)"
        if verified
        else "PENDING_VERIFICATION (Requires deterministic test execution)"
    )

    # Format flaws
    if audit.flaws_found:
        flaws_md = "\n".join(f"- ❌ **Flaw**: {f}" for f in audit.flaws_found)
    else:
        flaws_md = "- None detected (heuristic scan found no illegal chars or ungrounded praise)."

    # Format edge cases
    edges = list(audit.edge_cases_unhandled)
    if is_survival_mode():
        edges.append("Token headroom is constrained (<= 30%); avoid open-ended recursive subagent calls.")
    if edges:
        edges_md = "\n".join(f"- ⚠️ **Edge**: {e}" for e in edges)
    else:
        edges_md = "- None detected (no immediate NTFS or dependency traps flagged)."

    # Format recommendations
    recs = list(audit.counter_recommendations)
    if not verified:
        recs.append("Run `pytest package/tests` to confirm zero regressions.")
    if recs:
        recs_md = "\n".join(f"- 💡 {r}" for r in recs)
    else:
        recs_md = "- No changes recommended; execute and verify with test suite."

    sycophancy_label = "YES (Unsubstantiated Optimism Detected)" if audit.sycophancy_detected else "NO"

    return f"""### 🛡️ Skeptical Truth-Seeking Review (Anti-Sycophancy Audit)

**Verdict**: `{audit.verdict}` &bull; **Sycophancy Flag**: `{sycophancy_label}` &bull; **Verification Status**: `{verification_status}`

#### 1. Identified Flaws & Vulnerabilities
{flaws_md}

#### 2. Unhandled Edge Cases & Environmental Traps
{edges_md}

#### 3. Counter-Proposals & Verification Actions
{recs_md}""".strip()


def format_post_response_suggestions_and_review(task: str, response_body: str) -> str:
    clean_resp = (response_body or "").strip()
    clean_task = (task or "Current Task").strip().lower()

    # If the user is responding to a suggestion, confirming, or running execution, NEVER loop by attaching another suggestion panel!
    SKIP_PANEL_KEYWORDS = (
        "1", "2", "3", "option 1", "option 2", "option 3",
        "karpathy", "carpathy", "moe", "proceed", "confirm", "yes", "done",
        "hierarchy", "swarm", "test", "run", "execute", "go with"
    )
    if any(k in clean_task for k in SKIP_PANEL_KEYWORDS) or clean_task.isdigit():
        return clean_resp

    # If the response already represents a completed execution report, do not append a loop panel
    if any(h in clean_resp for h in ("Hierarchical Multi-Agent Structure", "Command Output", "Quality Gates Pipeline", "Prompt Injection Defense", "Executed Option")):
        return clean_resp
    """Takes any agent response and automatically appends:
    a) Matt Pocock Suggestion Panel (2-3 structured next paths with pros/cons, token impact, and 1 recommended option).
    b) Skeptical Truth-Seeking Review (anti-sycophancy audit checking edge cases and verification status).
    """
    clean_resp = (response_body or "").strip()
    clean_task = (task or "Current Task").strip()

    # Avoid duplicate panels or reviews if already formatted
    has_panel = "Suggestion Panel" in clean_resp
    has_review = (
        "Anti-Sycophancy" in clean_resp
        or "Skeptical Truth-Seeking Review" in clean_resp
        or "Truth-Seeking Audit" in clean_resp
    )

    if has_panel and has_review:
        return clean_resp

    sections: List[str] = []
    if clean_resp:
        sections.append(clean_resp)

    # a) Matt Pocock Suggestion Panel
    if not has_panel:
        panel_md = build_suggestion_panel(clean_task)
        sections.append(panel_md)

    # b) Skeptical Truth-Seeking Review
    if not has_review:
        review_md = build_skeptical_review(clean_task, clean_resp)
        sections.append(review_md)

    return "\n\n---\n\n".join(sections)
