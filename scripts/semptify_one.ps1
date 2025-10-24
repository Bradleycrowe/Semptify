<#
semptify_one.ps1 - helper script for common tasks: zip, dev, prod
Usage:
  .\scripts\semptify_one.ps1 -Action zip
  .\scripts\semptify_one.ps1 -Action dev [-Port 5000] [-NoReload]
  .\scripts\semptify_one.ps1 -Action prod [-Port 8080]

Behaviors:
 - zip: creates Semptify_FlaskBundle_<date>.zip of repo root (excluding .venv)
 - dev: activates .venv if present and runs Semptify.py; disables reloader by default
 - prod: activates .venv if present and starts run_prod.py in background using Start-Process
#>
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('zip','dev','prod','stop','status')]
    [string]$Action,

    [int]$Port = 5000,

    [switch]$NoReload
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Path $MyInvocation.MyCommand.Path -Parent | Split-Path -Parent
Write-Host "Repo root: $RepoRoot"
Push-Location $RepoRoot

function Activate-Venv {
    $venvPath = Join-Path $RepoRoot '.venv'
    if (Test-Path $venvPath) {
        $activate = Join-Path $venvPath 'Scripts\Activate.ps1'
        if (Test-Path $activate) {
            Write-Host 'Activating virtualenv...'
            & $activate
            return $true
        }
    }
    return $false
}

switch ($Action) {
    'zip' {
        $zipName = "Semptify_FlaskBundle_$(Get-Date -Format yyyy-MM-dd).zip"
        Write-Host "Creating archive $zipName (excluding .venv, node_modules, uploads, logs, and __pycache__)"
        $exclude = @('.venv','__pycache__','node_modules','uploads','logs','.git')
        $items = Get-ChildItem -File -Recurse -Force | Where-Object {
            foreach ($e in $exclude) { if ($_.FullName -like "*$e*") { return $false } }
            return $true
        }
        $temp = Join-Path $env:TEMP ([guid]::NewGuid().ToString() + '.txt')
        $items | ForEach-Object { $_.FullName } | Out-File -FilePath $temp -Encoding utf8
        Compress-Archive -Path (Get-Content $temp) -DestinationPath $zipName -Force
        Remove-Item $temp -ErrorAction SilentlyContinue
        Write-Host "Created $zipName"
    }
    'dev' {
        $activated = Activate-Venv
        if ($NoReload) {
            $env:SEMPTIFY_USE_RELOADER = '0'
        } else {
            # default is disabled in Semptify.py; set to 1 only if explicitly asked
            $env:SEMPTIFY_USE_RELOADER = '0'
        }
        $env:FLASK_APP = 'Semptify.py'
        Write-Host "Starting dev server on port $Port (reloader disabled)"
        & python .\Semptify.py
    }
    'prod' {
        $activated = Activate-Venv
        $env:SEMPTIFY_PORT = $Port
        Write-Host "Starting production runner (run_prod.py) on port $Port in background"
        # ensure logs dir exists
        $logsDir = Join-Path $RepoRoot 'logs'
        if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir | Out-Null }
        $outLog = Join-Path $logsDir 'prod.stdout.log'
        $errLog = Join-Path $logsDir 'prod.stderr.log'

        # Start process and redirect stdout/stderr to files (works on modern PowerShell)
        try {
            $proc = Start-Process -FilePath python -ArgumentList '.\run_prod.py' -RedirectStandardOutput $outLog -RedirectStandardError $errLog -WindowStyle Hidden -PassThru
            Write-Host "Started PID: $($proc.Id)"
            # Write PID so stop can find it
            $pidFile = Join-Path $RepoRoot 'run_prod.pid'
            $proc.Id | Out-File -FilePath $pidFile -Encoding ascii -Force
            Write-Host "Wrote PID to $pidFile"
            Write-Host "Stdout -> $outLog"
            Write-Host "Stderr -> $errLog"
        } catch {
            Write-Warning "Failed to start production runner: $_"
        }
    }
    'stop' {
        # Stop process started by prod action (uses pid file) or fallback to processes running run_prod.py
        $pidFile = Join-Path $RepoRoot 'run_prod.pid'
        if (Test-Path $pidFile) {
            $pidFromFile = Get-Content $pidFile | Select-Object -First 1
            try {
                Stop-Process -Id $pidFromFile -ErrorAction Stop
                Remove-Item $pidFile -ErrorAction SilentlyContinue
                Write-Host "Stopped process $pidFromFile and removed pid file"
            } catch {
                Write-Warning ("Failed to stop pid {0}: {1}" -f $pidFromFile, $_)
            }
        } else {
            # fallback: try to find python processes that have run_prod.py in commandline
            $found = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -match 'run_prod.py' }
            if ($found) {
                foreach ($proc in $found) {
                    try {
                        Stop-Process -Id $proc.ProcessId -ErrorAction Stop
                        Write-Host "Stopped process $($proc.ProcessId)"
                    } catch {
                        Write-Warning ("Failed to stop {0}: {1}" -f $($proc.ProcessId), $_)
                    }
                }
            } else {
                Write-Host "No run_prod.py processes found to stop"
            }
        }
    }
    'status' {
        $pidFile = Join-Path $RepoRoot 'run_prod.pid'
        if (Test-Path $pidFile) {
            $pidFromFile = Get-Content $pidFile | Select-Object -First 1
            Write-Host "PID file: $pidFile -> $pidFromFile"
            $proc = Get-Process -Id $pidFromFile -ErrorAction SilentlyContinue
            if ($proc) {
                Write-Host "Process $pidFromFile is running. CPU: $($proc.CPU) Threads: $($proc.Threads.Count)"
            } else {
                Write-Host "Process $pidFromFile not running"
            }
        } else {
            Write-Host "No pid file found at $pidFile"
        }
        # tail logs if present
        $initLog = Join-Path $RepoRoot 'logs\init.log'
        if (Test-Path $initLog) {
            Write-Host "\n--- last 200 lines of logs/init.log ---"
            Get-Content $initLog -Tail 200 | ForEach-Object { Write-Host $_ }
        }
        $eventsLog = Join-Path $RepoRoot 'logs\events.log'
        if (Test-Path $eventsLog) {
            Write-Host "\n--- last 200 lines of logs/events.log ---"
            Get-Content $eventsLog -Tail 200 | ForEach-Object { Write-Host $_ }
        }
        # show prod stdout/stderr if present
        $prodOut = Join-Path $RepoRoot 'logs\prod.stdout.log'
        $prodErr = Join-Path $RepoRoot 'logs\prod.stderr.log'
        if (Test-Path $prodOut) {
            Write-Host "\n--- tail prod.stdout.log ---"
            Get-Content $prodOut -Tail 80 | ForEach-Object { Write-Host $_ }
        }
        if (Test-Path $prodErr) {
            Write-Host "\n--- tail prod.stderr.log ---"
            Get-Content $prodErr -Tail 80 | ForEach-Object { Write-Host $_ }
        }
    }
}

Pop-Location

