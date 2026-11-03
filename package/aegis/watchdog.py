import json
import os
import subprocess
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from .config import DEFAULT_OPEN_SOURCE_ROOT, get_current_mode
from .db import add_alert, get_tracked_prs, track_pr


def fetch_github_pr(repo: str, pr_number: int) -> Optional[Dict[str, Any]]:
    """Fetch pull request status from GitHub API using standard library urllib."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "User-Agent": "AegisBrain/1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        # Ignore network/rate limit hiccups gracefully
        pass
    return None


def inspect_git_repo_status(repo_dir: Path) -> Optional[Dict[str, Any]]:
    """Inspect local git repository for dirty working tree or unpushed commits."""
    if not (repo_dir / ".git").exists():
        return None

    info = {
        "name": repo_dir.name,
        "path": str(repo_dir),
        "branch": "unknown",
        "is_dirty": False,
        "unpushed_count": 0,
    }

    try:
        # Branch
        b_res = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if b_res.returncode == 0:
            info["branch"] = b_res.stdout.strip()

        # Status
        s_res = subprocess.run(
            ["git", "-C", str(repo_dir), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if s_res.returncode == 0:
            info["is_dirty"] = bool(s_res.stdout.strip())

        # Unpushed commits compared to upstream
        u_res = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-list", "@{u}..HEAD", "--count"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if u_res.returncode == 0:
            try:
                info["unpushed_count"] = int(u_res.stdout.strip())
            except ValueError:
                pass
    except Exception:
        pass

    return info


def sweep_tracked_prs() -> List[str]:
    """Check all tracked PRs against GitHub API and update database + alerts."""
    if get_current_mode() == "private":
        return []

    alerts: List[str] = []
    prs = get_tracked_prs()

    for item in prs:
        repo = item["repo"]
        pr_num = item["pr_number"]
        old_status = item["status"]

        data = fetch_github_pr(repo, pr_num)
        if not data:
            continue

        raw_state = data.get("state", "open")
        is_merged = data.get("merged", False)
        labels = [l.get("name") for l in data.get("labels", []) if isinstance(l, dict) and "name" in l]
        title = data.get("title", item["title"])

        new_status = "merged" if is_merged else raw_state
        ci_status = data.get("mergeable_state", item.get("ci_status", "pending"))

        # Detect changes
        if new_status != old_status:
            msg = f"PR {repo}#{pr_num} transitioned from '{old_status}' to '{new_status}'."
            add_alert("PR_STATUS", msg)
            alerts.append(msg)

        # Detect review comments or labels added
        if labels and set(labels) != set(item.get("labels") or []):
            msg = f"PR {repo}#{pr_num} labels updated: {', '.join(labels)}"
            add_alert("PR_LABELS", msg)
            alerts.append(msg)

        track_pr(
            repo=repo,
            pr_number=pr_num,
            title=title,
            status=new_status,
            labels=labels,
            ci_status=ci_status,
        )

    return alerts


def sweep_local_repos(root: Path = DEFAULT_OPEN_SOURCE_ROOT) -> List[str]:
    """Scan repositories in open-source directory for dirty state."""
    if not root.exists():
        return []

    alerts: List[str] = []
    for item in root.iterdir():
        if item.is_dir() and (item / ".git").exists():
            status = inspect_git_repo_status(item)
            if status and status["is_dirty"]:
                msg = f"Repo '{item.name}' on branch '{status['branch']}' has uncommitted changes."
                alerts.append(msg)

    return alerts


class WatchdogRunner:
    """Background daemon thread that periodically checks PRs and git state."""

    def __init__(self, interval_seconds: int = 300):
        self.interval = interval_seconds
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="AegisWatchdog")
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                sweep_tracked_prs()
            except Exception:
                pass
            self._stop_event.wait(self.interval)
