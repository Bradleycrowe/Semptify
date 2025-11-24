# Single-User Mode Setup Guide

## What Changed?
- ✅ **Removed multi-user authentication** - No login required
- ✅ **Added profile system** - Manage multiple cases/clients under one account
- ✅ **R2 persistent storage** - All data backed up to Cloudflare R2
- ✅ **Local AI support** - Run AI on your own PC (no API costs)

---

## Quick Start (3 Steps)

### Step 1: Configure Storage (R2)
Your data is stored in Cloudflare R2 (already set up). Add your credentials to `.env`:

```env
R2_ACCOUNT_ID=<your_account_id>
R2_ACCESS_KEY_ID=<your_key>
R2_SECRET_ACCESS_KEY=<your_secret>
R2_BUCKET_NAME=Semptify
R2_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
```

**Where to find R2 credentials:**
1. Go to Cloudflare Dashboard → R2
2. Click "Manage R2 API Tokens"
3. Create new token with read/write access
4. Copy Account ID, Access Key, Secret Key

### Step 2: Setup Local AI (Optional but Recommended)

**Install Ollama on Windows:**
```powershell
# Download from https://ollama.com/download
# Or use winget:
winget install Ollama.Ollama

# Pull recommended model (1.3GB):
ollama pull llama3.2

# Verify it works:
curl http://localhost:11434/api/tags
```

**Using Another PC as AI Server:**
If you have a more powerful PC on your network:
```powershell
# On the AI server PC:
$env:OLLAMA_HOST="0.0.0.0"
ollama serve

# In Semptify .env:
OLLAMA_BASE_URL=http://192.168.1.100:11434  # Replace with actual IP
```

### Step 3: Run Semptify
```powershell
cd C:\Semptify\Semptify
.\.venv\Scripts\Activate.ps1
python Semptify.py
```

Access at: **http://localhost:5000**

---

## Managing Multiple Cases/Clients

### Access Profile Manager
Navigate to: **http://localhost:5000/profiles**

### Create New Profile
1. Click the **"+"** card
2. Enter name: `"Smith Property Dispute"`
3. Add description: `"Rent increase issue, started Oct 2025"`
4. Pick a color tag
5. Click Save

### Switch Between Profiles
- Click **"Switch to This"** on any profile card
- All data (vault, ledger, timeline) is isolated per profile

### Profile Data Structure
Each profile gets its own directory:
```
data/profiles/
  ├── default/           # Your first case
  ├── smith_property/    # Second case
  └── jones_manager/     # Third case
```

**Everything is automatically synced to R2** - switch devices anytime!

---

## Environment Variables Reference

### Required (Single-User Mode)
```env
SECURITY_MODE=open              # No login required
FLASK_SECRET=any_random_string  # For sessions
```

### R2 Storage (Persistent Data)
```env
R2_ACCOUNT_ID=abc123
R2_ACCESS_KEY_ID=your_key
R2_SECRET_ACCESS_KEY=your_secret
R2_BUCKET_NAME=Semptify
R2_ENDPOINT_URL=https://abc123.r2.cloudflarestorage.com
```

### Local AI (Ollama)
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=120
AI_PROVIDER=ollama
```

### Optional Features
```env
# GitHub integration (for releases)
GITHUB_TOKEN=ghp_xxxxx

# Google Drive OAuth
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret
```

---

## How Data is Stored

### Local (Fast Access)
```
C:\Semptify\Semptify\
  ├── data/profiles/          # Profile configs
  ├── uploads/vault/          # Documents (cached locally)
  ├── logs/                   # Application logs
  └── users.db                # Minimal local state
```

### R2 (Persistent Backup)
```
Semptify (bucket)
  ├── data/profiles/
  │   ├── profiles.json       # All profiles
  │   ├── active_profile.json # Current active
  │   ├── default/            # Case 1 data
  │   └── smith_property/     # Case 2 data
  ├── vault/                  # All documents
  └── logs/                   # Event history
```

**Sync happens automatically:**
- On startup: Downloads latest from R2
- On profile switch: Syncs to R2
- On document upload: Uploads to R2

---

## Recommended AI Models

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| `llama3.2` | 1.3GB | General use, fast | ⚡⚡⚡ |
| `mistral` | 4.1GB | Legal reasoning | ⚡⚡ |
| `phi3` | 2.3GB | Small but smart | ⚡⚡⚡ |
| `llama3.1:8b` | 4.7GB | Accuracy | ⚡ |
| `codellama` | 3.8GB | Document analysis | ⚡⚡ |

**Pull a model:**
```powershell
ollama pull llama3.2
ollama pull mistral
```

**Switch models in .env:**
```env
OLLAMA_MODEL=mistral  # Use mistral instead
```

---

## Troubleshooting

### R2 Connection Issues
```powershell
# Test R2 connection:
.\.venv\Scripts\python.exe -c "from r2_profile_storage import get_r2_client, sync_profiles_to_r2; client = get_r2_client(); print('✓ R2 connected' if client else '✗ R2 offline'); sync_profiles_to_r2()"
```

### Ollama Not Found
```powershell
# Check if Ollama is running:
curl http://localhost:11434/api/tags

# If offline, start it:
ollama serve
```

### Profile Not Switching
```powershell
# Reset to default profile:
.\.venv\Scripts\python.exe -c "from profile_manager import set_active_profile; set_active_profile('default'); print('✓ Reset to default')"
```

---

## Next Steps

1. **Access the app**: http://localhost:5000
2. **Create profiles**: /profiles
3. **Start using modules** (see MODULES_REFERENCE.md):
   - Vault: Upload documents
   - Complaint Filing: Generate court forms
   - Ledger: Track rent payments
   - Learning: Let AI learn your case patterns

4. **Check AI status**: /admin (shows Ollama connection)

---

## Benefits of This Setup

✅ **No external dependencies** - Everything runs on your PC  
✅ **No API costs** - Local AI is free  
✅ **Data privacy** - Your R2 bucket, your control  
✅ **Multiple cases** - Organize by client/property  
✅ **Real-world data** - Every case trains your AI better  
✅ **Portable** - Access from any device with R2 sync  

---

## Need Help?

- Module reference: `MODULES_REFERENCE.md`
- Architecture: `.github/copilot-instructions.md`
- Ollama docs: https://ollama.com/docs
- Cloudflare R2: https://developers.cloudflare.com/r2/
