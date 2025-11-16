# RENDER SERVICE CLEANUP GUIDE

## Current Situation
You have 3 services on Render:
1. **Semptify-0rlz (Ohio)** - KEEP THIS ONE ✓
   - Runtime: Docker
   - Status: Deployed 
   - Has latest code with maintenance engine
   - URL: https://semptify-0rlz.onrender.com

2. **Semptify (Oregon)** - DELETE
   - Runtime: Docker
   - Status: Deployed but outdated (1 day old)
   - Missing maintenance engine
   
3. **semptify-0rlz (Oregon)** - DELETE  
   - Runtime: Python 3 (wrong!)
   - Status: Failed deploy
   - Wrong configuration

## STEP-BY-STEP CLEANUP

### Step 1: Verify Ohio Service is Working
```powershell
# Test maintenance endpoint (may take 30s if cold start)
Invoke-RestMethod https://semptify-0rlz.onrender.com/maintenance/tasks

# Expected output: {"available_tasks": ["rotate_logs", "vacuum_db", ...]}
```

If you get timeout, wait 1 minute and try again - Render free tier cold starts.

### Step 2: Delete Failed Oregon Service
1. Go to: https://dashboard.render.com
2. Click on: **semptify-0rlz** (Oregon, Python 3, Failed)
3. Scroll down → Settings tab
4. Click: "Delete Service" button (red button at bottom)
5. Type service name to confirm: `semptify-0rlz`
6. Click: "Yes, delete this service"

### Step 3: Suspend Old Oregon Service
1. Go to: https://dashboard.render.com
2. Click on: **Semptify** (Oregon, 1 day old)
3. Scroll down → Settings tab
4. Click: "Suspend Service" (keeps config, stops billing)
   OR
   Click: "Delete Service" (permanent removal)

**Recommendation:** Suspend first, test Ohio for 24h, then delete Oregon permanently.

### Step 4: Configure Auto-Deploy on Ohio
1. Go to: https://dashboard.render.com
2. Click on: **Semptify-0rlz** (Ohio)
3. Go to: Settings tab
4. Find: "Build & Deploy" section
5. Set: Auto-Deploy: Yes
6. Branch: `clean-deploy`
7. Click: Save Changes

### Step 5: Update Environment Variables (if needed)
Check if Ohio service has all required env vars:
- FLASK_SECRET_KEY
- SECURITY_MODE (open or enforced)
- AI provider keys (OPENAI_API_KEY, AZURE_*, OLLAMA_BASE_URL)
- GITHUB_TOKEN (for release features)
- DATABASE_URL (if using external Postgres)

Copy from old Oregon service if needed:
1. Oregon service → Environment tab → Copy values
2. Ohio service → Environment tab → Paste values
3. Click: Save Changes (triggers redeploy)

## VERIFICATION CHECKLIST

After cleanup, verify Ohio service:

```powershell
$url = "https://semptify-0rlz.onrender.com"

# 1. Homepage loads
Invoke-WebRequest $url

# 2. Maintenance engine works
Invoke-RestMethod "$url/maintenance/tasks"

# 3. Improvement engine works  
Invoke-RestMethod "$url/improvement/proposals"

# 4. Readiness check passes
Invoke-RestMethod "$url/readyz"

# 5. Run full maintenance
Invoke-RestMethod -Method POST "$url/maintenance/run"
```

## DNS/CUSTOM DOMAIN (if applicable)

If you have custom domain pointing to old Oregon service:
1. Dashboard → Semptify-0rlz (Ohio) → Settings
2. Add custom domain
3. Update DNS records as shown
4. Wait for SSL certificate (5-10 minutes)

## MONITORING

After cleanup, monitor Ohio service:
- Dashboard → Semptify-0rlz → Logs (watch for errors)
- Look for: "[OK] Maintenance routes registered (/maintenance/*)"
- Check metrics: https://semptify-0rlz.onrender.com/metrics

## QUICK REFERENCE

**Primary Service:** Semptify-0rlz (Ohio)
**URL:** https://semptify-0rlz.onrender.com
**Branch:** clean-deploy
**Runtime:** Docker
**Region:** Ohio (us-east)

**Autonomous Endpoints:**
- POST /maintenance/run
- GET /maintenance/tasks
- GET /improvement/scan
- POST /seed/start

---
Generated: 2025-11-15
Next: Delete Oregon services, verify Ohio is stable
