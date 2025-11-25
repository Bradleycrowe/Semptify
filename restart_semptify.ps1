# Restart Semptify with Production Server
# PowerShell version for quick restarts

Write-Host ""
Write-Host "🔄 RESTARTING SEMPTIFY" -ForegroundColor Cyan
Write-Host "=" * 60

# Kill existing processes
Write-Host ""
Write-Host "🛑 Stopping existing Semptify processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*Semptify.py*" -or $_.CommandLine -like "*run_prod.py*"
} | Stop-Process -Force
Start-Sleep -Seconds 2

# Check if port is free
Write-Host "🔍 Checking port 5000..." -ForegroundColor Yellow
$port = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
if ($port) {
    Write-Host "⚠️  Port 5000 in use, waiting..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

# Start production server
Write-Host ""
Write-Host "🚀 Starting production server (Waitress)..." -ForegroundColor Green
Write-Host ""

Set-Location "C:\Semptify\Semptify"

# Check if run_prod.py exists
if (Test-Path "run_prod.py") {
    Write-Host "Starting with run_prod.py..." -ForegroundColor Cyan
    Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "run_prod.py" -NoNewWindow
} else {
    Write-Host "Starting with Semptify.py..." -ForegroundColor Cyan
    Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "Semptify.py" -NoNewWindow
}

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "✅ SEMPTIFY RESTARTED!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access at:" -ForegroundColor Cyan
Write-Host "   http://localhost:5000" -ForegroundColor Gray
Write-Host "   http://localhost:5000/hub" -ForegroundColor Gray
Write-Host "   http://localhost:5000/jurisdiction/dashboard" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Server running in background. Use Task Manager to stop." -ForegroundColor Yellow
Write-Host ""
