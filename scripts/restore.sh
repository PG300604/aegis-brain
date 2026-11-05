#!/usr/bin/env bash
# ==============================================================================
# AegisBrain Universal Agent Mindset Rollback Script
# POSIX Bash implementation for Linux, macOS, WSL, and BSD.
# Restores all agent configurations with ZERO RESIDUE.
# ==============================================================================
set -euo pipefail

TARGET_SNAPSHOT_ID="${1:-}"
FORCE=false

if [ "$TARGET_SNAPSHOT_ID" = "-f" ] || [ "$TARGET_SNAPSHOT_ID" = "--force" ] || [ "$TARGET_SNAPSHOT_ID" = "-y" ] || [ "$TARGET_SNAPSHOT_ID" = "--yes" ]; then
  FORCE=true
  TARGET_SNAPSHOT_ID=""
fi

if [ "${2:-}" = "-f" ] || [ "${2:-}" = "--force" ] || [ "${2:-}" = "-y" ] || [ "${2:-}" = "--yes" ]; then
  FORCE=true
fi

echo ""
echo -e "\033[1;36m========================================================================\033[0m"
echo -e "\033[1;36m AegisBrain Universal Agent Mindset Rollback & Restore\033[0m"
echo -e "\033[1;36m========================================================================\033[0m"
echo ""

HOME_DIR="${HOME:-$(eval echo "~")}"
if command -v cygpath >/dev/null 2>&1; then
  HOME_DIR="$(cygpath -m "$HOME_DIR")"
fi
SNAPSHOTS_DIR="$HOME_DIR/.aegis-brain/snapshots"
LATEST_POINTER="$SNAPSHOTS_DIR/LATEST_MINDSET_SNAPSHOT.txt"

# 1. Resolve Snapshot ID
if [ -z "$TARGET_SNAPSHOT_ID" ]; then
  if [ -f "$LATEST_POINTER" ]; then
    TARGET_SNAPSHOT_ID="$(tr -d ' \r\n' < "$LATEST_POINTER")"
  fi
fi

if [ -z "$TARGET_SNAPSHOT_ID" ]; then
  if [ -d "$SNAPSHOTS_DIR" ]; then
    latest_dir="$(find "$SNAPSHOTS_DIR" -maxdepth 1 -mindepth 1 -type d -name "*mindset_override*" | sort -r | head -n 1 || true)"
    if [ -n "$latest_dir" ]; then
      TARGET_SNAPSHOT_ID="$(basename "$latest_dir")"
    else
      latest_any="$(find "$SNAPSHOTS_DIR" -maxdepth 1 -mindepth 1 -type d | sort -r | head -n 1 || true)"
      if [ -n "$latest_any" ]; then
        TARGET_SNAPSHOT_ID="$(basename "$latest_any")"
      fi
    fi
  fi
fi

if [ -z "$TARGET_SNAPSHOT_ID" ]; then
  echo -e "\033[1;31m[ERROR] No restore points found in $SNAPSHOTS_DIR\033[0m"
  exit 1
fi

SNAPSHOT_TARGET_DIR="$SNAPSHOTS_DIR/$TARGET_SNAPSHOT_ID"
if [ ! -d "$SNAPSHOT_TARGET_DIR" ]; then
  # Try partial match
  matched_dir="$(find "$SNAPSHOTS_DIR" -maxdepth 1 -mindepth 1 -type d -name "*$TARGET_SNAPSHOT_ID*" | sort -r | head -n 1 || true)"
  if [ -n "$matched_dir" ]; then
    SNAPSHOT_TARGET_DIR="$matched_dir"
    TARGET_SNAPSHOT_ID="$(basename "$matched_dir")"
  else
    echo -e "\033[1;31m[ERROR] Snapshot '$TARGET_SNAPSHOT_ID' does not exist in $SNAPSHOTS_DIR\033[0m"
    exit 1
  fi
fi

MANIFEST_PATH="$SNAPSHOT_TARGET_DIR/manifest.json"
if [ ! -f "$MANIFEST_PATH" ]; then
  echo -e "\033[1;31m[ERROR] Corrupt snapshot: missing manifest.json in $SNAPSHOT_TARGET_DIR\033[0m"
  exit 1
fi

PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
  echo -e "\033[1;31m[ERROR] Python is required to parse manifest.json\033[0m"
  exit 1
fi

# Print metadata
export AEGIS_MANIFEST_PATH="$MANIFEST_PATH"
"$PYTHON_CMD" - << 'EOF'
import json
import os
from pathlib import Path

manifest_path = os.environ.get("AEGIS_MANIFEST_PATH", "")
m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
print(f" Identified Restore Point:")
print(f"   Snapshot ID : {m.get('snapshot_id')}")
print(f"   Created At  : {m.get('created_at')}")
print(f"   Reason      : {m.get('reason')}")
print(f"   Backed Files: {len(m.get('files', []))}")
print(f"   Created Files to Remove: {len(m.get('created_files', []))}")
print("")
EOF

if [ "$FORCE" = false ] && [ -t 0 ] && [ -z "${CI:-}" ] && [ -z "${NONINTERACTIVE:-}" ]; then
  read -r -p "Proceed with restoring this snapshot? All post-snapshot changes will be reverted. [Y/n] " resp
  if [[ "$resp" =~ ^[nN] ]]; then
    echo -e "\033[1;33m[AegisBrain] Rollback cancelled by user.\033[0m"
    exit 0
  fi
fi

# 2. Execute Restoration via Python engine
echo -e "\033[1;36m[1/4] Restoring pre-override configuration files...\033[0m"
echo -e "\033[1;36m[2/4] Removing newly created files (Zero Residue)...\033[0m"
echo -e "\033[1;36m[3/4] Cleaning up empty installer-created directories...\033[0m"
echo -e "\033[1;36m[4/4] Executing defense-in-depth residual marker check...\033[0m"

export AEGIS_MANIFEST_PATH="$MANIFEST_PATH"
export AEGIS_SNAPSHOT_TARGET_DIR="$SNAPSHOT_TARGET_DIR"
export AEGIS_HOME_DIR="$HOME_DIR"
"$PYTHON_CMD" - << 'EOF'
import json
import os
import shutil
import re
from pathlib import Path

manifest_p = Path(os.environ.get("AEGIS_MANIFEST_PATH", ""))
snap_dir = Path(os.environ.get("AEGIS_SNAPSHOT_TARGET_DIR", ""))
home = Path(os.environ.get("AEGIS_HOME_DIR", ""))

manifest = json.loads(manifest_p.read_text(encoding="utf-8"))

restored_count = 0
for f_info in manifest.get("files", []):
    orig = Path(f_info["original_path"])
    bk = snap_dir / f_info["backup_path"]
    if bk.exists():
        orig.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bk, orig)
        restored_count += 1
        print(f"      [RESTORED] {orig}")
    else:
        print(f"      [WARN] Missing backup: {bk}")

cleaned_files_count = 0
for c_path_str in manifest.get("created_files", []):
    cp = Path(c_path_str)
    if cp.exists() and cp.is_file():
        try:
            cp.unlink()
            cleaned_files_count += 1
            print(f"      [REMOVED] {cp}")
        except Exception as e:
            print(f"      [WARN] Could not remove {cp}: {e}")

cleaned_dirs_count = 0
for d_path_str in reversed(manifest.get("created_dirs", [])):
    dp = Path(d_path_str)
    if dp.exists() and dp.is_dir():
        try:
            if not any(dp.iterdir()):
                dp.rmdir()
                cleaned_dirs_count += 1
                print(f"      [CLEANED] Empty directory: {dp}")
        except Exception:
            pass

# Defense-in-depth marker scrubber
monitored = [
    home / ".gemini" / "config" / "GEMINI.md",
    home / ".claude" / "CLAUDE.md",
    home / ".codex" / "instructions.md",
    home / ".aider" / "conventions.md",
]
ws = manifest.get("workspace")
if ws:
    monitored.append(Path(ws) / "CLAUDE.md")
    monitored.append(Path(ws) / "AGENTS.md")

pattern = re.compile(r"<!-- AEGIS_BRAIN_MINDSET_START -->[\s\S]*?<!-- AEGIS_BRAIN_MINDSET_END -->")

for m_path in monitored:
    if m_path.exists() and m_path.is_file():
        try:
            content = m_path.read_text(encoding="utf-8")
            if pattern.search(content):
                scrubbed = pattern.sub("", content).strip()
                if not scrubbed and str(m_path) in manifest.get("created_files", []):
                    m_path.unlink()
                    print(f"      [CLEANED] Removed empty residual file: {m_path}")
                else:
                    m_path.write_text(scrubbed + ("\n" if scrubbed else ""), encoding="utf-8")
                    print(f"      [SCRUBBED] Stripped residual marker from: {m_path}")
        except Exception:
            pass

print("")
print("========================================================================")
print(" [SUCCESS] Mindset override rolled back successfully with ZERO RESIDUE!")
print("========================================================================")
print(f" Summary:")
print(f"   Files Restored : {restored_count}")
print(f"   Files Removed  : {cleaned_files_count}")
print(f"   Dirs Cleaned   : {cleaned_dirs_count}")
print("========================================================================")
EOF

echo ""
