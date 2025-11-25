$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$Desktop\Semptify.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Semptify\Semptify\launch_semptify.vbs"
$Shortcut.WorkingDirectory = "C:\Semptify\Semptify"
$Shortcut.Description = "Start Semptify Production Server"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,44"  # Scales/justice icon
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: Semptify.lnk" -ForegroundColor Green
