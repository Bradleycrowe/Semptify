# R2 Persistence - Quick Reference

## ✅ What's Working
- **Cloudflare R2 Storage**: Fully operational
- **Bucket**: semptify (lowercase required)
- **Connection**: Verified with upload/download tests
- **Brad GUI**: Accessible at http://127.0.0.1:5001/brad
- **Client Data**: Persists to R2 (data/brad_clients/)
- **Vault Files**: Persists to R2 (uploads/vault/)

## 🚀 Quick Start

### Option 1: Use start script (recommended)
```powershell
.\start.ps1
```

### Option 2: Manual with R2
```powershell
. .\set_r2_env.ps1
python .\Semptify.py
```

### Option 3: Just venv activation
```powershell
.\.venv\Scripts\Activate.ps1
. .\set_r2_env.ps1
python .\Semptify.py
```

## 📊 Verify R2 Status
- Visit: http://127.0.0.1:5001/storage/status
- Should show: `"provider": "Cloudflare R2", "configured": true`

## 🔐 Environment Variables Set
- R2_ACCOUNT_ID: be2a39...
- R2_ACCESS_KEY_ID: c99403...
- R2_SECRET_ACCESS_KEY: (masked)
- R2_BUCKET_NAME: semptify
- R2_ENDPOINT_URL: https://be2a39cd3624261169fa8e800d75923f.r2.cloudflarestorage.com

## 📝 What Persists to R2
1. Client profiles: `data/profiles/{client_id}/*`
2. Brad clients list: Local + R2 backup (via storage_manager)
3. Vault documents: `data/profiles/{user_id}/{filename}`
4. Timeline events: Database + R2 backup

## ⚠️ Important Notes
- Data now survives restarts (stored in R2)
- Local copies still created as fallback
- Bucket name MUST be lowercase (AWS S3 requirement)
- First startup may show "Failed to restore" (normal if bucket empty)

## 🛠️ Troubleshooting
**"InvalidBucketName" error**: Check R2_BUCKET_NAME is lowercase
**"Access Denied"**: Verify credentials in set_r2_env.ps1
**"Connection refused"**: Check R2_ENDPOINT_URL format
**"Not configured" warning**: Ensure set_r2_env.ps1 sourced before python

## 📂 Files Created
- `set_r2_env.ps1`: R2 credentials (git-ignored)
- `start.ps1`: One-command launcher
- `r2_test.py`: Standalone connectivity test
- `r2_direct_test.py`: Direct boto3 validation

## 🎯 Next Steps for Production
1. Move credentials to secure vault (Azure KeyVault, 1Password, etc.)
2. Set environment variables in deployment platform (Render, Railway, etc.)
3. Enable Google Drive fallback (optional secondary backup)
4. Configure automated database backups to R2
