import unittest
import sys
import os
os.environ["PYTEST_CURRENT_TEST"] = "1"
from pathlib import Path

# Ensure package is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aegis.db import init_db
from aegis.caffeinate import (
    enable_caffeinate,
    disable_caffeinate,
    is_caffeinate_active,
    get_caffeinate_status,
)
from aegis.remote import (
    handle_remote_command,
    format_twiml_response,
    handle_twilio_webhook,
    execute_shell,
    load_remote_config,
    save_remote_config,
    send_telegram_message,
)


class TestCaffeinateAndRemote(unittest.TestCase):
    def setUp(self):
        init_db()
        disable_caffeinate()
        # Ensure test number is authorized in remote config
        self.orig_cfg = load_remote_config()
        test_cfg = dict(self.orig_cfg)
        test_cfg["allowed_numbers"] = ["whatsapp:+1234567890", "123456789"]
        test_cfg["auth_pin"] = "8765"
        save_remote_config(test_cfg)

    def tearDown(self):
        disable_caffeinate()
        save_remote_config(self.orig_cfg)

    def test_caffeinate_toggle(self):
        ok, msg = enable_caffeinate()
        self.assertTrue(ok)
        self.assertTrue(is_caffeinate_active())

        status = get_caffeinate_status()
        self.assertTrue(status["active"])
        self.assertIn("platform", status)

        ok2, msg2 = disable_caffeinate()
        self.assertTrue(ok2)
        self.assertFalse(is_caffeinate_active())

    def test_remote_help_command(self):
        res = handle_remote_command("whatsapp:+1234567890", "/help")
        self.assertIn("AegisBrain Remote Commands", res)
        self.assertIn("/status", res)
        self.assertIn("/caffeinate", res)

    def test_remote_status_command(self):
        res = handle_remote_command("whatsapp:+1234567890", "/status")
        self.assertIn("AegisBrain Workstation Status", res)
        self.assertIn("Daemon:", res)

    def test_remote_caffeinate_command(self):
        res_on = handle_remote_command("whatsapp:+1234567890", "/caffeinate on")
        self.assertIn("Caffeinate ON", res_on)
        self.assertTrue(is_caffeinate_active())

        res_off = handle_remote_command("whatsapp:+1234567890", "/caffeinate off")
        self.assertIn("Caffeinate OFF", res_off)
        self.assertFalse(is_caffeinate_active())

    def test_execute_shell_echo(self):
        res = execute_shell("echo aegis_test_ok")
        self.assertIn("aegis_test_ok", res)

    def test_webhook_handler(self):
        post_data = {
            "From": "whatsapp:+1234567890",
            "Body": "/help",
        }
        twiml = handle_twilio_webhook(post_data)
        self.assertIn("<Response>", twiml)
        self.assertIn("<Message>", twiml)
        self.assertIn("AegisBrain Remote Commands", twiml)

    def test_auth_pin_command(self):
        # Test authenticating an unauthorized number
        res = handle_remote_command("whatsapp:+9999999999", "/auth 8765")
        self.assertIn("Authentication Successful", res)

        # Test with wrong PIN
        res_fail = handle_remote_command("whatsapp:+8888888888", "/auth 0000")
        self.assertIn("Incorrect PIN", res_fail)

    def test_telegram_unconfigured(self):
        ok, msg = send_telegram_message("123456", "test", config={"telegram_token": ""})
        self.assertFalse(ok)
        self.assertIn("not configured", msg)


    def test_remote_type_and_clip(self):
        # Test /clip with text
        res_clip_set = handle_remote_command("whatsapp:+1234567890", "/clip Hello Aegis Test")
        self.assertIn("Clipboard", res_clip_set)

        # Test /clip inspection
        res_clip_get = handle_remote_command("whatsapp:+1234567890", "/clip")
        self.assertIn("PC Clipboard Contents", res_clip_get)
        self.assertIn("Hello Aegis Test", res_clip_get)

        # Test /type command
        from unittest.mock import patch
        with patch("aegis.remote.is_workstation_locked", return_value=False):
            res_type = handle_remote_command("whatsapp:+1234567890", "/type Test Prompt Injection")
            self.assertIn("Agent Input", res_type)

    def test_remote_mode_toggle(self):
        from aegis.remote import set_away_mode
        set_away_mode(False)
        # Switch to chat mode
        res_chat = handle_remote_command("whatsapp:+1234567890", "/mode chat")
        self.assertIn("Switched to CHAT", res_chat)

        # Unprefixed message should now type into desktop rather than execute shell
        from unittest.mock import patch
        with patch("aegis.remote.is_workstation_locked", return_value=False):
            res_msg = handle_remote_command("whatsapp:+1234567890", "Analyze my code architecture")
            self.assertIn("Prompt Sent", res_msg)

        # Switch back to exec mode
        res_exec = handle_remote_command("whatsapp:+1234567890", "/mode exec")
        self.assertIn("Switched to EXEC", res_exec)

    def test_remote_security_commands(self):
        from unittest.mock import patch
        
        # Test /blockinput
        res_block = handle_remote_command("whatsapp:+1234567890", "/blockinput on")
        self.assertIn("Physical Input Protection", res_block)

        # Test /alarm
        res_alarm = handle_remote_command("whatsapp:+1234567890", "/alarm")
        self.assertIn("Alert Triggered", res_alarm)

        # Test /lock with mock to avoid locking physical screen during test run
        with patch("aegis.remote.remote_lock_workstation", return_value=(True, "Workstation locked for test")):
            res_lock = handle_remote_command("whatsapp:+1234567890", "/lock")
            self.assertIn("Workstation Lock", res_lock)
            self.assertIn("Workstation locked for test", res_lock)


    def test_remote_away_mode_and_locked_execution(self):
        from unittest.mock import patch
        from aegis.remote import set_away_mode

        # 1. Shell commands execute headlessly
        res_sh = handle_remote_command("whatsapp:+1234567890", "python -c \"print('remote_exec_test')\"")
        self.assertIn("Command Output", res_sh)
        self.assertIn("remote_exec_test", res_sh)

        # 2. In locked state with blocked desktop, /type queues safely rather than crashing or dropping
        with patch("aegis.remote.type_to_desktop", return_value=(False, "Workstation is locked")), \
             patch("aegis.remote.is_workstation_locked", return_value=True):
            res_type_locked = handle_remote_command("whatsapp:+1234567890", "/type echo locked_run")
            self.assertIn("Workstation Screen Locked", res_type_locked)

        # 3. Clean away mode toggle
        set_away_mode(True)
        res_away_off = handle_remote_command("whatsapp:+1234567890", "/away off")
        self.assertIn("Away Mode OFF", res_away_off)

    def test_telegram_inbox_persistence(self):
        from aegis.db import (
            record_telegram_message,
            get_pending_telegram_messages,
            mark_telegram_message_processed,
            get_recent_telegram_messages,
        )
        import time
        test_uid = int(time.time() * 1000)
        row_id = record_telegram_message(
            update_id=test_uid,
            chat_id="2119188945",
            text="Analyze my code architecture",
            sender_username="testuser",
            sender_name="Test User",
            message_id=42,
        )
        self.assertGreater(row_id, 0)

        pending = get_pending_telegram_messages(limit=10)
        found = [p for p in pending if p["update_id"] == test_uid]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["text"], "Analyze my code architecture")
        self.assertEqual(found[0]["status"], "pending")

        mark_telegram_message_processed(test_uid, result_summary="Analysis completed via AST engine")
        recent = get_recent_telegram_messages(limit=10)
        found_recent = [r for r in recent if r["update_id"] == test_uid]
        self.assertEqual(len(found_recent), 1)
        self.assertEqual(found_recent[0]["status"], "processed")
        self.assertIn("AST engine", found_recent[0]["result_summary"])

    def test_btw_in_flight_command(self):
        res_empty = handle_remote_command("whatsapp:+1234567890", "/btw")
        self.assertIn("In-Flight By-The-Way Query", res_empty)

        res_query = handle_remote_command("whatsapp:+1234567890", "/btw how is CPU load?")
        self.assertIn("[In-Flight Query", res_query)
        self.assertIn("Session:", res_query)

    def test_alt_m_and_in_flight_typing(self):
        from aegis.remote import type_to_desktop
        ok, msg = type_to_desktop("refactor engine /alt+m", press_enter=True)
        self.assertTrue(ok)
        self.assertIn("Alt+M in-flight", msg)
        self.assertIn("refactor engine", msg)

        res_alt = handle_remote_command("whatsapp:+1234567890", "/alt+m")
        self.assertIn("In-Flight Signal Sent", res_alt)

        res_type_alt = handle_remote_command("whatsapp:+1234567890", "/type speed up build /alt+m")
        self.assertIn("Agent Input", res_type_alt)
        self.assertIn("Alt+M in-flight", res_type_alt)

    def test_handle_incoming_document(self):
        import tempfile
        from aegis.remote import handle_incoming_document
        with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as f:
            f.write("def sample_test():\n    return 42\n")
            f_path = Path(f.name)
        try:
            res_doc = handle_incoming_document(
                chat_id="123456789",
                doc_path=f_path,
                filename="sample.py",
                mime_type="text/x-python",
                caption="Please review this test function",
            )
            self.assertIn("Document Received on Desktop", res_doc)
            self.assertIn("sample.py", res_doc)
            self.assertIn("sample_test", res_doc)
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_handle_incoming_voice(self):
        import tempfile
        from aegis.remote import handle_incoming_voice
        with tempfile.NamedTemporaryFile("wb", suffix=".oga", delete=False) as f:
            f.write(b"OggS dummy voice bytes")
            f_path = Path(f.name)
        try:
            res_voice = handle_incoming_voice(
                chat_id="123456789",
                audio_path=f_path,
            )
            self.assertTrue(len(res_voice) > 0)
        finally:
            if f_path.exists():
                f_path.unlink()


    def test_staged_desktop_prompt_queue_and_drain(self):
        from aegis.remote import (
            queue_pending_desktop_prompt,
            get_pending_desktop_prompts_count,
            drain_pending_desktop_prompts,
        )
        from unittest.mock import patch

        # Queue while locked
        queue_pending_desktop_prompt("2119188945", "Fix button component", press_enter=True)
        self.assertGreaterEqual(get_pending_desktop_prompts_count(), 1)

        # While locked, drain returns 0
        with patch("aegis.remote.is_workstation_locked", return_value=True):
            drained_locked = drain_pending_desktop_prompts()
            self.assertEqual(drained_locked, 0)
            self.assertGreaterEqual(get_pending_desktop_prompts_count(), 1)

        # When unlocked, drain delivers and clears queue
        with patch("aegis.remote.is_workstation_locked", return_value=False), \
             patch("aegis.remote.send_telegram_message"):
            drained_unlocked = drain_pending_desktop_prompts()
            self.assertGreaterEqual(drained_unlocked, 1)
            self.assertEqual(get_pending_desktop_prompts_count(), 0)


if __name__ == "__main__":
    unittest.main()
