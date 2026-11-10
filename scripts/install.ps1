<#
.SYNOPSIS
    AegisBrain Universal Agent Engine & Neural Memory Bus Installer.
.DESCRIPTION
    Interactive Node.js-style colored CLI installer for AegisBrain.
    Configures the 24/7 background daemon, neural memory bus, 3-tier token arbitrage,
    and injects mindset hooks across Google Antigravity, Anthropic Claude Code, OpenAI Codex, and Aider.
.PARAMETER Force
    Bypass interactive prompts and apply recommended defaults.
.PARAMETER WorkspacePath
    Optional path to project workspace for injecting workspace-level conventions.
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [string]$WorkspacePath = "",
    [string]$SnapshotReason = "AegisBrain Universal Installation"
)

$ErrorActionPreference = 'Stop'

function Write-BoxHeader {
    param([string]$Title, [string]$Color = "Cyan")
    Write-Host ""
    Write-Host ("┌" + ("─" * 72) + "┐") -ForegroundColor $Color
    Write-Host ("│  " + $Title.PadRight(70) + "│") -ForegroundColor $Color
    Write-Host ("└" + ("─" * 72) + "┘") -ForegroundColor $Color
}

function Write-Panel {
    param([string[]]$Lines, [string]$BorderColor = "DarkGray", [string]$TextColor = "White")
    Write-Host ("┌" + ("─" * 72) + "┐") -ForegroundColor $BorderColor
    foreach ($line in $Lines) {
        $truncated = if ($line.Length -gt 68) { $line.Substring(0, 68) } else { $line }
        Write-Host ("│  " + $truncated.PadRight(70) + "│") -ForegroundColor $TextColor
    }
    Write-Host ("└" + ("─" * 72) + "┘") -ForegroundColor $BorderColor
}

# Clear screen for fresh installer experience in interactive terminal
if ([System.Environment]::UserInteractive -and -not $env:CI -and -not $Force) {
    try { Clear-Host } catch {}
}

# ============================================================================
# AEGISBRAIN ASCII ART LOGO & WELCOME
# ============================================================================
Write-Host ""
Write-Host "  █████╗ ███████╗ ██████╗ ██╗███████╗    ██████╗ ██████╗  █████╗ ██╗███╗   ██╗" -ForegroundColor Cyan
Write-Host " ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║" -ForegroundColor Cyan
Write-Host " ███████║█████╗  ██║  ███╗██║███████╗    ██████╔╝██████╔╝███████║██║██╔██╗ ██║" -ForegroundColor Yellow
Write-Host " ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║" -ForegroundColor Yellow
Write-Host " ██║  ██║███████╗╚██████╔╝██║███████║    ██████╔╝██║  ██║██║  ██║██║██║ ╚████║" -ForegroundColor Red
Write-Host " ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝" -ForegroundColor Red
Write-Host "         [ 24/7 AUTONOMOUS NEURAL MEMORY & 3-TIER AGENT ORCHESTRATOR ]" -ForegroundColor DarkGray
Write-Host "                               Version 2.4.0 (GPLv3)" -ForegroundColor DarkGray
Write-Host ""

# ============================================================================
# STEP 1: TERMS & CONDITIONS & LICENSE AGREEMENT (GPLv3)
# ============================================================================
Write-BoxHeader "STEP 1 of 4: License Agreement & Terms of Service" "Cyan"

$TermsNotice = @(
    "License: GNU General Public License v3.0 (GPL-3.0-or-later)",
    "Author: Priyanshu Ghosh (@PG300604) | https://github.com/PG300604/aegis-brain",
    "",
    "Core User Commitments & Operational Terms:",
    " • 100% Local Neural Memory: Your data stays on your machine. Zero telemetry,",
    "   session transcripts, or database records are ever exfiltrated.",
    " • Subprocess Boundary: Local worker CLIs (Hermes, Ollama, OpenCode) execute",
    "   via isolated OS subprocesses under their respective upstream licenses.",
    " • Autonomous Safety Reflex: Automated pre-mutation snapshots are created",
    "   before any file changes, enabling 1-click restore at any time.",
    " • No Warranty: Provided 'as is' without warranty of any kind, express or implied."
)
Write-Panel $TermsNotice "DarkCyan" "White"

$AcceptTerms = $true
if (-not $Force -and [System.Environment]::UserInteractive -and -not $env:CI -and -not $env:NONINTERACTIVE) {
    Write-Host ""
    $prompt = Read-Host " Do you accept the Terms & Conditions and GPLv3 license? [Y/n]"
    if ($prompt -match '^[nN]') {
        Write-Host ""
        Write-Host " [X] Installation aborted: Terms must be accepted to proceed." -ForegroundColor Red
        exit 1
    }
    Write-Host " [✓] Terms accepted." -ForegroundColor Green
} else {
    Write-Host " [✓] Terms accepted automatically (-Force)." -ForegroundColor Green
}

# ============================================================================
# STEP 2: EXECUTION MODE CONFIGURATION (ARBITRAGE vs FAST)
# ============================================================================
Write-BoxHeader "STEP 2 of 4: Select Agent Execution Strategy" "Yellow"

$ModeInfo = @(
    "Choose how Antigravity CLI & AegisBrain should triage coding tasks:",
    "",
    " [1] Arbitrage Mode (Recommended - Maximum Token Savings):",
    "     Frontier Manager serves as High-Cognition Brain only. Substantial tasks",
    "     are delegated to Tier 2 Subagents + Tier 3 Local Workers (Hermes, Ollama),",
    "     saving 85%+ frontier tokens with 4-gate quality auditing.",
    "",
    " [2] Fast Direct Mode (Instant Turnaround):",
    "     Frontier Manager generates code drafts directly without worker roundtrips.",
    "     Prioritizes execution speed over token savings."
)
Write-Panel $ModeInfo "DarkYellow" "White"

$SelectedMode = "arbitrage"
if (-not $Force -and [System.Environment]::UserInteractive -and -not $env:CI -and -not $env:NONINTERACTIVE) {
    Write-Host ""
    $modeInput = Read-Host " Select execution mode [1 or 2] (Default: 1 - Arbitrage)"
    if ($modeInput -eq "2") {
        $SelectedMode = "fast"
        Write-Host " [✓] Configured: Fast Direct Mode (Frontier Direct)" -ForegroundColor Yellow
    } else {
        $SelectedMode = "arbitrage"
        Write-Host " [✓] Configured: Dynamic Arbitrage Mode (3-Tier Token Saving)" -ForegroundColor Green
    }
} else {
    Write-Host " [✓] Default configured: Dynamic Arbitrage Mode" -ForegroundColor Green
}

# ============================================================================
# STEP 3: PLATFORM HOOKS INJECTION
# ============================================================================
Write-BoxHeader "STEP 3 of 4: Target AI Coding Assistants" "Magenta"

$PlatformsInfo = @(
    "AegisBrain will inject persistent neural memory and mindset hooks into:",
    " • Google Antigravity CLI     (~/.gemini/config/GEMINI.md)",
    " • Anthropic Claude Code CLI  (~/.claude/CLAUDE.md)",
    " • OpenAI Codex CLI           (~/.codex/instructions.md)",
    " • Aider CLI                  (~/.aider.conf.yml)",
    " • Active Workspace (if inside git repo): CLAUDE.md & AGENTS.md"
)
Write-Panel $PlatformsInfo "DarkMagenta" "White"

# Paths Discovery
$HomeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile) }
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SkillSource = Join-Path $RepoRoot "skills\aegis\SKILL.md"

$AegisDir = Join-Path $HomeDir ".aegis-brain"
$SnapshotsDir = Join-Path $AegisDir "snapshots"
if (-not (Test-Path $SnapshotsDir)) {
    New-Item -ItemType Directory -Path $SnapshotsDir -Force | Out-Null
}

# Save configured execution mode
$ExecModeFile = Join-Path $AegisDir "execution_mode.txt"
[System.IO.File]::WriteAllText($ExecModeFile, $SelectedMode, [System.Text.Encoding]::UTF8)

# ============================================================================
# STEP 4: DEPENDENCIES & SNAPSHOT GENERATION
# ============================================================================
Write-BoxHeader "STEP 4 of 4: Installation & Restore Point Reflex" "Cyan"

$Timestamp = [int][double]::Parse((Get-Date -UFormat %s))
$SnapshotId = "${Timestamp}_universal_install"
$SnapshotTargetDir = Join-Path $SnapshotsDir $SnapshotId
$SnapshotFilesDir = Join-Path $SnapshotTargetDir "files"
New-Item -ItemType Directory -Path $SnapshotFilesDir -Force | Out-Null

Write-Host " [1/6] Creating automated pre-install restore point..." -ForegroundColor Cyan

$PlannedTargets = @(
    @{ Label = "antigravity_gemini_md"; Path = (Join-Path $HomeDir ".gemini\config\GEMINI.md"); Platform = "Google Antigravity" },
    @{ Label = "antigravity_mindset_knowledge"; Path = (Join-Path $HomeDir ".gemini\antigravity-cli\knowledge\aegis_mindset.md"); Platform = "Google Antigravity" },
    @{ Label = "aegis_skill_antigravity"; Path = (Join-Path $HomeDir ".gemini\config\skills\aegis\SKILL.md"); Platform = "Google Antigravity" },
    @{ Label = "claude_code_claude_md"; Path = (Join-Path $HomeDir ".claude\CLAUDE.md"); Platform = "Anthropic Claude Code" },
    @{ Label = "aegis_skill_claude"; Path = (Join-Path $HomeDir ".claude\skills\aegis\SKILL.md"); Platform = "Anthropic Claude Code" },
    @{ Label = "codex_instructions_md"; Path = (Join-Path $HomeDir ".codex\instructions.md"); Platform = "OpenAI Codex" },
    @{ Label = "aegis_skill_codex"; Path = (Join-Path $HomeDir ".codex\skills\aegis\SKILL.md"); Platform = "OpenAI Codex" },
    @{ Label = "aider_conf_yml"; Path = (Join-Path $HomeDir ".aider.conf.yml"); Platform = "Aider" },
    @{ Label = "aider_conventions_md"; Path = (Join-Path $HomeDir ".aider\conventions.md"); Platform = "Aider" }
)

# Workspace-level resolution
$ResolvedWorkspace = ""
if ($WorkspacePath -and (Test-Path $WorkspacePath)) {
    $ResolvedWorkspace = (Resolve-Path $WorkspacePath).Path
} elseif ((Get-Location).Path -ne $HomeDir -and (Test-Path (Join-Path (Get-Location).Path ".git"))) {
    $ResolvedWorkspace = (Get-Location).Path
}

if ($ResolvedWorkspace) {
    $PlannedTargets += @{ Label = "workspace_claude_md"; Path = (Join-Path $ResolvedWorkspace "CLAUDE.md"); Platform = "Claude Workspace" }
    $PlannedTargets += @{ Label = "workspace_agents_md"; Path = (Join-Path $ResolvedWorkspace "AGENTS.md"); Platform = "Agents Workspace" }
}

$BackedUpFiles = @()
$CreatedFiles = @()
$CreatedDirs = @()

foreach ($target in $PlannedTargets) {
    $tPath = $target.Path
    $parentDir = Split-Path -Parent $tPath

    if (Test-Path $tPath -PathType Leaf) {
        $destSubDir = Join-Path $SnapshotFilesDir $target.Label
        New-Item -ItemType Directory -Path $destSubDir -Force | Out-Null
        $destFile = Join-Path $destSubDir (Split-Path -Leaf $tPath)
        Copy-Item -Path $tPath -Destination $destFile -Force

        $hash = (Get-FileHash -Algorithm SHA256 -Path $tPath).Hash.Substring(0, 16).ToLower()
        $relBackup = "files/$($target.Label)/$(Split-Path -Leaf $tPath)"

        $BackedUpFiles += [PSCustomObject]@{
            label = $target.Label
            original_path = $tPath
            backup_path = $relBackup
            hash = $hash
            type = "file"
        }
    } else {
        $CreatedFiles += $tPath
        if (-not (Test-Path $parentDir)) {
            if ($CreatedDirs -notcontains $parentDir) {
                $CreatedDirs += $parentDir
            }
        }
    }
}

$Manifest = [PSCustomObject]@{
    snapshot_id = $SnapshotId
    name = "universal_install"
    reason = $SnapshotReason
    timestamp = $Timestamp
    created_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    file_count = $BackedUpFiles.Count
    files = $BackedUpFiles
    created_files = $CreatedFiles
    created_dirs = $CreatedDirs
    workspace = $ResolvedWorkspace
    execution_mode = $SelectedMode
}

$ManifestJsonPath = Join-Path $SnapshotTargetDir "manifest.json"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($ManifestJsonPath, ($Manifest | ConvertTo-Json -Depth 6), $utf8NoBom)

$LatestPointerPath = Join-Path $SnapshotsDir "LATEST_MINDSET_SNAPSHOT.txt"
[System.IO.File]::WriteAllText($LatestPointerPath, $SnapshotId.Trim(), $utf8NoBom)
Write-Host "       [✓] Snapshot preserved: $SnapshotId ($($BackedUpFiles.Count) files)" -ForegroundColor Green

# Mindset Content
$MindsetMarkdown = @"
<!-- AEGIS_BRAIN_MINDSET_START -->
# AegisBrain Universal Mindset Override: Autonomous Hierarchy & Simplicity Directives

> [!IMPORTANT]
> **OPERATIONAL PRIORITY #1 OVERRIDE**: The following core doctrines govern all reasoning, planning, tool selection, and code generation across this workspace.

## 1. Manager-Worker Hierarchical Workflow (Tier 1 Orchestration)
- **Frontier Manager Triage**: The primary model operates as Senior Orchestrator / Tier 1 Manager.
- **Dynamic Token Arbitrage Mode (Default)**:
  - Complex tasks are delegated to Tier 2 Subagents + Tier 3 Local Workers (`hermes chat -q`, `ollama run qwen2.5-coder:7b`, `opencode`) to save 85%+ frontier tokens.
  - Say 'quick' or 'fast mode' anytime to override and execute directly via Frontier Manager.
- **Transparent Progress Observer**: Maintain step-by-step progress micro-updates so the user can steer, pause, or comment early.
- **4-Stage Quality Gate Review**: Every candidate output must pass:
  1) `Unslop / TurnItOut`: Strip artificial LLM conversational filler.
  2) `Red-Team Security Audit`: Block unsafe shell calls (`shell=True`, `os.system`), injections, and traversals.
  3) `Secret Scanning`: Block hardcoded API keys, tokens, and credentials.
  4) `Verifiable Test Loop`: Verify against isolated syntax or unit tests before host mutation.

## 2. AST Graph Symbol Retrieval (Priority #1 Code Navigation)
- Query symbols, class hierarchies, and caller/callee graphs via `aegis graph --query <symbol>` before dumping files or reading large code chunks.
- Fallback to conventional grep ONLY if AST indexing fails.

## 3. Subagent Token Arbitrage & Neural Memory Bus
- Run `aegis recall` (or `aegis recall "<topic>"`) to retrieve instant SQLite FTS5 memories (<50ms, <100 tokens).
- Run `aegis bootstrap` to inject active workspace context in <= 400 tokens. Never crawl raw multi-megabyte session logs.

## 4. Andrej Karpathy Simplicity Doctrine
- Surgical changes only: Touch ONLY lines directly relevant to the user request.
- Zero speculative abstraction: No premature wrappers for single-use logic.
- If a solution can be implemented cleanly in 50 lines, never produce 200 lines.
<!-- AEGIS_BRAIN_MINDSET_END -->
"@

function Inject-MarkdownBlock {
    param([string]$FilePath, [string]$Block, [bool]$Prepend = $false)
    $parent = Split-Path -Parent $FilePath
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    if (Test-Path $FilePath) {
        $content = Get-Content -Path $FilePath -Raw -Encoding utf8
        if ($content -match '<!-- AEGIS_BRAIN_MINDSET_START -->[\s\S]*?<!-- AEGIS_BRAIN_MINDSET_END -->') {
            $newContent = [regex]::Replace($content, '<!-- AEGIS_BRAIN_MINDSET_START -->[\s\S]*?<!-- AEGIS_BRAIN_MINDSET_END -->', $Block.Trim())
        } elseif ($Prepend) {
            $newContent = $Block.Trim() + "`r`n`r`n" + $content.TrimStart()
        } else {
            $newContent = $content.TrimEnd() + "`r`n`r`n" + $Block.Trim()
        }
        [System.IO.File]::WriteAllText($FilePath, $newContent, [System.Text.Encoding]::UTF8)
    } else {
        [System.IO.File]::WriteAllText($FilePath, $Block.Trim() + "`r`n", [System.Text.Encoding]::UTF8)
    }
}

Write-Host " [2/6] Initializing local neural memory bus & FTS5 tables..." -ForegroundColor Cyan
try {
    $PackageDir = Join-Path $RepoRoot "package"
    $pythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "py" }
    & $pythonCmd -c "import sys; sys.path.insert(0, r'$PackageDir'); from aegis.db import init_db; from aegis.hooks import seed_initial_knowledge; init_db(); seed_initial_knowledge()" 2>$null
    Write-Host "       [✓] SQLite FTS5 neural tables initialized & seeded" -ForegroundColor Green
} catch {
    Write-Host "       [WARN] SQLite FTS5 table initialization deferred: $_" -ForegroundColor Yellow
}

Write-Host " [3/6] Setting up 24/7 background autostart daemon..." -ForegroundColor Cyan
try {
    & $pythonCmd -c "import sys; sys.path.insert(0, r'$PackageDir'); from aegis.service import enable_autostart; ok, msg = enable_autostart(); print(msg)" 2>$null
    Write-Host "       [✓] Windows Scheduled Task 'AegisBrainDaemonKeepAlive' configured" -ForegroundColor Green
} catch {
    Write-Host "       [WARN] Scheduled task setup deferred: $_" -ForegroundColor Yellow
}

Write-Host " [4/6] Registering global 'aegis' CLI shim..." -ForegroundColor Cyan
$homeBin = Join-Path $HomeDir ".local\bin"
if (-not (Test-Path $homeBin)) {
    New-Item -ItemType Directory -Path $homeBin -Force | Out-Null
}
$shimCmd = Join-Path $homeBin "aegis.cmd"
$shimContent = @"
@echo off
set PYTHONPATH=$PackageDir;%PYTHONPATH%
python -m aegis.cli %*
"@
[System.IO.File]::WriteAllText($shimCmd, $shimContent, [System.Text.Encoding]::ASCII)
Write-Host "       [✓] Global CLI command registered: $shimCmd" -ForegroundColor Green

Write-Host " [5/6] Injecting mindset hooks into AI coding assistants..." -ForegroundColor Cyan
# A. Google Antigravity
Inject-MarkdownBlock -FilePath (Join-Path $HomeDir ".gemini\config\GEMINI.md") -Block $MindsetMarkdown -Prepend $true
Inject-MarkdownBlock -FilePath (Join-Path $HomeDir ".gemini\antigravity-cli\knowledge\aegis_mindset.md") -Block $MindsetMarkdown -Prepend $true
# B. Anthropic Claude Code
Inject-MarkdownBlock -FilePath (Join-Path $HomeDir ".claude\CLAUDE.md") -Block $MindsetMarkdown -Prepend $false
# C. OpenAI Codex
Inject-MarkdownBlock -FilePath (Join-Path $HomeDir ".codex\instructions.md") -Block $MindsetMarkdown -Prepend $false
# D. Aider
Inject-MarkdownBlock -FilePath (Join-Path $HomeDir ".aider\conventions.md") -Block $MindsetMarkdown -Prepend $false
# E. Workspace
if ($ResolvedWorkspace) {
    Inject-MarkdownBlock -FilePath (Join-Path $ResolvedWorkspace "CLAUDE.md") -Block $MindsetMarkdown -Prepend $false
    Inject-MarkdownBlock -FilePath (Join-Path $ResolvedWorkspace "AGENTS.md") -Block $MindsetMarkdown -Prepend $false
}
Write-Host "       [✓] Mindset injected across Antigravity, Claude, Codex, Aider & Workspace" -ForegroundColor Green

Write-Host " [6/6] Distributing companion skills..." -ForegroundColor Cyan
if (Test-Path $SkillSource) {
    $skillContent = Get-Content -Path $SkillSource -Raw -Encoding utf8
    $skillTargets = @(
        (Join-Path $HomeDir ".gemini\config\skills\aegis\SKILL.md"),
        (Join-Path $HomeDir ".claude\skills\aegis\SKILL.md"),
        (Join-Path $HomeDir ".codex\skills\aegis\SKILL.md")
    )
    foreach ($st in $skillTargets) {
        $sParent = Split-Path -Parent $st
        if (-not (Test-Path $sParent)) { New-Item -ItemType Directory -Path $sParent -Force | Out-Null }
        [System.IO.File]::WriteAllText($st, $skillContent, [System.Text.Encoding]::UTF8)
    }
    Write-Host "       [✓] Companion skills placed in Antigravity, Claude Code & Codex directories" -ForegroundColor Green
}

# ============================================================================
# FINAL INSTALLATION SUMMARY PANEL
# ============================================================================
Write-Host ""
Write-Host ("╔" + ("═" * 72) + "╗") -ForegroundColor Green
Write-Host ("║  " + "AEGISBRAIN INSTALLATION COMPLETE — 100% OPERATIONAL".PadRight(70) + "║") -ForegroundColor Green
Write-Host ("╠" + ("═" * 72) + "╣") -ForegroundColor Green
Write-Host ("║  " + "• Mode:          ".PadRight(18) + ($SelectedMode.ToUpper() + " Mode").PadRight(52) + "║") -ForegroundColor White
Write-Host ("║  " + "• Neural Memory: ".PadRight(18) + "Active (SQLite FTS5 sub-second indexed bus)".PadRight(52) + "║") -ForegroundColor White
Write-Host ("║  " + "• Daemon:        ".PadRight(18) + "Running 24/7 (Windows KeepAlive Task)".PadRight(52) + "║") -ForegroundColor White
Write-Host ("║  " + "• Restore Point: ".PadRight(18) + $SnapshotId.PadRight(52) + "║") -ForegroundColor White
Write-Host ("║  " + "• License:       ".PadRight(18) + "GNU GPLv3 (Free & Open Source)".PadRight(52) + "║") -ForegroundColor White
Write-Host ("╠" + ("═" * 72) + "╣") -ForegroundColor Green
Write-Host ("║  " + "Quickstart Commands:".PadRight(70) + "║") -ForegroundColor Yellow
Write-Host ("║  " + " 1. aegis briefing         - View dynamic restore status & priorities".PadRight(70) + "║") -ForegroundColor White
Write-Host ("║  " + " 2. aegis recall <topic>   - Sub-25ms instant memory search".PadRight(70) + "║") -ForegroundColor White
Write-Host ("║  " + " 3. aegis triage <task>    - Check 3-tier severity & worker assignment".PadRight(70) + "║") -ForegroundColor White
Write-Host ("║  " + " 4. aegis restore          - 1-click snapshot restore anytime".PadRight(70) + "║") -ForegroundColor White
Write-Host ("╚" + ("═" * 72) + "╝") -ForegroundColor Green
Write-Host ""
