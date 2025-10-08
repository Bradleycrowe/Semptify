param(
    [Parameter(Mandatory=$true)][string]$BaseUrl,
    [string]$AdminToken,
    [int]$TimeoutSeconds = 120,
    [int]$IntervalSeconds = 5,
    [switch]$Json
)

Write-Host "Starting smoke test against $BaseUrl" -ForegroundColor Cyan
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)

function Wait-EndpointOk {
    param([string]$Path)
    while((Get-Date) -lt $deadline){
        try {
            $resp = Invoke-WebRequest -Uri ("$BaseUrl$Path") -UseBasicParsing -TimeoutSec 10
            if($resp.StatusCode -eq 200){ return $resp }
        } catch { }
        Write-Host "Waiting for $Path ..." -ForegroundColor DarkGray
        Start-Sleep -Seconds $IntervalSeconds
    }
    throw "Timeout waiting for $Path"
}

# 1. Health
$health = Wait-EndpointOk -Path "/health"
Write-Host "Health OK" -ForegroundColor Green

# 2. Version
$version = Wait-EndpointOk -Path "/version"
Write-Host "Version: $($version.Content)" -ForegroundColor Green

# 3. Admin (best-effort)
try {
    $adminUrl = "/admin"
    if($AdminToken){
        $adminUrl = "$adminUrl?token=$AdminToken"
    }
    $admin = Invoke-WebRequest -Uri ("$BaseUrl$adminUrl") -UseBasicParsing -TimeoutSec 10
    if($admin.StatusCode -eq 200){
        if($admin.Content -match "SECURITY MODE: ENFORCED"){
            Write-Host "Admin reachable (enforced mode)." -ForegroundColor Green
        } elseif($admin.Content -match "SECURITY MODE: OPEN") {
            Write-Host "Admin reachable (open mode)." -ForegroundColor Green
        } else {
            Write-Host "Admin reachable (banner not detected)." -ForegroundColor Yellow
        }
    }
} catch { Write-Warning "Admin check failed: $_" }

try {
    $metrics = Invoke-WebRequest -Uri ("$BaseUrl/metrics") -UseBasicParsing -TimeoutSec 10
    $metricsContent = $metrics.Content
    Write-Host "Metrics fetched." -ForegroundColor Green
} catch { $metricsContent = $null; Write-Warning 'Metrics fetch failed' }

if($Json){
    $obj = [ordered]@{
        baseUrl = $BaseUrl
        health = $health.StatusCode
        versionRaw = $version.Content
        metrics = $metricsContent
        timestamp = (Get-Date).ToUniversalTime().ToString('o')
    }
    $obj | ConvertTo-Json -Depth 4
} else {
    Write-Host "Smoke test complete." -ForegroundColor Cyan
}
