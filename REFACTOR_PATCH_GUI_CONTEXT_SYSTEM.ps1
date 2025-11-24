<#
.SYNOPSIS
    GUI Refactoring Patch - Context Data System Integration

.DESCRIPTION
    This script refactors all 5 GUIs to use the Context Data System instead of direct database queries.
    
    WHAT THIS DOES:
    - Replaces multiple SELECT queries with ONE call to get_context(user_id)
    - Cleaner code, faster performance, consistent data across all GUIs
    - Context Ring provides circular intelligence (documents ↔ timeline ↔ cases ↔ events)
    
    WHAT THIS DOES NOT DO:
    - Does NOT change database structure
    - Does NOT modify user_database.py
    - Does NOT touch INSERT/UPDATE queries (logging still works)

.NOTES
    Created: November 23, 2025
    Status: READY TO RUN (tested pattern on learning_dashboard_routes.py)
    Backup: Automatically creates .backup files before changes
    
    RUN THIS WHEN: Ready to connect all GUIs to Context Data System
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  GUI REFACTOR - Context Data System Integration" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# FILE 1: learning_dashboard_routes.py
# ============================================================================

Write-Host "[1/5] Refactoring learning_dashboard_routes.py..." -ForegroundColor Yellow

$file1 = "C:\Semptify\Semptify\learning_dashboard_routes.py"

# Backup
Copy-Item $file1 "$file1.backup" -Force
Write-Host "  ✓ Backup created" -ForegroundColor Green

# Read file
$content = Get-Content $file1 -Raw -Encoding UTF8

# CHANGE 1: Already has import (verify)
if ($content -notmatch "from semptify_core import get_context") {
    $content = $content -replace "(from user_database import _get_db)", "`$1`nfrom semptify_core import get_context  # Context Data System"
    Write-Host "  ✓ Added Context System import" -ForegroundColor Green
} else {
    Write-Host "  ✓ Import already exists" -ForegroundColor Green
}

# CHANGE 2: Replace profile query
$oldProfilePattern = @'
    # Get user profile from database
    conn = _get_db\(\)
    cursor = conn\.cursor\(\)

    cursor\.execute\('''
        SELECT u\.\*, lp\.\*
        FROM users u
        LEFT JOIN user_learning_profiles lp ON u\.id = lp\.user_id
        WHERE u\.id = \?
    ''', \(user_id,\)\)
    
    profile = cursor\.fetchone\(\)
