"""AegisBrain Offline Briefing & Session Synchronization Engine.

Automatically triggered whenever the user says 'hi', 'hello', or begins a new session:
1. Greets the user based on the current time of day.
2. Checks all background activity, tracked PRs, reviews, and offline updates.
3. Summarizes pending tasks, open alerts, and recent repository commits.
4. Dynamically retrieves recent milestones, completed tasks, and fresh community trends from neural memory DB.
5. Asks what to prioritize next so the user can steer instantly.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from .db import (
    get_active_alerts,
    get_recent_decisions,
    get_tracked_prs,
    init_db,
)
from .config import get_current_mode
from .caffeinate import get_caffeinate_status
from .snapshot import list_snapshots
from .task_lifecycle import list_active_tasks, get_task_history
from .creator_intel import get_recent_trends


class OfflineBriefingEngine:
    """Compiles a high-signal briefing of offline events, reviews, and pending work."""

    @classmethod
    def get_greeting_salutation(cls, user_name: Optional[str] = None) -> str:
        name = user_name or os.environ.get("AEGIS_USER_NAME") or os.environ.get("USERNAME") or os.environ.get("USER") or "Developer"
        hour = datetime.now().hour
        if 5 <= hour < 12:
            time_str = "Good morning"
        elif 12 <= hour < 17:
            time_str = "Good afternoon"
        elif 17 <= hour < 22:
            time_str = "Good evening"
        else:
            time_str = "Late night greetings"
        return f"{time_str}, {name}!"

    @classmethod
    def generate_briefing(cls, user_name: Optional[str] = None) -> str:
        name = user_name or os.environ.get("AEGIS_USER_NAME") or os.environ.get("USERNAME") or os.environ.get("USER") or "Developer"
        init_db()

        # Zero-prompt auto-resurrect of background AegisBrain daemon & Telegram listener
        try:
            from .service import is_daemon_running, start_daemon
            if not is_daemon_running():
                start_daemon()
        except Exception:
            pass

        salutation = cls.get_greeting_salutation(name)
        mode = get_current_mode()
        caff = get_caffeinate_status()
        tracked_prs = get_tracked_prs()
        alerts = get_active_alerts()
        recent_decisions = get_recent_decisions(limit=5)
        snapshots = list_snapshots()[:3]
        active_tasks = list_active_tasks()
        task_history = get_task_history(limit=5)
        recent_trends = get_recent_trends(limit=4)

        # 1. Tracked PRs & Code Reviews
        pr_lines: List[str] = []
        for pr in tracked_prs:
            rev_badge = f" &bull; Review: `{pr.get('latest_review_state')}`" if pr.get("latest_review_state") else ""
            pr_lines.append(f"- 🐙 **[{pr['repo']}#{pr['pr_number']}]({pr.get('html_url', '#')})**: {pr['title']} (`{pr['status'].upper()}`{rev_badge})")
        if not pr_lines:
            pr_lines.append("- No external PRs currently blocking.")

        # 2. Open Alerts & Reviews
        alert_lines: List[str] = []
        for a in alerts[:4]:
            category = a.get("category", "ALERT")
            msg = a.get("message", "")
            # Truncate first line for clean briefing
            short_msg = msg.split("\n")[0] if "\n" in msg else msg
            alert_lines.append(f"- ⚠️ **{category}**: {short_msg[:120]}...")
        if not alert_lines:
            alert_lines.append("- All systems nominal. Zero unaddressed critical alerts.")

        # 3. Dynamic Recent Milestones & Completed Tasks (from Neural Memory & DB)
        completed_lines: List[str] = []

        # A. Include recent architectural decisions & session handoffs
        for d in recent_decisions:
            d_title = d.get("title", "")
            d_dec = d.get("decision", "")
            d_cat = d.get("category", "GENERAL")
            if d_dec:
                short_dec = d_dec.split("\n")[0] if "\n" in d_dec else d_dec
                completed_lines.append(f"- 🧠 **{d_title}** [{d_cat}]: {short_dec[:140]}")
            if len(completed_lines) >= 3:
                break

        # B. Include recent completed tasks from task history
        for t in task_history:
            if len(completed_lines) >= 5:
                break
            t_title = t.get("title", "")
            t_outcome = t.get("outcome") or "Completed and verified."
            completed_lines.append(f"- ✅ **{t_title}**: {t_outcome}")

        # Fallback only if no dynamic history exists
        if not completed_lines:
            completed_lines = [
                "- ✅ **System Baseline Initialized**: Neural memory ready and operational.",
            ]

        # 4. Snapshots & Restore Point Info
        if snapshots:
            snap_id = snapshots[0]["snapshot_id"]
            reason = snapshots[0].get("reason", "manual")
            latest_snap_str = f"`{snap_id}` ({reason})"
        else:
            latest_snap_str = "`None`"

        # 5. Fresh Community & Tech Radar Trends
        trend_lines: List[str] = []
        for tr in recent_trends:
            src = tr.get("source", "Radar")
            title = tr.get("title", "")
            url = tr.get("url", "#")
            score = tr.get("score", 0)
            score_str = f" (+{score})" if score else ""
            trend_lines.append(f"- 🔥 **[{src}]** [{title}]({url}){score_str}")
        if not trend_lines:
            trend_lines.append("- Radar nominal. Zero external breaking updates detected.")

        # 6. Dynamic Suggested Priorities for Today
        priority_lines: List[str] = []
        # Priority from active tasks
        for t in active_tasks[:2]:
            priority_lines.append(f"**Task #{t['id']} ({t['title']})**: {t.get('description') or 'Continue execution.'}")
        # Priority from tracked PRs with alerts
        for pr in tracked_prs:
            if pr.get("status") == "open":
                priority_lines.append(f"**{pr['repo']} PR #{pr['pr_number']}**: Address review comments on '{pr['title']}'.")
                break
        # Priority from latest handoff or decision
        if recent_decisions:
            top_dec = recent_decisions[0]
            if "handoff" in top_dec.get("title", "").lower() or "handoff" in str(top_dec.get("tags", "")).lower():
                priority_lines.append(f"**Resume Handoff ({top_dec['title']})**: {top_dec['decision'][:80]}...")

        # Roadmap fallbacks to ensure 3-4 actionable choices
        default_priorities = [
            "**Personal Lightweight AI Agent**: Design and build your personal desktop agent on drive `P:\\`.",
            "**Chrome Web Store Release**: Finalize store submission package and listing metadata.",
            "**GitGuardian Secret Remediation**: Review and rotate flagged historical credentials.",
        ]
        for dp in default_priorities:
            if len(priority_lines) < 4:
                prefix = dp.split(":")[0]
                if not any(prefix in p for p in priority_lines):
                    priority_lines.append(dp)

        numbered_priorities = "\n".join(f"{idx}. {item}" for idx, item in enumerate(priority_lines[:4], 1))

        # Format Final Markdown Output
        return f"""
# 🌅 {salutation} Welcome Back to AegisBrain!

> **System State**: Mode: `{mode.upper()}` &bull; Caffeinate: `{'ACTIVE' if caff.get('active') else 'OFF'}` &bull; Latest Restore Point: {latest_snap_str}

---

### 📌 Completed in Last Session
{chr(10).join(completed_lines)}

### 🌐 Fresh Community & Tech Radar
{chr(10).join(trend_lines)}

### 📬 Offline Updates & External Feedback
{chr(10).join(pr_lines)}

### ⚠️ Active Attention Items
{chr(10).join(alert_lines)}

---

### ❓ What would you like to tackle today?
{numbered_priorities}
""".strip()
