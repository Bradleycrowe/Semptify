# Start SemptifyGUI production runner in background and write PID to .service_semptify.pid
# Usage: .\scripts\start_service.ps1

$root = Resolve-Path "$PSScriptRoot\.." | Select-Object -ExpandProperty Path
Set-Location $root

$python = Join-Path $root ".venv\Scripts\python.exe"
$pidfile = Join-Path $root ".service_semptify.pid"
$log = Join-Path $root "logs\service.log"

if (-Not (Test-Path $python)) {
    Write-Error ".venv python not found at $python. Activate venv or create it first."
    exit 1
}

# If pidfile exists and process is alive, do nothing
if (Test-Path $pidfile) {
    try {
        $existing = Get-Content $pidfile -ErrorAction Stop | Out-String | Trim
        if ($existing -and (Get-Process -Id $existing -ErrorAction SilentlyContinue)) {
            Write-Host "Service appears to be running (PID $existing). Use scripts\stop_service.ps1 to stop it first."; exit 0
        } else {
            Remove-Item $pidfile -ErrorAction SilentlyContinue
        }
    } catch {
        # ignore
    }
}

# Ensure logs folder exists
if (-Not (Test-Path (Join-Path $root 'logs'))) { New-Item -ItemType Directory -Path (Join-Path $root 'logs') | Out-Null }

# Start the process directly and redirect stdout/stderr to separate files
$outLog = Join-Path $root "logs\out.log"
$errLog = Join-Path $root "logs\err.log"

# Ensure logs directory exists
if (-Not (Test-Path (Join-Path $root 'logs'))) { New-Item -ItemType Directory -Path (Join-Path $root 'logs') | Out-Null }

$proc = Start-Process -FilePath $python -ArgumentList 'run_prod.py' -WorkingDirectory $root -RedirectStandardOutput $outLog -RedirectStandardError $errLog -WindowStyle Hidden -PassThru
if ($proc -and $proc.Id) {
    $proc.Id | Out-File -FilePath $pidfile -Encoding ascii
    Write-Host "Started SemptifyGUI (pid $($proc.Id)). Logs -> $outLog and $errLog"
    exit 0
} else {
    Write-Error "Failed to start process"
    exit 2
}
