# Chapter 13: Fast-Path Testing & AST Verification

This chapter describes AegisBrain's Fast-Path testing architecture (`aegis test`), in-memory Abstract Syntax Tree (AST) validation, scoped test discovery, and CI/CD parity maintenance.

---

## 1. The Full-Suite Latency Problem

In enterprise repositories and mature codebases, executing the full test suite across hundreds of test cases takes between 30 and 120 seconds. 

When developers or autonomous agents run the entire test suite on every minor change:
- Iteration loops stall, slowing agent velocity.
- Machine resources spike, causing CPU thermal throttling.
- Token context windows are flooded with hundreds of lines of irrelevant test output.

AegisBrain resolves this with **Fast-Path Verification**, reducing validation latency from minutes to **$< 1\text{ second}$**.

---

## 2. In-Memory AST Validation Engine

Before launching any external test process, `aegis.workers.run_fast_test()` parses the target file directly in memory using Python's native `ast` module:

```python
def _run_ast_validation(file_path: Path) -> Tuple[bool, str]:
    try:
        source = file_path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(file_path))
        return True, "AST Syntax Valid"
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
```

**AST Benefits**:
- Executes in **$< 10\text{ ms}$**.
- Immediately flags indentation mistakes, unmatched brackets, or malformed syntax.
- Bypasses expensive subprocess invocations if the code cannot parse.

---

## 3. Scoped Test Discovery & Execution

If the AST validation passes, the engine automatically resolves the corresponding scoped test file:

```
    Target File: package/aegis/caffeinate.py
                     │
                     ▼
    Discovery: tests/test_caffeinate.py
                     │
                     ▼
    Runner Invocation: `uv run pytest tests/test_caffeinate.py -q --tb=short`
                     │
                     ▼
    Execution Time: < 800 ms (Single test target)
```

If the target is already a test file (e.g. `tests/test_workers.py`), it executes that file directly.

### 3.1 Telemetry Output Schema
The fast-path test runner returns structured JSON telemetry:
```json
{
  "status": "pass",
  "ast_valid": true,
  "ast_message": "AST Syntax Valid",
  "test_target": "tests/test_caffeinate.py",
  "test_output": "12 passed in 0.42s",
  "elapsed_ms": 482.15
}
```

---

## 4. Continuous Integration & Parity

While fast-path testing accelerates local agent iteration, continuous integration requires exhaustive validation across all target environments.

### 4.1 CI Workflow Configuration (`.github/workflows/ci.yml`)
AegisBrain enforces a strict multi-OS and multi-version test matrix on every commit:
- **Operating Systems**: Ubuntu Linux (`ubuntu-latest`), macOS (`macos-latest`), Windows (`windows-latest`).
- **Python Versions**: Python 3.10, 3.11, 3.12, 3.13.
- **Pass Rate Invariant**: **281 / 281 tests passing (100%)**.

Any commit that causes a regression in the 281-test baseline is automatically blocked by CI status checks.

---

## 5. CLI Usage

```bash
# Execute fast-path AST check and scoped test on a single file (< 1s)
aegis test package/aegis/workers.py

# Execute scoped test directly
aegis test tests/test_hierarchy.py

# Output test result as structured JSON for agent consumption
aegis test package/aegis/hands.py --json
```
