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


def fetch_github_endpoint(path: str) -> Optional[Any]:
    """Fetch GitHub REST API endpoint using standard library urllib."""
    clean_path = path.lstrip("/")
    url = f"https://api.github.com/{clean_path}"
    headers = {
        "User-Agent": "AegisBrain/1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception:
        # Ignore network / rate limit hiccups gracefully
        pass
    return None


def fetch_github_pr(repo: str, pr_number: int) -> Optional[Dict[str, Any]]:
    """Fetch pull request status from GitHub API using standard library urllib."""
    return fetch_github_endpoint(f"repos/{repo}/pulls/{pr_number}")


def notify_remote_alert(category: str, message: str) -> None:
    """Record alert in SQLite and dispatch immediate Telegram/WhatsApp push notification."""
    add_alert(category, message)
    try:
        from .remote import load_remote_config, send_remote_message
        cfg = load_remote_config()
        chat_id = cfg.get("telegram_chat_id")
        if chat_id:
            telegram_body = f"🛡️ *AegisBrain Sentinel Alert*\n\n{message}"
            send_remote_message(chat_id, telegram_body, config=cfg)
    except Exception:
        pass


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
        b_res = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if b_res.returncode == 0:
            info["branch"] = b_res.stdout.strip()

        s_res = subprocess.run(
            ["git", "-C", str(repo_dir), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=2.0,
        )
        if s_res.returncode == 0:
            info["is_dirty"] = bool(s_res.stdout.strip())

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
    """Check all tracked PRs against GitHub API and update database + alerts + Telegram push."""
    if get_current_mode() == "private":
        return []

    from .db import init_db
    init_db()
    alerts: List[str] = []
    prs = get_tracked_prs()

    for item in prs:
        repo = item["repo"]
        pr_num = item["pr_number"]
        old_status = item.get("status", "open")

        data = fetch_github_pr(repo, pr_num)
        if not data:
            continue

        raw_state = data.get("state", "open")
        is_merged = data.get("merged", False)
        labels = [l.get("name") for l in data.get("labels", []) if isinstance(l, dict) and "name" in l]
        title = data.get("title", item.get("title", ""))
        ci_status = data.get("mergeable_state", item.get("ci_status", "pending"))
        pr_url = data.get("html_url", f"https://github.com/{repo}/pull/{pr_num}")

        new_status = "merged" if is_merged else raw_state
        current_comments = data.get("comments", 0)
        current_review_comments = data.get("review_comments", 0)
        current_updated_at = data.get("updated_at", "")

        old_comments = item.get("comments_count") or 0
        old_review_comments = item.get("review_comments_count") or 0
        old_review_state = item.get("latest_review_state") or ""
        old_updated_at = item.get("updated_at") or ""

        # 1. Detect PR Status / Merge transitions
        if new_status != old_status:
            if new_status == "merged":
                msg = f"🎉 *PR MERGED!* [{repo}#{pr_num}]({pr_url})\n*{title}*\nYour contribution has been successfully merged into upstream!"
            elif new_status == "closed":
                msg = f"⛔ *PR CLOSED* [{repo}#{pr_num}]({pr_url})\n*{title}*\nPull request was closed."
            else:
                msg = f"📌 *PR Status Changed* [{repo}#{pr_num}]({pr_url})\nStatus: `{old_status}` ➔ `{new_status}`"
            notify_remote_alert("PR_STATUS", msg)
            alerts.append(msg)

        # 2. Detect Labels update
        old_labels = set(item.get("labels") or [])
        new_labels = set(labels)
        if labels and new_labels != old_labels:
            msg = f"🏷️ *PR Labels Updated* [{repo}#{pr_num}]({pr_url})\nLabels: {', '.join(labels)}"
            notify_remote_alert("PR_LABELS", msg)
            alerts.append(msg)

        # 3. Detect Formal Reviews & Approvals
        new_review_state = old_review_state
        reviews_data = fetch_github_endpoint(f"repos/{repo}/pulls/{pr_num}/reviews")
        if isinstance(reviews_data, list) and reviews_data:
            # Filter out self-reviews by user to avoid self-notification noise
            external_reviews = [
                r for r in reviews_data
                if r.get("state") not in ("DISMISSED", "PENDING")
                and r.get("user", {}).get("login", "").lower() != "pg300604"
            ]
            if external_reviews:
                latest_rev = external_reviews[-1]
                rev_state = latest_rev.get("state", "").upper()
                rev_user = latest_rev.get("user", {}).get("login", "maintainer")
                rev_body = (latest_rev.get("body") or "").strip()

                if rev_state and rev_state != old_review_state:
                    new_review_state = rev_state
                    if rev_state == "APPROVED":
                        msg = f"✅ *PR APPROVED!* [{repo}#{pr_num}]({pr_url})\nReviewer: @{rev_user}\n{('> ' + rev_body[:250]) if rev_body else 'Approved for merge!'}"
                    elif rev_state == "CHANGES_REQUESTED":
                        msg = f"⚠️ *Changes Requested* [{repo}#{pr_num}]({pr_url})\nReviewer: @{rev_user}\n> {rev_body[:300] if rev_body else 'Maintainer requested revisions.'}"
                    else:
                        msg = f"📝 *Review Submitted ({rev_state})* [{repo}#{pr_num}]({pr_url})\nReviewer: @{rev_user}\n> {rev_body[:300] if rev_body else ''}"
                    notify_remote_alert("PR_REVIEW", msg)
                    alerts.append(msg)

        # 4. Detect General Comments
        if current_comments > old_comments:
            diff_comments = current_comments - old_comments
            comments_data = fetch_github_endpoint(f"repos/{repo}/issues/{pr_num}/comments?sort=created&direction=desc&per_page={max(1, diff_comments)}")
            if isinstance(comments_data, list) and comments_data:
                for c in comments_data[:diff_comments]:
                    c_user = c.get("user", {}).get("login", "")
                    c_body = (c.get("body") or "").strip()
                    if c_user.lower() != "pg300604":
                        msg = f"💬 *New Comment on PR* [{repo}#{pr_num}]({pr_url})\nFrom: @{c_user}\n> {c_body[:350]}"
                        notify_remote_alert("PR_COMMENT", msg)
                        alerts.append(msg)

        # 5. Detect Code Review Inline Comments
        if current_review_comments > old_review_comments:
            diff_rc = current_review_comments - old_review_comments
            rc_data = fetch_github_endpoint(f"repos/{repo}/pulls/{pr_num}/comments?sort=created&direction=desc&per_page={max(1, diff_rc)}")
            if isinstance(rc_data, list) and rc_data:
                for rc in rc_data[:diff_rc]:
                    rc_user = rc.get("user", {}).get("login", "")
                    rc_path = rc.get("path", "")
                    rc_body = (rc.get("body") or "").strip()
                    if rc_user.lower() != "pg300604":
                        msg = f"🔍 *Code Review Comment* [{repo}#{pr_num}]({pr_url})\nFrom @{rc_user} on `{rc_path}`:\n> {rc_body[:350]}"
                        notify_remote_alert("PR_INLINE_COMMENT", msg)
                        alerts.append(msg)

        # Persist updated state
        track_pr(
            repo=repo,
            pr_number=pr_num,
            title=title,
            status=new_status,
            labels=labels,
            ci_status=ci_status,
            comments_count=current_comments,
            review_comments_count=current_review_comments,
            latest_review_state=new_review_state,
            updated_at=current_updated_at,
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

            # Periodically drain queued Telegram mobile links & reels when host is idle
            try:
                from .telegram_queue import TelegramQueue
                tq = TelegramQueue()
                tq.drain(idle_only=True, max_items=3)
            except Exception:
                pass

            # Check and drain execution queue if terminal is idle/ready for next prompt
            try:
                from .remote import is_terminal_busy, drain_execution_queue, get_execution_queue_count
                if not is_terminal_busy() and get_execution_queue_count() > 0:
                    drain_execution_queue()
            except Exception:
                pass

            self._stop_event.wait(self.interval)
