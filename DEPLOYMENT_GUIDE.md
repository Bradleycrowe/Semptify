# Semptify Deployment Guide

## Overview
Semptify is configured for automatic deployment to Render.com via GitHub Actions. This guide covers deployment methods, configuration, and troubleshooting.

## Deployment Methods

### 1. Automatic Deployment (Recommended)
Every push to the `main` branch automatically triggers a deployment.

**Process:**
1. Merge your PR to `main` or push directly to `main`
2. GitHub Actions workflow `.github/workflows/deploy.yml` triggers automatically
3. Workflow triggers Render deployment via API
4. Render builds Docker image from `Dockerfile`
5. Render deploys new version
6. Smoke tests run automatically (health check + readyz)

**Timeline:** ~3-5 minutes for typical deployments

### 2. Manual Deployment via GitHub Actions
Trigger a deployment without pushing code:

1. Go to: https://github.com/Bradleycrowe/Semptify/actions/workflows/deploy.yml
2. Click "Run workflow"
3. Select branch: `main`
4. Optionally check "Skip smoke test"
5. Click "Run workflow"

### 3. Manual Deployment via Render Dashboard
1. Go to: https://dashboard.render.com
2. Select the Semptify service
3. Click "Manual Deploy"
4. Select "Deploy latest commit" or specific commit
5. Click "Deploy"

### 4. Manual Deployment via Render API
```bash
curl -X POST \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys \
  -d '{"clearCache":false}'
```

## Configuration

### Required GitHub Secrets
Configure these in repository settings → Secrets and variables → Actions:

| Secret | Description | Required |
|--------|-------------|----------|
| `RENDER_API_KEY` | Render API key for deployments | Yes |
| `RENDER_SERVICE_ID` | Render service ID | Yes |
| `RENDER_BASE_URL` | Base URL for smoke tests (optional) | No |

### Render Environment Variables
Configure these in Render Dashboard → Service → Environment:

#### Required
- `FLASK_SECRET` - Flask session secret (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

#### Recommended
- `SECURITY_MODE=enforced` - Enable security features
- `ADMIN_TOKEN` - Admin access token
- `FORCE_HTTPS=1` - Force HTTPS redirects
- `ACCESS_LOG_JSON=1` - JSON access logs

#### Optional AI Configuration
- `AI_PROVIDER=openai` - AI provider (openai, azure, ollama)
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_BASE_URL` - Custom OpenAI endpoint
- `OPENAI_MODEL` - Model name

See `render.yaml` for complete environment variable reference.

## Deployment Workflow Details

### GitHub Actions Workflow
**File:** `.github/workflows/deploy.yml`

**Steps:**
1. **Verify secrets** - Ensures required secrets are configured
2. **Trigger deploy** - Calls Render API to start deployment
3. **Poll status** - Monitors deployment progress (max 15 minutes)
4. **Smoke test** - Validates `/health` and `/readyz` endpoints
5. **Summary** - Reports deployment duration and phase history

**Outputs:**
- Phase history artifact (shows deployment progression)
- Duration metrics
- Deployment summary in GitHub Actions UI

## Monitoring Deployment

### Via GitHub Actions
1. Go to: https://github.com/Bradleycrowe/Semptify/actions
2. Select the deploy workflow run
3. View "Summary" for deployment details
4. Download "phase-history" artifact for detailed timing

### Via Render Dashboard
1. Go to: https://dashboard.render.com
2. Select Semptify service
3. View "Events" tab for deployment log
4. View "Logs" tab for application logs

## Build Process

### Multi-Stage Docker Build
**File:** `Dockerfile`

**Stage 1 - Builder:**
- Base: `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Copies source code

**Stage 2 - Runtime:**
- Base: `python:3.11-slim`
- Copies dependencies from builder (faster, smaller)
- Removes tests and cache files
- Removes committed token files (security)
- Exposes port 8080
- Starts with `python ./run_prod.py`

**Build arguments:**
- `GIT_SHA` - Git commit SHA
- `BUILD_TIME` - Build timestamp
- `CACHE_BUST` - Force rebuild (update as needed)

## Smoke Tests

The deployment workflow includes optional smoke tests:

```bash
# Health check
curl -fsS https://semptify.onrender.com/health

# Readiness check
curl -fsS https://semptify.onrender.com/readyz
```

**Response for healthy service:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-11T14:27:00Z"
}
```

## Troubleshooting

### Deployment Fails at Build Stage
**Symptoms:** Build logs show dependency installation errors

**Solutions:**
1. Check `requirements.txt` for version conflicts
2. Clear cache: Manual Deploy → check "Clear build cache"
3. Verify Python 3.11 compatibility

### Deployment Stuck in "Building" Phase
**Symptoms:** Phase doesn't progress for >10 minutes

**Solutions:**
1. Check Render status page: https://status.render.com
2. Review build logs in Render Dashboard
3. Cancel and retry deployment

### Smoke Tests Fail
**Symptoms:** `/health` or `/readyz` returns errors

**Solutions:**
1. Check application logs in Render Dashboard
2. Verify `FLASK_SECRET` is set
3. Check security settings (`SECURITY_MODE`)
4. Verify all required directories are created

### 429 Rate Limit Errors
**Symptoms:** Admin endpoints return 429

**Solutions:**
1. Adjust rate limits via environment variables:
   - `ADMIN_RATE_WINDOW=60` (seconds)
   - `ADMIN_RATE_MAX=60` (requests per window)
2. Check for automated tools hitting endpoints

### Missing Environment Variables
**Symptoms:** Application starts but features don't work

**Solutions:**
1. Review Render Dashboard → Environment
2. Compare with `render.yaml` and `.env.example`
3. Verify secrets are not empty

## Post-Deployment Verification

### Manual Verification Steps
1. **Health Check:**
   ```bash
   curl https://semptify.onrender.com/health
   ```

2. **Readiness Check:**
   ```bash
   curl https://semptify.onrender.com/readyz
   ```

3. **Metrics Endpoint:**
   ```bash
   curl https://semptify.onrender.com/metrics
   ```

4. **Homepage:**
   ```bash
   curl -I https://semptify.onrender.com/
   ```

### Expected Responses
- All health endpoints should return 200 OK
- Metrics should include `requests_total` and `uptime_seconds`
- Homepage should return 200 OK with HTML

## Rollback Procedure

### Via Render Dashboard
1. Go to Render Dashboard → Semptify service
2. Click "Events" tab
3. Find previous successful deployment
4. Click "Redeploy" on that deployment

### Via GitHub
1. Revert the commit that caused issues
2. Push to `main` (triggers auto-deployment)

Or manually trigger workflow with earlier commit:
1. Checkout earlier commit: `git checkout <commit-sha>`
2. Push to trigger deployment

## Security Considerations

### Secrets Management
- Never commit secrets to the repository
- Rotate `FLASK_SECRET` and `ADMIN_TOKEN` periodically
- Use Render's environment variables (encrypted at rest)

### Token Files
- `security/admin_tokens.json` is removed during build
- Tokens are bootstrapped from `ADMIN_TOKEN` env var
- Break-glass procedure available for emergency access

### HTTPS
- Always use `FORCE_HTTPS=1` in production
- HSTS headers configured via environment variables
- Certificate managed by Render

## Performance Tuning

### Waitress Server Settings
Configured in `run_prod.py`:
- Threads: `SEMPTIFY_THREADS` (default: 8)
- Backlog: `SEMPTIFY_BACKLOG` (default: 1024)
- Host: `SEMPTIFY_HOST` (default: 0.0.0.0)
- Port: `SEMPTIFY_PORT` or `PORT` (default: 8080)

### Render Service Settings
Configure in Render Dashboard:
- Instance type: Free / Starter / Standard
- Auto-scaling: Configure min/max instances
- Health check path: `/health`
- Health check interval: 30 seconds

## Support & Resources

### Documentation
- Main README: `README.md`
- Startup guide: `00_START_HERE.md`
- Production startup: `PRODUCTION_STARTUP.md`
- Config reference: `CONFIG_REFERENCE.md`

### Monitoring
- GitHub Actions: Workflow runs and artifacts
- Render Dashboard: Deployment events and logs
- Application logs: `/logs/` directory (in container)

### Getting Help
1. Check deployment workflow logs
2. Review Render service logs
3. Verify environment variables
4. Test endpoints manually
5. Check GitHub Issues for similar problems

## Quick Reference

### Deploy to Production
```bash
# Trigger via git push
git push origin main

# Or trigger manually via GitHub Actions UI
# https://github.com/Bradleycrowe/Semptify/actions/workflows/deploy.yml
```

### Check Deployment Status
```bash
# Via curl
curl https://semptify.onrender.com/health

# Via GitHub Actions
# Check: https://github.com/Bradleycrowe/Semptify/actions
```

### View Logs
```bash
# Via Render CLI (if installed)
render logs -s <service-name>

# Via Render Dashboard
# https://dashboard.render.com → Service → Logs
```

---

**Last Updated:** November 2025  
**Deployment Platform:** Render.com  
**Repository:** https://github.com/Bradleycrowe/Semptify
