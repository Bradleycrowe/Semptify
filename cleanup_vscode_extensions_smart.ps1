#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Smart cleanup: keep a small allowlist of extensions and uninstall everything else.
.DESCRIPTION
    Designed for Semptify (Python/Flask). Adjust $keep list as needed.
#>

$keep = @(
    # Python core
    'ms-python.python',
    'ms-python.vscode-pylance',
    'ms-python.debugpy',
    'ms-python.pylint',

    # GitHub + Copilot
    'github.copilot',
    'github.copilot-chat',
    'github.vscode-pull-request-github',
    'github.vscode-github-actions',

    # Flask/Jinja helpers
    'maveric.flask-helper',
    'waseemakram.jinja-snippets-flask',

    # Docker
    'ms-azuretools.vscode-docker',

    # Render integration
    'nplusone-studio.render',

    # Helpful infra
    'ms-azuretools.vscode-azure-github-copilot',
    'ms-azuretools.vscode-azure-mcp-server',
    'ms-vscode.vscode-websearchforcopilot'
)

$installed = code --list-extensions
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Could not list extensions. Is VS Code CLI installed and on PATH?' -ForegroundColor Red
    exit 1
}

$toRemove = $installed | Where-Object { $_ -notin $keep }

Write-Host "Installed: $($installed.Count) | To keep: $($keep.Count) | To remove: $($toRemove.Count)" -ForegroundColor Cyan
if ($toRemove.Count -eq 0) {
    Write-Host 'Nothing to remove.' -ForegroundColor Green
    exit 0
}

Write-Host "Keeping:" -ForegroundColor Green
$keep | ForEach-Object { Write-Host "  - $_" }

Write-Host "\nWill remove (sample up to 20):" -ForegroundColor Yellow
$toRemove | Select-Object -First 20 | ForEach-Object { Write-Host "  - $_" }

$resp = Read-Host '\nProceed to uninstall ALL non-keep extensions? (y/n)'
if ($resp -notin @('y','Y')) { Write-Host 'Cancelled.'; exit 0 }

$removed = 0; $failed = 0
foreach ($ext in $toRemove) {
    Write-Host -NoNewline "Uninstalling $ext... "
    code --uninstall-extension $ext *> $null
    if ($LASTEXITCODE -eq 0) { Write-Host 'OK' -ForegroundColor Green; $removed++ }
    else { Write-Host 'FAIL' -ForegroundColor Red; $failed++ }
}

Write-Host "\nDone. Removed: $removed, Failed: $failed" -ForegroundColor Cyan
Write-Host 'Restart VS Code to fully apply changes.' -ForegroundColor Yellow
