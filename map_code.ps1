# MAP CURRENT CODE ORGANIZATION

Write-Host "
═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🗺️  CURRENT CODE LOCATION AUDIT" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════
" -ForegroundColor Cyan

# Find all engine files
Write-Host "🔧 ENGINES (Business Logic):" -ForegroundColor Yellow
Get-ChildItem -Filter "*_engine.py" | ForEach-Object {
    $lines = (Get-Content $_.Name | Measure-Object -Line).Lines
    $functions = (Select-String -Path $_.Name -Pattern "^def " | Measure-Object).Count
    Write-Host "  📄 $($_.Name) - $lines lines, $functions functions" -ForegroundColor Green
}

# Find all module files
Write-Host "
📦 MODULES:" -ForegroundColor Yellow
Get-ChildItem -Filter "*_module*.py" | ForEach-Object {
    $lines = (Get-Content $_.Name | Measure-Object -Line).Lines
    Write-Host "  📄 $($_.Name) - $lines lines" -ForegroundColor Green
}

# Check for learning-related files
Write-Host "
🧠 LEARNING SYSTEM FILES:" -ForegroundColor Yellow
Get-ChildItem -Filter "*learning*.py" | ForEach-Object {
    $lines = (Get-Content $_.Name | Measure-Object -Line).Lines
    $hasEngine = Select-String -Path $_.Name -Pattern "def.*learn|def.*adapt|def.*suggest" -Quiet
    $type = if ($_.Name -match "_routes") { "ROUTE (GUI)" } 
             elseif ($_.Name -match "_engine") { "ENGINE (Core)" }
             else { "MODULE" }
    Write-Host "  📄 $($_.Name) - $lines lines [$type]" -ForegroundColor 
}

# Check for curiosity files
Write-Host "
🤔 CURIOSITY SYSTEM FILES:" -ForegroundColor Yellow
Get-ChildItem -Filter "*curiosity*.py" | ForEach-Object {
    $lines = (Get-Content $_.Name | Measure-Object -Line).Lines
    $hasEngine = Select-String -Path $_.Name -Pattern "def.*reason|def.*suggest|def.*adapt" -Quiet
    Write-Host "  📄 $($_.Name) - $lines lines" -ForegroundColor Green
}

# Check for seed files
Write-Host "
🌱 SEED FILES:" -ForegroundColor Yellow
Get-ChildItem -Filter "*seed*.py" | ForEach-Object {
    Write-Host "  📄 $($_.Name)" -ForegroundColor Green
}

# Check data/learning_patterns.json
Write-Host "
📊 DATA FILES:" -ForegroundColor Yellow
if (Test-Path "data/learning_patterns.json") {
    $size = (Get-Item "data/learning_patterns.json").Length
    Write-Host "  📄 data/learning_patterns.json - $size bytes" -ForegroundColor Green
}

# Analyze a key engine file
Write-Host "

═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📖 DETAILED ANALYSIS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════
" -ForegroundColor Cyan

if (Test-Path "curiosity_engine.py") {
    Write-Host "🔍 curiosity_engine.py CONTENTS:" -ForegroundColor Yellow
    $content = Get-Content "curiosity_engine.py" -Raw
    $functions = [regex]::Matches($content, "def\s+(\w+)") | ForEach-Object { $_.Groups[1].Value }
    Write-Host "  Functions: $($functions -join ', ')" -ForegroundColor Cyan
    
    if ($content -match "class\s+(\w+)") {
        Write-Host "  Classes: Found class definitions" -ForegroundColor Cyan
    }
}

# Check where business logic lives
Write-Host "

═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎯 ORGANIZATION SUMMARY" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════
" -ForegroundColor Cyan

Write-Host "📂 CURRENT STRUCTURE:" -ForegroundColor Yellow
Write-Host ""
Write-Host "ENGINES (Backend/Core Logic):" -ForegroundColor Green
Write-Host "  • *_engine.py files - Business logic, algorithms"
Write-Host "  • Should be in Semptify core"
Write-Host ""
Write-Host "ROUTES (Frontend/GUI):" -ForegroundColor Yellow
Write-Host "  • *_routes.py files - HTTP endpoints, templates"
Write-Host "  • Should call engines via core API"
Write-Host ""
Write-Host "MODULES (Utilities):" -ForegroundColor Cyan
Write-Host "  • Helper functions, shared code"
Write-Host "  • Could be in core or utils"

Write-Host "

💡 RECOMMENDATION:" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "MOVE TO semptify_core.py:" -ForegroundColor Green
Write-Host "  ✓ All *_engine.py files (business logic)"
Write-Host "  ✓ Learning patterns/seeds"
Write-Host "  ✓ Curiosity system"
Write-Host "  ✓ Data access functions"
Write-Host ""
Write-Host "KEEP IN GUIs (*_routes.py):" -ForegroundColor Yellow
Write-Host "  ✓ Route definitions (@app.route)"
Write-Host "  ✓ Template rendering"
Write-Host "  ✓ Request/response handling"
Write-Host "  ✓ Display logic only"
Write-Host ""
Write-Host "KEEP SEPARATE:" -ForegroundColor Cyan
Write-Host "  ✓ user_database.py (data layer)"
Write-Host "  ✓ security.py (auth/session)"
Write-Host "  ✓ Templates (HTML/CSS/JS)"
