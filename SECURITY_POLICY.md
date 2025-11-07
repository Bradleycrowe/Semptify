# 🔒 Semptify Security & Access Control Policy

## Core Principle: Tenant Privacy is Paramount

Semptify is a **tenant's sidekick**, not a landlord's tool. User privacy and document security are the highest priority.

---

## Access Control Matrix

| Resource | Document Owner | Admin (MASTER_KEY) | Other Users |
|----------|----------------|---------------------|-------------|
| **Own Vault** | ✅ Full Access | ❌ NO ACCESS | ❌ NO ACCESS |
| **Own Documents** | ✅ Full Access | ❌ NO ACCESS | ⏳ Only if granted |
| **Calendar Events** | ✅ Full Access | ✅ View Only (all events) | ❌ NO ACCESS |
| **Admin Settings** | ❌ NO ACCESS | ✅ Full Access | ❌ NO ACCESS |
| **User List** | ❌ NO ACCESS | ✅ Full Access | ❌ NO ACCESS |
| **System Logs** | ❌ NO ACCESS | ✅ Full Access | ❌ NO ACCESS |

---

## Vault Security Rules

### 1. Document Owner Controls Access
```
✅ CORRECT: Only user with valid user_token can access their vault
❌ WRONG: Admin can view all vaults
```

**Code enforcement:**
```python
# vault.py line 81
uid = validate_user_token(token)
if not uid:
    return jsonify({"error": "unauthorized"}), 401
# Admin token does NOT work here - only user token
```

### 2. Admin Master Key Limitations
```
✅ Admin can: Configure settings, view logs, manage system
❌ Admin cannot: Access user vaults, read user documents, bypass vault security
```

**Rationale:** Semptify helps tenants against landlords. Admin access to vaults would violate tenant trust.

### 3. Sharing (Future Feature)
```
⏳ User can grant temporary access to specific documents
⏳ Share tokens expire after set time
⏳ User can revoke access anytime
```

---

## User Registration & Identity

### Registration Fields (Required)
- ✅ First Name
- ✅ Last Name
- ✅ Street Address
- ✅ County
- ✅ City
- ✅ State (dropdown)
- ✅ ZIP Code
- ✅ Phone Number (10 digits, formatted: (555) 555-5555)
- ✅ Email Address

### User Token
- Generated at registration: 12-digit anonymous number
- Example: `824691357203`
- Used for all vault operations
- Never shared with admin

### User ID vs User Token
```
user_id: Internal identifier (UUID)
user_token: 12-digit number user sees and uses
```

**Important:** Both are private. Admin sees user_id for system management, but CANNOT use it to access vault.

---

## Storage Architecture

### Document ID Storage (Correct ✅)
```
vault/
  doc_abc123/           ← Document ID
    lease.pdf
    lease.pdf.cert.json
  doc_xyz789/
    witness_statement.pdf
    witness_statement.pdf.cert.json
```

### User ID Storage (Wrong ❌)
```
vault/
  user_12345/           ← Mixes all documents together
    doc1.pdf
    doc2.pdf
    doc3.pdf
```

**Why Document ID?**
- Each document independent
- Can grant access per-document (future)
- Easier to manage certificates
- Better for legal evidence chain

---

## Token Types & Uses

### 1. User Token (Vault Access)
```python
# Generated at registration
token = '824691357203'  # 12 digits

# Used for vault operations
GET /vault?user_token=824691357203
POST /vault/upload with X-User-Token: 824691357203
```

### 2. Admin Token (System Access)
```python
# Set in Render environment
ADMIN_TOKEN = 'SbNw7uld3MQTrVgayjhBez06YmpIqWxn'

# Used for admin operations
POST /admin/settings with X-Admin-Token: <token>
```

### 3. Master Key (Superadmin)
```python
# Set in Render environment
MASTER_KEY = '<your-secure-master-key>'

# Admin access everywhere (except vault!)
POST /admin/* with X-Admin-Token: <master_key>
GET /api/calendar/all with X-Admin-Token: <master_key>

# Still CANNOT access vault
GET /vault?user_token=<master_key>  # ❌ FAILS - need real user token
```

---

## Calendar Access Rules

### User's Own Events
```python
# User can CRUD their own calendar events
GET /api/calendar?user_token=<token>          # View own events
POST /api/calendar?user_token=<token>         # Create event
PUT /api/calendar/<id>?user_token=<token>     # Update own event
DELETE /api/calendar/<id>?user_token=<token>  # Delete own event
```

### Admin View (All Events)
```python
# Admin can view all events (for system overview)
GET /api/calendar/all with X-Admin-Token: <master_key>

# But admin CANNOT modify user events
PUT /api/calendar/<id> with X-Admin-Token: <token>  # ❌ FAILS
# Rationale: User controls their own schedule
```

---

## Rate Limiting

### Registration (Prevent Spam)
```
IP-based: 5 registrations per hour per IP
Prevents: Automated account creation
```

### Admin Actions (Prevent Abuse)
```
Token-based: 100 actions per hour per admin token
Prevents: Compromised admin token abuse
```

### Vault Operations (Prevent DoS)
```
User-based: 1000 uploads per day per user
Prevents: Storage abuse
```

---

## Security Best Practices

### Environment Variables (Render)
```bash
# Required for all deployments
FLASK_SECRET=<64-char-random>        # Session security
ADMIN_TOKEN=<32-char-random>         # Admin access
MASTER_KEY=<32-char-random>          # Superadmin access
SECURITY_MODE=enforced               # Enable all security

# Optional but recommended
FORCE_HTTPS=1                        # Redirect HTTP → HTTPS
ADMIN_RATE_WINDOW=3600              # 1 hour rate limit window
ADMIN_RATE_MAX=100                   # 100 actions per window
```

### Never Commit Secrets
```bash
# ❌ NEVER commit these files:
security/admin_tokens.json
security/users.json
security/*.flag
.env
config.env

# ✅ Use .gitignore
```

### Token Rotation
```bash
# Rotate admin tokens quarterly
python create_admin_token.py

# Rotate master key annually
# Update MASTER_KEY in Render environment
```

---

## Audit Trail

### Events Logged
```json
{
  "timestamp": "2025-11-07T12:34:56Z",
  "type": "vault_upload",
  "details": {
    "user_id": "uuid-here",
    "filename": "lease.pdf",
    "sha256": "abc123...",
    "request_id": "req-xyz"
  }
}
```

### What's Tracked
- ✅ Vault uploads/downloads
- ✅ Admin actions (master key usage)
- ✅ Failed authentication attempts
- ✅ Rate limit violations
- ✅ User registrations
- ✅ Calendar event changes

### What's NOT Tracked
- ❌ Document contents (privacy)
- ❌ User personal info (GDPR)
- ❌ IP addresses (unless rate limiting)

---

## Compliance & Privacy

### GDPR Considerations
- User can request data deletion
- Minimal data collection
- No sharing with third parties
- Audit trail for accountability

### Legal Evidence Chain
- SHA-256 hash of every document
- Timestamp certificates
- Attestation support (witness signatures)
- Immutable audit logs

---

## Summary: The Golden Rules

1. **🔐 Vault = User's Private Space**
   - Only user token grants access
   - Admin master key does NOT work
   - No backdoors, no exceptions

2. **👔 Admin = System Manager**
   - Configure settings
   - View system health
   - Manage user accounts
   - But CANNOT access user vaults

3. **📄 Document ID Storage**
   - Each document independent
   - Stored by doc ID, not user ID
   - Enables granular access control

4. **🎯 Tenant-First Design**
   - Semptify is the tenant's sidekick
   - Privacy over convenience
   - Transparency in security

---

**Questions?** Check the code:
- `security.py` - Token validation
- `vault.py` - Vault access control
- `calendar_api.py` - Calendar permissions
- `modules/register/register_bp.py` - User registration
