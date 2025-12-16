# Fix modern_gui_routes.py to use existing vault.html template
$content = Get-Content "modern_gui_routes.py" -Raw
$content = $content -replace 'render_template\("modern_gui/vault\.html"', 'render_template("vault.html"'
Set-Content -Path "modern_gui_routes.py" -Value $content -Encoding UTF8
Write-Host "✓ Fixed vault template path in modern_gui_routes.py" -ForegroundColor Green
