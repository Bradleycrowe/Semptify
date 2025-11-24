$env_vars = @('R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME', 'R2_ENDPOINT_URL')
foreach ($var in $env_vars) {
    $val = [Environment]::GetEnvironmentVariable($var)
    if ($val) {
        $masked = $val.Substring(0, [Math]::Min(8, $val.Length)) + '...'
        Write-Host "$var = $masked"
    } else {
        Write-Host "$var = NOT SET" -ForegroundColor Red
    }
}
