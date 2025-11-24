# 🔐 SEMPTIFY UNIFIED IDENTITY & SECURITY SYSTEM
Complete Technical Reference

---

## 🎯 OVERVIEW

Semptify uses a **privacy-first, token-based identity system** with NO passwords or personal data required.

---

## 1️⃣ USER ID SYSTEM (5 Layers)

### Layer 1: Database User ID
- **Format:** Integer (1, 2, 3...)
- **Usage:** Internal references only
- **Privacy:** Never exposed to user

### Layer 2: User Token (Primary Identity)
- **Format:** 12-digit numeric (e.g., 847392056184)
- **Generation:** secrets.randbelow(10**12)
- **Storage:** SHA-256 hash in security/users.json
- **Usage:** User authentication, vault access

### Layer 3: Document ID
- **Format:** doc_<timestamp>_<random>
- **Usage:** Track individual uploaded files

### Layer 4: Session ID  
- **Format:** Flask session UUID
- **Lifetime:** Browser session or 30 days (remember me)

### Layer 5: Request ID
- **Format:** UUID v4
- **Usage:** Log correlation, tracing
- **Header:** X-Request-Id

---

## 2️⃣ TOKEN SYSTEM

### User Tokens
- **Purpose:** Anonymous tenant auth
- **Format:** 12 digits (000000000000-999999999999)
- **Hashing:** SHA-256
- **File:** security/users.json
- **Validation:** validate_user_token() from security.py
- **Lifetime:** Permanent

**Example:**
```
User token: 847392056184
Hash stored: 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
```

### Admin Tokens
- **Purpose:** System management
- **Format:** 32+ char random string
- **Generation:** python create_admin_token.py
- **Hashing:** SHA-256
- **File:** security/admin_tokens.json
- **Features:** Multi-token, rotation, break-glass

**Multi-Token Format:**
```json
[
  {"id": "admin_001", "hash": "sha256...", "created": "2025-11-23"},
  {"id": "admin_002", "hash": "sha256...", "breakglass": true}
]
```

### CSRF Tokens
- **Purpose:** Form protection
- **Format:** 32-char hex
- **Storage:** Flask session
- **Required:** All POST forms in enforced mode

### Remember Tokens
- **Purpose:** Persistent sessions
- **Format:** 32-char random
- **Storage:** remember_tokens table (SQLite)
- **Lifetime:** 30 days

---

## 3️⃣ SECURITY SYSTEM (security.py)

### Components
1. Token Validation (user + admin)
2. CSRF Protection
3. Rate Limiting (sliding window)
4. Metrics Collection (Prometheus)
5. Audit Logging

### Security Modes

**open** (Development):
- Admin routes accessible without tokens
- CSRF disabled
- Lenient rate limits
- For testing only

**enforced** (Production):
- Admin tokens required
- CSRF on all POSTs
- Strict rate limiting
- Break-glass available

### Rate Limiting
```
ADMIN_RATE_WINDOW=300  # 5 minutes
ADMIN_RATE_MAX=10      # 10 requests per window
```

### Metrics
**GET /metrics** - Prometheus format
**GET /readyz** - Health check

---

## 4️⃣ USER REGISTRATION (adaptive_registration.py)

### Flow

**Step 1: GET /register**
- Show registration form
- Optional: email, storage provider
- Generate CSRF token

**Step 2: POST /register**
- Generate 12-digit token
- Hash with SHA-256
- Create user in database
- Store hash in security/users.json

**Step 3: /register_success**
- Display token ONCE
- User must save it
- Cannot be recovered

### Code
```python
# Generate token
user_token = str(secrets.randbelow(10**12)).zfill(12)
token_hash = hashlib.sha256(user_token.encode()).hexdigest()

# Create user
user_id = create_user(email=None, token_hash=token_hash)

# Store hash
users[f"user_{user_id}"] = {"hash": token_hash, "created": "2025-11-23"}
```

### Database
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password_hash TEXT,  -- Always NULL
    created_at TEXT NOT NULL
);
```

### No PII Required
- Email: Optional
- Password: Never collected
- Name: Not stored
- Phone: Not stored

---

## 5️⃣ ADMIN SIGNUP

No separate signup - use admin token creation:

```powershell
python create_admin_token.py
```

Output:
```
Admin Token: a3f9e2b8d1c4567890abcdef12345678
SAVE THIS - Cannot be recovered!
```

### Admin Access
```
# Query param
GET /admin/dashboard?admin_token=a3f9e2...

# Header
X-Admin-Token: a3f9e2b8...

# Form field
admin_token=a3f9e2b8...
```

---

## 6️⃣ STORAGE SYSTEM (storage_manager.py)

### Backends
1. **Local** (default) - uploads/ directory
2. **Cloudflare R2** - S3-compatible
3. **Google Drive** - OAuth-based

### Configuration
```bash
STORAGE_BACKEND=local  # or r2, google
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
GOOGLE_CREDENTIALS_PATH=...
```

### API
```python
from storage_manager import get_storage_backend

storage = get_storage_backend()
storage.upload(file_path, destination)
storage.download(remote_path, local_path)
files = storage.list_files(prefix="vault/")
storage.delete(remote_path)
```

### Document Certification
Every upload gets a JSON certificate:
```json
{
  "document_id": "doc_20251123_a3f9e2",
  "sha256": "7f83b1...",
  "filename": "lease.pdf",
  "user_id": 42,
  "uploaded_at": "2025-11-23T14:30:00"
}
```

---

## 7️⃣ AUTHENTICATION FLOWS

### User Registration
```
Browser → GET /register
       ← Registration form

Browser → POST /register
       ← Generate 12-digit token
       ← Create user in database
       ← Store hash in security/users.json
       ← Show token ONCE

Browser → Save token manually
       → GET /vault?user_token=847392056184
```

### Vault Access
```
Browser → GET /vault?user_token=847392056184

security.py → validate_user_token()
           → Hash token
           → Compare to stored
           → Return user_id if valid

Vault Page ← Show user documents
```

### Admin Access
```
Admin → GET /admin?admin_token=a3f9e2...

security.py → validate_admin_token()
           → Check SECURITY_MODE
           → Hash token
           → Check rate limit
           → Allow if valid

Admin Dashboard ← Show metrics, config
```

---

## 8️⃣ SECURITY BEST PRACTICES

### DO ✅
- Store only SHA-256 hashes
- Use secrets module for generation
- Display tokens ONCE
- Use HTTPS (FORCE_HTTPS=1)
- Rotate admin tokens

### DON'T ❌
- Log plaintext tokens
- Send tokens in URLs (use headers)
- Reuse tokens
- Store in JavaScript/localStorage

### Rate Limiting
```python
if not check_rate_limit(f"admin:{request.remote_addr}:/admin"):
    return jsonify({"error": "Rate limit"}), 429
```

### CSRF
```html
<form method="POST">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
</form>
```

### Audit Logging
```json
{
  "event": "user_login",
  "user_id": "user_42",
  "ip": "192.168.1.100",
  "success": true
}
```

---

## 🔟 QUICK REFERENCE

### Key Files
- security.py - All auth logic
- adaptive_registration.py - User signup
- user_database.py - SQLite database
- storage_manager.py - Unified storage
- security/users.json - User token hashes
- security/admin_tokens.json - Admin token hashes

### Environment Variables
```bash
SECURITY_MODE=enforced
FLASK_SECRET_KEY=<random>
STORAGE_BACKEND=local
ADMIN_RATE_WINDOW=300
ADMIN_RATE_MAX=10
FORCE_HTTPS=1
```

### Token Formats
- **User:** 12 digits (847392056184)
- **Admin:** 32+ chars (a3f9e2b8d1c4567890abcdef12345678)
- **CSRF:** 32-char hex
- **Remember:** 32-char random

---

**END OF REFERENCE**
