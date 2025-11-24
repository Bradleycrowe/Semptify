$files = @()
$files += Get-ChildItem -Filter "*gui*.py" -File
$files += Get-ChildItem -Filter "*dashboard*.py" -File  
$files += Get-ChildItem -Filter "*ui*.py" -File

Write-Host "
=== GUI/Dashboard/UI Files ===" -ForegroundColor Cyan
$files | Sort-Object Name -Unique | Select-Object Name, Length | Format-Table -AutoSize
