# Build script for Dakota County Eviction Defense Module
# Creates checkpoint zip for distribution

$ErrorActionPreference = "Stop"
$moduleDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$moduleName = "DakotaCounty_EvictionDefense_2025-11-21"
$zipPath = Join-Path (Split-Path -Parent $moduleDir) "$moduleName.zip"

Write-Host "Building Dakota County Eviction Defense Module..." -ForegroundColor Cyan

# Files to include
$files = @(
    "README.md",
    "process_flow.md",
    "motions_actions.md",
    "proactive_tactics.md",
    "statutes_forms.md",
    "ui_strings.json",
    "build_dakota_module.ps1"
)

# Verify all files exist
$missing = @()
foreach ($file in $files) {
    $fullPath = Join-Path $moduleDir $file
    if (-not (Test-Path $fullPath)) {
        $missing += $file
    }
}

if ($missing.Count -gt 0) {
    Write-Host "ERROR: Missing files:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}

# Remove existing zip if present
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "Removed existing zip: $zipPath" -ForegroundColor Yellow
}

# Create zip using .NET (PowerShell 5+ compatible)
Add-Type -AssemblyName System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)

foreach ($file in $files) {
    $fullPath = Join-Path $moduleDir $file
    $entryName = "$moduleName/$file"
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $fullPath, $entryName) | Out-Null
    Write-Host "Added: $file" -ForegroundColor Green
}

$zip.Dispose()

Write-Host "`nBuild complete!" -ForegroundColor Green
Write-Host "Output: $zipPath" -ForegroundColor Cyan
Write-Host "Files: $($files.Count)" -ForegroundColor Cyan

# Display zip contents
Write-Host "`nZip contents:" -ForegroundColor Yellow
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipRead = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
$zipRead.Entries | ForEach-Object { Write-Host "  $($_.FullName)" }
$zipRead.Dispose()

Write-Host "`nReady for distribution or import into Semptify library." -ForegroundColor Cyan
