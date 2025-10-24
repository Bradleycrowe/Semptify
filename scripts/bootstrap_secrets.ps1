param(
  [switch]$Force,
  [switch]$ShowHash
)
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[secrets] $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host "[secrets] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[secrets] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[secrets] $m" -ForegroundColor Red }

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$envFile = Join-Path $repo 'security/render.env'

function New-RandomBase64Url([int]$bytes = 32){
  $buf = New-Object byte[] $bytes
  [System.Security.Cryptography.RandomNumberGenerator]::Fill($buf)
  $b64 = [Convert]::ToBase64String($buf)
  # Convert to URL-safe (drop padding)
  return ($b64 -replace '\+','-' -replace '/','_' -replace '=','')
}

function Get-FileLinesOrEmpty([string]$path){
  if(Test-Path $path){ return Get-Content -Raw -Path $path -Encoding UTF8 -ErrorAction Stop -EA Stop -ea Stop -ReadCount 0 -TotalCount 0 -Delimiter ([Environment]::NewLine) }
  return @()
}

function Upsert-Key([string[]]$lines, [string]$key, [string]$value){
  $found = $false
  for($i=0; $i -lt $lines.Count; $i++){
    $line = $lines[$i].Trim()
    if($line -and -not $line.StartsWith('#') -and $line.StartsWith("$key=")){
      $lines[$i] = "$key=$value"
      $found = $true
      break
    }
  }
  if(-not $found){ $lines += "$key=$value" }
  return ,$lines
}

Info "Ensuring security/render.env contains strong FLASK_SECRET and ADMIN_TOKEN"

$lines = @()
if(Test-Path $envFile){
  $lines = Get-Content -Path $envFile -Encoding UTF8
} else {
  Warn "Creating $envFile (not committed to git)"
}

# Read existing values if present
$existing = @{ }
foreach($ln in $lines){
  $t = $ln.Trim()
  if($t -and -not $t.StartsWith('#')){
    $idx = $t.IndexOf('=')
    if($idx -gt 0){ $existing[$t.Substring(0,$idx)] = $t.Substring($idx+1) }
  }
}

$needSecret = $Force -or -not $existing.ContainsKey('FLASK_SECRET') -or [string]::IsNullOrWhiteSpace($existing['FLASK_SECRET'])
$needAdmin  = $Force -or -not $existing.ContainsKey('ADMIN_TOKEN') -or [string]::IsNullOrWhiteSpace($existing['ADMIN_TOKEN'])

if($needSecret){
  $secret = New-RandomBase64Url 32
  $lines = Upsert-Key $lines 'FLASK_SECRET' $secret
  Ok "Generated FLASK_SECRET"
} else { Info "FLASK_SECRET already present (use -Force to rotate)" }

if($needAdmin){
  $admin = New-RandomBase64Url 32
  $lines = Upsert-Key $lines 'ADMIN_TOKEN' $admin
  Ok "Generated ADMIN_TOKEN"
} else { Info "ADMIN_TOKEN already present (use -Force to rotate)" }

# Write back
$lines | Set-Content -Path $envFile -Encoding UTF8
Ok "Updated $envFile"

if($ShowHash){
  $adminVal = (Select-String -Path $envFile -Pattern '^ADMIN_TOKEN=').Line.Split('=')[1]
  $bytes = [Text.Encoding]::UTF8.GetBytes($adminVal)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $hashBytes = $sha.ComputeHash($bytes)
  $hex = -join ($hashBytes | ForEach-Object { $_.ToString('x2') })
  $full = "sha256:$hex"
  Write-Host "Suggested admin_tokens.json entry (optional multi-token setup):" -ForegroundColor Yellow
  Write-Host "[ {`"id`": `"primary`", `"hash`": `"$full`", `"enabled`": true } ]" -ForegroundColor Yellow
}

Info "Remember to add these in Render Dashboard secrets if not syncing from env file: FLASK_SECRET, ADMIN_TOKEN"
Ok "Done."
