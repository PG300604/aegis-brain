# Chapter 03: 3-Tier Multi-Agent Power Hierarchy

This chapter describes AegisBrain's **Division of Cognition** — a strict hierarchical division of labor that separates strategic reasoning from raw code synthesis to eliminate frontier token waste and prevent hallucinations.

---

## 1. The Division of Cognition Rationale

In conventional AI workflows, developers task a single frontier model (e.g., Opus 5.5, Gemini 4, or Fable 5.1) with both high-level system architecture and low-level code generation. This creates two failure modes:

1. **Frontier Token Burn**: High-cognition reasoning tokens are wasted generating repetitive boilerplate, serialization routines, and unit tests.
2. **Cognitive Fatigue & Hallucination**: When a model simultaneously manages multi-file dependencies, architectural invariants, and line-by-line syntax, attention is divided, leading to subtle logic inversions and edge-case omissions.

AegisBrain resolves this by establishing three distinct tiers with enforced responsibilities and code invariants:

```
                                  TIER 1: SENIOR BOSS
                       (Fable 5.1 / Opus 5.5 / Gemini 4 / Argon)
               ┌─────────────────────────────────────────────────────────────┐
               │ - System Architecture & Invariants Definition               │
               │ - Options Exploration Matrix (Pros & Cons)                  │
               │ - Final Verification & Executive Sign-off                   │
               │ * INVARIANT: Zero Direct Code (Intervenes ONLY on Escalation)│
               └──────────────────────────────┬──────────────────────────────┘
                                              │ Dispatches scoped directives
                                              ▼
                                 TIER 2: JUNIOR BOSSES
                       (Domain Tech Leads: Backend, Frontend, QA, Sec)
               ┌─────────────────────────────────────────────────────────────┐
               │ - Scoping boundaries & Subagent task allocation             │
               │ - 4-Gate Quality Architecture Auditing                      │
               │ - Error-Reduction Coaching Loops                            │
               │ * INVARIANT: Zero Direct Code (Guides Workers; No Typing)   │
               └──────────────────────────────┬──────────────────────────────┘
                                              │ Commands execution workers
                                              ▼
                                 TIER 3: EXECUTION WORKERS
                       (Hermes CLI / OpenCode Free / Local Ollama MoE)
               ┌─────────────────────────────────────────────────────────────┐
               │ - 100% Raw Code Implementation & File Writes                │
               │ - Boilerplate, Syntax, Unit Tests, and Data Structures      │
               │ - Zero Frontier Token Cost (Free Cloud or Local Hardware)   │
               └─────────────────────────────────────────────────────────────┘
```

---

## 2. Division of Labor & Invariants Matrix

| Tier | Role | Supported Engines | Responsibilities | Direct Code Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Senior Boss** | Supreme Orchestrator & Strategic Brain | Fable 5.1, Opus 5.5, Gemini 4, Argon | Architecture planning, options analysis (Options 1/2/3 with pros/cons), strict invariants definition, test review, error detection, final sign-off. | **Zero Direct Code by default**. Writes implementation code *only* if Tier 2 issues a formal Escalation Dossier. |
| **Tier 2: Junior Bosses** | Domain Tech Leads (Backend, Frontend, Sec, QA) | Subagents spawned via `invoke_subagent` | Scoping task boundaries, dispatching commands to Tier 3 workers, bottom-to-top 4-Gate auditing, coaching error-reduction loops. | **Zero Direct Code**. Formulates coaching prompts; never writes code drafts directly. |
| **Tier 3: Execution Workers** | Code Synthesis Muscle | Hermes CLI, OpenCode Free, Codex CLI, Claude Code CLI, Ollama MoE | Writes all raw code drafts, functions, boilerplate, and implementations using free/local tokens. | **Writes 100% of candidate code**. Subject to iterative coaching loops until 0 errors remain. |

---

## 3. Dynamic Hardware Sizing & Bottleneck Protection

To prevent local execution from freezing the developer's workstation during heavy parallel agent runs, AegisBrain features an automated **Hardware Bottleneck Guard** in `aegis.hardware`.

### 3.1 Host Metrics Monitored
- **Available Physical RAM**: Scanned in real time via OS memory counters.
- **CPU Load Percentage**: Moving 5-second average across logical cores.
- **Thermal Status & Swap Memory Pressure**: Throttles background tasks when swap paging spikes.

### 3.2 Dynamic Concurrency Throttling Rules

```python
# Hardware Guard Invariant in aegis.hardware
if free_ram_gb < 3.5 or cpu_load_pct > 85.0:
    # Throttle to single-worker mode to prevent OS UI freezes
    max_active_subagents = 1
    preferred_tier = ModelTier.CLOUD_FREE  # Offload from local RAM
elif free_ram_gb >= 6.0 and cpu_load_pct <= 60.0:
    # Ample headroom: Scale dynamically to parallel subagents
    max_active_subagents = 4
    preferred_tier = ModelTier.LOCAL_MOE   # Utilize local Ollama
```

### 3.3 Hardware Sizing Tiers

| Tier Name | System Requirements | Concurrency Limit | Default Model Allocations |
| :--- | :--- | :---: | :--- |
| **Tier S (Workstation)** | $\ge 32\text{ GB}$ RAM, 8+ cores | 6 parallel workers | Local Ollama 14B/32B + OpenCode Free |
| **Tier A (Standard PC)** | $16\text{ GB}$ RAM, 4–8 cores | 3 parallel workers | Local Ollama 7B + Hermes Cloud Fallbacks |
| **Tier B (Ultralight / Laptop)** | $8\text{ GB}$ RAM, 2–4 cores | 1 worker | 100% Cloud-Free Workers (0 local RAM footprint) |
| **Tier C (Constrained / VPS)** | $< 8\text{ GB}$ RAM | 1 worker (serialized) | Throttled Cloud-Free Workers |

Check active hardware metrics anytime:
```bash
aegis hardware
```
