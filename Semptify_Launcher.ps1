# Semptify One-Click Launcher (ASCII-safe)
# Starts Ollama, validates environment, launches server, opens GUI

$ErrorActionPreference = "Continue"

function Write-Header {
  param([string]$text)
  Write-Host "`n==================== $text ====================" -ForegroundColor Cyan
}

function Wait-ForUrl {
  param([string]$Url, [int]$TimeoutSeconds = 15)
  for ($i = 0; $i -lt $TimeoutSeconds; $i++) {
    try {
      Invoke-WebRequest -Uri $Url -TimeoutSec 1 -ErrorAction Stop | Out-Null
      return $true
    } catch {
      Start-Sleep -Seconds 1
    }
  }
  return $false
}

Write-Header "Semptify Launcher"
Write-Host "Starting system..." -ForegroundColor Gray

# 1) Start Ollama
Write-Header "1/5 Ollama"
$ollamaOk = $false
try {
  Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop | Out-Null
  $ollamaOk = $true
  Write-Host "[OK] Ollama is running" -ForegroundColor Green
} catch {
  $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama app.exe"
  if (Test-Path $ollamaPath) {
    Write-Host "[INFO] Starting Ollama..." -ForegroundColor Yellow
    Start-Process -FilePath $ollamaPath -WindowStyle Hidden | Out-Null
    $ollamaOk = Wait-ForUrl -Url "http://localhost:11434/api/tags" -TimeoutSeconds 20
    if ($ollamaOk) { Write-Host "[OK] Ollama started" -ForegroundColor Green } else { Write-Host "[WARN] Ollama not ready yet; continuing" -ForegroundColor Yellow }
  } else {
    Write-Host "[WARN] Ollama not installed. AI features disabled." -ForegroundColor Yellow
  }
}

# 2) Python venv
Write-Header "2/5 Python Env"
$venvPy = "C:\Semptify\Semptify\.venv\Scripts\python.exe"
if (Test-Path $venvPy) {
  Write-Host "[OK] Virtual environment detected" -ForegroundColor Green
} else {
  Write-Host "[ERROR] Virtual environment not found at $venvPy" -ForegroundColor Red
  Write-Host "        Run: python -m venv .venv" -ForegroundColor Gray
  Read-Host "Press Enter to exit"
  exit 1
}

# 3) Storage config
Write-Header "3/5 Storage"
if (Test-Path ".env") {
  $envContent = Get-Content ".env" -Raw
  if ($envContent -match "R2_ACCESS_KEY_ID=(?!your_)") { Write-Host "[OK] R2 configured" -ForegroundColor Green }
  else { Write-Host "[WARN] R2 not configured; using local storage" -ForegroundColor Yellow }
} else {
  Write-Host "[WARN] .env not found; using defaults" -ForegroundColor Yellow
}

# 4) Start server
Write-Header "4/5 Server"
Set-Location "C:\Semptify\Semptify"
$port = "8080"
$env:SEMPTIFY_PORT = $port

$serverJob = Start-Job -ScriptBlock {
  param($venvPyInner, $portInner)
  try {
    Set-Location "C:\Semptify\Semptify"
    $env:SEMPTIFY_PORT = $portInner
    & $venvPyInner "run_prod.py"
  } catch {
    Write-Host "[ERROR] Server failed: $($_.Exception.Message)" -ForegroundColor Red
  }
} -ArgumentList $venvPy, $port

Write-Host "[INFO] Waiting for server on http://localhost:$port" -ForegroundColor Gray
$serverReady = Wait-ForUrl -Url "http://localhost:$port" -TimeoutSeconds 20
if ($serverReady) { Write-Host "[OK] Server is up" -ForegroundColor Green } else { Write-Host "[WARN] Server not responding yet" -ForegroundColor Yellow }

# 5) Open GUI
Write-Header "5/5 GUI"
Start-Process "http://localhost:$port/gui" | Out-Null
Write-Host "[OK] GUI opened in browser" -ForegroundColor Green

Write-Host ""; Write-Host "Semptify is running. Close this window to stop." -ForegroundColor Cyan

# Monitor job
try {
  while ($true) {
    $state = (Get-Job -Id $serverJob.Id).State
    if ($state -ne "Running") {
      Write-Host "[WARN] Server stopped (state: $state)" -ForegroundColor Yellow
      break
    }
    Receive-Job -Id $serverJob.Id -Keep -ErrorAction SilentlyContinue | ForEach-Object { Write-Host $_ -ForegroundColor DarkGray }
    Start-Sleep -Seconds 2
  }
}
finally {
  Stop-Job -Id $serverJob.Id -ErrorAction SilentlyContinue | Out-Null
  Remove-Job -Id $serverJob.Id -Force -ErrorAction SilentlyContinue | Out-Null
  Write-Host "[OK] Semptify stopped" -ForegroundColor Green
}
