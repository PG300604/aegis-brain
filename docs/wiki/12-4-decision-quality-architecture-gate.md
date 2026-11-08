# Chapter 12: 4-Decision Quality Architecture Gate

This chapter specifies AegisBrain's **4-Decision Quality Architecture Gate** (`aegis.pipeline`) — the automated pre-delivery audit pipeline that all candidate code must pass before reaching the user or Git repository.

---

## 1. The Quality Gate Rationale

When execution workers (whether Tier 3 free cloud models or local Ollama instances) generate code drafts, they often introduce conversational noise, speculative abstractions, or security anti-patterns. 

AegisBrain interposes a multi-stage deterministic gate that evaluates, sanitizes, and verifies candidate code:

```
                      [ Candidate Code from Worker ]
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Gate 1: Karpathy Simplicity Doctrine                   │
       │ - Surgical, minimal lines of code                      │
       │ - Zero speculative abstractions or unused wrappers     │
       │ - Rewrites 200 lines into 50 if overengineered         │
       └────────────────────────────┬───────────────────────────┘
                                    │ Passed
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Gate 2: Ponytail / Unslop / TurnItOut                  │
       │ - Strips conversational preambles ("Certainly!", etc.) │
       │ - Eliminates conversational markdown explanations      │
       │ - Guarantees clean, human-grade raw code output        │
       └────────────────────────────┬───────────────────────────┘
                                    │ Passed
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Gate 3: Red-Team Security & Cloudflare Audit           │
       │ - Blocks `shell=True`, `os.system()`, dynamic `eval`   │
       │ - AST inspection for path traversals (../)             │
       │ - Secret Scanner: blocks API keys, tokens, passwords   │
       └────────────────────────────┬───────────────────────────┘
                                    │ Passed
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Gate 4: Dual-Environment Verification                  │
       │ - In-memory AST syntax validation                      │
       │ - Sandboxed compilation check                          │
       │ - Host workspace verification & scoped pytest          │
       └────────────────────────────┬───────────────────────────┘
                                    │ Passed
                                    ▼
                    [ Executive Sign-Off & Delivery ]
```

---

## 2. Gate Specifications

### Gate 1: Karpathy Simplicity Doctrine
Inspired by Andrej Karpathy's software engineering doctrine:
- **Zero Speculative Generalization**: No abstractions, interfaces, or classes designed for "future flexibility" that was not explicitly requested.
- **Surgical Changes**: Modifications touch only the exact functions or lines required. Adjacent formatting or working code is preserved untouched.
- **Complexity Cuts**: If a candidate implementation produces 200 lines for a task solvable in 50 lines using the standard library, it is rejected and simplified.

### Gate 2: Ponytail / Unslop / TurnItOut (`aegis/unslop_master.py`)
Removes all conversational AI artifacts:
- Purges polite conversational headers ("Here is the complete solution:", "Sure, I can help with that:").
- Eliminates conversational sign-offs ("Let me know if you need anything else!").
- Strips malformed markdown code fences when the output format requires a pure, raw script.
- Generates clean, idiomatic code indistinguishable from an experienced human engineer's work.

### Gate 3: Red-Team Security & Cloudflare Audit (`aegis/challenge.py`)
Enforces perimeter security through AST and pattern inspection:
- **Command Injection Prevention**: Detects and rejects `subprocess.Popen(..., shell=True)` and `os.system(...)`.
- **Dangerous Builtins**: Blocks unauthorized `eval()`, `exec()`, or `__import__` operations.
- **Path Traversal Guard**: Flags unvalidated file paths containing `../` or arbitrary system paths (`/etc/`, `C:\Windows\System32\`).
- **Secret Scanner**: Runs regex patterns against candidate strings to prevent committing private API keys (`AKIA...`, `sk-...`, `ghp_...`).

### Gate 4: Dual-Environment Verification
Guarantees syntax and execution safety before filesystem modification:
1. **In-Memory AST Parsing**: Source code is parsed via Python's native `ast.parse()`. If syntax errors or invalid indentation exist, the file is never written to disk.
2. **Sandbox Compilation**: The module is dry-run compiled in an isolated temporary buffer.
3. **Scoped Verification**: Targeted scoped tests are executed via `aegis.workers.run_fast_test()`, verifying functionality in $< 1\text{ second}$.

---

## 3. CLI Usage

Run any file or candidate draft through the Quality Gate:

```bash
# Audit a file through all 4 gates
aegis pipeline package/aegis/server.py

# Audit and automatically strip conversational AI slop
aegis pipeline candidate_output.py --fix

# Run red-team challenge audit on a file
aegis challenge scripts/deploy.py

# Run standalone unslop sanitizer on code or markdown
aegis unslop documentation_draft.md
```
