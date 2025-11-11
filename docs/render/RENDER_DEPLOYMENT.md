# 🚀 Semptify Deployment Guide for Render.com

Complete step-by-step guide to deploy Semptify on Render.com with full production capabilities.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ GitHub account with the Semptify repository
- ✅ [Render.com](https://render.com) account (free tier available)
- ✅ Git repository pushed to GitHub (or ready to push)
- ✅ Environment variables prepared

**Typical deployment time:** 5-10 minutes

---

## 🔑 Step 1: Prepare Environment Variables

Before deploying, you'll need to set these Render environment variables. Create a secure `.env` file or set them in Render's dashboard:

### Essential Variables (Required)

```bash
# Flask security
FLASK_SECRET=generate_a_strong_random_hex_string_here
SECRET_KEY=generate_another_strong_random_hex_string_here

# Security mode (production should be "enforced")
SECURITY_MODE=enforced

# Admin authentication
ADMIN_TOKEN=your_secure_admin_token_here

# Port (Render sets PORT env var, but we use this)
SEMPTIFY_PORT=8080
```

### AI Provider Configuration (Choose One)

**Option A: Groq (Free & Fast)**
```bash
AI_PROVIDER=openai
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=llama-3.1-8b-instant
OPENAI_API_KEY=your_groq_api_key
```

**Option B: OpenAI**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4-turbo
```

**Option C: Azure OpenAI**
```bash
AI_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Optional Security Variables

```bash
# Rate limiting
ADMIN_RATE_WINDOW=60        # seconds
ADMIN_RATE_MAX=60           # requests per window
ADMIN_RATE_STATUS=429       # HTTP status code

# HTTPS/Security headers
FORCE_HTTPS=1
HSTS_MAX_AGE=31536000
HSTS_PRELOAD=1

# Logging
ACCESS_LOG_JSON=1           # Enable JSON logging
LOG_MAX_BYTES=1048576       # Log rotation size

# GitHub integration (optional)
GITHUB_OWNER=Bradleycrowe
GITHUB_REPO=Semptify
GITHUB_TOKEN=your_github_token_for_releases
```

---

## 🎯 Step 2: Connect GitHub to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **+ New** → **Web Service**
3. Select **Build and deploy from a Git repository**
4. Click **Connect your GitHub account** (if not already connected)
5. Authorize Render to access your GitHub repos
6. Select **Bradleycrowe/SemptifyGUI** repository
7. Choose branch: **main** (or your current branch)
8. Click **Connect**

---

## ⚙️ Step 3: Configure Web Service

Fill in the service configuration:

| Field | Value |
|-------|-------|
| **Name** | `semptify` (or your preferred name) |
| **Region** | `Ohio` (or closest to your users) |
| **Branch** | `main` |
| **Runtime** | `Docker` |
| **Build Command** | *(Leave empty - uses Dockerfile)* |
| **Start Command** | *(Leave empty - uses Dockerfile CMD)* |

### Instance Type

- **Free Tier**: 0.5 CPU, 512 MB RAM (suitable for dev/testing)
- **Starter**: 2 CPU, 2 GB RAM (recommended for production)

Click **Create Web Service**

---

## 🔒 Step 4: Add Environment Variables

In the Render dashboard for your service:

1. Go to **Environment** tab
2. Add all variables from Step 1
3. For sensitive values (API keys, tokens), use Render's "Secret Files" feature:
   - Scroll to **Secret Files** section
   - Create a file named `.env`
   - Paste your sensitive environment variables
4. Click **Save Changes**

---

## 🐳 Step 5: Docker Build (Automatic)

Render will automatically:

1. ✅ Read the `Dockerfile` from your repository
2. ✅ Build the Docker image
3. ✅ Create a container
4. ✅ Deploy to their infrastructure
5. ✅ Provide you with a public URL

Monitor the build in **Logs** tab. First deployment typically takes 5-10 minutes.

Expected output:
```
Building image
Pushing image to registry
Deploying to service
Your service is live at: https://semptify-xxxxx.onrender.com
```

---

## ✅ Step 6: Verify Deployment

Once deployed, test your service:

### Health Check
```bash
curl https://semptify-xxxxx.onrender.com/health
# Expected response: {"status": "ok"}
```

### Readiness Check
```bash
curl https://semptify-xxxxx.onrender.com/readyz
# Expected response: {"status": "ready"}
```

### Metrics Endpoint
```bash
curl https://semptify-xxxxx.onrender.com/metrics
```

### Access the SPA
Open in browser:
```
https://semptify-xxxxx.onrender.com/spa
```

### Register a User
```
https://semptify-xxxxx.onrender.com/register
```

---

## 🔄 Step 7: Configure Auto-Deployment

To automatically deploy on every push to main:

1. Go to **Settings** → **Build & Deploy**
2. Under "Deploy on Push", select **Yes**
3. Choose trigger: **main** branch
4. Click **Save**

Now every push to `main` automatically redeploys!

---

## 📊 Monitoring & Logs

### View Logs
1. Go to **Logs** tab in Render dashboard
2. See real-time logs from your running service
3. Filter by date/time if needed

### Common Issues & Solutions

#### Service won't start
```
Check logs for: ImportError, ModuleNotFoundError
Solution: Ensure requirements.txt has all dependencies
```

#### Port already in use
```
Error: Address already in use
Solution: Render manages ports automatically - this shouldn't happen
```

#### Health check failing
```
GET /health → 503 Service Unavailable
Solution: Check initialization logs, ensure data directories created
```

#### Timeout on first deploy
```
Error: Deployment timed out
Solution: Increase timeout in Settings, or reduce build complexity
```

---

## 💾 Database & Persistent Storage

⚠️ **Important:** Render's free tier has **ephemeral storage** - data is deleted when service restarts!

### For Production:

1. **Use External Database:**
   - Render PostgreSQL service (recommended)
   - AWS RDS
   - Azure Database

2. **Configure Semptify to use it:**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:5432/semptify
   ```

3. **Mount persistent storage:**
   - Use Render Disks feature (paid)
   - Or integrate with S3/Azure Blob Storage

For production data, configure:
- `uploads/` → S3 bucket
- `ledgers/` → Database
- `logs/` → CloudWatch/Loki

---

## 🔐 Security Best Practices

### 1. **Generate Strong Tokens**
```bash
# Generate random hex tokens (run locally)
python -c "import secrets; print(secrets.token_hex(32))"
```

Use this for:
- `FLASK_SECRET`
- `ADMIN_TOKEN`
- `SECRET_KEY`

### 2. **Rotate Tokens Regularly**
- Update environment variables every 90 days
- Use Render's secret rotation feature

### 3. **Enable HTTPS**
Render automatically provides HTTPS. Ensure:
```bash
FORCE_HTTPS=1
HSTS_MAX_AGE=31536000
HSTS_PRELOAD=1
```

### 4. **Rate Limiting**
Already configured:
```bash
ADMIN_RATE_WINDOW=60
ADMIN_RATE_MAX=60
```

### 5. **Monitor Admin Activity**
- Check logs for `admin_` events
- Review `/metrics` endpoint for suspicious activity
- Set up alerts for rate limiting hits

---

## 📈 Scaling (Paid Plans)

If your deployment needs scaling:

1. Upgrade instance type (More CPU/RAM)
2. Enable auto-scaling
3. Use Render Load Balancer
4. Add PostgreSQL database for sessions

---

## 🔗 Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **Semptify GitHub:** https://github.com/Bradleycrowe/SemptifyGUI
- **API Health:** https://semptify-xxxxx.onrender.com/health
- **SPA App:** https://semptify-xxxxx.onrender.com/spa
- **Documentation:** Check README.md in repository

---

## ❓ Troubleshooting

### Push to GitHub Still Failing?

```bash
# Check git status
git status

# Verify large files are removed from cache
git ls-files | grep -E '\.(zip|exe)$'

# If files still tracked, remove them:
git rm --cached <filename>
git commit -m "Remove large files"

# Try push again
git push origin main
```

### Render Deployment Won't Start?

1. Check Dockerfile is valid: `docker build -t semptify .`
2. Verify requirements.txt dependencies
3. Check environment variables are set
4. Look at Render logs for specific error

### Need to Rollback?

```bash
# Go to Render dashboard → Deployments
# Select previous successful deployment
# Click "Redeploy"
```

---

## 🎉 Success Indicators

Your Semptify deployment is working when:

✅ `/health` returns 200 OK
✅ `/readyz` returns ready status
✅ `/spa` loads the single-page app
✅ `/register` shows registration form
✅ Can create users and view vault
✅ Can access calendar and ledger system

---

## 📞 Support

For issues:
1. Check Render logs first
2. Review this guide's troubleshooting section
3. Check Semptify GitHub issues
4. Contact Render support for infrastructure issues

---

**Your Semptify instance is now ready for production!** 🚀

