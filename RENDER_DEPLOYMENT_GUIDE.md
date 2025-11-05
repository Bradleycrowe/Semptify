# 🚀 Render Deployment Guide for Semptify

## Quick Start (5 minutes)

### **Step 1: Prepare Your Repository**
Your repo is ready! The `render.yaml` file contains all deployment configuration.

### **Step 2: Connect to Render Dashboard**

1. Go to https://dashboard.render.com
2. Sign up or log in with your GitHub account
3. Click "New +" button
4. Select "Web Service"
5. Choose "Build and deploy from a Git repository"

### **Step 3: Connect Your GitHub Repository**

1. Click "Connect account" and authorize Render to access your GitHub repos
2. Search for and select: **Bradleycrowe/Semptify**
3. Select branch: **main** (or **copilot/vscode1762361470744** for testing)
4. Click "Connect"

### **Step 4: Configure the Service**

Render will auto-detect `render.yaml`. Review these settings:

- **Name:** Semptify
- **Runtime:** Docker ✓ (auto-detected)
- **Region:** Ohio (recommended for US)
- **Plan:** Free tier
- **Auto-deploy:** Enabled (deploys on every Git push)

### **Step 5: Add Environment Secrets**

Click "Add Environment Variable" and add:

```
FLASK_SECRET             → Generate random hex (use: python -c "import secrets; print(secrets.token_hex(32))")
ADMIN_TOKEN              → Your admin password
SECURITY_MODE            → enforced
OPENAI_API_KEY          → Your OpenAI key (if using)
GITHUB_TOKEN            → Your GitHub PAT (for releases)
```

**⚠️ IMPORTANT:** Set `sync: false` for these secrets in `render.yaml` so they don't auto-sync from Git!

### **Step 6: Deploy!**

1. Click "Create Web Service"
2. Render builds and deploys automatically
3. Wait 2-5 minutes for first deployment
4. Your app is live at `https://semptify-[random].onrender.com`

---

## Manual Deployment via Git Push

After connecting Render, it auto-deploys on every push to your branch:

```powershell
cd c:\repos git\UTAV\Semptify
git add .
git commit -m "feat: update features"
git push origin main
# Render automatically deploys!
```

---

## Environment Variables

### Required
| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_SECRET` | Session/CSRF token | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `SECURITY_MODE` | Security level | `enforced` or `open` |

### Optional (API Providers)
| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API access | `sk-...` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | `https://*.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key | API key |
| `GITHUB_TOKEN` | GitHub releases | `ghp_...` |

---

## Docker Configuration

Render uses your `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000
CMD ["python", "run_prod.py"]
```

**Key Points:**
- ✅ Uses `run_prod.py` (production WSGI server)
- ✅ Exposes port 10000 (Render's standard)
- ✅ Installs all dependencies from `requirements.txt`
- ✅ Copies entire app into container

---

## Troubleshooting

### Deployment Fails
- Check "Logs" tab in Render dashboard
- Common issues:
  - Missing `Dockerfile`
  - Missing dependencies in `requirements.txt`
  - Port not set to 10000

### App Crashes After Deploy
- Check environment variables are set
- Check `FLASK_SECRET` is not empty
- Review app logs in Render dashboard

### Slow First Deployment
- First build can take 3-5 minutes
- Subsequent deploys are faster (layer caching)

---

## Live Deployment

Once deployed, your app is live at:
- **URL:** `https://semptify-[random].onrender.com`
- **Health Check:** `https://semptify-[random].onrender.com/health`
- **Admin Panel:** `https://semptify-[random].onrender.com/admin`

---

## Auto-Deployment on Git Push

After connecting, **every push triggers auto-deploy:**

```powershell
# Dev branch auto-deploys
git push origin copilot/vscode1762361470744

# Main branch auto-deploys
git push origin main
```

Check deployment status in Render Dashboard → Deploys tab.

---

## Custom Domain (Optional)

1. Go to Render Dashboard → Your Service
2. Click "Settings" → "Custom Domains"
3. Add your domain: `semptify.yourdomain.com`
4. Follow DNS configuration instructions
5. DNS propagates in 24-48 hours

---

## Monitoring & Logs

### View Logs
- Render Dashboard → Your Service → "Logs"
- Real-time streaming of app output

### View Metrics
- Render Dashboard → Your Service → "Metrics"
- CPU, Memory, Disk usage

### Health Checks
Render automatically checks `/health` endpoint every 5 minutes.

---

## Rollback (If Needed)

1. Go to Render Dashboard
2. Click "Deploys"
3. Find previous successful deployment
4. Click "..." → "Redeploy"

---

## Pricing

- **Free Tier:** 750 hours/month (1 service)
- **Pro Tier:** $7/month per service
- Scales automatically

---

## Next Steps

✅ Connect to Render Dashboard  
✅ Add environment variables  
✅ Click "Create Web Service"  
✅ Wait for deployment  
✅ Visit your live URL  

Your Semptify app is ready to deploy! 🎉
