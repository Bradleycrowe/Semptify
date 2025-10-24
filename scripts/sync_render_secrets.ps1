<#
.SYNOPSIS
Sync critical environment variables/secrets to a Render service via API.

.DESCRIPTION
Reads security/render.env, ensures FLASK_SECRET and ADMIN_TOKEN exist (generating if missing),
and attempts to upsert the full set of production env vars to the specified Render service.
If the API shape changes, the script fails gracefully with clear next steps.

.ENVIRONMENT
RENDER_API_KEY      Render API key (required)
RENDER_SERVICE_ID   Render Service ID (required)

.USAGE
pwsh ./scripts/sync_render_secrets.ps1
pwsh ./scripts/sync_render_secrets.ps1 -Verbose
#>
[CmdletBinding()]
param(
  [switch]$ForceGenerate
)
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[secrets-sync] $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host "[secrets-sync] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[secrets-sync] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[secrets-sync] $m" -ForegroundColor Red }

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $scriptDir
$envFile = Join-Path $repo 'security/render.env'

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

function Ensure-LocalSecrets {
  if(-not (Test-Path $envFile)){ return }
  $need = $ForceGenerate -or [string]::IsNullOrWhiteSpace($env:FLASK_SECRET) -or [string]::IsNullOrWhiteSpace($env:ADMIN_TOKEN)
  if($need){
    Info 'Ensuring FLASK_SECRET and ADMIN_TOKEN exist locally (bootstrap if missing)'
    & (Join-Path $repo 'scripts/bootstrap_secrets.ps1') | Out-Null
    Import-EnvFile $envFile
  }
}

Import-EnvFile $envFile
Ensure-LocalSecrets

$api = $env:RENDER_API_KEY
$svc = $env:RENDER_SERVICE_ID
if([string]::IsNullOrWhiteSpace($api)){ Err 'Missing RENDER_API_KEY (set in security/render.env)'; exit 1 }
if([string]::IsNullOrWhiteSpace($svc)){ Err 'Missing RENDER_SERVICE_ID (set in security/render.env)'; exit 1 }

# Desired production vars
$desired = @{
  'FLASK_SECRET' = $env:FLASK_SECRET
  'ADMIN_TOKEN'  = $env:ADMIN_TOKEN
  'SECURITY_MODE' = ($env:SECURITY_MODE | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'enforced'}else{$_} })
  'FORCE_HTTPS' = ($env:FORCE_HTTPS | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'1'}else{$_} })
  'HSTS_MAX_AGE' = ($env:HSTS_MAX_AGE | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'31536000'}else{$_} })
  'HSTS_PRELOAD' = ($env:HSTS_PRELOAD | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'1'}else{$_} })
  'ACCESS_LOG_JSON' = ($env:ACCESS_LOG_JSON | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'1'}else{$_} })
  'ADMIN_RATE_WINDOW' = ($env:ADMIN_RATE_WINDOW | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'60'}else{$_} })
  'ADMIN_RATE_MAX' = ($env:ADMIN_RATE_MAX | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'60'}else{$_} })
  'ADMIN_RATE_STATUS' = ($env:ADMIN_RATE_STATUS | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'429'}else{$_} })
  'SEMPTIFY_PORT' = ($env:SEMPTIFY_PORT | ForEach-Object { if([string]::IsNullOrWhiteSpace($_)){'8080'}else{$_} })
}

foreach($k in @('FLASK_SECRET','ADMIN_TOKEN')){
  if([string]::IsNullOrWhiteSpace($desired[$k])){ Err "$k is empty; cannot sync"; exit 1 }
}

$headers = @{ Authorization = "Bearer $api"; Accept='application/json' }
$envArray = @()
foreach($kv in $desired.GetEnumerator()){
  $envArray += @{ key = $kv.Key; value = [string]$kv.Value }
}
$body = @{ clear = $false; envVars = $envArray } | ConvertTo-Json -Depth 4 -Compress

Info 'Syncing env vars to Render (attempt 1: POST)'
try {
  Invoke-RestMethod -Method Post -Uri "https://api.render.com/v1/services/$svc/env-vars" -Headers $headers -ContentType 'application/json' -Body $body -ErrorAction Stop | Out-Null
  Ok 'Env vars updated via POST'
} catch {
  Warn ("POST /env-vars failed: " + $_.Exception.Message + ' ; trying PUT')
  try {
    Invoke-RestMethod -Method Put -Uri "https://api.render.com/v1/services/$svc/env-vars" -Headers $headers -ContentType 'application/json' -Body $body -ErrorAction Stop | Out-Null
    Ok 'Env vars updated via PUT'
  } catch {
    Err ("PUT /env-vars failed: " + $_.Exception.Message)
    Warn 'Could not sync env vars via API. Please set the keys in the Render Dashboard manually.'
    exit 2
  }
}

Ok 'Secrets sync complete.'
