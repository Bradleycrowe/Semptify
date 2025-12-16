# Dakota County Eviction Defense - Quick Start
# Run this to start the server with Dakota routes working

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"

Write-Host "`n🚀 Starting Semptify with Dakota County Eviction Defense..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Yellow

& ".\.venv\Scripts\python.exe" -m uvicorn semptify_complete:app --host 0.0.0.0 --port 5000 --reload

