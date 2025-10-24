param(
  [Parameter(Mandatory=$true)][string]$BaseUrl,
  [int]$TimeoutSeconds = 180,
  [int]$IntervalSeconds = 3,
  [switch]$Json
)
$ErrorActionPreference='Stop'

function Test-Endpoint {
  param([string]$Path,[int[]]$AcceptCodes)
  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while((Get-Date) -lt $deadline){
    try {
      $r = Invoke-WebRequest -Uri ("$BaseUrl$Path") -UseBasicParsing -TimeoutSec 10
      $code = [int]$r.StatusCode
      if($AcceptCodes -contains $code){ return @{ path=$Path; code=$code; ok=$true } }
      return @{ path=$Path; code=$code; ok=$false }
    } catch {
      # Capture status code for non-2xx responses
      try {
        $resp = $_.Exception.Response
        if($null -ne $resp -and $resp.StatusCode){
          $code = [int]$resp.StatusCode
          if($AcceptCodes -contains $code){ return @{ path=$Path; code=$code; ok=$true } }
          return @{ path=$Path; code=$code; ok=$false }
        }
      } catch {}
      Start-Sleep -Seconds $IntervalSeconds
    }
  }
  return @{ path=$Path; code=-1; ok=$false }
}

$checks = @(
  @{ path='/'; accept=@(200) },
  @{ path='/resources'; accept=@(200) },
  @{ path='/resources/witness_statement'; accept=@(200) },
  @{ path='/resources/filing_packet'; accept=@(200) },
  @{ path='/resources/service_animal'; accept=@(200) },
  @{ path='/resources/move_checklist'; accept=@(200) },
  @{ path='/static/css/app.css'; accept=@(200) },
  @{ path='/static/manifest.webmanifest'; accept=@(200) },
  @{ path='/vault'; accept=@(200,401,403) } # 401/403 expected without user_token
)

$results = @()
foreach($c in $checks){
  $res = Test-Endpoint -Path $c.path -AcceptCodes $c.accept
  $results += $res
}

if($Json){
  $obj = [ordered]@{}
  foreach($r in $results){ $obj[$r.path] = @{ code=$r.code; ok=$r.ok } }
  $obj | ConvertTo-Json -Depth 3
} else {
  Write-Host "Full smoke results for $BaseUrl" -ForegroundColor Cyan
  foreach($r in $results){
    $color = if($r.ok){ 'Green' } else { 'Red' }
    Write-Host ("{0,-32} {1}" -f $r.path, $r.code) -ForegroundColor $color
  }
  if(-not ($results | Where-Object { -not $_.ok } | Measure-Object).Count){
    Write-Host "All checks passed." -ForegroundColor Green
    exit 0
  } else {
    Write-Host "Some checks failed." -ForegroundColor Red
    exit 1
  }
}
