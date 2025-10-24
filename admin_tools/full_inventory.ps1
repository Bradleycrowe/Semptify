$report = @()
$expectedDirs = @("modules", "templates", "static", "uploads", "logs", "security", "copilot_sync", "final_notices", "tests", ".github", "admin_tools")
$expectedFiles = @("Semptify.py", "run_prod.py", "requirements.txt", "README.md")

$report += "=== Directory Inventory ==="
Get-ChildItem -Directory | ForEach-Object {
    if ($expectedDirs -notcontains $_.Name) {
        $report += "⚠️  Unexpected directory: $($_.Name)"
    } else {
        $report += "✔ $($_.Name)"
    }
}

$report += "`n=== File Inventory ==="
Get-ChildItem -File | ForEach-Object {
    if ($expectedFiles -notcontains $_.Name) {
        $report += "⚠️  Unexpected file: $($_.Name)"
    } else {
        $report += "✔ $($_.Name)"
    }
}

$report += "`n=== Runtime Directory Check ==="
foreach ($dir in $expectedDirs) {
    if (!(Test-Path $dir)) {
        $report += "❌ Missing runtime dir: $dir"
    } else {
        $report += "✔ $dir exists"
    }
}

$report += "`n=== Module Inventory ==="
Get-ChildItem -Path "modules" -Recurse -Include *.py | ForEach-Object { $report += $_.FullName }

$report += "`n=== Template Inventory ==="
Get-ChildItem -Path "templates" -Recurse -Include *.html | ForEach-Object { $report += $_.FullName }

$report += "`n=== Static Asset Inventory ==="
Get-ChildItem -Path "static" -Recurse | ForEach-Object { $report += $_.FullName }

$report += "`n=== Notes, TODOs, and Instructions ==="
$searchPatterns = @("TODO", "NOTE", "INSTRUCTION", "FIXME")
foreach ($pattern in $searchPatterns) {
    $report += "`n--- $pattern ---"
    Get-ChildItem -Path . -Recurse -Include *.py,*.html,*.md | ForEach-Object {
        $matches = Select-String -Path $_.FullName -Pattern $pattern
        foreach ($m in $matches) {
            $report += "$($m.Path): $($m.Line)"
        }
    }
}

$reportPath = "admin_tools\full_inventory_report.txt"
$report | Set-Content $reportPath

Write-Host "`nFull inventory report saved to $reportPath"
Write-Host "Review this file for missing items, notes, TODOs, and instructions."

