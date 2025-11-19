<#
.SYNOPSIS
Regenerates aggregated references.json from individual source files.

.DESCRIPTION
Combines all JSON files in references/ (except references.json itself)
into a single versioned references.json with metadata.
#>

$ErrorActionPreference = "Stop"

Write-Host "Updating aggregated library..." -ForegroundColor Cyan

$sourceDir = "modules/legal_library/references"
$targetFile = "$sourceDir/references.json"
$allRefs = @()

Get-ChildItem "$sourceDir/*.json" -Exclude "references.json" | ForEach-Object {
    $content = Get-Content -Path $_.FullName -Raw | ConvertFrom-Json
    $allRefs += $content
    Write-Host "  Loaded $($content.Count) from $($_.Name)" -ForegroundColor Gray
}

$output = @{
    version = "0.1.0"
    generated = (Get-Date -Format "yyyy-MM-dd")
    total_entries = $allRefs.Count
    references = $allRefs
}

$output | ConvertTo-Json -Depth 10 | Set-Content -Path $targetFile -Encoding UTF8

Write-Host "✓ Wrote $($allRefs.Count) entries → references.json" -ForegroundColor Green
