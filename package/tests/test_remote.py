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


if __name__ == "__main__":
    unittest.main()
