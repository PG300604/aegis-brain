"""AegisBrain Autonomous Task Severity Triage & Bottleneck-Aware Multi-Agent Dispatcher.

Enforces the Boss-Worker hierarchical agent doctrine:
1. Severity & Complexity Judge:
   - Evaluates tasks across security, risk, scope, and technical depth.
   - CRITICAL: Handled directly by Frontier Manager (Claude / Gemini 3.8 Flash High) with strict review.
   - MODERATE / ROUTINE: Automatically offloaded to Local Workers (Hermes CLI, OpenCode, Qwen 2.5) or
     Antigravity Subagents to eliminate token burn.
2. PC Resource & Bottleneck Guard:
   - Inspects real-time RAM, memory load %, and CPU core headroom before spawning models.
   - Prevents system freezing or RAM thrashing on multitasking systems (Spotify, IDEs, browser).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from .hardware import get_hardware_status, recommend_model_tier
from .confidence import recommend_agent, get_agent_confidence


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"          # Security, auth, secrets, architectural invariant changes
    MODERATE = "MODERATE"          # Feature implementations, multi-file refactors, bugfixes
    ROUTINE = "ROUTINE"            # Boilerplate, unit tests, scrapers, documentation, formatting


class ExecutionStrategy(str, Enum):
    FRONTIER_DIRECT = "FRONTIER_DIRECT"
    LOCAL_WORKER_WITH_MANAGER_REVIEW = "LOCAL_WORKER_WITH_MANAGER_REVIEW"
    PARALLEL_SUBAGENTS = "PARALLEL_SUBAGENTS"
    LIGHTWEIGHT_CLI = "LIGHTWEIGHT_CLI"


@dataclass
class TriageDecision:
    task: str
    severity: SeverityLevel
    complexity_score: int         # 1 - 10
    execution_strategy: ExecutionStrategy
    recommended_worker: str
    bottleneck_risk: str          # "LOW", "MEDIUM", "HIGH"
    avail_ram_gb: float
    load_percent: int
    rationale: str
    invariants: List[str] = field(default_factory=list)
    subagents_count: int = 1
    workers_per_subagent: int = 1
    cognition_power: str = "BALANCED"
    cpu_load_percent: float = 15.0
    autonomous_decision: bool = True  # Always True: zero prompt interruption

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "severity": self.severity.value,
            "complexity_score": self.complexity_score,
            "execution_strategy": self.execution_strategy.value,
            "recommended_worker": self.recommended_worker,
            "bottleneck_risk": self.bottleneck_risk,
            "avail_ram_gb": self.avail_ram_gb,
            "load_percent": self.load_percent,
            "cpu_load_percent": self.cpu_load_percent,
            "rationale": self.rationale,
            "invariants": self.invariants,
            "subagents_count": self.subagents_count,
            "workers_per_subagent": self.workers_per_subagent,
            "cognition_power": self.cognition_power,
            "autonomous_decision": self.autonomous_decision,
        }

    def format_banner(self) -> str:
        """Format a concise visual status header for the CLI response."""
        risk_icon = "🟢" if self.bottleneck_risk == "LOW" else "🟡" if self.bottleneck_risk == "MEDIUM" else "🔴"
        sev_icon = "🚨" if self.severity == SeverityLevel.CRITICAL else "⚡" if self.severity == SeverityLevel.MODERATE else "🌱"
        
        return (
            f"🎯 **[Aegis Severity Triage]** {sev_icon} `{self.severity.value}` (Cognition: {self.cognition_power}, Score: {self.complexity_score}/10) | "
            f"Strategy: `{self.execution_strategy.value}` | Subagents: `{self.subagents_count}` (Workers/Sub: `{self.workers_per_subagent}`) | "
            f"PC Headroom: {risk_icon} {self.avail_ram_gb}GB Free ({self.load_percent}% RAM, {self.cpu_load_percent}% CPU)\n"
            f"💡 *Rationale:* {self.rationale}"
        )


class SeverityTriageEngine:
    """Evaluates task intent, scores complexity, checks hardware, and assigns execution muscle."""

    CRITICAL_PATTERNS = [
        r"\b(security|vulnerability|exploit|cve|injection|jwt|auth|token|secret|password|credential)\b",
        r"\b(vault|encrypt|decrypt|private\s+key|private\s+account|leaked)\b",
        r"\b(production|deploy|release|drop\s+database|truncate|migration)\b",
        r"\b(architecture\s+invariants|core\s+refactor|breaking\s+change)\b",
        r"\b(final\s+year\s+project|fyp|spring\s+ai)\b",
    ]

    ROUTINE_PATTERNS = [
        r"\b(boilerplate|scaffold|test|unit\s+test|mock|fixture|pytest)\b",
        r"\b(scrape|scraper|crawl|extract\s+data|regex|format|clean\s+up)\b",
        r"\b(readme|docstring|documentation|markdown|comment)\b",
        r"\b(dto|getter|setter|schema|json\s+schema|dataclass)\b",
    ]

    EXPLICIT_HIGH_PRIORITY = [
        r"\b(high\s+priority|urgent|critical|highest\s+priority|p0)\b",
    ]

    EXPLICIT_LOW_PRIORITY = [
        r"\b(low\s+priority|trivial|background|p3)\b",
    ]

    @classmethod
    def evaluate(cls, task: str, context: Optional[str] = None) -> TriageDecision:
        lower_task = (task + " " + (context or "")).lower()

        # 1. Inspect PC Hardware Status (RAM & CPU load) to prevent bottlenecks
        hw = get_hardware_status()
        avail_ram = hw.get("avail_ram_gb", 8.0)
        load_pct = hw.get("load_percent", 50)
        cpu_load = hw.get("cpu_load_percent", 15.0)

        if avail_ram < 3.0 or load_pct >= 85 or cpu_load >= 85.0:
            bottleneck_risk = "HIGH"
        elif avail_ram < 5.5 or load_pct >= 70 or cpu_load >= 65.0:
            bottleneck_risk = "MEDIUM"
        else:
            bottleneck_risk = "LOW"

        # 2. Determine Severity & Complexity Score with explicit user priority override
        explicit_high = any(re.search(pat, lower_task) for pat in cls.EXPLICIT_HIGH_PRIORITY)
        explicit_low = any(re.search(pat, lower_task) for pat in cls.EXPLICIT_LOW_PRIORITY)
        is_critical = explicit_high or any(re.search(pat, lower_task) for pat in cls.CRITICAL_PATTERNS)
        is_routine = not explicit_high and (explicit_low or any(re.search(pat, lower_task) for pat in cls.ROUTINE_PATTERNS))

        if is_critical:
            severity = SeverityLevel.CRITICAL
            complexity = 10 if explicit_high else 9
            cognition = "MAX_FRONTIER"
            invariants = [
                "Zero data leakage: verify no credentials exposed",
                "Senior engineer audit required before applying diffs",
                "Require explicit test pass with 100% assertions",
            ]
        elif is_routine:
            severity = SeverityLevel.ROUTINE
            complexity = 2 if explicit_low else 3
            cognition = "FAST_TOKEN_EFFICIENT"
            invariants = [
                "Surgical implementation: touch only target test/model files",
                "Standard library first, zero speculative dependencies",
            ]
        else:
            severity = SeverityLevel.MODERATE
            complexity = 6
            cognition = "COGNITIVE_BALANCED"
            invariants = [
                "Preserve existing architecture without collateral changes",
                "Adhere to user taste profile & Karpathy simplicity",
            ]

        # 3. Dynamic Subagent & Worker Count Scaling
        if bottleneck_risk == "HIGH":
            subagents_count = 1
            workers_per_sub = 1
        elif severity == SeverityLevel.CRITICAL:
            subagents_count = 1 if bottleneck_risk != "LOW" else 2
            workers_per_sub = 1
        elif severity == SeverityLevel.MODERATE:
            subagents_count = 2 if bottleneck_risk == "MEDIUM" else 3
            workers_per_sub = 2
        else:
            subagents_count = 1 if bottleneck_risk == "MEDIUM" else 2
            workers_per_sub = 2

        # 4. Strategy & Worker Assignment based on Severity + Hardware Headroom
        if severity == SeverityLevel.CRITICAL:
            strategy = ExecutionStrategy.FRONTIER_DIRECT
            recommended_worker = "frontier_manager"
            rationale = "High-security or user-flagged critical priority requires Frontier direct navigation."
        elif bottleneck_risk == "HIGH":
            strategy = ExecutionStrategy.LIGHTWEIGHT_CLI
            recommended_worker = "hermes-cli"
            rationale = f"Host resource pressure detected ({avail_ram}GB free RAM, {cpu_load}% CPU). Routing to zero-RAM Hermes CLI to protect active processes."
        elif severity == SeverityLevel.ROUTINE:
            strategy = ExecutionStrategy.LOCAL_WORKER_WITH_MANAGER_REVIEW
            best_worker = recommend_agent("code_synthesis")
            recommended_worker = best_worker if best_worker != "frontier_manager" else "qwen2.5-coder:7b"
            rationale = "Boilerplate/testing task routed to parallel local workers to preserve frontier tokens (Boss-Worker)."
        else:
            strategy = ExecutionStrategy.LOCAL_WORKER_WITH_MANAGER_REVIEW
            recommended_worker = "hermes"
            rationale = "Balanced task delegated to parallel local workers with junior boss verification."

        return TriageDecision(
            task=task,
            severity=severity,
            complexity_score=complexity,
            execution_strategy=strategy,
            recommended_worker=recommended_worker,
            bottleneck_risk=bottleneck_risk,
            avail_ram_gb=avail_ram,
            load_percent=load_pct,
            rationale=rationale,
            invariants=invariants,
            subagents_count=subagents_count,
            workers_per_subagent=workers_per_sub,
            cognition_power=cognition,
            cpu_load_percent=cpu_load,
            autonomous_decision=True,
        )


def judge_task_severity(task: str, context: Optional[str] = None) -> TriageDecision:
    """Convenience wrapper to triage a task and determine the multi-agent routing."""
    return SeverityTriageEngine.evaluate(task, context)


def should_delegate_to_worker(task: str) -> Tuple[bool, TriageDecision]:
    """Check if task should be pushed to worker/subagent rather than burning frontier tokens."""
    decision = judge_task_severity(task)
    delegate = decision.severity in (SeverityLevel.ROUTINE, SeverityLevel.MODERATE)
    return delegate, decision
