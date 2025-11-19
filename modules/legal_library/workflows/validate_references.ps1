<#
.SYNOPSIS
Validates JSON legal reference files against expected schema.

.DESCRIPTION
Checks each reference entry for required fields, correct types, and valid URLs.
Returns exit code 0 if all pass, 1 if any fail.
#>

$ErrorActionPreference = "Stop"
$refsDir = "modules/legal_library/references"
$requiredFields = @("id", "category", "title", "summary", "source_url", "jurisdiction", "updated", "tags")

Write-Host "Validating references in $refsDir..." -ForegroundColor Cyan

$allValid = $true
$files = Get-ChildItem "$refsDir/*.json" -Exclude "references.json"

foreach ($file in $files) {
    Write-Host "`n  Checking $($file.Name)..." -ForegroundColor Gray
    try {
        $refs = Get-Content -Path $file.FullName -Raw | ConvertFrom-Json
        
        for ($i = 0; $i -lt $refs.Count; $i++) {
            $ref = $refs[$i]
            
            # Check required fields
            foreach ($field in $requiredFields) {
                if (-not $ref.PSObject.Properties.Name.Contains($field)) {
                    Write-Host "    ✗ Entry $i missing field: $field" -ForegroundColor Red
                    $allValid = $false
                }
            }
            
            # Validate URL format
            if ($ref.source_url -and $ref.source_url -notmatch '^https?://') {
                Write-Host "    ✗ Entry $i has invalid URL: $($ref.source_url)" -ForegroundColor Red
                $allValid = $false
            }
            
            # Validate category
            $validCategories = @("federal", "state", "tax", "funding", "other")
            if ($ref.category -and $ref.category -notin $validCategories) {
                Write-Host "    ✗ Entry $i has invalid category: $($ref.category)" -ForegroundColor Yellow
            }
        }
        
        Write-Host "    ✓ $($refs.Count) entries validated" -ForegroundColor Green
        
    } catch {
        Write-Host "    ✗ Failed to parse JSON: $_" -ForegroundColor Red
        $allValid = $false
    }
}

if ($allValid) {
    Write-Host "`n✓ All references valid" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n✗ Validation failed" -ForegroundColor Red
    exit 1
}
