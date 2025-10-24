<#!
.SYNOPSIS
One-and-done: lint, test, build, (optional SBOM/scan), push, trigger Render deploy, poll, and smoke.

.PARAMETER Message
Commit message (default: chore: one-and-done)
.PARAMETER Push
Actually push to main (default: true)
.PARAMETER FailOnVuln
Fail if Trivy finds HIGH/CRITICAL (default: false)
.PARAMETER SkipSBOM
Skip SBOM generation
.PARAMETER SkipTrivy
Skip vulnerability scan
.PARAMETER SkipDocker
Skip docker build + smoke
.PARAMETER TimeoutMinutes
Render deploy wait timeout (default: 15)

.ENVIRONMENT
RENDER_API_KEY, RENDER_SERVICE_ID (required for deploy)
RENDER_BASE_URL (optional for smoke)
#>
[CmdletBinding()]
param(
  [string]$Message = 'chore: one-and-done',
  [bool]$Push = $true,
  [switch]$FailOnVuln,
  [switch]$SkipSBOM,
  [switch]$SkipTrivy,
  [switch]$SkipDocker,
  [switch]$SkipDeploy,
  [int]$TimeoutMinutes = 15
)
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[OAD] $m" -ForegroundColor Cyan }
function Warn($m){ Write-Host "[OAD] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[OAD] $m" -ForegroundColor Red }

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $repo

# Opportunistically import env vars for Render from security/render.env or .env
function Import-EnvFile {
  param([string]$Path)
  if(-not (Test-Path $Path)){ return }
  Info "Loading env from $Path"
  Get-Content -Raw -Path $Path | ForEach-Object {
    $_ -split "`n" | ForEach-Object {
      $line = $_.Trim()
      if([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith('#')){ return }
      $idx = $line.IndexOf('=')
      if($idx -lt 1){ return }
      $key = $line.Substring(0,$idx).Trim()
      $val = $line.Substring($idx+1).Trim().Trim('"').Trim("'")
      if($key){ ${env:$key} = $val }
    }
  }
}
$cand1 = Join-Path $repo 'security/render.env'
$cand2 = Join-Path $repo '.env'
if(Test-Path $cand1){ Import-EnvFile $cand1 } elseif(Test-Path $cand2){ Import-EnvFile $cand2 }

# venv minimal
function New-Venv {
  if(Test-Path .venv){
    Info 'Removing broken venv'
    try {
      Remove-Item -Recurse -Force .venv -ErrorAction Stop
    } catch {
      Warn "Direct delete failed: $($_.Exception.Message). Attempting rename workaround"
      $bak = ".venv.bak.$([DateTime]::UtcNow.ToString('yyyyMMddHHmmssfff'))"
      try { Rename-Item -Path .venv -NewName $bak -ErrorAction Stop; Start-Sleep -Milliseconds 250 } catch { Warn "Rename also failed: $($_.Exception.Message)" }
    }
  }
  Info 'Creating venv'
  try { python -m venv .venv } catch { Info 'Retry creating venv via py launcher'; py -3 -m venv .venv }
}
if(-not (Test-Path .venv\Scripts\Activate.ps1)){
  New-Venv
}
. .\.venv\Scripts\Activate.ps1

function Initialize-Pip {
  try { python -m pip --version | Out-Null; return } catch {}
  Info 'Bootstrapping pip via ensurepip (--default-pip)'
  try { python -m ensurepip --default-pip | Out-Null; python -m pip --version | Out-Null; return } catch {}
  $gp = Join-Path (Get-Location) '.venv/get-pip.py'
  Info 'Bootstrapping pip via get-pip.py --force-reinstall'
  Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile $gp -UseBasicParsing
  python $gp --force-reinstall | Out-Null
}

Initialize-Pip
if($LASTEXITCODE -ne 0){ Warn 'pip still not available; recreating venv and retrying pip bootstrap'; New-Venv; . .\.venv\Scripts\Activate.ps1; Initialize-Pip }
$UseDockerCI = $false
try { python -m pip --version | Out-Null } catch { Warn 'pip is not available even after retry; switching lint/tests to Docker fallback'; $UseDockerCI = $true }
function Invoke-Pip { param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
  $pipExe = Join-Path (Get-Location) '.venv/Scripts/pip.exe'
  if(Test-Path $pipExe){ & $pipExe @Args }
  else { python -m pip @Args }
}
if(-not $UseDockerCI){
  Invoke-Pip install -q --upgrade pip
  Invoke-Pip install -q -r requirements-dev.txt
  if($LASTEXITCODE -ne 0){ Warn 'pip install failed; switching lint/tests to Docker fallback'; $UseDockerCI = $true }
}

# Lint + tests
if(-not $UseDockerCI){
  Info 'Linting (ruff)'
  python -m ruff check .
  Info 'Running tests'
  python -m pytest -q
} else {
  if(-not (Get-Command docker -ErrorAction SilentlyContinue)){
    Err 'Neither local Python nor Docker is available for lint/tests. Please run in Dev Container/WSL or install Docker Desktop.'
    throw 'no execution environment'
  }
  Info 'Using Docker fallback for lint/tests'
  $cmd = "pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt pytest ruff && ruff check . && pytest -q"
  docker run --rm -v "${pwd}:/app" -w /app python:3.13-slim bash -lc $cmd
}

# Docker build + smoke (local)
$image='Semptify:oad'
if(-not $SkipDocker){
  if(-not (Get-Command docker -ErrorAction SilentlyContinue)){
    Warn 'Docker not found; skipping docker build & smoke'
  } else {
  Info 'Building docker image'
  docker build -t $image .
  Info 'Local health smoke'
  $null = docker run -d -p 127.0.0.1:8091:8080 --name semptify_oad $image
  Start-Sleep -Seconds 6
  try { (Invoke-WebRequest 'http://127.0.0.1:8091/health' -UseBasicParsing).StatusCode | Out-Null } catch { Warn 'Local smoke failed' }
  docker rm -f semptify_oad *> $null
  }
} else { Warn 'Skipping docker build & smoke' }

# SBOM & Trivy
New-Item -ItemType Directory -Force -Path sbom | Out-Null
New-Item -ItemType Directory -Force -Path security | Out-Null
if(-not $SkipSBOM){
  if($SkipDocker){ Warn 'SBOM requires a built image; building image'; docker build -t $image . }
  Info 'Generating SBOM (Syft)'
  docker run --rm anchore/syft:latest $image -o json > sbom/sbom.json
}
if(-not $SkipTrivy){
  if($SkipDocker){ Warn 'Trivy requires a built image; building image'; docker build -t $image . }
  Info 'Trivy scan'
  $code=0; docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --format sarif --output security/trivy-report.sarif --severity HIGH,CRITICAL $image || ($code=$LASTEXITCODE)
  if($FailOnVuln -and $code -ne 0){ Err 'Vulnerabilities found'; throw }
}

# Commit & push
git add -A
try { git commit -m $Message } catch { Warn 'Nothing to commit' }
if($Push){ git push origin main } else { Warn 'Push disabled' }

# Render deploy
if(-not $SkipDeploy){
  Info 'Trigger Render deploy'
  & "$repo\scripts\deploy_render.ps1" -TimeoutMinutes $TimeoutMinutes
  Info 'Done.'
} else { Warn 'Skipping deploy' }

