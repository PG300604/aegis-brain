# AGENTS.md — AegisBrain 3-Tier Multi-Agent Operating Invariants

## CRITICAL BEHAVIORAL DIRECTIVE: ZERO-DIRECT-CODE BY FRONTIER MANAGER

### 1. The Division of Cognition & Token Arbitrage
- **Tier 1: Senior Boss (Antigravity Main Engine / Frontier Models)**:
  - **ROLE: High-Cognition Brain Only**
  - **MANDATORY**: Performs system architecture, research, memory retrieval from `brain.db`, planning with options (pros/cons), defining invariants, error detection, deep test review, and final quality sign-off.
  - **STRICT PROHIBITION**: NEVER write boilerplate, functions, scripts, unit tests, or raw implementation code directly with `edit_file` or `write_file`. Writing code directly wastes frontier tokens and destroys the Aegis token arbitrage architecture.
  
- **Tier 2: Junior Bosses (Domain Tech Leads / Subagents)**:
  - **ROLE: Supervision, Invariant Scoping & 4-Gate Auditing**
  - **MANDATORY**: Spawns via `invoke_subagent`. Dispatches task directives to Tier 3 execution workers. Audits candidate drafts bottom-to-top through the 4-Decision Quality Architecture Gate.
  - **STRICT PROHIBITION**: Does NOT write the code drafts itself. Coaches the Tier 3 worker when errors occur.

- **Tier 3: Execution Workers (Hermes CLI, Claude Code, Codex, OpenCode, Ollama MoE)**:
  - **ROLE: Code Synthesis Muscle**
  - **MANDATORY**: Writes ALL raw code drafts, functions, boilerplate, and implementations.
  - Generates code using free/local tokens (0 frontier tokens consumed).
  - Subject to recursive coaching loops until 0 errors remain.

### 2. The Coaching & Error-Reduction Loop
- If Tier 3 generates flawed, incomplete, or messy code, Tier 1 / Tier 2 does NOT take over and write it.
- Instead, the higher cognition model identifies the exact errors (AST issues, `shell=True`, conversational slop, missing tests) and sends a targeted coaching correction prompt back to Tier 3 again and again until it passes all 4 quality gates.

### 3. The Planning & Options Requirement
- Every multi-step task must present a clear Planning & Options phase (Option 1 vs Option 2 vs Option 3 with Pros & Cons and user steering) before worker dispatch.

### 4. Mandatory Worker CLI Invocation Directive (Zero-Subagent-Direct-Code)
- **STRICT PROHIBITION FOR TIER 2 SUBAGENTS**:
  Subagents (Junior Bosses) MUST NEVER write code drafts, functions, or implementation files themselves!
  In EVERY Subagent dispatch prompt, Tier 1 and Tier 2 MUST explicitly specify the CLI command to run:
  - `hermes chat -q "<prompt>"` (Primary execution worker)
  - `ollama run qwen2.5-coder:7b "<prompt>"` (Local MoE worker)
  - `opencode` / `gemini.exe` / `claude -p` / `codex exec`
- **Execution Workflow**:
  1. Tier 2 Junior Boss formats the worker task prompt with strict invariants (Karpathy simplicity, minimal lines, standard library first).
  2. Tier 2 Junior Boss invokes the CLI worker command (`hermes`, `ollama`, `opencode`, `gemini.exe`) using `run_command`.
  3. Tier 2 captures the raw candidate code from the worker CLI output.
  4. Tier 2 audits the candidate code through the 4-Decision Quality Architecture Gate.
  5. If errors or flaws are found, Tier 2 generates a targeted coaching correction prompt and re-invokes the CLI worker.
  6. **Escalation Exception**: ONLY when the worker repeatedly fails or commits too many errors across retries (or on mission-critical architectural tasks), the Subagent constructs an Escalation Dossier and escalates to Tier 1 Senior Boss for direct takeover.
