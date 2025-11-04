# Semptify Production Server Startup Guide

## Overview

This guide explains how to start the Semptify Flask application in production mode using the provided startup scripts. The setup includes automatic dependency checks, directory validation, and proper environment configuration.

## Files Created

### 1. **start_production.py** (Python)
- Main production server launcher
- Performs startup checks (directories, environment, database)
- Uses Waitress WSGI server for production
- Includes signal handlers for graceful shutdown
- Comprehensive logging to console and file

### 2. **Start-Production.ps1** (PowerShell - Windows)
- Windows-native startup script
- Activates Python virtual environment
- Checks and installs dependencies
- Colorized console output
- Handles all platform-specific requirements

### 3. **start_production.sh** (Bash - Linux/macOS)
- Unix/Linux startup script
- Similar functionality to PowerShell version
- POSIX-compliant
- Signal trap handling for clean shutdown

---

## Quick Start

### Windows (PowerShell)

```powershell
# Navigate to Semptify directory
cd c:\Semptify\Semptify

# Run startup script (requires PowerShell execution policy)
.\Start-Production.ps1

# Or with custom parameters
.\Start-Production.ps1 -Port 9000 -Host localhost -Threads 8
```

### Linux/macOS (Bash)

```bash
# Navigate to Semptify directory
cd /path/to/Semptify

# Make script executable
chmod +x start_production.sh

# Run startup script
./start_production.sh

# Or with custom environment variables
SEMPTIFY_PORT=9000 ./start_production.sh
```

### Direct Python

```bash
# Activate virtual environment first (Windows)
.\.venv\Scripts\Activate.ps1

# Or (Linux/macOS)
source .venv/bin/activate

# Then run
python start_production.py
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_SECRET` | Secret key for Flask sessions | `your-secret-key-here` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SEMPTIFY_PORT` | `8080` | Port to listen on |
| `SEMPTIFY_HOST` | `0.0.0.0` | Host address (0.0.0.0 = all interfaces) |
| `SEMPTIFY_THREADS` | `4` | Number of worker threads |
| `SEMPTIFY_WORKERS` | `1` | Number of worker processes |
| `SECURITY_MODE` | `enforced` | Security mode: `open` or `enforced` |
| `FLASK_ENV` | `production` | Flask environment |
| `FORCE_HTTPS` | not set | Set to force HTTPS scheme |
| `AI_PROVIDER` | not set | AI provider: `openai`, `azure`, `ollama` |
| `MAX_REQUEST_BODY_SIZE` | `16777216` | Max request body in bytes (16MB) |
| `SHUTDOWN_TIMEOUT` | `30` | Graceful shutdown timeout in seconds |
| `ACCESS_LOG_JSON` | not set | Set to `1` for JSON access logs |

### Setting Environment Variables

**Windows (PowerShell):**
```powershell
$env:FLASK_SECRET = "your-secret-key"
$env:SEMPTIFY_PORT = "9000"
$env:SECURITY_MODE = "enforced"
```

**Linux/macOS (Bash):**
```bash
export FLASK_SECRET="your-secret-key"
export SEMPTIFY_PORT="9000"
export SECURITY_MODE="enforced"
```

**Or create a `.env` file** (if using python-dotenv):
```
FLASK_SECRET=your-secret-key
SEMPTIFY_PORT=9000
SECURITY_MODE=enforced
```

---

## Startup Checks

The startup process automatically verifies:

✓ **Python Installation** - Checks if Python 3.8+ is installed
✓ **Virtual Environment** - Creates if missing, activates automatically
✓ **Dependencies** - Verifies Flask, Waitress, requests are installed
✓ **Directories** - Creates required directories:
  - `uploads/` - File uploads
  - `logs/` - Application logs
  - `security/` - Security tokens and config
  - `copilot_sync/` - Copilot synchronization
  - `final_notices/` - Generated notices
  - `data/` - Application data
✓ **Environment** - Validates required variables
✓ **Database** - Checks database connectivity
✓ **Logging** - Sets up file and console logging

---

## Logging

Logs are saved to:
- **Console**: Real-time output in terminal
- **File**: `logs/production.log` for persistent records

Log format includes timestamp, module, level, and message:
```
2025-11-04 10:30:45,123 - __main__ - INFO - ✓ Directory exists: uploads
```

---

## Graceful Shutdown

The server responds to signals for clean shutdown:

- **Ctrl+C** (SIGINT) - Initiates graceful shutdown
- **kill -TERM** (SIGTERM) - Initiates graceful shutdown

All active connections are allowed to complete within the shutdown timeout (default: 30 seconds).

---

## Configuration Examples

### Development Server (localhost, high debugging)
```bash
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:SEMPTIFY_PORT = "5000"
$env:SEMPTIFY_HOST = "127.0.0.1"
python start_production.py
```

### Production Server (all interfaces, 8 threads)
```bash
$env:FLASK_ENV = "production"
$env:SEMPTIFY_PORT = "8080"
$env:SEMPTIFY_THREADS = "8"
$env:SECURITY_MODE = "enforced"
python start_production.py
```

### High-Performance Server
```bash
export FLASK_ENV=production
export SEMPTIFY_PORT=8080
export SEMPTIFY_THREADS=16
export SEMPTIFY_WORKERS=4
export MAX_REQUEST_BODY_SIZE=33554432  # 32MB
./start_production.sh
```

---

## Deployment Options

### 1. **Direct Execution**
```bash
python start_production.py &
```

### 2. **systemd (Linux)**
Create `/etc/systemd/system/semptify.service`:
```ini
[Unit]
Description=Semptify Production Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/semptify
Environment="PATH=/var/www/semptify/.venv/bin"
Environment="FLASK_ENV=production"
Environment="FLASK_SECRET=<your-secret>"
ExecStart=/usr/bin/python3 start_production.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable semptify
sudo systemctl start semptify
sudo systemctl status semptify
```

### 3. **Windows Service (NSSM)**
```bash
# Install
nssm install Semptify "C:\Python39\python.exe" "c:\Semptify\Semptify\start_production.py"
nssm set Semptify AppDirectory "c:\Semptify\Semptify"
nssm set Semptify AppEnvironmentExtra FLASK_ENV=production
nssm set Semptify AppEnvironmentExtra FLASK_SECRET=your-secret

# Start
nssm start Semptify

# Status
nssm status Semptify

# Stop
nssm stop Semptify
```

### 4. **Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
CMD ["python", "start_production.py"]
```

---

## Troubleshooting

### Python Not Found
```
✗ Python not found. Please install Python 3.8+
```
**Solution**: Install Python from python.org

### Virtual Environment Errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Ensure venv is activated:
- Windows: `.\.venv\Scripts\Activate.ps1`
- Linux: `source .venv/bin/activate`

### Port Already in Use
```
Address already in use
```
**Solution**: Use a different port:
```bash
$env:SEMPTIFY_PORT = 9000
python start_production.py
```

### Permission Denied (Linux)
```
Permission denied: './start_production.sh'
```
**Solution**: Make script executable:
```bash
chmod +x start_production.sh
```

### Missing FLASK_SECRET
```
⚠ Missing environment variable: FLASK_SECRET
```
**Solution**: Set before running:
```bash
$env:FLASK_SECRET = "your-secret-key-here"
```

---

## Performance Tuning

### For High Traffic

```bash
# Increase threads and workers
export SEMPTIFY_THREADS=16
export SEMPTIFY_WORKERS=4
export MAX_REQUEST_BODY_SIZE=33554432  # 32MB
python start_production.py
```

### For Low-Resource Systems

```bash
# Reduce threads and workers
export SEMPTIFY_THREADS=2
export SEMPTIFY_WORKERS=1
python start_production.py
```

### Monitor Resource Usage

**Linux**:
```bash
# Watch CPU and memory
watch -n 1 'ps aux | grep python'
```

**Windows**:
```powershell
# Monitor process
Get-Process python | Select-Object Name,CPU,Memory
```

---

## Health Checks

The server provides health endpoints (if configured in Semptify.py):

```bash
# Basic health check
curl http://localhost:8080/health

# Readiness check
curl http://localhost:8080/readyz

# Metrics
curl http://localhost:8080/metrics
```

---

## Next Steps

1. **Configure Environment**: Set `FLASK_SECRET` and other variables
2. **Test Locally**: Run startup script to verify everything works
3. **Set Up Logging**: Monitor `logs/production.log`
4. **Deploy**: Choose a deployment option from above
5. **Monitor**: Use health checks and metrics endpoints

---

## Support & Troubleshooting

For issues or questions:
1. Check the logs: `logs/production.log`
2. Verify environment variables are set
3. Ensure all required directories exist
4. Check Python version compatibility
5. Verify firewall allows the configured port

---

**Last Updated**: November 4, 2025
**Version**: 1.0
