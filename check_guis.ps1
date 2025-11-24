Write-Host "
=== GUI Functionality Check ===" -ForegroundColor Cyan

# Check if app is running
$response = try { 
    Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -TimeoutSec 2 -UseBasicParsing 
} catch { 
    $null 
}

if ($response) {
    Write-Host "✓ App is running on port 5000" -ForegroundColor Green
} else {
    Write-Host "✗ App not running - need to start it first" -ForegroundColor Red
    exit 1
}

# Test each GUI endpoint
Write-Host "
Testing GUIs:" -ForegroundColor Yellow

$tests = @(
    @{Name="Main Dashboard"; URL="http://127.0.0.1:5000/"},
    @{Name="Brad GUI"; URL="http://127.0.0.1:5000/brad/"},
    @{Name="Modern GUI"; URL="http://127.0.0.1:5000/app/"},
    @{Name="Timeline Assistant"; URL="http://127.0.0.1:5000/timeline/assistant"},
    @{Name="Vault"; URL="http://127.0.0.1:5000/vault"},
    @{Name="Admin"; URL="http://127.0.0.1:5000/admin"},
    @{Name="Metrics"; URL="http://127.0.0.1:5000/metrics"},
)

foreach ($test in $tests) {
    try {
        $result = Invoke-WebRequest -Uri $test.URL -TimeoutSec 3 -UseBasicParsing
        $status = $result.StatusCode
        $size = $result.Content.Length
        
        if ($status -eq 200) {
            Write-Host "  ✓ $($test.Name) - OK ($size bytes)" -ForegroundColor Green
        } elseif ($status -eq 302 -or $status -eq 301) {
            Write-Host "  ↗ $($test.Name) - Redirect (status $status)" -ForegroundColor Yellow
        } elseif ($status -eq 401) {
            Write-Host "  🔒 $($test.Name) - Auth required (status $status)" -ForegroundColor Cyan
        } else {
            Write-Host "  ⚠ $($test.Name) - Status $status" -ForegroundColor Yellow
        }
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.Value__
        if ($statusCode -eq 404) {
            Write-Host "  ✗ $($test.Name) - NOT FOUND (404)" -ForegroundColor Red
        } elseif ($statusCode -eq 401) {
            Write-Host "  🔒 $($test.Name) - Auth required (401)" -ForegroundColor Cyan
        } elseif ($statusCode -eq 500) {
            Write-Host "  💥 $($test.Name) - Server error (500)" -ForegroundColor Red
        } else {
            Write-Host "  ✗ $($test.Name) - Error: $statusCode" -ForegroundColor Red
        }
    }
}

Write-Host "
Detailed checks..." -ForegroundColor Yellow
