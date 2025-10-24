<#
All-in-one helper for the FastAPI prototype in app-backend.

Usage:
  .\scripts\run_fastapi_all.ps1 -Action init      # create venv in app-backend
  .\scripts\run_fastapi_all.ps1 -Action install   # install requirements into venv
  .\scripts\run_fastapi_all.ps1 -Action start     # start uvicorn (background), writes run_fastapi.pid
  .\scripts\run_fastapi_all.ps1 -Action stop      # stop uvicorn using pid file
  .\scripts\run_fastapi_all.ps1 -Action status    # show status of background process
  .\scripts\run_fastapi_all.ps1 -Action open      # open http://localhost:8000 in default browser
  .\scripts\run_fastapi_all.ps1 -Action full      # init + install + start + open

This script assumes PowerShell (pwsh.exe) on Windows. It installs into
`app-backend/.venv` and starts uvicorn from that venv.
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('init','install','start','stop','status','open','full')]
    [string]$Action
)

Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir '..')
$AppBackend = Join-Path $RepoRoot 'app-backend'
$VenvPath = Join-Path $AppBackend '.venv'
$VenvPython = Join-Path $VenvPath 'Scripts\python.exe'
$ReqFile = Join-Path $AppBackend 'requirements.txt'
$PidFile = Join-Path $AppBackend 'run_fastapi.pid'


function Test-AppBackendExists {
    if (-not (Test-Path $AppBackend)) {
        Write-Error "app-backend directory not found at $AppBackend"
        exit 1
    }
}

Test-AppBackendExists

switch ($Action) {
    'init' {
        if (Test-Path $VenvPath) {
            Write-Host "Virtual environment already exists at $VenvPath"
            break
        }
        Push-Location $AppBackend
        Write-Host "Creating virtual environment in $VenvPath..."
        python -m venv .venv
        Pop-Location
        Write-Host "Created venv. Run '-Action install' to install dependencies."
    }

    'install' {
        if (-not (Test-Path $VenvPython)) {
            Write-Error "Venv python not found. Run -Action init first."
            exit 1
        }
        Write-Host "Upgrading pip and installing requirements from $ReqFile..."
        & $VenvPython -m pip install --upgrade pip
        & $VenvPython -m pip install -r $ReqFile
        Write-Host "Installed requirements."
    }

    'start' {
        if (-not (Test-Path $VenvPython)) {
            Write-Error "Venv python not found. Run -Action init and install first."
            exit 1
        }
        if (Test-Path $PidFile) {
            $existing = Get-Content $PidFile -ErrorAction SilentlyContinue
            if ($existing -and (Get-Process -Id $existing -ErrorAction SilentlyContinue)) {
                Write-Host "Server appears to be already running (PID $existing). Use -Action status or stop first."
                break
            }
        }

        # ensure logs directory exists and prepare log file paths
        $LogsDir = Join-Path $AppBackend 'logs'
        if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir | Out-Null }
        $ts = (Get-Date).ToString('yyyyMMdd-HHmmss')
        $outLog = Join-Path $LogsDir "uvicorn-$ts.stdout.log"
        $errLog = Join-Path $LogsDir "uvicorn-$ts.stderr.log"

        $uvArgs = @('-m','uvicorn','app.main:app','--host','0.0.0.0','--port','8000')
        Write-Host "Starting uvicorn in background (working dir: $AppBackend). Logs: $outLog / $errLog"
        # Start uvicorn with redirected stdout/stderr into log files. -NoNewWindow keeps it backgrounded.
        $proc = Start-Process -FilePath $VenvPython -ArgumentList $uvArgs -WorkingDirectory $AppBackend -RedirectStandardOutput $outLog -RedirectStandardError $errLog -NoNewWindow -PassThru
        Start-Sleep -Milliseconds 400
        $procId = $proc.Id
        Set-Content -Path $PidFile -Value $procId
        Write-Host "Started uvicorn (PID $procId). PID file: $PidFile"
        Write-Host "Tailing logs: tail -f $outLog (or open files in your editor)"

        # Create or update stable 'latest' log paths for easy tailing. Try symlink first, fall back to copy.
        $latestOut = Join-Path $LogsDir 'uvicorn.latest.stdout.log'
        $latestErr = Join-Path $LogsDir 'uvicorn.latest.stderr.log'
        try {
            if (Test-Path $latestOut) { Remove-Item $latestOut -Force -ErrorAction SilentlyContinue }
            if (Test-Path $latestErr) { Remove-Item $latestErr -Force -ErrorAction SilentlyContinue }
            # Attempt to create symlink (administrator or Developer Mode may be required on Windows)
            New-Item -ItemType SymbolicLink -Path $latestOut -Target $outLog -ErrorAction Stop | Out-Null
            New-Item -ItemType SymbolicLink -Path $latestErr -Target $errLog -ErrorAction Stop | Out-Null
            Write-Host "Created symlinks: $latestOut -> $outLog and $latestErr -> $errLog"
        } catch {
            # Symlink creation failed (common on Windows without permissions). Fall back to copying the current logs.
            try {
                Copy-Item -Path $outLog -Destination $latestOut -Force -ErrorAction SilentlyContinue
                Copy-Item -Path $errLog -Destination $latestErr -Force -ErrorAction SilentlyContinue
                Write-Host "Created copies for latest logs: $latestOut, $latestErr"
            } catch { Write-Host "Unable to create latest-log symlink or copy: $($_.Exception.Message)" }
        }
    }

    'stop' {
        if (-not (Test-Path $PidFile)) { Write-Host "PID file not found ($PidFile). Nothing to stop."; break }
        $pidValue = Get-Content $PidFile -ErrorAction SilentlyContinue
        if (-not $pidValue) { Write-Host "PID file is empty or unreadable."; break }
        if (Get-Process -Id $pidValue -ErrorAction SilentlyContinue) {
            Stop-Process -Id $pidValue -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process $pidValue"
        } else {
            Write-Host "Process $pidValue not running"
        }
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    }

    'status' {
        if (-not (Test-Path $PidFile)) { Write-Host "No PID file ($PidFile). Server probably not started."; break }
        $pidValue = Get-Content $PidFile -ErrorAction SilentlyContinue
        if (-not $pidValue) { Write-Host "PID file empty"; break }
        $p = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
        if ($p) {
            Write-Host "Process $pidValue is running. Threads: $($p.Threads.Count). CPU: $($p.CPU)"
        } else {
            Write-Host "Process $pidValue not found or not running."
        }
    }

    'open' {
        Start-Process 'http://localhost:8000'
    }

    'full' {
        & $MyInvocation.MyCommand.Path -Action init
        & $MyInvocation.MyCommand.Path -Action install
        & $MyInvocation.MyCommand.Path -Action start
        Start-Sleep -Seconds 1
        Start-Process 'http://localhost:8000'
    }

    default { Write-Error "Unknown action: $Action" }
}
