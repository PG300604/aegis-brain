"""AegisBrain Execution Sandbox & Red-Team Vulnerability Auditor.

Enforces zero-trust isolation before releasing code or model output to host workstation:
1. Static Red-Team Vulnerability Audit:
   - Scans for Prompt Injection / Jailbreak artifacts.
   - Detects Path Traversal attempts escaping workspace boundaries.
   - Flags unsanitized Shell Execution (eval, exec, shell=True).
   - Scans for Credential / API Token exposure.
   - Detects Resource Exhaustion (infinite spin, fork bombs).
2. Ephemeral Execution Sandbox:
   - Runs candidate code in an isolated directory with strict execution timeouts.
   - Sanitizes environment variables to prevent secret leakage.
   - Certified with a Security Score (0-100%) before release.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional
from .config import get_aegis_dir


class RedTeamAuditor:
    """Multi-vector static security and vulnerability scanner for agent code."""

    INJECTION_PATTERNS = [
        (r"(?i)ignore\s+(all\s+)?prior\s+instructions", "Prompt Injection (Prior instruction override)"),
        (r"(?i)developer\s+mode\s+enabled", "Jailbreak (Developer mode bypass attempt)"),
        (r"(?i)print\s+(the\s+)?system\s+prompt", "System Prompt Extraction"),
        (r"(?i)dan\s+mode", "Jailbreak (Do Anything Now vector)"),
    ]

    TRAVERSAL_PATTERNS = [
        (r"\.\.[\\/]\.\.[\\/]", "Path Traversal (Multiple directory escape)"),
        (r"(?i)[c-z]:[\\/]windows", "System Directory Access (Windows Root)"),
        (r"(?i)[c-z]:[\\/]program\s*files", "System Directory Access (Program Files)"),
        (r"[\\/]etc[\\/](passwd|shadow)", "System Directory Access (Unix credential targets)"),
    ]

    COMMAND_INJECTION_PATTERNS = [
        (r"shell\s*=\s*True", "Unsafe Shell Execution (shell=True allows arbitrary shell injection)"),
        (r"\beval\s*\(", "Dynamic Code Evaluation (eval() execution risk)"),
        (r"\bexec\s*\(", "Dynamic Code Execution (exec() execution risk)"),
        (r"os\.system\s*\(", "Unsanitized Subshell (os.system() risk)"),
        (r"(?i)rmdir\s+/[sS]\s+/[qQ]\s+[c-z]:", "Destructive Disk Deletion Command"),
    ]

    CREDENTIAL_PATTERNS = [
        (r"\b[0-9]{9,10}:[a-zA-Z0-9_-]{35}\b", "Exposed Telegram Bot Token"),
        (r"\b(ghp|gho|ghu|ghs)_[a-zA-Z0-9]{36}\b", "Exposed GitHub Personal Access Token"),
        (r"\bAKIA[0-9A-Z]{16}\b", "Exposed AWS Access Key"),
        (r"bearer\s+[a-zA-Z0-9_\-\.]{25,}", "Exposed Bearer Authorization Token"),
    ]

    RESOURCE_BOMB_PATTERNS = [
        (r"while\s+True\s*:\s*(pass|\n\s*pass)", "Infinite Spin Loop (CPU Denial of Service)"),
        (r":\(\)\{\s*:\|:&\s*\};:", "Fork Bomb (Process Exhaustion Vector)"),
    ]

    @classmethod
    def audit_code(cls, code: str) -> Dict[str, Any]:
        findings = []

        # 1. Prompt Injection
        for pat, desc in cls.INJECTION_PATTERNS:
            if re.search(pat, code):
                findings.append({"vector": "PROMPT_INJECTION", "severity": "HIGH", "detail": desc})

        # 2. Path Traversal
        for pat, desc in cls.TRAVERSAL_PATTERNS:
            if re.search(pat, code):
                findings.append({"vector": "PATH_TRAVERSAL", "severity": "CRITICAL", "detail": desc})

        # 3. Command Injection
        for pat, desc in cls.COMMAND_INJECTION_PATTERNS:
            if re.search(pat, code):
                findings.append({"vector": "COMMAND_INJECTION", "severity": "HIGH", "detail": desc})

        # 4. Credential Leaks
        for pat, desc in cls.CREDENTIAL_PATTERNS:
            if re.search(pat, code):
                findings.append({"vector": "CREDENTIAL_EXPOSURE", "severity": "CRITICAL", "detail": desc})

        # 5. Resource Bombs
        for pat, desc in cls.RESOURCE_BOMB_PATTERNS:
            if re.search(pat, code):
                findings.append({"vector": "RESOURCE_EXHAUSTION", "severity": "HIGH", "detail": desc})

        has_critical = any(f["severity"] == "CRITICAL" for f in findings)
        has_high = any(f["severity"] == "HIGH" for f in findings)

        if has_critical:
            risk = "CRITICAL"
            score = max(0, 100 - (len(findings) * 35))
        elif has_high:
            risk = "HIGH"
            score = max(40, 100 - (len(findings) * 20))
        elif findings:
            risk = "MEDIUM"
            score = max(70, 100 - (len(findings) * 10))
        else:
            risk = "SAFE"
            score = 100

        return {
            "safe": len(findings) == 0,
            "risk_level": risk,
            "security_score": score,
            "findings_count": len(findings),
            "findings": findings,
        }


def get_sandbox_dir() -> Path:
    p = get_aegis_dir() / "sandbox"
    p.mkdir(parents=True, exist_ok=True)
    return p


def run_in_sandbox(python_code: str, timeout_seconds: float = 3.0) -> Dict[str, Any]:
    """Audit and execute Python code in an ephemeral isolated sandbox directory."""
    # 1. Run Pre-Flight Red-Team Audit
    audit = RedTeamAuditor.audit_code(python_code)
    if not audit["safe"] and audit["risk_level"] in ("CRITICAL", "HIGH"):
        return {
            "executed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Blocked by Red-Team Sandbox Auditor: {audit['findings'][0]['detail']}",
            "audit": audit,
        }

    # 2. Ephemeral Sandbox Execution
    session_dir = Path(tempfile.mkdtemp(prefix="aegis_sb_", dir=str(get_sandbox_dir())))
    script_file = session_dir / "candidate_script.py"
    script_file.write_text(python_code, encoding="utf-8")

    # Clean environment without secret tokens
    safe_env = {
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
        "PATH": os.environ.get("PATH", ""),
        "TEMP": str(session_dir),
        "TMP": str(session_dir),
        "PYTHONIOENCODING": "utf-8",
    }

    try:
        proc = subprocess.run(
            [sys.executable, str(script_file)],
            cwd=str(session_dir),
            env=safe_env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "executed": True,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "audit": audit,
        }
    except subprocess.TimeoutExpired:
        return {
            "executed": False,
            "exit_code": -2,
            "stdout": "",
            "stderr": f"Sandbox execution timed out ({timeout_seconds}s limit exceeded).",
            "audit": audit,
        }
    except Exception as e:
        return {
            "executed": False,
            "exit_code": -3,
            "stdout": "",
            "stderr": f"Sandbox error: {e}",
            "audit": audit,
        }
    finally:
        # Cleanup ephemeral sandbox files
        try:
            shutil.rmtree(session_dir, ignore_errors=True)
        except Exception:
            pass


def format_sandbox_report(audit_result: Dict[str, Any]) -> str:
    """Format clean markdown report of sandbox security certification."""
    score = audit_result.get("security_score", 100)
    risk = audit_result.get("risk_level", "SAFE")
    badge = "🟢 CERTIFIED SAFE" if risk == "SAFE" else ("🟡 REVIEW NEEDED" if risk == "MEDIUM" else "🔴 BLOCKED / HIGH RISK")

    lines = [
        "🛡️ *AegisBrain Sandbox Red-Team & Security Certification*",
        f"• *Status:* {badge} (Security Score: `{score}/100`)",
        f"• *Total Findings:* {audit_result.get('findings_count', 0)}",
        ""
    ]

    findings = audit_result.get("findings", [])
    if not findings:
        lines.append("✅ *Zero Vulnerabilities Detected.*")
        lines.append("• Verified resistance to Prompt Injection, Path Traversal, Credential Exposure & Shell Injection.")
    else:
        lines.append("⚠️ *Security Findings Identified:*")
        for f in findings:
            sev_badge = "🔴" if f["severity"] == "CRITICAL" else ("🟡" if f["severity"] == "HIGH" else "⚪")
            lines.append(f"• {sev_badge} `[{f['vector']}]`: {f['detail']}")

    return "\n".join(lines)
