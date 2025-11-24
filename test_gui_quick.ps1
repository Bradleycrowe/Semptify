# Quick GUI functionality test
Write-Host "
=== Testing Each GUI ===" -ForegroundColor Cyan

$guis = @{
    "Main Dashboard" = "/"
    "Brad GUI" = "/brad/"
    "Modern GUI" = "/app/"
    "Timeline Assistant" = "/timeline/assistant"
    "Vault" = "/vault"
    "Admin" = "/admin"
    "Metrics" = "/metrics"
}

foreach ($name in $guis.Keys) {
    $url = "http://127.0.0.1:5000$($guis[$name])"
    try {
        $result = Invoke-WebRequest -Uri $url -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        Write-Host "✓ $name - OK ($($result.StatusCode))" -ForegroundColor Green
    } catch {
        $code = $_.Exception.Response.StatusCode.Value__
        if ($code -eq 404) {
            Write-Host "✗ $name - NOT FOUND" -ForegroundColor Red
        } elseif ($code -eq 401) {
            Write-Host "🔒 $name - Auth Required" -ForegroundColor Yellow
        } else {
            Write-Host "⚠ $name - Error $code" -ForegroundColor Yellow
        }
    }
}
