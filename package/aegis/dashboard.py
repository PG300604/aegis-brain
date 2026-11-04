"""AegisBrain Feedback, Benchmarks & GUI Dashboard Engine.

Provides persistent tracking of:
- Tool performance benchmarks (tokens consumed, tokens saved, latency).
- Tool fallback occurrences (e.g. when AST graph falls back to conventional grep).
- User feedback (ratings, critique, suggestions) to drive autonomous model evolution.
- Lightweight local Web GUI & ANSI TUI Dashboard.
"""

import json
import sqlite3
import time
from typing import Any, Dict, List, Optional
from .config import get_db_path, get_current_mode
from .snapshot import list_snapshots


DASHBOARD_SCHEMA = """
CREATE TABLE IF NOT EXISTS feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    rating INTEGER DEFAULT 5,
    comment TEXT NOT NULL,
    task_ref TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS benchmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    tokens_saved INTEGER DEFAULT 0,
    latency_ms REAL DEFAULT 0.0,
    outcome TEXT DEFAULT 'success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tool_fallbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_requested TEXT NOT NULL,
    fallback_used TEXT NOT NULL,
    reason TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_dashboard_tables() -> None:
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.executescript(DASHBOARD_SCHEMA)


def record_feedback(category: str, rating: int, comment: str, task_ref: str = "") -> int:
    init_dashboard_tables()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO feedbacks (category, rating, comment, task_ref) VALUES (?, ?, ?, ?)",
            (category, rating, comment, task_ref)
        )
        conn.commit()
        return cur.lastrowid


def record_benchmark(tool_name: str, tokens_used: int, tokens_saved: int, latency_ms: float, outcome: str = "success") -> int:
    init_dashboard_tables()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO benchmarks (tool_name, tokens_used, tokens_saved, latency_ms, outcome) VALUES (?, ?, ?, ?, ?)",
            (tool_name, tokens_used, tokens_saved, latency_ms, outcome)
        )
        conn.commit()
        return cur.lastrowid


def record_tool_fallback(tool_requested: str, fallback_used: str, reason: str = "") -> int:
    init_dashboard_tables()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tool_fallbacks (tool_requested, fallback_used, reason) VALUES (?, ?, ?)",
            (tool_requested, fallback_used, reason)
        )
        conn.commit()
        return cur.lastrowid


def get_dashboard_summary() -> Dict[str, Any]:
    init_dashboard_tables()
    db_p = get_db_path()
    with sqlite3.connect(db_p) as conn:
        conn.row_factory = sqlite3.Row

        # Benchmarks
        bench_cur = conn.execute("SELECT COUNT(*), SUM(tokens_used), SUM(tokens_saved), AVG(latency_ms) FROM benchmarks")
        bench_row = bench_cur.fetchone()
        bench_count = bench_row[0] or 0
        total_tokens_used = bench_row[1] or 0
        total_tokens_saved = bench_row[2] or 0
        avg_latency = round(bench_row[3] or 0.0, 1)

        # Fallbacks
        fallbacks_cur = conn.execute("SELECT tool_requested, fallback_used, reason, created_at FROM tool_fallbacks ORDER BY id DESC LIMIT 5")
        fallbacks = [dict(r) for r in fallbacks_cur.fetchall()]

        # Feedbacks
        feedback_cur = conn.execute("SELECT category, rating, comment, task_ref, created_at FROM feedbacks ORDER BY id DESC LIMIT 5")
        feedbacks = [dict(r) for r in feedback_cur.fetchall()]

    snapshots = list_snapshots()[:5]

    return {
        "benchmarks": {
            "total_runs": bench_count,
            "tokens_used": total_tokens_used,
            "tokens_saved": total_tokens_saved,
            "avg_latency_ms": avg_latency
        },
        "fallbacks": fallbacks,
        "feedbacks": feedbacks,
        "recent_snapshots": snapshots
    }


def format_dashboard_tui() -> str:
    """Format dashboard statistics into clean ANSI text for terminal users."""
    data = get_dashboard_summary()
    b = data["benchmarks"]

    lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║           AEGISBRAIN AUTONOMOUS INTELLIGENCE DASHBOARD       ║",
        "╚══════════════════════════════════════════════════════════════╝",
        f"  Total Runs Tracked:  {b['total_runs']}",
        f"  Tokens Saved:        {b['tokens_saved']:,} tokens",
        f"  Average Latency:     {b['avg_latency_ms']} ms",
        "",
        "─── Recent Restore Points ──────────────────────────────────────"
    ]

    if not data["recent_snapshots"]:
        lines.append("  (No snapshots found. Run 'aegis snapshot create' to create one)")
    else:
        for s in data["recent_snapshots"][:3]:
            lines.append(f"  • [{s.get('snapshot_id')}] {s.get('name')} ({s.get('created_at')})")

    lines.append("")
    lines.append("─── Tool Fallback History ──────────────────────────────────────")
    if not data["fallbacks"]:
        lines.append("  (Zero fallbacks recorded — high efficiency maintained)")
    else:
        for fb in data["fallbacks"][:3]:
            lines.append(f"  • {fb['tool_requested']} ➔ {fb['fallback_used']} ({fb.get('reason', '')})")

    lines.append("")
    lines.append("─── Recent User Feedbacks ──────────────────────────────────────")
    if not data["feedbacks"]:
        lines.append("  (No feedback recorded. Run 'aegis feedback' to add critique)")
    else:
        for f in data["feedbacks"][:3]:
            stars = "★" * f.get("rating", 5)
            lines.append(f"  • [{stars}] ({f.get('category')}) {f.get('comment')}")

    lines.append("════════════════════════════════════════════════════════════════")
    return "\n".join(lines)


def render_dashboard_html() -> str:
    """Render a lightweight, dark-mode Web GUI for AegisBrain."""
    data = get_dashboard_summary()
    b = data["benchmarks"]

    snapshots_rows = "".join(
        f"<tr><td><code>{s.get('snapshot_id')}</code></td><td>{s.get('name')}</td><td>{s.get('reason')}</td><td>{s.get('created_at')}</td><td><button onclick=\"restore('{s.get('snapshot_id')}')\">Rollback</button></td></tr>"
        for s in data["recent_snapshots"]
    ) or "<tr><td colspan='5'>No snapshots recorded.</td></tr>"

    feedbacks_rows = "".join(
        f"<tr><td>{'★' * f.get('rating', 5)}</td><td><b>{f.get('category')}</b></td><td>{f.get('comment')}</td><td>{f.get('created_at')}</td></tr>"
        for f in data["feedbacks"]
    ) or "<tr><td colspan='4'>No feedback recorded yet.</td></tr>"

    fallbacks_rows = "".join(
        f"<tr><td><code>{fb.get('tool_requested')}</code></td><td><code>{fb.get('fallback_used')}</code></td><td>{fb.get('reason')}</td><td>{fb.get('created_at')}</td></tr>"
        for fb in data["fallbacks"]
    ) or "<tr><td colspan='4'>Zero tool fallbacks! All native AST tools active.</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AegisBrain Autonomous Dashboard</title>
  <style>
    :root {{ --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9; --accent: #58a6ff; --green: #2ea043; --warn: #d29922; }}
    body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 24px; }}
    h1, h2, h3 {{ color: #ffffff; margin-top: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
    .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 18px; }}
    .metric {{ font-size: 28px; font-weight: bold; color: var(--accent); margin-top: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid var(--border); font-size: 14px; }}
    th {{ background: #21262d; color: #8b949e; }}
    button {{ background: var(--accent); color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }}
    button:hover {{ opacity: 0.9; }}
    input, textarea, select {{ background: #0d1117; border: 1px solid var(--border); color: #fff; padding: 8px; border-radius: 4px; width: 100%; box-sizing: border-box; margin-bottom: 12px; }}
  </style>
</head>
<body>
  <h1>🛡️ AegisBrain Autonomous Neural Dashboard</h1>
  <p>Local Memory Bus, AST Graph Optimization, and Security Quality Gates</p>

  <div class="grid">
    <div class="card">
      <div>Tokens Saved (Arbitrage)</div>
      <div class="metric">{b['tokens_saved']:,}</div>
    </div>
    <div class="card">
      <div>Execution Runs</div>
      <div class="metric">{b['total_runs']}</div>
    </div>
    <div class="card">
      <div>Avg Agent Latency</div>
      <div class="metric">{b['avg_latency_ms']} ms</div>
    </div>
    <div class="card">
      <div>Available Snapshots</div>
      <div class="metric">{len(data['recent_snapshots'])}</div>
    </div>
  </div>

  <div class="card" style="margin-bottom: 24px;">
    <h2>💾 Restore Points & Rollback Snapshots</h2>
    <table>
      <thead>
        <tr><th>Snapshot ID</th><th>Name</th><th>Reason</th><th>Created</th><th>Action</th></tr>
      </thead>
      <tbody>{snapshots_rows}</tbody>
    </table>
  </div>

  <div class="grid">
    <div class="card">
      <h2>🔄 Tool Fallbacks (Efficiency Watchdog)</h2>
      <table>
        <thead><tr><th>Tool</th><th>Fallback</th><th>Reason</th><th>Time</th></tr></thead>
        <tbody>{fallbacks_rows}</tbody>
      </table>
    </div>

    <div class="card">
      <h2>⭐ Submit Experience Feedback</h2>
      <form action="/api/feedback" method="POST">
        <label>Category</label>
        <select name="category">
          <option value="code_quality">Code Quality & Simplicity</option>
          <option value="speed">Speed & Token Efficiency</option>
          <option value="transparency">Observer Transparency</option>
          <option value="security">Security & GitGuardian Gates</option>
        </select>
        <label>Rating (1-5 Stars)</label>
        <select name="rating">
          <option value="5">★★★★★ (Excellent)</option>
          <option value="4">★★★★☆ (Good)</option>
          <option value="3">★★★☆☆ (Acceptable)</option>
          <option value="2">★★☆☆☆ (Needs Improvement)</option>
          <option value="1">★☆☆☆☆ (Failed Expectations)</option>
        </select>
        <label>Comment / Critique</label>
        <textarea name="comment" rows="3" placeholder="Describe where the agent succeeded or what needs tuning..."></textarea>
        <button type="submit">Submit Feedback to Aegis Memory</button>
      </form>
    </div>
  </div>

  <div class="card" style="margin-top: 24px;">
    <h2>📝 Recent Feedback & Continuous Evolution</h2>
    <table>
      <thead><tr><th>Rating</th><th>Category</th><th>Comment</th><th>Date</th></tr></thead>
      <tbody>{feedbacks_rows}</tbody>
    </table>
  </div>

  <script>
    function restore(id) {{
      if (confirm("Rollback AI CLI configuration to snapshot " + id + "?")) {{
        fetch("/api/restore?id=" + encodeURIComponent(id), {{ method: "POST" }})
          .then(r => r.json())
          .then(d => {{ alert(d.message); location.reload(); }});
      }}
    }}
  </script>
</body>
</html>"""
    return html
