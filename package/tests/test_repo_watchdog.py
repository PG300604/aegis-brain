"""Unit tests for repository-level PR auto-discovery and watchdog sweeping."""

import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

PACKAGE_DIR = Path(__file__).resolve().parent.parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from aegis import config, watchdog  # noqa: E402
from aegis.briefing import OfflineBriefingEngine  # noqa: E402
from aegis.db import (  # noqa: E402
    get_active_alerts,
    get_tracked_prs,
    get_tracked_repos,
    init_db,
    untrack_pr,
    unwatch_repo,
    watch_repo,
)
from aegis.server import create_server  # noqa: E402


class TestRepoWatchdog(unittest.TestCase):
    _test_tmp: Path = Path()
    _prev_aegis_dir: str | None = None
    _prev_aegis_mode: str | None = None

    @classmethod
    def setUpClass(cls):
        cls._prev_aegis_dir = os.environ.get("AEGIS_DIR")
        cls._prev_aegis_mode = os.environ.get("AEGIS_MODE")
        cls._test_tmp = Path(tempfile.mkdtemp(prefix="aegis_repo_watch_"))
        os.environ["AEGIS_DIR"] = str(cls._test_tmp)
        os.environ["AEGIS_MODE"] = "public"
        init_db()

    @classmethod
    def tearDownClass(cls):
        if cls._prev_aegis_dir is None:
            os.environ.pop("AEGIS_DIR", None)
        else:
            os.environ["AEGIS_DIR"] = cls._prev_aegis_dir
        if cls._prev_aegis_mode is None:
            os.environ.pop("AEGIS_MODE", None)
        else:
            os.environ["AEGIS_MODE"] = cls._prev_aegis_mode
        shutil.rmtree(cls._test_tmp, ignore_errors=True)

    def setUp(self):
        config.set_current_mode("public")
        for r in get_tracked_repos():
            unwatch_repo(r["repo"])
        for pr in get_tracked_prs():
            untrack_pr(pr["repo"], pr["pr_number"])

    def test_watch_repo_monotonic_and_unwatch(self):
        watch_repo("example-org/sample-repo", last_seen_pr=14, auto_track_prs=True)
        repos = get_tracked_repos()
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0]["repo"], "example-org/sample-repo")
        self.assertEqual(repos[0]["last_seen_pr"], 14)

        # Updating without last_seen_pr or with lower PR number must not downgrade
        watch_repo("example-org/sample-repo", last_seen_pr=10, auto_track_prs=True)
        repos = get_tracked_repos()
        self.assertEqual(repos[0]["last_seen_pr"], 14)

        self.assertTrue(unwatch_repo("example-org/sample-repo"))
        self.assertEqual(get_tracked_repos(), [])

    def test_sweep_tracked_repos_discovers_new_pr_once(self):
        watch_repo("example-org/sample-repo", last_seen_pr=14, auto_track_prs=True)

        fake_open_prs = [
            {
                "number": 14,
                "title": "Previous release PR",
                "user": {"login": "alice"},
                "html_url": "https://github.com/example-org/sample-repo/pull/14",
                "labels": [],
                "comments": 0,
                "review_comments": 0,
                "updated_at": "2026-11-27T10:00:00Z",
            },
            {
                "number": 20,
                "title": "feat(hardening): handle unreadable directory permissions",
                "user": {"login": "bob"},
                "html_url": "https://github.com/example-org/sample-repo/pull/20",
                "labels": [{"name": "enhancement"}],
                "comments": 1,
                "review_comments": 0,
                "updated_at": "2026-11-28T09:00:00Z",
            },
        ]

        with patch.object(watchdog, "fetch_github_repo_prs", return_value=fake_open_prs), \
             patch("aegis.remote.send_remote_message"):
            alerts = watchdog.sweep_tracked_repos()

        self.assertEqual(len(alerts), 1)
        self.assertIn("example-org/sample-repo#20", alerts[0])
        self.assertIn("@bob", alerts[0])

        # PR #20 should be auto-tracked and last_seen_pr updated to 20
        tracked_nums = {p["pr_number"] for p in get_tracked_prs() if p["repo"] == "example-org/sample-repo"}
        self.assertIn(20, tracked_nums)
        self.assertNotIn(14, tracked_nums)
        self.assertEqual(get_tracked_repos()[0]["last_seen_pr"], 20)

        # Active alert recorded
        active_alerts = get_active_alerts()
        self.assertTrue(any(a["category"] == "REPO_NEW_PR" and "#20" in a["message"] for a in active_alerts))

        # Second sweep with same PR list produces 0 duplicate alerts
        with patch.object(watchdog, "fetch_github_repo_prs", return_value=fake_open_prs), \
             patch("aegis.remote.send_remote_message"):
            second_alerts = watchdog.sweep_tracked_repos()
        self.assertEqual(second_alerts, [])

    def test_briefing_and_http_endpoints(self):
        watch_repo("example-org/sample-repo", last_seen_pr=14, auto_track_prs=True)
        with patch("aegis.service.is_daemon_running", return_value=True):
            briefing_text = OfflineBriefingEngine.generate_briefing("Developer")
        self.assertIn("Watching repo example-org/sample-repo", briefing_text)

        server = create_server(host="127.0.0.1", port=9877)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        time.sleep(0.1)
        try:
            with urllib.request.urlopen("http://127.0.0.1:9877/tracked_repos", timeout=2.0) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode("utf-8"))
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["repo"], "example-org/sample-repo")

            req = urllib.request.Request(
                "http://127.0.0.1:9877/tracked_repos",
                data=json.dumps({"repo": "example-org/sample-repo", "action": "unwatch"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=2.0) as res:
                self.assertEqual(res.status, 200)
                resp = json.loads(res.read().decode("utf-8"))
                self.assertEqual(resp["status"], "unwatched")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
