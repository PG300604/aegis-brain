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
        
        with patch("aegis.remote.remote_block_input", return_value=(True, "Hardware input blocked")), \
             patch("aegis.remote.remote_trigger_alarm", return_value=(True, "Alarm sounded")), \
             patch("aegis.remote.remote_lock_workstation", return_value=(True, "Locked")), \
             patch("aegis.remote.send_telegram_inline_keyboard"):
            # Test /blockinput
            res_block = handle_remote_command("whatsapp:+1234567890", "/blockinput on")
            self.assertIn("Physical Input Protection", res_block)

            # Test /alarm
            res_alarm = handle_remote_command("whatsapp:+1234567890", "/alarm")
            self.assertIn("Alert Triggered", res_alarm)

            # Test /lock with mock to avoid locking physical screen during test run
            res_lock = handle_remote_command("whatsapp:+1234567890", "/lock")
            self.assertIn("Away Mode ACTIVATED", res_lock)
            self.assertIn("Caffeinate", res_lock)


    def test_remote_away_mode_and_locked_execution(self):
        from aegis.remote import set_away_mode, set_mock_terminal_busy

        # 1. Shell commands execute headlessly
        res_sh = handle_remote_command("whatsapp:+1234567890", "python -c \"print('remote_exec_test')\"")
        self.assertIn("Command Output", res_sh)
        self.assertIn("remote_exec_test", res_sh)

        # 2. When terminal is idle, /type delivers immediately without queuing
        set_mock_terminal_busy(False)
        res_type_idle = handle_remote_command("whatsapp:+1234567890", "/type echo idle_run")
        self.assertIn("Agent Input", res_type_idle)
        self.assertIn("idle_run", res_type_idle)

        # 3. When terminal is busy, /type queues for next turn unless /altm is specified
        set_mock_terminal_busy(True)
        res_type_busy = handle_remote_command("whatsapp:+1234567890", "/type echo busy_run")
        self.assertIn("Session Busy", res_type_busy)
        self.assertIn("Prompt Queued for Next Turn", res_type_busy)

        # 4. In busy state with /altm, it interrupts and delivers immediately
        res_type_altm = handle_remote_command("whatsapp:+1234567890", "/type echo urgent_run /altm")
        self.assertIn("In-Flight Interrupt Delivered", res_type_altm)
        self.assertIn("urgent_run", res_type_altm)

        set_mock_terminal_busy(None)

        # 5. Clean away mode toggle
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
        self.assertIn("In-Flight Interrupt Delivered", res_type_alt)
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
            queue_execution_prompt,
            get_execution_queue_count,
            drain_execution_queue,
            set_mock_terminal_busy,
            clear_execution_queue,
        )
        from unittest.mock import patch

        clear_execution_queue()

        # Queue while busy
        queue_execution_prompt("2119188945", "Fix button component", press_enter=True)
        self.assertGreaterEqual(get_execution_queue_count(), 1)

        # While terminal is busy executing a task, drain returns 0
        set_mock_terminal_busy(True)
        drained_busy = drain_execution_queue()
        self.assertEqual(drained_busy, 0)
        self.assertGreaterEqual(get_execution_queue_count(), 1)

        # When terminal finishes task and becomes idle, drain delivers prompt and clears queue
        set_mock_terminal_busy(False)
        with patch("aegis.remote.send_telegram_message"):
            drained_idle = drain_execution_queue()
            self.assertGreaterEqual(drained_idle, 1)
            self.assertEqual(get_execution_queue_count(), 0)

        set_mock_terminal_busy(None)

    def test_remote_lock_command_invokes_lock_workstation(self):
        from unittest.mock import patch
        from aegis.remote import handle_remote_command, is_away_mode_active

        with patch("aegis.remote.remote_lock_workstation") as mock_lock:
            mock_lock.return_value = (True, "Locked")
            with patch("aegis.remote.send_telegram_inline_keyboard"):
                res = handle_remote_command("whatsapp:+1234567890", "/lock")
                self.assertIn("Workstation Screen LOCKED", res)
                self.assertTrue(is_away_mode_active())
                mock_lock.assert_called_once()

    def test_vim_mode_commands_and_injection(self):
        from aegis.remote import (
            handle_remote_command,
            is_antigravity_vim_mode,
            type_to_desktop,
            save_remote_config,
            load_remote_config,
        )
        from unittest.mock import patch

        # Test /vim on
        res_on = handle_remote_command("whatsapp:+1234567890", "/vim on")
        self.assertIn("Vim Mode ON", res_on)
        self.assertTrue(is_antigravity_vim_mode())

        # Test /vim status
        res_stat = handle_remote_command("whatsapp:+1234567890", "/vim status")
        self.assertIn("Vim Mode is ENABLED", res_stat)

        # Test /vim off
        res_off = handle_remote_command("whatsapp:+1234567890", "/vim off")
        self.assertIn("Vim Mode OFF", res_off)
        self.assertFalse(is_antigravity_vim_mode())

        # Test type_to_desktop with vim_mode=True in test mode
        ok, msg = type_to_desktop("Test prompt for vim", vim_mode=True)
        self.assertTrue(ok)
        self.assertIn("[Vim Mode calibrated]", msg)

        # Test type_to_desktop with vim_mode=False in test mode
        ok2, msg2 = type_to_desktop("Test prompt standard", vim_mode=False)
        self.assertTrue(ok2)
        self.assertNotIn("[Vim Mode calibrated]", msg2)

    def test_vim_mode_enter_does_not_escape_in_type_to_desktop_core(self):
        """When press_enter=True in Vim Mode, _type_to_desktop_core stays in Insert Mode without EscEsc before Enter."""
        if sys.platform != "win32":
            import unittest
            raise unittest.SkipTest("Windows-only console injection test")
        from aegis.remote import _type_to_desktop_core
        from unittest.mock import patch, MagicMock

        events = []
        def mock_keybd_event(vk, scan, flags, extra):
            events.append((vk, scan, flags))

        with patch.dict(os.environ, {}, clear=False):
            # Temporarily remove PYTEST_CURRENT_TEST to test the real Windows code path
            if "PYTEST_CURRENT_TEST" in os.environ:
                del os.environ["PYTEST_CURRENT_TEST"]
            with patch("ctypes.windll.user32.keybd_event", side_effect=mock_keybd_event), \
                 patch("ctypes.windll.user32.GetForegroundWindow", return_value=1234), \
                 patch("ctypes.windll.user32.GetWindowTextLengthW", return_value=10), \
                 patch("ctypes.windll.user32.GetWindowTextW", return_value=10), \
                 patch("aegis.remote.attach_to_input_desktop"), \
                 patch("aegis.remote.copy_to_desktop_clipboard", return_value=True), \
                 patch("aegis.remote.inject_console_input", return_value=(False, "fallback")):
                
                # Case 1: press_enter=True (must NOT press Esc before Enter)
                events.clear()
                ok, msg = _type_to_desktop_core("my prompt", press_enter=True, press_alt_m=False, vim_mode=True)
                self.assertTrue(ok)
                # Initial sequence to enter Insert Mode: Esc (0x1B), Esc (0x1B), i (0x49)
                vk_calls = [ev[0] for ev in events]
                # Count 0x1B occurrences: should only be the initial 2 Esc key presses (down+up = 4 calls)
                esc_calls = [ev for ev in events if ev[0] == 0x1B]
                self.assertEqual(len(esc_calls), 4, "Initial <Esc><Esc> to switch to insert mode should be exactly 2 keypresses (4 events)")
                # Enter (0x0D) should be pressed (down+up = 2 calls)
                enter_calls = [ev for ev in events if ev[0] == 0x0D]
                self.assertEqual(len(enter_calls), 2, "Enter (0x0D) must be pressed to execute prompt immediately")

                # Case 2: press_enter=False (paste only: MUST escape back to normal mode)
                events.clear()
                ok2, msg2 = _type_to_desktop_core("my prompt", press_enter=False, press_alt_m=False, vim_mode=True)
                self.assertTrue(ok2)
                esc_calls2 = [ev for ev in events if ev[0] == 0x1B]
                self.assertEqual(len(esc_calls2), 6, "Initial 2 Esc + trailing 1 Esc when not pressing enter = 3 keypresses (6 events)")

    def test_handle_incoming_voice_executes_prompt_with_press_enter(self):
        """Transcribed voice prompt from Whisper is executed with press_enter=True and not trapped."""
        from aegis.remote import handle_incoming_voice
        from unittest.mock import patch
        import tempfile

        with tempfile.NamedTemporaryFile("wb", suffix=".oga", delete=False) as f:
            f.write(b"OggS dummy voice bytes")
            f_path = Path(f.name)
        try:
            with patch("aegis.remote.transcribe_telegram_audio", return_value="Refactor the authentication middleware"), \
                 patch("aegis.remote.send_telegram_message", return_value=(True, {})):
                res = handle_incoming_voice("123456789", f_path)
                self.assertIn("Typed and submitted", res)
                self.assertIn("Refactor the authentication middleware", res)
        finally:
            if f_path.exists():
                f_path.unlink()


if __name__ == "__main__":
    unittest.main()
