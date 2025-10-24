# ensure runtime directories exist and append startup log
$dirs = @("uploads","logs","copilot_sync","final_notices","security")
foreach ($d in $dirs) {
    if (!(Test-Path $d)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
}
$init = Join-Path (Get-Location) "logs\init.log"
if (!(Test-Path $init)) { "" | Out-File -FilePath $init -Encoding utf8 }
Add-Content -Path $init -Value ("Startup ensured: " + (Get-Date -Format o))
