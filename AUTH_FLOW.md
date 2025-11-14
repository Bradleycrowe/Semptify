# USER REGISTRATION & LOGIN FLOW
# ================================

## NEW USER REGISTRATION FLOW:
1. Visit / (homepage) → Shows welcome page with "Get Started" button
2. Click "Get Started" → /register
3. Fill form (name, email, address) → POST /register
4. System generates:
   - user_id (random token)
   - 6-digit verification code
5. Email sent with code → /verify?user_id=xxx
6. Enter code → POST /verify
7. ✅ User verified → session['user_id'] set → Redirect to /dashboard

## RETURNING USER LOGIN FLOW (WITH REMEMBER ME):
1. Visit / (homepage)
2. Check for "remember_me" cookie:
   - ✅ Cookie exists & valid → Auto-login → session['user_id'] set → /dashboard
   - ❌ No cookie or expired → Show welcome page with "Sign In" button
3. Click "Sign In" → /login
4. Enter email → POST /login
5. System generates 6-digit code → Email sent → /verify?user_id=xxx
6. Enter code + check "Remember Me" box → POST /verify
7. ✅ Verified:
   - session['user_id'] set
   - If "Remember Me" checked: Create 30-day remember_token → Set cookie
   - Redirect to /dashboard

## LOGOUT FLOW:
1. /logout → Delete remember_me cookie → Clear session → Redirect to /

## SESSION vs REMEMBER TOKEN:
- **session['user_id']**: Temporary (browser session only, ~1 hour)
- **remember_me cookie**: Persistent (30 days, survives browser close)

## DATABASE TABLES:
- users: Stores user_id, email, name, address (permanent)
- pending_users: Temporary verification codes (expires in 10 min)
- remember_tokens: Persistent login tokens (expires in 30 days)

