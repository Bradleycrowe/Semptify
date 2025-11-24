# Semptify Production Server - PowerShell Launcher
# Uses Waitress WSGI server (production-grade)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Semptify Production Server" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is running
Write-Host "[1/4] Checking Ollama AI service..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "  ✓ Ollama is running" -ForegroundColor Green
    $models = ($response.Content | ConvertFrom-Json).models.name
    Write-Host "  Models: $($models -join ', ')" -ForegroundColor Gray
} catch {
    Write-Host "  ⚠ Ollama not running, attempting to start..." -ForegroundColor Red
    $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama app.exe"
    if (Test-Path $ollamaPath) {
        Start-Process -FilePath $ollamaPath
        Write-Host "  Waiting for Ollama to start..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
    } else {
        Write-Host "  ✗ Ollama not installed. Install from: https://ollama.com/download" -ForegroundColor Red
    }
}

# Check R2 configuration
Write-Host "[2/4] Checking R2 storage configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "R2_ACCESS_KEY_ID=(?!your_)") {
        Write-Host "  ✓ R2 configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ R2 not configured (using local storage)" -ForegroundColor Yellow
    }
}

# Activate virtual environment
Write-Host "[3/4] Activating Python environment..." -ForegroundColor Yellow
Set-Location "C:\Semptify\Semptify"
& ".\.venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Start Production Server
Write-Host "[4/4] Starting production server (Waitress)..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  🚀 Semptify Production Server (Waitress)" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Web UI:     http://localhost:8080" -ForegroundColor White
Write-Host "  Profiles:   http://localhost:8080/profiles" -ForegroundColor White
Write-Host "  Admin:      http://localhost:8080/admin" -ForegroundColor White
Write-Host ""
Write-Host "  Server:     Waitress (Production WSGI)" -ForegroundColor Cyan
Write-Host "  AI Backend: Ollama (Local)" -ForegroundColor Cyan
Write-Host "  Storage:    R2 Auto-sync" -ForegroundColor Cyan
Write-Host "  Threads:    8 workers" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Press Ctrl+C to stop server" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$env:SEMPTIFY_PORT = "8080"
python run_prod.py
