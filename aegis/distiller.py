"""Skill Distillation & Quality Guard Engine.

Distills 500+ arsenal skills and plugins into hyper-compact constraint vectors
suitable for smaller local models (e.g. Qwen 2.5 Coder 7B, DeepSeek Coder 14B,
Llama 3 8B via Ollama or Hermes).
"""

from typing import Dict, List, Optional

CORE_DISTILLED_RULES = {
    "karpathy_simplicity": (
        "1. Surgical changes only: touch only lines directly relevant to the user request. "
        "2. Zero speculative abstractions, wrappers, or unused configurability. "
        "3. Match existing style and preserve comments. Write verifiable code."
    ),
    "security_baseline": (
        "1. Never leak secrets, API keys, or private environment variables. "
        "2. Strictly validate all external inputs against injection and path traversal. "
        "3. Never bypass sandbox or permission controls."
    ),
    "java_spring": (
        "1. OpenTelemetry metrics: omit attributes when null/empty to prevent tag explosion. "
        "2. Backward compatibility: default interface methods returning null; preserve constructors. "
        "3. Follow Spring JavaFormat."
    ),
    "python_fast": (
        "1. Zero unnecessary external dependencies; prefer standard library where possible. "
        "2. Strict type hinting with mypy/ruff compliance. "
        "3. Use context managers for all I/O and DB connections."
    ),
}

KEYWORDS_TO_SKILLS = {
    "spring": ["java_spring", "karpathy_simplicity"],
    "otel": ["java_spring"],
    "observation": ["java_spring"],
    "metrics": ["java_spring"],
    "python": ["python_fast", "karpathy_simplicity"],
    "fastapi": ["python_fast"],
    "security": ["security_baseline"],
    "auth": ["security_baseline"],
}


def distill_rules_for_prompt(prompt_text: str, extra_tags: Optional[List[str]] = None) -> str:
    """Analyze prompt text and tags to synthesize an ultra-compact system constraint block (<100 tokens)."""
    selected_rules: set[str] = {"karpathy_simplicity", "security_baseline"}

    lowered = (prompt_text + " " + " ".join(extra_tags or [])).lower()
    for kw, rule_keys in KEYWORDS_TO_SKILLS.items():
        if kw in lowered:
            selected_rules.update(rule_keys)

    lines = ["## Aegis Quality & Skill Guardrails"]
    for r_key in sorted(selected_rules):
        rule_text = CORE_DISTILLED_RULES.get(r_key)
        if rule_text:
            lines.append(f"- **[{r_key.upper()}]**: {rule_text}")

    return "\n".join(lines)
