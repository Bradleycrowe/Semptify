# Stop SemptifyGUI production runner if running
# Usage: .\scripts\stop_service.ps1

$root = Resolve-Path "$PSScriptRoot\.." | Select-Object -ExpandProperty Path
Set-Location $root
$pidfile = Join-Path $root ".service_semptify.pid"

if (-Not (Test-Path $pidfile)) {
    Write-Host "No pidfile found. Service may not be running."; exit 0
}

$procId = (Get-Content $pidfile -ErrorAction Stop).Trim()
if (-not $procId) { Remove-Item $pidfile -ErrorAction SilentlyContinue; Write-Host "No pid found in pidfile"; exit 0 }

try {
    Stop-Process -Id $procId -Force -ErrorAction Stop
    Write-Host "Stopped process $procId"
    Remove-Item $pidfile -ErrorAction SilentlyContinue
} catch {
    Write-Error ("Failed to stop process {0}: {1}" -f $procId, $_.Exception.Message)
}
