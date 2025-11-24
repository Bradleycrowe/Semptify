# One-Push Startup for Semptify
param([switch]$Production, [switch]$NoOllama, [switch]$CheckOnly)

$ErrorActionPreference = "Continue"
$startTime = Get-Date

function Write-Step { param($msg) Write-Host "`n🔹 $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "   ✅ $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "   ⚠️  $msg" -ForegroundColor Yellow }
function Write-Fail { param($msg) Write-Host "   ❌ $msg" -ForegroundColor Red }

Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   🚀 SEMPTIFY - ONE-PUSH STARTUP 🚀          ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Green

# Validate environment
Write-Step "Validating environment..."
$pythonPath = ".\.venv\Scripts\python.exe"
if (!(Test-Path $pythonPath)) {
    Write-Fail "Virtual environment not found"
    Write-Host "   Run: python -m venv .venv`n" -ForegroundColor Yellow
    exit 1
}
$pythonVersion = & $pythonPath --version 2>&1
Write-Success "Python: $pythonVersion"

# Create required directories
$requiredDirs = @("uploads", "logs", "security", "data", "data/brad_clients", "uploads/vault", "copilot_sync", "final_notices")
foreach ($dir in $requiredDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Success "All directories ready"

# Check database
if (!(Test-Path "users.db")) {
    Write-Warning "Initializing database..."
    & $pythonPath -c "from user_database import init_database, init_remember_tokens_table; init_database(); init_remember_tokens_table()"
    Write-Success "Database initialized"
} else {
    Write-Success "Database ready"
}

# Check AI providers
Write-Step "Checking AI providers..."
$aiConfigured = $false
if ($env:OPENAI_API_KEY) {
    Write-Success "OpenAI configured"
    $aiConfigured = $true
}
if (!$NoOllama) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
        Write-Success "Ollama running with $($response.models.Count) models"
        $aiConfigured = $true
    } catch {
        Write-Warning "Ollama not running"
    }
}
if (!$aiConfigured) {
    Write-Warning "No AI providers - AI features limited"
}

# Check critical files
Write-Step "Checking application files..."
$files = @("Semptify.py", "brad_gui_routes.py", "brad_integration_routes.py")
$allOk = $true
foreach ($f in $files) {
    if (Test-Path $f) {
        Write-Success $f
    } else {
        Write-Fail "Missing: $f"
        $allOk = $false
    }
}
if (!$allOk) { exit 1 }

if ($CheckOnly) {
    Write-Host "`n✅ All checks passed!`n" -ForegroundColor Green
    exit 0
}

# Start application
Write-Step "Starting Semptify..."
$port = if ($env:PORT) { $env:PORT } else { "5000" }
Write-Host "`n   URL:  http://localhost:$port" -ForegroundColor Cyan
Write-Host "   Brad: http://localhost:$port/brad`n" -ForegroundColor Cyan

if (!$env:SECURITY_MODE) { $env:SECURITY_MODE = "open" }

$elapsed = (Get-Date) - $startTime
Write-Host "⏱️  Ready in $($elapsed.TotalSeconds.ToString('F2'))s`n" -ForegroundColor Gray
Write-Host "🚀 Starting server...`n" -ForegroundColor Green

try {
    if ($Production) {
        & $pythonPath run_prod.py
    } else {
        & $pythonPath Semptify.py
    }
} catch {
    Write-Fail "Failed: $_"
    exit 1
}
