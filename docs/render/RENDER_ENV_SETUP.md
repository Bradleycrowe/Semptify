# Quick Render Environment Setup

## Required Environment Variables for Flask

Your Semptify app needs these environment variables set in Render:

### 1. FLASK_SECRET (REQUIRED)
Generate a secure secret:
```powershell
# Run this to generate a secure Flask secret
$secret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host "FLASK_SECRET=$secret" -ForegroundColor Green
```

### 2. ADMIN_TOKEN (REQUIRED)
Generate an admin token:
```powershell
# Run this to generate a secure admin token
$adminToken = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "ADMIN_TOKEN=$adminToken" -ForegroundColor Green
```

### 3. Set Variables in Render Dashboard

**Option A: Manual (Easiest)**
1. Go to https://dashboard.render.com
2. Click on your "Semptify" service
3. Click "EnviClick on your "Semptify" service
ronment" tab
4. Click "Add Environment Variable"
5. Add these one by one:

```
Key: FLASK_SECRET
Value: <paste the generated secret from above>

Key: ADMIN_TOKEN
Value: <paste the generated token from above>

Key: SECURITY_MODE
Value: enforced

Key: FORCE_HTTPS
Value: 1

Key: HSTS_MAX_AGE
Value: 31536000

Key: HSTS_PRELOAD
Value: 1

Key: ACCESS_LOG_JSON
Value: 1

Key: ADMIN_RATE_WINDOW
Value: 60

Key: ADMIN_RATE_MAX
Value: 60

Key: ADMIN_RATE_STATUS
Value: 429
```

6. Click "Save Changes" (Render will auto-redeploy)

---

**Option B: Using PowerShell Script (Advanced)**

If you want to use the automated script:

1. Get your Render API token:
   - Go to https://dashboard.render.com/account/api
   - Click "Create API Key"
   - Copy the token (starts with `rnd_`)

2. Run the script:
```powershell
# Set your Render API token (replace with your actual token)
$env:RENDER_API_TOKEN = Read-Host -Prompt "Paste your Render API token"

# Run the setup script
cd C:\Semptify\Semptify
.\scripts\render_setup.ps1
```

The script will:
- Find your Semptify service automatically
- Generate secure FLASK_SECRET and ADMIN_TOKEN
- Set all required environment variables
- Trigger a new deployment

---

## Quick Start (Recommended)

**Just run these 3 commands:**

```powershell
# 1. Generate FLASK_SECRET
$secret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host "`nFLASK_SECRET=$secret`n" -ForegroundColor Green

# 2. Generate ADMIN_TOKEN
$adminToken = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "ADMIN_TOKEN=$adminToken`n" -ForegroundColor Yellow

# 3. Show what to do next
Write-Host "Copy these values and add them in Render Dashboard:" -ForegroundColor Cyan
Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Click your Semptify service -> Environment tab" -ForegroundColor White
Write-Host "3. Add the two variables above" -ForegroundColor White
Write-Host "4. Add SECURITY_MODE=enforced and other settings" -ForegroundColor White
Write-Host "5. Click Save Changes" -ForegroundColor White
```

---

## What Each Variable Does

- **FLASK_SECRET**: Encrypts session cookies and CSRF tokens (REQUIRED)
- **ADMIN_TOKEN**: Access token for admin endpoints like /admin, /metrics (REQUIRED)
- **SECURITY_MODE**: `enforced` = production security, `open` = development only
- **FORCE_HTTPS**: Redirect HTTP to HTTPS
- **HSTS_MAX_AGE**: How long browsers should remember to use HTTPS
- **ACCESS_LOG_JSON**: Enable JSON-formatted access logs for monitoring

---

## After Setting Variables

Once you save environment variables in Render:
1. Render will automatically trigger a new deployment
2. Wait 2-3 minutes for the build to complete
3. Your app will restart with the new configuration
4. Visit https://semptify.onrender.com/ to verify it works

---

## Verify Configuration

After deployment, test these endpoints:

```powershell
# Health check (should return {"status": "ok"})
curl https://semptify.onrender.com/health

# Readiness check (should show configuration status)
curl https://semptify.onrender.com/readyz
```

---

## Troubleshooting

**App won't start?**
- Check Render logs for errors
- Verify FLASK_SECRET and ADMIN_TOKEN are set
- Make sure variables have no extra spaces

**Can't access admin pages?**
- Set SECURITY_MODE=open temporarily for testing
- Check ADMIN_TOKEN is correct
- Use the token in requests: `Authorization: Bearer <your-admin-token>`

**Need to reset?**
- Generate new secrets with the commands above
- Update in Render dashboard
- App will auto-redeploy
