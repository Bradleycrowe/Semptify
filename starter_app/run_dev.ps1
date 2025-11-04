# Run this PowerShell script from the starter_app folder to create venv and run the app
Set-Location -LiteralPath $PSScriptRoot
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python -m starter_app
