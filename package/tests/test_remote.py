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
)


class TestCaffeinateAndRemote(unittest.TestCase):
    def setUp(self):
        init_db()
        disable_caffeinate()

    def tearDown(self):
        disable_caffeinate()

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

    def test_remote_shell_exec(self):
        out = execute_shell("python -V")
        self.assertIn("Python 3", out)

    def test_twiml_formatting(self):
        twiml = format_twiml_response("Test message with & < > characters")
        self.assertIn("<Response>", twiml)
        self.assertIn("<Message>", twiml)
        self.assertIn("&amp;", twiml)
        self.assertIn("&lt;", twiml)

    def test_webhook_handler(self):
        twiml = handle_twilio_webhook({"From": "whatsapp:+1234567890", "Body": "/help"})
        self.assertIn("<Response>", twiml)
        self.assertIn("AegisBrain Remote Commands", twiml)


if __name__ == "__main__":
    unittest.main()
