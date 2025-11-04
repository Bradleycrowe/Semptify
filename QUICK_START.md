# Semptify Production Server - Quick Start Guide

## 🚀 Quick Start (Choose Your OS)

### Windows (PowerShell)
```powershell
# 1. Navigate to project
cd c:\Semptify\Semptify

# 2. Set secret key (REQUIRED)
$env:FLASK_SECRET = "your-secret-key-here"

# 3. Start server
.\Start-Production.ps1
```

### Linux/macOS (Bash)
```bash
# 1. Navigate to project
cd /path/to/Semptify

# 2. Set secret key (REQUIRED)
export FLASK_SECRET="your-secret-key-here"

# 3. Make script executable (first time only)
chmod +x start_production.sh

# 4. Start server
./start_production.sh
```

### Direct Python (Any OS)
```bash
# Activate virtual environment
# Windows: .\.venv\Scripts\Activate.ps1
# Linux/Mac: source .venv/bin/activate

# Set secret
export FLASK_SECRET="your-secret-key-here"

# Run
python start_production.py
```

---

## 📋 Essential Setup

### 1. Generate Secret Key
```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 2: OpenSSL
openssl rand -hex 32
```

### 2. Set Required Variables
```bash
# Windows PowerShell
$env:FLASK_SECRET = "your-generated-key"

# Linux/macOS Bash
export FLASK_SECRET="your-generated-key"
```

### 3. Start Server
See "Quick Start" section above for your OS.

---

## 🛠️ Common Configuration

### Run on Different Port
```bash
# Windows
$env:SEMPTIFY_PORT = 9000

# Linux/macOS
export SEMPTIFY_PORT=9000

# Then start normally
python start_production.py
```

### Run on Local Network Only
```bash
# Windows
$env:SEMPTIFY_HOST = "127.0.0.1"

# Linux/macOS
export SEMPTIFY_HOST="127.0.0.1"

python start_production.py
```

### Increase Performance
```bash
# Windows
$env:SEMPTIFY_THREADS = "8"

# Linux/macOS
export SEMPTIFY_THREADS=8

python start_production.py
```

---

## 🔐 Production Checklist

- [ ] Generated and set `FLASK_SECRET` to a strong random value
- [ ] Set `SECURITY_MODE=enforced` for production
- [ ] Created required directories (auto-created by script)
- [ ] Installed all dependencies from `requirements.txt`
- [ ] Tested server on local environment
- [ ] Configured firewall to allow port 8080 (or your chosen port)
- [ ] Set up log rotation for `logs/production.log`
- [ ] Configured HTTPS/SSL if needed
- [ ] Set up monitoring and alerting
- [ ] Tested graceful shutdown (Ctrl+C)

---

## 📊 Monitoring

### Check Server Status
```bash
# Test basic connectivity
curl http://localhost:8080/

# Check health endpoint
curl http://localhost:8080/health

# View metrics
curl http://localhost:8080/metrics
```

### View Logs
```bash
# Real-time logs (Linux/macOS)
tail -f logs/production.log

# Real-time logs (Windows PowerShell)
Get-Content -Path logs/production.log -Wait

# Last 100 lines
tail -n 100 logs/production.log
```

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `start_production.py` | Main server launcher (all platforms) |
| `Start-Production.ps1` | Windows PowerShell startup script |
| `start_production.sh` | Linux/macOS bash startup script |
| `config.env.template` | Configuration template (copy to `.env`) |
| `PRODUCTION_STARTUP.md` | Detailed documentation |

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change port
export SEMPTIFY_PORT=9000

# Or kill process using port (Linux/macOS)
lsof -i :8080
kill -9 <PID>
```

### Virtual Environment Not Activating
```bash
# Manually activate before running
# Windows
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

# Then run
python start_production.py
```

### Missing Dependencies
```bash
# Install from requirements
pip install -r requirements.txt

# Or install specific package
pip install flask waitress requests
```

### Permission Denied (Linux)
```bash
# Make script executable
chmod +x start_production.sh

# Run script
./start_production.sh
```

---

## 📚 Full Documentation

For detailed information, see `PRODUCTION_STARTUP.md`

Topics covered:
- Environment variables reference
- Startup checks explained
- Deployment options (systemd, Docker, Windows Service)
- Performance tuning
- Security best practices
- Advanced configuration

---

## 🚨 What Gets Created/Checked

The startup script automatically:

✅ Verifies Python 3.8+ installed
✅ Creates/activates virtual environment
✅ Installs required packages
✅ Creates required directories:
   - uploads/
   - logs/
   - security/
   - copilot_sync/
   - final_notices/
   - data/
✅ Validates environment variables
✅ Sets up logging
✅ Configures signal handlers for clean shutdown

---

## 🔄 Graceful Shutdown

The server properly handles shutdown signals:

```bash
# Press Ctrl+C to stop
# Or send signal from another terminal
kill -TERM <process_id>

# Server will:
# - Stop accepting new connections
# - Complete in-flight requests (30 sec timeout)
# - Clean up resources
# - Exit gracefully
```

---

## 🌐 Server URLs

Once running, access:

| URL | Purpose |
|-----|---------|
| `http://localhost:8080/` | Main application |
| `http://localhost:8080/health` | Health check |
| `http://localhost:8080/healthz` | Kubernetes health |
| `http://localhost:8080/readyz` | Readiness check |
| `http://localhost:8080/metrics` | Prometheus metrics |

---

## 💾 Database & Files

Server creates/uses these directories:

```
Semptify/
├── uploads/          # User file uploads
├── logs/             # Application logs
│   └── production.log
├── security/         # Security tokens & config
├── copilot_sync/     # Copilot sync data
├── final_notices/    # Generated notices
└── data/             # Application data
```

---

## 🎯 Next Steps

1. **Generate Secret**: Get a strong random key
2. **Set Environment**: Export `FLASK_SECRET`
3. **Start Server**: Run appropriate startup script for your OS
4. **Test**: Access `http://localhost:8080`
5. **Monitor**: Check logs in `logs/production.log`
6. **Deploy**: Follow deployment options in full docs

---

**Last Updated**: November 4, 2025
**Version**: 1.0
