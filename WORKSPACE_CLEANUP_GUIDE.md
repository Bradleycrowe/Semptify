# Semptify Workspace Cleanup Guide

## Current Situation
You have **multiple Semptify directories** with different spellings and duplicated content across your PC.

## Active Production Repository
**✅ KEEP THIS ONE - Connected to GitHub:**
- **Primary:** `C:\Semptify\Semptify\`
- **Worktree:** `C:\Semptify\Semptify.worktrees\main\`
- **Remote:** https://github.com/Bradleycrowe/Semptify.git
- **Status:** This is what's deployed to Render

## All Semptify Directories Found

### Primary Locations (Review Before Deleting)
1. ✅ **C:\Semptify\Semptify** - ACTIVE git repo, connected to GitHub
2. ✅ **C:\Semptify\Semptify.worktrees\main** - Clean worktree we use to push fixes
3. ⚠️ **C:\Semptify\SemptifyGUI** - Possibly old, check if needed
4. ⚠️ **C:\Users\bradc\SemptifyGUI** - User directory copy

### Archive/Backup Directories (Safe to Delete After Verification)
5. 📦 **C:\msndopilot\Semptify_Full_ModulePack_2025-10-26** - Old backup
6. 📦 **C:\repos git\UTAV\Semptify** - Different repo location
7. 📦 **C:\Semptify\workspaces\Semptify** - Workspace copy
8. 📦 **C:\Users\bradc\SemptifyBlueprints** - Documentation/design files

### Nested Duplicates (Likely Safe to Delete)
9. ❌ **C:\Semptify\Semptify\Semptify** - Nested duplicate
10. ❌ **C:\Semptify\Semptify\SemptifyGUI** - Nested old version
11. ❌ **C:\Semptify\SemptifyGUI\semptify-verify-module** - Test module
12. ❌ **C:\Semptify\Semptify\semptify-verify-module** - Test module duplicate
13. ❌ **C:\Semptify\Semptify\semptify-verify-module-1** - Test module duplicate

### Bundle/Package Directories (Archives)
14. 📦 **C:\Semptify\Semptify\SemptifyGUI_FlaskBundle_2025-10-18** - Old bundle
15. 📦 **C:\Semptify\SemptifyGUI\SemptifyGUI_FlaskBundle_2025-10-18** - Duplicate bundle
16. 📦 **C:\Semptify\Semptify\SemptifyOfficeBundle_2025-10-27** - Office bundle
17. 📦 **C:\Semptify\Semptify\SemptifyTools** - Tools package
18. 📦 **C:\Semptify\SemptifyGUI\SemptifyTools** - Duplicate tools

## Recommended Cleanup Strategy

### Phase 1: Verify Active Repository
```powershell
# Confirm the active repo
cd C:\Semptify\Semptify
git status
git log --oneline -5
git remote -v

# Confirm worktree
cd C:\Semptify\Semptify.worktrees\main
git status
```

### Phase 2: Archive Important Duplicates (Optional)
```powershell
# Create a backup archive directory
New-Item -Path "C:\Semptify_Archive_$(Get-Date -Format 'yyyy-MM-dd')" -ItemType Directory

# Move old bundles to archive (optional - only if you want to keep them)
Move-Item "C:\msndopilot\Semptify_Full_ModulePack_2025-10-26" "C:\Semptify_Archive_$(Get-Date -Format 'yyyy-MM-dd')\"
Move-Item "C:\Semptify\Semptify\SemptifyOfficeBundle_2025-10-27" "C:\Semptify_Archive_$(Get-Date -Format 'yyyy-MM-dd')\"
```

### Phase 3: Safe Cleanup (After Verification)
**⚠️ ONLY RUN AFTER CONFIRMING YOU DON'T NEED THESE!**

```powershell
# Remove nested duplicates
Remove-Item "C:\Semptify\Semptify\Semptify" -Recurse -Force
Remove-Item "C:\Semptify\Semptify\SemptifyGUI" -Recurse -Force
Remove-Item "C:\Semptify\Semptify\semptify-verify-module" -Recurse -Force
Remove-Item "C:\Semptify\Semptify\semptify-verify-module-1" -Recurse -Force

# Remove old bundles (if already archived or not needed)
Remove-Item "C:\Semptify\Semptify\SemptifyGUI_FlaskBundle_2025-10-18" -Recurse -Force
Remove-Item "C:\Semptify\Semptify\SemptifyTools" -Recurse -Force
```

### Phase 4: Review Top-Level Duplicates
```powershell
# Check what's in these directories before deleting
explorer "C:\Semptify\SemptifyGUI"
explorer "C:\Users\bradc\SemptifyGUI"
explorer "C:\repos git\UTAV\Semptify"
explorer "C:\Semptify\workspaces\Semptify"

# If they're old/unused, remove them:
# Remove-Item "C:\Semptify\SemptifyGUI" -Recurse -Force
# Remove-Item "C:\Users\bradc\SemptifyGUI" -Recurse -Force
```

## Final Clean Structure (Goal)
```
C:\Semptify\
├── Semptify\                    ← Active git repository
│   ├── .git\
│   ├── Semptify.py
│   ├── run_prod.py
│   ├── templates\
│   ├── static\
│   └── ... (all your source code)
└── Semptify.worktrees\
    └── main\                    ← Clean worktree for pushes
        └── (same files as above)
```

## Quick Cleanup Script (Conservative)
**This removes only obvious duplicates - run after manual verification:**

```powershell
# Navigate to main repo
cd C:\Semptify\Semptify

# Remove nested duplicates (safe - they're inside the main repo)
$toRemove = @(
    "C:\Semptify\Semptify\Semptify",
    "C:\Semptify\Semptify\SemptifyGUI",
    "C:\Semptify\Semptify\semptify-verify-module",
    "C:\Semptify\Semptify\semptify-verify-module-1",
    "C:\Semptify\SemptifyGUI\semptify-verify-module",
    "C:\Semptify\SemptifyGUI\semptify-verify-module-1"
)

foreach ($path in $toRemove) {
    if (Test-Path $path) {
        Write-Host "Removing: $path" -ForegroundColor Yellow
        Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "✓ Removed" -ForegroundColor Green
    }
}

Write-Host "`nCleanup complete. Check remaining directories manually." -ForegroundColor Cyan
```

## What NOT to Delete
- ✅ `C:\Semptify\Semptify\` (main repository)
- ✅ `C:\Semptify\Semptify.worktrees\` (worktree for clean pushes)
- ⚠️ Any directory you're actively working in
- ⚠️ Any directory with uncommitted changes

## Check for Uncommitted Work
Before deleting any directory, check for uncommitted changes:

```powershell
# Check a directory for git status
cd "C:\path\to\directory"
git status 2>$null
if ($?) {
    Write-Host "This is a git repo - check for uncommitted changes!"
    git status --short
}
```

## Disk Space Recovery Estimate
Based on typical Semptify installation:
- Each full copy: ~50-200 MB
- With 15+ duplicates: Potential to free **1-3 GB**

## After Cleanup
1. Verify the main repo still works: `cd C:\Semptify\Semptify; python Semptify.py`
2. Confirm git pushes still work: `cd C:\Semptify\Semptify.worktrees\main; git status`
3. Update any shortcuts or scripts pointing to old locations

## Questions Before You Delete?
- Are any old directories in use by running processes?
- Do you have any custom configurations or data files in the duplicates?
- Have you confirmed backups exist elsewhere (GitHub is your backup for code)?
