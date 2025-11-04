# ============================================================
# Semptify Production Web Server Startup Script (PowerShell)
# Starts Flask with Waitress WSGI server
# ============================================================

param(
    [int]$Port = 8080,
    [string]$Host = "0.0.0.0",
    [int]$Threads = 4,
    [string]$Environment = "production"
)

# ============================================================
# CONFIGURATION
# ============================================================

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$scriptName = "Semptify Production Server"
$pythonScript = "start_production.py"
$venvPath = ".\.venv"
$venvActivate = "$venvPath\Scripts\Activate.ps1"

# ============================================================
# FUNCTIONS
# ============================================================

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan -NoNewline
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Warning-Message {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

# ============================================================
# STARTUP CHECKS
# ============================================================

Write-Header " $scriptName Startup "

# Check if Python is installed
Write-Info "Checking Python installation..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
} catch {
    Write-Error-Message "Python not found. Please install Python 3.8+"
    exit 1
}

# Check if virtual environment exists
Write-Info "Checking virtual environment..."
if (-not (Test-Path $venvPath)) {
    Write-Warning-Message "Virtual environment not found at $venvPath"
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
    Write-Success "Virtual environment created"
} else {
    Write-Success "Virtual environment found"
}

# Activate virtual environment
Write-Info "Activating virtual environment..."
& $venvActivate

# Check if requirements are installed
Write-Info "Checking dependencies..."
$requiredPackages = @("flask", "waitress", "requests")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        $null = python -m pip show $package 2>&1
        Write-Success "Package installed: $package"
    } catch {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Warning-Message "Missing packages: $($missingPackages -join ', ')"
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
    Write-Success "Requirements installed"
} else {
    Write-Success "All required packages are installed"
}

# Check required directories
Write-Info "Checking required directories..."
$dirs = @("uploads", "logs", "security", "copilot_sync", "final_notices", "data")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Success "Created directory: $dir"
    } else {
        Write-Success "Directory exists: $dir"
    }
}

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

Write-Info "Setting environment variables..."

# Set Flask environment
$env:FLASK_ENV = $Environment
$env:FLASK_DEBUG = "0"

# Set server configuration
$env:SEMPTIFY_PORT = $Port
$env:SEMPTIFY_HOST = $Host
$env:SEMPTIFY_THREADS = $Threads

# Security
if (-not $env:FLASK_SECRET) {
    Write-Warning-Message "FLASK_SECRET not set. Using development default."
    $env:FLASK_SECRET = "dev-secret-change-in-production"
}

# Ensure security mode is set
if (-not $env:SECURITY_MODE) {
    $env:SECURITY_MODE = "enforced"
    Write-Info "SECURITY_MODE set to: enforced"
}

Write-Success "Environment variables configured"

# ============================================================
# STARTUP INFO
# ============================================================

Write-Header " SERVER CONFIGURATION "

Write-Host "Host:                $Host"
Write-Host "Port:                $Port"
Write-Host "Threads:             $Threads"
Write-Host "Environment:         $Environment"
Write-Host "Python:              $pythonVersion"
Write-Host "Working Directory:   $(Get-Location)"
Write-Host ""

# ============================================================
# START SERVER
# ============================================================

Write-Header " STARTING SEMPTIFY PRODUCTION SERVER "

Write-Host "🚀 Server starting at http://$($Host):$Port" -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Cyan
Write-Host ""

# Start the production server
try {
    & python $pythonScript
} catch {
    Write-Error-Message "Failed to start server: $_"
    exit 1
}
