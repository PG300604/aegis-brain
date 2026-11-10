# AegisBrain Live Interactive Terminal Demo Runner
# Use this script when recording with Recordly or Windows Terminal
# It launches separate windows and types each command with realistic delays.

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " AegisBrain Live Terminal Demo Runner (for Recordly)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "1. Open Recordly (C:\Users\priya\AppData\Local\Programs\Recordly\Recordly.exe)" -ForegroundColor Yellow
Write-Host "2. Hit Record in Recordly" -ForegroundColor Yellow
Write-Host "3. Press any key in this window to start the automated demo..." -ForegroundColor Yellow
Write-Host ""
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

function Send-Keystrokes ($text, $delayMs = 40) {
    foreach ($char in $text.ToCharArray()) {
        [System.Windows.Forms.SendKeys]::SendWait($char)
        Start-Sleep -Milliseconds $delayMs
    }
    Start-Sleep -Milliseconds 400
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
}

Add-Type -AssemblyName System.Windows.Forms

# Step 1: Mock Project Briefing
Clear-Host
Write-Host "PS P:\open-source\mock-aegis-demo> " -NoNewline -ForegroundColor Gray
Start-Sleep -Seconds 1
Write-Host "aegis briefing" -ForegroundColor White
Start-Sleep -Milliseconds 600
cd P:\open-source\mock-aegis-demo
aegis briefing
Start-Sleep -Seconds 4

# Step 2: Sub-Second Neural Memory Bus Recall
Write-Host ""
Write-Host "PS P:\open-source\mock-aegis-demo> " -NoNewline -ForegroundColor Gray
Start-Sleep -Seconds 1
Write-Host 'aegis recall "rate limiter"' -ForegroundColor White
Start-Sleep -Milliseconds 600
aegis recall "rate limiter"
Start-Sleep -Seconds 4

# Step 3: Dynamic Severity & Workload Triage
Write-Host ""
Write-Host "PS P:\open-source\mock-aegis-demo> " -NoNewline -ForegroundColor Gray
Start-Sleep -Seconds 1
Write-Host 'aegis triage "Implement TokenBucketLimiter with Redis burst protection"' -ForegroundColor White
Start-Sleep -Milliseconds 600
aegis triage "Implement TokenBucketLimiter with Redis burst protection"
Start-Sleep -Seconds 4

# Step 4: 4-Decision Quality Architecture Gate & Pytest
Write-Host ""
Write-Host "PS P:\open-source\mock-aegis-demo> " -NoNewline -ForegroundColor Gray
Start-Sleep -Seconds 1
Write-Host "uv run pytest tests/test_limiter.py -v" -ForegroundColor White
Start-Sleep -Milliseconds 600
uv run pytest tests/test_limiter.py -v
Start-Sleep -Seconds 4

# Step 5: Zero-Residue Snapshot Rollback
Write-Host ""
Write-Host "PS P:\open-source\mock-aegis-demo> " -NoNewline -ForegroundColor Gray
Start-Sleep -Seconds 1
Write-Host 'aegis snapshot create --reason "pre-production demo"' -ForegroundColor White
Start-Sleep -Milliseconds 600
aegis snapshot create --reason "pre-production demo"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "PS P:\open-source\mock-aegis-demo> " -NoNewline -ForegroundColor Gray
Start-Sleep -Seconds 1
Write-Host "aegis restore 1" -ForegroundColor White
Start-Sleep -Milliseconds 600
aegis restore 1
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " [DEMO COMPLETE] Stop recording in Recordly!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
