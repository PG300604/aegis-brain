"""AegisBrain Universal Agent Interchangeability Protocol.

Enables seamless interchangeability of agents across architectural tiers:
- Tier 1 (Boss / Executive Authority): Any agent (Antigravity, OpenCode, Codex, Claude, Hermes, etc.)
  with custom model specification (e.g. Codex with gpt-6-astra, OpenCode with claude-opus-5-5).
- Tier 3 (Execution Workers): Any execution engine (OpenCode, Hermes, Ollama, Codex, Claude, etc.)
  synthesizing candidate code drafts with 0 frontier token waste.
- Standardized Universal Execution Envelope normalizing task dispatch, worker responses,
  4-Decision Quality Architecture Gate audit scores, and executive deliverables.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from aegis.db import get_active_boss, get_active_worker, set_active_boss, set_active_worker

logger = logging.getLogger(__name__)


class AgentRole(str, Enum):
    BOSS = "boss"
    WORKER = "worker"


@dataclass
class AgentDescriptor:
    name: str
    model: Optional[str] = None
    role: AgentRole = AgentRole.WORKER
    executable: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        if self.model:
            return f"{self.name} ({self.model})"
        return self.name


@dataclass
class AgentExecutionResponse:
    worker_name: str
    worker_model: Optional[str] = None
    raw_output: str = ""
    clean_code: str = ""
    success: bool = True
    tokens_saved: int = 0
    duration_ms: float = 0.0
    audit_details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    status: str = "completed"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "worker_name": self.worker_name,
            "worker_model": self.worker_model,
            "raw_output": self.raw_output,
            "clean_code": self.clean_code,
            "success": self.success,
            "tokens_saved": self.tokens_saved,
            "duration_ms": round(self.duration_ms, 2),
            "audit_details": self.audit_details,
            "issues": self.issues,
            "status": self.status,
        }


@dataclass
class UniversalAgentEnvelope:
    task: str
    boss_name: str
    boss_model: Optional[str] = None
    worker_name: str = "hermes"
    worker_model: Optional[str] = None
    execution_response: AgentExecutionResponse = field(
        default_factory=lambda: AgentExecutionResponse(worker_name="unknown")
    )
    quality_gate_passed: bool = True
    gate_scores: Dict[str, bool] = field(
        default_factory=lambda: {
            "karpathy_simplicity": True,
            "unslop_turnitout": True,
            "security_redteam": True,
            "dual_env_verification": True,
        }
    )
    executive_deliverable: str = ""
    tokens_saved: int = 0
    status: str = "completed"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "boss_name": self.boss_name,
            "boss_model": self.boss_model,
            "worker_name": self.worker_name,
            "worker_model": self.worker_model,
            "execution_response": self.execution_response.to_dict(),
            "quality_gate_passed": self.quality_gate_passed,
            "gate_scores": self.gate_scores,
            "executive_deliverable": self.executive_deliverable,
            "tokens_saved": self.tokens_saved,
            "status": self.status,
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def map_worker_name_to_type(name: str):
    """Map string worker name to WorkerType enum safely."""
    from aegis.hierarchy import WorkerType

    norm = name.lower().strip()
    if norm in ("opencode", "opencode-interpreter"):
        return WorkerType.OPENCODE
    if norm in ("codex", "openai-codex"):
        return WorkerType.CODEX
    if norm in ("claude", "claude-code"):
        return WorkerType.CLAUDE
    if norm in ("ollama", "moe", "local"):
        return WorkerType.MOE
    if norm in ("gemini", "agy"):
        return WorkerType.GEMINI
    if norm in ("local_compiler", "compiler"):
        return WorkerType.LOCAL_COMPILER
    return WorkerType.HERMES


def dispatch_universal_task(
    task: str,
    boss_name: Optional[str] = None,
    boss_model: Optional[str] = None,
    worker_name: Optional[str] = None,
    worker_model: Optional[str] = None,
    simulate: bool = False,
    max_retries: int = 3,
    **kwargs: Any,
) -> UniversalAgentEnvelope:
    """Universal task dispatcher across arbitrary Boss and Worker agent combinations.
    
    1. Normalizes Boss (Tier 1) and Worker (Tier 3) agents from arguments or database persistence.
    2. Executes candidate drafting via Worker CLI (or simulation) using 0 frontier tokens.
    3. Runs candidate output through the 4-Decision Quality Architecture Gate.
    4. Constructs signed executive deliverable from the Tier 1 Boss.
    5. Returns standardized UniversalAgentEnvelope.
    """
    from aegis.hierarchy import SubagentNode, WorkerType

    # Resolve Boss Configuration
    active_boss = get_active_boss()
    resolved_boss_name = boss_name or active_boss.get("name") or "antigravity"
    resolved_boss_model = boss_model if boss_model is not None else active_boss.get("model")

    # Resolve Worker Configuration
    active_worker = get_active_worker()
    resolved_worker_name = worker_name or active_worker.get("name") or "hermes"
    resolved_worker_model = worker_model if worker_model is not None else active_worker.get("model")

    w_type = map_worker_name_to_type(resolved_worker_name)

    # Subagent Junior Boss to supervise the execution worker
    sa = SubagentNode(
        subagent_id=f"universal-{resolved_worker_name}-lead",
        name=f"{resolved_boss_name.capitalize()} Junior Boss (Supervising {resolved_worker_name.capitalize()})",
        domain="universal_execution",
        allowed_workers=[w_type],
    )

    t0 = time.time()
    ok, clean_code, audit_info = sa.execute_worker_with_coaching_loop(
        task_spec=task,
        worker_type=w_type,
        max_retries=max_retries,
        simulate=simulate,
    )
    elapsed_ms = (time.time() - t0) * 1000.0

    last_session = sa.worker_sessions[-1] if sa.worker_sessions else None
    raw_output = last_session.raw_output if last_session else ""
    tokens_saved = last_session.tokens_saved if last_session else (1050 if ok else 0)

    audit_details = audit_info.get("audit_details", {})
    gate_scores = audit_details.get(
        "gates",
        {
            "karpathy_simplicity": ok,
            "unslop_turnitout": ok,
            "security_redteam": ok,
            "dual_env_verification": ok,
        },
    )
    issues = audit_details.get("issues", [])

    status_str = audit_info.get("status", "completed" if ok else "failed")

    # Executive Deliverable signed off by Tier 1 Boss
    boss_label = resolved_boss_name.capitalize() + (f" ({resolved_boss_model})" if resolved_boss_model else "")
    worker_label = resolved_worker_name.capitalize() + (f" ({resolved_worker_model})" if resolved_worker_model else "")

    status_tag = "PASSED (4 Quality Gates Verified)" if ok else f"REVISION REQUIRED ({status_str})"
    deliverable = (
        f"# Executive Deliverable signed off by {boss_label}\n"
        f"**Task:** {task}\n"
        f"**Execution Worker:** {worker_label}\n"
        f"**Quality Verification Status:** {status_tag}\n\n"
        f"```python\n{clean_code}\n```"
    )

    exec_response = AgentExecutionResponse(
        worker_name=resolved_worker_name,
        worker_model=resolved_worker_model,
        raw_output=raw_output,
        clean_code=clean_code,
        success=ok,
        tokens_saved=tokens_saved,
        duration_ms=elapsed_ms,
        audit_details=audit_details,
        issues=issues,
        status=status_str,
    )

    envelope = UniversalAgentEnvelope(
        task=task,
        boss_name=resolved_boss_name,
        boss_model=resolved_boss_model,
        worker_name=resolved_worker_name,
        worker_model=resolved_worker_model,
        execution_response=exec_response,
        quality_gate_passed=ok,
        gate_scores=gate_scores,
        executive_deliverable=deliverable,
        tokens_saved=tokens_saved,
        status=status_str,
        metadata={
            "elapsed_ms": round(elapsed_ms, 2),
            "attempts": audit_info.get("attempts", 1),
            "simulated": simulate,
        },
    )

    return envelope
