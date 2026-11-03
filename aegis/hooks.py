from pathlib import Path
from typing import Optional
from .config import get_current_mode
from .db import init_db, record_decision, record_session, track_pr
from .governor import generate_active_context


def seed_initial_knowledge() -> None:
    """Seed initial project memory with Spring AI contribution & architectural decisions."""
    init_db()

    # Track Spring AI PR #7308
    track_pr(
        repo="spring-projects/spring-ai",
        pr_number=7308,
        title="Add missing GenAI request attributes to observations",
        status="open",
        labels=["status: waiting-for-triage"],
        ci_status="dco-passed",
    )

    # Key Architectural Decisions
    record_decision(
        category="ARCHITECTURE",
        title="OTel GenAI Request Attributes & Low Cardinality",
        decision="Omit attributes when values are null or empty string to avoid metric tag explosion.",
        rationale="Conforms to OpenTelemetry v1.37.0 semantic conventions and Spring AI conventions.",
        tags=["spring-ai", "opentelemetry", "observability", "metrics"],
    )

    record_decision(
        category="ARCHITECTURE",
        title="Backward-Compatible ChatOptions Extensions",
        decision="Use default getters returning null on ChatOptions interface, preserving constructors on DefaultChatOptions.",
        rationale="Guarantees zero breaking changes for existing model client implementations.",
        tags=["spring-ai", "java", "api-design"],
    )

    record_decision(
        category="INFRASTRUCTURE",
        title="Dedicated Open Source Development Drive",
        decision="Host all open-source repositories and development workspaces under P:\\open-source\\.",
        rationale="Preserves Drive C system storage and centralizes multi-agent development projects.",
        tags=["storage", "workspace", "windows"],
    )


def bootstrap_agent_session(agent_name: str, workspace_path: Optional[Path] = None) -> str:
    """Entry point called by any agent CLI (Antigravity, Hermes, OpenCode).

    Generates the ultra-compact active context, records the session, and returns
    the markdown prompt block.
    """
    path = workspace_path or Path.cwd()
    context = generate_active_context(path)

    if get_current_mode() == "public":
        import uuid
        session_id = f"{agent_name}-{uuid.uuid4().hex[:8]}"
        record_session(
            session_id=session_id,
            agent_name=agent_name,
            workspace_path=str(path),
            summary=f"Bootstrapped in {path.name}",
        )

    return context
