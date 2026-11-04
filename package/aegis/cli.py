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

    # plan (Matt Pocock Suggestion Panel)
    plan_parser = subparsers.add_parser("plan", help="Generate an interactive Suggestion Panel with trade-offs and options")
    plan_parser.add_argument("task", help="Task or decision to analyze")

    # orchestrate (Manager-Worker Pipeline & Token Arbitrage)
    orch_parser = subparsers.add_parser("orchestrate", help="Run Manager-Worker task execution and record distillation trajectory")
    orch_parser.add_argument("task", nargs="?", default="", help="Task prompt to execute")
    orch_parser.add_argument("--simulate", "-s", action="store_true", help="Simulate worker draft for quick testing")
    orch_parser.add_argument("--stats", action="store_true", help="View cumulative tokens saved and distillation history")

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
        suggs = create_default_suggestions_for_task(args.task)
        panel = format_suggestion_panel(args.task, suggs, recommended_index=0)
        print(panel)

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

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
