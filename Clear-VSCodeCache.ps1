#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Clears VS Code workspace cache to fix task detection issues.
.DESCRIPTION
    This script removes cached VS Code workspace state that may contain
    stale task configurations (like /usr/local/bin/python on Windows).
    Safe to run - only deletes VS Code cache, not your code or settings.
#>

Write-Host "🔧 VS Code Cache Cleanup for Semptify" -ForegroundColor Cyan
Write-Host "=" * 60

$workspacePath = "C:\Semptify\Semptify"
$storageRoot = "$env:APPDATA\Code\User\workspaceStorage"

if (-not (Test-Path $storageRoot)) {
    Write-Host "✓ No workspace cache found (clean install)" -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "Searching for Semptify workspace cache..." -ForegroundColor Yellow

$cleaned = 0
Get-ChildItem -Path $storageRoot -Directory | ForEach-Object {
    $wsFile = Join-Path $_.FullName "workspace.json"
    if (Test-Path $wsFile) {
        $content = Get-Content $wsFile -Raw
        if ($content -match "Semptify") {
            Write-Host "  Found: $($_.Name)" -ForegroundColor White
            try {
                Remove-Item $_.FullName -Recurse -Force
                Write-Host "  ✓ Cleared cache: $($_.Name)" -ForegroundColor Green
                $cleaned++
            } catch {
                Write-Host "  ✗ Failed to clear: $_" -ForegroundColor Red
            }
        }
    }
}

Write-Host ""
if ($cleaned -eq 0) {
    Write-Host "✓ No stale cache found" -ForegroundColor Green
} else {
    Write-Host "✅ Cleared $cleaned workspace cache folder(s)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Close all VS Code windows"
Write-Host "  2. Reopen VS Code in: $workspacePath"
Write-Host "  3. Task detection will rebuild from .vscode/tasks.json"
Write-Host ""
Write-Host "The /usr/local/bin/python error should NOT reappear." -ForegroundColor Yellow
