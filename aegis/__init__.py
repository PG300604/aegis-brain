"""AegisBrain - Zero-UI Background Neural Memory Bus and Agent Orchestrator."""

__version__ = "0.1.0"

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
