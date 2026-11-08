# Chapter 11: Role-Based Dynamic Arsenal

This chapter specifies AegisBrain's role-based dynamic arsenal architecture (`aegis.armory`), archetype profiles, the Armory database (`armory.db`), and Just-In-Time (JIT) skill expansion via the Jev Semantic Decision Head.

---

## 1. The Tool Bloat vs. Lean Footprint Dilemma

Modern coding agent harnesses frequently suffer from **Tool Saturation**: installing dozens of MCP tools, plugins, and custom prompt templates upfront creates significant issues:
1. **Context Window Inflation**: Injecting hundreds of tool schemas consumes 30% to 50% of the agent's context window before any code is read.
2. **Tool Routing Ambiguity**: Large language models exhibit degraded routing accuracy when presented with 50+ overlapping tools.
3. **Workstation Overhead**: Running multiple background MCP server processes consumes hundreds of megabytes of RAM.

AegisBrain resolves this through **Targeted Archetype Profiles** combined with **Just-In-Time (JIT) Dynamic Mounting**.

---

## 2. Archetype Profiles

Developers initialize their workstation using lean, domain-specific archetypes configured in `aegis.armory`:

```
                           [ Developer Workstation ]
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        ┌───────────────────────┐             ┌───────────────────────┐
        │   DEVELOPER PROFILE   │             │    CREATOR PROFILE    │
        │ - AST Code Graph      │             │ - Local Whisper STT   │
        │ - Git Sweep & PRs     │             │ - FFmpeg Video Slicing│
        │ - Scoped Pytest       │             │ - UI-UX Pro Max Engine│
        │ - Worker Token Cascade│             │ - OpenMontage Studio  │
        └───────────────────────┘             └───────────────────────┘
                    ▲                                     ▲
                    │                                     │
        ┌───────────┴───────────┐             ┌───────────┴───────────┐
        │   SECURITY PROFILE    │             │      OMNI PROFILE     │
        │ - Artemis Vuln Audit  │             │ - All Archetypes      │
        │ - Secret Regex Guard  │             │   Simultaneously      │
        │ - DAST / AST Checker  │             │   Mounted for Power   │
        │ - Sandboxed Execution │             │   Workstations        │
        └───────────────────────┘             └───────────────────────┘
```

### 2.1 Profile Breakdown

| Profile | Target Persona | Key Mounted Modules | RAM Footprint |
| :--- | :--- | :--- | :---: |
| **`developer`** | Backend, Systems, & Core Engineers | `code_graph`, `fast_test`, `workers`, `git_sweep` | $< 20\text{ MB}$ |
| **`creator`** | Frontend, Design, & Media Creators | `hands`, `whisper`, `ui_ux_promax`, `media_bridge` | $< 35\text{ MB}$ |
| **`security`** | Red-Team, AppSec, & Auditing | `truth_seeking`, `challenge`, `secret_scanner`, `sandbox` | $< 22\text{ MB}$ |
| **`omni`** | High-Spec Workstations & Leads | All modules and tools active | $< 45\text{ MB}$ |

Mount an archetype directly:
```bash
aegis setup --profile developer
```

---

## 3. The Armory Database (`~/.aegis-brain/armory.db`)

All skills, tool definitions, and companion prompts are indexed in `armory.db` using SQLite FTS5:

### 3.1 Security Verification Gate (`evaluate_skill_security`)
Before any imported skill or tool is mounted into an agent's active profile, AegisBrain executes an automated security audit:
- Checks for unvalidated `eval()`, `exec()`, or dynamic code compilation.
- Scans for dangerous shell executions (`os.system`, `subprocess(shell=True)`).
- Detects unauthorized outbound socket calls or credential exfiltration attempts.

Skills failing the security gate are quarantined and prevented from mounting.

### 3.2 Cross-Agent Skill Projection
Once a skill is mounted in AegisBrain, it is projected across all installed agent environments automatically:
- Antigravity companion skills (`~/.gemini/config/skills/`)
- Claude Code skill directories (`~/.claude/skills/`)
- OpenCode custom tools (`~/.config/opencode/tools/`)

---

## 4. JIT Skill Expansion via Jev Decision Head (`aegis jev`)

What happens if a developer running the lean `developer` profile suddenly receives a multimedia video task or security audit prompt?

The **Jev Semantic Decision Head** (`aegis.jev`) evaluates incoming user prompts in sub-100ms:
1. **Classification**: Identifies required capability domain (e.g. `video`, `security`, `frontend`).
2. **Gap Detection**: Detects if the needed tool is currently unmounted.
3. **JIT Mounting**: Dynamically mounts the required skill from `armory.db` for the duration of the task.
4. **Transient Cleanup**: Automatically unmounts the tool after task completion, preserving the lean baseline footprint.

```bash
# Analyze a prompt and inspect recommended JIT skill expansions
aegis optimize "Extract audio from MP4 and transcribe with Whisper"

# Query the Jev Decision Engine directly
aegis jev "Audit this codebase for hardcoded secrets"
```
