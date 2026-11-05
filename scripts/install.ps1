<#
.SYNOPSIS
    AegisBrain Universal Agent Mindset Override & Installation Script.
.DESCRIPTION
    Injects the AegisBrain priority #1 reasoning mindset across Google Antigravity,
    Anthropic Claude Code, OpenAI Codex, and Aider with autonomous snapshot restore points.
.PARAMETER Force
    Bypass interactive confirmation prompt for automated/CI environments.
.PARAMETER WorkspacePath
    Optional path to project workspace for injecting workspace-level CLAUDE.md / AGENTS.md.
.PARAMETER SnapshotReason
    Custom description recorded in the snapshot manifest.
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [string]$WorkspacePath = "",
    [string]$SnapshotReason = "Universal Agent Mindset Override"
)

$ErrorActionPreference = 'Stop'

# 1. Interactive Notice & Warning Banner
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host " [!] WARNING: AEGISBRAIN UNIVERSAL AGENT MINDSET OVERRIDE" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host " Warning: This will configure the reasoning mindset and tool" -ForegroundColor White
Write-Host " prioritization of your AI coding assistants. A full snapshot will" -ForegroundColor White
Write-Host " be created allowing 1-click restore." -ForegroundColor White
Write-Host "========================================================================" -ForegroundColor Yellow
Write-Host ""

if (-not $Force -and [System.Environment]::UserInteractive -and -not $env:CI -and -not $env:NONINTERACTIVE) {
    try {
        $response = Read-Host "Do you wish to proceed with Mindset Override? [Y/n]"
        if ($response -match '^[nN]') {
            Write-Host "[AegisBrain] Installation cancelled by user." -ForegroundColor Yellow
            exit 0
        }
    } catch {
        # Non-interactive fallback
    }
}

# 2. Path & Environment Discovery
$HomeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile) }
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SkillSource = Join-Path $RepoRoot "skills\aegis\SKILL.md"

$AegisDir = Join-Path $HomeDir ".aegis-brain"
$SnapshotsDir = Join-Path $AegisDir "snapshots"
if (-not (Test-Path $SnapshotsDir)) {
    New-Item -ItemType Directory -Path $SnapshotsDir -Force | Out-Null
}

$Timestamp = [int][double]::Parse((Get-Date -UFormat %s))
$SnapshotId = "${Timestamp}_mindset_override"
$SnapshotTargetDir = Join-Path $SnapshotsDir $SnapshotId
$SnapshotFilesDir = Join-Path $SnapshotTargetDir "files"
New-Item -ItemType Directory -Path $SnapshotFilesDir -Force | Out-Null

Write-Host "[1/5] Initializing Restore Point Reflex..." -ForegroundColor Cyan

# 3. Define Monitored Targets across Platforms
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

# Optional workspace-level injection
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

# 4. Execute Snapshot Before Any Mutation
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

        if (Get-Command Get-FileHash -ErrorAction SilentlyContinue) {
            $hash = (Get-FileHash -Algorithm SHA256 -Path $tPath).Hash.Substring(0, 16).ToLower()
        } else {
            $stream = [System.IO.File]::OpenRead($tPath)
            $sha = [System.Security.Cryptography.SHA256]::Create()
            $hashBytes = $sha.ComputeHash($stream)
            $stream.Close()
            $sha.Dispose()
            $hash = [System.BitConverter]::ToString($hashBytes).Replace("-", "").Substring(0, 16).ToLower()
        }
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
    name = "mindset_override"
    reason = $SnapshotReason
    timestamp = $Timestamp
    created_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    file_count = $BackedUpFiles.Count
    files = $BackedUpFiles
    created_files = $CreatedFiles
    created_dirs = $CreatedDirs
    workspace = $ResolvedWorkspace
}

$ManifestJsonPath = Join-Path $SnapshotTargetDir "manifest.json"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($ManifestJsonPath, ($Manifest | ConvertTo-Json -Depth 6), $utf8NoBom)

$LatestPointerPath = Join-Path $SnapshotsDir "LATEST_MINDSET_SNAPSHOT.txt"
[System.IO.File]::WriteAllText($LatestPointerPath, $SnapshotId.Trim(), $utf8NoBom)

Write-Host "      [OK] Snapshot created: $SnapshotId ($($BackedUpFiles.Count) files backed up)" -ForegroundColor Green
Write-Host "      [OK] Restore pointer recorded to: $LatestPointerPath" -ForegroundColor Green

# 5. Mindset Directives Definition
$MindsetMarkdown = @"
<!-- AEGIS_BRAIN_MINDSET_START -->
# AegisBrain Universal Mindset Override: Autonomous Hierarchy & Simplicity Directives

> [!IMPORTANT]
> **OPERATIONAL PRIORITY #1 OVERRIDE**: The following four core doctrines govern all reasoning, planning, tool selection, and code generation across this workspace. Conventional generic workflows or raw filesystem crawling are strictly fallback-only.

## 1. Manager-Worker Hierarchical Workflow (Tier 1 Orchestration)
- **Frontier Manager Triage**: The primary model operates as Senior Orchestrator / Tier 1 Manager.
- **Decomposition & Delegation**: Break complex tasks into distinct, verifiable work units. Routine code drafting and boilerplate generation are delegated to local workers (`aegis orchestrate`, `call_local_worker`, or subagents).
- **Transparent Progress Observer**: Maintain step-by-step progress micro-updates so the user can steer, pause, or comment early.
- **4-Stage Quality Gate Review**: Every candidate output must be audited before presentation:
  1) `Unslop / TurnItOut`: Strip artificial LLM filler and conversational watermarks.
  2) `Red-Team & Security Audit`: Block unsafe shell commands (`shell=True`, `os.system`), injection payloads, and path traversals.
  3) `Secret Scanning`: Block hardcoded API keys, tokens, and sensitive credentials.
  4) `Verifiable Test Loop`: Verify against isolated syntax, unit tests, or compiler checks.

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
"@

function Inject-MarkdownBlock {
    param(
        [string]$FilePath,
        [string]$Block,
        [bool]$Prepend = $false
    )
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

Write-Host "[2/5] Injecting Mindset Override into Target Platforms..." -ForegroundColor Cyan

# A. Google Antigravity CLI
$AntigravityGemini = Join-Path $HomeDir ".gemini\config\GEMINI.md"
Inject-MarkdownBlock -FilePath $AntigravityGemini -Block $MindsetMarkdown -Prepend $true
Write-Host "      [OK] Google Antigravity: Injected into $AntigravityGemini" -ForegroundColor Green

$AntigravityKnowledge = Join-Path $HomeDir ".gemini\antigravity-cli\knowledge\aegis_mindset.md"
Inject-MarkdownBlock -FilePath $AntigravityKnowledge -Block $MindsetMarkdown -Prepend $true
Write-Host "      [OK] Google Antigravity: Injected into $AntigravityKnowledge" -ForegroundColor Green

# B. Anthropic Claude Code
$ClaudeMd = Join-Path $HomeDir ".claude\CLAUDE.md"
Inject-MarkdownBlock -FilePath $ClaudeMd -Block $MindsetMarkdown -Prepend $false
Write-Host "      [OK] Claude Code: Injected into $ClaudeMd" -ForegroundColor Green

# C. OpenAI Codex CLI
$CodexInstructions = Join-Path $HomeDir ".codex\instructions.md"
Inject-MarkdownBlock -FilePath $CodexInstructions -Block $MindsetMarkdown -Prepend $false
Write-Host "      [OK] OpenAI Codex: Injected into $CodexInstructions" -ForegroundColor Green

# D. Aider CLI
$AiderConventions = Join-Path $HomeDir ".aider\conventions.md"
Inject-MarkdownBlock -FilePath $AiderConventions -Block $MindsetMarkdown -Prepend $false
Write-Host "      [OK] Aider: Injected into $AiderConventions" -ForegroundColor Green

$AiderConf = Join-Path $HomeDir ".aider.conf.yml"
$aiderParent = Split-Path -Parent $AiderConf
if (-not (Test-Path $aiderParent)) {
    New-Item -ItemType Directory -Path $aiderParent -Force | Out-Null
}
$conventionsRef = "~/.aider/conventions.md"
if (Test-Path $AiderConf) {
    $aiderContent = Get-Content -Path $AiderConf -Raw -Encoding utf8
    if ($aiderContent -notmatch 'conventions\.md') {
        $updatedAider = $aiderContent.TrimEnd() + "`r`n`r`n# AegisBrain Mindset Integration`r`nread:`r`n  - $conventionsRef`r`n"
        [System.IO.File]::WriteAllText($AiderConf, $updatedAider, [System.Text.Encoding]::UTF8)
        Write-Host "      [OK] Aider: Added conventions reference to $AiderConf" -ForegroundColor Green
    } else {
        Write-Host "      [OK] Aider: $AiderConf already references conventions" -ForegroundColor Green
    }
} else {
    $initAider = "# AegisBrain Universal Mindset Configuration for Aider`r`nread:`r`n  - $conventionsRef`r`n"
    [System.IO.File]::WriteAllText($AiderConf, $initAider, [System.Text.Encoding]::UTF8)
    Write-Host "      [OK] Aider: Created $AiderConf" -ForegroundColor Green
}

# E. Workspace Injection (if active)
if ($ResolvedWorkspace) {
    $wsClaude = Join-Path $ResolvedWorkspace "CLAUDE.md"
    $wsAgents = Join-Path $ResolvedWorkspace "AGENTS.md"
    Inject-MarkdownBlock -FilePath $wsClaude -Block $MindsetMarkdown -Prepend $false
    Inject-MarkdownBlock -FilePath $wsAgents -Block $MindsetMarkdown -Prepend $false
    Write-Host "      [OK] Workspace: Injected into $wsClaude & $wsAgents" -ForegroundColor Green
}

# 6. Distribute Companion Skills
Write-Host "[3/5] Distributing Aegis Companion Skills..." -ForegroundColor Cyan
if (Test-Path $SkillSource) {
    $skillContent = Get-Content -Path $SkillSource -Raw -Encoding utf8
    $skillTargets = @(
        (Join-Path $HomeDir ".gemini\config\skills\aegis\SKILL.md"),
        (Join-Path $HomeDir ".claude\skills\aegis\SKILL.md"),
        (Join-Path $HomeDir ".codex\skills\aegis\SKILL.md")
    )
    foreach ($st in $skillTargets) {
        $sParent = Split-Path -Parent $st
        if (-not (Test-Path $sParent)) {
            New-Item -ItemType Directory -Path $sParent -Force | Out-Null
        }
        [System.IO.File]::WriteAllText($st, $skillContent, [System.Text.Encoding]::UTF8)
        Write-Host "      [OK] Skill installed: $st" -ForegroundColor Green
    }
}

# 7. Verification Gate
Write-Host "[4/5] Verifying Mindset Override Integrity..." -ForegroundColor Cyan
$verified = $true
$checkList = @($AntigravityGemini, $ClaudeMd, $CodexInstructions, $AiderConventions)
foreach ($chk in $checkList) {
    if (Test-Path $chk) {
        $txt = Get-Content -Path $chk -Raw -Encoding utf8
        if ($txt -match '<!-- AEGIS_BRAIN_MINDSET_START -->') {
            Write-Host "      [VERIFIED] $chk" -ForegroundColor Green
        } else {
            Write-Host "      [FAILED] Missing mindset marker in $chk" -ForegroundColor Red
            $verified = $false
        }
    }
}

if (-not $verified) {
    Write-Host "[!] Verification warnings detected. Check output above." -ForegroundColor Yellow
}

# 8. Complete & Output Rollback Instructions
Write-Host "[5/5] Installation Complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host " AegisBrain Universal Mindset Override successfully active!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host " Restore Point ID: $SnapshotId" -ForegroundColor White
Write-Host " Rollback Command: .\scripts\restore.ps1 -SnapshotId $SnapshotId" -ForegroundColor Yellow
Write-Host " (or 1-click restore anytime via: .\scripts\restore.ps1)" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
