# Production Server Startup for Semptify
param([int]$Port = 8080, [switch]$CheckOnly)
$ErrorActionPreference = "Continue"

function Write-Step { param($msg) Write-Host "`n🔹 $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "   ✅ $msg" -ForegroundColor Green }
function Write-Warning { param($msg) Write-Host "   ⚠️  $msg" -ForegroundColor Yellow }

Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   �� SEMPTIFY PRODUCTION SERVER 🚀           ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Step "Validating production environment..."
$pythonPath = ".\.venv\Scripts\python.exe"
if (!(Test-Path $pythonPath)) {
    Write-Host "   ❌ Virtual environment not found" -ForegroundColor Red
    exit 1
}
Write-Success "Python ready"

# Check Waitress
try {
    $waitressCheck = & $pythonPath -c "import waitress; print('OK')" 2>&1
    if ($waitressCheck -match "OK") {
        Write-Success "Waitress WSGI server installed"
    } else {
        throw "Not installed"
    }
} catch {
    Write-Warning "Installing Waitress..."
    & $pythonPath -m pip install waitress --quiet
    Write-Success "Waitress installed"
}

# Create directories
$dirs = @("uploads", "logs", "security", "data", "data/brad_clients", "uploads/vault")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
}
Write-Success "Directories ready"

# Database
if (!(Test-Path "users.db")) {
    Write-Warning "Initializing database..."
    & $pythonPath -c "from user_database import init_database, init_remember_tokens_table; init_database(); init_remember_tokens_table()"
    Write-Success "Database initialized"
} else {
    Write-Success "Database ready"
}

# AI check
Write-Step "Checking AI providers..."
$aiCount = 0
if ($env:OPENAI_API_KEY) { 
    Write-Success "OpenAI configured"
    $aiCount++
}
try {
    Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 1 -ErrorAction Stop | Out-Null
    Write-Success "Ollama running"
    $aiCount++
} catch {}
if ($aiCount -eq 0) { Write-Warning "No AI providers" }

if ($CheckOnly) {
    Write-Host "`n✅ Production ready!`n" -ForegroundColor Green
    exit 0
}

# Production config
$env:SECURITY_MODE = "open"
$env:PORT = $Port
$env:FLASK_ENV = "production"

Write-Step "Starting production server..."
$localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' } | Select-Object -First 1).IPAddress
Write-Host "`n   📍 Binding: 0.0.0.0:$Port" -ForegroundColor Gray
Write-Host "   🌐 Local:   http://localhost:$Port" -ForegroundColor Cyan
Write-Host "   🌐 Network: http://${localIp}:$Port" -ForegroundColor Cyan
Write-Host "   🎯 Brad:    http://localhost:$Port/brad" -ForegroundColor Cyan
Write-Host "`n   ⚙️  Threads: 4 | Timeout: 120s" -ForegroundColor Gray
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "🚀 Server starting... (Ctrl+C to stop)" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray

& $pythonPath run_prod.py
