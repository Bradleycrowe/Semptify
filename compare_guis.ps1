Write-Host "
=== GUI Comparison Analysis ===" -ForegroundColor Cyan

# Brad GUI
Write-Host "
1. BRAD GUI (/brad/)" -ForegroundColor Yellow
Select-String -Path brad_gui_routes.py -Pattern "@brad_bp.route" | ForEach-Object { 
    if ($_.Line -match '@brad_bp\.route\("([^"]+)"') { 
        Write-Host "  - $($Matches[1])" 
    } 
} | Select-Object -First 12
Write-Host "  Purpose:" -ForegroundColor Cyan
Get-Content brad_gui_routes.py | Select-Object -First 20 | Select-String -Pattern "^#|'''|\"\"\"" | Select-Object -First 3

# Modern GUI  
Write-Host "
2. MODERN GUI (/app/)" -ForegroundColor Yellow
Select-String -Path modern_gui_routes.py -Pattern "@.*route" | ForEach-Object {
    if ($_.Line -match '@.*\.route\("([^"]+)"') {
        Write-Host "  - $($Matches[1])"
    }
}
Write-Host "  Purpose:" -ForegroundColor Cyan
Get-Content modern_gui_routes.py | Select-Object -First 15 | Select-String -Pattern "^#|'''|\"\"\"" | Select-Object -First 3

# Main Dashboard
Write-Host "
3. MAIN DASHBOARD" -ForegroundColor Yellow
Select-String -Path main_dashboard_routes.py -Pattern "@.*route" | ForEach-Object {
    if ($_.Line -match '@.*\.route\("([^"]+)"') {
        Write-Host "  - $($Matches[1])"
    }
}
Write-Host "  Purpose:" -ForegroundColor Cyan
Get-Content main_dashboard_routes.py | Select-Object -First 15 | Select-String -Pattern "^#|'''|\"\"\"" | Select-Object -First 3

# Learning Dashboard
Write-Host "
4. LEARNING DASHBOARD" -ForegroundColor Yellow
Select-String -Path learning_dashboard_routes.py -Pattern "@.*route" | ForEach-Object {
    if ($_.Line -match '@.*\.route\("([^"]+)"') {
        Write-Host "  - $($Matches[1])"
    }
} | Select-Object -First 8
Write-Host "  Purpose:" -ForegroundColor Cyan
Get-Content learning_dashboard_routes.py | Select-Object -First 15 | Select-String -Pattern "^#|'''|\"\"\"" | Select-Object -First 3

# Calendar Vault UI
Write-Host "
5. CALENDAR VAULT UI" -ForegroundColor Yellow
Select-String -Path calendar_vault_ui_routes.py -Pattern "@.*route" | ForEach-Object {
    if ($_.Line -match '@.*\.route\("([^"]+)"') {
        Write-Host "  - $($Matches[1])"
    }
}
Write-Host "  Purpose:" -ForegroundColor Cyan
Get-Content calendar_vault_ui_routes.py | Select-Object -First 15 | Select-String -Pattern "^#|'''|\"\"\"" | Select-Object -First 3
