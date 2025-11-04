# Run the project's test suite (PowerShell helper)
Set-Location -LiteralPath "$PSScriptRoot/.."
python -m pytest -q
