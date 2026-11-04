"""AegisBrain Anti-Sycophancy & Skeptical Truth-Seeking Protocol.

Provides:
1. Skeptical Truth Review:
   - Actively audits code, plans, and prompts for unverified assumptions, false passes,
     mocking traps, Windows filesystem hazards, and sycophantic approval bias.
   - Rejects unproven "everything works" claims without verifiable execution evidence.
2. Mistake Ledger & Adaptive Learning:
   - Persistently logs operational mistakes, root causes, and verified fixes
     into ~/.aegis/mistakes.json so agents never repeat past errors in their environment.
3. Pre-Flight Mistake Recall:
   - Scans the environment before running commands to surface past traps
     (e.g., Windows path colon restrictions, missing python libraries, PowerShell quotes).
"""

import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class MistakeEntry:
    id: str
    timestamp: str
    task: str
    mistake_description: str
    root_cause: str
    corrective_action: str
    tags: List[str] = field(default_factory=list)


@dataclass
class SkepticalAuditResult:
    has_critical_flaws: bool
    sycophancy_detected: bool
    flaws_found: List[str]
    edge_cases_unhandled: List[str]
    counter_recommendations: List[str]
    verdict: str  # "REJECT", "WARNING", "VERIFIED_SOUND"

    def to_markdown(self) -> str:
        flaws_md = "\n".join(f"- ❌ **Flaw**: {f}" for f in self.flaws_found) or "None detected."
        edges_md = "\n".join(f"- ⚠️ **Edge**: {e}" for e in self.edge_cases_unhandled) or "None detected."
        recs_md = "\n".join(f"- 💡 {r}" for r in self.counter_recommendations) or "No changes recommended."

        return f"""
### 🛡️ Aegis Anti-Sycophancy & Truth-Seeking Audit

**Verdict**: `{self.verdict}` &bull; **Sycophancy Flag**: `{'YES (Unsubstantiated Optimism Detected)' if self.sycophancy_detected else 'NO'}`

#### 1. Identified Flaws & Vulnerabilities
{flaws_md}

#### 2. Unhandled Edge Cases & Environmental Traps
{edges_md}

#### 3. Counter-Proposals & Constructive Fixes
{recs_md}
""".strip()


class SkepticalTruthReviewer:
    """Rigorous Devil's Advocate auditor that challenges code and claims."""

    SYCOPHANTIC_PHRASES = [
        "looks great", "looks perfect", "everything is working", "no bugs found",
        "100% complete", "completely flawless", "no issues at all", "all tests pass without checking"
    ]

    WINDOWS_ILLEGAL_CHARS = [':', '*', '?', '"', '<', '>', '|']

    @classmethod
    def audit_proposal_or_code(cls, text: str, context: Optional[str] = None) -> SkepticalAuditResult:
        flaws: List[str] = []
        edges: List[str] = []
        recs: List[str] = []
        text_lower = text.lower()

        # 1. Sycophancy detection
        sycophancy = any(phrase in text_lower for phrase in cls.SYCOPHANTIC_PHRASES)
        if sycophancy:
            flaws.append("Sycophantic optimism detected without backing test execution or logs.")
            recs.append("Replace vague praise with reproducible exit codes, test counts, or coverage metrics.")

        # 2. Windows NTFS filesystem traps
        # Scan quoted paths and filename string literals
        quoted_paths = re.findall(r'["\']([^"\']+\.[a-zA-Z0-9]+)["\']|["\']([^"\']*[\\/][^"\']*)["\']', text)
        all_paths = [p[0] or p[1] for p in quoted_paths]
        for p in all_paths:
            # Ignore web URLs
            if p.startswith(('http://', 'https://', 'ws://', 'wss://')):
                continue
            # Strip valid drive letter prefix like C:\ or P:/
            sanitized_p = re.sub(r'^[a-zA-Z]:[\\/]', '', p)
            for ch in cls.WINDOWS_ILLEGAL_CHARS:
                if ch in sanitized_p:
                    flaws.append(f"Windows NTFS illegal character '{ch}' detected in file path/pattern: '{p}'.")
                    edges.append("Git clone and checkout will fail with 'invalid path' on Windows.")
                    recs.append("Sanitize filenames with slugify or regex `[^a-zA-Z0-9_-]`.")
                    break
            if ".." in sanitized_p and not sanitized_p.startswith(".."):
                flaws.append(f"Trailing double-dots detected in filename: '{p}'.")
                edges.append("NTFS strips trailing dots or fails to resolve file paths.")
                recs.append("Trim trailing dots and whitespace from all generated filenames.")

        # 3. Fragile Python standard library vs 3rd party
        if "import requests" in text and "urllib" not in text:
            edges.append("Environment dependency: `requests` is often not installed in bare python environments.")
            recs.append("Prefer standard library `urllib.request` or verify dependency with `uv`.")

        # 4. Insecure / Overwriting solution files
        if "overwrite" in text_lower and ("solution" in text_lower or "leetcode" in text_lower):
            edges.append("Overwriting prior solutions destroys historical attempt data and beats progression.")
            recs.append("Use date-stamped file naming `Solution_<YYYY-MM-DD>.<ext>` to preserve progression.")

        # 5. Shell injection / Unescaped strings in PowerShell
        if 'python -c "' in text and '"' in text.replace('python -c "', ''):
            edges.append("PowerShell nested double-quotes in inline `python -c` frequently corrupt syntax.")
            recs.append("Write logic to temporary scratch script and execute via `python script.py`.")

        # Determine verdict
        if flaws:
            verdict = "REJECT"
        elif edges:
            verdict = "WARNING"
        else:
            verdict = "VERIFIED_SOUND"

        return SkepticalAuditResult(
            has_critical_flaws=bool(flaws),
            sycophancy_detected=sycophancy,
            flaws_found=flaws,
            edge_cases_unhandled=edges,
            counter_recommendations=recs,
            verdict=verdict
        )


class MistakeLedger:
    """Persistent storage and retrieval for agent learning and mistake avoidance."""

    DEFAULT_LEDGER_PATH = Path.home() / ".aegis" / "mistakes.json"

    # Pre-seeded foundational lessons learned from actual session incidents
    DEFAULT_MISTAKES = [
        MistakeEntry(
            id="win_ntfs_colon_bug",
            timestamp="2026-11-04T18:00:00Z",
            task="git checkout LeetCode-Solutions on Windows",
            mistake_description="Remote repository contained filename '3551: Minimum Swaps...java' causing checkout failure.",
            root_cause="Windows NTFS explicitly forbids colons (':') and trailing dots in filenames.",
            corrective_action="Extract blobs with `git cat-file`, sanitize slug to `3551-minimum-swaps-...`, and restructure into packages.",
            tags=["windows", "ntfs", "git", "filesystem", "leetcode"]
        ),
        MistakeEntry(
            id="bare_python_requests_missing",
            timestamp="2026-11-04T18:30:00Z",
            task="execute update_readme.py",
            mistake_description="Script threw `ModuleNotFoundError: No module named 'requests'`.",
            root_cause="Host python installation is a bare runtime without requests installed in site-packages.",
            corrective_action="Use standard library `urllib.request` and `json` to guarantee zero-dependency execution.",
            tags=["python", "dependencies", "requests", "urllib"]
        ),
        MistakeEntry(
            id="powershell_nested_quotes_syntax",
            timestamp="2026-11-04T19:00:00Z",
            task="inline python execution in PowerShell",
            mistake_description="`python -c \"...\"` failed with SyntaxError due to PowerShell quote stripping.",
            root_cause="PowerShell handles escaped quotes differently than bash/zsh, mutilating JSON or nested strings.",
            corrective_action="Save scripts to `<appDataDir>/brain/<conversation-id>/scratch/` and run `python script.py`.",
            tags=["powershell", "python", "quoting", "windows"]
        ),
        MistakeEntry(
            id="gitguardian_secret_exposure",
            timestamp="2026-11-04T20:30:00Z",
            task="repository scanning & secret hygiene",
            mistake_description="GitGuardian reported 28 secret incidents across 29 repositories.",
            root_cause="API keys and PATs were committed in git history or configuration files without pre-commit gating.",
            corrective_action="Enforce Aegis Secret Scanner / GitGuardian pre-commit hooks and rotate all exposed credentials.",
            tags=["security", "gitguardian", "secrets", "api_key", "hygiene"]
        )
    ]

    def __init__(self, ledger_path: Optional[Path] = None):
        self.ledger_path = ledger_path or self.DEFAULT_LEDGER_PATH
        self._ensure_initialized()

    def _ensure_initialized(self) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self._save_entries(self.DEFAULT_MISTAKES)

    def _load_entries(self) -> List[MistakeEntry]:
        try:
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [MistakeEntry(**item) for item in data]
        except Exception:
            return list(self.DEFAULT_MISTAKES)

    def _save_entries(self, entries: List[MistakeEntry]) -> None:
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in entries], f, indent=2)

    def record_mistake(
        self,
        task: str,
        mistake_description: str,
        root_cause: str,
        corrective_action: str,
        tags: Optional[List[str]] = None
    ) -> MistakeEntry:
        """Add a new verified mistake to the ledger for future agent learning."""
        entry_id = f"mistake_{int(datetime.now().timestamp())}"
        entry = MistakeEntry(
            id=entry_id,
            timestamp=datetime.now().isoformat(),
            task=task,
            mistake_description=mistake_description,
            root_cause=root_cause,
            corrective_action=corrective_action,
            tags=tags or []
        )
        entries = self._load_entries()
        entries.insert(0, entry)
        self._save_entries(entries)
        return entry

    def query_mistakes(self, query: str, limit: int = 5) -> List[MistakeEntry]:
        """Search relevant past mistakes by keyword or tags."""
        entries = self._load_entries()
        query_terms = [t.lower() for t in query.split()]

        scored: List[tuple[int, MistakeEntry]] = []
        for entry in entries:
            score = 0
            full_text = f"{entry.task} {entry.mistake_description} {entry.root_cause} {entry.corrective_action} {' '.join(entry.tags)}".lower()
            for term in query_terms:
                if term in full_text:
                    score += 1
            if score > 0 or not query_terms:
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def get_all(self) -> List[MistakeEntry]:
        return self._load_entries()
