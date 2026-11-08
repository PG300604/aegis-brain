import argparse
import sys
from pathlib import Path
from .config import DEFAULT_HOST, DEFAULT_PORT, get_current_mode, get_db_path, set_current_mode
from .db import (
    get_active_alerts,
    get_recent_decisions,
    get_tracked_prs,
    init_db,
    record_decision,
    search_memories,
)
from .governor import generate_active_context
from .hooks import seed_initial_knowledge
from .server import run_daemon
from .service import (
    disable_autostart,
    enable_autostart,
    is_autostart_enabled,
    is_daemon_running,
    start_daemon,
    stop_daemon,
)
from .watchdog import sweep_tracked_prs
from .media import generate_media
from .hardware import format_hardware_report
from .governance import (
    load_governance_config,
    save_governance_config,
    format_governance_status,
    get_telemetry_terms,
)
from .diagnostics import format_diagnostic_markdown, get_github_issue_url
from .environment import format_environment_report, queue_pending_installation
from .taste import format_taste_display
from .planner import format_suggestion_panel, create_default_suggestions_for_task
from .orchestrator import run_manager_worker_pipeline, format_distillation_report
from .caffeinate import (
    enable_caffeinate,
    disable_caffeinate,
    get_caffeinate_status,
    remote_suspend_pc,
    remote_shutdown_pc,
    remote_lock_workstation,
    remote_block_input,
    remote_trigger_alarm,
)
from .remote import type_to_desktop
from .remote import (
    run_remote_setup_wizard,
    show_remote_status,
    run_remote_test,
    start_remote_session,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aegis",
        description="AegisBrain: Local Neural Memory & Agent Orchestrator",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # daemon
    daemon_parser = subparsers.add_parser("daemon", help="Start the background daemon server")
    daemon_parser.add_argument("--host", default=DEFAULT_HOST, help="Host to bind (default: 127.0.0.1)")
    daemon_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind (default: 8765)")
    daemon_parser.add_argument("--interval", type=int, default=300, help="Watchdog interval seconds (default: 300)")

    # status
    subparsers.add_parser("status", help="Show AegisBrain system status")

    # mode
    mode_parser = subparsers.add_parser("mode", help="Get or set public/private storage mode")
    mode_parser.add_argument("target", nargs="?", choices=["public", "private"], help="Target mode to switch to")

    # bootstrap
    boot_parser = subparsers.add_parser("bootstrap", help="Compile and display active context for an agent")
    boot_parser.add_argument("--workspace", "-w", type=Path, default=None, help="Workspace path to inspect")

    # search
    search_parser = subparsers.add_parser("search", help="Sub-millisecond FTS5 search across architectural memories")
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument("--limit", "-n", type=int, default=5, help="Max results")

    # recall (instant recall for recent tasks or query)
    recall_parser = subparsers.add_parser("recall", help="Instantly recall recent tasks, decisions, or search memories")
    recall_parser.add_argument("query", nargs="?", default=None, help="Optional search query keyword")
    recall_parser.add_argument("--limit", "-n", type=int, default=5, help="Max results (default: 5)")

    # decision
    dec_parser = subparsers.add_parser("decision", help="Record an architectural decision")
    dec_parser.add_argument("--category", "-c", default="GENERAL", help="Decision category")
    dec_parser.add_argument("--title", "-t", required=True, help="Decision title")
    dec_parser.add_argument("--desc", "-d", required=True, help="Decision content")
    dec_parser.add_argument("--rationale", "-r", default="", help="Rationale")
    dec_parser.add_argument("--tags", nargs="*", default=[], help="Tags")

    # seed
    subparsers.add_parser("seed", help="Seed default project memories (Spring AI PR #7308, etc.)")

    # poll
    subparsers.add_parser("poll", help="Run immediate watchdog sweep on tracked PRs")

    # start (detached daemon)
    subparsers.add_parser("start", help="Start background AegisBrain daemon")

    # stop (stop background daemon)
    subparsers.add_parser("stop", help="Stop running background AegisBrain daemon")

    # autostart
    auto_parser = subparsers.add_parser("autostart", help="Manage system logon autostart")
    auto_parser.add_argument("state", nargs="?", choices=["on", "off", "status"], default="status", help="Enable, disable, or query autostart")

    # caffeinate (anti-sleep wake-lock)
    caff_parser = subparsers.add_parser("caffeinate", help="Prevent system sleep while agents run")
    caff_parser.add_argument("state", nargs="?", choices=["on", "off", "status", "sleep", "shutdown", "lock"], default="status", help="Turn caffeinate on/off, inspect status, or trigger lock/sleep/shutdown")
    caff_parser.add_argument("--display", "-d", action="store_true", help="Also prevent display from turning off")

    # lock
    subparsers.add_parser("lock", help="Instantly lock screen (AI agents keep running in background)")

    # type (type into active desktop window)
    type_parser = subparsers.add_parser("type", help="Type text into active IDE window and submit")
    type_parser.add_argument("text", help="Text or prompt to type")
    type_parser.add_argument("--no-enter", action="store_true", help="Do not press Enter after typing")

    # remote (WhatsApp remote bridge)
    rem_parser = subparsers.add_parser("remote", help="Manage WhatsApp remote control and agent execution bridge")
    rem_parser.add_argument("action", nargs="?", choices=["start", "setup", "status", "test"], default="status", help="Start session, run setup wizard, view status, or send test ping")
    rem_parser.add_argument("--message", "-m", default=None, help="Custom test message string for 'test' action")

    # media (OpenHiggsfield AI generation bridge)
    media_parser = subparsers.add_parser("media", help="Generate AI image/video assets via OpenHiggsfield bridge")
    media_parser.add_argument("--model", "-m", default="flux-2", help="Model name (e.g. flux-2, seedance-2.5, kling-3, wan-2.6)")
    media_parser.add_argument("--prompt", "-p", required=True, help="Generation prompt description")
    media_parser.add_argument("--ratio", "-r", default="16:9", choices=["16:9", "9:16", "1:1", "4:3"], help="Aspect ratio (default: 16:9)")

    # config (User Model Governance)
    cfg_parser = subparsers.add_parser("config", help="View or modify model governance and resource limits")
    cfg_parser.add_argument("--manager", "-m", help="Frontier Manager model (e.g. gemini-3.8-flash-high, claude-3-7-sonnet)")
    cfg_parser.add_argument("--worker", "-w", help="Local worker model (e.g. auto, qwen2.5-coder:7b)")
    cfg_parser.add_argument("--telemetry", "-t", choices=["on", "off"], help="Toggle anonymous opt-in telemetry")
    cfg_parser.add_argument("--backend", "-b", choices=["ollama", "freetoken", "local"], help="Worker execution backend")
    cfg_parser.add_argument("--model-dir", "-d", help="Custom model storage disk/directory (e.g. P:\\aegis-models)")
    cfg_parser.add_argument("--moe-ram", type=float, help="Max RAM allocation cap for lightweight MoE (default: 7.5 GB)")

    # hardware (Resource Sizing Profile)
    subparsers.add_parser("hardware", help="Inspect workstation RAM and dynamic model sizing tier")

    # report (Diagnostic Bundler & GitHub Issue Generator)
    rep_parser = subparsers.add_parser("report", help="Generate sanitized diagnostic report and GitHub issue URL")
    rep_parser.add_argument("--issue", "-i", action="store_true", help="Print pre-filled 1-click GitHub issue URL")
    rep_parser.add_argument("--desc", "-d", default="", help="Description of issue for GitHub URL")

    # terms (Telemetry Policy Terms)
    subparsers.add_parser("terms", help="Display transparent zero-leakage telemetry policy")

    # env (Workstation Tool & Runtime Inspector)
    env_parser = subparsers.add_parser("env", help="Inspect workstation software tools, Ollama, OpenCode, and pending setups")
    env_parser.add_argument("--queue", "-q", nargs=3, metavar=("PACKAGE", "INSTALLER", "REASON"), help="Queue a pending software installation requirement")
    env_parser.add_argument("--admin", action="store_true", help="Flag that the queued package requires administrator elevation")

    # taste (User Taste Profile & Aesthetic Engine)
    subparsers.add_parser("taste", help="View user aesthetic preferences, coding doctrine, and persona alignment")

    # plan (Deep Planning & YC Feasibility Engine)
    plan_parser = subparsers.add_parser("plan", help="Generate Deep Planning, YC Feasibility, and Clarification Interview")
    plan_parser.add_argument("task", help="Task or decision to analyze")
    plan_parser.add_argument("--questions", "-q", type=int, default=6, help="Number of clarifying questions to generate (4-20)")

    # orchestrate (Manager-Worker Pipeline & Token Arbitrage)
    orch_parser = subparsers.add_parser("orchestrate", help="Run Manager-Worker task execution and record distillation trajectory")
    orch_parser.add_argument("task", nargs="?", default="", help="Task prompt to execute")
    orch_parser.add_argument("--simulate", "-s", action="store_true", help="Simulate worker draft for quick testing")
    orch_parser.add_argument("--stats", action="store_true", help="View cumulative tokens saved and distillation history")

    # triage (Task Severity & Bottleneck-Aware Multi-Agent Dispatcher)
    triage_parser = subparsers.add_parser("triage", help="Judge task severity and recommend multi-agent execution strategy")
    triage_parser.add_argument("task", help="Task description to triage")

    # hierarchy (3-Tier Multi-Agent Power & Quality Structure)
    hier_parser = subparsers.add_parser("hierarchy", help="Display 3-Tier Multi-Agent Hierarchy, bottleneck risk, and active tree")
    hier_parser.add_argument("task", nargs="?", default="", help="Optional task to plan hierarchy for")
    hier_parser.add_argument("--plan", "-p", action="store_true", help="Generate full planning phase, research context, and implementation options with pros/cons")
    hier_parser.add_argument("--execute", "-e", action="store_true", help="Execute hierarchy with worker coaching loop")
    hier_parser.add_argument("--simulate", "-s", action="store_true", help="Simulate worker execution for testing")
    hier_parser.add_argument("--worker", "-w", choices=["hermes", "claude", "codex", "opencode", "moe", "gemini"], default=None, help="Execution worker model/tool")

    # coach (Junior Boss Subagent Supervised Coaching Loop)
    coach_parser = subparsers.add_parser("coach", help="Junior Boss Subagent coaches execution workers (Hermes/Claude/Codex/MoE) through the 4 Quality Gates")
    coach_parser.add_argument("task", help="Task specification for worker execution")
    coach_parser.add_argument("--worker", "-w", choices=["hermes", "claude", "codex", "opencode", "moe", "gemini"], default="hermes", help="Target execution worker")
    coach_parser.add_argument("--simulate", "-s", action="store_true", help="Simulate worker draft and coaching corrections")
    coach_parser.add_argument("--retries", "-r", type=int, default=3, help="Max coaching retries")

    # scout (Autonomous Skill Scout & Arsenal Intelligence)
    scout_parser = subparsers.add_parser("scout", help="Autonomous skill discovery matching user taste and niches")
    scout_parser.add_argument("--run", "-r", action="store_true", help="Run active skill scan and store discovered skills")
    scout_parser.add_argument("--niche", "-n", help="Filter discovered skills by niche (e.g. video, backend, seo, frontend, ai-ml)")
    scout_parser.add_argument("--install", "-i", help="Mark a discovered skill as installed in Arsenal")
    scout_parser.add_argument("--digest", "-d", action="store_true", help="Send weekly digest to Telegram")

    # moe (Dynamic MoE & Latency Scheduler)
    moe_parser = subparsers.add_parser("moe", help="Dynamic MoE routing, latency estimation, and RAM headroom check")
    moe_parser.add_argument("--tier", "-t", choices=["constrained", "moe_lightweight", "frontier_arbitrage"], help="Force specific model execution tier")
    moe_parser.add_argument("--tokens", type=int, default=350, help="Estimated output tokens for latency calculation (default: 350)")

    # graph (AST Codebase Graph Traversal)
    graph_parser = subparsers.add_parser("graph", help="Query or index AST codebase knowledge graph without visual bloat")
    graph_parser.add_argument("--query", "-q", help="Search graph symbols, functions, or classes")
    graph_parser.add_argument("--index", "-i", action="store_true", help="Force re-indexing of current workspace")
    graph_parser.add_argument("--neighbors", "-n", help="Inspect caller/callee edges for a specific node ID")

    # task (Episodic Task Lifecycle & Memory Compaction)
    task_parser = subparsers.add_parser("task", help="Manage ongoing tasks, future ideas, and memory compaction")
    task_parser.add_argument("action", nargs="?", choices=["list", "add", "done", "history"], default="list", help="Task action (default: list)")
    task_parser.add_argument("task_id_or_title", nargs="?", default="", help="Task ID (for done) or Title (for add)")
    task_parser.add_argument("--desc", "-d", default="", help="Task description")
    task_parser.add_argument("--cat", "-c", default="feature", help="Category: feature, bugfix, idea, model-setup")
    task_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], default="medium", help="Priority level")
    task_parser.add_argument("--outcome", "-o", default="", help="Completion outcome details")

    # sandbox (Isolated Execution Sandbox & Red-Team Audit)
    sb_parser = subparsers.add_parser("sandbox", help="Audit and execute code in an isolated security sandbox")
    sb_parser.add_argument("target", help="Code string or path to python file")
    sb_parser.add_argument("--audit-only", "-a", action="store_true", help="Perform static Red-Team vulnerability audit only")

    # swarm (Hierarchical Nested Multi-Agent Swarm)
    swarm_parser = subparsers.add_parser("swarm", help="Execute nested 4-tier multi-agent swarm across domain leads")
    swarm_parser.add_argument("task", help="Macro objective or task specification")
    swarm_parser.add_argument("--simulate", "-s", action="store_true", help="Simulate local worker outputs")

    # away (Toggle remote away mode & terminal streaming)
    away_parser = subparsers.add_parser("away", help="Toggle Away Mode & terminal output streaming to mobile")
    away_parser.add_argument("state", nargs="?", choices=["on", "off", "status"], default="status", help="Toggle state (on/off)")

    # nav (Navigate terminal logs)
    nav_parser = subparsers.add_parser("nav", help="Browse terminal output pages from desktop or mobile mirror")
    nav_parser.add_argument("page", nargs="?", type=int, default=1, help="Page number to inspect (default: 1)")

    # snapshot (Restore point creation & inspection)
    snap_parser = subparsers.add_parser("snapshot", help="Create or list agent configuration restore points")
    snap_parser.add_argument("action", nargs="?", choices=["create", "list"], default="list", help="Action (create/list)")
    snap_parser.add_argument("--name", "-n", default=None, help="Optional friendly name for the snapshot")
    snap_parser.add_argument("--reason", "-r", default="manual", help="Reason for creating snapshot")

    # restore / rollback
    restore_parser = subparsers.add_parser("restore", help="Rollback agent configuration and rules to a previous restore point")
    restore_parser.add_argument("snapshot_id", nargs="?", default="latest", help="Snapshot ID or partial name to restore")

    # browse (Lightweight AI Browser)
    browse_parser = subparsers.add_parser("browse", help="Fetch and distill web content into token-efficient markdown (Jev-compatible)")
    browse_parser.add_argument("url", help="URL to browse and distill")
    browse_parser.add_argument("--chars", "-c", type=int, default=4000, help="Max characters to return (default: 4000)")

    # research (Autonomous Skill Sourcing & Web Exploration)
    res_parser = subparsers.add_parser("research", help="Autonomous domain research and skill scraper")
    res_parser.add_argument("query", help="Topic or research objective")

    # align (Educational Concept Briefing & Matt Pocock Grill-Me Interview)
    align_parser = subparsers.add_parser("align", help="Run interactive concept education and Grill-Me diagnostic interview")
    align_parser.add_argument("task", help="Macro objective or technology to align on")

    # pipeline (4-Stage Quality Gates: Unslop, Red-Team, GitGuardian, Sandbox)
    pipe_parser = subparsers.add_parser("pipeline", help="Execute 4-stage post-processing quality gates on code output")
    pipe_parser.add_argument("target", help="Code string or file path to evaluate")
    pipe_parser.add_argument("--sandbox", "-s", action="store_true", help="Execute candidate in ephemeral sandbox")

    # dashboard (Feedback, Benchmarks & GUI Dashboard)
    dash_parser = subparsers.add_parser("dashboard", help="Display AegisBrain benchmarks, feedbacks, and Web GUI")
    dash_parser.add_argument("--tui", action="store_true", help="Render ANSI terminal UI")
    dash_parser.add_argument("--open", "-o", action="store_true", help="Open Web GUI in default browser")

    # feedback (Submit critique and ratings to memory)
    feed_parser = subparsers.add_parser("feedback", help="Submit rating and critique to Aegis memory for continuous evolution")
    feed_parser.add_argument("comment", help="Feedback text")
    feed_parser.add_argument("--cat", "-c", default="general", help="Category (e.g. code_quality, speed, security)")
    feed_parser.add_argument("--rating", "-r", type=int, default=5, choices=[1, 2, 3, 4, 5], help="Rating 1-5 stars")

    # briefing / hi (Greeting & Offline Task Synchronization)
    brief_parser = subparsers.add_parser("briefing", aliases=["hi", "greeting"], help="Greet user, synchronize offline PRs/alerts, and review pending tasks")
    brief_parser.add_argument("--name", "-n", default=None, help="User name to greet (defaults to current system user)")

    # bye / session-end (Graceful Session Close, Snapshot & Context Compaction)
    bye_parser = subparsers.add_parser("bye", aliases=["close-session", "session-end"], help="Create session snapshot, compress context, and persist to brain DB")
    bye_parser.add_argument("--summary", "-s", default="", help="Summary of work completed in session")
    bye_parser.add_argument("--agent", "-a", default="antigravity", help="Agent name (default: antigravity)")

    # optimize (Proactive Arsenal Skill & Web Research Recommendations)
    opt_parser = subparsers.add_parser("optimize", help="Proactively recommend highest-scoring Arsenal skills and web research vectors")
    opt_parser.add_argument("task", nargs="+", help="Target task, technology, or feature prompt")

    # ceo (YC CEO Ideation & Stress-Testing)
    ceo_parser = subparsers.add_parser("ceo", help="YC CEO ideation stress-test & feasibility critique")
    ceo_parser.add_argument("idea", nargs="+", help="Product concept or architectural proposal to stress-test")

    # challenge (Anti-Sycophancy & Skeptical Truth-Seeking)
    chal_parser = subparsers.add_parser("challenge", help="Anti-sycophancy and skeptical truth-seeking audit")
    chal_parser.add_argument("target", nargs="+", help="Code snippet, file path, or plan to challenge")

    # mistakes (Mistake Ledger & Environment Trap Recall)
    mist_parser = subparsers.add_parser("mistakes", help="Mistake ledger for agent learning and avoiding past traps")
    mist_sub = mist_parser.add_subparsers(dest="mistake_action", help="Mistake action")
    
    m_list = mist_sub.add_parser("list", help="List recorded mistakes")
    m_list.add_argument("--limit", "-n", type=int, default=10, help="Max entries to return")

    m_recall = mist_sub.add_parser("recall", help="Recall relevant mistakes for a task or topic")
    m_recall.add_argument("query", help="Task or technology keyword (e.g. windows, git, python)")

    # act / nlp / do (Zero-Command Natural Language Intent Router)
    act_parser = subparsers.add_parser("act", aliases=["nlp", "do"], help="Execute any natural language instruction via NLP Intent Router")
    act_parser.add_argument("query", nargs="+", help="Natural language request or conversation text")

    # sensory / ingest / reel (Multi-Platform Reel & Social Sensory Ingestion Pipeline)
    sens_parser = subparsers.add_parser("sensory", aliases=["ingest", "reel"], help="Ingest reel/video/social post, transcribe audio with Whisper, extract FFmpeg frames, and evaluate feasibility")
    sens_parser.add_argument("url", help="Media or post URL (Instagram, TikTok, YouTube, Reddit, X/Twitter)")
    sens_parser.add_argument("--out", "-o", default=None, help="Custom output directory")

    # radar (Community Trends & Tracked Creators Radar)
    radar_parser = subparsers.add_parser("radar", help="Scan tech subreddits (LocalLLaMA, etc.) and tracked creator updates")
    radar_parser.add_argument("--sub", "-s", default=None, help="Specific subreddit to inspect (e.g. LocalLLaMA)")

    # telegram / tg (Lightweight Mobile Telegram Ingestion Queue & Idle Processor)
    tg_parser = subparsers.add_parser("telegram", aliases=["tg"], help="Telegram bot queue: poll updates, check status, or drain queue during idle periods")
    tg_sub = tg_parser.add_subparsers(dest="tg_action", help="Telegram action")
    
    tg_setup = tg_sub.add_parser("setup", help="Configure Telegram Bot Token")
    tg_setup.add_argument("token", nargs="+", help="Bot token from @BotFather")
    
    tg_poll = tg_sub.add_parser("poll", help="Poll unread messages from Telegram into local queue")
    
    tg_status = tg_sub.add_parser("status", help="Show Telegram queue metrics and system idle status")
    
    tg_drain = tg_sub.add_parser("drain", help="Drain and process pending links in queue")
    tg_drain.add_argument("--force", "-f", action="store_true", help="Process immediately even if system is not idle")
    tg_drain.add_argument("--limit", "-l", type=int, default=5, help="Max items to process")
    tg_drain.add_argument("--threshold", "-t", type=float, default=35.0, help="Max CPU percent threshold to consider system idle")

    tg_listen = tg_sub.add_parser("listen", help="Run polling loop that drains automatically when system is idle")
    tg_listen.add_argument("--interval", "-i", type=int, default=15, help="Polling interval in seconds")

    m_record = mist_sub.add_parser("record", help="Record a verified mistake and fix into ledger")
    m_record.add_argument("--task", required=True, help="Task during which mistake occurred")
    m_record.add_argument("--desc", required=True, help="Description of mistake")
    m_record.add_argument("--cause", required=True, help="Root cause")
    m_record.add_argument("--fix", required=True, help="Corrective action / solution")
    m_record.add_argument("--tags", nargs="*", default=[], help="Tags (e.g. windows ntfs git)")

    # armory (Clean-Room Global Skill Armory & Cross-Agent Projection)
    armory_parser = subparsers.add_parser("armory", help="Aegis Global Skill Armory: FTS5 search, 4-gate security, cross-agent projection")
    armory_sub = armory_parser.add_subparsers(dest="armory_action", help="Armory action")

    armory_sub.add_parser("status", help="Show Global Skill Armory status")

    arm_list = armory_sub.add_parser("list", help="List registered skills")
    arm_list.add_argument("--category", "-c", default=None, help="Category filter")
    arm_list.add_argument("--status", "-s", default="active", help="Status filter (active/quarantined)")

    arm_search = armory_sub.add_parser("search", help="Sub-millisecond FTS5 search across armory skills")
    arm_search.add_argument("query", help="Search query")
    arm_search.add_argument("--limit", "-n", type=int, default=10, help="Max results")

    arm_inspect = armory_sub.add_parser("inspect", help="Inspect metadata for a skill")
    arm_inspect.add_argument("name", help="Skill name")

    arm_scan = armory_sub.add_parser("scan", help="Run 4-gate quarantine security evaluation on a skill file")
    arm_scan.add_argument("path", help="Path to SKILL.md file")

    arm_mount = armory_sub.add_parser("mount", help="Project / mount a skill into an agent directory")
    arm_mount.add_argument("name", help="Skill name")
    arm_mount.add_argument("--agent", "-a", default="antigravity", help="Target agent (antigravity, claude, hermes, opencode)")
    arm_mount.add_argument("--dir", "-d", type=Path, default=None, help="Target directory path")

    arm_unmount = armory_sub.add_parser("unmount", help="Unmount a skill from an agent directory")
    arm_unmount.add_argument("name", help="Skill name")
    arm_unmount.add_argument("--agent", "-a", default="antigravity", help="Target agent")
    arm_unmount.add_argument("--dir", "-d", type=Path, default=None, help="Target directory path")

    arm_mine = armory_sub.add_parser("mine", help="Queue a URL for mining or process mining queue")
    arm_mine.add_argument("url", nargs="?", default=None, help="Source URL to queue for mining")
    arm_mine.add_argument("--process", action="store_true", help="Process pending items in miner queue")

    arm_delete = armory_sub.add_parser("delete", help="Delete a skill (core native skills are protected)")
    arm_delete.add_argument("name", help="Skill name")

    arm_profile = armory_sub.add_parser("profile", help="View or switch active arsenal archetype profile")
    arm_profile.add_argument("name", nargs="?", choices=["developer", "creator", "security", "omni"], help="Target archetype profile name")

    # setup (Role-Based Dynamic Arsenal Installation Wizard)
    setup_parser = subparsers.add_parser("setup", help="Role-based Arsenal Installation & Archetype Setup Wizard")
    setup_parser.add_argument("--profile", "-p", choices=["developer", "creator", "security", "omni"], help="Target archetype profile name")

    # unslop
    unslop_parser = subparsers.add_parser(
        "unslop",
        aliases=["deslop"],
        help="Consolidated AI slop removal (code, prose, UI, and AI hallmarks)",
    )
    unslop_parser.add_argument(
        "--file", "-f",
        type=Path,
        default=None,
        help="Target file to scrub (modifies in place or prints if --stdout)",
    )
    unslop_parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Input text string (reads from stdin if omitted and no --file)",
    )
    unslop_parser.add_argument(
        "--deep", "-d",
        action="store_true",
        help="Enable second-pass AST, stock buzzword, and UI slop scrubbing",
    )
    unslop_parser.add_argument(
        "--mode", "-m",
        choices=["auto", "code", "prose", "ui"],
        default="auto",
        help="Content mode (default: auto)",
    )
    unslop_parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of in-place editing when --file is given",
    )
    unslop_parser.add_argument(
        "--check",
        action="store_true",
        help="Check only: exit with code 1 if slop is detected",
    )

    # jev
    jev_parser = subparsers.add_parser(
        "jev",
        help="TypeSafe AI-inspired Jev Semantic Decision Engine: sub-100ms routing, risk gating, and skill pruning",
    )
    jev_sub = jev_parser.add_subparsers(dest="jev_action")

    j_decide = jev_sub.add_parser("decide", help="Make sub-100ms decision: risk gating, model routing, and skill pruning")
    j_decide.add_argument("prompt", help="Input prompt / task description")
    j_decide.add_argument("--json", action="store_true", help="Output raw JSON")

    j_route = jev_sub.add_parser("route", help="Route prompt to model tier (Tier 1/2/3)")
    j_route.add_argument("prompt", help="Input prompt / task description")
    j_route.add_argument("--json", action="store_true", help="Output raw JSON")

    j_status = jev_sub.add_parser("status", help="Show Jev Semantic Engine status and metrics")
    j_status.add_argument("--json", action="store_true", help="Output raw JSON")

    # doctor (Host Capabilities & Diagnostics)
    doc_parser = subparsers.add_parser(
        "doctor",
        aliases=["check", "install"],
        help="Inspect host platform capabilities and run environment doctor",
    )
    doc_parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically prompt or run installation of missing optional tools",
    )
    doc_parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON for AI agents",
    )
    doc_parser.add_argument(
        "--setup",
        action="store_true",
        help="Launch Role-based Arsenal Installation & Archetype Setup Wizard",
    )
    doc_parser.add_argument(
        "--profile",
        "-p",
        choices=["developer", "creator", "security", "omni"],
        help="Directly select archetype pack during doctor/setup",
    )
    doc_parser.add_argument(
        "tool",
        nargs="?",
        default=None,
        help="Specific tool to install (when using 'install' alias)",
    )

    args = parser.parse_args()

    if args.command == "daemon":
        run_daemon(host=args.host, port=args.port, watchdog_interval=args.interval)

    elif args.command == "status":
        init_db()
        mode = get_current_mode()
        prs = get_tracked_prs()
        alerts = get_active_alerts()
        decisions = get_recent_decisions(limit=100)
        running = is_daemon_running()
        auto_enabled = is_autostart_enabled()

        print("=== AegisBrain Status ===")
        print(f"Daemon:        {'RUNNING (http://127.0.0.1:8765)' if running else 'STOPPED'}")
        print(f"Autostart:     {'ENABLED (starts on login/wake)' if auto_enabled else 'DISABLED'}")
        print(f"Mode:          {mode.upper()}")
        caff = get_caffeinate_status()
        caff_str = f"ACTIVE ({caff['uptime_seconds']}s)" if caff["active"] else "INACTIVE"
        print(f"Caffeinate:    {caff_str}")
        db_p = get_db_path()
        print(f"Database:      {db_p} ({'Exists' if db_p.exists() else 'Not initialized'})")
        print(f"Decisions:     {len(decisions)} recorded")
        print(f"Tracked PRs:   {len(prs)}")
        for pr in prs:
            print(f"  - {pr['repo']}#{pr['pr_number']}: {pr['title']} [{pr['status']}]")
        print(f"Active Alerts: {len(alerts)}")
        for a in alerts:
            print(f"  - [{a['category']}] {a['message']}")

    elif args.command == "mode":
        if args.target:
            set_current_mode(args.target)
            print(f"[AegisBrain] Mode set to: {args.target.upper()}")
        else:
            print(f"[AegisBrain] Current mode: {get_current_mode().upper()}")

    elif args.command == "bootstrap":
        ctx = generate_active_context(args.workspace)
        print(ctx)

    elif args.command == "search":
        results = search_memories(args.query, limit=args.limit)
        print(f"Found {len(results)} matches for '{args.query}':\n")
        for idx, r in enumerate(results, 1):
            print(f"[{idx}] [{r.get('category')}] {r.get('title')}")
            print(f"    Decision:  {r.get('decision')}")
            if r.get("rationale"):
                print(f"    Rationale: {r.get('rationale')}")
            print()

    elif args.command == "recall":
        if args.query:
            results = search_memories(args.query, limit=args.limit)
            header = f"Matches for '{args.query}'"
        else:
            results = get_recent_decisions(limit=args.limit)
            header = "Recent Decisions and Workflows"

        print(f"=== AegisBrain Memory Recall ({header}) ===\n")
        if not results:
            print("No matching memories found.")
        for idx, r in enumerate(results, 1):
            created = r.get("created_at", "")
            time_str = f" [{created}]" if created else ""
            print(f"[{idx}] [{r.get('category')}]{time_str} {r.get('title')}")
            print(f"    Summary:   {r.get('decision')}")
            if r.get("rationale"):
                print(f"    Rationale: {r.get('rationale')}")
            tags = r.get("tags")
            if tags:
                if isinstance(tags, list):
                    print(f"    Tags:      {', '.join(tags)}")
            print()

    elif args.command == "decision":
        row_id = record_decision(
            category=args.category,
            title=args.title,
            decision=args.desc,
            rationale=args.rationale,
            tags=args.tags,
        )
        if row_id:
            print(f"[AegisBrain] Decision recorded with ID: {row_id}")
        else:
            print("[AegisBrain] Bypassed (system is in PRIVATE mode)")

    elif args.command == "seed":
        seed_initial_knowledge()
        print("[AegisBrain] Initial knowledge seeded successfully.")

    elif args.command == "poll":
        init_db()
        alerts = sweep_tracked_prs()
        print(f"[AegisBrain] Watchdog sweep complete. New alerts: {len(alerts)}")
        for a in alerts:
            print(f"  - {a}")

    elif args.command == "start":
        ok, msg = start_daemon()
        print(f"[AegisBrain] {msg}")

    elif args.command == "stop":
        ok, msg = stop_daemon()
        print(f"[AegisBrain] {msg}")

    elif args.command == "autostart":
        if args.state == "on":
            ok, msg = enable_autostart()
            print(f"[AegisBrain] {msg}")
        elif args.state == "off":
            ok, msg = disable_autostart()
            print(f"[AegisBrain] {msg}")
        else:
            enabled = is_autostart_enabled()
            running = is_daemon_running()
            print(f"Autostart: {'ENABLED' if enabled else 'DISABLED'}")
            print(f"Daemon:    {'RUNNING' if running else 'STOPPED'}")

    elif args.command == "caffeinate":
        if args.state == "on":
            ok, msg = enable_caffeinate(keep_display=args.display)
            print(f"[AegisBrain] {msg}")
        elif args.state == "off":
            ok, msg = disable_caffeinate()
            print(f"[AegisBrain] {msg}")
        elif args.state == "sleep":
            ok, msg = remote_suspend_pc()
            print(f"[AegisBrain] {msg}")
        elif args.state == "shutdown":
            ok, msg = remote_shutdown_pc(delay_seconds=10)
            print(f"[AegisBrain] {msg}")
        elif args.state == "lock":
            ok, msg = remote_lock_workstation()
            print(f"[AegisBrain] {msg}")
        else:
            st = get_caffeinate_status()
            active_str = f"ACTIVE ({st['uptime_seconds']}s)" if st["active"] else "INACTIVE"
            print("=== AegisBrain Caffeinate Status ===")
            print(f"Status:       {active_str}")
            print(f"Platform:     {st['platform']}")
            print(f"Keep Display: {st['keep_display']}")

    elif args.command == "remote":
        if args.action == "setup":
            run_remote_setup_wizard()
        elif args.action == "start":
            start_remote_session()
        elif args.action == "test":
            msg = args.message or "🟢 AegisBrain Remote Test Ping!"
            run_remote_test(msg)
        else:
            show_remote_status()

    elif args.command == "media":
        print(f"[AegisBrain] Media generation dispatch (OpenHiggsfield)")
        print(f"  Model:  {args.model}")
        print(f"  Prompt: {args.prompt}")
        print(f"  Ratio:  {args.ratio}")
        res = generate_media(model=args.model, prompt=args.prompt, aspect_ratio=args.ratio)
        status = res.get("status", "unknown")
        print(f"  Status: {status.upper()}")
        if "images" in res:
            for img in res["images"]:
                print(f"  Image:  {img.get('url')}")
        if "video" in res:
            print(f"  Video:  {res['video'].get('url')}")
        if "message" in res:
            print(f"  Note:   {res['message']}")
        if "error" in res:
            print(f"  Error:  {res['error']}")

    elif args.command == "lock":
        ok, msg = remote_lock_workstation()
        print(f"[AegisBrain] {msg}")

    elif args.command == "type":
        ok, msg = type_to_desktop(args.text, press_enter=not args.no_enter)
        print(f"[AegisBrain] {msg}")

    elif args.command == "config":
        gov_cfg = load_governance_config()
        changed = False
        if args.manager:
            gov_cfg["manager_model"] = args.manager
            changed = True
            print(f"[AegisBrain] Manager model set to: {args.manager}")
        if args.worker:
            gov_cfg["worker_model"] = args.worker
            changed = True
            print(f"[AegisBrain] Worker model set to: {args.worker}")
        if args.backend:
            gov_cfg["worker_provider"] = args.backend
            changed = True
            print(f"[AegisBrain] Worker backend set to: {args.backend}")
        if args.telemetry:
            val = (args.telemetry == "on")
            gov_cfg["telemetry_enabled"] = val
            gov_cfg["telemetry_acknowledged"] = True
            changed = True
            state_str = "ENABLED (Opted-in)" if val else "DISABLED (Default-Deny)"
            print(f"[AegisBrain] Telemetry set to: {state_str}")
        if args.model_dir:
            from .config import set_model_dir
            p = set_model_dir(args.model_dir)
            gov_cfg["model_dir"] = str(p)
            changed = True
            print(f"[AegisBrain] Model storage drive set to: {p}")
        if args.moe_ram:
            gov_cfg["max_moe_ram_gb"] = float(args.moe_ram)
            changed = True
            print(f"[AegisBrain] Max MoE RAM cap set to: {args.moe_ram} GB")
        
        if changed:
            save_governance_config(gov_cfg)
        else:
            print(format_governance_status())

    elif args.command == "hardware":
        print(format_hardware_report())

    elif args.command == "report":
        print(format_diagnostic_markdown())
        if args.issue or True:
            url = get_github_issue_url(title="User Issue via CLI", error_desc=args.desc)
            print(f"\n🔗 Submit Issue via GitHub (1-Click Pre-filled):\n{url}\n")

    elif args.command == "terms":
        print(get_telemetry_terms())

    elif args.command == "env":
        if args.queue:
            pkg, inst, reason = args.queue
            row_id = queue_pending_installation(pkg, inst, reason, requires_admin=args.admin)
            admin_tag = " (Admin Required)" if args.admin else ""
            print(f"[AegisBrain] Queued installation for '{pkg}'{admin_tag} with ID: {row_id}")
        else:
            print(format_environment_report())

    elif args.command == "taste":
        print(format_taste_display())

    elif args.command == "plan":
        from .deep_planner import DeepPlanningEngine
        q_count = getattr(args, "questions", 6) or 6
        deep_plan = DeepPlanningEngine.create_plan(args.task, question_count=q_count)
        print(deep_plan.to_markdown())

    elif args.command == "orchestrate":
        if args.stats or not args.task:
            print(format_distillation_report())
        else:
            print(f"[AegisBrain] Running Manager-Worker Orchestration for: {args.task}")
            res = run_manager_worker_pipeline(args.task, simulate_worker=args.simulate)
            print(f"• Manager (Boss):  {res['manager_model']}")
            print(f"• Worker (Synthesizer): {res['worker_model']} (Hardware Tier: {res['hardware_tier']})")
            print(f"• Invariants:      {len(res['invariants'])} enforced")
            print(f"• Critique:        {res['manager_critique']}")
            print(f"• Tokens Saved:    +{res['tokens_saved_estimate']} tokens")
            print(f"\nFinal Verified Output:\n{res['final_code']}")

    elif args.command == "scout":
        from .skill_scout import (
            run_skill_scout,
            get_discovered_skills,
            mark_skill_status,
            format_skill_scout_display,
            send_weekly_scout_digest,
        )
        if args.install:
            ok = mark_skill_status(args.install, "installed")
            if ok:
                print(f"[AegisBrain] Skill '{args.install}' marked as INSTALLED in Arsenal.")
            else:
                print(f"[AegisBrain] Skill '{args.install}' not found in scout database.")
        elif args.digest:
            sent = send_weekly_scout_digest()
            print(f"[AegisBrain] Telegram scout digest sent: {sent}")
        else:
            if args.run:
                run_skill_scout(niche_filter=args.niche)
            skills = get_discovered_skills()
            if args.niche:
                skills = [s for s in skills if args.niche.lower() in s.get("category", "").lower()]
            print(format_skill_scout_display(skills))

    elif args.command == "moe":
        from .moe_engine import format_tier_status_display, select_execution_tier
        if args.tier:
            res = select_execution_tier(user_choice=args.tier, estimated_output_tokens=args.tokens)
            print(f"[AegisBrain] Execution Tier Forced: {res['tier_name']}")
            print(f"• Model: `{res['model']}` | Speed: ~{res['throughput_tok_sec']} tok/s | Est Latency: ~{res['estimated_latency_sec']}s")
        else:
            print(format_tier_status_display(estimated_tokens=args.tokens))

    elif args.command == "graph":
        from .code_graph import get_active_graph
        graph = get_active_graph()
        if args.index:
            graph.index_workspace()
            print("[AegisBrain] Codebase AST graph re-indexed successfully.")
        if args.query:
            matches = graph.query_graph(args.query)
            print(f"Found {len(matches)} graph node matches for '{args.query}':\n")
            for m in matches:
                doc = f" - {m['docstring'][:60]}..." if m.get("docstring") else ""
                print(f"• `{m['name']}` [{m['kind'].upper()}] in `{m['file_path']}`{doc}")
        elif args.neighbors:
            res = graph.get_neighbors(args.neighbors)
            print(f"Neighbors for node `{args.neighbors}`:")
            print(f"• Inbound Dependents:  {len(res['incoming'])}")
            print(f"• Outbound Calls/Defs: {len(res['outgoing'])}")
        else:
            print(graph.format_summary())

    elif args.command == "task":
        from .task_lifecycle import create_task, list_active_tasks, complete_task, format_tasks_display
        act = args.action
        if act == "add":
            title = args.task_id_or_title or "Untitled Task"
            tid = create_task(title=title, description=args.desc, category=args.cat, priority=args.priority)
            print(f"[AegisBrain] Active task registered with ID: [#{tid}]")
        elif act == "done":
            try:
                tid = int(args.task_id_or_title)
                ok = complete_task(tid, outcome=args.outcome)
                if ok:
                    print(f"[AegisBrain] Task [#{tid}] completed! Shifted from active working memory to historical archive.")
                else:
                    print(f"[AegisBrain] Task [#{tid}] not found.")
            except ValueError:
                print("Usage: `aegis task done <id>`")
        elif act == "history":
            print(format_tasks_display(show_history=True))
        else:
            print(format_tasks_display(show_history=False))

    elif args.command == "sandbox":
        from .sandbox import RedTeamAuditor, run_in_sandbox, format_sandbox_report
        target_str = args.target
        p = Path(target_str)
        if p.exists() and p.is_file():
            code = p.read_text(encoding="utf-8", errors="replace")
        else:
            code = target_str

        if args.audit_only:
            audit = RedTeamAuditor.audit_code(code)
            print(format_sandbox_report(audit))
        else:
            res = run_in_sandbox(code)
            print(format_sandbox_report(res["audit"]))
            print(f"\nExecution Result (Exit: {res['exit_code']}):")
            if res["stdout"]:
                print(f"STDOUT:\n{res['stdout']}")
            if res["stderr"]:
                print(f"STDERR:\n{res['stderr']}")

    elif args.command == "swarm":
        from .swarm import run_nested_swarm, format_swarm_display
        print(f"[AegisBrain] Initializing 4-Tier Swarm for: {args.task}...")
        res = run_nested_swarm(args.task, simulate_workers=args.simulate, on_progress=print)
        print("\n" + format_swarm_display(res))

    elif args.command == "away":
        from .remote import is_away_mode_active, set_away_mode
        if args.state == "on":
            set_away_mode(True)
            print("[AegisBrain] Away Mode ACTIVATED. All terminal outputs and agent milestones are streaming to your phone.")
        elif args.state == "off":
            set_away_mode(False)
            print("[AegisBrain] Away Mode DEACTIVATED. Output streaming paused.")
        else:
            state = "ACTIVE" if is_away_mode_active() else "INACTIVE"
            print(f"[AegisBrain] Away Mode: {state}")

    elif args.command == "nav":
        from .remote import get_terminal_mirror
        mirror = get_terminal_mirror()
        items, page, total_pages = mirror.get_page(page=args.page, page_size=5)
        print(f"=== AegisBrain Terminal Mirror Buffer (Page {page}/{total_pages}) ===")
        if not items:
            print("(No logs captured yet)")
        for it in items:
            print(f"[{it['time_str']} {it['source'].upper()}] {it['text']}")

    elif args.command == "snapshot":
        from .snapshot import create_snapshot, list_snapshots
        if args.action == "create":
            res = create_snapshot(name=args.name, reason=args.reason)
            print(f"[AegisBrain] Snapshot created: {res['snapshot_id']} ({res['file_count']} files archived)")
        else:
            snaps = list_snapshots()
            print("=== AegisBrain Configuration Restore Points ===")
            if not snaps:
                print("  No snapshots found. Run `aegis snapshot create` to create a restore point.")
            for s in snaps:
                print(f"  • [{s.get('snapshot_id')}] {s.get('name')} - {s.get('reason')} ({s.get('created_at')})")

    elif args.command == "restore":
        from .snapshot import restore_snapshot, list_snapshots
        snap_id = args.snapshot_id
        if snap_id == "latest":
            snaps = list_snapshots()
            if not snaps:
                print("[AegisBrain] No snapshots available to restore.")
                return
            snap_id = snaps[0]["snapshot_id"]
        ok, msg = restore_snapshot(snap_id)
        status_lbl = "[OK]" if ok else "[ERROR]"
        print(f"[AegisBrain] {status_lbl} {msg}")

    elif args.command == "browse":
        from .browser import fetch_url_content
        print(f"[AegisBrain Browser] Fetching and distilling: {args.url}...")
        ok, content = fetch_url_content(args.url, max_chars=args.chars)
        if ok:
            print(content)
        else:
            print(f"[AegisBrain Browser Error] {content}")

    elif args.command == "research":
        from .browser import search_web_duckduckgo
        from .skill_scout import discover_skills
        print(f"[AegisBrain Research] Exploring web and skill arsenal for: {args.query}...")
        results = search_web_duckduckgo(args.query, max_results=4)
        skills = discover_skills(limit=3)
        print("\n--- High-Signal Search Insights ---")
        for r in results:
            print(f"• {r.get('title')}: {r.get('url')}\n  ↪ {r.get('snippet')}\n")
        print("--- Curated Domain Skills ---")
        for s in skills:
            print(f"• {s.name} ({s.niche}): {s.summary}")

    elif args.command == "align":
        from .alignment import AlignmentEngine
        print(f"[AegisBrain Alignment] Aligning on task: {args.task}...")
        edu = AlignmentEngine.generate_educational_blueprint(args.task)
        print("\n" + edu)
        questions = AlignmentEngine.generate_grill_me_interview(args.task)
        print("\n### ❓ Matt Pocock 'Grill Me' Diagnostic Interview")
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. {q['question']}")
            for opt in q['options']:
                print(f"   - {opt}")

    elif args.command == "pipeline":
        from .pipeline import QualityGatesPipeline
        target = args.target
        p = Path(target)
        if p.exists() and p.is_file():
            raw_text = p.read_text(encoding="utf-8", errors="replace")
        else:
            raw_text = target
        res = QualityGatesPipeline.run_pipeline(raw_text, run_sandbox=args.sandbox)
        print(f"=== AegisBrain Quality Gates Certification ===")
        print(f"Passed:            {'YES' if res.passed else 'NO'}")
        print(f"Security Score:    {res.security_score}%")
        print(f"Unslop Applied:    {'Yes' if res.unslop_applied else 'No'}")
        print(f"GitGuardian Alert: {len(res.secret_findings)} secrets flagged")
        print(f"Summary:           {res.summary}")
        if res.secret_findings:
            print("\n[CRITICAL BLOCKED SECRETS]:")
            for sf in res.secret_findings:
                print(f"  • {sf['detail']} (preview: {sf['preview']})")

    elif args.command == "dashboard":
        from .dashboard import format_dashboard_tui
        if args.open:
            if not is_daemon_running():
                print("[AegisBrain] Daemon is not active. Auto-starting in background...")
                start_daemon()
                import time
                for _ in range(15):
                    if is_daemon_running():
                        break
                    time.sleep(0.2)
            import webbrowser
            webbrowser.open("http://127.0.0.1:8765/dashboard")
            print("[AegisBrain] Dashboard opened at http://127.0.0.1:8765/dashboard")
        else:
            print(format_dashboard_tui())

    elif args.command in ["briefing", "hi", "greeting"]:
        from .briefing import OfflineBriefingEngine
        print(OfflineBriefingEngine.generate_briefing(user_name=args.name))

    elif args.command in ["bye", "close-session", "session-end"]:
        from .session_close import close_session, format_session_close_display
        res = close_session(agent_name=args.agent, summary=args.summary)
        print(format_session_close_display(res))

    elif args.command == "optimize":
        from .arsenal_optimizer import ArsenalOptimizer
        task_str = " ".join(args.task) if isinstance(args.task, list) else str(args.task)
        plan = ArsenalOptimizer.analyze_and_optimize(task_str)
        print(plan.to_markdown())

    elif args.command == "feedback":
        from .dashboard import record_feedback
        row_id = record_feedback(category=args.cat, rating=args.rating, comment=args.comment)
        print(f"[AegisBrain] Feedback recorded (ID #{row_id}) into neural memory. Thank you!")

    elif args.command == "ceo":
        from .ceo_stress_test import YCCEOStressTester
        idea_str = " ".join(args.idea) if isinstance(args.idea, list) else str(args.idea)
        critique = YCCEOStressTester.evaluate(idea_str)
        print(critique.to_markdown())

    elif args.command == "challenge":
        from .truth_seeking import SkepticalTruthReviewer
        target_str = " ".join(args.target) if isinstance(args.target, list) else str(args.target)
        target = target_str
        p = Path(target)
        if p.exists() and p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
        else:
            text = target
        audit = SkepticalTruthReviewer.audit_proposal_or_code(text)
        print(audit.to_markdown())

    elif args.command == "mistakes":
        from .truth_seeking import MistakeLedger
        ledger = MistakeLedger()
        action = args.mistake_action or "list"
        
        if action == "list":
            entries = ledger.get_all()[:args.limit]
            print(f"=== AegisBrain Mistake Ledger ({len(entries)} recorded) ===")
            for e in entries:
                print(f"[{e.id}] Task: {e.task}")
                print(f"  Mistake: {e.mistake_description}")
                print(f"  Cause:   {e.root_cause}")
                print(f"  Fix:     {e.corrective_action}")
                print(f"  Tags:    {', '.join(e.tags)}\n")

        elif action == "recall":
            matches = ledger.query_mistakes(args.query, limit=5)
            print(f"=== AegisBrain Mistake Recall for '{args.query}' ({len(matches)} matches) ===")
            if not matches:
                print("No matching past mistakes recorded. Proceed with standard caution.")
            for e in matches:
                print(f"⚠️ [{e.id}] {e.task}")
                print(f"   Mistake: {e.mistake_description}")
                print(f"   Fix:     {e.corrective_action}\n")

        elif action == "record":
            entry = ledger.record_mistake(
                task=args.task,
                mistake_description=args.desc,
                root_cause=args.cause,
                corrective_action=args.fix,
                tags=args.tags
            )
            print(f"[AegisBrain] Recorded mistake into ledger (ID: {entry.id}). Agents will avoid this pattern.")

    elif args.command in ("act", "nlp", "do"):
        from .nlp_router import route_and_execute
        query_str = " ".join(args.query) if isinstance(args.query, list) else str(args.query)
        print(route_and_execute(query_str))

    elif args.command in ("sensory", "ingest", "reel"):
        from .sensory import process_sensory_link
        out_dir = Path(args.out) if args.out else None
        print(f"[AegisBrain] Processing sensory ingestion for: {args.url}...")
        res = process_sensory_link(args.url, output_base=out_dir)
        art = res["artifact"]
        analysis = res["analysis"]
        print(f"\n=======================================================")
        print(f"🎬 Sensory Ingestion Summary: {art['platform'].upper()}")
        print(f"=======================================================")
        print(f"📌 Title:       {art.get('title') or 'N/A'}")
        print(f"👤 Author:      {art.get('author') or 'N/A'}")
        print(f"⏱️ Duration:    {art.get('duration_seconds', 0):.1f}s")
        print(f"📁 Manifest:    {res.get('manifest_path')}")
        if art.get('comment_trigger_keyword'):
            print(f"🔑 Gate Trigger:  Comment '{art['comment_trigger_keyword']}' detected -> Auto-bypassed")
        if art.get('gated_resource_urls'):
            print(f"🔗 Retrieved Resources:")
            for r in art['gated_resource_urls'][:3]:
                print(f"   - {r}")
        if art.get('keyframes'):
            print(f"🖼️ Keyframes:   {len(art['keyframes'])} frames extracted")
            for k in art['keyframes'][:3]:
                print(f"   - {k}")
        if art.get('transcript'):
            print(f"\n🎙️ Spoken Transcript:")
            print(f"   {art['transcript']}")
        elif art.get('description'):
            print(f"\n📝 Content Description / Text:")
            print(f"   {art['description'][:500]}...")
            
        if art.get('gated_resource_content'):
            print(f"\n📄 Decoded Resource Payload:")
            print(f"   {art['gated_resource_content'][:600]}...")
            
        cre = res.get("creator")
        if cre:
            print(f"\n🧠 Creator Intelligence Profile:")
            print(f"   Handle:      @{cre['handle']} ({cre['videos_count']} videos tracked)")
            print(f"   Niche:       {cre['niche']}")
            if cre.get('topics'):
                print(f"   Key Themes:  {', '.join(cre['topics'][:5])}")
                
        refs = res.get("cultural_references")
        if refs:
            print(f"\n🎭 Cultural Memes & Tech Lingo Detected ({len(refs)}):")
            for ref in refs:
                print(f"   - '{ref['term']}': {ref['meaning']} ({ref['vibe']})")

        print(f"\n💡 YC Feasibility & Inculcation Delta:")
        yc = analysis.get("yc_ceo_feasibility")
        if yc:
            print(f"   Verdict:     {yc.get('strategic_verdict')} (Score: {yc.get('feasibility_score')}/10, Risk: {yc.get('risk_level')})")
            print(f"   Pain Check:  {yc.get('urgent_pain_assessment')}")
            print(f"   MVP Scope:   {yc.get('smallest_verifiable_mvp')}")

    elif args.command == "radar":
        from .creator_intel import get_all_tracked_creators, radar_sweep, scrape_tech_subreddit
        if args.sub:
            print(f"[AegisBrain] Sweeping r/{args.sub}...")
            items = scrape_tech_subreddit(args.sub, limit=5)
            print(f"\n🔥 Top Discussions in r/{args.sub}:")
            for it in items:
                print(f"  ⬆️ {it['score']:>4} | {it['title']}")
                print(f"     🔗 {it['url']}\n")
        else:
            sweep = radar_sweep()
            print(f"📡 AegisBrain Community & Creator Radar")
            print(f"   Tracked Creators: {sweep['tracked_creators_count']}")
            print(f"   Lexicon Terms:    {sweep['lexicon_terms_indexed']}")
            if sweep.get('recent_creators'):
                print(f"\n👤 Active Tracked Creators:")
                for c in sweep['recent_creators']:
                    print(f"   - @{c['handle']} ({c['platform']}) &bull; {c['videos_count']} videos &bull; Topics: {', '.join(c.get('topics', [])[:4])}")
            if sweep.get('fresh_community_trends'):
                print(f"\n🌐 Hot Ecosystem Discussions:")
                for t in sweep['fresh_community_trends'][:4]:
                    print(f"   - [{t['source']}] {t['title']} (⬆️ {t['score']})")

    elif args.command in ("telegram", "tg"):
        from .telegram_queue import TelegramQueue, set_telegram_token, is_system_idle
        queue = TelegramQueue()
        action = getattr(args, "tg_action", None)
        if action == "setup":
            token_val = "".join(args.token).strip() if isinstance(args.token, list) else str(args.token).strip()
            set_telegram_token(token_val)
            print(f"[AegisBrain] Telegram bot token configured successfully in ~/.aegis/config.json")
        elif action == "poll":
            queued, max_id = queue.poll()
            print(f"[AegisBrain] Telegram Poll Complete: {queued} new items queued (Latest Update ID: {max_id})")
        elif action == "drain":
            force = getattr(args, "force", False)
            limit = getattr(args, "limit", 5)
            thresh = getattr(args, "threshold", 35.0)
            print(f"[AegisBrain] Draining Telegram queue (Idle Only: {not force}, Limit: {limit})...")
            processed = queue.drain(idle_only=not force, max_items=limit, cpu_threshold=thresh)
            if not processed:
                idle, reason = is_system_idle(thresh)
                if not idle and not force:
                    print(f"⏳ System not idle: {reason}. Drain deferred.")
                else:
                    print(f"✨ No pending items in Telegram inbox.")
            else:
                print(f"✅ Successfully processed {len(processed)} queued item(s)!")
        elif action == "listen":
            interval = getattr(args, "interval", 15)
            print(f"🎧 Listening for Telegram messages every {interval}s (drains when system is idle). Press Ctrl+C to stop.")
            try:
                while True:
                    queued, _ = queue.poll()
                    if queued > 0:
                        print(f"📥 Queued {queued} new item(s) from Telegram.")
                    queue.drain(idle_only=True, max_items=3)
                    time.sleep(interval)
            except KeyboardInterrupt:
                print("\nStopped Telegram listener.")
        else:
            st = queue.status()
            idle_indicator = "🟢 Idle" if st['system_idle'] else "🟡 Busy"
            print("🤖 AegisBrain Telegram Mobile Ingestion Queue")
            print(f"   Bot:          {st['bot']}")
            print(f"   System State: {idle_indicator} ({st['idle_reason']})")
            print(f"   Inbox Queue:  {st['pending']} pending | {st['completed']} completed | {st['failed']} failed | {st['total']} total")

    elif args.command == "triage":
        from .severity_triage import judge_task_severity
        decision = judge_task_severity(args.task)
        print(decision.format_banner())

    elif args.command == "hierarchy":
        from .hierarchy import HierarchicalAgentOrchestrator, WorkerType
        orch = HierarchicalAgentOrchestrator()
        task_str = args.task or "General Multi-Agent Operation"
        if getattr(args, "execute", False):
            w_type = WorkerType(args.worker) if args.worker else None
            res = orch.execute_hierarchy(task_str, worker_type=w_type, simulate=args.simulate)
            print(orch.format_hierarchy_report(task_str))
            print("\n🚀 Execution & Coaching Summary:")
            for sub in res["subagent_executions"]:
                print(f"  • {sub['name']} ({sub['domain']}): Passed={sub['passed']}, Attempts={sub['attempts']}, Error Delta={sub['initial_errors']} ➔ {sub['final_errors']}")
                if sub["coaching_history"]:
                    print(f"    Coaching: {sub['coaching_history'][-1]}")
        else:
            orch.plan_hierarchy(task_str)
            print(orch.format_hierarchy_report(task_str))

    elif args.command == "coach":
        from .hierarchy import SubagentNode, WorkerType
        w_type = WorkerType(args.worker)
        sa = SubagentNode(
            subagent_id="subagent-lead",
            name="Antigravity Junior Boss (Domain Lead)",
            domain="core_execution",
            allowed_workers=[w_type],
        )
        print(f"👔 Junior Boss initiating supervised execution with worker `{w_type.value}`...")
        ok, code, info = sa.execute_worker_with_coaching_loop(
            task_spec=args.task,
            worker_type=w_type,
            max_retries=args.retries,
            simulate=args.simulate,
        )
        print(f"🎯 Status: {'PASSED ✅' if ok else 'REVISIONS NEEDED ⚠️'} (Attempts: {info['attempts']}, Initial Errors: {info['initial_errors']} ➔ Final Errors: {info['final_errors']})")
        if info.get("coaching_history"):
            print("\nCoaching Interventions:")
            for c in info["coaching_history"]:
                print(f"  - {c}")
        print(f"\nFinal Verified Output:\n```python\n{code}\n```")

    elif args.command == "armory":
        from .armory import (
            init_armory_db,
            format_armory_status,
            list_armory_skills,
            search_armory,
            get_skill,
            evaluate_skill_security,
            mount_skill,
            unmount_skill,
            queue_skill_for_mining,
            process_miner_queue,
            delete_skill,
        )
        init_armory_db()
        action = getattr(args, "armory_action", "status") or "status"

        if action == "status":
            print(format_armory_status())
        elif action == "list":
            skills = list_armory_skills(category=args.category, status=args.status)
            print(f"=== Aegis Skill Armory ({len(skills)} skills, status={args.status}) ===")
            for s in skills:
                print(f"• {s['name']} [{s['category']}] (Score: {s.get('security_score', 100)}) - {s.get('description', '')}")
        elif action == "search":
            results = search_armory(args.query, limit=args.limit)
            print(f"Found {len(results)} matches for '{args.query}':\n")
            for r in results:
                print(f"• {r['name']} [{r.get('category', 'general')}] (Status: {r.get('status', 'active')})")
                print(f"  {r.get('description', '')}\n")
        elif action == "inspect":
            s = get_skill(args.name)
            if not s:
                print(f"Skill '{args.name}' not found.")
            else:
                print(f"Skill: {s['name']}")
                print(f"Category: {s.get('category')}")
                print(f"Status: {s.get('status')} (Score: {s.get('security_score')})")
                print(f"Path: {s.get('path')}")
                print(f"Description: {s.get('description')}")
        elif action == "scan":
            p = Path(args.path)
            res = evaluate_skill_security(p)
            print(f"Security Scan Report for {p.name}:")
            print(f"  Passed: {res['passed']} (Score: {res['score']}/100)")
            for g, ok in res.get("gates", {}).items():
                print(f"  - Gate {g}: {'PASSED ✅' if ok else 'FAILED ❌'}")
            if res.get("violations"):
                print("  Violations:")
                for v in res["violations"]:
                    print(f"    • {v}")
        elif action == "mount":
            res = mount_skill(args.name, target_agent=args.agent, target_dir=args.dir)
            print(f"Mounted '{args.name}' to {args.agent} (Mode: {res.get('mode', 'link')}): {res.get('target_path', '')}")
        elif action == "unmount":
            try:
                ok = unmount_skill(args.name, target_agent=args.agent, target_dir=args.dir)
                print(f"Unmounted '{args.name}' from {args.agent}: {'SUCCESS' if ok else 'NOT FOUND'}")
            except ValueError as e:
                print(f"PROTECTED INVARIANT: {e}")
        elif action == "mine":
            if args.url:
                qid = queue_skill_for_mining(args.url)
                print(f"Queued URL for mining (Queue ID: {qid}): {args.url}")
            if args.process or not args.url:
                processed = process_miner_queue()
                print(f"Processed {len(processed)} queued item(s) from miner.")
                for item in processed:
                    print(f"  • {item.get('name')}: {item.get('status')} (Queue ID: {item.get('queue_id')})")
        elif action == "delete":
            try:
                ok = delete_skill(args.name)
                print(f"Deleted skill '{args.name}': {'SUCCESS' if ok else 'NOT FOUND'}")
            except ValueError as e:
                print(f"PROTECTED INVARIANT: {e}")
        elif action == "profile":
            from .armory import ARSENAL_ARCHETYPES, apply_archetype_profile, get_active_archetype
            target_profile = getattr(args, "name", None)
            if target_profile:
                res = apply_archetype_profile(target_profile)
                print(f"✅ {res['message']}")
                print(f"Mounted Skills ({len(res['mounted_skills'])}): {', '.join(res['mounted_skills'])}")
            else:
                current = get_active_archetype()
                print("=== Aegis Arsenal Archetype Profile ===")
                print(f"Active Profile: {current.upper()}")
                print("\nAvailable Archetypes:")
                for k, v in ARSENAL_ARCHETYPES.items():
                    active_marker = " [ACTIVE]" if k == current else ""
                    print(f"• {k.capitalize()}{active_marker}: {v['description']}")

    elif args.command in ("unslop", "deslop"):
        from .unslop_master import UnslopMaster

        input_text = ""
        file_path = args.file

        if file_path:
            if not file_path.exists():
                print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
                sys.exit(1)
            input_text = file_path.read_text(encoding="utf-8", errors="replace")
        elif args.text:
            input_text = args.text
        elif not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print("Error: Provide text as argument, --file <path>, or pipe via stdin.", file=sys.stderr)
            sys.exit(1)

        res = UnslopMaster.run(input_text, mode=args.mode, deep=args.deep)

        if args.check:
            print(f"Slop Score: {res.score}/100")
            print(f"Slop Detected: {'YES' if res.slop_detected else 'NO'}")
            if res.findings:
                print("\nFindings:")
                for f in res.findings:
                    p = f.get("pillar", "general")
                    d = f.get("details", "")
                    print(f"  • [{p}] {d}")
            sys.exit(1 if res.slop_detected else 0)

        if file_path and not args.stdout:
            file_path.write_text(res.cleaned_text, encoding="utf-8")
            status = "Cleaned & overwritten" if res.slop_detected else "Already clean"
            print(f"[{status}] {file_path} (Score: {res.score}/100)")
        else:
            print(res.cleaned_text)

    elif args.command == "jev":
        from .jev import JevDecisionEngine
        engine = JevDecisionEngine()
        action = getattr(args, "jev_action", None)

        if action == "decide":
            decision = engine.decide(args.prompt)
            if getattr(args, "json", False):
                import json
                print(json.dumps(decision.to_dict(), indent=2))
            else:
                print(decision.format_banner())
        elif action == "route":
            risk, _ = engine.classify_risk(args.prompt)
            tier, worker, rationale = engine.route_model(args.prompt, risk)
            if getattr(args, "json", False):
                import json
                print(json.dumps({
                    "prompt": args.prompt,
                    "model_tier": tier.value if hasattr(tier, "value") else str(tier),
                    "recommended_worker": worker,
                    "risk_level": risk.value if hasattr(risk, "value") else str(risk),
                    "rationale": rationale,
                }, indent=2))
            else:
                print(f"Model Tier: {tier.value if hasattr(tier, 'value') else str(tier)}")
                print(f"Worker:     {worker}")
                print(f"Risk Level: {risk.value if hasattr(risk, 'value') else str(risk)}")
                print(f"Rationale:  {rationale}")
        elif action == "status" or not action:
            status = engine.get_status()
            if getattr(args, "json", False):
                import json
                print(json.dumps(status, indent=2))
            else:
                print("=== Aegis Jev Semantic Decision Engine Status ===")
                for k, v in status.items():
                    print(f"• {k}: {v}")

    elif args.command == "setup":
        from .environment import run_arsenal_wizard
        prof = getattr(args, "profile", None)
        res = run_arsenal_wizard(profile=prof)
        print(f"\n✅ {res['message']}")
        print(f"Mounted Skills ({len(res['mounted_skills'])}): {', '.join(res['mounted_skills'])}")

    elif args.command in ("doctor", "check", "install"):
        from .environment import run_doctor, format_doctor_report, save_host_capabilities, install_tool, run_arsenal_wizard

        if getattr(args, "setup", False) or getattr(args, "profile", None):
            prof = getattr(args, "profile", None)
            res = run_arsenal_wizard(profile=prof)
            print(f"\n✅ {res['message']}")
            print(f"Mounted Skills ({len(res['mounted_skills'])}): {', '.join(res['mounted_skills'])}")
            return

        target_tool = getattr(args, "tool", None)
        if target_tool:
            print(f"[AegisDoctor] Attempting installation of '{target_tool}'...")
            ok = install_tool(target_tool)
            if ok:
                print(f"✅ Successfully installed '{target_tool}'.")
            else:
                print(f"❌ Failed to install '{target_tool}'. Please verify package name or permissions.")
        else:
            doc_res = run_doctor()
            save_host_capabilities(doc_res)

            if getattr(args, "json", False):
                import json
                print(json.dumps(doc_res, indent=2))
            else:
                show_fix = getattr(args, "fix", False)
                print(format_doctor_report(doc_res, show_fix=show_fix))

                if show_fix:
                    missing = []
                    for tier_key in ("core_essentials", "sensory_accelerators", "token_arbitrage_workers", "workstation_modifiers"):
                        items = doc_res.get(tier_key, {})
                        for t_name, t_info in items.items():
                            if t_info.get("status") in ("MISSING_OPTIONAL", "MISSING_CORE"):
                                missing.append((t_name, t_info.get("install_cmd", "")))

                    if missing:
                        print(f"\n[AegisDoctor --fix] Auto-installing {len(missing)} missing component(s)...")
                        for m_name, m_cmd in missing:
                            print(f"-> Installing {m_name}...")
                            ok = install_tool(m_name)
                            if ok:
                                print(f"   ✅ {m_name} installed successfully.")
                            else:
                                print(f"   ⚠️ {m_name} installation failed or requires manual elevation.")
                    else:
                        print("\n[AegisDoctor --fix] All components are already installed.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
