# PowerShell script to start Semptify backend, check endpoints, and show status

# Stop all running Python servers
Write-Host "Stopping all running Python servers..."
taskkill /F /IM python.exe

# Activate virtual environment (if exists)
$venvPath = "C:\Semptify\Semptify\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    & $venvPath
} else {
    Write-Host "No virtual environment found. Skipping activation."
}

# Start backend server
Write-Host "Starting Semptify backend server (Waitress)..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList ".\run_prod.py"
Start-Sleep -Seconds 5

# Test endpoints
Write-Host "Testing /register endpoint..."
try {
    $register = Invoke-WebRequest -Uri "http://127.0.0.1:8080/register" -UseBasicParsing
    Write-Host "Register endpoint response: $($register.StatusCode)"
} catch {
    Write-Host "Register endpoint not reachable."
}

Write-Host "Testing /vault endpoint..."
try {
    $vault = Invoke-WebRequest -Uri "http://127.0.0.1:8080/vault" -UseBasicParsing
    Write-Host "Vault endpoint response: $($vault.StatusCode)"
} catch {
    Write-Host "Vault endpoint not reachable."
}

Write-Host "Check logs for errors if endpoints are not reachable."
Write-Host "Done."
