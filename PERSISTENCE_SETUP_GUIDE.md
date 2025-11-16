# Persistence Configuration Guide

## CRITICAL: Semptify Requires Persistent Storage

### Problem
Render.com containers are **ephemeral** - all data is lost on:
- Container restarts
- New deployments
- Platform maintenance
- Scaling events

### What Gets Lost Without Persistence
❌ **User vault documents** (PDFs, images, evidence)
❌ **Notary certificates** (SHA256 hashes, timestamps)
❌ **User accounts** (login credentials, tokens)
❌ **Timeline events** (user history)
❌ **Admin tokens** (admin authentication)
❌ **Learning patterns** (AI adaptive knowledge)

### Solutions Implemented

#### 1. Document Storage (Vault Files)
**Solution**: StorageAdapter with R2/GCS backend
- Files: `uploads/vault/**/*`
- Handler: `storage_adapter.py`
- Status: ✓ Code ready, needs configuration

#### 2. Database (users.db)
**Solution**: Cloud backup/restore service
- File: `users.db` (SQLite)
- Handler: `services/db_persistence.py`
- Features:
  - Restores from cloud on startup
  - Auto-backup every 5 minutes
  - Backup on graceful shutdown
- Status: ✓ Implemented, needs R2/GCS

#### 3. Critical Config Files
**Solution**: Include in git or use env vars
- `security/admin_tokens.json` → Regenerate or commit
- `security/users.json` → Stored in users.db
- `data/learning_patterns.json` → Backup to cloud

## Setup: Enable Persistence

### Option A: Cloudflare R2 (Recommended)

1. **Create R2 bucket**:
   - Go to Cloudflare dashboard
   - R2 → Create bucket → "semptify-vault"
   
2. **Generate API token**:
   - R2 → Manage R2 API Tokens → Create API Token
   - Permissions: Read/Write
   - Copy: Account ID, Access Key ID, Secret Access Key

3. **Configure Render environment**:
   ```
   R2_ACCOUNT_ID=your_account_id
   R2_ACCESS_KEY_ID=your_access_key
   R2_SECRET_ACCESS_KEY=your_secret_key
   R2_BUCKET_NAME=semptify-vault
   R2_ENDPOINT_URL=https://your_account_id.r2.cloudflarestorage.com
   ```

4. **Deploy**:
   - StorageAdapter automatically detects R2 config
   - All vault operations persist to R2
   - Database backups every 5 minutes

### Option B: Google Cloud Storage

1. **Install package** (add to requirements.txt):
   ```
   google-cloud-storage>=2.10.0
   ```

2. **Create GCS bucket**:
   - GCP Console → Cloud Storage → Create bucket
   - Name: "semptify-vault"
   - Location: Multi-region
   
3. **Create service account**:
   - IAM → Service Accounts → Create
   - Grant: Storage Object Admin
   - Create key (JSON)

4. **Configure Render**:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/app/gcs-key.json
   GCS_BUCKET_NAME=semptify-vault
   GOOGLE_CLOUD_PROJECT=your-project-id
   ```

5. **Upload service account key**:
   - Render → Environment → Secret Files
   - Add `gcs-key.json` with service account JSON

### Option C: Render Persistent Disk (Paid)

1. **Create persistent disk** (Render dashboard)
   - Size: 10GB minimum
   - Mount path: `/mnt/data`

2. **Update code** to use `/mnt/data`:
   ```python
   DB_PATH = "/mnt/data/users.db"
   VAULT_BASE = "/mnt/data/vault"
   ```

3. **Pros**: Simple, fast, no external service
4. **Cons**: Paid feature, single-region only

## Verification

### Test Persistence
```bash
# 1. Upload a document to vault
curl -X POST https://semptify.onrender.com/vault \
  -F "file=@test.pdf" \
  -H "X-User-Token: your_token"

# 2. Trigger deploy (or restart container)
# 3. Check if document still exists
curl https://semptify.onrender.com/vault?user_token=your_token

# Document should still be there ✓
```

### Check Database Backup
```bash
# In Render logs, look for:
[DB] Initializing database persistence...
[DB] ✓ Restored 42.3 KB from cloud
[DB-PERSIST] Auto-backup started (every 300s)
```

### Monitor Storage Usage
- R2: Cloudflare dashboard → R2 → Bucket metrics
- GCS: GCP Console → Cloud Storage → Bucket details
- Files stored: `vault/user_id/*`, `database/users.db`

## Cost Estimate

### R2 (Cloudflare)
- Storage: $0.015/GB/month
- Operations: Class A (write) $4.50/million, Class B (read) $0.36/million
- **Typical 100 users**: ~$2-3/month

### GCS (Google)
- Storage: $0.020/GB/month (Standard)
- Operations: Class A $0.05/10k, Class B $0.004/10k
- Free tier: 5GB storage, 5k Class A, 50k Class B
- **Typical 100 users**: Free tier sufficient

### Render Persistent Disk
- 10GB: $10/month
- 100GB: $25/month
- **Simple but more expensive**

## Recommendation

🎯 **Use Cloudflare R2**:
- Cheaper than GCS
- No package dependencies (uses boto3, already installed)
- Global CDN included
- Simple setup

## Current Status

✓ Code implemented (`storage_adapter.py`, `services/db_persistence.py`)
✓ Integrated into Semptify.py startup
✓ Auto-backup every 5 minutes
✓ Graceful shutdown backup
❌ **NOT CONFIGURED** - using ephemeral local storage

⚠️ **ACTION REQUIRED**: Set R2/GCS environment variables to enable persistence
