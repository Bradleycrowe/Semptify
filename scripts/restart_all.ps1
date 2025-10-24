<#!
.SYNOPSIS
    Full clean restart of Semptify (local dev / pre-deploy) on Windows PowerShell.
.DESCRIPTION
    Recreates virtual environment (optional), installs dependencies, purges runtime folders (except security allowlist),
    optionally generates an ADMIN_TOKEN & FLASK_SECRET, runs tests, and (optionally) starts the dev or production server.
.PARAMETER ForceVenv
    If set, removes existing .venv and recreates it.
.PARAMETER Prod
    If set, runs run_prod.py with waitress instead of the debug Flask dev server.
.PARAMETER KeepLogs
    If set, preserves existing logs directory contents.
.PARAMETER GenToken
    If set, generates a random ADMIN_TOKEN and exports it for the session.
.PARAMETER Enforced
    If set, sets SECURITY_MODE=enforced (otherwise open).
.PARAMETER SkipTests
    If set, skips running pytest.
.PARAMETER AutoStart
    If set, automatically launches the server after setup.
.EXAMPLE
    ./scripts/restart_all.ps1 -ForceVenv -GenToken -Enforced -AutoStart -Prod
#>
[CmdletBinding()]
param(
    [switch]$ForceVenv,
    [switch]$Prod,
    [switch]$KeepLogs,
    [switch]$GenToken,
    [switch]$Enforced,
    [switch]$SkipTests,
    [switch]$AutoStart
)
$ErrorActionPreference = 'Stop'

function Write-Info($msg){ Write-Host "[*] $msg" -ForegroundColor Cyan }
function Write-Ok($msg){ Write-Host "[+] $msg" -ForegroundColor Green }
function Write-Warn($msg){ Write-Host "[!] $msg" -ForegroundColor Yellow }
function Write-Err($msg){ Write-Host "[x] $msg" -ForegroundColor Red }

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $RepoRoot
Write-Info "Repo root: $RepoRoot"

$venv = Join-Path $RepoRoot '.venv'
if($ForceVenv -and (Test-Path $venv)){
    Write-Info 'Removing existing virtual environment (.venv)'
    Remove-Item -Recurse -Force $venv
}
if(!(Test-Path $venv)){
    Write-Info 'Creating virtual environment (.venv)'
    python -m venv .venv
}
Write-Info 'Activating venv'
. .\.venv\Scripts\Activate.ps1

Write-Info 'Upgrading pip'
python -m pip install --upgrade pip >$null

Write-Info 'Installing requirements'
pip install -r requirements.txt

$RuntimeDirs = @('uploads','logs','copilot_sync','final_notices')
foreach($d in $RuntimeDirs){
    $path = Join-Path $RepoRoot $d
    if(Test-Path $path){
        if($d -eq 'logs' -and $KeepLogs){
            Write-Info "Preserving logs in $d"; continue
        }
        Write-Info "Purging $d/*"
        Get-ChildItem -Force -LiteralPath $path | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    } else { New-Item -ItemType Directory -Path $path | Out-Null }
}

# Ensure security dir exists
$secDir = Join-Path $RepoRoot 'security'
if(!(Test-Path $secDir)){ New-Item -ItemType Directory -Path $secDir | Out-Null }

if($GenToken){
    $token = -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 48 | % {[char]$_})
    $env:ADMIN_TOKEN = $token
    Write-Ok "Generated ADMIN_TOKEN (NOT persisted)." 
}
if(-not $env:FLASK_SECRET){
    $env:FLASK_SECRET = [Guid]::NewGuid().ToString('N') + [Guid]::NewGuid().ToString('N')
    Write-Ok 'Generated FLASK_SECRET for session.'
}
$env:SECURITY_MODE = if($Enforced){ 'enforced' } else { 'open' }
Write-Info "SECURITY_MODE=$($env:SECURITY_MODE)"

if(-not $SkipTests){
    Write-Info 'Running tests (pytest -q)'
    try {
        python -m pytest -q
        Write-Ok 'Tests passed'
    } catch {
        Write-Err 'Tests failed'
        throw
    }
}

if($AutoStart){
    if($Prod){
        Write-Info 'Starting production server (waitress)'
        python run_prod.py
    } else {
        Write-Info 'Starting development server (Flask debug)'
        python Semptify.py
    }
} else {
    Write-Ok 'Restart sequence completed. Use -AutoStart to auto-run next time.'
    Write-Host 'Manual start (dev): .\.venv\Scripts\Activate.ps1; python Semptify.py'
    Write-Host 'Manual start (prod): .\.venv\Scripts\Activate.ps1; python run_prod.py'
}

