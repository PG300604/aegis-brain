---
name: unslop-master
description: "Consolidated AI slop removal super skill: code unslop (Karpathy simplicity + Ponytail minimal diffs), prose unslop (TurnItOut + Unslop CLI sycophancy & stock buzzword eradication), UI/design anti-slop (zero blurred gradient blobs), AI hallmark eradication, and callable two-stage scrubbing."
tools: [claude-code, codex, gemini-cli, antigravity, hermes, cursor, opencode, aider]
category: writing
risk: safe
tags: [unslop, deslop, anti-ui-slop, turnitout, ponytail, karpathy-simplicity, ai-watermarks, code-quality, prose-quality, two-stage-scrub]
---

# Unslop Master: Consolidated AI Slop Removal Super Skill

> **One skill to rule them all.** Unslop Master consolidates the battle-tested anti-slop doctrines from Karpathy's simplicity principles, Ponytail's minimal diffs, TurnItOut's prose hygiene, and the Unslop CLI's vocabulary eradication into a single, callable, two-stage scrubbing pipeline. Use it as a library, a CLI, or a pre-commit gate.

---

## Core Philosophy & Architecture

### Why AI Slop Happens

LLMs are trained to be helpful, verbose, and "impressive." This produces five systemic failure modes:

| Failure Mode | Manifestation | Root Cause |
|--------------|---------------|------------|
| **Speculative Over-Engineering** | Wrapper classes, factory patterns, abstract base classes for 50-line scripts | RLHF reward for "completeness" |
| **Sycophantic Prose** | "Certainly! Here's a comprehensive solution..." | Training on assistant-like dialogue |
| **Stock Vocabulary** | "delve," "tapestry," "pivotal," "seamless," "robust" | High-probability tokens in corporate/tech writing |
| **UI Template Rot** | Blurred gradient blobs, purple/pink amorphous backgrounds | Copy-paste from Dribbble/CodePen trends |
| **AI Hallmarks** | Em-dash pileups, negative tricolons, robotic transitions | Decoding artifacts + training distribution |

### How Unslop Master Eradicates It

Unslop Master operates on a **two-stage pipeline** that can run during generation (streaming), post-generation (CLI), or at commit time (pre-commit hook):

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT (code / prose / UI)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: FAST PASS (regex, streaming-compatible, <5ms)         │
│  • Sycophancy phrase stripping                                  │
│  • Stock vocabulary regex replacement                           │
│  • Em-dash normalization                                        │
│  • Negative tricolon detection                                  │
│  • Robotic transition removal                                   │
│  • Trivial comment eradication (code)                           │
│  • Blurred gradient blob detection (UI)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: DEEP PASS (--deep flag, AST-aware, ~50-200ms)         │
│  • Python AST inspection: unused imports, dead code, complexity │
│  • Ponytail minimal diff enforcement                            │
│  • Karpathy simplicity scoring (stdlib first, no wrappers)      │
│  • Comprehensive vocabulary replacement with context awareness  │
│  • UI contrast token audit & accessibility check                │
│  • Mandatory UI state verification (loading/empty/error/disabled)│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLEAN OUTPUT + METRICS REPORT                │
└─────────────────────────────────────────────────────────────────┘
```

---

## The 4 Pillars of Slop Removal

### Pillar 1: Code Unslop

#### 1.1 Andrej Karpathy Simplicity Doctrine

> **"The best code is no code. The second best is standard library. The third best is a boring, obvious solution."**

**Rules:**
- **Standard library first** — `urllib`, `json`, `pathlib`, `dataclasses`, `itertools`, `functools` before any third-party dependency
- **Zero speculative wrappers** — No `DatabaseManager`, `ConfigLoader`, `ServiceFactory` unless the problem *demands* it
- **Surgical diffs** — Touch only the lines that change behavior; no "while we're here" refactorings
- **Flat > nested** — Prefer module-level functions over classes; prefer composition over inheritance
- **Explicit > implicit** — No magic, no metaclasses, no `__getattr__` tricks unless absolutely necessary

**Anti-Patterns → Clean Patterns:**

| Anti-Pattern (Slop) | Clean Pattern (Unslop) |
|---------------------|------------------------|
| `class ConfigManager: ...` wrapping `json.load()` | `config = json.loads(path.read_text())` |
| `AbstractBaseService` + 3 subclasses for one endpoint | `def fetch_user(id): return httpx.get(...).json()` |
| `Factory.create()` returning `Strategy` implementations | `if condition: return path_a(); return path_b()` |
| 50-line `__init__.py` re-exporting everything | `from .core import main` (one line) |

#### 1.2 Ponytail Minimal Diffs

> **"Touch only what was asked. No unsolicited refactorings. No drive-by cleanups."**

**Rules:**
- **Single intent per change** — One PR/commit = one logical change
- **No formatting drive-bys** — Don't reformat unrelated files; don't fix lint in untouched code
- **No "improvements" in passing** — If you notice a typo in a comment *outside* your diff, file a separate issue
- **Test the delta** — Verify only the changed behavior works; don't rewrite tests for unchanged code

**Enforcement (Deep Pass):**
```python
# AST-based diff analysis
def enforce_minimal_diff(old_ast, new_ast, changed_lines):
    # Reject: new imports not used in changed_lines
    # Reject: function signature changes outside changed_lines
    # Reject: class hierarchy modifications outside changed_lines
    # Allow: only nodes intersecting changed_lines
```

#### 1.3 Trivial/Redundant Comment Eradication

**Delete on sight (Stage 1 regex):**

```python
# BAD — trivial comments
import os                    # Import os module
class User:                 # User class
    def __init__(self):     # Constructor
        self.name = ""      # Initialize name
    def get_name(self):     # Helper function to get name
        return self.name    # Return the name

# GOOD — self-documenting code
import os
class User:
    def __init__(self):
        self.name = ""
    def get_name(self):
        return self.name
```

**Patterns nuked (regex):**
- `^\s*#\s*(Import|Importing)\s+\w+`
- `^\s*#\s*(Constructor|Initializer)`
- `^\s*#\s*(Helper|Utility)\s+(function|method)`
- `^\s*#\s*(Initialize|Initializing)\s+\w+`
- `^\s*#\s*Return\s+(the\s+)?\w+`
- `^\s*//\s*(Constructor|Constructor for|Initializes)`

---

### Pillar 2: Prose Unslop

#### 2.1 Conversational Sycophancy & AI Pleasantries Eradication

**Stage 1 (Fast Pass) — Zero-tolerance regex strip list:**

| Category | Phrases Nuked |
|----------|---------------|
| **Openers** | "Certainly!", "Sure!", "Of course!", "Absolutely!", "Definitely!", "I'd be happy to", "I would be happy to", "I'm happy to", "Let me help you with", "I can help with that" |
| **Transitions** | "Let's dive in", "Let's get started", "Here's a comprehensive", "Here is a detailed", "Below you'll find", "Following is a" |
| **Closers** | "I hope this helps!", "Hope this helps!", "Let me know if you need anything else", "Feel free to ask", "Happy to help further", "I'm here if you need anything" |
| **Identity** | "As an AI language model", "As an AI", "As a language model", "I don't have personal opinions", "I cannot browse" |
| **Hedging** | "It's important to note that", "It should be noted that", "Please note that", "Note that", "Keep in mind that" |

**Replacement logic:** Delete entirely. No replacement text. The content starts *immediately*.

#### 2.2 Stock AI Vocabulary Eradication

**Stage 1 (Fast Pass) — High-confidence replacements:**

| Slop Word | Replacement | Context Notes |
|-----------|-------------|---------------|
| delve | explore, examine, investigate | Never "delve into" |
| tapestry | fabric, mosaic, weave (literal only) | Metaphorical use → delete |
| testament | proof, evidence, sign | "A testament to" → "shows" |
| pivotal | key, critical, central | |
| seamless | smooth, integrated, unified | |
| robust | strong, reliable, resilient | |
| leverage | use, exploit, apply | Never as noun |
| in today's world | today, now, currently | Delete phrase entirely |
| supercharge | boost, accelerate, enhance | |
| game-changer | breakthrough, turning point | |
| cutting-edge | advanced, latest, modern | |
| elevate | raise, improve, lift | |
| unleash | release, launch, enable | |
| demystify | clarify, explain, simplify | |
| landscape | field, domain, space | "AI landscape" → "AI field" |
| paradigm shift | fundamental change | |
| holistic | comprehensive, complete | |
| granular | detailed, fine-grained | |
| actionable | practical, concrete | |
| bandwidth | capacity, time, resources | |
| low-hanging fruit | easy wins, quick wins | |
| move the needle | make a difference, change outcomes | |
| at the end of the day | ultimately, finally | |
| deep dive | thorough analysis, detailed review | |
| best practice | recommended approach | |
| silver bullet | simple solution | |
| low-hanging fruit | easy wins | |
| circle back | revisit, return to | |
| touch base | contact, follow up | |

**Stage 2 (Deep Pass) — Context-aware LLM pass:**
- Detects *novel* stock phrases not in static list
- Preserves legitimate technical usage (e.g., "robust" in "robust statistics")
- Rewrites sentences for human cadence, not token probability

---

### Pillar 3: UI/Design Unslop (Anti-UI-Slop)

#### 3.1 Zero Blurred Gradient Blob Templates

**Banned patterns (Stage 1 detection):**

```css
/* NEVER ALLOWED */
.blob {
  filter: blur(80px) / blur(100px) / blur(120px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* or */
  background: radial-gradient(circle, #ff6b6b, #ee5a5a);
  /* purple/pink amorphous divs */
  position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
}
```

**Enforcement:**
- Stage 1: Regex scan for `filter:\s*blur\(` + gradient backgrounds on same element
- Stage 2: Computed style audit — flag any element with `backdrop-filter: blur()` covering >20% viewport

#### 3.2 Real Product Contrast Tokens & Accessible Palette

**Required token system (enforced at Gate 1):**

```css
:root {
  /* Semantic tokens — NO raw hex in components */
  --color-bg: #0a0a0b;
  --color-bg-elevated: #141416;
  --color-border: #2a2a2e;
  --color-border-strong: #3d3d42;
  
  --color-fg: #fafafa;
  --color-fg-muted: #a1a1aa;
  --color-fg-subtle: #71717a;
  
  --color-brand: #3b82f6;        /* WCAG AA on --color-bg */
  --color-brand-hover: #2563eb;
  --color-brand-muted: #1e3a5f;  /* 4.5:1 on --color-bg */
  
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Focus ring — mandatory visible focus */
  --focus-ring: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-brand);
}
```

**Audit rules (Deep Pass):**
- Every `color:` / `background:` / `border-color:` must reference a token
- All interactive states meet WCAG AA (4.5:1 normal, 3:1 large)
- Focus indicators visible and not `outline: none`

#### 3.3 Mandatory UI States

**Every interactive component MUST define (Deep Pass audit):**

| State | Required | Example |
|-------|----------|---------|
| **Default** | Yes | `btn { background: var(--color-brand) }` |
| **Hover** | Yes | `btn:hover { background: var(--color-brand-hover) }` |
| **Active/Pressed** | Yes | `btn:active { transform: scale(0.98) }` |
| **Focus-visible** | Yes | `btn:focus-visible { box-shadow: var(--focus-ring) }` |
| **Disabled** | Yes | `btn:disabled { opacity: 0.5; cursor: not-allowed }` |
| **Loading** | Yes | `btn.loading { position: relative; } btn.loading::after { content: ""; @keyframes spin... }` |
| **Empty** | For lists/tables | `.empty-state { padding: 3rem; text-align: center; color: var(--color-fg-muted) }` |
| **Error** | For forms/inputs | `.input.error { border-color: var(--color-error) } .error-message { color: var(--color-error) }` |

**Missing state = Gate 1 failure.**

---

### Pillar 4: AI Hallmark & Watermark Eradication

#### 4.1 Em-Dash Pileup Normalization

**Pattern:** ` — ... — ... — ` (multiple em-dashes in one paragraph)

**Stage 1 Fix:**
```python
# Normalize: keep at most ONE em-dash per sentence
# "This — that — the other" → "This; that, and the other."
# "A — B — C — D" → "A, B, C, and D."
```

**Rules:**
- Max 1 em-dash per 200 characters
- Convert parenthetical em-dash pairs to parentheses or commas
- Convert list-separating em-dashes to commas/semicolons

#### 4.2 Negative Tricolon Normalization

**Pattern:** "No X, no Y, no Z" / "Not A, not B, not C" / "Never X, never Y, never Z"

**Stage 1 Fix:**
```python
# Detect: (no|not|never)\s+\w+,\s*(no|not|never)\s+\w+,\s*(no|not|never)\s+\w+
# Rewrite: "No X, no Y, no Z" → "Neither X nor Y nor Z" / "None of X, Y, or Z"
```

**Why:** This cadence is a high-probability LLM decoding artifact; humans rarely chain three parallel negatives.

#### 4.3 Robotic Transition Removal

**Stage 1 Strip List (delete entirely, no replacement):**

| Transition | Action |
|------------|--------|
| "Moreover," | Delete |
| "Furthermore," | Delete |
| "Additionally," | Delete |
| "In addition," | Delete |
| "Also," (sentence-initial) | Delete |
| "Consequently," | Delete → "So," / "Therefore," |
| "In conclusion," | Delete |
| "To summarize," | Delete |
| "To sum up," | Delete |
| "Overall," | Delete |
| "Ultimately," | Delete |
| "It is worth noting that" | Delete |
| "It should be noted that" | Delete |
| "It is important to note that" | Delete |
| "Please note that" | Delete |
| "Note that" | Delete |
| "Keep in mind that" | Delete |
| "Bear in mind that" | Delete |

**Stage 2:** Rewrites sentence boundaries for natural flow instead of list-like transitions.

---

## Callable Two-Stage Scrub

### Stage 1: Fast Pass (Streaming-Compatible)

**Characteristics:**
- Pure regex / string replacement — no AST, no LLM
- **< 5ms** for typical input (< 10KB)
- Runs inline during generation (streaming callback) or as first CLI pass
- Deterministic, idempotent, no false positives on code

**Pipeline:**
```python
def fast_pass(text: str, mode: Mode = "auto") -> FastPassResult:
    text = strip_sycophancy(text)
    text = replace_stock_vocab(text)
    text = normalize_em_dashes(text)
    text = normalize_negative_tricolons(text)
    text = strip_robotic_transitions(text)
    
    if mode in ("auto", "code"):
        text = strip_trivial_comments(text)
    
    if mode in ("auto", "ui"):
        text = flag_blur_blobs(text)  # Returns warnings, doesn't mutate
    
    return FastPassResult(cleaned=text, warnings=warnings, metrics=metrics)
```

**Streaming usage:**
```python
# In your generation pipeline
async def generate_with_unslop(prompt, stream_callback):
    buffer = ""
    async for chunk in llm.stream(prompt):
        buffer += chunk
        # Fast pass every ~500 chars or at sentence boundaries
        if len(buffer) > 500 or chunk.endswith((".", "!", "?")):
            clean, _ = fast_pass(buffer)
            stream_callback(clean)
            buffer = ""
    if buffer:
        stream_callback(fast_pass(buffer).cleaned)
```

### Stage 2: Deep Pass (`--deep`)

**Characteristics:**
- AST-aware (Python), LLM-assisted (prose), computed-style audit (UI)
- **~50-200ms** depending on input size
- Runs post-generation, at commit, or on demand
- Produces detailed metrics report

**Pipeline:**
```python
def deep_pass(text: str, mode: Mode = "auto", filepath: Path = None) -> DeepPassResult:
    result = fast_pass(text, mode)  # Always run fast pass first
    
    if mode in ("auto", "code") and is_python(filepath):
        result = python_ast_audit(result.cleaned, filepath)
        # - Unused imports
        # - Dead code (unreachable after return/raise)
        # - Cyclomatic complexity > 10
        # - Ponytail minimal diff check (if git diff available)
        # - Karpathy simplicity score
    
    if mode in ("auto", "prose"):
        result = llm_vocab_audit(result.cleaned)
        # - Novel stock phrases not in static list
        # - Sentence variety score
        # - Passive voice density
        # - Readability metrics (Flesch-Kincaid)
    
    if mode in ("auto", "ui") and is_css_or_jsx(filepath):
        result = ui_audit(result.cleaned, filepath)
        # - Token compliance
        # - Contrast ratios
        # - Mandatory state coverage
        # - Blur blob computed style check
    
    return result
```

**Python AST Audit Details:**
```python
class PythonASTAuditor(ast.NodeVisitor):
    def visit_Import(self, node):
        # Track imports; cross-reference with Name/Attribute visits
        # Flag unused after full traversal
    
    def visit_FunctionDef(self, node):
        # Complexity: count if/for/while/try/except/and/or
        # Flag > 10
        # Dead code: statements after return/raise/break/continue
    
    def visit_ClassDef(self, node):
        # Flag: single-method classes (use function)
        # Flag: classes only wrapping stdlib (Karpathy violation)
    
    def karpathy_score(self, tree) -> float:
        # 0.0 = maximum slop, 1.0 = Karpathy ideal
        # Factors: stdlib usage, nesting depth, wrapper classes, lines per function
```

---

## CLI & API Reference

### CLI: `aegis unslop`

```bash
# Basic usage (fast pass only)
aegis unslop "Your text here"

# Deep pass
aegis unslop "Your text here" --deep

# Explicit mode
aegis unslop "code snippet" --mode code --deep
aegis unslop "blog post" --mode prose --deep
aegis unslop "component.jsx" --mode ui --deep

# From file
aegis unslop --file src/main.py --deep

# Check mode (exit code 1 if slop found, no output)
aegis unslop --file src/main.py --check
echo $?  # 0 = clean, 1 = slop detected

# Output metrics JSON
aegis unslop --file src/main.py --deep --json
```

**Full CLI Help:**
```
usage: aegis unslop [-h] [text] [--deep] [--mode {auto,code,prose,ui}] 
                    [--file PATH] [--check] [--json] [--output PATH]

Consolidated AI slop removal: code, prose, UI, and hallmark eradication.

positional arguments:
  text                  Input text (stdin if omitted)

options:
  -h, --help            Show this help message and exit
  --deep                Run Stage 2 deep pass (AST, LLM vocab, UI audit)
  --mode {auto,code,prose,ui}
                        Force mode (default: auto-detect from content/file)
  --file PATH           Read input from file instead of stdin/arg
  --check               Exit 1 if slop found, 0 if clean; no output
  --json                Output metrics report as JSON
  --output PATH         Write cleaned output to file (default: stdout)
```

### Python Programmatic API

```python
from aegis.unslop_master import UnslopMaster, unslop, Mode, FastPassResult, DeepPassResult

# Simple one-liner (fast pass)
clean = unslop("Certainly! Here's a robust solution that delves into...")

# Deep pass with metrics
result: DeepPassResult = unslop(content, deep=True, mode=Mode.CODE)
print(result.cleaned)
print(result.metrics)
# {
#   "fast_pass": {"sycophancy_stripped": 2, "vocab_replaced": 5, ...},
#   "deep_pass": {"unused_imports": 3, "complexity_violations": 1, "karpathy_score": 0.72}
# }

# Class-based for configuration/reuse
master = UnslopMaster(
    deep=True,
    mode=Mode.AUTO,
    custom_vocab_replacements={"foo": "bar"},
    karpathy_threshold=0.7,
    complexity_threshold=10
)
result = master.scrub(filepath=Path("src/app.py"))
```

**Types:**
```python
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List

class Mode(Enum):
    AUTO = "auto"
    CODE = "code"
    PROSE = "prose"
    UI = "ui"

@dataclass
class Metrics:
    fast_pass: Dict[str, int]
    deep_pass: Optional[Dict[str, Any]] = None
    warnings: List[str] = None

@dataclass
class FastPassResult:
    cleaned: str
    metrics: Metrics
    warnings: List[str]

@dataclass
class DeepPassResult(FastPassResult):
    ast_findings: Optional[List[Dict]] = None
    ui_audit: Optional[Dict] = None
```

---

## Integration with Quality Gates

### Gate 1 Enforcement in `package/aegis/pipeline.py`

Unslop Master runs as **Gate 1** — before security audits, secret scans, and type checking — because slop removal can *change* the code surface that later gates analyze.

```python
# package/aegis/pipeline.py
from aegis.unslop_master import UnslopMaster, Mode
from aegis.gates import Gate, GateResult, Severity

class UnslopGate(Gate):
    """Gate 1: AI Slop Removal — must pass before all other gates."""
    
    name = "unslop"
    order = 1  # Runs FIRST
    
    def __init__(self, config: Dict = None):
        self.master = UnslopMaster(
            deep=config.get("deep", True),
            karpathy_threshold=config.get("karpathy_threshold", 0.7),
            complexity_threshold=config.get("complexity_threshold", 10),
            fail_on_warnings=config.get("fail_on_warnings", False)
        )
    
    def run(self, context: PipelineContext) -> GateResult:
        findings = []
        
        for file_path in context.changed_files:
            # Skip non-text files
            if not self._is_text_file(file_path):
                continue
            
            mode = self._detect_mode(file_path)
            result = self.master.scrub(filepath=file_path, mode=mode)
            
            # Fast pass findings (warnings only by default)
            for warning in result.warnings:
                findings.append(Finding(
                    file=file_path,
                    line=warning.line,
                    severity=Severity.WARNING,
                    code="UNSLOP_FAST_PASS",
                    message=warning.message
                ))
            
            # Deep pass findings (errors if thresholds breached)
            if result.deep_pass:
                for finding in result.ast_findings or []:
                    sev = Severity.ERROR if finding["severity"] == "error" else Severity.WARNING
                    findings.append(Finding(
                        file=file_path,
                        line=finding["line"],
                        severity=sev,
                        code=f"UNSLOP_{finding['code']}",
                        message=finding["message"]
                    ))
                
                # Karpathy score gate
                if result.metrics.deep_pass.get("karpathy_score", 1.0) < self.master.karpathy_threshold:
                    findings.append(Finding(
                        file=file_path,
                        line=1,
                        severity=Severity.ERROR,
                        code="UNSLOP_KARPATHY_SCORE",
                        message=f"Karpathy simplicity score {result.metrics.deep_pass['karpathy_score']:.2f} "
                                f"below threshold {self.master.karpathy_threshold}"
                    ))
                
                # Complexity gate
                for func in result.metrics.deep_pass.get("complex_functions", []):
                    if func["complexity"] > self.master.complexity_threshold:
                        findings.append(Finding(
                            file=file_path,
                            line=func["line"],
                            severity=Severity.ERROR,
                            code="UNSLOP_COMPLEXITY",
                            message=f"Function '{func['name']}' complexity {func['complexity']} "
                                    f"exceeds threshold {self.master.complexity_threshold}"
                        ))
        
        return GateResult(
            passed=not any(f.severity == Severity.ERROR for f in findings),
            findings=findings,
            metrics=result.metrics if 'result' in locals() else None
        )
```

**Gate Ordering in Pipeline:**
```python
# package/aegis/pipeline.py
GATE_REGISTRY = [
    UnslopGate,           # 1: Slop removal (MUST be first)
    SecurityAuditGate,    # 2: Bandit, semgrep
    SecretScanGate,       # 3: GitGuardian, trufflehog
    TypeCheckGate,        # 4: pyright/mypy
    LintGate,             # 5: ruff, eslint
    TestGate,             # 6: pytest, vitest
    BuildGate,            # 7: Compilation/bundling
]
```

### Git Pre-Commit Hook Integration

**`.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: local
    hooks:
      - id: aegis-unslop
        name: "Aegis Unslop Master (Gate 1)"
        entry: aegis unslop --check
        language: system
        types: [python, javascript, typescript, jsx, tsx, css, scss, markdown, md]
        require_serial: true
        # Run on staged files only
        args: ["--deep"]
        # Fail commit if slop detected
        verbose: true
```

**Install:**
```bash
pre-commit install
pre-commit run aegis-unslop --all-files  # Test run
```

**Bypass (emergency only):**
```bash
git commit --no-verify  # Skips all hooks
# OR
SKIP=aegis-unslop git commit  # Skips only this hook
```

### CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/quality.yml
name: Quality Gates
on: [push, pull_request]

jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Install Aegis
        run: pip install -e ./package/aegis
      
      - name: Run Unslop Gate (Gate 1)
        id: unslop
        run: |
          aegis unslop --check --deep --json > unslop-report.json || true
          echo "report=$(cat unslop-report.json)" >> $GITHUB_OUTPUT
      
      - name: Upload Unslop Report
        uses: actions/upload-artifact@v4
        with:
          name: unslop-report
          path: unslop-report.json
      
      - name: Fail if Gate 1 Failed
        if: fromJson(steps.unslop.outputs.report).passed == false
        run: |
          echo "::error::Unslop Gate failed — see artifact for details"
          exit 1
      
      # Subsequent gates only run if Unslop passes
      - name: Run Security Audit
        if: steps.unslop.outputs.report.passed == 'true'
        run: aegis gate security
      
      - name: Run Secret Scan
        if: steps.unslop.outputs.report.passed == 'true'
        run: aegis gate secrets
      
      # ... etc
```

---

## Configuration Reference

### `aegis.unslop` Config Section (YAML/TOML/JSON)

```yaml
# aegis.config.yaml
unslop:
  # Global toggles
  enabled: true
  deep_by_default: false          # --deep required for deep pass
  fail_on_warnings: false         # Treat warnings as errors
  
  # Thresholds
  karpathy_threshold: 0.7         # 0.0-1.0, deep pass only
  complexity_threshold: 10        # Cyclomatic complexity, deep pass only
  max_em_dashes_per_200_chars: 1  # Fast pass
  
  # Custom vocabulary replacements (merged with built-in)
  custom_vocab:
    "utilize": "use"
    "methodology": "method"
    "facilitate": "help"
    "optimize": "improve"
  
  # Mode-specific
  code:
    strip_trivial_comments: true
    enforce_minimal_diffs: true   # Requires git repo
    allow_stdlib_wrappers: false  # Karpathy strict mode
  
  prose:
    llm_vocab_audit: true         # Deep pass: LLM-assisted
    target_readability: "flesch-kincaid-60"
    max_passive_voice_ratio: 0.15
  
  ui:
    require_tokens: true          # All colors must use CSS custom properties
    wcag_level: "AA"              # AA or AAA
    mandatory_states:
      - hover
      - focus-visible
      - active
      - disabled
      - loading
      - empty
      - error
    ban_blur_blobs: true
```

---

## Metrics & Reporting

### Fast Pass Metrics
```json
{
  "fast_pass": {
    "sycophancy_phrases_stripped": 3,
    "stock_vocab_replacements": 7,
    "em_dashes_normalized": 2,
    "negative_tricolons_rewritten": 1,
    "robotic_transitions_removed": 4,
    "trivial_comments_stripped": 12,
    "blur_blob_warnings": 0,
    "chars_processed": 15420,
    "duration_ms": 3
  }
}
```

### Deep Pass Metrics (Code)
```json
{
  "deep_pass": {
    "karpathy_score": 0.73,
    "karpathy_threshold": 0.7,
    "karpathy_passed": true,
    "unused_imports": 2,
    "dead_code_blocks": 1,
    "complex_functions": [
      {"name": "process_data", "line": 45, "complexity": 14}
    ],
    "minimal_diff_violations": 0,
    "wrapper_classes_flagged": 1,
    "duration_ms": 87
  }
}
```

### Deep Pass Metrics (UI)
```json
{
  "deep_pass": {
    "ui_audit": {
      "token_compliance": 0.94,
      "contrast_violations": 0,
      "missing_states": {
        "Button": ["loading", "empty"],
        "DataTable": ["error"]
      },
      "blur_blob_elements": 0,
      "focus_visible_coverage": 1.0
    },
    "duration_ms": 112
  }
}
```

---

## Quick Reference Card

| Task | Command/API |
|------|-------------|
| **Quick clean (clipboard)** | `aegis unslop "$(pbpaste)" | pbcopy` |
| **Clean file in place** | `aegis unslop --file src/main.py --deep --output src/main.py` |
| **Check only (CI)** | `aegis unslop --check --deep --file src/main.py` |
| **Python: fast pass** | `unslop(text)` |
| **Python: deep pass** | `unslop(text, deep=True, mode=Mode.CODE)` |
| **Python: with metrics** | `result = unslop(text, deep=True); print(result.metrics)` |
| **Pre-commit install** | `pre-commit install` |
| **View config** | `aegis config show unslop` |

---

## Philosophy Summary

> **Unslop Master doesn't make your code "better" — it makes it *honest*.**  
> It removes the performance of competence so actual competence can show through.  
> No theater. No filler. No gradients. Just signal.

---

*Part of the Aegis quality pipeline. Gate 1 of 7. Zero tolerance for slop.*
