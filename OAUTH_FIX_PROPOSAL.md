# PROPOSED FIX: Automatic Login After OAuth

## Current Flow (Broken)
1. OAuth callback → generates user_token
2. Saves to cloud storage
3. Redirects to /welcome?user_token=XXX
4. Welcome page shows token
5. User clicks 'Go to Vault'
6. **Middleware can't find credentials → redirect to /setup** ❌

## New Flow (Fixed)
1. OAuth callback → generates user_token
2. Saves to cloud storage
3. **Sets session cookie with credentials + user_token**
4. Redirects to /vault-ui (NOT /welcome)
5. Middleware finds session credentials
6. **User is in vault immediately** ✅

## Code Changes Needed

### 1. Fix google_oauth_callback (line ~221)
\\\python
# BEFORE:
print('[OAUTH][Google] Success folder_id=' + folder_id)
return redirect(f'/welcome?user_token={user_token}')

# AFTER:
# Keep session credentials for immediate access
session.permanent = True
session['user_token'] = user_token  # NEW: Store token in session
session['authenticated'] = True     # NEW: Mark as authenticated
print('[OAUTH][Google] Success folder_id=' + folder_id)
return redirect('/vault-ui')  # Direct to vault, not welcome
\\\

### 2. Fix dropbox_oauth_callback (similar change)
\\\python
# AFTER saving token and session data:
session.permanent = True
session['user_token'] = user_token
session['authenticated'] = True
return redirect('/vault-ui')
\\\

### 3. Update storage_autologin middleware
\\\python
# In _get_storage_client(), check session first:
if 'user_token' in session:
    # User already authenticated in this session
    g.user_token = session['user_token']
    g.authenticated = True
\\\

### 4. Optional: Keep /welcome for first-time users
- Show 'Setup Complete' message
- Explain what .semptify folder is
- Auto-redirect to vault after 3 seconds
- OR: Just skip welcome entirely

