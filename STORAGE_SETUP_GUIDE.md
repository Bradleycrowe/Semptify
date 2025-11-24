# STORAGE_SETUP_GUIDE.md - Tiered Storage Configuration

## Overview
Semptify uses **tiered storage**: R2 (primary) + Google Drive (fallback) + Local (last resort).

## Architecture
- **Single User**: YOU manage the system
- **Multiple Clients**: Separate profiles for each case/client
- **R2 Primary**: Fast, S3-compatible Cloudflare storage
- **Google Drive Secondary**: Redundant backup using 1semptify@gmail.com
- **Local Fallback**: Always saves locally if cloud fails

## Storage Modes (STORAGE_MODE env var)
- `auto` (default): Try R2 → Google Drive → Local
- `r2_only`: Only use R2 (fail if unavailable)
- `gdrive_only`: Only use Google Drive
- `both`: Upload to both R2 AND Google Drive simultaneously

---

## Setup: Google Drive (1semptify@gmail.com)

### 1. Create Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Create new project: "Semptify Storage"
3. Enable Google Drive API:
   - APIs & Services → Library → Search "Google Drive API" → Enable

### 2. Create OAuth 2.0 Credentials
1. APIs & Services → Credentials → Create Credentials → OAuth client ID
2. Application type: **Desktop app**
3. Name: "Semptify Desktop"
4. Download JSON → Save as `security/gdrive_credentials.json`

### 3. Add Test User (1semptify@gmail.com)
1. OAuth consent screen → Test users → Add users
2. Add: `1semptify@gmail.com`

### 4. First-Time Authorization
Run:
```powershell
C:\Semptify\Semptify\.venv\Scripts\python.exe test_storage_tiers.py
```

Browser opens → Sign in with `1semptify@gmail.com` → Allow access
Token saved to `security/gdrive_token.json`

---

## Setup: R2 Storage

### From Render Dashboard
1. Open: https://dashboard.render.com/
2. Select your Semptify service
3. Environment → Reveal Config Vars
4. Copy these values:
   - `R2_ENDPOINT_URL`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`
   - `R2_BUCKET_NAME`

### Add to Local .env
```env
# R2 Storage (Cloudflare)
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key_here
R2_SECRET_ACCESS_KEY=your_secret_key_here
R2_BUCKET_NAME=Semptify

# Google Drive (Optional - for redundancy)
GDRIVE_CREDENTIALS_FILE=security/gdrive_credentials.json
GDRIVE_TOKEN_FILE=security/gdrive_token.json
GDRIVE_FOLDER_NAME=Semptify_Storage

# Storage Mode
STORAGE_MODE=auto
```

---

## Testing Storage

### Test All Backends
```powershell
C:\Semptify\Semptify\.venv\Scripts\python.exe test_storage_tiers.py
```

Expected output:
```
[INFO] Initializing storage backends...
[OK] R2 connected
[OK] Google Drive connected (folder: abc123xyz)
[INFO] Storage: R2=True, GoogleDrive=True, Local=True

=== Storage Availability ===
[OK] R2: True
[OK] GDRIVE: True
[OK] LOCAL: True

=== Testing Upload (profile: test_client_001) ===
[OK] Uploaded to R2: test_document.txt
[OK] Uploaded to Google Drive: test_document.txt
Upload results: {'r2': True, 'gdrive': True, 'local': True}
```

### Check Google Drive
1. Go to: https://drive.google.com/ (sign in as 1semptify@gmail.com)
2. Look for folder: **Semptify_Storage**
3. Inside: **test_client_001** folder with uploaded files

---

## Integration with Existing Modules

### Vault Module
Update `vault.py` to use `storage_manager`:
```python
from storage_manager import upload_file, download_file, list_files

# Replace local file saves with:
upload_file(profile_id, filename, file_data)

# Replace local file reads with:
data = download_file(profile_id, filename)
```

### Profile Manager
Update `profile_manager.py`:
```python
from storage_manager import save_json, load_json

# Replace profile file operations with:
save_json(profile_id, "metadata.json", profile_data)
data = load_json(profile_id, "metadata.json")
```

---

## File Structure in Storage

### R2 Bucket Layout
```
Semptify/
  data/
    profiles/
      default/
        case_notes.txt
        evidence_photo.jpg
      client_001/
        lease_agreement.pdf
        timeline.json
      client_002/
        ...
```

### Google Drive Layout
```
Semptify_Storage/          (root folder)
  default/
    case_notes.txt
    evidence_photo.jpg
  client_001/
    lease_agreement.pdf
    timeline.json
  client_002/
    ...
```

### Local Fallback Layout
```
C:\Semptify\Semptify\
  data/
    profiles/
      default/
        case_notes.txt
      client_001/
        ...
```

---

## Security Notes

**DO NOT commit these files:**
- `security/gdrive_credentials.json` (OAuth client secret)
- `security/gdrive_token.json` (User access token)
- `.env` (R2 credentials)

**Already in .gitignore:**
```
security/
.env
data/
```

---

## Troubleshooting

### Google Drive: "Access blocked"
- Add `1semptify@gmail.com` to OAuth test users
- Make sure project is in "Testing" mode

### R2: "Signature mismatch"
- Check `R2_ENDPOINT_URL` includes `https://`
- Verify access key and secret are correct
- Make sure bucket name matches (case-sensitive)

### "Local fallback only"
- Both R2 and Google Drive failed
- Check logs for specific errors
- Verify credentials in `.env`

---

## Next Steps

1. Get Google Drive credentials → Save as `security/gdrive_credentials.json`
2. Run test script → Authorize with 1semptify@gmail.com
3. Add R2 credentials from Render → Update `.env`
4. Run test again → Verify both backends work
5. Update vault/profile modules to use `storage_manager`

