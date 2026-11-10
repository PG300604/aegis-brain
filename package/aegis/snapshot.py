"""AegisBrain Snapshot & Rollback Engine.

Provides automated restore points before any agent configuration mutation,
behavior injection, or skill installation. Allows instant, zero-risk rollback
to previous states (similar to Linux Btrfs snapshots or Windows System Restore).
"""

import hashlib
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .config import get_aegis_dir


def get_snapshots_dir() -> Path:
    s_dir = get_aegis_dir() / "snapshots"
    s_dir.mkdir(parents=True, exist_ok=True)
    return s_dir


def get_monitored_agent_paths() -> List[Tuple[str, Path]]:
    """Return key configuration and rule files across supported agent platforms."""
    home = Path.home()
    return [
        ("antigravity_gemini_md", home / ".gemini" / "config" / "GEMINI.md"),
        ("antigravity_rules_dir", home / ".gemini" / "config" / "rules"),
        ("claude_code_claude_md", home / ".claude" / "CLAUDE.md"),
        ("claude_code_config_json", home / ".claude.json"),
        ("cursor_global_rules", home / ".cursorrules"),
        ("windsurf_global_rules", home / ".windsurfrules"),
        ("aegis_skill_antigravity", home / ".gemini" / "config" / "skills" / "aegis" / "SKILL.md"),
        ("aegis_skill_claude", home / ".claude" / "skills" / "aegis" / "SKILL.md"),
        ("codex_instructions_md", home / ".codex" / "instructions.md"),
        ("aegis_skill_codex", home / ".codex" / "skills" / "aegis" / "SKILL.md"),
        ("aider_conf_yml", home / ".aider.conf.yml"),
        ("aider_conventions_md", home / ".aider" / "conventions.md"),
        ("aegis_windows_shim", home / ".local" / "bin" / "aegis.cmd"),
        ("aegis_posix_shim", home / ".local" / "bin" / "aegis"),
    ]


def _calc_file_hash(p: Path) -> str:
    if not p.exists() or not p.is_file():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:16]


def create_snapshot(name: Optional[str] = None, reason: str = "manual") -> Dict[str, Any]:
    """Capture a restore point of all agent configurations, prompts, and shims."""
    ts = int(time.time())
    snap_id = f"{ts}_{name or 'snapshot'}"
    target_dir = get_snapshots_dir() / snap_id
    target_dir.mkdir(parents=True, exist_ok=True)

    files_backup = []
    for label, src_path in get_monitored_agent_paths():
        if src_path.exists():
            if src_path.is_file():
                rel_dest = target_dir / "files" / label / src_path.name
                rel_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, rel_dest)
                files_backup.append({
                    "label": label,
                    "original_path": str(src_path),
                    "backup_path": str(rel_dest.relative_to(target_dir)),
                    "hash": _calc_file_hash(src_path),
                    "type": "file"
                })
            elif src_path.is_dir():
                dest_sub = target_dir / "files" / label
                shutil.copytree(src_path, dest_sub, dirs_exist_ok=True)
                files_backup.append({
                    "label": label,
                    "original_path": str(src_path),
                    "backup_path": str(dest_sub.relative_to(target_dir)),
                    "type": "dir"
                })

    manifest = {
        "snapshot_id": snap_id,
        "name": name or snap_id,
        "reason": reason,
        "timestamp": ts,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)),
        "file_count": len(files_backup),
        "files": files_backup
    }

    manifest_path = target_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def list_snapshots() -> List[Dict[str, Any]]:
    """List all available restore points in chronological order (newest first)."""
    snaps = []
    root = get_snapshots_dir()
    for child in sorted(root.iterdir(), reverse=True):
        if child.is_dir():
            manifest_file = child / "manifest.json"
            if manifest_file.exists():
                try:
                    data = json.loads(manifest_file.read_text(encoding="utf-8"))
                    snaps.append(data)
                except Exception:
                    pass
    return snaps


def format_snapshot_table(snaps: Optional[List[Dict[str, Any]]] = None, limit: Optional[int] = 20) -> str:
    """Format restore points into a clean human-readable table with dates and numbers."""
    if snaps is None:
        snaps = list_snapshots()
    if not snaps:
        return "  No restore points found. Run `aegis snapshot create` to create one."

    lines = [
        "=" * 92,
        "  #   Date / Time          Files  Snapshot ID                    Reason",
        "-" * 92,
    ]
    displayed = snaps[:limit] if limit else snaps
    for idx, s in enumerate(displayed, 1):
        sid = s.get("snapshot_id", "unknown")
        dt = s.get("created_at", "unknown")
        fc = s.get("file_count", 0)
        reason = s.get("reason", "manual")
        if len(reason) > 36:
            reason = reason[:33] + "..."
        lines.append(f" [{idx:>2}] {dt:<19}  {fc:>2}    {sid:<30} {reason}")
    lines.append("-" * 92)
    if limit and len(snaps) > limit:
        lines.append(f"  (Showing newest {limit} of {len(snaps)} snapshots. Pass --all to see full history)")
    return "\n".join(lines)


def restore_snapshot(snapshot_id: str = "latest") -> Tuple[bool, str]:
    """Restore agent configurations from a specified snapshot ID, index number, or latest."""
    root = get_snapshots_dir()
    snaps = list_snapshots()
    if not snaps:
        return False, f"No snapshots available in {root}"

    # Handle numeric index (e.g., '1', '2')
    resolved_id = snapshot_id
    if str(snapshot_id).isdigit():
        idx = int(snapshot_id) - 1
        if 0 <= idx < len(snaps):
            resolved_id = snaps[idx]["snapshot_id"]
        else:
            return False, f"Invalid snapshot number: {snapshot_id} (Available: 1..{len(snaps)})"
    elif snapshot_id in ("latest", "", None):
        resolved_id = snaps[0]["snapshot_id"]

    target_dir = root / resolved_id

    if not target_dir.exists():
        # Check if user passed partial name or substring
        matched = [d for d in root.iterdir() if d.is_dir() and resolved_id in d.name]
        if matched:
            target_dir = matched[0]
        else:
            return False, f"Snapshot '{resolved_id}' not found in {root}"

    manifest_file = target_dir / "manifest.json"
    if not manifest_file.exists():
        return False, f"Corrupted snapshot: missing manifest in {target_dir}"

    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"Failed to parse manifest: {exc}"

    restored_count = 0
    errors = []

    for item in manifest.get("files", []):
        orig_p = Path(item["original_path"])
        bk_rel = target_dir / item["backup_path"]

        try:
            orig_p.parent.mkdir(parents=True, exist_ok=True)
            if item.get("type") == "dir":
                if orig_p.exists():
                    shutil.rmtree(orig_p)
                shutil.copytree(bk_rel, orig_p, dirs_exist_ok=True)
            else:
                shutil.copy2(bk_rel, orig_p)
            restored_count += 1
        except Exception as exc:
            errors.append(f"{orig_p.name}: {exc}")

    # Clean up newly created files and directories for zero residue
    cleaned_count = 0
    for created_item in manifest.get("created_files", []):
        try:
            c_path = Path(created_item)
            if c_path.exists() and (c_path.is_file() or c_path.is_symlink()):
                c_path.unlink()
                cleaned_count += 1
        except Exception as exc:
            errors.append(f"cleanup {created_item}: {exc}")

    for created_dir in reversed(manifest.get("created_dirs", [])):
        try:
            d_path = Path(created_dir)
            if d_path.exists() and d_path.is_dir() and not any(d_path.iterdir()):
                d_path.rmdir()
        except Exception:
            pass

    msg = f"Restored {restored_count} files from restore point '{manifest.get('name')}'"
    if cleaned_count:
        msg += f" (cleaned {cleaned_count} newly created files for zero residue)"
    if errors:
        msg += f" (warnings: {'; '.join(errors)})"
    return True, msg
