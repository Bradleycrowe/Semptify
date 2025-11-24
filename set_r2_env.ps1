# Semptify R2 Environment Configuration
# Source this before running: . .\set_r2_env.ps1

$env:R2_ACCOUNT_ID='be2a39cd3624261169fa8e800d75923f'
$env:R2_ACCESS_KEY_ID='c994035322007ef21464f670821c0e3d'
$env:R2_SECRET_ACCESS_KEY='3b05227e537b441eb62b2d633fe969e74faa532d404d2c89cb5ab8f6e57f0ff7'
$env:R2_BUCKET_NAME='semptify'
$env:R2_ENDPOINT_URL='https://be2a39cd3624261169fa8e800d75923f.r2.cloudflarestorage.com'
$env:PYTHONIOENCODING='utf-8'

Write-Host "✓ R2 environment variables configured" -ForegroundColor Green
Write-Host "  Account: $($env:R2_ACCOUNT_ID.Substring(0,8))..." -ForegroundColor Cyan
Write-Host "  Bucket: $env:R2_BUCKET_NAME" -ForegroundColor Cyan
Write-Host "  Endpoint: $env:R2_ENDPOINT_URL" -ForegroundColor Cyan
