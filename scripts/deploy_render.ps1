<#!
.SYNOPSIS
Trigger a Render deploy, poll until live, and run smoke checks.

.DESCRIPTION
Uses Render API to trigger a deploy for the configured service, polls deploy status until live (or timeout),
and optionally runs smoke checks against RENDER_BASE_URL.

.PARAMETER TimeoutMinutes
Max minutes to wait for deploy to become live. Default: 15

.PARAMETER SkipSmoke
If set, skip smoke checks even if RENDER_BASE_URL is provided.

.ENVIRONMENT
RENDER_API_KEY      Render API key (required)
RENDER_SERVICE_ID   Render Service ID (required)
RENDER_BASE_URL     Base URL for smoke (optional), e.g. https://Semptify.onrender.com

.EXAMPLE
pwsh ./scripts/deploy_render.ps1

.EXAMPLE
pwsh ./scripts/deploy_render.ps1 -TimeoutMinutes 20
#>
[CmdletBinding()]
param(
  [int]$TimeoutMinutes = 15,
  [switch]$SkipSmoke,
  [string]$ApiKey,
  [string]$ServiceId,
  [string]$BaseUrl,
  [string]$DeployHookUrl
)
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[deploy] $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host "[deploy] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[deploy] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[deploy] $m" -ForegroundColor Red }

# Load env vars from a .env-like file (KEY=VALUE), ignoring comments and blanks
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

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $scriptDir

# If required envs are missing, try to load from security/render.env, then .env
if([string]::IsNullOrWhiteSpace($env:RENDER_API_KEY) -or [string]::IsNullOrWhiteSpace($env:RENDER_SERVICE_ID) -or [string]::IsNullOrWhiteSpace($env:RENDER_BASE_URL) -or [string]::IsNullOrWhiteSpace($env:RENDER_DEPLOY_HOOK_URL)){
  $cand1 = Join-Path $repo 'security/render.env'
  $cand2 = Join-Path $repo '.env'
  if(Test-Path $cand1){ Import-EnvFile $cand1 }
  elseif(Test-Path $cand2){ Import-EnvFile $cand2 }
}

# Precedence: parameters > env vars (possibly loaded) > prompt interactively
$apiKey = if(-not [string]::IsNullOrWhiteSpace($ApiKey)) { $ApiKey } else { $env:RENDER_API_KEY }
$svcId = if(-not [string]::IsNullOrWhiteSpace($ServiceId)) { $ServiceId } else { $env:RENDER_SERVICE_ID }
$hook = if(-not [string]::IsNullOrWhiteSpace($DeployHookUrl)) { $DeployHookUrl } else { $env:RENDER_DEPLOY_HOOK_URL }
if([string]::IsNullOrWhiteSpace($apiKey)){
  Warn 'RENDER_API_KEY not provided. You can avoid this prompt by setting env vars or security/render.env.'
  $sec = Read-Host 'Enter Render API Key' -AsSecureString
  $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
  try { $apiKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto($ptr) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}
if([string]::IsNullOrWhiteSpace($svcId)){
  Warn 'RENDER_SERVICE_ID not provided. You can avoid this prompt by setting env vars or security/render.env.'
  $svcId = Read-Host 'Enter Render Service ID'
}
if([string]::IsNullOrWhiteSpace($svcId)){ throw 'Missing RENDER_SERVICE_ID' }

# If no API key but a deploy hook was provided, we'll use the hook path without API operations
$usingHookOnly = $false
if([string]::IsNullOrWhiteSpace($apiKey) -and -not [string]::IsNullOrWhiteSpace($hook)){
  $usingHookOnly = $true
  Warn 'No API key provided; will use Deploy Hook to trigger deploy and skip API-based preflight.'
}

# Utilities
function Format-Secret { param([string]$k) if([string]::IsNullOrWhiteSpace($k)){ return '(empty)' } if($k.Length -gt 10){ return ($k.Substring(0,4) + '...' + $k.Substring($k.Length-4)) } else { return '(short-key)' } }
function Get-HttpStatus { param($Err) try { return [int]$Err.Exception.Response.StatusCode } catch { return $null } }

$headers = if(-not [string]::IsNullOrWhiteSpace($apiKey)) { @{ Authorization = "Bearer $apiKey"; Accept='application/json' } } else { @{} }

if(-not $usingHookOnly){
  # Preflight: validate that the API key can access the service
  Info ("Preflight: checking access to service $svcId with key " + (Format-Secret $apiKey))
  try {
    $svcMeta = Invoke-RestMethod -Method Get -Uri "https://api.render.com/v1/services/$svcId" -Headers $headers -ErrorAction Stop
    if(-not $svcMeta){ Warn 'Preflight: received empty service metadata (continuing)'}
  } catch {
    $code = Get-HttpStatus $_
    if($code -eq 401){ Err 'Unauthorized: API key is invalid or belongs to another account/team.'; throw }
    elseif($code -eq 404){ Err "Service not found: verify the Service ID belongs to the same account/team as the API key ($svcId)"; throw }
    else { Err ("Preflight failed: " + $_.Exception.Message); throw }
  }
}

Info "Triggering deploy for service $svcId"
$payload = @{ clearCache = $false }
$json = $payload | ConvertTo-Json -Compress
function Invoke-DeployHook {
  param([string]$HookUrl)
  Info 'Triggering deploy via Deploy Hook URL'
  try {
    Invoke-RestMethod -Method Post -Uri $HookUrl -ErrorAction Stop | Out-Null
    Ok 'Deploy hook accepted'
  } catch {
    Warn ("Deploy hook POST failed: " + $_.Exception.Message + "; trying GET")
    Invoke-RestMethod -Method Get -Uri $HookUrl -ErrorAction Stop | Out-Null
    Ok 'Deploy hook GET accepted'
  }
}

try {
  if($usingHookOnly){
    if([string]::IsNullOrWhiteSpace($hook)){ throw 'Missing RENDER_DEPLOY_HOOK_URL for hook-only mode' }
    Invoke-DeployHook -HookUrl $hook
    $resp = $null
  } else {
    $resp = Invoke-RestMethod -Method Post -Uri "https://api.render.com/v1/services/$svcId/deploys" -Headers $headers -ContentType 'application/json' -Body $json -ErrorAction Stop
  }
} catch {
  $msg = $_.ErrorDetails.Message
  if(-not $msg){ $msg = $_.Exception.Message }
  if($msg -match 'invalid JSON'){
    Warn "Server said 'invalid JSON' with clearCache payload; retrying with '{}'"
    try {
      $resp = Invoke-RestMethod -Method Post -Uri "https://api.render.com/v1/services/$svcId/deploys" -Headers $headers -ContentType 'application/json' -Body '{}' -ErrorAction Stop
    } catch {
      $msg2 = $_.ErrorDetails.Message; if(-not $msg2){ $msg2 = $_.Exception.Message }
      if($msg2 -match 'invalid JSON'){
        if(-not [string]::IsNullOrWhiteSpace($hook)){
          Warn "Server still says 'invalid JSON'; falling back to Deploy Hook URL"
          Invoke-DeployHook -HookUrl $hook
          $resp = $null
        } else {
          Warn "Server still says 'invalid JSON'; retrying with no body"
          $resp = Invoke-RestMethod -Method Post -Uri "https://api.render.com/v1/services/$svcId/deploys" -Headers $headers -Method Post -ErrorAction Stop
        }
      } else { throw }
    }
  } else { throw }
}
if($null -ne $resp){
  $deployId = $resp.id
} else {
  # No response (hook mode). Try to resolve latest deploy id via API if possible
  if(-not [string]::IsNullOrWhiteSpace($apiKey)){
    try {
      $list = Invoke-RestMethod -Method Get -Uri "https://api.render.com/v1/services/$svcId/deploys" -Headers $headers -ErrorAction Stop
      if($list -is [System.Array]){ $deployId = $list[0].id } else { $deployId = $list.id }
    } catch {
      Warn "Could not resolve deploy id after hook trigger; will skip polling"
      $deployId = $null
    }
  } else {
    Warn 'Hook triggered without API key; skipping polling'
    $deployId = $null
  }
}
if($deployId){ Ok "Deploy created: $deployId" }

$deadline = (Get-Date).AddMinutes($TimeoutMinutes)
$phaseHistory = @()
$last = ''
function Get-DeployStatus {
  param([string]$Id)
  try {
    return Invoke-RestMethod -Method Get -Uri "https://api.render.com/v1/deploys/$Id" -Headers $headers -ErrorAction Stop
  } catch {
    $code = Get-HttpStatus $_
    if($code -eq 404){
      try {
        return Invoke-RestMethod -Method Get -Uri "https://api.render.com/v1/services/$svcId/deploys/$Id" -Headers $headers -ErrorAction Stop
      } catch { throw }
    }
    throw
  }
}
while((Get-Date) -lt $deadline){
  try {
    $d = Get-DeployStatus -Id $deployId
  } catch {
    Warn "Polling error: $($_.Exception.Message)"; Start-Sleep -Seconds 5; continue
  }
  $phase = $d.status
  if($phase -ne $last){ $phaseHistory += "$(Get-Date -AsUTC -Format o) $phase"; $last = $phase }
  Info "Phase: $phase"
  switch ($phase) {
    'live' { Ok 'Deploy is live'; break }
    'build_failed' { Err 'Build failed'; throw 'Render build failed' }
    'deactivated' { Err 'Service deactivated'; throw 'Render service deactivated' }
    'canceled' { Err 'Deploy canceled'; throw 'Render deploy canceled' }
    'failed' { Err 'Deploy failed'; throw 'Render deploy failed' }
  }
  Start-Sleep -Seconds 8
}
if($last -ne 'live'){ throw "Timed out waiting for live (last=$last)" }

if(-not $SkipSmoke){
  $base = if(-not [string]::IsNullOrWhiteSpace($BaseUrl)) { $BaseUrl } else { $env:RENDER_BASE_URL }
  if(-not [string]::IsNullOrWhiteSpace($base)){
    Info "Running smoke against $base"
    try {
      $code1 = (Invoke-WebRequest -Uri "$base/health" -UseBasicParsing -TimeoutSec 10).StatusCode
      $code2 = (Invoke-WebRequest -Uri "$base/readyz" -UseBasicParsing -TimeoutSec 10).StatusCode
      if($code1 -ne 200 -or $code2 -ne 200){ throw "Smoke failed /health=$code1 /readyz=$code2" }
      Ok 'Smoke OK'
    } catch {
      Err "Smoke test failed: $($_.Exception.Message)"; throw
    }
  } else {
    Warn 'RENDER_BASE_URL not set; skipping smoke'
  }
} else { Warn 'SkipSmoke set; skipping smoke checks' }

Write-Host ''
Write-Host '==== Render Deploy Summary ====' -ForegroundColor Green
Write-Host "Service     : $svcId"
Write-Host "Deploy ID   : $deployId"
Write-Host "Status      : live"
Write-Host 'Phase trail :'
$phaseHistory | ForEach-Object { Write-Host "  $_" }
Write-Host '===============================' -ForegroundColor Green

