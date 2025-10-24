Write-Host "=== Semptify Setup Script ==="

# 1. Create required runtime directories
$dirs = @("uploads", "logs", "copilot_sync", "final_notices", "security", "modules", "templates", "static")
foreach ($d in $dirs) {
    if (!(Test-Path $d)) {
        New-Item -ItemType Directory -Path $d | Out-Null
        Write-Host "Created directory: $d"
    } else {
        Write-Host "Directory exists: $d"
    }
}

# 2. Set up Python virtual environment
if (!(Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment (.venv)..."
    python -m venv .venv
} else {
    Write-Host "Python virtual environment (.venv) already exists."
}

# 3. Activate venv and install requirements
Write-Host "Activating virtual environment and installing requirements..."
& .\.venv\Scripts\Activate.ps1
if (Test-Path "requirements.txt") {
    pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "Python dependencies installed."
} else {
    Write-Host "requirements.txt not found. Please add it before running the app."
}

# 4. Print instructions for running the app
Write-Host "`n=== Setup Complete ==="
Write-Host "To run Semptify in development:"
Write-Host "    python Semptify.py"
Write-Host "To run in production (waitress):"
Write-Host "    python run_prod.py"
Write-Host "`nRemember to set environment variables in .env or Render dashboard as needed."
Write-Host "If you need to run tests:"
Write-Host "    python -m pytest -q"
Write-Host "`nAll required folders and dependencies are now set up."

