# Skill Distillation & Local Model Orchestration 🤖

One of the greatest challenges when using local open-source models (such as `qwen2.5-coder:7b`, `deepseek-coder:14b`, or `llama3:8b` via Ollama) is that they lack the context window and instruction-following capacity to parse hundreds of raw Markdown skills.

AegisBrain solves this by acting as a **distillation proxy**:

---

## 🔄 Proxy Workflow

```
┌─────────────────────┐
│ Hermes / OpenCode / │
│   Coding Agents     │
└──────────┬──────────┘
           │ Request: { messages: [...] }
           ▼
┌───────────────────────────────────────────────┐
│ AegisBrain Proxy (http://127.0.0.1:8765/v1)   │
│                                               │
│ 1. Extract user intent & domain keywords      │
│ 2. Distill relevant skills (<100 tokens)      │
│ 3. Inject ACTIVE_CONTEXT.md (<=400 tokens)    │
└──────────────────────┬────────────────────────┘
                       │ Augmented System Prompt
                       ▼
┌───────────────────────────────────────────────┐
│ Local Ollama Runtime (http://127.0.0.1:11434) │
│ - Executes Qwen / DeepSeek with full context  │
└───────────────────────────────────────────────┘
```

---

## 🛠️ Configuration

Configure your CLI agent (Hermes, OpenCode, Aider, or Continue) to use AegisBrain as its API endpoint:

```ini
API Base URL: http://127.0.0.1:8765/v1
API Key:      aegis-local (or any string)
Model:        qwen2.5-coder:7b
```

### Quality Guardrails Injected
Every request sent through the proxy automatically enforces:
- **Karpathy Simplicity**: Surgical changes, minimal diffs, no speculative abstractions.
- **Security Baseline**: Input validation, parameter checks, zero secret exposure.
- **Framework Standards**: Framework-specific best practices (e.g. low-cardinality OpenTelemetry metrics for Spring AI, strict typing for FastAPI).
