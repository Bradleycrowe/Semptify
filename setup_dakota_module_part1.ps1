# Semptify: Dakota County Eviction — Complete Interactive Module
# File: Semptify_DakotaEviction_Complete.ps1
# Integrates: Federal/State/County law, all forms, procedures, Zoom guidance, local contacts

$ErrorActionPreference = "Stop"

# ===== Paths =====
$root = Join-Path $PWD "Semptify"
$moduleRoot = Join-Path $root "modules"
$bundle = Join-Path $moduleRoot "DakotaCountyEviction"
$docs = Join-Path $bundle "docs"
$exports = Join-Path $bundle "exports"
$logs = Join-Path $bundle "logs"
$refs = Join-Path $bundle "authorities"
$forms = Join-Path $bundle "forms"
$templates_dir = Join-Path $bundle "templates"

$dirs = @($root,$moduleRoot,$bundle,$docs,$exports,$logs,$refs,$forms,$templates_dir)
foreach ($d in $dirs) { if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null } }

Write-Host "✓ Directory structure created" -ForegroundColor Green

# ===== Profile =====
$ProfilePath = Join-Path $bundle "litigant.json"
if (-not (Test-Path $ProfilePath)) {
  @{
    tenant_name = ""
    tenant_address = ""
    landlord_name = ""
    landlord_address = ""
    case_number = ""
    court_location = "Dakota County District Court"
    hearing_zoom_link = ""
    hearing_date = ""
    interpreter_lang = ""
    rent_assistance_contact = "360 Communities: (952) 985-5300"
    sheriff_contact = "Dakota County Sheriff: 651-438-4700"
    legal_aid_contact = "LADC: 952-431-3200 | SMRLS: 1-877-696-6529"
  } | ConvertTo-Json | Set-Content -Path $ProfilePath -Encoding UTF8
}

Write-Host "✓ Profile initialized" -ForegroundColor Green
