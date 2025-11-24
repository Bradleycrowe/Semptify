# Semptify Windows Launcher - Quick Reference

## What You Got

**Desktop Icon**: Blue "S" icon on your desktop - double-click to start Semptify like any Windows program

**One-Click Startup**: Automatically starts:
- Ollama AI service
- Semptify production server
- Opens GUI in browser

**No More Command Lines**: Just double-click the icon and wait 5-10 seconds!

---

## How to Use

### Start Semptify
1. **Double-click** the "Semptify" desktop icon
2. Wait for terminal window to show "✅ SEMPTIFY IS RUNNING!"
3. Browser opens automatically to the GUI

### Stop Semptify
- Close the terminal window (or press Ctrl+C)

### Pin to Taskbar (Optional)
- Right-click desktop icon → "Pin to taskbar"
- Now you can launch from taskbar like any other app!

---

## What Gets Started

When you click the icon:

1. **Ollama AI** - Local AI service (port 11434)
   - Auto-starts if not running
   - Provides AI assistant features

2. **Semptify Server** - Production WSGI server (port 8080)
   - Waitress server with 8 workers
   - Handles all web requests

3. **GUI Dashboard** - Opens in browser
   - http://localhost:8080/gui
   - Access all 43+ modules

---

## Files Created

\\\
Desktop:
  Semptify.lnk              # Desktop shortcut (double-click this!)

C:\Semptify\Semptify\:
  Semptify.bat              # Batch launcher
  Semptify_Launcher.ps1     # Main PowerShell script
  semptify_icon.ico         # Custom blue "S" icon
  Create_Desktop_Shortcut.ps1  # Shortcut installer
  generate_icon.py          # Icon generator script
\\\

---

## Troubleshooting

**Icon doesn't appear on desktop?**
- Run: \.\Create_Desktop_Shortcut.ps1\ from C:\Semptify\Semptify

**Server already running error?**
- Close any existing Semptify terminal windows first
- Or use Task Manager to end python.exe processes

**Ollama won't start?**
- Install from: https://ollama.com/download
- Or continue without AI (still works, just no AI features)

**Browser doesn't open?**
- Manually go to: http://localhost:8080/gui

---

## Advanced Options

### Run from Command Line (if needed)
\\\powershell
cd C:\Semptify\Semptify
.\Semptify_Launcher.ps1
\\\

### Just Start Server (no auto-launch browser)
\\\powershell
.\start_production.ps1
\\\

### Recreate Desktop Icon
\\\powershell
.\Create_Desktop_Shortcut.ps1
\\\

---

## System Requirements

- Windows 10/11
- Python 3.8+ with virtual environment
- Ollama (optional, for AI features)
- Modern web browser (Chrome, Edge, Firefox)

---

## URLs When Running

- **Main GUI**: http://localhost:8080/gui
- **Profiles**: http://localhost:8080/profiles
- **AI Assistant**: http://localhost:8080/gui/ai-dev
- **Admin**: http://localhost:8080/admin
- **Vault**: http://localhost:8080/vault

---

## Tips

💡 **Pin to Taskbar**: Right-click icon → "Pin to taskbar" for quick access

💡 **Safe to Click Multiple Times**: If server already running, just opens browser

💡 **Keep Terminal Open**: Don't close the terminal window while using Semptify

💡 **Clean Shutdown**: Always close terminal window properly (don't force-quit)

---

## Support

For issues, check:
1. Terminal window output for error messages
2. logs/ directory for detailed logs
3. Make sure port 8080 is not used by another app

