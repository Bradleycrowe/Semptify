<#
render_setup.ps1

Safe helper script to upsert environment variables for a Render service using the Render API.
Run this locally. Do NOT commit your API token to git.

Usage (PowerShell):
  # Option A (safer): paste token interactively
  $env:RENDER_API_TOKEN = Read-Host -Prompt "Paste your Render API token (will be kept only in this session)"
  .\scripts\render_setup.ps1

  # Option B (less secure): set token inline (only if you understand the risk)
  $env:RENDER_API_TOKEN = 'rnd_xxx'
  .\scripts\render_setup.ps1

What it does:
  - Lists your Render services and lets you select one by number (defaults to a service named 'Semptify' if present)
  - Fetches existing env vars for that service
  - Deletes any env var in the list below if present, then creates/updates values

Environment variables configured by default (change below in the script):
  FLASK_SECRET, ADMIN_TOKEN, SECURITY_MODE, FORCE_HTTPS,
  HSTS_MAX_AGE, HSTS_PRELOAD, ACCESS_LOG_JSON, ADMIN_RATE_WINDOW, ADMIN_RATE_MAX, ADMIN_RATE_STATUS

  NOTE: SEMPTIFY_PORT removed - Render automatically provides PORT env var

#>

Param()

function Get-ApiToken {
    if ($env:RENDER_API_TOKEN -and $env:RENDER_API_TOKEN.Trim().Length -gt 0) {
        return $env:RENDER_API_TOKEN
    }
    else {
        Write-Host "No RENDER_API_TOKEN environment variable detected." -ForegroundColor Yellow
        Write-Host "Please set the token into the environment variable before running the script, e.g.:" -ForegroundColor Yellow
        Write-Host '$env:RENDER_API_TOKEN = Read-Host -Prompt "Paste your Render API token"' -ForegroundColor Cyan
        Write-Host "Then run the script again." -ForegroundColor Yellow
        throw "No API token provided. Set RENDER_API_TOKEN and re-run."
    }
}

$token = Get-ApiToken
$base = 'https://api.render.com/v1'
$headers = @{ Authorization = "Bearer $token"; Accept = 'application/json' }

Write-Host "Fetching Render services..." -ForegroundColor Cyan
$services = Invoke-RestMethod -Uri "$base/services" -Headers $headers -Method Get -ErrorAction Stop

# Prefer service named Semptify
$svc = $services | Where-Object { $_.name -eq 'Semptify' } | Select-Object -First 1
if (-not $svc) {
    Write-Host "No service named 'Semptify' found. Choose from the list:" -ForegroundColor Yellow
    $i = 0
    $services | ForEach-Object { $i++; Write-Host "[$i] $_.name (id=$($_.id))" }
    $choice = Read-Host "Enter number of service to use"
    if (-not $choice) { throw "No selection provided" }
    $svc = $services[ [int]$choice - 1 ]
}

$serviceId = $svc.id
Write-Host "Selected service: $($svc.name) (id=$serviceId)" -ForegroundColor Green

# Default env vars to set - edit here if you want different values
$envPairs = @{
    FLASK_SECRET = (New-Guid).Guid.Replace('-','') + '00' ; # short random secret, you may replace
    ADMIN_TOKEN = ([guid]::NewGuid()).ToString('N').Substring(0,32);
    SECURITY_MODE = 'enforced';
    FORCE_HTTPS = '1';
    HSTS_MAX_AGE = '31536000';
    HSTS_PRELOAD = '1';
    ACCESS_LOG_JSON = '1';
    ADMIN_RATE_WINDOW = '60';
    ADMIN_RATE_MAX = '60';
    ADMIN_RATE_STATUS = '429';
}

Write-Host "Existing environment variables for service (fetched)..." -ForegroundColor Cyan
$existing = Invoke-RestMethod -Uri "$base/services/$serviceId/env-vars" -Headers $headers -Method Get -ErrorAction Stop
$existing | ForEach-Object { Write-Host "  $($_.key) = (secret)" }

# Upsert: if key exists, delete then create (Render API does not have a single upsert endpoint)
foreach ($k in $envPairs.Keys) {
    $present = $existing | Where-Object { $_.key -eq $k }
    if ($present) {
        Write-Host "Deleting existing env var: $k" -ForegroundColor Yellow
        Invoke-RestMethod -Uri "$base/services/$serviceId/env-vars/$($present.id)" -Headers $headers -Method Delete -ErrorAction Stop
    }
    $body = @{ key = $k; value = $envPairs[$k]; sync = $false } | ConvertTo-Json
    Write-Host "Creating env var: $k" -ForegroundColor Green
    Invoke-RestMethod -Uri "$base/services/$serviceId/env-vars" -Headers $headers -Method Post -Body $body -ContentType 'application/json' -ErrorAction Stop
}

Write-Host "All done. Triggering manual deploy..." -ForegroundColor Cyan
# Trigger manual deploy (create deploy)
$deployBody = @{ serviceId = $serviceId; clearCache = $true } | ConvertTo-Json
Invoke-RestMethod -Uri "$base/services/$serviceId/deploys" -Headers $headers -Method Post -Body $deployBody -ContentType 'application/json' -ErrorAction Stop

Write-Host "Deploy requested. Watch Render dashboard for build logs." -ForegroundColor Green

# End of script
