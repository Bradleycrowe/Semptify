# 🚀 Semptify Production Server Startup System

## Overview

Complete production-ready web server startup solution with automatic dependency management, validation, and configuration. Supports Windows, Linux, and macOS with comprehensive documentation.

---

## 📂 Files Included

### **Launcher Scripts** (Pick one for your OS)

| File | OS | Format | Usage |
|------|-----|--------|-------|
| `start.bat` | Windows | Batch | Double-click to start |
| `Start-Production.ps1` | Windows | PowerShell | `.\Start-Production.ps1` |
| `start_production.sh` | Linux/macOS | Bash | `./start_production.sh` |
| `start_production.py` | All | Python | `python start_production.py` |

### **Documentation** (Read these)

| File | Purpose | Length |
|------|---------|--------|
| `STARTUP_SUMMARY.md` | Overview & quick reference | 1 page |
| `QUICK_START.md` | Fast setup guide | 1 page |
| `PRODUCTION_STARTUP.md` | Complete documentation | 5 pages |
| `config.env.template` | Configuration reference | Reference |

---

## ⚡ Fastest Start (Choose Your Platform)

### **Windows - Double Click**
```
1. set FLASK_SECRET=your-secret-key-here
2. Double-click start.bat
3. Server runs at http://localhost:8080
```

### **Windows - PowerShell**
```powershell
$env:FLASK_SECRET = "your-secret-key-here"
.\Start-Production.ps1
```

### **Linux/macOS - Terminal**
```bash
export FLASK_SECRET="your-secret-key-here"
chmod +x start_production.sh
./start_production.sh
```

### **Any OS - Python**
```bash
export FLASK_SECRET="your-secret-key-here"
python start_production.py
```

---

## ✨ What Happens on Startup

```
✓ Python 3.8+ check
✓ Virtual environment setup
✓ Dependencies installation
✓ Required directories creation
✓ Environment validation
✓ Database connectivity check
✓ Logging initialization
✓ Server startup
```

---

## 🎯 Key Features

✅ **Automatic Setup**
- Detects and creates missing components
- Installs dependencies automatically
- Creates required directories

✅ **Production Ready**
- Waitress WSGI server
- Request tracking
- Comprehensive logging
- Signal handling for graceful shutdown

✅ **Cross-Platform**
- Native scripts for Windows, Linux, macOS
- Python fallback for any platform
- Environment detection

✅ **Configurable**
- 30+ configuration options
- Environment variable support
- Per-platform customization

✅ **Well Documented**
- Multiple guide levels (quick, standard, detailed)
- Troubleshooting sections
- Configuration examples

---

## 📋 Configuration

### **Required**
```bash
export FLASK_SECRET="your-secret-key-here"
```

### **Common**
```bash
export SEMPTIFY_PORT=8080           # Change port
export SEMPTIFY_HOST=127.0.0.1      # Local only
export SEMPTIFY_THREADS=8           # More performance
export SECURITY_MODE=enforced       # Enable security
```

### **Optional**
```bash
export AI_PROVIDER=openai           # AI integration
export OPENAI_API_KEY=key           # AI keys
export GITHUB_TOKEN=token           # GitHub integration
```

See `config.env.template` for all options.

---

## 📊 Startup Information

When server starts, you'll see:

```
===========================================================
 SEMPTIFY PRODUCTION STARTUP
===========================================================
ℹ Checking Python installation...
✓ Python found: Python 3.11.0

ℹ Checking virtual environment...
✓ Virtual environment found

ℹ Checking dependencies...
✓ Package installed: flask
✓ Package installed: waitress

ℹ Checking required directories...
✓ Directory exists: uploads
✓ Directory exists: logs

===========================================================
 STARTING WEB SERVER
===========================================================
Host: 0.0.0.0
Port: 8080
Threads: 4
Environment: production

🚀 Server starting at http://0.0.0.0:8080
   Press Ctrl+C to stop
```

---

## 🔍 Monitoring & Testing

```bash
# Test server is running
curl http://localhost:8080/

# Health check
curl http://localhost:8080/health

# View metrics
curl http://localhost:8080/metrics

# Check logs (Linux/macOS)
tail -f logs/production.log

# Check logs (Windows PowerShell)
Get-Content logs/production.log -Wait
```

---

## 🛑 Stopping Server

- **Keyboard**: Press `Ctrl+C` in terminal
- **Graceful**: Server completes in-flight requests before stopping
- **Force stop**: `Ctrl+C` twice

---

## 🐛 Troubleshooting

### Server won't start
1. Check `logs/production.log` for errors
2. Verify `FLASK_SECRET` is set: `echo $FLASK_SECRET`
3. Test Python: `python --version`
4. Try direct Python: `python start_production.py`

### Port already in use
```bash
export SEMPTIFY_PORT=9000
# Run server normally
```

### Permission denied (Linux/macOS)
```bash
chmod +x start_production.sh
./start_production.sh
```

### Virtual environment issues
```bash
# Manual activation
source .venv/bin/activate        # Linux/macOS
.\.venv\Scripts\Activate.ps1     # Windows

# Then run
python start_production.py
```

See `PRODUCTION_STARTUP.md` for more troubleshooting.

---

## 📚 Documentation Levels

### **🏃 Super Quick (30 seconds)**
See "Fastest Start" section above

### **📖 Quick Start (5 minutes)**
Read: `QUICK_START.md`
- Copy-paste commands
- Common configurations
- Quick troubleshooting

### **📖 Complete Guide (15 minutes)**
Read: `PRODUCTION_STARTUP.md`
- Environment variables reference
- All configuration options
- Deployment options
- Performance tuning
- Advanced troubleshooting

### **📋 Reference**
Use: `config.env.template`
- Every configuration option
- Default values
- Example configurations

---

## 🔐 Security Checklist

- [ ] Generated strong `FLASK_SECRET`
- [ ] Set `SECURITY_MODE=enforced`
- [ ] Enabled HTTPS if needed
- [ ] Configured firewall rules
- [ ] Set up log rotation
- [ ] Regular secret rotation schedule
- [ ] Monitoring/alerting in place

---

## 🚀 Deployment Options

From `PRODUCTION_STARTUP.md`:

1. **systemd** (Linux) - Production standard
2. **Windows Service** - NSSM or native
3. **Docker** - Container deployment
4. **Cloud** - Render, Heroku, AWS, Azure
5. **Direct** - Manual execution with process manager

See detailed instructions in `PRODUCTION_STARTUP.md`.

---

## 📊 Generated Structure

Server creates and uses:

```
Semptify/
├── logs/
│   ├── production.log          ← Server logs
│   ├── init.log               ← Startup log
│   └── events.log             ← Event log
├── uploads/                   ← User uploads
├── security/                  ← Security config
├── copilot_sync/             ← Copilot data
├── final_notices/            ← Generated docs
└── data/                      ← Application data
```

---

## 💡 Pro Tips

**Tip 1**: Save secret in file for easy setup
```bash
# Save to file (add to .gitignore)
echo "export FLASK_SECRET='your-secret'" > .env.local
source .env.local
./start_production.sh
```

**Tip 2**: Use screen/tmux to keep server running
```bash
screen -S semptify
export FLASK_SECRET="key"
python start_production.py

# Detach: Ctrl+A then D
# Reattach: screen -r semptify
```

**Tip 3**: Monitor with system tools
```bash
watch -n 1 'curl -s http://localhost:8080/health | jq'
```

**Tip 4**: Custom port for testing
```bash
export SEMPTIFY_PORT=9000
./Start-Production.ps1  # Or appropriate script
```

---

## 📞 Support

**For issues:**
1. Check `logs/production.log`
2. Read troubleshooting in `PRODUCTION_STARTUP.md`
3. Verify environment: `echo $FLASK_SECRET`
4. Test connectivity: `curl http://localhost:8080`

**For detailed help:**
- See `PRODUCTION_STARTUP.md` - Comprehensive guide
- See `QUICK_START.md` - Quick reference
- Check `config.env.template` - All options

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| **Generate secret** | `python -c "import secrets; print(secrets.token_hex(32))"` |
| **Set secret (PowerShell)** | `$env:FLASK_SECRET = "key"` |
| **Set secret (Bash)** | `export FLASK_SECRET="key"` |
| **Start (Windows batch)** | `start.bat` |
| **Start (PowerShell)** | `.\Start-Production.ps1` |
| **Start (Bash)** | `./start_production.sh` |
| **Start (Python)** | `python start_production.py` |
| **View logs** | `tail -f logs/production.log` |
| **Stop server** | `Ctrl+C` |
| **Test server** | `curl http://localhost:8080` |

---

## ✅ Verification Checklist

- [ ] All startup files are present
- [ ] Documentation is readable
- [ ] Generated a test `FLASK_SECRET`
- [ ] Can execute startup script for your OS
- [ ] Server starts and responds to requests
- [ ] Can access `http://localhost:8080`
- [ ] Logs appear in `logs/production.log`
- [ ] Can stop server gracefully with `Ctrl+C`

---

## 📝 Version Info

**Created**: November 4, 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready

---

## 🎓 Next Steps

1. **Start Server**: Follow "Fastest Start" section
2. **Test Access**: Visit `http://localhost:8080`
3. **Review Logs**: Check `logs/production.log`
4. **Configure**: Customize with environment variables
5. **Deploy**: Choose deployment method from `PRODUCTION_STARTUP.md`
6. **Monitor**: Set up health checks and alerting

---

**Ready to launch? Choose your platform above and get started in 30 seconds!** 🚀
