# USER FLOW ANALYSIS: OAuth to Vault

## Current Broken Flow

1. User visits /setup
2. Clicks 'Connect Google Drive' or 'Connect Dropbox'
3. OAuth redirects to provider
4. User authorizes
5. Callback returns to /oauth/google/callback or /oauth/dropbox/callback
6. **Callback creates user_token BUT...**
7. Redirects to /welcome with token
8. User clicks 'Go to Vault'
9. **LOOPS BACK TO /setup** ❌

## Why It Fails

### Problem 1: No Clear Exit Strategy
- welcome.html shows token but doesn't persist it
- User expected to manually copy/paste token?
- No automatic login after OAuth
- No 'remember me' mechanism

### Problem 2: Token Storage Confusion
- Token saved to cloud storage (auth_token.enc)
- Token hash saved to security/users.json (ephemeral!)
- Session has credentials but no user_id
- Middleware can't authenticate without session

### Problem 3: Session Not Persisting
- Missing FLASK_SECRET_KEY means session dies
- Callback sets session['drive_credentials']
- Next request has empty session
- Middleware redirects to /setup

## Root Cause
**No persistent user session + No cookie-based authentication**

