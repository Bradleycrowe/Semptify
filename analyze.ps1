# Analyze test failure patterns
$output = .\.venv\Scripts\python.exe -m pytest -q --tb=short 2>&1
$failures = $output | Select-String "FAILED|AssertionError|assert"

Write-Host "`n=== Test Failure Analysis ===" -ForegroundColor Cyan
Write-Host "`nCommon patterns:"
$failures | ForEach-Object { $_.Line } | Sort-Object -Unique | Select-Object -First 15
