# Semptify Public Exposure Modal Installer
$basePath = "$PSScriptRoot\Semptify\modules"
New-Item -ItemType Directory -Path $basePath -Force | Out-Null

# List of required files
$files = @(
    "public_exposure_modal.html",
    "violation_pattern_mapper.html",
    "rights_scenario_explorer.html",
    "fraud_exposure_dashboard.html",
    "license_disruption_tracker.html",
    "case_briefing.md"
)

# Copy each file into Semptify/modules
foreach ($file in $files) {
    Copy-Item -Path "$PSScriptRoot\$file" -Destination "$basePath\$file" -Force
}

# Update README.md
$readmePath = "$PSScriptRoot\Semptify\modules\README.md"
$entry = @"
### Public Exposure Modal

Combines all harm-mapping tools into one press-ready interface. Includes multilingual UI, emotional intro, and export/share buttons.
"@
Add-Content -Path $readmePath -Value $entry

Write-Host "✅ Semptify Public Exposure Modal installed successfully."
Write-Host "📂 Location: $basePath"
