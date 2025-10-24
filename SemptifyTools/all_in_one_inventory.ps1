# All-in-one Semptify inventory script

$toolsPath = "SemptifyTools"
if (!(Test-Path $toolsPath)) {
    New-Item -ItemType Directory -Path $toolsPath | Out-Null
}

$modules = Get-ChildItem -Path "modules" -Recurse -Include *.py | Select-Object -ExpandProperty FullName
$pages = Get-ChildItem -Path "templates" -Recurse -Include *.html | Select-Object -ExpandProperty FullName

$report = @()
$report += "=== Semptify Module Inventory ==="
$report += $modules
$report += "`n=== Semptify HTML Page Inventory ==="
$report += $pages

$reportPath = Join-Path $toolsPath "inventory_report.txt"
$report | Set-Content $reportPath
powershell .\SemptifyTools\all_in_one_inventory.ps1
Write-Host "`nInventory saved to $reportPath`n"
Write-Host ($report -join "`n")
