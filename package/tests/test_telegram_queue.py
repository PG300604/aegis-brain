import json
from unittest.mock import MagicMock, patch
import pytest

from aegis.db import get_connection, init_db
from aegis.telegram_queue import (
    TelegramClient,
    TelegramQueue,
    is_system_idle,
    get_cpu_usage_sample,
    get_telegram_token,
    set_telegram_token,
)


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test_aegis.db"
    monkeypatch.setattr("aegis.config.get_db_path", lambda: test_db)
    monkeypatch.setattr("aegis.config.get_aegis_dir", lambda: tmp_path)
    init_db()
    return test_db


def test_cpu_and_idle_detection():
    # Measure sample (should not throw and return a float >= 0.0)
    sample = get_cpu_usage_sample(sample_duration=0.05)
    assert isinstance(sample, float)
    assert 0.0 <= sample <= 100.0

    idle, reason = is_system_idle(cpu_threshold=100.0)
    assert idle is True
    assert "System is idle" in reason


def test_token_get_and_set(tmp_path):
    set_telegram_token("123456:TEST_TOKEN_ABC")
    assert get_telegram_token() == "123456:TEST_TOKEN_ABC"


def test_telegram_queue_poll_and_drain(monkeypatch):
    queue = TelegramQueue(token="fake_token")

    # Mock client
    mock_client = MagicMock()
    mock_client.get_me.return_value = {"username": "aegis_test_bot", "first_name": "Aegis"}
    mock_client.get_updates.return_value = [
        {
            "update_id": 1001,
            "message": {
                "message_id": 42,
                "chat": {"id": 12345},
                "from": {"first_name": "Priyanshu", "username": "priyanshu_dev"},
                "text": "Check this reel https://www.instagram.com/reel/De4mz5RTxEx/ about AI",
            }
        }
    ]
    monkeypatch.setattr(queue, "get_client", lambda: mock_client)

    # 1. Poll
    queued, max_id = queue.poll()
    assert queued == 1
    assert max_id == 1001

    # Verify status
    st = queue.status()
    assert st["pending"] == 1
    assert st["total"] == 1

    # 2. Drain with mocked sensory pipeline
    with patch("aegis.sensory.process_sensory_link") as mock_sensory:
        mock_sensory.return_value = {
            "artifact": {
                "title": "Awesome AI Tool",
                "author": "thedigidoor",
                "gated_resource_urls": ["https://github.com/example/repo"],
            },
            "analysis": {
                "summary": "A great walkthrough of open-source models.",
                "yc_ceo_feasibility": {"feasibility_score": 9},
            },
            "status": "success",
        }

        processed = queue.drain(idle_only=False, max_items=5)
        assert len(processed) == 1
        assert processed[0]["status"] == "completed"
        assert "https://www.instagram.com/reel/De4mz5RTxEx/" in processed[0]["urls"]

    # Verify DB state
    st_after = queue.status()
    assert st_after["pending"] == 0
    assert st_after["completed"] == 1
