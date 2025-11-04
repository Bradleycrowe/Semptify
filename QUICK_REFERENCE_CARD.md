# ⚡ COPILOT WORK QUICK REFERENCE CARD

**Bookmark this file - it has everything on one page!**

---

## 🎯 WHAT WAS CREATED IN THIS SESSION

| Item | Type | File | Purpose |
|------|------|------|---------|
| 1 | 🚀 Script | `start_production.py` | **MAIN LAUNCHER** - Run this to start server |
| 2 | 🚀 Script | `Start-Production.ps1` | Windows PowerShell launcher |
| 3 | 🚀 Script | `start_production.sh` | Linux/macOS launcher |
| 4 | 🚀 Script | `start.bat` | Windows double-click launcher |
| 5 | 🌐 Website | `templates/full_site.html` | Modern responsive website |
| 6 | 📖 Guide | `00_START_HERE.md` | **READ THIS FIRST** |
| 7 | 📖 Guide | `QUICK_START.md` | 5-minute setup guide |
| 8 | 📖 Guide | `PRODUCTION_STARTUP.md` | 15+ page comprehensive guide |
| 9 | 📖 Guide | `DEPLOYMENT_CI_CD.md` | Docker, K8s, AWS, Azure examples |
| 10 | 📖 Guide | `config.env.template` | Configuration reference (40+ options) |
| 11 | 📖 Guide | `COPILOT_SESSION_CONTEXT_MASTER.md` | **THIS FILE** - Master context |

---

## ⚡ START SERVER IN 30 SECONDS

### Windows
```powershell
cd c:\Semptify\Semptify
python start_production.py
```

### Linux/macOS
```bash
cd /path/to/Semptify
python start_production.py
```

**Then open:** http://localhost:8080

---

## 🔐 GENERATE YOUR KEYS (DO THIS FIRST)

### FLASK_SECRET (for server startup)
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output and set: $env:FLASK_SECRET = "YOUR_KEY"
```

### ADMIN TOKEN (for admin access)
```powershell
python -c "
from security import save_admin_token
aid, token = save_admin_token()
print(f'Token: {token}')
"
```

### USER TOKEN (for document vault)
```powershell
# Option 1: Visit http://localhost:8080/register
# Option 2: Via Python:
python -c "
from security import save_user_token
uid, token = save_user_token()
print(f'Token: {token}')
"
```

---

## 🌐 AFTER SERVER STARTS - WHAT TO ACCESS

| Page | URL | Requires |
|------|-----|----------|
| **Home** | http://localhost:8080 | Nothing |
| **Website** | http://localhost:8080/full_site | Nothing |
| **Health** | http://localhost:8080/health | Nothing |
| **Admin Panel** | http://localhost:8080/admin?token=YOUR_ADMIN_TOKEN | Admin token |
| **Document Vault** | http://localhost:8080/vault?user_token=YOUR_USER_TOKEN | User token |
| **Metrics** | http://localhost:8080/metrics?token=YOUR_ADMIN_TOKEN | Admin token |

---

## 📁 WHERE ARE ALL THE FILES?

**All in:** `c:\Semptify\Semptify\`

```
Startup Scripts:
  start_production.py ..................... MAIN ONE
  Start-Production.ps1 ................... Windows alt
  start_production.sh .................... Linux alt
  start.bat ............................ Windows alt

Documentation:
  COPILOT_SESSION_CONTEXT_MASTER.md ..... THIS MASTER FILE
  00_START_HERE.md ...................... Read first
  QUICK_START.md ........................ 5-min guide
  PRODUCTION_STARTUP.md ................. Full guide

Website:
  templates/full_site.html .............. Website code

Config:
  config.env.template ................... All options explained
```

---

## ✅ AFTER PC RESTART - FOLLOW THIS

1. **Open terminal:** `powershell` (Windows) or `bash` (Linux/macOS)
2. **Navigate:** `cd c:\Semptify\Semptify`
3. **Activate venv:** `.\.venv\Scripts\Activate.ps1` (Windows)
4. **Set secret:** `$env:FLASK_SECRET = "YOUR_KEY_FROM_BEFORE"`
5. **Start:** `python start_production.py`
6. **Access:** http://localhost:8080

---

## 🚨 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | `pip install -r requirements.txt` |
| `FLASK_SECRET not set` | `$env:FLASK_SECRET = $(python -c "import secrets; print(secrets.token_hex(32))")` |
| `Address already in use` | Change port: `set PORT=8081` then run |
| `Permission denied` on `.sh` file | `chmod +x start_production.sh` |
| Admin token not working | Verify token in `security/admin_tokens.json` |
| Server won't start | Check `logs/production.log` for errors |
| Port 8080 blocked | Use different: `$env:PORT = 8081` |

---

## 💾 ALL DOCUMENTATION LOCATIONS

```
Main Entry Points:
  00_START_HERE.md ...................... ⭐ READ THIS FIRST
  QUICK_START.md ........................ ⚡ 5 minutes
  COPILOT_SESSION_CONTEXT_MASTER.md .... 📋 Everything

Detailed Guides:
  PRODUCTION_STARTUP.md ................. 📖 Full details
  DEPLOYMENT_CI_CD.md ................... 🚀 Deploy anywhere
  config.env.template ................... ⚙️ All options

Current Status:
  INSTALLATION_COMPLETE.md .............. ✅ Checklist
  STARTUP_SUMMARY.md .................... 📊 Features
  STARTUP_README.md ..................... 📑 Index
```

---

## 🎓 WHAT EACH STARTUP SCRIPT DOES

### `start_production.py` (RECOMMENDED)
- ✅ Works on Windows, Linux, macOS
- ✅ No dependencies except Python
- ✅ Best error reporting
- ✅ Automatic startup validation
- ✅ **USE THIS ONE**

### `Start-Production.ps1`
- Windows only
- PowerShell advanced features
- Colored output
- Parameter support: `-Port 8080 -Environment production`

### `start_production.sh`
- Linux/macOS only
- POSIX compatible
- Identical features to PowerShell

### `start.bat`
- Windows only
- Double-click to run
- Simple/minimal setup

---

## 📊 TOKEN TYPES - WHAT'S WHAT

```
FLASK_SECRET
  ├─ What: Session encryption key
  ├─ Generated: python -c "import secrets; print(secrets.token_hex(32))"
  ├─ Used For: Server startup (set before running)
  ├─ Where: Environment variable $env:FLASK_SECRET
  └─ NOT for: Authentication/login

ADMIN_TOKEN
  ├─ What: Admin panel access
  ├─ Generated: python -c "from security import save_admin_token; print(save_admin_token()[1])"
  ├─ Used For: /admin routes, release management, metrics
  ├─ Where: URL: ?token=VALUE or header: X-Admin-Token
  └─ Access: /admin, /release_now, /metrics, /info

USER_TOKEN
  ├─ What: Document vault access
  ├─ Generated: Visit /register OR python -c "from security import save_user_token; print(save_user_token()[1])"
  ├─ Used For: /vault route, document storage
  ├─ Where: URL: ?user_token=VALUE
  └─ Access: /vault (personal documents only)
```

---

## 🎯 COMMON COMMANDS YOU'LL USE

```powershell
# Generate Flask Secret Key
python -c "import secrets; print(secrets.token_hex(32))"

# Generate Admin Token
python -c "from security import save_admin_token; aid,tok=save_admin_token(); print(tok)"

# Generate User Token
python -c "from security import save_user_token; uid,tok=save_user_token(); print(tok)"

# Set Flask Secret (Windows)
$env:FLASK_SECRET = "your-key-here"

# Set Flask Secret (Linux/macOS)
export FLASK_SECRET="your-key-here"

# Start server
python start_production.py

# Stop server
# Press Ctrl+C (graceful shutdown)

# Check server status
curl http://localhost:8080/health

# View production log
Get-Content logs/production.log -Tail 20

# View events log
Get-Content logs/events.log -Tail 20
```

---

## 📞 FIND DOCUMENTATION BY NEED

| I Need To... | Read This File |
|-------------|----------------|
| Get started in 5 minutes | `QUICK_START.md` |
| Understand everything | `PRODUCTION_STARTUP.md` |
| Deploy to Docker/K8s | `DEPLOYMENT_CI_CD.md` |
| Deploy to AWS/Azure | `DEPLOYMENT_CI_CD.md` |
| Configure all options | `config.env.template` |
| Set up on Windows | `QUICK_START.md` + `PRODUCTION_STARTUP.md` |
| Set up on Linux | `QUICK_START.md` + `start_production.sh` |
| Troubleshoot issues | `PRODUCTION_STARTUP.md` (Troubleshooting section) |
| Find everything | `COPILOT_SESSION_CONTEXT_MASTER.md` (this master) |

---

## 🔄 RESTART PROCEDURE (AFTER PC REBOOT)

**Step 1:** Open PowerShell
```powershell
cd c:\Semptify\Semptify
```

**Step 2:** Activate virtual environment
```powershell
.\.venv\Scripts\Activate.ps1
```

**Step 3:** Set Flask Secret
```powershell
$env:FLASK_SECRET = "your-saved-secret-key"
```

**Step 4:** Start server
```powershell
python start_production.py
```

**Step 5:** Access in browser
```
http://localhost:8080
```

---

## 🎉 YOU'RE ALL SET!

Everything created in this session is:
- ✅ Saved in: `c:\Semptify\Semptify\`
- ✅ Documented in: This file + 8 guides
- ✅ Ready to use: Just run `python start_production.py`
- ✅ Production-ready: Use in professional environments
- ✅ Cross-platform: Windows, Linux, macOS

**Bookmark this file and reference it after each PC restart!**

---

*Created by GitHub Copilot - November 4, 2025*  
*All work preserved and ready for production use*
