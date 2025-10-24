<#
AllInOne-Push.ps1
Purpose: One-stop local pipeline: lint -> test -> build (with metadata) -> container smoke test -> SBOM (Syft) -> Trivy scan -> optional tag -> push.

Usage examples:
  ./AllInOne-Push.ps1 -Message "feat: add x" -TagAuto
  ./AllInOne-Push.ps1 -Message "chore: maintenance" -FailOnVuln
  ./AllInOne-Push.ps1 -SkipSBOM -SkipTrivy

Parameters:
  -Message        Commit message (default: chore: all-in-one autopush)
  -Tag            Explicit tag name (e.g. v1.2.3). Skips auto strategy.
  -TagAuto        If set and -Tag not supplied, creates timestamp tag vYYYYMMDDHHMMSS
  -FailOnVuln     Exit non-zero if Trivy finds HIGH/CRITICAL vulns
  -SkipSBOM       Skip SBOM generation
  -SkipTrivy      Skip vulnerability scan
  -SkipDocker     Skip docker build + smoke
  -SkipVenv       Skip virtual environment setup
  -Push           Actually push branch + tag (otherwise dry-run commit only)
  -DispatchCI     After push, attempt to dispatch ci.yml workflow via GitHub API (needs GITHUB_TOKEN env)

Outputs:
  sbom/sbom.json              (if SBOM not skipped)
  security/trivy-report.sarif (if Trivy not skipped; directory created if absent)

Prerequisites:
  - Docker installed (for Syft/Trivy container invocations)
  - Git configured
  - Python available
  - Optional env: GITHUB_TOKEN for workflow dispatch / tagging via API not required here (git tag local)
#>
param(
  [string]$Message = "chore: all-in-one autopush",
  [string]$Tag = "",
  [switch]$TagAuto,
  [switch]$FailOnVuln,
  [switch]$SkipSBOM,
  [switch]$SkipTrivy,
  [switch]$SkipDocker,
  [switch]$SkipVenv,
  [switch]$Push,
  [switch]$DispatchCI
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repo

# --- Helpers ---
function Info($m){ Write-Host "[AIO] $m" -ForegroundColor Cyan }
function Warn($m){ Write-Host "[AIO] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[AIO] $m" -ForegroundColor Red }
function Run($cmd){ Info $cmd; Invoke-Expression $cmd }

# --- Venv setup ---
$venv = Join-Path $repo '.venv'
if(-not $SkipVenv){
  if(-not (Test-Path (Join-Path $venv 'pyvenv.cfg'))){
    Info "(Re)creating venv"
    python -m venv .venv
  }
  . .\.venv\Scripts\Activate.ps1
  pip install --upgrade pip >$null
  pip install -q -r requirements.txt
  pip install -q ruff pytest || throw 'Dependency install failed'
}else{ Warn 'Skipping venv phase' }

# --- Lint ---
Info 'Linting with ruff'
try { ruff check . } catch { Err 'Lint failed'; throw }

# --- Tests ---
Info 'Running tests'
python -m pytest -q

$gitSha = (git rev-parse --short HEAD).Trim()
$buildTime = (Get-Date -Format o)

# --- Docker build & smoke ---
$imageName = 'Semptify:local'
if(-not $SkipDocker){
  Info "Building image $imageName (sha=$gitSha)"
  docker build --build-arg GIT_SHA=$gitSha --build-arg BUILD_TIME=$buildTime -t $imageName .
  Info 'Running container smoke test'
  $cid = docker run -d -p 127.0.0.1:8090:8080 --name semptify_aio $imageName
  Start-Sleep -Seconds 6
  try {
    $resp = Invoke-WebRequest -Uri 'http://127.0.0.1:8090/health' -UseBasicParsing -TimeoutSec 5
    if($resp.StatusCode -ne 200){ Warn "Health returned $($resp.StatusCode)" }
  } catch { Warn "Health check failed: $($_.Exception.Message)" }
  docker stop semptify_aio *> $null
  docker rm semptify_aio *> $null
}else{ Warn 'Skipping docker build & smoke' }

New-Item -ItemType Directory -Force -Path sbom | Out-Null
New-Item -ItemType Directory -Force -Path security | Out-Null

# --- SBOM ---
$sbomFile = 'sbom/sbom.json'
if(-not $SkipSBOM){
  if($SkipDocker){ Warn 'SBOM requires built image; building lightweight image'; docker build -t $imageName . }
  Info 'Generating SBOM (Syft container)'
  docker run --rm anchore/syft:latest $imageName -o json > $sbomFile
  if(-not (Test-Path $sbomFile) -or (Get-Item $sbomFile).Length -lt 50){ Err 'SBOM generation failed'; throw }
}else{ Warn 'Skipping SBOM generation' }

# --- Trivy scan ---
$trivySarif = 'security/trivy-report.sarif'
$vulnExit = 0
if(-not $SkipTrivy){
  if($SkipDocker){ Warn 'Trivy requires image; building image'; docker build -t $imageName . }
  Info 'Running Trivy vulnerability scan'
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --format sarif --output $trivySarif --severity HIGH,CRITICAL $imageName || ($vulnExit=$LASTEXITCODE)
  if(-not (Test-Path $trivySarif)){ Err 'Trivy SARIF not produced'; throw }
  if($FailOnVuln -and $vulnExit -ne 0){ Err 'Failing due to vulnerabilities'; throw 'Vulnerabilities found' }
}else{ Warn 'Skipping Trivy scan' }

# --- Git commit + optional tag ---
Info 'Staging changes (excluding bulky runtime)'
# Avoid adding uploads/logs/security
Get-ChildItem -Force | Out-Null

git add .dockerignore Dockerfile *.py templates/ sbom/ security/trivy-report.sarif 2>$null
if(Test-Path $sbomFile){ git add $sbomFile }
try { git commit -m $Message } catch { Warn 'Nothing to commit or commit failed (maybe no changes)' }

if([string]::IsNullOrWhiteSpace($Tag)){
  if($TagAuto){ $Tag = 'v' + (Get-Date -Format 'yyyyMMddHHmmss') }
}
if(-not [string]::IsNullOrWhiteSpace($Tag)){
  if(-not (git tag -l $Tag)){ git tag $Tag; Info "Created tag $Tag" } else { Warn "Tag $Tag already exists" }
}

if($Push){
  Info 'Pushing branch'
  git push origin main
  if(-not [string]::IsNullOrWhiteSpace($Tag)){ git push origin $Tag }
} else {
  Warn 'Push skipped (use -Push to enable)'
}

# --- Optional workflow dispatch ---
if($DispatchCI -and $Push){
  if($env:GITHUB_TOKEN){
    $owner = $env:GITHUB_OWNER; if(-not $owner){ $owner='Bradleycrowe' }
    $repoName = $env:GITHUB_REPO; if(-not $repoName){ $repoName='Semptify' }
    $body = '{"ref":"main"}'
    $url = "https://api.github.com/repos/$owner/$repoName/actions/workflows/ci.yml/dispatches"
    Info 'Dispatching CI workflow'
    try {
      Invoke-RestMethod -Method Post -Uri $url -Headers @{Authorization="token $($env:GITHUB_TOKEN)"; Accept='application/vnd.github+json'} -Body $body
    } catch { Warn "Workflow dispatch failed: $($_.Exception.Message)" }
  } else { Warn 'GITHUB_TOKEN not set; cannot dispatch workflow' }
}

Write-Host ''
Write-Host '========== All-In-One Summary ==========' -ForegroundColor Green
Write-Host "Commit Message : $Message"
Write-Host "Tag            : $([string]::IsNullOrWhiteSpace($Tag) ? 'none' : $Tag)"
Write-Host "Pushed         : $Push"
Write-Host "SBOM           : $([bool](-not $SkipSBOM)) -> $sbomFile"
Write-Host "Trivy Scan     : $([bool](-not $SkipTrivy)) -> $trivySarif"
Write-Host "FailOnVuln     : $FailOnVuln (exit=$vulnExit)"
Write-Host "Docker Built   : $([bool](-not $SkipDocker))"
Write-Host "Git SHA        : $gitSha"
Write-Host '=========================================' -ForegroundColor Green

