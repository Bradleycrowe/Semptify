# Start-BradGUI.ps1 - One-click startup for Brad's GUI
$ErrorActionPreference = "Stop"

Write-Host "`n=== Starting Brad's GUI ===" -ForegroundColor Cyan

# Set working directory
Set-Location "C:\Semptify\Semptify"

# Load R2 credentials from registry
$env:R2_ACCOUNT_ID = [System.Environment]::GetEnvironmentVariable('R2_ACCOUNT_ID', 'User')
$env:R2_ACCESS_KEY_ID = [System.Environment]::GetEnvironmentVariable('R2_ACCESS_KEY_ID', 'User')
$env:R2_SECRET_ACCESS_KEY = [System.Environment]::GetEnvironmentVariable('R2_SECRET_ACCESS_KEY', 'User')
$env:R2_BUCKET_NAME = [System.Environment]::GetEnvironmentVariable('R2_BUCKET_NAME', 'User')
$env:R2_ENDPOINT_URL = [System.Environment]::GetEnvironmentVariable('R2_ENDPOINT_URL', 'User')
$env:SECURITY_MODE = [System.Environment]::GetEnvironmentVariable('SECURITY_MODE', 'User')

# Load Google OAuth credentials
$env:GOOGLE_OAUTH_CLIENT_ID = [System.Environment]::GetEnvironmentVariable('GOOGLE_OAUTH_CLIENT_ID', 'User')
$env:GOOGLE_OAUTH_CLIENT_SECRET = [System.Environment]::GetEnvironmentVariable('GOOGLE_OAUTH_CLIENT_SECRET', 'User')
$env:GOOGLE_OAUTH_REDIRECT_URI = [System.Environment]::GetEnvironmentVariable('GOOGLE_OAUTH_REDIRECT_URI', 'User')

Write-Host "✓ Environment loaded" -ForegroundColor Green

# Start production server in background
Write-Host "Starting Waitress production server on port 8080..." -ForegroundColor Yellow
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Semptify\Semptify"
    & ".\.venv\Scripts\python.exe" ".\run_prod.py"
}

Write-Host "✓ Server starting (Job ID: $($serverJob.Id))" -ForegroundColor Green

# Wait for server to be ready
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test server
$maxAttempts = 10
$attempt = 0
$serverReady = $false

while ($attempt -lt $maxAttempts -and -not $serverReady) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/brad" -Method Head -TimeoutSec 2 -ErrorAction Stop
        $serverReady = $true
        Write-Host "✓ Server ready!" -ForegroundColor Green
    } catch {
        $attempt++
        Write-Host "  Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
}

if ($serverReady) {
    # Open Brad's GUI in default browser
    Write-Host "`nOpening Brad's GUI..." -ForegroundColor Cyan
    Start-Process "http://localhost:8080/brad"
    
    Write-Host "`n=== Brad's GUI is ready! ===" -ForegroundColor Green
    Write-Host "URL: http://localhost:8080/brad" -ForegroundColor White
    Write-Host "`nServer Job ID: $($serverJob.Id)" -ForegroundColor Gray
    Write-Host "To stop server: Stop-Job -Id $($serverJob.Id); Remove-Job -Id $($serverJob.Id)" -ForegroundColor Gray
    Write-Host "`nPress Ctrl+C to exit (server will continue running)" -ForegroundColor Yellow
    
    # Keep script alive
    Wait-Job -Id $serverJob.Id
} else {
    Write-Host "`n✗ Server failed to start" -ForegroundColor Red
    Write-Host "Check server output:" -ForegroundColor Yellow
    Receive-Job -Id $serverJob.Id
    Stop-Job -Id $serverJob.Id
    Remove-Job -Id $serverJob.Id
    exit 1
}
