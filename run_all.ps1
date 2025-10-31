m<#
run_all.ps1
Helper script to activate the project's virtual environment, install dependencies,
and start the Flask server and the PyQt5 GUI in separate processes.

Usage: From the repo root in PowerShell:
  .\run_all.ps1
#>

Write-Output "Starting Semptify: activating venv and installing requirements..."

$venvActivate = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
} else {
    Write-Warning ".venv not found. Create a virtual environment first: python -m venv .venv"
}

Write-Output "Installing requirements (may skip already-installed packages)..."
pip install -r requirements.txt

Write-Output "Launching Flask server and GUI..."

# Start Flask server
Start-Process -FilePath "python" -ArgumentList "Semptify.py" -WorkingDirectory (Get-Location) -WindowStyle Normal

# Start GUI
Start-Process -FilePath "python" -ArgumentList "SemptifyAppGUI.py" -WorkingDirectory (Get-Location) -WindowStyle Normal

Write-Output "Processes started. Check terminals or logs for output/errors."
