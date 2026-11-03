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

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
