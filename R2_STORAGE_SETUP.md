# Cloudflare R2 Storage Setup for Semptify

## What You Get
- **10GB free storage** on Cloudflare R2
- **Persistent storage** - data survives Render redeployments
- **Fast access** - Cloudflare's global CDN
- **Zero-config fallback** - works without R2 (local storage for dev)

---

## Step 1: Create Cloudflare R2 Bucket (5 minutes)

### 1.1 Sign Up / Login
1. Go to https://dash.cloudflare.com/
2. Sign up (if new) or login
3. You may need to add a payment method, but **10GB is free** (no charges unless you exceed)

### 1.2 Create R2 Bucket
1. In Cloudflare dashboard, click **R2** in left sidebar
2. Click **Create bucket**
3. **Name**: `semptify-storage` (or your preferred name)
4. **Location**: Automatic (Cloudflare chooses best)
5. Click **Create bucket**

### 1.3 Create API Token
1. In R2 section, click **Manage R2 API Tokens**
2. Click **Create API Token**
3. **Token Name**: `Semptify App`
4. **Permissions**: 
   - ✅ Object Read & Write
   - ✅ Edit
5. **TTL**: Forever (or 1 year if you prefer rotation)
6. **Bucket**: Choose `semptify-storage` (or select "All buckets")
7. Click **Create API Token**

### 1.4 Save Credentials
**IMPORTANT**: Copy these values immediately (you won't see them again):
- **Account ID**: looks like `abc123def456...`
- **Access Key ID**: looks like `a1b2c3d4e5f6...`
- **Secret Access Key**: looks like `X7Y8Z9A0B1C2...` (long string)
- **Bucket Name**: `semptify-storage`

---

## Step 2: Add to Render Environment Variables

1. Go to https://dashboard.render.com/
2. Select your **Semptify** service
3. Click **Environment** tab
4. Click **Add Environment Variable** for each:

```
R2_ACCOUNT_ID = <your-account-id>
R2_ACCESS_KEY_ID = <your-access-key-id>
R2_SECRET_ACCESS_KEY = <your-secret-access-key>
R2_BUCKET_NAME = semptify-storage
```

5. Also add your security tokens if not already present:
```
FLASK_SECRET = 4hBPciTbKz19MlaqsUyfvxJYW7AkGrwX8mnHedLEu6NIC5DjRSoOpQF30VtgZ2
ADMIN_TOKEN = SbNw7uld3MQTrVgayjhBez06YmpIqWxn
SECURITY_MODE = enforced
FORCE_HTTPS = 1
```

6. Click **Save Changes** - Render will redeploy automatically

---

## Step 3: Verify Storage Mode

After Render finishes deploying, check your logs:

1. Go to **Logs** tab in Render dashboard
2. Look for this line during startup:
   ```
   Storage mode: R2
   ```

If you see `Storage mode: Local (ephemeral)`, check that:
- All 4 R2 environment variables are set correctly
- boto3 installed (in requirements.txt - already done ✅)
- No typos in variable names

---

## How It Works

### Storage Adapter (`storage_adapter.py`)
- **Automatic detection**: If R2 credentials present, uses R2. Otherwise local.
- **Zero code changes**: Import `storage` and use it anywhere
- **Graceful fallback**: If boto3 missing or R2 errors, falls back to local

### Example Usage
```python
from storage_adapter import storage

# Save a file
storage.save_file(
    'vault/user123/document.pdf',
    file_bytes,
    metadata={'user': 'user123', 'ts': '2025-11-07'}
)

# Read a file
content = storage.read_file('vault/user123/document.pdf')

# Check if file exists
if storage.file_exists('vault/user123/document.pdf'):
    print("File found!")

# List files
files = storage.list_files(prefix='vault/user123/')

# Delete file
storage.delete_file('vault/user123/document.pdf')
```

---

## Cost Breakdown

### Cloudflare R2 Free Tier (per month)
- ✅ **10 GB storage** - FREE
- ✅ **1 million Class A operations** (write/list) - FREE
- ✅ **10 million Class B operations** (read) - FREE
- ⚠️ **No egress charges** (unlike AWS S3!)

### If You Exceed Free Tier
- $0.015/GB storage over 10GB
- Example: 20GB = 10GB free + 10GB × $0.015 = **$0.15/month**

### Comparison to Alternatives
| Service | Free Tier | Cost Over |
|---------|-----------|-----------|
| Cloudflare R2 | 10GB | $0.015/GB |
| Render Disk | 0GB | $0.25/GB |
| AWS S3 | 5GB (first year) | $0.023/GB + egress |

**Winner**: Cloudflare R2 🏆

---

## Testing Your Setup

### Test 1: Check Storage Mode
```bash
curl https://semptify.onrender.com/health
# Look for logs showing "Storage mode: R2"
```

### Test 2: Upload a File (Vault)
1. Register a user: https://semptify.onrender.com/register
2. Go to vault: https://semptify.onrender.com/vault?user_token=<your-token>
3. Upload a file
4. Check Cloudflare R2 bucket - file should appear under `vault/<user_id>/`

### Test 3: Persistence Check
1. Upload a file
2. Trigger Render redeploy (or wait for next deploy)
3. File should still be accessible after redeploy

---

## What Gets Stored in R2

With current implementation:
- ✅ **Vault uploads** - user document storage
- ⏳ **Witness statements** (ready to migrate)
- ⏳ **Service packets** (ready to migrate)
- ⏳ **Calendar attachments** (ready to migrate)
- ⏳ **Ledger exports** (ready to migrate)

To migrate other features, update their modules to use:
```python
from storage_adapter import storage
# Instead of: open('uploads/file.pdf', 'wb')
# Use: storage.save_file('file.pdf', content)
```

---

## Troubleshooting

### "Storage mode: Local (ephemeral)" in logs
**Cause**: R2 credentials not detected
**Fix**: 
1. Check all 4 R2 env vars are set in Render
2. No typos in variable names
3. Redeploy after adding vars

### "R2 save error" messages
**Cause**: boto3 import failed or credentials invalid
**Fix**:
1. Check requirements.txt has `boto3>=1.34.0` ✅
2. Verify Access Key ID and Secret Access Key are correct
3. Check bucket name matches exactly

### Files not appearing in R2 bucket
**Cause**: Using old code that writes to local filesystem
**Fix**: Update modules to use `storage_adapter` instead of `open()`

### "Access Denied" errors
**Cause**: API token doesn't have write permissions
**Fix**: Recreate API token with "Object Read & Write" enabled

---

## Next Steps

### Immediate
1. ✅ Add R2 credentials to Render
2. ✅ Verify "Storage mode: R2" in logs
3. ⏳ Test file upload in vault

### Future Enhancements
- **Migrate other modules** to use storage_adapter
- **Add file browser** - UI to view R2 files
- **Automatic backups** - daily snapshots to another bucket
- **CDN integration** - serve files via Cloudflare CDN (currently R2 direct)

---

## Security Notes

- ✅ R2 credentials are secret (never commit to git)
- ✅ Files are private by default (not publicly accessible)
- ✅ Access controlled via user tokens and admin tokens
- ⚠️ Consider adding encryption at rest (R2 supports this)
- ⚠️ Consider adding presigned URLs for time-limited access

---

## Questions?

- **What happens if R2 goes down?** - App falls back to local storage (ephemeral)
- **Can I switch back to local?** - Yes, just remove R2 env vars
- **Can I use S3 instead?** - Yes, change endpoint in `storage_adapter.py` line 41
- **How do I backup R2?** - Use `rclone` or Cloudflare's backup features

---

**Status**: ✅ Storage adapter deployed (commit aeb36cc)
**Next**: Add R2 credentials to Render dashboard
