<#
.SYNOPSIS
    AegisBrain Universal Agent Mindset Rollback Script.
.DESCRIPTION
    Restores all agent configurations, prompts, and rules back to their exact pre-override
    state with ZERO RESIDUE.
.PARAMETER SnapshotId
    Optional snapshot ID to restore. If omitted, restores the latest mindset snapshot.
.PARAMETER Force
    Bypass interactive confirmation prompt.
#>
[CmdletBinding()]
param(
    [string]$SnapshotId = "",
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " AegisBrain Universal Agent Mindset Rollback & Restore" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

$HomeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile) }
$SnapshotsDir = Join-Path $HomeDir ".aegis-brain\snapshots"
$LatestPointer = Join-Path $SnapshotsDir "LATEST_MINDSET_SNAPSHOT.txt"

# 1. Discover all valid snapshots
$SnapshotsList = @()
if (Test-Path $SnapshotsDir) {
    Get-ChildItem -Path $SnapshotsDir -Directory | Sort-Object Name -Descending | ForEach-Object {
        $mPath = Join-Path $_.FullName "manifest.json"
        if (Test-Path $mPath) {
            try {
                $mData = Get-Content -Path $mPath -Raw -Encoding utf8 | ConvertFrom-Json
                $SnapshotsList += [PSCustomObject]@{
                    Id = $_.Name
                    Date = if ($mData.created_at) { $mData.created_at } else { $_.CreationTime.ToString("yyyy-MM-dd HH:mm:ss") }
                    Reason = if ($mData.reason) { $mData.reason } else { "manual" }
                    Files = if ($mData.file_count) { $mData.file_count } else { 0 }
                    Path = $_.FullName
                }
            } catch {}
        }
    }
}

if ($SnapshotsList.Count -eq 0) {
    Write-Host "[ERROR] No restore points found in $SnapshotsDir" -ForegroundColor Red
    exit 1
}

# 2. Interactive Selection Menu or Parameter Resolution
$TargetSnapshotId = $SnapshotId
if (-not $TargetSnapshotId -and -not $Force -and -not $env:CI -and -not $env:NONINTERACTIVE) {
    Write-Host " Available Configuration Restore Points:" -ForegroundColor White
    Write-Host "--------------------------------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host (" {0,-5} {1,-20} {2,-6} {3,-30} {4}" -f "#", "Date / Time", "Files", "Snapshot ID", "Reason") -ForegroundColor Cyan
    Write-Host "--------------------------------------------------------------------------------------------" -ForegroundColor DarkGray

    $maxShow = [Math]::Min($SnapshotsList.Count, 20)
    for ($i = 0; $i -lt $maxShow; $i++) {
        $s = $SnapshotsList[$i]
        $num = "[{0,2}]" -f ($i + 1)
        $rShort = if ($s.Reason.Length -gt 32) { $s.Reason.Substring(0, 29) + "..." } else { $s.Reason }
        Write-Host (" {0,-5} {1,-20} {2,5}   {3,-30} {4}" -f $num, $s.Date, $s.Files, $s.Id, $rShort) -ForegroundColor Gray
    }
    Write-Host "--------------------------------------------------------------------------------------------" -ForegroundColor DarkGray
    if ($SnapshotsList.Count -gt $maxShow) {
        Write-Host " (Showing newest $maxShow of $($SnapshotsList.Count) snapshots)" -ForegroundColor DarkGray
    }
    Write-Host ""

    try {
        $sel = Read-Host "Select snapshot number to restore [1..$($SnapshotsList.Count)], ID, or Enter for latest [1] (or 'q' to quit)"
        $sel = $sel.Trim()
        if ($sel -match '^[qQ]') {
            Write-Host "[AegisBrain] Restore cancelled." -ForegroundColor Yellow
            exit 0
        } elseif ($sel -match '^\d+$') {
            $idx = [int]$sel - 1
            if ($idx -ge 0 -and $idx -lt $SnapshotsList.Count) {
                $TargetSnapshotId = $SnapshotsList[$idx].Id
            } else {
                Write-Host "[ERROR] Invalid selection '$sel'. Must be between 1 and $($SnapshotsList.Count)." -ForegroundColor Red
                exit 1
            }
        } elseif ($sel) {
            $TargetSnapshotId = $sel
        } else {
            $TargetSnapshotId = $SnapshotsList[0].Id
        }
    } catch {
        $TargetSnapshotId = $SnapshotsList[0].Id
    }
} elseif (-not $TargetSnapshotId) {
    # Non-interactive / Force default
    if (Test-Path $LatestPointer) {
        $TargetSnapshotId = (Get-Content -Path $LatestPointer -Raw -Encoding utf8).Trim()
    } else {
        $TargetSnapshotId = $SnapshotsList[0].Id
    }
} elseif ($TargetSnapshotId -match '^\d+$') {
    # Numeric index passed via parameter
    $idx = [int]$TargetSnapshotId - 1
    if ($idx -ge 0 -and $idx -lt $SnapshotsList.Count) {
        $TargetSnapshotId = $SnapshotsList[$idx].Id
    }
}

$SnapshotTargetDir = Join-Path $SnapshotsDir $TargetSnapshotId
if (-not (Test-Path $SnapshotTargetDir)) {
    # Check partial match
    $candidates = Get-ChildItem -Path $SnapshotsDir -Directory | Where-Object { $_.Name -like "*$TargetSnapshotId*" }
    if ($candidates) {
        $SnapshotTargetDir = $candidates[0].FullName
        $TargetSnapshotId = $candidates[0].Name
    } else {
        Write-Host "[ERROR] Snapshot '$TargetSnapshotId' does not exist in $SnapshotsDir" -ForegroundColor Red
        exit 1
    }
}

$ManifestPath = Join-Path $SnapshotTargetDir "manifest.json"
if (-not (Test-Path $ManifestPath)) {
    Write-Host "[ERROR] Corrupt snapshot: missing manifest.json in $SnapshotTargetDir" -ForegroundColor Red
    exit 1
}

$Manifest = Get-Content -Path $ManifestPath -Raw -Encoding utf8 | ConvertFrom-Json

Write-Host " Identified Restore Point:" -ForegroundColor White
Write-Host "   Snapshot ID : $($Manifest.snapshot_id)" -ForegroundColor Yellow
Write-Host "   Created At  : $($Manifest.created_at)" -ForegroundColor Yellow
Write-Host "   Reason      : $($Manifest.reason)" -ForegroundColor Yellow
Write-Host "   Backed Files: $($Manifest.file_count)" -ForegroundColor Yellow
Write-Host ""

if (-not $Force -and [System.Environment]::UserInteractive -and -not $env:CI -and -not $env:NONINTERACTIVE) {
    try {
        $resp = Read-Host "Proceed with restoring this snapshot? All post-snapshot changes will be reverted. [Y/n]"
        if ($resp -match '^[nN]') {
            Write-Host "[AegisBrain] Rollback cancelled by user." -ForegroundColor Yellow
            exit 0
        }
    } catch {
        # Non-interactive fallback
    }
}

Write-Host "[1/4] Restoring pre-override configuration files..." -ForegroundColor Cyan
$restoredCount = 0
$restoreErrors = @()

foreach ($file in $Manifest.files) {
    $origPath = $file.original_path
    $backupPath = Join-Path $SnapshotTargetDir $file.backup_path

    if (Test-Path $backupPath) {
        try {
            $parent = Split-Path -Parent $origPath
            if (-not (Test-Path $parent)) {
                New-Item -ItemType Directory -Path $parent -Force | Out-Null
            }
            Copy-Item -Path $backupPath -Destination $origPath -Force
            $restoredCount++
            Write-Host "      [RESTORED] $origPath" -ForegroundColor Green
        } catch {
            $msg = "$($origPath): $($_.Exception.Message)"
            $restoreErrors += $msg
            Write-Host "      [FAIL] $msg" -ForegroundColor Red
        }
    } else {
        $msg = "Backup missing for $($origPath) at $($backupPath)"
        $restoreErrors += $msg
        Write-Host "      [WARN] $msg" -ForegroundColor Yellow
    }
}

Write-Host "[2/4] Removing newly created files (Zero Residue)..." -ForegroundColor Cyan
$cleanedFilesCount = 0
if ($Manifest.created_files) {
    foreach ($createdPath in $Manifest.created_files) {
        if (Test-Path $createdPath -PathType Leaf) {
            try {
                Remove-Item -Path $createdPath -Force
                $cleanedFilesCount++
                Write-Host "      [REMOVED] $createdPath" -ForegroundColor Green
            } catch {
                Write-Host "      [WARN] Could not remove $($createdPath) : $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
    }
}

Write-Host "[3/4] Cleaning up empty installer-created directories..." -ForegroundColor Cyan
$cleanedDirsCount = 0
if ($Manifest.created_dirs) {
    # Reverse to clean deepest directories first
    $reversedDirs = [System.Collections.ArrayList]@($Manifest.created_dirs)
    $reversedDirs.Reverse()

    foreach ($createdDir in $reversedDirs) {
        if (Test-Path $createdDir -PathType Container) {
            $items = Get-ChildItem -Path $createdDir -Force
            if ($items.Count -eq 0) {
                try {
                    Remove-Item -Path $createdDir -Force -Recurse
                    $cleanedDirsCount++
                    Write-Host "      [CLEANED] Empty directory: $createdDir" -ForegroundColor Green
                } catch {
                    # Ignore directory removal errors if locked or in use
                }
            }
        }
    }
}

Write-Host "[4/4] Executing defense-in-depth residual marker check..." -ForegroundColor Cyan
# Ensure no stray marker remains in any monitored file
$allMonitored = @(
    (Join-Path $HomeDir ".gemini\config\GEMINI.md"),
    (Join-Path $HomeDir ".claude\CLAUDE.md"),
    (Join-Path $HomeDir ".codex\instructions.md"),
    (Join-Path $HomeDir ".aider\conventions.md")
)
if ($Manifest.workspace) {
    $allMonitored += (Join-Path $Manifest.workspace "CLAUDE.md")
    $allMonitored += (Join-Path $Manifest.workspace "AGENTS.md")
}

foreach ($targetFile in $allMonitored) {
    if (Test-Path $targetFile -PathType Leaf) {
        $raw = Get-Content -Path $targetFile -Raw -Encoding utf8
        if ($raw -match '<!-- AEGIS_BRAIN_MINDSET_START -->[\s\S]*?<!-- AEGIS_BRAIN_MINDSET_END -->') {
            $stripped = [regex]::Replace($raw, '(?m)^\s*<!-- AEGIS_BRAIN_MINDSET_START -->[\s\S]*?<!-- AEGIS_BRAIN_MINDSET_END -->\s*$', '').Trim()
            $utf8NoBom = New-Object System.Text.UTF8Encoding $false
            if ($stripped.Length -eq 0 -and ($Manifest.created_files -contains $targetFile)) {
                Remove-Item -Path $targetFile -Force
                Write-Host "      [CLEANED] Empty residual file removed: $targetFile" -ForegroundColor Green
            } else {
                [System.IO.File]::WriteAllText($targetFile, $stripped, $utf8NoBom)
                Write-Host "      [SCRUBBED] Stripped residual mindset marker from: $targetFile" -ForegroundColor Green
            }
        }
    }
}

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Mindset override rolled back successfully with ZERO RESIDUE!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host " Summary:" -ForegroundColor White
Write-Host "   Files Restored : $restoredCount" -ForegroundColor Green
Write-Host "   Files Removed  : $cleanedFilesCount" -ForegroundColor Green
Write-Host "   Dirs Cleaned   : $cleanedDirsCount" -ForegroundColor Green
if ($restoreErrors.Count -gt 0) {
    Write-Host "   Warnings       : $($restoreErrors.Count)" -ForegroundColor Yellow
}
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
