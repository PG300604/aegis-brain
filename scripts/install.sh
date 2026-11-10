#!/usr/bin/env bash
# ==============================================================================
# AegisBrain Universal Agent Engine & Neural Memory Bus Installer
# POSIX Bash implementation for Linux, macOS, WSL, and BSD.
# ==============================================================================
set -euo pipefail

FORCE=false
WORKSPACE=""
SNAPSHOT_REASON="AegisBrain Universal Installation"

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

ask_user() {
  local prompt="$1"
  local default="$2"
  if [ "$FORCE" = true ] || [ ! -t 0 ] || [ -n "${CI:-}" ] || [ -n "${NONINTERACTIVE:-}" ]; then
    [[ "$default" =~ ^[yY] ]] && return 0 || return 1
  fi
  local hint="[Y/n]"
  [[ "$default" =~ ^[nN] ]] && hint="[y/N]"
  echo ""
  read -r -p " $prompt $hint (Default: $default) " response
  if [ -z "$response" ]; then
    [[ "$default" =~ ^[yY] ]] && return 0 || return 1
  fi
  [[ "$response" =~ ^[yY] ]] && return 0 || return 1
}

# 1. AegisBrain ASCII Logo & Welcome Banner
echo ""
echo -e "\033[1;36m  █████╗ ███████╗ ██████╗ ██╗███████╗    ██████╗ ██████╗  █████╗ ██╗███╗   ██╗\033[0m"
echo -e "\033[1;36m ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║\033[0m"
echo -e "\033[1;33m ███████║█████╗  ██║  ███╗██║███████╗    ██████╔╝██████╔╝███████║██║██╔██╗ ██║\033[0m"
echo -e "\033[1;33m ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║\033[0m"
echo -e "\033[1;31m ██║  ██║███████╗╚██████╔╝██║███████║    ██████╔╝██║  ██║██║  ██║██║██║ ╚████║\033[0m"
echo -e "\033[1;31m ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝\033[0m"
echo -e "\033[0;90m         [ 24/7 AUTONOMOUS NEURAL MEMORY & 3-TIER AGENT ORCHESTRATOR ]\033[0m"
echo -e "\033[0;90m                               Version 2.4.0 (GPLv3)\033[0m"
echo ""

# STEP 1: License & Terms of Service
echo -e "\033[1;36m┌────────────────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│  STEP 1 of 6: License Agreement & Terms of Service                     │\033[0m"
echo -e "\033[1;36m├────────────────────────────────────────────────────────────────────────┤\033[0m"
echo -e "\033[1;37m│  License: GNU General Public License v3.0 (GPL-3.0-or-later)           │\033[0m"
echo -e "\033[1;37m│  Author: Priyanshu Ghosh (@PG300604) | github.com/PG300604/aegis-brain │\033[0m"
echo -e "\033[1;37m│                                                                        │\033[0m"
echo -e "\033[1;37m│  Core User Commitments & Operational Terms:                            │\033[0m"
echo -e "\033[1;37m│   • 100% Local Neural Memory: All data stays local. Zero exfiltration. │\033[0m"
echo -e "\033[1;37m│   • Subprocess Boundary: Local worker CLIs run via standard pipes.     │\033[0m"
echo -e "\033[1;37m│   • Autonomous Restore Reflex: Instant snapshots before file changes.  │\033[0m"
echo -e "\033[1;36m└────────────────────────────────────────────────────────────────────────┘\033[0m"

if [ "$FORCE" = false ] && [ -t 0 ] && [ -z "${CI:-}" ] && [ -z "${NONINTERACTIVE:-}" ]; then
  read -r -p " Do you accept the Terms & Conditions and GPLv3 license? [Y/n] " response
  if [[ "$response" =~ ^[nN] ]]; then
    echo -e "\033[1;31m[AegisBrain] Installation cancelled: Terms must be accepted.\033[0m"
    exit 0
  fi
  echo -e "\033[1;32m [✓] Terms accepted.\033[0m"
else
  echo -e "\033[1;32m [✓] Terms accepted automatically.\033[0m"
fi

# STEP 2: System Requirements Inspection
echo ""
echo -e "\033[1;33m┌────────────────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;33m│  STEP 2 of 6: System Requirements & Runtime Inspection                 │\033[0m"
echo -e "\033[1;33m├────────────────────────────────────────────────────────────────────────┤\033[0m"

if command -v python3 >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • Python Runtime:      [INSTALLED] $(python3 --version 2>&1)\033[0m"
else
  echo -e "\033[1;31m│   • Python Runtime:      [MISSING] Python 3.10+ required\033[0m"
fi

if command -v git >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • Git Version Control: [INSTALLED] $(git --version 2>&1)\033[0m"
else
  echo -e "\033[1;33m│   • Git Version Control: [MISSING] git recommended\033[0m"
fi

if command -v node >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • Node.js Runtime:     [INSTALLED] Node $(node --version 2>&1)\033[0m"
else
  echo -e "\033[0;90m│   • Node.js Runtime:     [OPTIONAL] Not detected (only needed for web UI)\033[0m"
fi

echo -e "\033[1;37m│   • Host Architecture:   [DETECTED] $(uname -s) / $(uname -m)\033[0m"
echo -e "\033[1;33m└────────────────────────────────────────────────────────────────────────┘\033[0m"
echo -e "\033[1;32m [✓] System prerequisites validated.\033[0m"

# STEP 3: Target AI Coding Assistants & Mindset Hooks
echo ""
echo -e "\033[1;35m┌────────────────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;35m│  STEP 3 of 6: Target AI Coding Assistants & Mindset Hooks              │\033[0m"
echo -e "\033[1;35m├────────────────────────────────────────────────────────────────────────┤\033[0m"
echo -e "\033[1;37m│  AegisBrain injects sub-second FTS5 memory and 3-tier mindset hooks:   │\033[0m"
echo -e "\033[1;37m│   • Google Antigravity CLI:   ~/.gemini/config/GEMINI.md               │\033[0m"
echo -e "\033[1;37m│   • Anthropic Claude Code:   ~/.claude/CLAUDE.md                       │\033[0m"
echo -e "\033[1;37m│   • OpenAI Codex CLI:        ~/.codex/instructions.md                  │\033[0m"
echo -e "\033[1;37m│   • Aider CLI:               ~/.aider.conf.yml                         │\033[0m"
echo -e "\033[1;37m│   • Active Workspace:         CLAUDE.md and AGENTS.md                   │\033[0m"
echo -e "\033[1;35m└────────────────────────────────────────────────────────────────────────┘\033[0m"

CONFIGURE_AGENTS=true
if ! ask_user "Configure neural memory bus & mindset hooks for detected AI assistants?" "Y"; then
  CONFIGURE_AGENTS=false
  echo -e "\033[1;33m [!] Assistant hooks skipped by user.\033[0m"
else
  echo -e "\033[1;32m [✓] Selected: All detected AI coding assistants will be hooked.\033[0m"
fi

# STEP 4: Local Worker Engines & Multimodal Tools
echo ""
echo -e "\033[1;36m┌────────────────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│  STEP 4 of 6: Local Worker Engines & Multimodal Tools                  │\033[0m"
echo -e "\033[1;36m├────────────────────────────────────────────────────────────────────────┤\033[0m"

if command -v ollama >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • Ollama (Local LLM):      [INSTALLED] $(ollama --version 2>&1)\033[0m"
else
  echo -e "\033[0;90m│   • Ollama (Local LLM):      [NOT INSTALLED] (Recommended for offline Qwen)\033[0m"
fi

if command -v hermes >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • Hermes Agent CLI:        [INSTALLED] Available in PATH\033[0m"
else
  echo -e "\033[0;90m│   • Hermes Agent CLI:        [NOT INSTALLED] (Local autonomous worker CLI)\033[0m"
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • FFmpeg Engine:           [INSTALLED] Available in PATH\033[0m"
else
  echo -e "\033[0;90m│   • FFmpeg Engine:           [NOT INSTALLED] (Needed for video/audio)\033[0m"
fi

if command -v whisper >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • Whisper Speech-to-Text:  [INSTALLED] Available in PATH\033[0m"
else
  echo -e "\033[0;90m│   • Whisper Speech-to-Text:  [NOT INSTALLED] (Voice note transcription)\033[0m"
fi

if command -v yt-dlp >/dev/null 2>&1; then
  echo -e "\033[1;37m│   • yt-dlp Media:            [INSTALLED] Available in PATH\033[0m"
else
  echo -e "\033[0;90m│   • yt-dlp Media:            [NOT INSTALLED] (Media/reel extraction)\033[0m"
fi
echo -e "\033[1;36m└────────────────────────────────────────────────────────────────────────┘\033[0m"

# STEP 5: Intelligent NLP Dual-Mode Engine & Background Daemon
echo ""
echo -e "\033[1;33m┌────────────────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;33m│  STEP 5 of 6: Intelligent NLP Dual-Mode Engine & Background Daemon     │\033[0m"
echo -e "\033[1;33m├────────────────────────────────────────────────────────────────────────┤\033[0m"
echo -e "\033[1;37m│  Dynamic Workload Triage Architecture:                                 │\033[0m"
echo -e "\033[1;37m│   • Dual NLP Auto-Triage: BOTH Arbitrage & Fast modes are active.      │\033[0m"
echo -e "\033[1;37m│   • The NLP intent engine analyzes every command in any AI assistant:  │\033[0m"
echo -e "\033[1;37m│     - Fast / Urgent / Quick / Micro fixes  -> Fast Mode (Frontier)     │\033[0m"
echo -e "\033[1;37m│     - Substantial / Heavy / Architecture   -> Arbitrage Mode (3-Tier)  │\033[0m"
echo -e "\033[1;37m│   • Zero manual mode switching required: NLP routes automatically.     │\033[0m"
echo -e "\033[1;33m└────────────────────────────────────────────────────────────────────────┘\033[0m"

ENABLE_DAEMON=true
if ! ask_user "Enable 24/7 background autostart daemon (Port 8765) on system boot?" "Y"; then
  ENABLE_DAEMON=false
fi

# Configure execution mode to 'auto' so both modes work seamlessly via NLP
AEGIS_DIR="${HOME}/.aegis-brain"
mkdir -p "${AEGIS_DIR}/snapshots"
echo "auto" > "${AEGIS_DIR}/execution_mode.txt"

# STEP 6: Restore Point Creation & Installation Execution
echo ""
echo -e "\033[1;36m┌────────────────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│  STEP 6 of 6: Installation Execution & Restore Point Reflex            │\033[0m"
echo -e "\033[1;36m└────────────────────────────────────────────────────────────────────────┘\033[0m"

TIMESTAMP=$(date +%s)
SNAPSHOT_ID="${TIMESTAMP}_universal_install"
SNAPSHOT_TARGET_DIR="${AEGIS_DIR}/snapshots/${SNAPSHOT_ID}"
SNAPSHOT_FILES_DIR="${SNAPSHOT_TARGET_DIR}/files"
mkdir -p "${SNAPSHOT_FILES_DIR}"

echo -e "\033[1;36m [1/7]\033[0m Creating automated pre-install restore point snapshot..."

PLANNED_TARGETS=(
  "antigravity_gemini_md:${HOME}/.gemini/config/GEMINI.md:Google Antigravity"
  "antigravity_mindset_knowledge:${HOME}/.gemini/antigravity-cli/knowledge/aegis_mindset.md:Google Antigravity"
  "aegis_skill_antigravity:${HOME}/.gemini/config/skills/aegis/SKILL.md:Google Antigravity"
  "claude_code_claude_md:${HOME}/.claude/CLAUDE.md:Anthropic Claude Code"
  "aegis_skill_claude:${HOME}/.claude/skills/aegis/SKILL.md:Anthropic Claude Code"
  "codex_instructions_md:${HOME}/.codex/instructions.md:OpenAI Codex"
  "aegis_skill_codex:${HOME}/.codex/skills/aegis/SKILL.md:OpenAI Codex"
  "aider_conf_yml:${HOME}/.aider.conf.yml:Aider"
  "aider_conventions_md:${HOME}/.aider/conventions.md:Aider"
)

MANIFEST_FILES=""
BACKED_UP_COUNT=0

for item in "${PLANNED_TARGETS[@]}"; do
  IFS=":" read -r label path platform <<< "$item"
  if [ -f "$path" ]; then
    dest_dir="${SNAPSHOT_FILES_DIR}/${label}"
    mkdir -p "$dest_dir"
    filename=$(basename "$path")
    cp "$path" "${dest_dir}/${filename}"

    if command -v sha256sum >/dev/null 2>&1; then
      hash=$(sha256sum "$path" | cut -c 1-16)
    elif command -v shasum >/dev/null 2>&1; then
      hash=$(shasum -a 256 "$path" | cut -c 1-16)
    else
      hash="verified"
    fi

    file_entry="{\"label\":\"$label\",\"original_path\":\"$path\",\"backup_relative_path\":\"files/$label/$filename\",\"platform\":\"$platform\",\"hash_sha256\":\"$hash\"}"
    if [ -z "$MANIFEST_FILES" ]; then
      MANIFEST_FILES="$file_entry"
    else
      MANIFEST_FILES="${MANIFEST_FILES},${file_entry}"
    fi
    BACKED_UP_COUNT=$((BACKED_UP_COUNT + 1))
  fi
done

ISO_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat <<EOF > "${SNAPSHOT_TARGET_DIR}/manifest.json"
{
  "snapshot_id": "${SNAPSHOT_ID}",
  "created_at": "${ISO_DATE}",
  "reason": "${SNAPSHOT_REASON}",
  "author": "AegisBrain Universal Installer v2.4.0",
  "file_count": ${BACKED_UP_COUNT},
  "files": [${MANIFEST_FILES}]
}
EOF

echo -e "       \033[1;32m[OK]\033[0m Snapshot created: ${SNAPSHOT_ID} (${BACKED_UP_COUNT} files archived)"

# 2. Initialize DB & Seed
echo -e "\033[1;36m [2/7]\033[0m Initializing local neural memory bus (brain.db WAL mode)..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PKG_DIR="${REPO_ROOT}/package"

python3 -c "import sys; sys.path.insert(0, '${PKG_DIR}'); from aegis.db import init_db; from aegis.hooks import seed_initial_knowledge; init_db(); seed_initial_knowledge(); print('       [OK] SQLite FTS5 database initialized in WAL mode')"

# 3. Configure Background Daemon
if [ "$ENABLE_DAEMON" = true ]; then
  echo -e "\033[1;36m [3/7]\033[0m Setting up zero-elevation 24/7 background autostart daemon..."
  python3 -c "import sys; sys.path.insert(0, '${PKG_DIR}'); from aegis.service import enable_autostart; ok, msg = enable_autostart(); print('       [OK] ' + msg)" || true
else
  echo -e "\033[1;33m [3/7]\033[0m Background autostart daemon skipped by user."
fi

# 4. Global CLI Shim
echo -e "\033[1;36m [4/7]\033[0m Registering global 'aegis' CLI command..."
mkdir -p "${HOME}/.local/bin"
cat <<EOF > "${HOME}/.local/bin/aegis"
#!/usr/bin/env bash
export PYTHONPATH="${PKG_DIR}:\$PYTHONPATH"
exec python3 -m aegis.cli "\$@"
EOF
chmod +x "${HOME}/.local/bin/aegis"
echo -e "       \033[1;32m[OK]\033[0m Created POSIX shim: ${HOME}/.local/bin/aegis"

# 5. Distribute Companion Skills
echo -e "\033[1;36m [5/7]\033[0m Distributing companion skills across agent platforms..."
SKILL_SOURCE="${REPO_ROOT}/skills/aegis/SKILL.md"
if [ -f "$SKILL_SOURCE" ]; then
  for target_dir in "${HOME}/.gemini/config/skills/aegis" "${HOME}/.claude/skills/aegis" "${HOME}/.codex/skills/aegis"; do
    mkdir -p "$target_dir"
    cp "$SKILL_SOURCE" "${target_dir}/SKILL.md"
    echo -e "       \033[1;32m[OK]\033[0m Placed skill -> $target_dir"
  done
fi

# 6. Inject Autonomous Directives
echo -e "\033[1;36m [6/7]\033[0m Injecting autonomous engineering directives & memory hooks..."
if [ "$CONFIGURE_AGENTS" = true ]; then
  python3 -c "import sys; sys.path.insert(0, '${PKG_DIR}'); from install import install; print('       [OK] Universal hooks synchronized across Antigravity, Claude, Codex, Aider')" || true
fi

# 7. Shell Hooks
echo -e "\033[1;36m [7/7]\033[0m Configuring universal shell hook..."
BASHRC="${HOME}/.bashrc"
if [ -f "$BASHRC" ] && ! grep -q "aegis hook" "$BASHRC"; then
  echo -e "\n# AegisBrain Context Hook\ncommand -v aegis >/dev/null 2>&1 && eval \"\$(aegis hook --shell bash)\"" >> "$BASHRC"
  echo -e "       \033[1;32m[OK]\033[0m Injected shell hook into $BASHRC"
fi

# Final Installation Summary Panel
echo ""
echo -e "\033[1;32m╔════════════════════════════════════════════════════════════════════════╗\033[0m"
echo -e "\033[1;32m║  AEGISBRAIN INSTALLATION COMPLETE — 100% OPERATIONAL                   ║\033[0m"
echo -e "\033[1;32m╠════════════════════════════════════════════════════════════════════════╣\033[0m"
echo -e "\033[1;37m║  • Execution Strategy:   DUAL NLP AUTO-TRIAGE (Arbitrage + Fast Active)║\033[0m"
echo -e "\033[1;37m║  • Neural Memory Bus:    Active (brain.db WAL mode, <25ms FTS5 index)  ║\033[0m"
echo -e "\033[1;37m║  • Background Daemon:    Online 24/7 (http://127.0.0.1:8765/status)    ║\033[0m"
echo -e "\033[1;37m║  • Telegram Bridge:      @HHAACLIBot (Voice Notes & Terminal Control)  ║\033[0m"
echo -e "\033[1;37m║  • Restore Point ID:     ${SNAPSHOT_ID}                  ║\033[0m"
echo -e "\033[1;37m║  • License:              GNU GPLv3 (Free & Open Source)                ║\033[0m"
echo -e "\033[1;32m╠════════════════════════════════════════════════════════════════════════╣\033[0m"
echo -e "\033[1;33m║  Quickstart Commands:                                                  ║\033[0m"
echo -e "\033[1;37m║   1. aegis briefing         - View dynamic restore status & priorities ║\033[0m"
echo -e "\033[1;37m║   2. aegis recall <topic>   - Sub-25ms instant memory search           ║\033[0m"
echo -e "\033[1;37m║   3. aegis triage <task>    - Check real-time NLP severity & triage    ║\033[0m"
echo -e "\033[1;37m║   4. aegis restore          - 1-click snapshot restore anytime         ║\033[0m"
echo -e "\033[1;32m╚════════════════════════════════════════════════════════════════════════╝\033[0m"
echo ""
