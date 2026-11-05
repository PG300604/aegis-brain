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


def test_restore_snapshot_zero_residue_cleanup(tmp_path, monkeypatch):
    monkeypatch.setattr("aegis.snapshot.get_snapshots_dir", lambda: tmp_path / "snapshots")

    # Create dummy original file
    dummy_orig = tmp_path / "orig.txt"
    dummy_orig.write_text("orig_content", encoding="utf-8")

    dummy_created = tmp_path / "created_by_installer.txt"
    dummy_created_dir = tmp_path / "created_dir"

    monkeypatch.setattr(
        "aegis.snapshot.get_monitored_agent_paths",
        lambda: [("dummy_orig", dummy_orig)]
    )

    # Create snapshot
    manifest = create_snapshot(name="pre_install_test")

    # Installer simulates creating new file and directory
    dummy_created_dir.mkdir(parents=True, exist_ok=True)
    dummy_created.write_text("injected_content", encoding="utf-8")
    dummy_orig.write_text("modified_content", encoding="utf-8")

    # Add created_files and created_dirs to manifest on disk
    snap_dir = tmp_path / "snapshots" / manifest["snapshot_id"]
    manifest["created_files"] = [str(dummy_created)]
    manifest["created_dirs"] = [str(dummy_created_dir)]
    (snap_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    assert dummy_created.exists()
    assert dummy_created_dir.exists()
    assert dummy_orig.read_text(encoding="utf-8") == "modified_content"

    # Restore
    ok, msg = restore_snapshot(manifest["snapshot_id"])
    assert ok is True
    assert "zero residue" in msg

    # Verify zero residue
    assert not dummy_created.exists()
    assert not dummy_created_dir.exists()
    assert dummy_orig.read_text(encoding="utf-8") == "orig_content"
