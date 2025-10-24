# Semptify_Verify.ps1
# One-click verification for Semptify draft files

# === CONFIG ===
$libraryPath = "semptify_library_legal_resources\library_index.json"
$draftPath = "Semptify\modules\draft.txt"

# === LOAD LIBRARY ===
if (!(Test-Path $libraryPath)) {
    Write-Host "❌ Library file not found at $libraryPath"
    exit
}
$libraryJson = Get-Content $libraryPath -Raw | ConvertFrom-Json
$validCitations = $libraryJson.citations

# === LOAD DRAFT ===
if (!(Test-Path $draftPath)) {
    Write-Host "❌ Draft file not found at $draftPath"
    exit
}
$draftText = Get-Content $draftPath -Raw

# === EXTRACT CITATIONS ===
$statutes = Select-String -InputObject $draftText -Pattern "Minn\. Stat\. §\s*\d+[A-Za-z0-9\.\-]*" -AllMatches | ForEach-Object { $_.Matches.Value }
$cases = Select-String -InputObject $draftText -Pattern "[A-Z][a-z]+ v\. [A-Z][a-z]+, \d+ [A-Z]{2,4} \d+ \(\d{4}\)" -AllMatches | ForEach-Object { $_.Matches.Value }
$citations = $statutes + $cases

# === VERIFY ===
$verified = @()
$missing = @()
foreach ($c in $citations) {
    if ($validCitations -contains $c) {
        $verified += $c
    } else {
        $missing += $c
    }
}

# === CONFIDENCE ===
if ($missing.Count -eq 0) {
    $confidence = "High"
} elseif ($verified.Count -gt 0) {
    $confidence = "Medium"
} else {
    $confidence = "Low"
}

# === OUTPUT ===
Write-Host "`n=== Semptify Verification Results ==="
Write-Host "Confidence Level: $confidence`n"
Write-Host "✔ Verified Citations:"
$verified | ForEach-Object { Write-Host "  $_" }
Write-Host "`n✖ Missing Citations:"
$missing | ForEach-Object { Write-Host "  $_" }
Write-Host "`n===================================="

