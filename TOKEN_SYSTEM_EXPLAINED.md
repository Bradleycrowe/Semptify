# 🔐 Token System Explained: User IDs, Tokens & Document IDs

Complete guide to how tokens, user IDs, and document IDs work together in Semptify.

---

## 📊 The Three Core Concepts

### 1️⃣ USER ID (Example: `u4a7c9d2b`)
**What it is:** Unique identifier for a registered user
**Format:** `u` + 8 random hex characters
**Generated:** When user registers (`/register`)
**Stored in:** `security/users.json` file
**Lifespan:** Permanent (stored in database)

### 2️⃣ USER TOKEN (Example: `tB2xJ9nK3vL-pQ`)
**What it is:** Secret password/passphrase for the user
**Format:** URL-safe random string (about 12 characters)
**Generated:** At same time as user ID
**Stored in:** `security/users.json` (as SHA-256 hash)
**Lifespan:** Permanent (never expires)

### 3️⃣ DOCUMENT ID (Example: `passport.pdf` or `birth_certificate.pdf`)
**What it is:** Filename of a document user uploads
**Format:** Any filename (sanitized)
**Generated:** When user uploads file to vault
**Stored in:** Filename in `uploads/vault/{user_id}/` folder
**Lifespan:** Until deleted by user or admin

---

## 🔄 How They Work Together

### Phase 1: Registration (User Signs Up)

```
User goes to /register
         ↓
Submits registration form (no password needed!)
         ↓
system generates:
  - USER ID:        u4a7c9d2b
  - USER TOKEN:     tB2xJ9nK3vL-pQ
         ↓
Stores in security/users.json:
  {
    "id": "u4a7c9d2b",
    "hash": "sha256:<hash_of_token>",
    "created": 1730688000,
    "enabled": true
  }
         ↓
User sees one-time token: tB2xJ9nK3vL-pQ
User writes it down (or saves it)
```

**Result:**
- User ID stored permanently
- Token stored as secure hash
- User has one-time token to access vault

---

### Phase 2: Vault Access (User Uploads Document)

```
User opens vault page with token
  URL: /vault?user_token=tB2xJ9nK3vL-pQ
         ↓
System validates token:
  1. Takes token: tB2xJ9nK3vL-pQ
  2. Hashes it: sha256(<hash>)
  3. Looks up in security/users.json
  4. Finds matching entry
  5. Extracts user ID: u4a7c9d2b
         ↓
Vault unlocked! User can upload files
         ↓
User uploads file: passport.pdf
  - FILE: passport.pdf
  - USER: u4a7c9d2b
         ↓
System stores in:
  uploads/vault/u4a7c9d2b/passport.pdf
         ↓
System creates certificate:
  uploads/vault/u4a7c9d2b/passport.pdf.cert.json
  {
    "filename": "passport.pdf",
    "sha256": "<hash_of_file>",
    "user_id": "u4a7c9d2b",
    "created": "2025-11-04T12:34:56.789Z",
    "request_id": "abc123def456",
    "attestations": []
  }
```

**Result:**
- Document uploaded to user's folder
- Certificate created with SHA-256 hash
- Event logged for audit trail

---

### Phase 3: Event Logging (Audit Trail)

```
When user uploads, system logs:

log_event(
  event_type="vault.upload",
  user_id="u4a7c9d2b",      ← Links to user
  doc_id="passport.pdf",     ← Links to document
  extra={"sha256": "..."}
)

Stored in logs/events.log:
{
  "ts": "2025-11-04T12:34:56.789+00:00",
  "event": "vault.upload",
  "user_id": "u4a7c9d2b",
  "doc_id": "passport.pdf",
  "extra": {"sha256": "abcd1234..."}
}
```

**Result:**
- Complete audit trail
- Can trace: WHO (user_id) + WHAT (doc_id) + WHEN (ts)
- Proof of document upload

---

## 🗂️ File Structure Hierarchy

```
security/
├── users.json          ← All user IDs + hashed tokens
├── admin_tokens.json   ← Admin tokens (not covered here)
└── breakglass.flag     ← Emergency access flag

uploads/
└── vault/
    └── {user_id}/              ← Creates folder per user
        ├── passport.pdf        ← User's document 1
        ├── passport.pdf.cert.json   ← Certificate for document 1
        ├── birth_cert.pdf      ← User's document 2
        └── birth_cert.pdf.cert.json ← Certificate for document 2

logs/
└── events.log          ← All user/doc/admin actions logged here
```

---

## 🔍 Detailed Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEMPTIFY TOKEN SYSTEM                         │
└─────────────────────────────────────────────────────────────────┘

STEP 1: USER REGISTRATION
┌──────────────────────────┐
│ User visits /register    │
│ Clicks "Register"        │
└──────────────┬───────────┘
               ↓
    ┌──────────────────────────┐
    │ System generates:        │
    │ - USER_ID: u4a7c9d2b    │
    │ - TOKEN:   tB2xJ9nK3vL  │
    └──────────────┬───────────┘
                   ↓
    ┌──────────────────────────────────────┐
    │ Save to security/users.json:         │
    │ {                                    │
    │   "id": "u4a7c9d2b",                │
    │   "hash": "sha256:...",             │
    │   "created": 1730688000,            │
    │   "enabled": true                   │
    │ }                                    │
    └──────────────┬───────────────────────┘
                   ↓
    ┌──────────────────────────────────────┐
    │ Display to user (ONE TIME):          │
    │ "Your token: tB2xJ9nK3vL-pQ"        │
    │ Save this somewhere safe!            │
    └──────────────────────────────────────┘

STEP 2: VAULT ACCESS (with token)
┌──────────────────────────────────────┐
│ User provides token:                  │
│ /vault?user_token=tB2xJ9nK3vL-pQ   │
└──────────────┬───────────────────────┘
               ↓
    ┌────────────────────────────────────┐
    │ validate_user_token(token):        │
    │ 1. Hash token: sha256(token)      │
    │ 2. Load security/users.json       │
    │ 3. Compare hash with stored hash  │
    │ 4. If match → return user_id     │
    └──────────────┬────────────────────┘
                   ↓
    ┌────────────────────────────────────┐
    │ Found! user_id = u4a7c9d2b       │
    │ Vault is now unlocked             │
    └──────────────┬────────────────────┘
                   ↓
    ┌────────────────────────────────────┐
    │ User can now upload documents      │
    │ Example: passport.pdf             │
    └────────────────────────────────────┘

STEP 3: DOCUMENT UPLOAD & CERTIFICATE
┌──────────────────────────────────────┐
│ User uploads: passport.pdf           │
│ User ID: u4a7c9d2b                 │
└──────────────┬───────────────────────┘
               ↓
    ┌────────────────────────────────────────────┐
    │ System saves file:                         │
    │ uploads/vault/u4a7c9d2b/passport.pdf     │
    └──────────────┬─────────────────────────────┘
                   ↓
    ┌────────────────────────────────────────────────┐
    │ Calculate file hash (SHA-256)                  │
    │ Create certificate:                            │
    │ {                                              │
    │   "filename": "passport.pdf",                 │
    │   "sha256": "a1b2c3d4e5f6...",               │
    │   "user_id": "u4a7c9d2b",                    │
    │   "created": "2025-11-04T12:34:56.789Z",    │
    │   "request_id": "abc123def456",              │
    │   "attestations": []                         │
    │ }                                              │
    │ Save as: uploads/vault/u4a7c9d2b/passport.pdf.cert.json
    └──────────────┬─────────────────────────────────┘
                   ↓
    ┌────────────────────────────────────────────┐
    │ Log event to events.log:                    │
    │ {                                           │
    │   "ts": "2025-11-04T12:34:56.789+00:00",  │
    │   "event": "vault.upload",                 │
    │   "user_id": "u4a7c9d2b",  ← WHO          │
    │   "doc_id": "passport.pdf", ← WHAT        │
    │   "extra": {                               │
    │     "sha256": "a1b2c3d4e5f6..."           │
    │   }                                         │
    │ }                                           │
    └────────────────────────────────────────────┘

RESULT: Complete audit trail established
```

---

## 💾 Example: Complete Data Journey

### Timeline of One User Upload

**Time 1: User Registers (Nov 4, 2:00 PM)**

```
POST /register
↓
Generated:
  user_id = "u4a7c9d2b"
  token = "tB2xJ9nK3vL-pQ"
↓
Stored in security/users.json:
[
  {
    "id": "u4a7c9d2b",
    "hash": "sha256:a1b2c3d4e5f6g7h8i9j0...",
    "created": 1730688000,
    "enabled": true
  }
]
```

**Time 2: User Uploads Document (Nov 4, 2:15 PM)**

```
POST /vault/upload
  token: "tB2xJ9nK3vL-pQ"  (provided by user)
  file: passport.pdf
↓
System validates token → finds user_id "u4a7c9d2b"
↓
File saved to: uploads/vault/u4a7c9d2b/passport.pdf
↓
Certificate created:
{
  "filename": "passport.pdf",
  "sha256": "deadbeefcafebabe123456789...",
  "user_id": "u4a7c9d2b",
  "created": "2025-11-04T14:15:30.123Z",
  "request_id": "req-789abc123",
  "attestations": []
}
Saved to: uploads/vault/u4a7c9d2b/passport.pdf.cert.json
↓
Event logged to logs/events.log:
{
  "ts": "2025-11-04T14:15:30.123+00:00",
  "event": "vault.upload",
  "user_id": "u4a7c9d2b",
  "doc_id": "passport.pdf",
  "extra": {
    "sha256": "deadbeefcafebabe123456789..."
  }
}
```

**Later: Admin Reviews Audit Trail**

```
Admin checks logs/events.log
Finds entry:
{
  "ts": "2025-11-04T14:15:30.123+00:00",
  "event": "vault.upload",
  "user_id": "u4a7c9d2b",    ← Can link to specific user
  "doc_id": "passport.pdf",   ← Can verify specific document
  "extra": {...}
}

Can verify:
✅ WHO uploaded: u4a7c9d2b (specific user)
✅ WHAT was uploaded: passport.pdf (specific document)
✅ WHEN: Nov 4 at 2:15:30 PM
✅ PROOF: SHA-256 hash of file
```

---

## 🔑 Key Relationships

### User ID Links

```
User ID: u4a7c9d2b

├── Stored in: security/users.json
│   └── With: hash of token, creation time, enabled flag
│
├── File folder: uploads/vault/u4a7c9d2b/
│   └── Contains: All user's documents + certificates
│
└── Event logs: logs/events.log
    └── Referenced: In all "vault.upload" events as user_id
```

### Document ID Links

```
Document ID: passport.pdf

├── Physical file: uploads/vault/u4a7c9d2b/passport.pdf
│
├── Certificate: uploads/vault/u4a7c9d2b/passport.pdf.cert.json
│   └── Contains: SHA-256, user_id, timestamp, request_id
│
└── Event log: logs/events.log
    └── Referenced: As doc_id in "vault.upload" event
```

### Token Links

```
Token (plain): tB2xJ9nK3vL-pQ

├── Plain text: User receives once (one-time)
│   └── User stores securely
│
├── Hashed: SHA-256 stored in security/users.json
│   └── Never stored in plain text
│
└── Validation: When user provides token
    └── System hashes it and compares to stored hash
    └── If match → retrieves user_id
    └── User ID unlocks their vault folder
```

---

## 🔐 Security Features

### 1. Tokens Never Stored in Plain Text
```
✅ User gets: "tB2xJ9nK3vL-pQ"
✅ System stores: SHA-256 hash only
❌ If database leaked: hashes are useless
```

### 2. Unique User IDs
```
✅ Each user gets unique ID: u4a7c9d2b
✅ IDs don't reveal personal info
✅ Can't guess another user's ID
```

### 3. Document Hashes
```
✅ Each document gets SHA-256 hash
✅ Proof of document integrity
✅ Can detect if file was tampered with
```

### 4. Event Logging
```
✅ All actions logged with timestamp
✅ Links user_id to doc_id to time
✅ Complete audit trail for compliance
```

---

## 📝 Common Questions

### Q: Can I use my token multiple times?
**A:** Yes! Token never expires. Save it somewhere safe. You can use it anytime to access your vault.

### Q: What if I lose my token?
**A:** Token is permanent. If lost, admin would need to delete your account and you'd need to register again. Store it safely (password manager, written down, etc).

### Q: Can someone guess my user ID?
**A:** Very unlikely. User IDs are random hex strings: `u` + 8 random characters = billions of possibilities. Even if they guessed the ID, they'd also need the token.

### Q: What's the certificate file for?
**A:** Proof that document was uploaded by you. Contains:
- Your user_id
- File hash (SHA-256)
- When it was uploaded
- Unique request ID
- Space for future attestations (signatures, etc)

### Q: Can I see who uploaded a document?
**A:** Admin can:
1. Look at events.log
2. Find entry with doc_id
3. See user_id who uploaded it
4. See exact timestamp
5. See SHA-256 hash for verification

### Q: What if two users upload files with same name?
**A:** No problem! Files stored in separate folders:
- User 1: `uploads/vault/u4a7c9d2b/passport.pdf`
- User 2: `uploads/vault/u9x8w7v6u5t/passport.pdf`

Different folders = no conflict.

---

## 🎯 Summary Table

| Item | User ID | Token | Document ID |
|------|---------|-------|-------------|
| **Format** | `u` + 8 hex | URL-safe string | Filename |
| **Generated** | At registration | At registration | At upload |
| **Stored As** | Plain text (ID) | SHA-256 hash | Filename |
| **Stored In** | security/users.json | security/users.json | uploads/vault/{user_id}/ |
| **Lifespan** | Permanent | Never expires | Until deleted |
| **Logged In** | events.log (user_id) | Never logged | events.log (doc_id) |
| **Uniqueness** | One per user | One per user | One per file per user |
| **Reveals Info** | No (random) | No (hashed) | Yes (filename visible) |
| **What It Does** | Identifies user | Unlocks vault | Identifies document |

---

## 🔗 Connection Points in Code

### Registration (register.py)
```python
token = save_user_token()  # Generates user_id + token
# Returns: user_id, plain_token
```

### Vault Access (vault.py)
```python
token = get_token_from_request(request)  # Gets token from user
uid = validate_user_token(token)        # Hashes and validates token
                                        # Returns: user_id
```

### Event Logging (security.py)
```python
log_event(
  event_type="vault.upload",
  user_id=uid,           # Links event to user
  doc_id=filename,       # Links event to document
  extra={"sha256": sha}  # Extra proof data
)
```

### Certificate Creation (vault.py)
```python
cert = {
    "filename": filename,
    "sha256": sha,
    "user_id": uid,      # Links cert to user
    "created": datetime.utcnow().isoformat(),
    "request_id": str(uuid.uuid4()),
    "attestations": [],
}
# Saved as: uploads/vault/{uid}/{filename}.cert.json
```

---

## ✨ The Complete Picture

When a user registers and uploads a document:

```
1. REGISTRATION
   └─ Creates: user_id (u4a7c9d2b) + token (tB2xJ9nK3vL-pQ)
   └─ Stores: In security/users.json

2. VAULT ACCESS
   └─ User provides: token (tB2xJ9nK3vL-pQ)
   └─ System validates: Hashes token, matches with stored hash
   └─ Result: Retrieves user_id (u4a7c9d2b)
   └─ Creates: Folder uploads/vault/u4a7c9d2b/

3. DOCUMENT UPLOAD
   └─ User uploads: passport.pdf
   └─ System saves: uploads/vault/u4a7c9d2b/passport.pdf
   └─ Calculates: SHA-256 hash of file
   └─ Creates: Certificate with user_id + filename + hash
   └─ Saves: uploads/vault/u4a7c9d2b/passport.pdf.cert.json

4. AUDIT LOG
   └─ Event created: user_id + doc_id + timestamp + hash
   └─ Logged to: logs/events.log
   └─ Result: Complete audit trail of WHO uploaded WHAT and WHEN

ALL LINKED BY:
- user_id (u4a7c9d2b) links all user's documents
- doc_id (passport.pdf) links to specific document
- timestamp links to when action happened
- SHA-256 links to file integrity
```

---

**Your Semptify system is now fully explained!** 🎉
