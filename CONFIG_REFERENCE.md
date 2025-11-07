# Semptify Configuration Reference

Quick reference for environment variables and configuration settings.

## Port Configuration

**How it works:**
- Render automatically provides `PORT` environment variable (usually 10000)
- `run_prod.py` reads `PORT` with fallback to 8080 for local testing
- Docker EXPOSE is set to 8080 (documentation only, not enforcement)
- **Do NOT set** `SEMPTIFY_PORT` on Render - it conflicts with Render's `PORT`

**Local development:**
```bash
# Option 1: Use default
python Semptify.py  # runs on port 5000

# Option 2: Custom port
$env:PORT = 3000
python run_prod.py  # runs on port 3000
```

**Production (Render):**
- Render sets `PORT` automatically
- `run_prod.py` uses that value
- No manual port configuration needed

## Required Environment Variables (Production)

### Security (REQUIRED)
```bash
FLASK_SECRET=<random-64-char-hex>    # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
ADMIN_TOKEN=<random-32-char-hex>     # Generate with: python -c "import secrets; print(secrets.token_hex(16))"
SECURITY_MODE=enforced               # Use 'enforced' for production, 'open' for testing
```

### HTTPS & Headers (Recommended for Production)
```bash
FORCE_HTTPS=1                        # Redirect HTTP to HTTPS
HSTS_MAX_AGE=31536000               # HSTS max age (1 year)
HSTS_PRELOAD=1                      # Enable HSTS preload
```

### Rate Limiting (Recommended)
```bash
ADMIN_RATE_WINDOW=60                # Rate limit window in seconds
ADMIN_RATE_MAX=60                   # Max requests per window
ADMIN_RATE_STATUS=429               # HTTP status for rate limited requests
```

### Logging (Optional)
```bash
ACCESS_LOG_JSON=1                   # Enable JSON access logs
```

## AI Provider Configuration (Optional)

### OpenAI
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
```

### Azure OpenAI
```bash
AI_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Ollama (Local)
```bash
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

## Render Deployment

### Using the PowerShell Script (Recommended)
```powershell
# Set your Render API token (get from https://dashboard.render.com/account/api)
$env:RENDER_API_TOKEN = Read-Host -Prompt "Paste your Render API token"

# Run the setup script
.\scripts\render_setup.ps1
```

This script will:
1. Find your Semptify service
2. Set/update environment variables
3. Trigger a new deployment

### Manual Configuration via Render Dashboard
1. Go to https://dashboard.render.com
2. Select your Semptify service
3. Go to "Environment" tab
4. Add/update variables listed above
5. Click "Save Changes" - Render will auto-deploy

## Configuration Files

- `render.yaml` - Render service definition (env var templates, NO port override)
- `config.env.template` - Local development template (copy to `.env`)
- `run_prod.py` - Production server startup (handles PORT fallback)
- `Semptify.py` - Development server (hardcoded port 5000)
- `Dockerfile` - Multi-stage build, EXPOSE 8080 (documentation)

## Port Conflict Resolution (FIXED)

**Previous issue:** Multiple conflicting port configurations
- ❌ `render.yaml` had `SEMPTIFY_PORT=8080`
- ❌ PowerShell script set `SEMPTIFY_PORT=8080`
- ❌ Render also provides `PORT` variable
- ❌ `run_prod.py` tried to read both

**Current solution:**
- ✅ `render.yaml` does NOT set any port variable
- ✅ PowerShell script does NOT set port variable
- ✅ `run_prod.py` reads `PORT` (from Render) or defaults to 8080
- ✅ No conflicts, Render controls the port

## Quick Start Checklist

### First-time Setup
- [ ] Generate `FLASK_SECRET` and save securely
- [ ] Generate `ADMIN_TOKEN` and save securely
- [ ] Set both in Render environment variables
- [ ] Set `SECURITY_MODE=enforced`
- [ ] Enable HTTPS settings (`FORCE_HTTPS=1`, etc.)
- [ ] Configure rate limiting
- [ ] (Optional) Add AI provider keys

### Every Deploy
- [ ] Verify environment variables in Render dashboard
- [ ] Check build logs for errors
- [ ] Test health endpoints: `/health`, `/healthz`, `/readyz`
- [ ] Verify admin access with token
- [ ] Check metrics at `/metrics`

## Troubleshooting

### "Address already in use" locally
```powershell
# Find process using the port
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <pid> /F
```

### Render deployment fails
1. Check build logs in Render dashboard
2. Verify all required env vars are set
3. Check for import errors in logs
4. Ensure `requirements.txt` is up to date

### "Unauthorized" on admin endpoints
1. Verify `ADMIN_TOKEN` is set in Render
2. Check `SECURITY_MODE` is correct
3. Try break-glass procedure if needed (see security docs)

## Security Notes

- Never commit `.env` files or tokens to git
- Use different tokens for dev/staging/production
- Rotate tokens periodically
- Keep `SECURITY_MODE=enforced` in production
- Monitor `/metrics` for suspicious activity
- Check `/admin/status` regularly

## See Also

- `RENDER_QUICK_START.md` - Render deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deploy checklist
- `.github/copilot-instructions.md` - Project conventions
