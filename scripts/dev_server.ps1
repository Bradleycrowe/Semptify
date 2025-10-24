param(
  [switch]$Https,
  [string]$DataRoot,
  [switch]$AccessLog
)

$ErrorActionPreference = 'Stop'

# Move to repo root (this script lives in scripts/)
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venv = Join-Path $repoRoot '.venv'
$py = Join-Path $venv 'Scripts/python.exe'
$pip = Join-Path $venv 'Scripts/pip.exe'

if (-not (Test-Path $py)) {
  Write-Host 'Creating virtual environment (.venv)...'
  python -m venv .venv
}

Write-Host 'Ensuring dependencies are installed...'
& $pip install -r requirements.txt | Out-Host

# Environment for dev
$env:SECURITY_MODE = 'open'
if ($DataRoot) { $env:SEMPTIFY_DATA_ROOT = $DataRoot }
if ($AccessLog) { $env:ACCESS_LOG_JSON = '1' }

if ($Https) {
  Write-Host 'Starting HTTPS dev server...'
  & $py .\run_dev_ssl.py
} else {
  Write-Host 'Starting dev server...'
  & $py .\Semptify.py
}

