# Check SemptifyGUI service status
# Usage: .\scripts\status_service.ps1

$root = Resolve-Path "$PSScriptRoot\.." | Select-Object -ExpandProperty Path
Set-Location $root
$pidfile = Join-Path $root ".service_semptify.pid"

if (Test-Path $pidfile) {
    $pidval = (Get-Content $pidfile -ErrorAction SilentlyContinue).Trim()
    if ($pidval -and (Get-Process -Id $pidval -ErrorAction SilentlyContinue)) {
        Write-Host "Service running (pid $pidval)"
        netstat -ano | Select-String ":8080"
    } else {
        Write-Host "Pidfile present but process not found. Remove $pidfile to clean up." 
    }
} else {
    Write-Host "Service not running (no pidfile)."
}
