param(
  [string]$UserId = 'bradley',
  [string]$Name = 'Bradley Crowe'
)
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[user-bootstrap] $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host "[user-bootstrap] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[user-bootstrap] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[user-bootstrap] $m" -ForegroundColor Red }

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$usersPath = Join-Path $repo 'security/users.json'

# Generate a strong token
function New-RandomBase64Url([int]$bytes = 32){
  $buf = New-Object byte[] $bytes
  [System.Security.Cryptography.RandomNumberGenerator]::Fill($buf)
  $b64 = [Convert]::ToBase64String($buf)
  return ($b64 -replace '\+','-' -replace '/','_' -replace '=','')
}

# Compute sha256 in the app's format
function Get-TokenHash([string]$s){
  $bytes = [Text.Encoding]::UTF8.GetBytes($s)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $hashBytes = $sha.ComputeHash($bytes)
  $hex = -join ($hashBytes | ForEach-Object { $_.ToString('x2') })
  return "sha256:$hex"
}

$tokenPlain = New-RandomBase64Url 32
$user = @{ id = $UserId; name = $Name; hash = (Get-TokenHash $tokenPlain); enabled = $true }
$data = @()
if(Test-Path $usersPath){
  try { $data = Get-Content -Raw -Path $usersPath | ConvertFrom-Json } catch { $data = @() }
}
$data = @($data) + $user
($data | ConvertTo-Json -Depth 4) | Set-Content -Path $usersPath -Encoding UTF8
Ok "Created/updated $usersPath with user $UserId"
Write-Host "User token (store securely): $tokenPlain" -ForegroundColor Yellow
