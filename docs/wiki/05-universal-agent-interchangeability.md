# Chapter 05: Universal Agent Interchangeability

This chapter specifies AegisBrain's tool-agnostic protocol, enabling arbitrary combinations of AI coding tools to collaborate seamlessly via the standardized `UniversalAgentEnvelope`.

---

## 1. Tool-Agnostic Design Rationale

The AI developer ecosystem is highly fragmented:
- **Anthropic Claude Code**: High cognitive synthesis and reasoning.
- **OpenAI Codex CLI**: Fast code edits and script execution.
- **Google Antigravity CLI**: Complex multi-turn workflows and agent coordination.
- **Nous Research Hermes**: Fast local and cloud-based reasoning agents.
- **OpenCode CLI**: Flexible terminal-native coding agent supporting diverse cloud models.

Historically, each tool operates in an isolated silo with proprietary prompt formats and incompatible session logs. AegisBrain abstracts these tools into interchangeable components of a single unified pipeline:

```
               ┌────────────────────────────────────────────────────────┐
               │              CONFIGURABLE TIER 1 BOSS                  │
               │   OpenCode (GPT-6 Astra) | Claude Code | Antigravity   │
               └───────────────────────────┬────────────────────────────┘
                                           │ Dispatches Universal Envelope
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │              CONFIGURABLE TIER 3 WORKER                │
               │   Codex CLI | Hermes Agent | Local Ollama MoE | Aider  │
               └────────────────────────────────────────────────────────┘
```

---

## 2. Supported Boss-Worker Pairings

Any supported tool can be designated as the high-cognition **Tier 1 Boss** or the fast **Tier 3 Execution Worker**:

| Boss Engine | Worker Engine | Invocation Example |
| :--- | :--- | :--- |
| **OpenCode** | **Codex** | `aegis dispatch "Build API gateway" --boss opencode --worker codex` |
| **Codex** | **OpenCode Free** | `aegis dispatch "Add user migrations" --boss codex --worker opencode --worker-model deepseek-v4.1-flash-free` |
| **Antigravity** | **Hermes** | `aegis dispatch "Refactor auth middleware" --boss antigravity --worker hermes` |
| **Claude Code** | **Ollama MoE** | `aegis dispatch "Implement unit tests" --boss claude --worker ollama --worker-model qwen2.5-coder:7b` |

---

## 3. The `UniversalAgentEnvelope` Schema

Regardless of which tool initiates or executes a task, all communication is normalized through the `UniversalAgentEnvelope` dataclass defined in `aegis.agent_adapters`:

```python
@dataclass
class UniversalAgentEnvelope:
    task: str
    boss_name: str
    boss_model: Optional[str] = None
    worker_name: str = "hermes"
    worker_model: Optional[str] = None
    execution_response: AgentExecutionResponse = field(
        default_factory=lambda: AgentExecutionResponse(worker_name="unknown")
    )
    quality_gate_passed: bool = True
    gate_scores: Dict[str, bool] = field(
        default_factory=lambda: {
            "karpathy_simplicity": True,
            "unslop_turnitout": True,
            "security_redteam": True,
            "dual_env_verification": True,
        }
    )
    executive_deliverable: str = ""
    tokens_saved: int = 0
    status: str = "completed"
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### 3.1 Field Definitions

- `task`: The natural-language or structured objective assigned to the pipeline.
- `boss_name`: Identifier of the Tier 1 supervisory engine (`antigravity`, `opencode`, `claude`, `codex`).
- `boss_model`: The specific model checkpoint used by Tier 1 (e.g., `gemini-3.8-flash`, `gpt-6-astra`).
- `worker_name`: Identifier of the Tier 3 muscle tool (`hermes`, `opencode`, `codex`, `ollama`).
- `worker_model`: Specific checkpoint executing raw synthesis (e.g., `qwen2.5-coder:7b`, `deepseek-v4.1-flash-free`).
- `gate_scores`: Boolean scorecard for each of the 4 Quality Architecture Gates.
- `executive_deliverable`: Final signed and verified code output or implementation plan.
- `tokens_saved`: Calculated token volume offloaded from frontier models to free/local workers.

---

## 4. Configuration & Dispatch CLI

### 4.1 Setting the Default Boss
Developers can configure their workstation's default Tier 1 Boss:

```bash
# Set default Boss to OpenCode with GPT-6 Astra
aegis hierarchy set-boss opencode --model gpt-6-astra

# Inspect currently active Boss configuration
aegis hierarchy get-boss
```

### 4.2 Executing Universal Task Dispatch
Dispatch tasks across arbitrary pairings:

```bash
# Execute real dispatch
aegis dispatch "Implement JWT token validation" --boss opencode --worker hermes

# Dry-run simulation returning structured JSON envelope
aegis dispatch "Audit database connection pooling" --boss claude --worker codex --simulate --json
```
