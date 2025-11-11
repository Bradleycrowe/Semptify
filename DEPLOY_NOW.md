# Deploy Semptify Now - Quick Guide

## ✅ Pre-Deployment Checklist

- [x] Application code is working and tested
- [x] Dependencies in `requirements.txt` are up to date
- [x] `Dockerfile` builds successfully
- [x] Production server (`run_prod.py`) starts correctly
- [x] GitHub Actions workflow (`.github/workflows/deploy.yml`) is configured
- [x] Render configuration (`render.yaml`) is up to date

## 🚀 Deployment Options

### Option 1: Automatic Deployment (Recommended)
**When:** Merge PR or push directly to `main` branch

```bash
# Ensure you're on main branch
git checkout main

# Pull latest changes
git pull origin main

# Push changes (triggers auto-deploy)
git push origin main
```

The deployment will automatically:
1. Trigger GitHub Actions workflow
2. Call Render API to start deployment
3. Build Docker image on Render
4. Deploy new version
5. Run smoke tests
6. Report status

**Timeline:** 3-5 minutes

---

### Option 2: Manual Deployment via GitHub UI
**When:** Want to deploy without committing new code

1. Go to: https://github.com/Bradleycrowe/Semptify/actions/workflows/deploy.yml
2. Click the **"Run workflow"** button (top right)
3. Select branch: `main`
4. Optionally check "Skip smoke test" if needed
5. Click **"Run workflow"**

**Timeline:** 3-5 minutes

---

### Option 3: Manual Deployment via Render Dashboard
**When:** Need direct control or GitHub Actions unavailable

1. Go to: https://dashboard.render.com
2. Find and select **Semptify** service
3. Click **"Manual Deploy"** button
4. Select commit or choose "Deploy latest commit"
5. Click **"Deploy"**

**Timeline:** 3-5 minutes

---

### Option 4: API-Based Deployment (Advanced)
**When:** Automating deployments from scripts or CI/CD

```bash
# Set your Render credentials
export RENDER_API_KEY="your-api-key"
export RENDER_SERVICE_ID="your-service-id"

# Trigger deployment
curl -X POST \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys \
  -d '{"clearCache":false}'
```

---

## 🔍 Monitor Deployment

### Via GitHub Actions
1. Go to: https://github.com/Bradleycrowe/Semptify/actions
2. Click on the latest "Deploy" workflow run
3. Watch the live log output
4. Check the summary for deployment metrics

### Via Render Dashboard
1. Go to: https://dashboard.render.com
2. Select **Semptify** service
3. Click **"Events"** tab to see deployment progress
4. Click **"Logs"** tab to see application logs

---

## ✓ Verify Deployment

After deployment completes, verify it's working:

```bash
# Health check
curl https://semptify.onrender.com/health

# Readiness check
curl https://semptify.onrender.com/readyz

# Homepage
curl -I https://semptify.onrender.com/
```

**Expected:** All should return `200 OK`

---

## 🔧 Required Configuration

### GitHub Secrets (Must be set)
Go to: Repository → Settings → Secrets and variables → Actions

- `RENDER_API_KEY` - Your Render API key
- `RENDER_SERVICE_ID` - Your Render service ID
- `RENDER_BASE_URL` - (Optional) For smoke tests

### Render Environment Variables (Must be set)
Go to: Render Dashboard → Service → Environment

**Required:**
- `FLASK_SECRET` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

**Recommended:**
- `SECURITY_MODE=enforced`
- `ADMIN_TOKEN` - Admin access token
- `FORCE_HTTPS=1`
- `ACCESS_LOG_JSON=1`

---

## ⚠️ Troubleshooting

### Deployment Fails
1. Check GitHub Actions logs
2. Check Render service logs
3. Verify all secrets are set
4. Try "Clear build cache" in Render

### Smoke Tests Fail
1. Check `/health` endpoint manually
2. Verify `FLASK_SECRET` is set in Render
3. Check application logs for errors

### 429 Rate Limit
1. Adjust `ADMIN_RATE_MAX` and `ADMIN_RATE_WINDOW`
2. Check for automated scanners

---

## 🎯 Quick Deploy Command

If you just want to deploy the current main branch **right now**:

```bash
# Via GitHub CLI (if installed)
gh workflow run deploy.yml

# Or use the GitHub UI (fastest)
# https://github.com/Bradleycrowe/Semptify/actions/workflows/deploy.yml
# Click "Run workflow" → Run workflow
```

---

## 📚 Additional Documentation

- Full deployment guide: `DEPLOYMENT_GUIDE.md`
- Configuration reference: `CONFIG_REFERENCE.md`
- Production startup: `PRODUCTION_STARTUP.md`
- Main README: `README.md`

---

**Need Help?**
- Check deployment workflow logs
- Review Render service logs
- Verify environment variables
- See `DEPLOYMENT_GUIDE.md` for detailed troubleshooting
