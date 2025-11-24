# Create Desktop Shortcut for Semptify
# Run this script to add a Semptify icon to your desktop

$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = "$Desktop\Semptify.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Target the batch file
$Shortcut.TargetPath = "C:\Semptify\Semptify\Semptify.bat"
$Shortcut.WorkingDirectory = "C:\Semptify\Semptify"
$Shortcut.Description = "Semptify - Tenant Rights Protection Platform"
$Shortcut.WindowStyle = 1  # Normal window

# Try to use PowerShell icon as temporary icon
$Shortcut.IconLocation = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe,0"

$Shortcut.Save()

Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅ DESKTOP SHORTCUT CREATED!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "  📍 Location: $ShortcutPath" -ForegroundColor White
Write-Host ""
Write-Host "  Double-click the 'Semptify' icon on your desktop to:" -ForegroundColor Cyan
Write-Host "    ✓ Start Ollama AI" -ForegroundColor Gray
Write-Host "    ✓ Start Semptify server" -ForegroundColor Gray
Write-Host "    ✓ Open GUI in browser" -ForegroundColor Gray
Write-Host ""
Write-Host "  It works just like a Windows program!" -ForegroundColor Green
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

# Optional: Pin to taskbar instructions
Write-Host "💡 TIP: Right-click the desktop icon and select" -ForegroundColor Yellow
Write-Host "   'Pin to taskbar' to add it to your taskbar!" -ForegroundColor Yellow
Write-Host ""
