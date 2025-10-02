# Full automated setup script for SemptifyGUI
# Usage: .\scripts\full_setup.ps1
# Requires: Python 3.11+ with venv support
# Optional: Run as Administrator to register Scheduled Task for auto-start

$ErrorActionPreference = 'Stop'
$root = Resolve-Path "$PSScriptRoot\.." | Select-Object -ExpandProperty Path
Set-Location $root

# Setup logging
$log = Join-Path $root "scripts\full_setup.log"
"=== Full setup started: $(Get-Date -Format o) ===" | Out-File $log -Encoding utf8

function L {
    param($m)
    "$((Get-Date).ToString('o')) $m" | Tee-Object -FilePath $log -Append
}

try {
    L "Working directory: $root"

    # 1) Ensure runtime folders exist (follows repo convention)
    L "Creating runtime folders..."
    $folders = @("uploads", "logs", "copilot_sync", "final_notices", "security", "sbom")
    foreach ($folder in $folders) {
        $folderPath = Join-Path $root $folder
        if (-not (Test-Path $folderPath)) {
            New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
            L "Created folder: $folder"
        } else {
            L "Folder exists: $folder"
        }
    }

    # Append to init.log per repo convention
    $timestamp = (Get-Date).ToString("o")
    $initLog = Join-Path $root "logs\init.log"
    "[$timestamp] full_setup.ps1: Ensured runtime folders exist`n" | Out-File -FilePath $initLog -Append -Encoding utf8
    L "Updated logs\init.log"

    # 2) Create virtual environment (if missing)
    $venvPath = Join-Path $root ".venv"
    if (-not (Test-Path $venvPath)) {
        L "Creating Python virtual environment..."
        & python -m venv .venv 2>&1 | Tee-Object -FilePath $log -Append
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
        L "Virtual environment created"
    } else {
        L "Virtual environment already exists"
    }

    # 3) Activate venv and upgrade pip
    L "Activating virtual environment..."
    $activateScript = Join-Path $root ".venv\Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        throw "Virtual environment activation script not found at $activateScript"
    }
    & $activateScript
    L "Virtual environment activated"

    L "Upgrading pip..."
    & python -m pip install --upgrade pip 2>&1 | Tee-Object -FilePath $log -Append
    if ($LASTEXITCODE -ne 0) {
        L "Warning: pip upgrade failed, continuing anyway"
    }

    # 4) Install dependencies from requirements.txt
    $requirementsPath = Join-Path $root "requirements.txt"
    if (Test-Path $requirementsPath) {
        L "Installing dependencies from requirements.txt..."
        & python -m pip install -r requirements.txt 2>&1 | Tee-Object -FilePath $log -Append
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install requirements"
        }
        L "Dependencies installed"
    } else {
        L "Warning: requirements.txt not found, skipping dependency installation"
    }

    # 5) Install pytest if not already installed
    L "Ensuring pytest is installed..."
    & python -m pip install pytest 2>&1 | Tee-Object -FilePath $log -Append

    # 6) Run tests
    L "Running tests with pytest..."
    $pytestOutput = Join-Path $root "logs\pytest.out"
    $pytestError = Join-Path $root "logs\pytest.err"
    
    & python -m pytest -q tests 2>$pytestError | Out-File -FilePath $pytestOutput -Encoding utf8
    $testExitCode = $LASTEXITCODE
    
    Get-Content $pytestOutput -ErrorAction SilentlyContinue | Tee-Object -FilePath $log -Append
    Get-Content $pytestError -ErrorAction SilentlyContinue | Tee-Object -FilePath $log -Append
    
    if ($testExitCode -eq 0) {
        L "Tests passed"
    } else {
        L "Warning: Tests failed with exit code $testExitCode, but continuing setup"
    }

    # 7) Start the production service
    L "Starting production service..."
    $startServiceScript = Join-Path $root "scripts\start_service.ps1"
    if (Test-Path $startServiceScript) {
        & $startServiceScript 2>&1 | Tee-Object -FilePath $log -Append
        L "Service start script executed"
    } else {
        L "Warning: start_service.ps1 not found, skipping service start"
    }

    # 8) Wait a moment and check if service is running
    Start-Sleep -Seconds 3
    L "Checking service status..."
    $statusScript = Join-Path $root "scripts\status_service.ps1"
    if (Test-Path $statusScript) {
        & $statusScript 2>&1 | Tee-Object -FilePath $log -Append
    }

    # 9) Show listening ports
    L "Checking network listeners..."
    netstat -ano | Select-String ":8080|:5000" | Tee-Object -FilePath $log -Append

    # 10) Register Scheduled Task for auto-start (requires Administrator)
    # Check if running as Administrator
    $isAdmin = $false
    try {
        $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
        $isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch {
        L "Unable to determine admin status: $($_.Exception.Message)"
    }

    if ($isAdmin) {
        try {
            L "Running as Administrator - attempting to register Scheduled Task..."
            $taskName = "SemptifyGUI Service"
            $startServicePath = Join-Path $root "scripts\start_service.ps1"
            
            # Check if task already exists
            $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
            if ($existingTask) {
                L "Scheduled Task '$taskName' already exists, unregistering old version..."
                Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
            }

            # Create new scheduled task
            $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$startServicePath`""
            $trigger = New-ScheduledTaskTrigger -AtLogOn
            $principal = New-ScheduledTaskPrincipal -UserId "BUILTIN\Users" -RunLevel Highest
            $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
            
            Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
            L "Successfully registered Scheduled Task '$taskName' for auto-start at logon"
        } catch {
            L "Failed to register Scheduled Task: $($_.Exception.Message)"
            L "Scheduled Task registration requires Administrator privileges"
        }
    } else {
        L "Not running as Administrator - skipping Scheduled Task registration"
        L "To enable auto-start at logon, run this script as Administrator"
    }

    # 11) Summary
    L ""
    L "========================================="
    L "Full setup completed successfully!"
    L "========================================="
    L "Runtime folders: $(($folders -join ', '))"
    L "Virtual environment: $venvPath"
    L "Service status: Check with .\scripts\status_service.ps1"
    L "Logs: $log"
    L ""
    L "Next steps:"
    L "  - Access the app at http://localhost:8080"
    L "  - View service logs: Get-Content logs\out.log -Tail 20"
    L "  - Stop service: .\scripts\stop_service.ps1"
    L ""
    if (-not $isAdmin) {
        L "Note: Run as Administrator to enable auto-start at logon"
    }
    L "========================================="
    
    "=== Completed: $(Get-Date -Format o) ===" | Out-File $log -Append
    
    Write-Host ""
    Write-Host "Setup completed successfully! See $log for details." -ForegroundColor Green
    Write-Host "Service should be running at http://localhost:8080" -ForegroundColor Green
    exit 0

} catch {
    L "ERROR: $($_.Exception.Message)"
    L "Stack trace: $($_.ScriptStackTrace)"
    Write-Host ""
    Write-Host "ERROR during setup. See $log for details" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
