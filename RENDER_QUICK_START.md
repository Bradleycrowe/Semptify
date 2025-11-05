# 🚀 Render Deployment - Quick Start (5 Minutes)

## Step 1: Generate Secure Tokens

Run this command locally to generate strong random tokens:

```powershell
python -c "import secrets; print('FLASK_SECRET=' + secrets.token_hex(32)); print('ADMIN_TOKEN=' + secrets.token_hex(16))"
```

Save the output - you'll need these tokens.

---

## Step 2: Push to GitHub

Your code is now being pushed to GitHub via: `copilot/communication-suite` branch

Once complete, create a **Pull Request** on GitHub:
- From: `copilot/communication-suite`
- To: `main`
- Merge it to `main`

Or simply push directly to `main`:
```bash
git checkout main
git merge copilot/communication-suite
git push origin main
```

---

## Step 3: Go to Render Dashboard

1. Open: https://dashboard.render.com
2. Click: **+ New** → **Web Service**
3. Select: **Connect your GitHub account** (if not already)
4. Choose repository: **SemptifyGUI**
5. Click: **Connect**

---

## Step 4: Configure the Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `semptify` |
| **Region** | `Ohio` (or closest) |
| **Branch** | `main` |
| **Runtime** | `Docker` |
| **Dockerfile** | `./Dockerfile` |

Leave Build Command and Start Command **empty** (uses Dockerfile)

### Instance Type:
- **Free**: 0.5 CPU, 512MB RAM (dev/test)
- **Starter+**: 2 CPU, 2GB RAM (recommended)

---

## Step 5: Add Environment Variables

In Render dashboard, go to **Environment**:

### Add these variables:

```
FLASK_SECRET=<your_generated_token>
SECRET_KEY=<another_secure_token>
ADMIN_TOKEN=<your_admin_token>
SECURITY_MODE=enforced
SEMPTIFY_PORT=8080
AI_PROVIDER=openai
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=llama-3.1-8b-instant
OPENAI_API_KEY=<your_groq_api_key>
FORCE_HTTPS=1
HSTS_MAX_AGE=31536000
HSTS_PRELOAD=1
ACCESS_LOG_JSON=1
```

### For Sensitive Keys:
Use Render's **Secret Files** section instead:
- Create file: `.env`
- Paste all sensitive variables there

Click **Save** when done.

---

## Step 6: Deploy!

1. Scroll to bottom and click: **Create Web Service**
2. Watch the **Logs** tab for build progress
3. Wait for: "Your service is live at: `https://semptify-xxxxx.onrender.com`"

Typical build time: **5-10 minutes** ⏳

---

## Step 7: Test Your Deployment

Once live, test these endpoints:

```bash
# Health check
curl https://semptify-xxxxx.onrender.com/health

# Readiness check
curl https://semptify-xxxxx.onrender.com/readyz

# Metrics
curl https://semptify-xxxxx.onrender.com/metrics

# Open the app
https://semptify-xxxxx.onrender.com/spa
```

---

## ✅ Success Indicators

Your Semptify is working when:

✅ `/health` returns `{"status":"ok"}`
✅ `/spa` loads the single-page app
✅ `/register` shows registration form
✅ Can create users and access features
✅ Logs show successful requests

---

## 🔗 Your Deployment Links

After deployment, you'll have:

- **Main App**: `https://semptify-xxxxx.onrender.com/spa`
- **Registration**: `https://semptify-xxxxx.onrender.com/register`
- **Health**: `https://semptify-xxxxx.onrender.com/health`
- **Admin**: `https://semptify-xxxxx.onrender.com/admin?token=<ADMIN_TOKEN>`

---

## 📊 Enable Auto-Deploy

To automatically deploy on every push to `main`:

1. Go to **Settings** → **Build & Deploy**
2. Under "Deploy on Push": Select **Yes**
3. Choose branch: **main**
4. Click **Save**

Now every push = automatic deployment! 🎉

---

## 🆘 Troubleshooting

### Build fails with ImportError
- Check `requirements.txt` has all dependencies
- Run locally: `pip install -r requirements.txt`

### Service won't start
- Check logs for specific error
- Verify environment variables are set
- Try restarting the service: Render dashboard → Restart

### Timeout on first deploy
- This is normal for large apps
- Render free tier can take 10-15 minutes
- Be patient, don't restart multiple times

### Can't access the app
- Wait 2-3 minutes after "live" message
- Clear browser cache and hard refresh
- Check HTTPS is enabled in environment

---

## 📞 Quick Support

- **Render Help**: https://render.com/docs
- **GitHub Repo**: https://github.com/Bradleycrowe/SemptifyGUI
- **Check Logs**: Render dashboard → Logs tab
- **Restart Service**: Render dashboard → Manual Restart

---

## 🎯 What's Deployed

Your Render instance includes:

✅ Full Flask application with all modules
✅ Calendar + Ledger system (central hub)
✅ Single-page application (SPA)
✅ User registration with tokens
✅ Evidence management system
✅ Communication suite
✅ All law notes modules
✅ Comprehensive security (CSRF, rate limiting)
✅ Automatic HTTPS
✅ Docker containerization
✅ Health checks & monitoring

---

## 🚀 Next Steps

1. ✅ Push code to GitHub (in progress)
2. ⏳ Merge to main branch
3. ✅ Connect Render to GitHub
4. ✅ Add environment variables
5. ✅ Click "Create Web Service"
6. ✅ Wait for deployment to complete
7. ✅ Test all features
8. 🎉 Live in production!

**Estimated total time: 5-10 minutes** ⏱️

