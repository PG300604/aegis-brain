# AegisBrain Wiki Portal

Technical documentation for the AegisBrain autonomous engineering chassis, neural memory bus, and 3-tier multi-agent governor.

This wiki provides reference specifications, system internals, protocols, configuration formats, and troubleshooting procedures.

---

## Master Table of Contents

| Chapter | Title | Summary |
| :---: | :--- | :--- |
| **[01](01-architecture-internals.md)** | **[Architecture & Internals](01-architecture-internals.md)** | Chassis daemon on `:8765`, SQLite WAL memory bus, FTS5 virtual tables, and AST graph tokens. |
| **[02](02-installation-and-shell-hooks.md)** | **[Installation & Shell Hooks](02-installation-and-shell-hooks.md)** | Universal installation, shell hooks (PowerShell, Bash, Zsh, Fish), and zero-elevation autostart services. |
| **[03](03-3-tier-multi-agent-power-hierarchy.md)** | **[3-Tier Multi-Agent Power Hierarchy](03-3-tier-multi-agent-power-hierarchy.md)** | Division of Cognition: Tier 1 Senior Boss, Tier 2 Junior Bosses, Tier 3 Workers, and dynamic hardware sizing. |
| **[04](04-senior-boss-escalation-and-coaching.md)** | **[Senior Boss Escalation & Coaching](04-senior-boss-escalation-and-coaching.md)** | Supervision rationale, Subagent coaching loops, Escalation Dossiers, and Senior Boss Takeover. |
| **[05](05-universal-agent-interchangeability.md)** | **[Universal Agent Interchangeability](05-universal-agent-interchangeability.md)** | Tool-agnostic orchestration: OpenCode, Codex, Antigravity, Claude Code, and the `UniversalAgentEnvelope` schema. |
| **[06](06-worker-cascade-and-free-models.md)** | **[Worker Cascade & Free Models](06-worker-cascade-and-free-models.md)** | Dynamic worker discovery (`opencode models`, `hermes fallback list`), free model tagging, and Ollama failover. |
| **[07](07-hands-engine-and-ui-testing.md)** | **[Hands Engine & UI Testing](07-hands-engine-and-ui-testing.md)** | Headless web inspection, DOM extraction, console error trapping, Playwright UI journey runner, and stdlib fallback. |
| **[08](08-neural-memory-and-context-governor.md)** | **[Neural Memory & Context Governor](08-neural-memory-and-context-governor.md)** | Sub-50ms FTS5 memory recall (`aegis recall`), deterministic $\le 400$-token context snapshots, and stealth mode. |
| **[09](09-mobile-remote-and-whisper-bridge.md)** | **[Mobile Remote & Whisper Bridge](09-mobile-remote-and-whisper-bridge.md)** | 24/7 Mobile Operations: Telegram (`@HHAACLIBot`) & WhatsApp, local Whisper audio transcription, and console injection. |
| **[10](10-power-management-caffeinate.md)** | **[Power Management & Caffeinate](10-power-management-caffeinate.md)** | System sleep prevention: Win32 `SetThreadExecutionState` continuous pulse thread, macOS `caffeinate`, and `systemd-inhibit`. |
| **[11](11-role-based-dynamic-arsenal.md)** | **[Role-Based Dynamic Arsenal](11-role-based-dynamic-arsenal.md)** | Archetype profiles (`developer`, `creator`, `security`, `omni`), JIT skill expansion, and Jev Decision Head. |
| **[12](12-4-decision-quality-architecture-gate.md)** | **[4-Decision Quality Architecture Gate](12-4-decision-quality-architecture-gate.md)** | Karpathy Simplicity Doctrine, Ponytail/Unslop AI watermark stripping, Red-Team audit, and Dual-Environment sandbox. |
| **[13](13-fast-path-testing-and-ast.md)** | **[Fast-Path Testing & AST Verification](13-fast-path-testing-and-ast.md)** | In-memory AST verification (`aegis test <file>`), scoped pytest execution (< 1s), and CI parity maintenance. |
| **[14](14-cli-reference-bible.md)** | **[CLI Reference Bible](14-cli-reference-bible.md)** | Exhaustive dictionary of all 58+ commands, subcommands, arguments, flags, options, and exit codes. |
| **[15](15-troubleshooting-and-diagnostics.md)** | **[Troubleshooting & Diagnostics](15-troubleshooting-and-diagnostics.md)** | System troubleshooting table: error messages, root causes, diagnostic recipes (`aegis doctor`), and recoveries. |

---

## Reading Paths by Engineering Persona

Depending on your integration objective, consult the following curated sequences:

### 1. System Architect & Multi-Agent Lead
Focus on cognitive division, token arbitrage, and cross-model orchestration:
1. [01. Architecture & Internals](01-architecture-internals.md)
2. [03. 3-Tier Multi-Agent Power Hierarchy](03-3-tier-multi-agent-power-hierarchy.md)
3. [04. Senior Boss Escalation & Coaching](04-senior-boss-escalation-and-coaching.md)
4. [05. Universal Agent Interchangeability](05-universal-agent-interchangeability.md)
5. [12. 4-Decision Quality Architecture Gate](12-4-decision-quality-architecture-gate.md)

### 2. DevOps & SRE Engineer
Focus on daemon stability, background service setup, power states, and diagnostics:
1. [01. Architecture & Internals](01-architecture-internals.md)
2. [02. Installation & Shell Hooks](02-installation-and-shell-hooks.md)
3. [10. Power Management & Caffeinate](10-power-management-caffeinate.md)
4. [13. Fast-Path Testing & AST Verification](13-fast-path-testing-and-ast.md)
5. [15. Troubleshooting & Diagnostics](15-troubleshooting-and-diagnostics.md)

### 3. Full-Stack & UI/Frontend Developer
Focus on automated DOM testing, fast verification, and token savings:
1. [06. Worker Cascade & Free Models](06-worker-cascade-and-free-models.md)
2. [07. Hands Engine & UI Testing](07-hands-engine-and-ui-testing.md)
3. [08. Neural Memory & Context Governor](08-neural-memory-and-context-governor.md)
4. [13. Fast-Path Testing & AST Verification](13-fast-path-testing-and-ast.md)

### 4. Remote & Mobile Operator
Focus on smartphone steering, local speech-to-text, and console injection:
1. [09. Mobile Remote & Whisper Bridge](09-mobile-remote-and-whisper-bridge.md)
2. [10. Power Management & Caffeinate](10-power-management-caffeinate.md)
3. [14. CLI Reference Bible](14-cli-reference-bible.md)
