# Dakota County Eviction Defense Module Validation Script
# Runs bi-weekly (twice per week) to verify content accuracy and freshness
# Checks: statute URLs, form links, content updates, statutory amendments

param(
    [switch]$SendEmail = $false,
    [string]$EmailTo = "",
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"
$moduleDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$validationLog = Join-Path $moduleDir "validation_log.json"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Initialize results
$results = @{
    timestamp = $timestamp
    status = "unknown"
    checks = @()
    warnings = @()
    errors = @()
    recommendations = @()
}

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Dakota County Eviction Defense Module Validation" -ForegroundColor White
Write-Host "  Run: $timestamp" -ForegroundColor Gray
Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# Helper: Test URL accessibility
function Test-UrlAccessible {
    param([string]$Url, [string]$Description)
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✓ $Description" -ForegroundColor Green
            return @{ passed = $true; url = $Url; description = $Description; status = $response.StatusCode }
        } else {
            Write-Host "  ⚠ $Description (Status: $($response.StatusCode))" -ForegroundColor Yellow
            return @{ passed = $false; url = $Url; description = $Description; status = $response.StatusCode; warning = "Non-200 status" }
        }
    } catch {
        Write-Host "  ✗ $Description (Error: $($_.Exception.Message))" -ForegroundColor Red
        return @{ passed = $false; url = $Url; description = $Description; error = $_.Exception.Message }
    }
}

# Helper: Check file freshness
function Test-FileFreshness {
    param([string]$FilePath, [int]$MaxDaysOld = 90)
    
    if (Test-Path $FilePath) {
        $file = Get-Item $FilePath
        $age = (Get-Date) - $file.LastWriteTime
        $fileName = $file.Name
        
        if ($age.TotalDays -gt $MaxDaysOld) {
            Write-Host "  ⚠ $fileName is $([int]$age.TotalDays) days old (threshold: $MaxDaysOld)" -ForegroundColor Yellow
            return @{ passed = $false; file = $fileName; age_days = [int]$age.TotalDays; warning = "File may be stale" }
        } else {
            Write-Host "  ✓ $fileName is current ($([int]$age.TotalDays) days old)" -ForegroundColor Green
            return @{ passed = $true; file = $fileName; age_days = [int]$age.TotalDays }
        }
    } else {
        Write-Host "  ✗ $fileName not found" -ForegroundColor Red
        return @{ passed = $false; file = (Split-Path -Leaf $FilePath); error = "File not found" }
    }
}

# Helper: Check for statute amendments (web scraping placeholder)
function Test-StatuteUpdates {
    param([string]$StatuteUrl)
    
    # Placeholder: In production, scrape MN Legislature site for "Last Amended" date
    # For now, just check URL accessibility
    try {
        $response = Invoke-WebRequest -Uri $StatuteUrl -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        
        # Basic check: Look for "2024" or "2025" in content to verify recent activity
        if ($response.Content -match "2025|2024") {
            Write-Host "  ✓ Statute page contains recent year references" -ForegroundColor Green
            return @{ passed = $true; url = $StatuteUrl; note = "Recent activity detected" }
        } else {
            Write-Host "  ⚠ Statute page may be outdated (no 2024/2025 references)" -ForegroundColor Yellow
            return @{ passed = $false; url = $StatuteUrl; warning = "No recent year references found" }
        }
    } catch {
        Write-Host "  ✗ Cannot access statute page: $($_.Exception.Message)" -ForegroundColor Red
        return @{ passed = $false; url = $StatuteUrl; error = $_.Exception.Message }
    }
}

# CHECK 1: External Links (Forms & Statutes)
Write-Host "[1] Checking External Links..." -ForegroundColor Cyan

$linkChecks = @(
    @{
        url = "https://www.mncourts.gov/getforms/housing-landlord-tenant"
        description = "MN Judicial Branch Housing Forms"
    },
    @{
        url = "https://www.lawhelpmn.org/self-help-library/legal-resource/landlord-and-tenant-problems-minnesota-court-forms-and-information"
        description = "LawHelp MN Eviction Resources"
    },
    @{
        url = "https://www.revisor.mn.gov/statutes/cite/504B"
        description = "MN Statutes Chapter 504B"
    },
    @{
        url = "https://www.revisor.mn.gov/statutes/cite/484.014"
        description = "MN Statute § 484.014 (Expungement)"
    }
)

foreach ($link in $linkChecks) {
    $result = Test-UrlAccessible -Url $link.url -Description $link.description
    $results.checks += $result
    
    if (-not $result.passed) {
        if ($result.error) {
            $results.errors += "External link failed: $($link.description) - $($result.error)"
        } else {
            $results.warnings += "External link warning: $($link.description) - $($result.warning)"
        }
    }
}

# CHECK 2: File Freshness
Write-Host "`n[2] Checking File Freshness..." -ForegroundColor Cyan

$moduleFiles = @(
    "process_flow.md",
    "motions_actions.md",
    "proactive_tactics.md",
    "statutes_forms.md"
)

foreach ($file in $moduleFiles) {
    $filePath = Join-Path $moduleDir $file
    $result = Test-FileFreshness -FilePath $filePath -MaxDaysOld 90
    $results.checks += $result
    
    if (-not $result.passed) {
        if ($result.error) {
            $results.errors += "File check failed: $file - $($result.error)"
        } else {
            $results.warnings += "File freshness warning: $file is $($result.age_days) days old"
            $results.recommendations += "Review $file for accuracy; consider updating if statutes changed"
        }
    }
}

# CHECK 3: Statute Amendment Detection
Write-Host "`n[3] Checking for Statute Amendments..." -ForegroundColor Cyan

$statuteUrls = @(
    "https://www.revisor.mn.gov/statutes/cite/504B.321",  # Service requirements
    "https://www.revisor.mn.gov/statutes/cite/504B.285",  # Retaliation
    "https://www.revisor.mn.gov/statutes/cite/504B.161"   # Habitability
)

foreach ($url in $statuteUrls) {
    $result = Test-StatuteUpdates -StatuteUrl $url
    $results.checks += $result
    
    if (-not $result.passed) {
        if ($result.error) {
            $results.errors += "Statute check failed: $url - $($result.error)"
        } else {
            $results.warnings += "Statute warning: $url - $($result.warning)"
        }
    }
}

# CHECK 4: Content Integrity (Placeholder fields present)
Write-Host "`n[4] Checking Motion Template Integrity..." -ForegroundColor Cyan

$motionsPath = Join-Path $moduleDir "motions_actions.md"
if (Test-Path $motionsPath) {
    $content = Get-Content -Path $motionsPath -Raw
    
    $requiredPlaceholders = @(
        "{{CASE_NO}}",
        "{{TENANT_NAME}}",
        "{{HEARING_DATE}}",
        "{{SERVICE_DATE}}"
    )
    
    $missingPlaceholders = @()
    foreach ($placeholder in $requiredPlaceholders) {
        if ($content -notmatch [regex]::Escape($placeholder)) {
            $missingPlaceholders += $placeholder
        }
    }
    
    if ($missingPlaceholders.Count -eq 0) {
        Write-Host "  ✓ All required placeholders present in motion templates" -ForegroundColor Green
        $results.checks += @{ passed = $true; check = "Template placeholders"; note = "All present" }
    } else {
        Write-Host "  ⚠ Missing placeholders: $($missingPlaceholders -join ', ')" -ForegroundColor Yellow
        $results.warnings += "Missing placeholders in motions_actions.md: $($missingPlaceholders -join ', ')"
        $results.checks += @{ passed = $false; check = "Template placeholders"; warning = "Missing: $($missingPlaceholders -join ', ')" }
    }
} else {
    Write-Host "  ✗ motions_actions.md not found" -ForegroundColor Red
    $results.errors += "motions_actions.md not found"
    $results.checks += @{ passed = $false; check = "Template integrity"; error = "File not found" }
}

# SUMMARY
Write-Host "`n════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
$totalChecks = $results.checks.Count
$passedChecks = ($results.checks | Where-Object { $_.passed -eq $true }).Count
$failedChecks = $totalChecks - $passedChecks

if ($results.errors.Count -eq 0 -and $results.warnings.Count -eq 0) {
    $results.status = "healthy"
    Write-Host "  ✅ VALIDATION PASSED" -ForegroundColor Green
    Write-Host "  All checks passed ($passedChecks/$totalChecks)" -ForegroundColor Gray
} elseif ($results.errors.Count -eq 0) {
    $results.status = "warning"
    Write-Host "  ⚠️  VALIDATION COMPLETED WITH WARNINGS" -ForegroundColor Yellow
    Write-Host "  Passed: $passedChecks/$totalChecks | Warnings: $($results.warnings.Count)" -ForegroundColor Gray
} else {
    $results.status = "failed"
    Write-Host "  ❌ VALIDATION FAILED" -ForegroundColor Red
    Write-Host "  Passed: $passedChecks/$totalChecks | Errors: $($results.errors.Count) | Warnings: $($results.warnings.Count)" -ForegroundColor Gray
}

Write-Host "════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# Display warnings
if ($results.warnings.Count -gt 0) {
    Write-Host "Warnings:" -ForegroundColor Yellow
    foreach ($warning in $results.warnings) {
        Write-Host "  • $warning" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Display errors
if ($results.errors.Count -gt 0) {
    Write-Host "Errors:" -ForegroundColor Red
    foreach ($error in $results.errors) {
        Write-Host "  • $error" -ForegroundColor Red
    }
    Write-Host ""
}

# Display recommendations
if ($results.recommendations.Count -gt 0) {
    Write-Host "Recommendations:" -ForegroundColor Cyan
    foreach ($rec in $results.recommendations) {
        Write-Host "  • $rec" -ForegroundColor Cyan
    }
    Write-Host ""
}

# Save validation log
$results | ConvertTo-Json -Depth 5 | Set-Content -Path $validationLog -Encoding UTF8
Write-Host "Validation log saved: $validationLog" -ForegroundColor Gray

# Email notification (if enabled)
if ($SendEmail -and $EmailTo) {
    $subject = "Dakota Eviction Module Validation: $($results.status.ToUpper())"
    $body = @"
Dakota County Eviction Defense Module Validation Report
Run: $timestamp
Status: $($results.status.ToUpper())

Summary:
- Total Checks: $totalChecks
- Passed: $passedChecks
- Failed: $failedChecks
- Errors: $($results.errors.Count)
- Warnings: $($results.warnings.Count)

$(if ($results.errors.Count -gt 0) { "ERRORS:`n" + ($results.errors | ForEach-Object { "  • $_" }) -join "`n" } else { "" })

$(if ($results.warnings.Count -gt 0) { "`nWARNINGS:`n" + ($results.warnings | ForEach-Object { "  • $_" }) -join "`n" } else { "" })

$(if ($results.recommendations.Count -gt 0) { "`nRECOMMENDATIONS:`n" + ($results.recommendations | ForEach-Object { "  • $_" }) -join "`n" } else { "" })

Full log: $validationLog
"@
    
    try {
        # Placeholder: Use Send-MailMessage or external SMTP
        Write-Host "`nEmail notification would be sent to: $EmailTo" -ForegroundColor Cyan
        Write-Host "Subject: $subject" -ForegroundColor Gray
        # Send-MailMessage -To $EmailTo -Subject $subject -Body $body -SmtpServer "smtp.example.com"
    } catch {
        Write-Host "Failed to send email: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Exit code
if ($results.status -eq "failed") {
    exit 1
} else {
    exit 0
}
