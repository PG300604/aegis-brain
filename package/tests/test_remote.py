import unittest
import sys
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
        res_type = handle_remote_command("whatsapp:+1234567890", "/type Test Prompt Injection")
        self.assertIn("Agent Input", res_type)

    def test_remote_mode_toggle(self):
        # Switch to chat mode
        res_chat = handle_remote_command("whatsapp:+1234567890", "/mode chat")
        self.assertIn("Switched to CHAT", res_chat)

        # Unprefixed message should now type into desktop rather than execute shell
        res_msg = handle_remote_command("whatsapp:+1234567890", "Analyze my code architecture")
        self.assertIn("Chat Mode", res_msg)

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


if __name__ == "__main__":
    unittest.main()
