# Get URL prefixes for each GUI
Write-Host "
=== Semptify GUI Interfaces ===" -ForegroundColor Cyan

$guis = @(
    @{Name="Brad GUI"; File="brad_gui_routes.py"; BP="brad_bp"},
    @{Name="Modern GUI"; File="modern_gui_routes.py"; BP="modern_gui_bp"},
    @{Name="Main Dashboard"; File="main_dashboard_routes.py"; BP="main_dashboard_bp"},
    @{Name="Learning Dashboard"; File="learning_dashboard_routes.py"; BP="learning_dashboard_bp"},
    @{Name="Calendar Vault UI"; File="calendar_vault_ui_routes.py"; BP="calendar_vault_ui_bp"}
)

foreach ($gui in $guis) {
    if (Test-Path $gui.File) {
        $prefix = Select-String -Path $gui.File -Pattern "url_prefix\s*=\s*['\"]([^'\"]+)" | Select-Object -First 1
        if ($prefix) {
            $url = $prefix.Matches.Groups[1].Value
            Write-Host "
✓ $($gui.Name)" -ForegroundColor Green
            Write-Host "  File: $($gui.File)"
            Write-Host "  Blueprint: $($gui.BP)"
            Write-Host "  URL: http://localhost:5000$url" -ForegroundColor Cyan
        } else {
            Write-Host "
✓ $($gui.Name)" -ForegroundColor Green  
            Write-Host "  File: $($gui.File)"
            Write-Host "  Blueprint: $($gui.BP)"
        }
    }
}
