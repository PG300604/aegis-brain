"""AegisBrain Worker Model Onboarding & Discovery Wizard.

Provides deterministic zero-guesswork discovery, configuration, and priority cascading
for Tier 3 execution workers (OpenCode, Hermes, Ollama):
- Priority 1: OpenCode (High-Reasoning Free Models, e.g. DeepSeek V4.1 Flash Free, Flint 40B)
- Priority 2: Hermes (Fast Cloud Fallback Chain)
- Priority 3: Local Ollama (qwen2.5-coder:7b strictly for offline failover, never left running to save RAM)

Invariants:
- Strict No-Guesswork Rule: When active model favorites cannot be proven statically (e.g. OpenCode TUI),
  never guess! Prompt user for exact names or terminal screenshot.
- Zero-cost: Focuses exclusively on $0.00 / Free Tier models.
- Fast-Path Testing: In-memory AST verification + scoped pytest (< 1s).
"""

from __future__ import annotations

import ast
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from aegis.db import (
    clear_worker_models,
    get_worker_cascade,
    get_worker_models,
    save_worker_model,
)

logger = logging.getLogger(__name__)

OPENCODE_SUGGESTED_FREE_MODELS = [
    "DeepSeek V4.1 Flash Free",
    "Flint 40B Free",
    "Nemotron 3.5 Super VL Free",
    "Big Pickle",
    "Crouton Alpha Free",
]


# =============================================================================
# OpenCode Detection (Strict No-Guesswork)
# =============================================================================

def _find_opencode_config_paths() -> List[Path]:
    """Return all known OpenCode config file paths across platforms."""
    paths: List[Path] = []
    home = Path.home()

    # Unix / standard .config
    paths.append(home / ".config" / "opencode" / "opencode.jsonc")
    paths.append(home / ".config" / "opencode" / "cli.json")
    paths.append(home / ".config" / "opencode" / "tui.jsonc")
    paths.append(home / ".config" / "opencode" / "models.json")
    paths.append(home / ".opencode" / "opencode.jsonc")
    paths.append(home / ".opencode" / "cli.json")

    # Windows AppData
    appdata = os.environ.get("APPDATA")
    if appdata:
        paths.append(Path(appdata) / "opencode" / "opencode.jsonc")
        paths.append(Path(appdata) / "opencode" / "cli.json")
        paths.append(Path(appdata) / "opencode" / "tui.jsonc")
        paths.append(Path(appdata) / "opencode" / "models.json")

    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        paths.append(Path(localappdata) / "opencode" / "opencode.jsonc")
        paths.append(Path(localappdata) / "opencode" / "cli.json")

    return paths


def _parse_jsonc(content: str) -> Optional[Dict[str, Any]]:
    """Parse JSONC (JSON with comments) safely."""
    # Strip single-line and multi-line comments
    clean = re.sub(r"//.*", "", content)
    clean = re.sub(r"/\*.*?\*/", "", clean, flags=re.DOTALL)
    try:
        data = json.loads(clean.strip())
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def detect_opencode_models() -> Dict[str, Any]:
    """Detect OpenCode installation and configured models with Strict No-Guesswork Rule."""
    # Check execution binary or npm shim
    has_binary = bool(
        shutil.which("opencode")
        or shutil.which("opencode.cmd")
        or shutil.which("opencode.ps1")
    )

    config_paths = _find_opencode_config_paths()
    config_dir_exists = any(p.parent.exists() for p in config_paths)

    if not has_binary and not config_dir_exists:
        return {
            "status": "not_installed",
            "installed": False,
            "models": [],
            "needs_user_input": False,
            "prompt_message": "",
            "suggested_free_models": OPENCODE_SUGGESTED_FREE_MODELS,
        }

    # Inspect config files for explicit model declarations
    found_models: List[str] = []
    for p in config_paths:
        if p.exists() and p.is_file():
            try:
                data = _parse_jsonc(p.read_text(encoding="utf-8", errors="replace"))
                if data:
                    for key in ("model", "models", "defaultModel", "selectedModel", "favorites"):
                        val = data.get(key)
                        if isinstance(val, str) and val.strip():
                            found_models.append(val.strip())
                        elif isinstance(val, list):
                            for item in val:
                                if isinstance(item, str) and item.strip():
                                    found_models.append(item.strip())
            except Exception:
                continue

    # Deduplicate
    unique_models = list(dict.fromkeys(found_models))

    # STRICT NO-GUESSWORK RULE:
    # If OpenCode exists, but models are selected interactively via TUI and not in JSON:
    if not unique_models:
        msg = (
            "OpenCode was detected on your system, but active model selections "
            "cannot be proven statically without guessing from the interactive TUI.\n"
            "Please specify your exact active models (e.g., DeepSeek V4.1 Flash Free, Flint 40B Free) "
            "or upload a terminal screenshot of your OpenCode model selection."
        )
        return {
            "status": "installed_unconfirmed",
            "installed": True,
            "models": [],
            "needs_user_input": True,
            "prompt_message": msg,
            "suggested_free_models": OPENCODE_SUGGESTED_FREE_MODELS,
        }

    return {
        "status": "detected",
        "installed": True,
        "models": unique_models,
        "needs_user_input": False,
        "prompt_message": "",
        "suggested_free_models": OPENCODE_SUGGESTED_FREE_MODELS,
    }


# =============================================================================
# Hermes Fallback Chain Detection
# =============================================================================

def _find_hermes_config_paths() -> List[Path]:
    """Return all known Hermes config paths."""
    paths: List[Path] = []
    home = Path.home()
    paths.append(home / ".hermes" / "config.yaml")

    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        paths.append(Path(localappdata) / "hermes" / "config.yaml")

    appdata = os.environ.get("APPDATA")
    if appdata:
        paths.append(Path(appdata) / "hermes" / "config.yaml")

    return paths


def detect_hermes_fallbacks() -> Dict[str, Any]:
    """Detect Hermes primary model and fallback chain from config.yaml."""
    paths = _find_hermes_config_paths()
    config_file: Optional[Path] = next((p for p in paths if p.exists() and p.is_file()), None)

    if not config_file:
        return {
            "status": "missing",
            "primary": None,
            "fallbacks": [],
            "models": [],
            "config_path": None,
        }

    try:
        content = config_file.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        logger.warning("Could not read Hermes config %s: %e", config_file, e)
        return {
            "status": "error",
            "primary": None,
            "fallbacks": [],
            "models": [],
            "config_path": str(config_file),
        }

    # Extract primary model (model.default or default: <model>)
    primary: Optional[str] = None
    m_default = re.search(r"^\s*model:\s*\n(?:\s+[^\n]+\n)*?\s+default:\s*[\"']?([^\"'\n\r]+)[\"']?", content, re.MULTILINE)
    if m_default:
        primary = m_default.group(1).strip()
    else:
        m_simple = re.search(r"^\s*default:\s*[\"']?([^\"'\n\r]+)[\"']?", content, re.MULTILINE)
        if m_simple:
            primary = m_simple.group(1).strip()

    # Extract fallback_providers
    fallbacks: List[str] = []
    fb_section = re.search(r"^\s*fallback_providers:\s*\n((?:[ \t]+[^\n]+\n?)+)", content, re.MULTILINE)
    if fb_section:
        fb_text = fb_section.group(1)
        # Match lines with `model: <model_name>`
        models_found = re.findall(r"model:\s*[\"']?([^\"'\n\r]+)[\"']?", fb_text)
        if not models_found:
            models_found = re.findall(r"-\s+[\"']?([^\"'\n\r]+)[\"']?", fb_text)
        for m in models_found:
            clean_m = m.strip()
            if clean_m and clean_m not in fallbacks:
                fallbacks.append(clean_m)

    all_models: List[str] = []
    if primary:
        all_models.append(primary)
    for fb in fallbacks:
        if fb not in all_models:
            all_models.append(fb)

    return {
        "status": "detected" if all_models else "empty",
        "primary": primary,
        "fallbacks": fallbacks,
        "models": all_models,
        "config_path": str(config_file),
    }


# =============================================================================
# Ollama Local Models on Disk (Zero RAM Cost)
# =============================================================================

def _find_ollama_manifests_dir() -> Optional[Path]:
    """Locate Ollama manifests directory on disk without starting the daemon."""
    home = Path.home()
    candidates: List[Path] = [
        home / ".ollama" / "models" / "manifests",
        Path("/usr/share/ollama/models/manifests"),
        Path("/var/lib/ollama/models/manifests"),
    ]
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        candidates.append(Path(localappdata) / "ollama" / "models" / "manifests")

    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return None


def detect_ollama_local_models() -> Dict[str, Any]:
    """Detect local models pulled to disk in ~/.ollama/models/manifests."""
    manifests_dir = _find_ollama_manifests_dir()
    if not manifests_dir:
        return {
            "status": "missing",
            "models": [],
            "offline_ready": False,
            "manifests_dir": None,
        }

    models: List[str] = []
    # Structure: manifests/registry.ollama.ai/library/<model>/<tag>
    try:
        for tag_file in manifests_dir.glob("*/*/*/*"):
            if tag_file.is_file():
                model_name = tag_file.parent.name
                tag = tag_file.name
                models.append(f"{model_name}:{tag}")
    except Exception as e:
        logger.warning("Error scanning Ollama manifests: %s", e)

    unique_models = list(dict.fromkeys(models))
    # Offline ready is true if qwen2.5-coder:7b exists
    has_coder = any("qwen2.5-coder:7b" in m for m in unique_models)

    return {
        "status": "detected" if unique_models else "empty",
        "models": unique_models,
        "offline_ready": has_coder,
        "manifests_dir": str(manifests_dir),
    }


# =============================================================================
# Zero-Dollar Worker Setup Advice
# =============================================================================

def get_worker_setup_advice(tool: Optional[str] = None) -> str:
    """Provide clear, actionable instructions to set up free models with zero dollar cost."""
    tool_key = (tool or "").lower().strip()

    opencode_guide = """### 1. OpenCode (Priority 1: High-Reasoning Free Models)
- **Install:** `npm install -g @opencode-ai/opencode`
- **Zero-Cost Free Models:**
  - `DeepSeek V4.1 Flash Free` (OpenRouter)
  - `Flint 40B Free` (Cognitive Computations)
  - `Nemotron 3.5 Super VL Free` (NVIDIA)
  - `Big Pickle` / `Crouton Alpha Free`
- **Config:** OpenCode runs an interactive TUI (`opencode`). Press `Ctrl+P` to select and favorite free models."""

    hermes_guide = """### 2. Hermes Agent (Priority 2: Fast Cloud Fallback Chain)
- **Install:** `pip install hermes-agent` (or `uv tool install hermes-agent`)
- **Configure Free Fallback Chain in `~/.hermes/config.yaml`:**
  ```yaml
  model:
    default: "nvidia/nemotron-3.5-bolt-e4b"

  fallback_providers:
    - model: "thinkingmachines/inkling:free"
    - model: "cohere/north-mini-code:free"
    - model: "google/gemma4-31b-it:free"
    - model: "openrouter/free"
  ```
- **Cost:** $0.00 / Free tier endpoints."""

    ollama_guide = """### 3. Local Ollama (Priority 3: Offline Failover Only)
- **Download:** https://ollama.ai/download
- **Pull Coding Model:**
  ```bash
  ollama pull qwen2.5-coder:7b
  ```
- **RAM Protection Policy:**
  Ollama is strictly for offline failover when network connectivity drops.
  Never leave the Ollama daemon idling in the background to preserve workstation RAM."""

    if tool_key == "opencode":
        return opencode_guide
    elif tool_key == "hermes":
        return hermes_guide
    elif tool_key == "ollama":
        return ollama_guide

    return "\n\n".join([
        "# 🛠️ AegisBrain Zero-Cost Worker Model Setup Guide",
        "Configure these free tiers to enable full token arbitrage without paying a dime:\n",
        opencode_guide,
        hermes_guide,
        ollama_guide,
        "---\n*After configuring, run `aegis workers setup` to auto-detect and persist your cascade.*",
    ])


# =============================================================================
# Onboarding & Discovery Wizard
# =============================================================================

def run_workers_wizard(
    interactive: bool = False,
    user_answers: Optional[Dict[str, Any]] = None,
    auto_save: bool = True,
) -> Dict[str, Any]:
    """Execute the Worker Model Onboarding & Discovery Wizard.

    Follows the team lead mandate:
    1. Check if user configured worker tools.
    2. If not configured: advise clearly how to configure zero-cost free models.
    3. If configured: auto-detect via CLI/configs.
    4. Strict No-Guesswork Rule: if OpenCode model cannot be proven statically,
       prompt for exact names or terminal screenshot.
    5. Save confirmed models into SQLite (brain.db) with priority cascade.
    """
    answers = user_answers or {}
    report: Dict[str, Any] = {
        "opencode": {},
        "hermes": {},
        "ollama": {},
        "cascade": [],
        "warnings": [],
        "setup_advice_needed": False,
        "saved_count": 0,
    }

    # Step 1: User explicitly stated tools are not yet configured
    if answers.get("configured") is False or answers.get("has_tools") is False:
        report["setup_advice_needed"] = True
        report["setup_advice"] = get_worker_setup_advice()
        return report

    # Step 2: Auto-detect tools
    oc_res = detect_opencode_models()
    hm_res = detect_hermes_fallbacks()
    ol_res = detect_ollama_local_models()

    report["opencode"] = oc_res
    report["hermes"] = hm_res
    report["ollama"] = ol_res

    # If nothing is detected at all and no models were confirmed by the user, return advice
    has_user_models = bool(answers.get("opencode_models") or answers.get("models"))
    if (
        not has_user_models
        and oc_res.get("status") == "not_installed"
        and hm_res.get("status") == "missing"
        and ol_res.get("status") == "missing"
    ):
        report["setup_advice_needed"] = True
        report["setup_advice"] = get_worker_setup_advice()
        report["warnings"].append("No worker tools detected. Review the zero-cost setup guide.")
        return report

    # Step 3: Strict No-Guesswork Rule for OpenCode
    confirmed_opencode_models: List[str] = []
    if answers.get("opencode_models") or answers.get("models"):
        raw = answers.get("opencode_models") or answers.get("models")
        if isinstance(raw, str):
            confirmed_opencode_models = [m.strip() for m in raw.split(",") if m.strip()]
        elif isinstance(raw, list):
            confirmed_opencode_models = [str(m).strip() for m in raw if str(m).strip()]
        report["opencode"]["status"] = "user_confirmed"
        report["opencode"]["needs_user_input"] = False
        report["opencode"]["models"] = confirmed_opencode_models

    elif oc_res.get("models"):
        confirmed_opencode_models = oc_res["models"]

    elif oc_res.get("needs_user_input"):
        report["warnings"].append(
            "OpenCode detected but active models unconfirmed. "
            "Please provide model names or terminal screenshot via `aegis workers setup --models ...`"
        )

    # Step 4: Persist confirmed models to DB with Priority Cascade
    if auto_save:
        clear_worker_models()

    cascade_entries: List[Dict[str, Any]] = []
    saved_count = 0

    # --- Priority 1: OpenCode High-Reasoning Free Models ---
    for i, m in enumerate(confirmed_opencode_models):
        entry = {
            "tool_name": "opencode",
            "model_name": m,
            "display_name": m,
            "priority": 1,
            "is_primary": (i == 0),
            "is_free": True,
            "fallback_order": i,
            "offline_ready": False,
        }
        cascade_entries.append(entry)
        if auto_save:
            save_worker_model(**entry)
            saved_count += 1

    # --- Priority 2: Hermes Cloud Fallback Chain ---
    if hm_res.get("primary"):
        primary_m = hm_res["primary"]
        is_primary = (len(confirmed_opencode_models) == 0)
        entry = {
            "tool_name": "hermes",
            "model_name": primary_m,
            "display_name": primary_m,
            "priority": 2,
            "is_primary": is_primary,
            "is_free": True,
            "fallback_order": 0,
            "offline_ready": False,
        }
        cascade_entries.append(entry)
        if auto_save:
            save_worker_model(**entry)
            saved_count += 1

    for idx, fb in enumerate(hm_res.get("fallbacks", [])):
        if fb != hm_res.get("primary"):
            entry = {
                "tool_name": "hermes",
                "model_name": fb,
                "display_name": fb,
                "priority": 2,
                "is_primary": False,
                "is_free": True,
                "fallback_order": idx + 1,
                "offline_ready": False,
            }
            cascade_entries.append(entry)
            if auto_save:
                save_worker_model(**entry)
                saved_count += 1

    # --- Priority 3: Local Ollama (qwen2.5-coder:7b) strictly for offline failover ---
    for idx, ol_m in enumerate(ol_res.get("models", [])):
        entry = {
            "tool_name": "ollama",
            "model_name": ol_m,
            "display_name": ol_m,
            "priority": 3,
            "is_primary": False,
            "is_free": True,
            "fallback_order": idx,
            "offline_ready": True,
        }
        cascade_entries.append(entry)
        if auto_save:
            save_worker_model(**entry)
            saved_count += 1

    report["cascade"] = cascade_entries
    report["saved_count"] = saved_count
    return report


# =============================================================================
# Reporting & Formatting
# =============================================================================

def format_worker_cascade_report(cascade: Dict[str, Any]) -> str:
    """Format confirmed worker models into a clean markdown table."""
    all_models = cascade.get("all_models", [])
    if not all_models and "cascade" in cascade:
        all_models = cascade["cascade"]

    lines: List[str] = [
        "# ⚡ AegisBrain Worker Model Cascade",
        "",
        "| Priority | Tool | Model | Cost | Primary | Offline |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    if not all_models:
        lines.append("| - | *None configured* | *Run `aegis workers setup`* | - | - | - |")
    else:
        for m in all_models:
            prio = f"P{m.get('priority', '?')}"
            tool = m.get("tool_name") or m.get("tool") or "?"
            name = m.get("model_name") or m.get("model") or "?"
            cost = "$0.00 / Free" if m.get("is_free", True) else "Paid"
            primary_badge = "🌟 Yes" if m.get("is_primary") else "No"
            offline_badge = "🛡️ Offline Failover" if (m.get("priority") == 3 or m.get("offline_ready")) else "☁️ Cloud"
            lines.append(f"| `{prio}` | **{tool}** | `{name}` | `{cost}` | {primary_badge} | {offline_badge} |")

    lines.extend([
        "",
        "### 🧠 Execution Tier Protocol",
        "- **Priority 1 (OpenCode):** High-Reasoning Free Models for code generation.",
        "- **Priority 2 (Hermes):** Cloud Fallback Chain when Priority 1 is busy or rate-limited.",
        "- **Priority 3 (Ollama):** Strictly for offline failover (`qwen2.5-coder:7b`). Preserves workstation RAM.",
    ])

    return "\n".join(lines)


# =============================================================================
# Fast-Path Testing (< 1s In-Memory AST + Scoped Pytest)
# =============================================================================

def _run_ast_validation(file_path: Path) -> Tuple[bool, str]:
    """Parse python source into AST in-memory to verify syntax instantly."""
    try:
        source = file_path.read_text(encoding="utf-8", errors="replace")
        ast.parse(source, filename=str(file_path))
        return True, "Valid AST syntax"
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def run_fast_test(scoped_path: Optional[str] = None) -> Dict[str, Any]:
    """Execute Fast-Path in-memory AST verification and scoped pytest in < 1 second."""
    start_time = time.perf_counter()

    target_file = Path(scoped_path) if scoped_path else Path(__file__)
    if not target_file.is_absolute():
        target_file = Path.cwd() / target_file

    ast_valid, ast_msg = _run_ast_validation(target_file) if target_file.exists() else (False, "File not found")

    # Locate matching test file if target is a source file
    test_target: Optional[Path] = None
    if "test" in target_file.stem:
        test_target = target_file
    else:
        # Check standard test locations
        candidate_test = target_file.parent.parent / "tests" / f"test_{target_file.stem}.py"
        if candidate_test.exists():
            test_target = candidate_test

    pytest_output = ""
    pytest_passed = True

    if test_target and test_target.exists():
        try:
            cmd = [sys.executable, "-m", "pytest", str(test_target), "-q", "--tb=short"]
            if shutil.which("uv"):
                cmd = ["uv", "run", "pytest", str(test_target), "-q", "--tb=short"]
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10.0,
            )
            pytest_output = (res.stdout + res.stderr).strip()
            pytest_passed = (res.returncode == 0)
        except subprocess.TimeoutExpired:
            pytest_output = "Pytest execution timed out (>5.0s)"
            pytest_passed = False
        except Exception as e:
            pytest_output = f"Pytest execution error: {e}"
            pytest_passed = False
    else:
        pytest_output = f"AST syntax verified for {target_file.name}. (No scoped test file found)"

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    overall_status = "pass" if (ast_valid and pytest_passed) else "fail"

    return {
        "status": overall_status,
        "ast_valid": ast_valid,
        "ast_message": ast_msg,
        "test_target": str(test_target) if test_target else None,
        "test_output": pytest_output,
        "elapsed_ms": round(elapsed_ms, 2),
    }
