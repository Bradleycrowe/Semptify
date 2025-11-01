# Semptify Communication Suite: Unified Wiring Script
# Created: 2025-11-01
# Author: Bradley + Copilot

$basePath = "C:\Semptify\LiveModules\CommunicationSuite"
$modules = @(
    "FormalMethods", "ContactManager", "CalendarEvents", "VaultModule",
    "LedgerModule", "DeliveryModule", "NotaryModule", "VoiceModule", "ScanModule"
)

# Create base folder
if (!(Test-Path $basePath)) { New-Item -ItemType Directory -Path $basePath }

# Create module folders
foreach ($mod in $modules) {
    $modPath = "$basePath\$mod"
    if (!(Test-Path $modPath)) { New-Item -ItemType Directory -Path $modPath }
    Write-Host "📦 Created module folder: $mod"
}

# Copy JSON scaffolds (assumes source files exist in Semptify/modules/)
$sourceBase = "C:\Semptify\modules\CommunicationSuite"
$files = @(
    "formal_communication.json", "contact_registry.json", "calendar_events.json",
    "vault_registry.json", "communication_ledger.json", "delivery_notary_registry.json",
    "notary_registry.json", "voice_triggers.json", "scan_modes.json",
    "modal_triggers.json", "help_text_multilingual.json"
)

foreach ($file in $files) {
    $src = "$sourceBase\$file"
    $dest = "$basePath\*\$file"
    Get-ChildItem $basePath -Directory | ForEach-Object {
        Copy-Item $src "$($_.FullName)\$file" -Force
    }
    Write-Host "✅ Wired: $file to all modules"
}

# Add README to each module
$readmeContent = @"
# Semptify Communication Suite Module

This module is part of the unified tenant-landlord communication system.
Includes multilingual help, modal triggers, and voice-ready onboarding.

Languages: English, Spanish, Somali, Hmong
Modal Triggers: View, Send, Track, Notarize, Scan, Record, Switch Language
"@
foreach ($mod in $modules) {
    $readmePath = "$basePath\$mod\README.md"
    $readmeContent | Out-File -Encoding UTF8 $readmePath
    Write-Host "📘 Added README to: $mod"
}

# Final confirmation
Write-Host "`n🎉 All Communication Suite modules wired and ready for deployment."
Write-Host "🔗 Path: $basePath"
