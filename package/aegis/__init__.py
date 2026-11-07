"""AegisBrain - Zero-UI Background Neural Memory Bus and Agent Orchestrator."""

__version__ = "0.1.0"

import sys

# Ensure UTF-8 output on Windows consoles and daemons to avoid cp1252 errors with emojis
if sys.platform == "win32":
    try:
        if sys.stdout is not None:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr is not None:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .config import (
    get_aegis_dir,
    get_db_path,
    get_active_context_path,
    get_current_mode,
    set_current_mode,
)
from .db import (
    init_db,
    record_decision,
    record_session,
    search_memories,
    track_pr,
    get_tracked_prs,
    get_recent_decisions,
    get_active_alerts,
)
from .governor import generate_active_context
from .hooks import bootstrap_agent_session, seed_initial_knowledge
from .caffeinate import (
    enable_caffeinate,
    disable_caffeinate,
    is_caffeinate_active,
    get_caffeinate_status,
    remote_suspend_pc,
    remote_shutdown_pc,
)
from .remote import (
    send_whatsapp_message,
    handle_remote_command,
    load_remote_config,
    save_remote_config,
)
from .ceo_stress_test import YCCEOStressTester, CEOCritique
from .truth_seeking import SkepticalTruthReviewer, MistakeLedger, SkepticalAuditResult
from .survival_mode import (
    is_survival_mode,
    enable_survival_mode,
    disable_survival_mode,
    format_post_response_suggestions_and_review,
)
from .confidence import (
    record_score,
    get_agent_confidence,
    format_confidence_report,
    recommend_agent,
)
from .severity_triage import (
    judge_task_severity,
    should_delegate_to_worker,
    SeverityLevel,
    ExecutionStrategy,
    TriageDecision,
)
from .armory import (
    CORE_NATIVE_SKILLS,
    is_core_skill,
    get_armory_dir,
    init_armory_db,
    evaluate_skill_security,
    register_skill,
    delete_skill,
    project_skill,
    mount_skill,
    unmount_skill,
    project_all_skills,
    queue_skill_for_mining,
    process_miner_queue,
    search_armory,
    list_armory_skills,
    get_skill,
    format_armory_status,
)
