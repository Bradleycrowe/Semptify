# STORAGE QUALIFICATION SYSTEM

## Concept
**No user accounts in Semptify.** Users prove they control R2 or Google Cloud Storage → they're qualified.

## Flow
1. User visits homepage
2. Clicks "Qualify with Storage"
3. Enters storage credentials:
   - **R2**: account_id, access_key, secret_key, bucket_name
   - **Google**: credentials_json, bucket_name
4. Semptify tests: write → read → delete test file
5. Success → user gets session token, is "qualified"
6. All user data stays in THEIR bucket
7. Semptify uses their credentials to read/write on their behalf

## Benefits
- **Zero user data in Semptify** - no emails, passwords, profiles
- **User owns their data** - it's in their bucket, not ours
- **Portable** - user can switch Semptify instances, keeps data
- **Scalable** - no user database to manage
- **Secure** - storage provider handles identity/auth

## Endpoints

### POST /storage/qualify
Test storage credentials and grant qualification.

**R2 Request:**
```json
{
  "provider": "r2",
  "account_id": "abc123",
  "access_key": "...",
  "secret_key": "...",
  "bucket_name": "my-semptify-data"
}
```

**Google Request:**
```json
{
  "provider": "google",
  "credentials_json": {...},
  "bucket_name": "my-semptify-data"
}
```

**Response (success):**
```json
{
  "qualified": true,
  "provider": "r2",
  "bucket": "my-semptify-data",
  "session_token": "...",
  "message": "Storage verified - you are qualified!"
}
```

### GET /storage/status
Check if current session is qualified.

### POST /storage/logout
Clear qualification session.

## Usage in Routes

```python
from storage_qualification import require_storage_qualification

@app.route('/vault')
@require_storage_qualification
def vault():
    # User must be storage-qualified to access
    bucket = session['bucket_name']
    creds = session['storage_creds']
    # ... use their credentials to access their bucket
```

## Security Notes
- Credentials stored in Flask session (encrypted with FLASK_SECRET_KEY)
- Session cookie httponly, secure in production
- Test file immediately deleted after verification
- No credentials logged or persisted to disk

## Migration from Old System
- Remove: user_database.py, /register, /login routes
- Keep: Anonymous sessions for non-qualified browsing
- Add: Storage qualification UI on homepage

---
Generated: 2025-11-15
Status: Implemented in storage_qualification.py
