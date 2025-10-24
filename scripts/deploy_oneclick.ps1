param(
  [int]$TimeoutMinutes = 25,
  [switch]$NoSmoke,
  [switch]$NoOpen
)
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[oneclick] $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host "[oneclick] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[oneclick] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[oneclick] $m" -ForegroundColor Red }

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$envFile = Join-Path $repo 'security/render.env'

if(Test-Path $envFile){
  Info "Loading env from $envFile"
  Get-Content -Raw -Path $envFile | ForEach-Object {
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
} else {
  Warn "Env file not found at $envFile; relying on current shell env vars."
}

$api  = $env:RENDER_API_KEY
$svc  = $env:RENDER_SERVICE_ID
$base = $env:RENDER_BASE_URL

if([string]::IsNullOrWhiteSpace($api)) { Err 'Missing RENDER_API_KEY (set in security/render.env)'; exit 1 }
if([string]::IsNullOrWhiteSpace($svc)) { Err 'Missing RENDER_SERVICE_ID (set in security/render.env)'; exit 1 }
if([string]::IsNullOrWhiteSpace($base)) { Warn 'RENDER_BASE_URL not set; smoke and auto-open will be skipped' }

# Ensure secrets exist and sync to Render first
Info "Syncing secrets to Render"
try {
  pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path (Join-Path $repo 'scripts') 'sync_render_secrets.ps1')
} catch {
  Warn "Secrets sync reported an error: $($_.Exception.Message). Continuing to deploy; ensure secrets are set in Render."
}

Info "Triggering deploy (no prompts)"
$deployArgs = @('-File', (Join-Path (Join-Path $repo 'scripts') 'deploy_render.ps1'), '-TimeoutMinutes', $TimeoutMinutes, '-ApiKey', $api, '-ServiceId', $svc)
if(-not [string]::IsNullOrWhiteSpace($base)) { $deployArgs += @('-BaseUrl', $base) }
if($NoSmoke){ $deployArgs += @('-SkipSmoke') }

pwsh -NoProfile -ExecutionPolicy Bypass @deployArgs

if(-not $NoOpen -and -not [string]::IsNullOrWhiteSpace($base)){
  try {
    Start-Process $base
    Ok "Opened $base"
  } catch {
    Warn "Could not open browser: $($_.Exception.Message)"
  }
}

Ok 'Done.'
