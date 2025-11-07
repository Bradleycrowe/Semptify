# ⚡ R2 Quick Setup - 5 Minutes

## 1️⃣ Cloudflare (2 min)
```
1. https://dash.cloudflare.com/ → R2 → Create bucket → "semptify-storage"
2. Manage R2 API Tokens → Create → Object Read & Write → Copy 4 values ⬇️
```

## 2️⃣ Render (2 min)
```
Go to: https://dashboard.render.com/ → Semptify → Environment → Add vars:

R2_ACCOUNT_ID = abc123...
R2_ACCESS_KEY_ID = a1b2c3...
R2_SECRET_ACCESS_KEY = X7Y8Z9...
R2_BUCKET_NAME = semptify-storage
```

## 3️⃣ Verify (1 min)
```
Render logs should show:
✅ "Storage mode: R2"
```

## 📊 What You Get
- ✅ 10GB free persistent storage
- ✅ Survives Render redeployments
- ✅ Zero code changes needed
- ✅ Automatic fallback to local if R2 unavailable

## 🚨 Important
- Save your Secret Access Key immediately (can't view again!)
- Never commit R2 credentials to git
- Current deployment: commit `aeb36cc`

## 📖 Full Guide
See `R2_STORAGE_SETUP.md` for detailed instructions, troubleshooting, and examples.

---

**Cost**: $0/month (under 10GB)  
**Status**: Code deployed ✅ | Credentials needed ⏳
