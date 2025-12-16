p# SEMPTIFY STORAGE & AUTHENTICATION RESEARCH SUMMARY
**Date:** November 27, 2025
**Purpose:** Comprehensive documentation of current user storage, OAuth, and authentication patterns

═══════════════════════════════════════════════════════════════════════════════════════

## CORE AUTHENTICATION MODEL

### THE "NO SIGN IN/UP" PATTERN:

**Registration Flow (Token-First):**
1. User visits /register
2. Fills form (name, email optional, address)
3. System generates **12-digit anonymous token** (digits only)
4. Token displayed ONE TIME (cannot be recovered)
5. Token hash stored in security/users.json (SHA-256)
6. User bookmarks: /vault?user_token=123456789012

**Key Principle: TOKEN = IDENTITY**
- No passwords
- No username/password database
- No email verification required
- No "forgot password" flow
- Token IS the authentication

═══════════════════════════════════════════════════════════════════════════════════════

## THREE-TIER STORAGE ARCHITECTURE

### 1. R2 STORAGE (Cloudflare)
**Purpose:** Persistent database + Admin storage ONLY

**Contains:**
- users.db (SQLite backup)
- Admin configurations
- System-level data

**Does NOT contain:**
- User documents (NO)
- User tokens (NO)
- Personal files (NO)

**Access:** Admin only

---

### 2. LOCAL STORAGE (Server-side)
**Purpose:** Runtime storage and token hashes

**Contains:**
- security/users.json - Token hashes (SHA-256)
- security/admin_tokens.json - Admin tokens
- logs/ - Application logs
- uploads/ - Temporary staging
- data/ - Learning patterns

**Who uses it:**
- Everyone (for authentication)
- Managers/Admins (for system operations)

---

### 3. USER STORAGE (OAuth2 Cloud)
**Purpose:** User-owned cloud storage for documents

**Supported Providers:**
- Dropbox (via OAuth2)
- Google Drive (via OAuth2)
- Local (fallback for development)

**Contains:**
- User documents (evidence, PDFs)
- Encrypted tokens (in .semptify folder)
- Timeline data
- Calendar events

**Privacy Model:**
- Users store in THEIR OWN clouds
- Semptify never stores user documents on servers
- Zero liability model (users own their data)

═══════════════════════════════════════════════════════════════════════════════════════

## COMPLETE AUTHENTICATION FLOW

### Step 1: Registration
GET /register → User fills form → POST /register
→ System generates 12-digit token
→ Token hash stored in security/users.json
→ Display token ONCE with warning
→ User saves token (write down, screenshot)

### Step 2: Storage Setup (Optional)
GET /setup-storage?user_token=847392016584
→ User chooses: Dropbox | Google Drive | Local
→ If cloud: OAuth2 authorization flow
→ App creates .semptify/ folder in users cloud
→ Encrypted token stored in .semptify/token.enc

### Step 3: Vault Access
GET /vault?user_token=847392016584
→ Validate token: Hash provided token, lookup in security/users.json
→ If valid: Load users documents from their storage
→ Display vault with upload/download capabilities

═══════════════════════════════════════════════════════════════════════════════════════

## DOCUMENT STORAGE ARCHITECTURE

**Storage by Document ID (Not User ID)**

Structure:
uploads/vault/
├── doc_a1b2c3d4e5f6/              (Document ID)
│   ├── lease_agreement.pdf
│   └── lease_agreement.pdf.cert.json
└── user_uuid-1234_docs.json       (User mapping)

**Why Document ID?**
- Each document is independent
- Can share specific documents (future)
- Clear ownership via certificate
- Better for legal evidence chain

═══════════════════════════════════════════════════════════════════════════════════════

## TOKEN STORAGE & ACCESS

### Token Hash Storage (security/users.json)
- Token NEVER stored in plain text
- Only SHA-256 hash stored
- Hash cannot be reversed
- Token shown ONCE during registration
- If lost, user must register again (by design)

### Token Access Methods:
1. Query parameter: ?user_token=123456789012
2. HTTP header: X-User-Token: 123456789012
3. Form field: <input name="user_token">

═══════════════════════════════════════════════════════════════════════════════════════

## OAUTH2 STORAGE BACKENDS

### Dropbox Integration
Environment Variables:
- DROPBOX_APP_KEY
- DROPBOX_APP_SECRET
- DROPBOX_REDIRECT_URI

OAuth Flow:
1. User clicks "Connect Dropbox"
2. Redirect to Dropbox OAuth URL
3. User grants permissions
4. Exchange code for access token
5. Create .semptify folder in users Dropbox
6. Store encrypted user token

### Google Drive Integration
Environment Variables:
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- GOOGLE_REDIRECT_URI

OAuth Flow: (Same as Dropbox but with Google)

═══════════════════════════════════════════════════════════════════════════════════════

## SECURITY ARCHITECTURE

### Dual-Mode Security (SECURITY_MODE)

**Open Mode (SECURITY_MODE=open):**
- Admin routes accessible without tokens
- Still logged and rate-limited
- Used in development/testing

**Enforced Mode (SECURITY_MODE=enforced):**
- Admin requires token validation
- CSRF on state-changing POSTs
- Production mode

### Admin vs User Tokens

**Admin Tokens:**
- Stored in security/admin_tokens.json
- SHA-256 hashed
- Multi-token support

**User Tokens:**
- Stored in security/users.json
- Anonymous 12-digit codes
- No recovery mechanism (by design)

═══════════════════════════════════════════════════════════════════════════════════════

## FILE STORAGE MATRIX

| File Type         | Storage Location        |
|-------------------|-------------------------|
| User documents    | Users Dropbox/Drive    |
| Token hashes      | Local (security/)       |
| Encrypted tokens  | Users cloud            |
| Database backup   | R2 (admin only)        |
| System logs       | Local (logs/)          |

═══════════════════════════════════════════════════════════════════════════════════════

## KEY DIFFERENCES FROM TRADITIONAL AUTH

### Traditional Auth:
- Username + password
- Email verification
- Forgot password flow
- Session cookies

### Semptify Auth:
- Anonymous 12-digit token
- No email required
- No password recovery (by design)
- Token = identity
- Minimal user database

### Why This Approach?
1. Privacy: No personally identifiable info required
2. Simplicity: No complex auth flows
3. Security: No passwords to leak
4. Portability: Token can be shared (with attorney)
5. Liability: Users control their own data

═══════════════════════════════════════════════════════════════════════════════════════

## VALIDATION CHECKLIST

### CORRECT in Current Architecture:
✅ Token-first authentication (no traditional signup)
✅ Anonymous 12-digit tokens
✅ SHA-256 hashing (never store plain tokens)
✅ Three-tier storage (R2, Local, User Cloud)
✅ OAuth2 for Dropbox/Drive
✅ Document ID storage (not user ID)
✅ Zero liability (users own their data)
✅ Privacy-first model
✅ One-time token display
✅ Bookmark-based access

### MISSING or PLANNED:
⏳ R2 as user-facing storage option
⏳ Document sharing via share tokens
⏳ Multi-device token sync

═══════════════════════════════════════════════════════════════════════════════════════

## IMPLEMENTATION FILES

### Core Authentication:
- security.py - Token validation, rate limiting
- security/users.json - Token hash storage
- user_database.py - SQLite user database

### Registration:
- adaptive_registration.py - Registration with location intelligence
- Semptify.py - /register endpoint

### Storage Setup:
- storage_setup_routes.py - OAuth2 flows for Dropbox/Drive
- storage_adapter.py - Abstraction for R2/Local storage

### Vault Access:
- vault.py or blueprints/vault_bp.py - Document management
- Routes: /vault, /vault/upload, /vault/download

═══════════════════════════════════════════════════════════════════════════════════════

## BOTTOM LINE

**Semptifys Authentication Model:**

Registration → Generate 12-digit token → Save token → Choose storage
              ↓
        Token = Identity
              ↓
        No passwords, no emails, no recovery
              ↓
        Documents in USERs cloud (Dropbox/Drive)
              ↓
        Semptify only stores token HASH
              ↓
        Zero liability, maximum privacy

**Storage Hierarchy:**
1. R2 → Database persistence (admin only)
2. Local → Token hashes + runtime (everyone)
3. User Clouds → Documents (user-owned via OAuth2)

**Key Principle:**
"Your documents. Your cloud. Your privacy. We just help organize."

═══════════════════════════════════════════════════════════════════════════════════════

**Research completed:** November 27, 2025
**Researched by:** GitHub Copilot (Claude Sonnet 4.5)
**Status:** READ-ONLY research (no changes made)
