# Full Setup Script Usage Guide

## Overview

The `scripts/full_setup.ps1` script provides complete automated setup and deployment for SemptifyGUI on Windows systems.

## What It Does

1. **Creates runtime folders**: `uploads`, `logs`, `copilot_sync`, `final_notices`, `security`, `sbom`
2. **Sets up Python virtual environment** (if not already present)
3. **Installs all dependencies** from `requirements.txt`
4. **Runs tests** with pytest to validate the installation
5. **Starts the production service** in the background via `scripts/start_service.ps1`
6. **Registers a Scheduled Task** (if running as Administrator) for auto-start at logon

## Usage

### Basic Usage (Regular User)

```powershell
cd D:\Semptify\SemptifyGUI
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\full_setup.ps1
```

This will set up everything except the Scheduled Task (requires admin privileges).

### Advanced Usage (Administrator)

Right-click PowerShell and select "Run as Administrator", then:

```powershell
cd D:\Semptify\SemptifyGUI
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\full_setup.ps1
```

This will perform the full setup including registering a Scheduled Task for auto-start at logon.

## What Happens During Execution

The script will:

1. Log all operations to `scripts/full_setup.log`
2. Create/verify runtime folders
3. Update `logs/init.log` with timestamp
4. Create `.venv` virtual environment (if missing)
5. Upgrade pip to latest version
6. Install all requirements from `requirements.txt`
7. Install pytest
8. Run all tests in the `tests/` directory
9. Start the production service (writes PID to `.service_semptify.pid`)
10. Check listening ports (8080, 5000)
11. If Administrator: Register "SemptifyGUI Service" Scheduled Task

## Scheduled Task Details

When run as Administrator, the script registers a Windows Scheduled Task with:

- **Name**: "SemptifyGUI Service"
- **Trigger**: At logon (any user)
- **Action**: Run `scripts/start_service.ps1` via PowerShell
- **User**: BUILTIN\Users
- **Run Level**: Highest (elevated)
- **Settings**: Start even on battery, don't stop if on battery, start when available

## After Running

Access the application at: **http://localhost:8080**

View service logs:
```powershell
Get-Content logs\out.log -Tail 20
Get-Content logs\err.log -Tail 20
```

Check service status:
```powershell
.\scripts\status_service.ps1
```

Stop the service:
```powershell
.\scripts\stop_service.ps1
```

## Troubleshooting

If the script fails:

1. Check the log file: `scripts\full_setup.log`
2. Ensure Python 3.11+ is installed and in PATH
3. Verify you have write permissions in the repository directory
4. For Scheduled Task issues, ensure you're running as Administrator

## Log Files

- `scripts\full_setup.log` - Full setup script execution log
- `logs\init.log` - Application initialization log
- `logs\out.log` - Service stdout output
- `logs\err.log` - Service stderr output
- `logs\pytest.out` - Test execution output
- `logs\pytest.err` - Test error output

## Exit Codes

- `0` - Success
- `1` - Error (check logs for details)
- `2` - Failed to start service process
