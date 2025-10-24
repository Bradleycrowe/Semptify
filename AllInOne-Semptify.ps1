# All-in-one Semptify setup and run script

# 1. Go to project folder
Set-Location -LiteralPath 'D:\Semptify\Semptify'

# 2. Create virtual environment if missing
if (!(Test-Path .\.venv)) {
    python -m venv .venv
}

# 3. Activate virtual environment
. .\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Ensure runtime directories exist
$dirs = @('uploads', 'logs', 'copilot_sync', 'final_notices', 'security')
foreach ($d in $dirs) {
    if (!(Test-Path $d)) { New-Item -ItemType Directory -Path $d }
}

# 6. Check for .env or RENDER.env
if (!(Test-Path .env) -and !(Test-Path RENDER.env)) {
    Write-Host "Warning: .env or RENDER.env not found. Some features may not work."
}

# 7. Run the app (production WSGI server)
python run_prod.py

