# Add-ShellCheckToPath.ps1
# Adds shellcheck.exe to the user PATH on Windows
# Usage: Run in PowerShell as administrator

param(
    [string]$ShellCheckDir = "D:\shellcheck-v0.11.0 (1)"
)

function Info($msg) { Write-Host "[ShellCheck] $msg" -ForegroundColor Cyan }

if (-not (Test-Path "$ShellCheckDir\shellcheck.exe")) {
    Info "shellcheck.exe not found in $ShellCheckDir. Please download and place shellcheck.exe there."
    exit 1
}

$envPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($envPath -notlike "*$ShellCheckDir*") {
    Info "Adding $ShellCheckDir to user PATH."
    $newPath = "$envPath;$ShellCheckDir"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Info "PATH updated. You may need to restart VS Code and terminals."
} else {
    Info "$ShellCheckDir is already in PATH."
}

Info "Test: shellcheck --version"
try {
    & "$ShellCheckDir\shellcheck.exe" --version
} catch {
    Info "shellcheck.exe not found or not executable."
}
