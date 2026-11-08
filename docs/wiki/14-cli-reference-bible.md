# Chapter 14: CLI Reference Bible

This chapter provides an exhaustive, alphabetical dictionary of all commands, subcommands, options, flags, arguments, and exit codes supported by the `aegis` command-line interface.

---

## Exit Codes

All `aegis` commands return standard POSIX-compliant exit codes:
- **`0`**: Operation completed successfully.
- **`1`**: General execution error or quality assertion failure.
- **`2`**: Invalid CLI argument, flag syntax, or missing mandatory parameter.
- **`130`**: Interrupted by user (`SIGINT` / Ctrl+C).

---

## 1. Core Chassis & Service Commands

### `aegis daemon`
Starts the foreground HTTP daemon listener on `127.0.0.1:8765`.
- **Options**:
  - `--port <PORT>`: Bind to custom TCP port (default: `8765`).
  - `--host <HOST>`: Bind interface (default: `127.0.0.1`).
- **Example**: `aegis daemon --port 8765`

### `aegis start`
Spawns the AegisBrain chassis daemon as a detached background process.
- **Example**: `aegis start`

### `aegis stop`
Terminates the running background daemon via PID file lookup.
- **Example**: `aegis stop`

### `aegis status`
Displays live system health: daemon status, database size, memory footprint, active git branch, and session metrics.
- **Options**:
  - `--detailed`: Include low-level thread pools and open file descriptors.
  - `--json`: Output metrics as machine-readable JSON.
- **Example**: `aegis status --detailed`

### `aegis autostart`
Configures zero-elevation operating system startup services (Windows VBS, Linux systemd user service, macOS LaunchAgent).
- **Subcommands**:
  - `on`: Install and enable the autostart service.
  - `off`: Remove and disable the autostart service.
  - `status`: Display active service configuration path and status.
- **Example**: `aegis autostart on`

### `aegis caffeinate`
Manages system sleep prevention and Win32 Away Mode wake-locks.
- **Subcommands**:
  - `enable`: Activate sleep prevention (display turns off, CPU remains active).
  - `disable`: Release wake-locks, returning to OS default power policy.
  - `status`: Check if wake-lock pulse thread is running.
- **Options**:
  - `--keep-display`: Prevent the monitor display from turning off.
- **Example**: `aegis caffeinate enable --keep-display`

### `aegis lock`
Immediately locks the desktop workstation via native Win32 `LockWorkStation()`. Background agent processes and test runners continue executing unaffected.
- **Example**: `aegis lock`

### `aegis doctor`
Performs an exhaustive audit of workstation software tools, python modules, network sockets, worker CLIs, and memory databases.
- **Options**:
  - `--fix`: Automatically resolve detected configuration errors and directory permissions.
  - `--models`: Run deep inspection on configured Tier 3 worker endpoints.
- **Example**: `aegis doctor --fix`

---

## 2. Memory & Context Commands

### `aegis recall`
Sub-50ms full-text search across decisions, conventions, and past milestones.
- **Arguments**:
  - `[query]`: Search terms (leave blank to view recent memories).
- **Options**:
  - `--limit <N>`: Maximum records returned (default: `5`).
  - `--category <CAT>`: Filter by category (`architecture`, `security`, `frontend`, etc.).
- **Example**: `aegis recall "argon2 password hashing" --limit 3`

### `aegis remember`
Records an architectural decision, rule, or milestone into SQLite WAL with auto-sync FTS5 indexing.
- **Arguments**:
  - `<text>`: Decision summary text.
- **Options**:
  - `--category <CAT>`: Categorization tag (default: `architecture`).
  - `--rationale <TEXT>`: Engineering justification and context.
- **Example**: `aegis remember "Always use Radix UI primitive Dialog" --category frontend`

### `aegis bootstrap`
Synthesizes current Git branch, uncommitted diffs, tracked PRs, and active decisions into a deterministic summary ($\le 400$ tokens).
- **Options**:
  - `--json`: Return structured JSON instead of formatted markdown.
- **Example**: `aegis bootstrap`

### `aegis stealth`
Toggles zero-disk private stealth mode for confidential or NDA repositories.
- **Arguments**:
  - `on`: Activate volatile in-memory storage (zero writes to `brain.db`).
  - `off`: Deactivate stealth mode and resume standard persistent logging.
- **Example**: `aegis stealth on`

### `aegis snapshot`
Creates an instant restore point of agent configurations, prompt templates, and local rules before major alterations.
- **Subcommands**:
  - `create [--reason <R>]`: Capture state snapshot.
  - `list`: Display historical snapshots.
  - `restore <ID>`: Roll back configuration to a designated snapshot ID.
- **Example**: `aegis snapshot create --reason "pre-refactor"`

---

## 3. Multi-Agent & Orchestration Commands

### `aegis hierarchy`
Inspects the 3-Tier Multi-Agent Power Hierarchy, active roles, and token arbitrage statistics.
- **Subcommands**:
  - `set-boss <NAME>`: Configure default Tier 1 Boss (`opencode`, `codex`, `antigravity`, `claude`).
  - `get-boss`: View current default Boss and model checkpoint.
- **Options**:
  - `--model <M>`: Model identifier (e.g. `gpt-6-astra`, `gemini-3.8-flash`).
- **Example**: `aegis hierarchy set-boss opencode --model gpt-6-astra`

### `aegis dispatch`
Universal Agent Dispatch: Routes tasks across arbitrary Boss-Worker tool pairings using the standardized `UniversalAgentEnvelope`.
- **Arguments**:
  - `<task>`: Description of the engineering task.
- **Options**:
  - `--boss <NAME>`: Tier 1 supervisory engine (`antigravity`, `opencode`, `claude`, `codex`).
  - `--worker <NAME>`: Tier 3 execution muscle (`hermes`, `opencode`, `codex`, `ollama`).
  - `--worker-model <M>`: Execution model checkpoint.
  - `--simulate`: Dry-run simulation without file mutation.
  - `--json`: Output serialized `UniversalAgentEnvelope` JSON.
- **Example**: `aegis dispatch "Implement JWT verification" --boss opencode --worker hermes`

### `aegis coach`
Runs a Subagent coaching cycle on an execution worker, auditing draft code through the 4 Quality Gates and guiding error reduction.
- **Arguments**:
  - `<target_file>`: File containing candidate worker code.
- **Options**:
  - `--retries <N>`: Maximum coaching iterations before escalation (default: `3`).
- **Example**: `aegis coach candidate_auth.py --retries 3`

### `aegis triage`
Evaluates task complexity and recommends the optimal multi-agent execution strategy based on current workstation hardware headroom.
- **Arguments**:
  - `<task_description>`: Description of the proposed feature or fix.
- **Example**: `aegis triage "Refactor entire database schema to PostgreSQL"`

---

## 4. Worker Management & Discovery

### `aegis workers`
Manages Tier 3 execution workers, free model detection, and fallback cascades.
- **Subcommands**:
  - `list`: Display configured worker models and priority cascade.
  - `advice`: Print step-by-step tutorial on configuring free cloud and local models.
  - `setup`: Launch guided interactive discovery wizard.
  - `clear`: Reset worker model configuration.
- **Example**: `aegis workers list`

---

## 5. UI Testing & Fast-Path Verification

### `aegis hands` (aliases: `ui`, `test-ui`)
Native headless web inspection, DOM extraction, and console error trapping.
- **Arguments**:
  - `<url>`: Target URL (e.g. `http://localhost:3000`).
- **Options**:
  - `--screenshot`: Capture full-page screenshot into `~/.aegis-brain/screenshots/`.
  - `--assert-clean`: Exit with non-zero code on HTTP $\ge 400$ or console errors.
  - `--json`: Output element tree as JSON.
- **Example**: `aegis hands http://localhost:3000 --assert-clean`

### `aegis test`
Fast-path in-memory AST syntax validation and scoped pytest execution in $< 1\text{ second}$.
- **Arguments**:
  - `<file>`: Source or test file to verify.
- **Options**:
  - `--scoped`: Run only the test file strictly matching the source module.
  - `--json`: Return structured pass/fail telemetry JSON.
- **Example**: `aegis test package/aegis/workers.py`

---

## 6. Mobile Remote & Bridge Commands

### `aegis remote`
Manages the 24/7 background mobile remote listener.
- **Subcommands**:
  - `start`: Launch background mobile listener thread.
  - `status`: View active mobile pairing state and PIN authorization.
- **Options**:
  - `--service <S>`: Remote service (`telegram` or `whatsapp`).
- **Example**: `aegis remote start --service telegram`

### `aegis type`
Injects text directly into the active console window via Win32 `WriteConsoleInputW()` and submits.
- **Arguments**:
  - `<text>`: Text string or command to type into the active console.
- **Example**: `aegis type "git status"`

---

## 7. Quality Architecture & Security

### `aegis pipeline`
Executes the 4-Decision Quality Architecture Gate on candidate source code.
- **Arguments**:
  - `<target_file>`: Path to code file.
- **Options**:
  - `--fix`: Automatically strip conversational AI preambles and slop.
- **Example**: `aegis pipeline candidate.py --fix`

### `aegis challenge`
Executes an adversarial red-team security audit, flagging command injections, `shell=True`, and path traversals.
- **Arguments**:
  - `<file_or_code>`: Target file or code snippet.
- **Example**: `aegis challenge scripts/install.sh`

### `aegis unslop` (alias: `deslop`)
Strips conversational AI watermarks, markdown fences, and pleasantries from files or standard input.
- **Arguments**:
  - `<file>`: File to clean.
- **Example**: `aegis unslop documentation_draft.md`

---

## 8. Session Lifecycle & Briefings

### `aegis briefing` (aliases: `hi`, `greeting`)
Generates an anti-slop developer briefing: offline PR activity, completed milestones, HackerNews/LocalLLaMA tech radar, and today's top priorities.
- **Example**: `aegis briefing`

### `aegis bye` (aliases: `close-session`, `session-end`)
Executes graceful session termination: creates a restore-point snapshot, compiles working context to `ACTIVE_CONTEXT.md`, and archives session metrics into `brain.db`.
- **Options**:
  - `--summary <TEXT>`: Executive summary of accomplishments.
- **Example**: `aegis bye --summary "Completed 3-Tier Multi-Agent Arch Wiki"`
