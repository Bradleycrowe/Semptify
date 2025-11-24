# EXISTING SECURITY AUDIT

Write-Host "
========================================" -ForegroundColor Cyan
Write-Host "  CURRENT SECURITY SYSTEMS IN SEMPTIFY" -ForegroundColor Cyan
Write-Host "========================================
" -ForegroundColor Cyan

# Check what exists in security.py
if (Test-Path "security.py") {
    Write-Host "📄 security.py EXISTS - Analyzing..." -ForegroundColor Green
    $content = Get-Content "security.py" -Raw
    
    Write-Host "
🔐 CURRENT SECURITY FEATURES:" -ForegroundColor Yellow
    
    # Check for admin tokens
    if ($content -match "admin.*token") {
        Write-Host "  ✓ Admin token validation (KEEP - convert to role-based)" -ForegroundColor Green
    }
    
    # Check for user tokens
    if ($content -match "user.*token" -or $content -match "validate_user") {
        Write-Host "  ✓ User token validation (KEEP - convert to role-based)" -ForegroundColor Green
    }
    
    # Check for rate limiting
    if ($content -match "rate.*limit") {
        Write-Host "  ✓ Rate limiting (KEEP - apply to all roles)" -ForegroundColor Green
    }
    
    # Check for CSRF
    if ($content -match "csrf") {
        Write-Host "  ✓ CSRF protection (KEEP - standard security)" -ForegroundColor Green
    }
    
    # Check for session management
    if ($content -match "session") {
        Write-Host "  ✓ Session management (KEEP - needed for role storage)" -ForegroundColor Green
    }
    
    # Check for metrics
    if ($content -match "metric") {
        Write-Host "  ✓ Metrics/monitoring (KEEP - audit trail)" -ForegroundColor Green
    }
    
    # Check for breakglass
    if ($content -match "breakglass") {
        Write-Host "  ✓ Break-glass emergency access (KEEP - maps to Developer role)" -ForegroundColor Green
    }
    
    Write-Host "
📊 SECURITY.PY STATS:" -ForegroundColor Yellow
    $lines = ($content -split "
").Count
    $functions = ([regex]::Matches($content, "def\s+\w+")).Count
    Write-Host "  Lines: $lines"
    Write-Host "  Functions: $functions"
}

# Check for scattered security in other files
Write-Host "

🔍 CHECKING FOR SCATTERED SECURITY..." -ForegroundColor Yellow

$securityFiles = @()
Get-ChildItem -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match "@.*auth|@.*login|@.*require|validate.*token|check.*permission") {
        $matches = ([regex]::Matches($content, "@.*auth|@.*login|@.*require|validate.*token|check.*permission")).Count
        if ($matches -gt 0) {
            $securityFiles += [PSCustomObject]@{
                File = $_.Name
                Matches = $matches
            }
        }
    }
}

if ($securityFiles.Count -gt 0) {
    Write-Host "
⚠️  SECURITY CODE FOUND IN OTHER FILES:" -ForegroundColor Red
    $securityFiles | Sort-Object -Property Matches -Descending | Select-Object -First 10 | ForEach-Object {
        Write-Host "  $($_.File): $($_.Matches) security checks" -ForegroundColor Yellow
    }
}

# Check user_database.py
if (Test-Path "user_database.py") {
    Write-Host "
📊 user_database.py:" -ForegroundColor Yellow
    $content = Get-Content "user_database.py" -Raw
    if ($content -match "password") {
        Write-Host "  ✓ Has password handling (KEEP)" -ForegroundColor Green
    }
    if ($content -match "remember.*token") {
        Write-Host "  ✓ Has remember tokens (KEEP)" -ForegroundColor Green
    }
    if ($content -match "role") {
        Write-Host "  ✓ Already has role support! (EXTEND)" -ForegroundColor Cyan
    } else {
        Write-Host "  ✗ No role column yet (ADD)" -ForegroundColor Red
    }
}

Write-Host "

========================================" -ForegroundColor Cyan
Write-Host "  RECOMMENDATIONS" -ForegroundColor Cyan
Write-Host "========================================
" -ForegroundColor Cyan

Write-Host "🎯 UNIFIED SECURITY MODULE APPROACH:
" -ForegroundColor Green

Write-Host "✅ KEEP IN security.py (consolidate):" -ForegroundColor Green
Write-Host "  1. Admin token validation → Role validation (UserRole.ADMIN)"
Write-Host "  2. User token validation → Role validation (UserRole.USER+)"
Write-Host "  3. Rate limiting (apply to all roles)"
Write-Host "  4. CSRF protection (standard web security)"
Write-Host "  5. Session management (stores user_id + user_role)"
Write-Host "  6. Metrics/audit logging"
Write-Host "  7. Break-glass → Emergency Developer access"

Write-Host "
❌ REMOVE/CONSOLIDATE:" -ForegroundColor Red
Write-Host "  1. Duplicate token systems → Single role-based auth"
Write-Host "  2. Scattered @auth decorators → Use @require_role()"
Write-Host "  3. Multiple token files (admin_tokens.json, users.json) → Database"
Write-Host "  4. Per-route security checks → Decorator pattern"

Write-Host "
🆕 ADD TO security.py:" -ForegroundColor Yellow
Write-Host "  1. @require_role(UserRole.X) decorator"
Write-Host "  2. has_permission(user_role, required_role) checker"
Write-Host "  3. get_user_role(user_id) from database"
Write-Host "  4. Role upgrade request system"
Write-Host "  5. Role change audit logging"

Write-Host "
📁 FINAL STRUCTURE:" -ForegroundColor Cyan
Write-Host "  security.py - SINGLE security module with:"
Write-Host "    • Role-based authentication (@require_role)"
Write-Host "    • Token validation (legacy support during migration)"
Write-Host "    • Rate limiting"
Write-Host "    • CSRF protection"
Write-Host "    • Session management"
Write-Host "    • Audit logging"
Write-Host "    • Emergency access (break-glass)"
Write-Host "
  user_database.py - User data with:"
Write-Host "    • user_role column (0-5)"
Write-Host "    • Password hashing"
Write-Host "    • Remember tokens"
Write-Host "    • Login tracking"

Write-Host "
✨ MIGRATION STRATEGY:" -ForegroundColor Magenta
Write-Host "  Phase 1: Add new role system alongside existing security"
Write-Host "  Phase 2: Convert routes one-by-one to use @require_role"
Write-Host "  Phase 3: Keep old token validation as fallback (3 months)"
Write-Host "  Phase 4: Remove old token system after full migration"

Write-Host "
💡 ANSWER: YES - One unified security.py module!" -ForegroundColor Green
Write-Host "   But keep old system during migration for safety.
"
