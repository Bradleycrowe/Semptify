param(
  [switch]$NoOpen
)
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[admin] $m" -ForegroundColor Cyan }
function Err($m){ Write-Host "[admin] $m" -ForegroundColor Red }

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$envFile = Join-Path $repo 'security/render.env'

if(Test-Path $envFile){
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
  Err "Env file not found: $envFile"; exit 1
}

$base = $env:RENDER_BASE_URL
$token = $env:ADMIN_TOKEN
if([string]::IsNullOrWhiteSpace($base)){ Err 'RENDER_BASE_URL missing in env'; exit 1 }
if([string]::IsNullOrWhiteSpace($token)){ Err 'ADMIN_TOKEN missing in env'; exit 1 }

$url = "$base/admin?token=$token"
Info "Admin URL: $url"
if(-not $NoOpen){ Start-Process $url }
