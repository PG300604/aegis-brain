import json
import os
import shutil
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path

# Override environment BEFORE any aegis module is loaded
TEST_TMP = Path(tempfile.mkdtemp(prefix="aegis_test_"))
os.environ["AEGIS_DIR"] = str(TEST_TMP)
os.environ["AEGIS_MODE"] = "public"

from aegis import config
from aegis.db import (
    get_recent_decisions,
    get_tracked_prs,
    init_db,
    record_decision,
    record_session,
    search_memories,
    track_pr,
)
from aegis.distiller import distill_rules_for_prompt
from aegis.governor import generate_active_context
from aegis.proxy import augment_chat_completion_payload
from aegis.server import create_server


class TestAegisBrain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        track_pr(
            repo="spring-projects/spring-ai",
            pr_number=7308,
            title="Add missing GenAI request attributes to observations",
            status="open",
            labels=["status: waiting-for-triage"],
            ci_status="dco-passed",
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_TMP, ignore_errors=True)

    def setUp(self):
        config.set_current_mode("public")

    def test_record_and_search_decision(self):
        row_id = record_decision(
            category="TESTING",
            title="Fast Execution Protocol",
            decision="Use in-memory SQLite and mock network requests for instant tests.",
            rationale="Sub-second test feedback prevents regressions.",
            tags=["unit-test", "performance"],
        )
        self.assertIsNotNone(row_id)

        # FTS5 search
        matches = search_memories("Sub-second")
        self.assertGreaterEqual(len(matches), 1)
        self.assertEqual(matches[0]["title"], "Fast Execution Protocol")

    def test_private_mode_bypass(self):
        config.set_current_mode("private")
        self.assertEqual(config.get_current_mode(), "private")

        res_session = record_session("priv-1", "agent-x", str(TEST_TMP))
        self.assertFalse(res_session)

        res_decision = record_decision(
            category="STEALTH",
            title="Confidential Discovery",
            decision="Secret algorithm payload",
        )
        self.assertIsNone(res_decision)

        # Verify not in DB
        matches = search_memories("Confidential")
        self.assertEqual(len(matches), 0)

    def test_pr_tracking(self):
        prs = get_tracked_prs()
        self.assertGreaterEqual(len(prs), 1)
        target = [p for p in prs if p["pr_number"] == 7308][0]
        self.assertEqual(target["ci_status"], "dco-passed")

    def test_context_generation(self):
        ctx = generate_active_context(TEST_TMP)
        self.assertIn("# Aegis Brain Active Context", ctx)
        self.assertIn("spring-projects/spring-ai#7308", ctx)
        self.assertTrue(config.get_active_context_path().exists())

    def test_distiller(self):
        # Java Spring prompt
        rules_spring = distill_rules_for_prompt("Fix Spring AI observation metrics for OpenTelemetry")
        self.assertIn("JAVA_SPRING", rules_spring)
        self.assertIn("KARPATHY_SIMPLICITY", rules_spring)

        # Python FastAPI prompt
        rules_py = distill_rules_for_prompt("Build a python fastapi microservice")
        self.assertIn("PYTHON_FAST", rules_py)

    def test_proxy_payload_augmentation(self):
        body = {
            "model": "qwen2.5-coder:7b",
            "messages": [
                {"role": "user", "content": "Help me implement a Spring observation convention"}
            ]
        }
        augmented = augment_chat_completion_payload(body)
        messages = augmented["messages"]
        self.assertEqual(messages[0]["role"], "system")
        self.assertIn("Aegis Brain Active Context", messages[0]["content"])
        self.assertIn("JAVA_SPRING", messages[0]["content"])

    def test_http_server_endpoints(self):
        record_decision(
            category="TESTING",
            title="Fast Execution Server Test",
            decision="Test HTTP endpoint for search.",
        )
        # Run test server on ephemeral port 9876
        server = create_server(host="127.0.0.1", port=9876)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        time.sleep(0.1)

        try:
            # 1. /health
            req = urllib.request.Request("http://127.0.0.1:9876/health")
            with urllib.request.urlopen(req, timeout=2.0) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode("utf-8"))
                self.assertEqual(data["service"], "aegis-brain")

            # 2. /bootstrap
            req_b = urllib.request.Request("http://127.0.0.1:9876/bootstrap")
            with urllib.request.urlopen(req_b, timeout=2.0) as res:
                self.assertEqual(res.status, 200)
                body = res.read().decode("utf-8")
                self.assertIn("Aegis Brain Active Context", body)

            # 3. /search
            req_s = urllib.request.Request("http://127.0.0.1:9876/search?q=Fast")
            with urllib.request.urlopen(req_s, timeout=2.0) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode("utf-8"))
                self.assertGreaterEqual(data["count"], 1)

        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
