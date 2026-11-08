# Chapter 06: Worker Cascade & Free Models

This chapter outlines AegisBrain's dynamic Tier 3 worker discovery, the 3-tier execution cascade, automatic free-model tagging, and the strict **Zero-Guesswork** onboarding protocol.

---

## 1. The 3-Tier Execution Cascade

AegisBrain eliminates frontier token expenses by routing implementation tasks through a resilient three-tier worker cascade:

```
                      [ Task Dispatched to Tier 3 ]
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Tier 3A: OpenCode Free Cloud Endpoints                 │
       │ (DeepSeek V4.1 Flash Free / Flint 40B / Big Pickle)    │
       └────────────────────────────┬───────────────────────────┘
                                    │ Failover (Rate-limited, quota, timeout)
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Tier 3B: Nous Hermes Agent Fallback Chain              │
       │ (Nemotron 3.5 Bolt + Multi-Endpoint Cloud Resiliency)  │
       └────────────────────────────┬───────────────────────────┘
                                    │ Failover (Offline, network partition)
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Tier 3C: Local Ollama Execution (Pure Offline)         │
       │ (Qwen2.5-Coder:7b / Llama3.1:8b; 0 Idle VRAM Footprint)│
       └────────────────────────────────────────────────────────┘
```

---

## 2. Dynamic Worker Discovery Engine (`aegis/workers.py`)

AegisBrain inspects workstation CLIs dynamically rather than relying on hardcoded configuration files.

### 2.1 Inspection Routines

1. **`detect_opencode_models()`**:
   - Queries OpenCode configuration files (`~/.config/opencode/` or platform equivalent).
   - Parses the active model registry and custom providers.
2. **`detect_hermes_fallbacks()`**:
   - Invokes `hermes fallback list` or parses `~/.hermes/config.yaml`.
   - Extracts the primary and secondary fallback endpoint chains.
3. **`detect_ollama_local_models()`**:
   - Queries `http://127.0.0.1:11434/api/tags` or runs `ollama list`.
   - Extracts installed local weights (e.g. `qwen2.5-coder:7b`, `deepseek-coder:6.7b`).

### 2.2 Free-Model Auto-Tagging (`is_free_model`)

AegisBrain inspects model identifiers using targeted regex heuristics to classify endpoints that incur $0 cost:

```python
FREE_MODEL_PATTERNS = [
    r"-free$",
    r":free$",
    r"big-pickle",
    r"free-tier",
    r"openrouter/free",
    r"deepseek.*free",
]

def is_free_model(model_name: str) -> bool:
    """Return True if model identifier represents a verified free endpoint."""
    name_lower = model_name.lower()
    return any(re.search(pat, name_lower) for pat in FREE_MODEL_PATTERNS)
```

Free models are prioritized in the execution chain to preserve paid API quotas.

---

## 3. Strict "No-Guesswork" Onboarding Standard

Interactive terminal UIs (such as OpenCode's interactive `/models` selector) do not always persist their active cursor position to non-interactive CLI calls. Inferring or guessing active models can lead to unexpected billing or unauthenticated model errors.

AegisBrain enforces a strict **Zero-Guesswork Standard**:

1. **Explicit Verification**: During `aegis setup --workers` or `aegis doctor --models`, AegisBrain never guesses an unverified model.
2. **Setup Advisory Guide**: For new developers, `aegis workers advice` prints explicit setup recipes for OpenCode, Hermes, and Ollama.
3. **Truthful Evidence Collection**: If automatic discovery cannot deterministically verify active favorites, the user is prompted to enter their preferred models or provide confirmation before saving to `brain.db`.

```bash
# Display the step-by-step free worker setup tutorial
aegis workers advice

# Launch the interactive Worker Discovery & Configuration Wizard
aegis setup --workers

# Inspect configured models and cascade health
aegis workers list
```

---

## 4. Zero-Idle-RAM Ollama Failover

When the cascade falls back to Tier 3C (Local Ollama), VRAM and system memory conservation is essential. 

AegisBrain configures Ollama requests with explicit unload parameters:
- **`keep_alive: "0s"`**: Instructs the Ollama daemon to immediately release GPU VRAM and system RAM upon completion of inference.
- **Zero Background Footprint**: When idle, Ollama consumes 0 MB of GPU memory, allowing developer IDEs, compilation tasks, and browsers to utilize full hardware capacity.
