# Semptify Unified Startup Script
Write-Host "================================" -ForegroundColor Cyan
Write-Host "   SEMPTIFY STARTUP" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Semptify\Semptify"

# Check if server already running
$existing = Get-Process python -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[INFO] Semptify already running" -ForegroundColor Yellow
    Write-Host "[OK] Opening dashboard..." -ForegroundColor Green
    Start-Process "http://localhost:5000/"
    Start-Sleep -Seconds 2
    exit
}

Write-Host "[START] Starting Semptify server..." -ForegroundColor Green
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "Semptify.py" -WorkingDirectory "C:\Semptify\Semptify" -WindowStyle Hidden

Write-Host "[WAIT] Initializing..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# Test if server is responding
try {
    $null = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
    Write-Host "[OK] Server running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  Opening Semptify Dashboard" -ForegroundColor White
    Write-Host "  http://localhost:5000" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Start-Process "http://localhost:5000/"
    Start-Sleep -Seconds 2
} catch {
    Write-Host "[ERROR] Server failed to start!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
