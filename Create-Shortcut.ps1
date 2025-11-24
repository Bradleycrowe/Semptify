# Create desktop shortcut for Semptify
$WshShell = New-Object -ComObject WScript.Shell
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Semptify.lnk"

$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"C:\Semptify\Semptify\Start-Semptify.ps1`""
$shortcut.WorkingDirectory = "C:\Semptify\Semptify"
$shortcut.Description = "Semptify - Brad's Single User System"
$shortcut.IconLocation = "shell32.dll,21"  # Folder with globe icon
$shortcut.Save()

Write-Host "`n✅ Desktop shortcut created: Semptify.lnk" -ForegroundColor Green
Write-Host "   Double-click to launch Semptify`n" -ForegroundColor Cyan
