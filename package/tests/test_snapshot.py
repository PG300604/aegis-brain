import json
import tempfile
from pathlib import Path
from aegis.snapshot import create_snapshot, list_snapshots, restore_snapshot, get_snapshots_dir


def test_create_and_list_snapshots(tmp_path, monkeypatch):
    monkeypatch.setattr("aegis.snapshot.get_snapshots_dir", lambda: tmp_path / "snapshots")

    # Create dummy file to backup
    dummy_file = tmp_path / "test_config.json"
    dummy_file.write_text('{"key": "original_value"}', encoding="utf-8")

    monkeypatch.setattr(
        "aegis.snapshot.get_monitored_agent_paths",
        lambda: [("dummy_config", dummy_file)]
    )

    manifest = create_snapshot(name="unit_test_snap", reason="test_reason")
    assert manifest["snapshot_id"]
    assert manifest["name"] == "unit_test_snap"
    assert manifest["file_count"] == 1

    snaps = list_snapshots()
    assert len(snaps) == 1
    assert snaps[0]["name"] == "unit_test_snap"


def test_restore_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr("aegis.snapshot.get_snapshots_dir", lambda: tmp_path / "snapshots")

    dummy_file = tmp_path / "test_config.json"
    dummy_file.write_text('{"key": "original_state"}', encoding="utf-8")

    monkeypatch.setattr(
        "aegis.snapshot.get_monitored_agent_paths",
        lambda: [("dummy_config", dummy_file)]
    )

    # 1. Create snapshot of original state
    snap = create_snapshot(name="pre_modification")

    # 2. Mutate file
    dummy_file.write_text('{"key": "mutated_state"}', encoding="utf-8")
    assert "mutated_state" in dummy_file.read_text(encoding="utf-8")

    # 3. Restore from snapshot
    ok, msg = restore_snapshot(snap["snapshot_id"])
    assert ok is True
    assert "Restored 1 files" in msg

    # 4. Verify original state restored
    restored_text = dummy_file.read_text(encoding="utf-8")
    assert "original_state" in restored_text
