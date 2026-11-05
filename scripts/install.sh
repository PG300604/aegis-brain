#!/usr/bin/env bash
# ==============================================================================
# AegisBrain Universal Agent Mindset Override & Installation Script
# POSIX Bash implementation for Linux, macOS, WSL, and BSD.
# ==============================================================================
set -euo pipefail

FORCE=false
WORKSPACE=""
SNAPSHOT_REASON="Universal Agent Mindset Override"

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -f|--force|-y|--yes)
      FORCE=true
      shift
      ;;
    -w|--workspace)
      WORKSPACE="$2"
      shift 2
      ;;
    -r|--reason)
      SNAPSHOT_REASON="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [-f|--force] [-w|--workspace <path>] [-r|--reason <text>]"
      exit 1
      ;;
  esac
done

# 1. Interactive Notice & Warning Banner
echo ""
echo -e "\033[1;33m========================================================================\033[0m"
echo -e "\033[1;33m [!] WARNING: AEGISBRAIN UNIVERSAL AGENT MINDSET OVERRIDE\033[0m"
echo -e "\033[1;33m========================================================================\033[0m"
echo -e "\033[1;37m Warning: This will configure the reasoning mindset and tool\033[0m"
echo -e "\033[1;37m prioritization of your AI coding assistants. A full snapshot will\033[0m"
echo -e "\033[1;37m be created allowing 1-click restore.\033[0m"
echo -e "\033[1;33m========================================================================\033[0m"
echo ""

if [ "$FORCE" = false ] && [ -t 0 ] && [ -z "${CI:-}" ] && [ -z "${NONINTERACTIVE:-}" ]; then
  read -r -p "Do you wish to proceed with Mindset Override? [Y/n] " response
  if [[ "$response" =~ ^[nN] ]]; then
    echo -e "\033[1;33m[AegisBrain] Installation cancelled by user.\033[0m"
    exit 0
  fi
fi

# 2. Path Discovery
HOME_DIR="${HOME:-$(eval echo "~")}"
if command -v cygpath >/dev/null 2>&1; then
  HOME_DIR="$(cygpath -m "$HOME_DIR")"
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if command -v cygpath >/dev/null 2>&1; then
  REPO_ROOT="$(cygpath -m "$REPO_ROOT")"
fi
SKILL_SOURCE="$REPO_ROOT/skills/aegis/SKILL.md"

AEGIS_DIR="$HOME_DIR/.aegis-brain"
SNAPSHOTS_DIR="$AEGIS_DIR/snapshots"
mkdir -p "$SNAPSHOTS_DIR"

TIMESTAMP="$(date +%s)"
SNAPSHOT_ID="${TIMESTAMP}_mindset_override"
SNAPSHOT_TARGET_DIR="$SNAPSHOTS_DIR/$SNAPSHOT_ID"
SNAPSHOT_FILES_DIR="$SNAPSHOT_TARGET_DIR/files"
mkdir -p "$SNAPSHOT_FILES_DIR"

echo -e "\033[1;36m[1/5] Initializing Restore Point Reflex...\033[0m"

# 3. Targets Discovery
RESOLVED_WORKSPACE=""
if [ -n "$WORKSPACE" ] && [ -d "$WORKSPACE" ]; then
  RESOLVED_WORKSPACE="$(cd "$WORKSPACE" && pwd)"
elif [ "$(pwd)" != "$HOME_DIR" ] && [ -d ".git" ]; then
  RESOLVED_WORKSPACE="$(pwd)"
fi
if [ -n "$RESOLVED_WORKSPACE" ] && command -v cygpath >/dev/null 2>&1; then
  RESOLVED_WORKSPACE="$(cygpath -m "$RESOLVED_WORKSPACE")"
fi

PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
fi

compute_sha256() {
  local f="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$f" | cut -d' ' -f1 | head -c 16
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$f" | cut -d' ' -f1 | head -c 16
  elif [ -n "$PYTHON_CMD" ]; then
    "$PYTHON_CMD" -c "import hashlib; print(hashlib.sha256(open('$f','rb').read()).hexdigest()[:16])"
  else
    echo "nohash"
  fi
}

# Collect monitored targets
TARGET_KEYS=()
TARGET_PATHS=()

register_target() {
  TARGET_KEYS+=("$1")
  TARGET_PATHS+=("$2")
}

register_target "antigravity_gemini_md" "$HOME_DIR/.gemini/config/GEMINI.md"
register_target "antigravity_mindset_knowledge" "$HOME_DIR/.gemini/antigravity-cli/knowledge/aegis_mindset.md"
register_target "aegis_skill_antigravity" "$HOME_DIR/.gemini/config/skills/aegis/SKILL.md"
register_target "claude_code_claude_md" "$HOME_DIR/.claude/CLAUDE.md"
register_target "aegis_skill_claude" "$HOME_DIR/.claude/skills/aegis/SKILL.md"
register_target "codex_instructions_md" "$HOME_DIR/.codex/instructions.md"
register_target "aegis_skill_codex" "$HOME_DIR/.codex/skills/aegis/SKILL.md"
register_target "aider_conf_yml" "$HOME_DIR/.aider.conf.yml"
register_target "aider_conventions_md" "$HOME_DIR/.aider/conventions.md"

if [ -n "$RESOLVED_WORKSPACE" ]; then
  register_target "workspace_claude_md" "$RESOLVED_WORKSPACE/CLAUDE.md"
  register_target "workspace_agents_md" "$RESOLVED_WORKSPACE/AGENTS.md"
fi

# 4. Create Snapshot
BACKED_FILES_JSON="[]"
CREATED_FILES_JSON="[]"
CREATED_DIRS_JSON="[]"

if [ -n "$PYTHON_CMD" ]; then
  export AEGIS_HOME_DIR="$HOME_DIR"
  export AEGIS_WORKSPACE="$RESOLVED_WORKSPACE"
  export AEGIS_SNAPSHOT_TARGET_DIR="$SNAPSHOT_TARGET_DIR"
  export AEGIS_SNAPSHOT_ID="$SNAPSHOT_ID"
  export AEGIS_SNAPSHOT_REASON="$SNAPSHOT_REASON"
  export AEGIS_TIMESTAMP="$TIMESTAMP"
  "$PYTHON_CMD" - << 'EOF'
import json
import os
import shutil
import time
import hashlib
from pathlib import Path

home_dir = os.environ.get("AEGIS_HOME_DIR", "")
targets = [
    ("antigravity_gemini_md", os.path.join(home_dir, ".gemini", "config", "GEMINI.md")),
    ("antigravity_mindset_knowledge", os.path.join(home_dir, ".gemini", "antigravity-cli", "knowledge", "aegis_mindset.md")),
    ("aegis_skill_antigravity", os.path.join(home_dir, ".gemini", "config", "skills", "aegis", "SKILL.md")),
    ("claude_code_claude_md", os.path.join(home_dir, ".claude", "CLAUDE.md")),
    ("aegis_skill_claude", os.path.join(home_dir, ".claude", "skills", "aegis", "SKILL.md")),
    ("codex_instructions_md", os.path.join(home_dir, ".codex", "instructions.md")),
    ("aegis_skill_codex", os.path.join(home_dir, ".codex", "skills", "aegis", "SKILL.md")),
    ("aider_conf_yml", os.path.join(home_dir, ".aider.conf.yml")),
    ("aider_conventions_md", os.path.join(home_dir, ".aider", "conventions.md")),
]
ws = os.environ.get("AEGIS_WORKSPACE", "")
if ws:
    targets.append(("workspace_claude_md", os.path.join(ws, "CLAUDE.md")))
    targets.append(("workspace_agents_md", os.path.join(ws, "AGENTS.md")))

snap_dir = Path(os.environ.get("AEGIS_SNAPSHOT_TARGET_DIR", ""))
snap_files = snap_dir / "files"
snap_files.mkdir(parents=True, exist_ok=True)

backed_files = []
created_files = []
created_dirs = []

for label, p_str in targets:
    p = Path(p_str)
    if p.exists() and p.is_file():
        dest = snap_files / label / p.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        backed_files.append({
            "label": label,
            "original_path": str(p),
            "backup_path": f"files/{label}/{p.name}",
            "hash": h,
            "type": "file"
        })
    else:
        created_files.append(str(p))
        parent = p.parent
        if not parent.exists() and str(parent) not in created_dirs:
            created_dirs.append(str(parent))

ts_val = int(os.environ.get("AEGIS_TIMESTAMP", "0"))
manifest = {
    "snapshot_id": os.environ.get("AEGIS_SNAPSHOT_ID", ""),
    "name": "mindset_override",
    "reason": os.environ.get("AEGIS_SNAPSHOT_REASON", ""),
    "timestamp": ts_val,
    "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts_val)),
    "file_count": len(backed_files),
    "files": backed_files,
    "created_files": created_files,
    "created_dirs": created_dirs,
    "workspace": ws
}

manifest_path = snap_dir / "manifest.json"
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"Backed up {len(backed_files)} files into {snap_dir}")
EOF
else
  # Pure bash fallback for snapshot creation
  for i in "${!TARGET_KEYS[@]}"; do
    key="${TARGET_KEYS[$i]}"
    p="${TARGET_PATHS[$i]}"
    parent="$(dirname "$p")"
    if [ -f "$p" ]; then
      dest_dir="$SNAPSHOT_FILES_DIR/$key"
      mkdir -p "$dest_dir"
      cp "$p" "$dest_dir/"
    fi
  done
fi

LATEST_POINTER="$SNAPSHOTS_DIR/LATEST_MINDSET_SNAPSHOT.txt"
echo "$SNAPSHOT_ID" > "$LATEST_POINTER"
echo -e "\033[1;32m      [OK] Snapshot created: $SNAPSHOT_ID\033[0m"
echo -e "\033[1;32m      [OK] Restore pointer recorded to: $LATEST_POINTER\033[0m"

# 5. Mindset Directives Text
read -r -d '' MINDSET_BLOCK << 'EOF' || true
<!-- AEGIS_BRAIN_MINDSET_START -->
# AegisBrain Universal Mindset Override: Autonomous Hierarchy & Simplicity Directives

> [!IMPORTANT]
> **OPERATIONAL PRIORITY #1 OVERRIDE**: The following four core doctrines govern all reasoning, planning, tool selection, and code generation across this workspace. Conventional generic workflows or raw filesystem crawling are strictly fallback-only.

## 1. Manager-Worker Hierarchical Workflow (Tier 1 Orchestration)
- **Frontier Manager Triage**: The primary model operates as Senior Orchestrator / Tier 1 Manager.
- **Decomposition & Delegation**: Break complex tasks into distinct, verifiable work units. Routine code drafting and boilerplate generation are delegated to local workers (`aegis orchestrate`, `call_local_worker`, or subagents).
- **Transparent Progress Observer**: Maintain step-by-step progress micro-updates so the user can steer, pause, or comment early.
- **4-Stage Quality Gate Review**: Every candidate output must be audited before presentation:
  1. `Unslop / TurnItOut`: Strip artificial LLM filler and conversational watermarks.
  2. `Red-Team & Security Audit`: Block unsafe shell commands (`shell=True`, `os.system`), injection payloads, and path traversals.
  3. `Secret Scanning`: Block hardcoded API keys, tokens, and sensitive credentials.
  4. `Verifiable Test Loop`: Verify against isolated syntax, unit tests, or compiler checks.

## 2. AST Graph Symbol Retrieval (Priority #1 Code Navigation)
- **Sub-Millisecond Code Navigation**: Query symbols, class hierarchies, and caller/callee graphs via `aegis graph --query <symbol>` before dumping files or reading large code chunks.
- **Dependency-Aware Context**: Trace inbound and outbound edges with zero token waste.
- **Fallback Rule**: Revert to conventional grep or file searches ONLY if AST indexing fails or file types are unsupported.

## 3. Subagent Token Arbitrage & Neural Memory Bus
- **Aggressive Subtask Offloading**: Parallelize independent research, deep test verification, heavy doc analysis, and multi-file exploration to subagents (`invoke_subagent`).
- **Context Protection**: Never blow the frontier model context window on raw multi-megabyte log files, raw transcripts, or multi-thousand line diffs.
- **Sub-Second Memory Reflex**:
  - Run `aegis recall` (or `aegis recall "<topic>"`) to retrieve instant SQLite FTS5 memories (<50ms, <100 tokens).
  - Run `aegis bootstrap` to inject active workspace context in <= 400 tokens.

## 4. Andrej Karpathy Simplicity Doctrine
- **Surgical Changes**: Touch ONLY lines directly relevant to the user request. Clean up your own mess; never reformat adjacent code or delete unrelated comments.
- **Zero Speculative Abstraction**: No premature wrappers, multi-layer handlers, or configuration flags for single-use logic.
- **Conciseness Benchmark**: If a solution can be implemented cleanly in 50 lines, never produce 200 lines.
- **Goal-Driven Verifiable Loops**: Define explicit success criteria, write tests that reproduce the issue, and loop until verified.
<!-- AEGIS_BRAIN_MINDSET_END -->
EOF

inject_markdown() {
  local target_file="$1"
  local prepend="${2:-false}"
  local dir
  dir="$(dirname "$target_file")"
  mkdir -p "$dir"

  if [ -f "$target_file" ]; then
    if [ -n "$PYTHON_CMD" ]; then
      export AEGIS_TARGET_FILE="$target_file"
      export AEGIS_MINDSET_BLOCK="$MINDSET_BLOCK"
      export AEGIS_PREPEND="$prepend"
      "$PYTHON_CMD" - << 'EOF'
import os
import re
from pathlib import Path

p = Path(os.environ.get("AEGIS_TARGET_FILE", ""))
content = p.read_text(encoding="utf-8")
block = os.environ.get("AEGIS_MINDSET_BLOCK", "")
pattern = r"<!-- AEGIS_BRAIN_MINDSET_START -->[\s\S]*?<!-- AEGIS_BRAIN_MINDSET_END -->"

if re.search(pattern, content):
    new_content = re.sub(pattern, block.strip(), content)
elif os.environ.get("AEGIS_PREPEND", "false") == "true":
    new_content = block.strip() + "\n\n" + content.lstrip()
else:
    new_content = content.rstrip() + "\n\n" + block.strip() + "\n"

p.write_text(new_content, encoding="utf-8")
EOF
    else
      # Pure bash fallback: if marker exists, strip and re-add
      grep -v "<!-- AEGIS_BRAIN_MINDSET_" "$target_file" > "$target_file.tmp" || true
      if [ "$prepend" = "true" ]; then
        printf "%s\n\n" "$MINDSET_BLOCK" > "$target_file"
        cat "$target_file.tmp" >> "$target_file"
      else
        cat "$target_file.tmp" > "$target_file"
        printf "\n\n%s\n" "$MINDSET_BLOCK" >> "$target_file"
      fi
      rm -f "$target_file.tmp"
    fi
  else
    printf "%s\n" "$MINDSET_BLOCK" > "$target_file"
  fi
}

echo -e "\033[1;36m[2/5] Injecting Mindset Override into Target Platforms...\033[0m"

# A. Google Antigravity CLI
ANTIGRAVITY_GEMINI="$HOME_DIR/.gemini/config/GEMINI.md"
inject_markdown "$ANTIGRAVITY_GEMINI" "true"
echo -e "\033[1;32m      [OK] Google Antigravity: Injected into $ANTIGRAVITY_GEMINI\033[0m"

ANTIGRAVITY_KNOWLEDGE="$HOME_DIR/.gemini/antigravity-cli/knowledge/aegis_mindset.md"
inject_markdown "$ANTIGRAVITY_KNOWLEDGE" "true"
echo -e "\033[1;32m      [OK] Google Antigravity: Injected into $ANTIGRAVITY_KNOWLEDGE\033[0m"

# B. Anthropic Claude Code
CLAUDE_MD="$HOME_DIR/.claude/CLAUDE.md"
inject_markdown "$CLAUDE_MD" "false"
echo -e "\033[1;32m      [OK] Claude Code: Injected into $CLAUDE_MD\033[0m"

# C. OpenAI Codex CLI
CODEX_INSTRUCTIONS="$HOME_DIR/.codex/instructions.md"
inject_markdown "$CODEX_INSTRUCTIONS" "false"
echo -e "\033[1;32m      [OK] OpenAI Codex: Injected into $CODEX_INSTRUCTIONS\033[0m"

# D. Aider CLI
AIDER_CONVENTIONS="$HOME_DIR/.aider/conventions.md"
inject_markdown "$AIDER_CONVENTIONS" "false"
echo -e "\033[1;32m      [OK] Aider: Injected into $AIDER_CONVENTIONS\033[0m"

AIDER_CONF="$HOME_DIR/.aider.conf.yml"
mkdir -p "$(dirname "$AIDER_CONF")"
if [ -f "$AIDER_CONF" ]; then
  if ! grep -q "conventions.md" "$AIDER_CONF"; then
    cat >> "$AIDER_CONF" << 'EOF'

# AegisBrain Mindset Integration
read:
  - ~/.aider/conventions.md
EOF
    echo -e "\033[1;32m      [OK] Aider: Added conventions reference to $AIDER_CONF\033[0m"
  else
    echo -e "\033[1;32m      [OK] Aider: $AIDER_CONF already references conventions\033[0m"
  fi
else
  cat > "$AIDER_CONF" << 'EOF'
# AegisBrain Universal Mindset Configuration for Aider
read:
  - ~/.aider/conventions.md
EOF
  echo -e "\033[1;32m      [OK] Aider: Created $AIDER_CONF\033[0m"
fi

# E. Workspace Injection (if active)
if [ -n "$RESOLVED_WORKSPACE" ]; then
  WS_CLAUDE="$RESOLVED_WORKSPACE/CLAUDE.md"
  WS_AGENTS="$RESOLVED_WORKSPACE/AGENTS.md"
  inject_markdown "$WS_CLAUDE" "false"
  inject_markdown "$WS_AGENTS" "false"
  echo -e "\033[1;32m      [OK] Workspace: Injected into $WS_CLAUDE & $WS_AGENTS\033[0m"
fi

# 6. Distribute Companion Skills
echo -e "\033[1;36m[3/5] Distributing Aegis Companion Skills...\033[0m"
if [ -f "$SKILL_SOURCE" ]; then
  SKILL_TARGETS=(
    "$HOME_DIR/.gemini/config/skills/aegis/SKILL.md"
    "$HOME_DIR/.claude/skills/aegis/SKILL.md"
    "$HOME_DIR/.codex/skills/aegis/SKILL.md"
  )
  for st in "${SKILL_TARGETS[@]}"; do
    mkdir -p "$(dirname "$st")"
    cp "$SKILL_SOURCE" "$st"
    echo -e "\033[1;32m      [OK] Skill installed: $st\033[0m"
  done
fi

# 7. Verification Gate
echo -e "\033[1;36m[4/5] Verifying Mindset Override Integrity...\033[0m"
VERIFIED=true
for chk in "$ANTIGRAVITY_GEMINI" "$CLAUDE_MD" "$CODEX_INSTRUCTIONS" "$AIDER_CONVENTIONS"; do
  if [ -f "$chk" ]; then
    if grep -q "<!-- AEGIS_BRAIN_MINDSET_START -->" "$chk"; then
      echo -e "\033[1;32m      [VERIFIED] $chk\033[0m"
    else
      echo -e "\033[1;31m      [FAILED] Missing mindset marker in $chk\033[0m"
      VERIFIED=false
    fi
  fi
done

# 8. Complete & Output Rollback Instructions
echo -e "\033[1;36m[5/5] Installation Complete!\033[0m"
echo ""
echo -e "\033[1;32m========================================================================\033[0m"
echo -e "\033[1;32m AegisBrain Universal Mindset Override successfully active!\033[0m"
echo -e "\033[1;32m========================================================================\033[0m"
echo -e "\033[1;37m Restore Point ID: $SNAPSHOT_ID\033[0m"
echo -e "\033[1;33m Rollback Command: ./scripts/restore.sh $SNAPSHOT_ID\033[0m"
echo -e "\033[1;33m (or 1-click restore anytime via: ./scripts/restore.sh)\033[0m"
echo -e "\033[1;32m========================================================================\033[0m"
echo ""
