# 📂 Document Storage Architecture

## Core Principle: Document ID Storage + User Token Access

**Storage Path**: Documents stored by **document ID** (not user ID)  
**Access Control**: Only users with valid **user token** can access their documents  
**Security**: Document ID is unencrypted (reference), but access requires authentication

---

## Storage Structure

```
uploads/vault/
├── doc_a1b2c3d4e5f6/              ← Document ID (unique per document)
│   ├── lease_agreement.pdf         ← Actual file
│   └── lease_agreement.pdf.cert.json  ← Certificate (hash, owner, timestamp)
├── doc_x7y8z9a0b1c2/
│   ├── witness_statement.pdf
│   └── witness_statement.pdf.cert.json
├── user_uuid-1234_docs.json       ← User's document mapping (private)
└── user_uuid-5678_docs.json       ← Another user's document mapping
```

---

## Why Document ID Instead of User ID?

### ❌ Old Approach (User ID Storage):
```
vault/user_12345/
  - lease.pdf
  - witness.pdf
  - receipt.pdf
```
**Problems:**
- All documents mixed in one folder
- Can't grant access to specific documents
- Hard to share individual documents
- Document ownership unclear

### ✅ New Approach (Document ID Storage):
```
vault/doc_abc123/lease.pdf
vault/doc_xyz789/witness.pdf
vault/doc_def456/receipt.pdf
```
**Benefits:**
- ✅ Each document independent
- ✅ Can share specific documents (future feature)
- ✅ Clear ownership via certificate
- ✅ Better for legal evidence chain
- ✅ Easier access control

---

## Access Control Flow

### 1. Upload Document
```
User → [POST /vault/upload with user_token]
  ↓
Validate user_token → Get user_id (uid)
  ↓
Generate doc_id = "doc_a1b2c3d4e5f6"
  ↓
Store file: vault/doc_a1b2c3d4e5f6/filename.pdf
  ↓
Create certificate with owner info
  ↓
Add to user's document mapping
  ↓
Return doc_id to user
```

**Key Points:**
- Document ID is **unique reference** (like a key)
- User token proves **ownership**
- Certificate stores **hash + owner + timestamp**

### 2. List Documents
```
User → [GET /vault/list with user_token]
  ↓
Validate user_token → Get user_id
  ↓
Read user_<uid>_docs.json
  ↓
Return list of documents user owns:
  [
    {"doc_id": "doc_abc123", "filename": "lease.pdf", "uploaded": "2025-11-07..."},
    {"doc_id": "doc_xyz789", "filename": "witness.pdf", "uploaded": "2025-11-07..."}
  ]
```

### 3. Download Document
```
User → [GET /vault/download?doc_id=doc_abc123&user_token=...]
  ↓
Validate user_token → Get user_id
  ↓
Check user owns doc_id (lookup in user's document mapping)
  ↓
If authorized:
  - Read file from vault/doc_abc123/
  - Verify SHA256 hash matches certificate
  - Return file
Else:
  - Return 404 (not found or not authorized)
```

**Security:**
- User token required (validates ownership)
- Document ID is just a reference (can't access without token)
- Hash verification prevents tampering

---

## API Endpoints

### Upload Document
```http
POST /vault/upload
Headers: X-User-Token: <user_token>
Body: multipart/form-data with file

Response:
{
  "ok": true,
  "doc_id": "doc_a1b2c3d4e5f6",
  "filename": "lease.pdf",
  "sha256": "abc123..."
}
```

### List User's Documents
```http
GET /vault/list
Headers: X-User-Token: <user_token>

Response:
{
  "ok": true,
  "documents": [
    {
      "doc_id": "doc_a1b2c3d4e5f6",
      "filename": "lease.pdf",
      "uploaded": "2025-11-07T12:34:56Z"
    },
    {
      "doc_id": "doc_x7y8z9a0b1c2",
      "filename": "witness_statement.pdf",
      "uploaded": "2025-11-07T13:45:21Z"
    }
  ]
}
```

### Download Document
```http
GET /vault/download?doc_id=doc_a1b2c3d4e5f6
Headers: X-User-Token: <user_token>

Response: File download (application/octet-stream)
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing user token
- `404 Not Found` - Document doesn't exist or user doesn't own it
- `409 Conflict` - Document tampered with (hash mismatch)

---

## Certificate Structure

Each document has a certificate (`.cert.json`):

```json
{
  "doc_id": "doc_a1b2c3d4e5f6",
  "filename": "lease_agreement.pdf",
  "sha256": "abc123def456...",
  "user_id": "uuid-1234-5678-abcd",
  "created": "2025-11-07T12:34:56Z",
  "request_id": "req-xyz789",
  "attestations": []
}
```

**Fields:**
- `doc_id` - Unique document identifier
- `filename` - Original filename
- `sha256` - Hash for integrity verification
- `user_id` - Owner's internal ID
- `created` - Timestamp when uploaded
- `request_id` - Trace ID for audit trail
- `attestations` - Witness signatures (future feature)

---

## User Document Mapping

Each user has a private mapping file: `user_<uid>_docs.json`

```json
[
  {
    "doc_id": "doc_a1b2c3d4e5f6",
    "filename": "lease_agreement.pdf",
    "uploaded": "2025-11-07T12:34:56Z"
  },
  {
    "doc_id": "doc_x7y8z9a0b1c2",
    "filename": "witness_statement.pdf",
    "uploaded": "2025-11-07T13:45:21Z"
  }
]
```

**Purpose:**
- Quick lookup of user's documents
- No need to scan entire vault directory
- User can list their documents without admin access

**Security:**
- File stored by user_id (only accessible with user token)
- Admin cannot use this to access documents (still needs user token)

---

## Security Properties

### 1. User Token Required
```python
# Every vault operation validates user token
uid = validate_user_token(token)
if not uid:
    return jsonify({"error": "unauthorized"}), 401
```

### 2. Ownership Verification
```python
# Check user owns document before download
user_docs = _get_user_documents(uid)
doc_info = next((d for d in user_docs if d['doc_id'] == doc_id), None)
if not doc_info:
    return 404  # Not found or not authorized
```

### 3. Integrity Verification
```python
# Verify file hasn't been tampered with
actual_hash = _sha256_of_file(path)
if actual_hash != cert['sha256']:
    log_event("vault.tamper_detected")
    return 409  # Conflict - tamper detected
```

### 4. Admin Isolation
```python
# Admin master key does NOT work for vault
# validate_user_token() only accepts USER tokens, not admin tokens
# Admin cannot access user's document mapping or documents
```

---

## Sharing Documents (Future Feature)

With document ID storage, we can implement granular sharing:

### Share Token System
```python
# User generates share token for specific document
POST /vault/share
{
  "doc_id": "doc_abc123",
  "recipient_email": "lawyer@example.com",
  "expires_in": 86400  # 24 hours
}

Response:
{
  "share_token": "share_xyz789",
  "expires": "2025-11-08T12:34:56Z",
  "share_url": "https://semptify.onrender.com/vault/shared?token=share_xyz789"
}
```

### Access Shared Document
```http
GET /vault/shared?token=share_xyz789

→ Validates share token
→ Returns document if:
  - Share token valid
  - Not expired
  - Not revoked by owner
```

### Revoke Access
```http
POST /vault/revoke
{
  "share_token": "share_xyz789"
}

→ Revokes access immediately
→ Shared URL no longer works
```

**Benefits of Document ID + Share Tokens:**
- User controls who can access each document
- Time-limited access (auto-expire)
- Audit trail (who accessed when)
- User can revoke anytime
- No need to copy documents (just share reference)

---

## Migration from Old Structure

If you have documents in the old structure (`vault/user_id/file.pdf`):

### Option 1: Keep Both (Backward Compatible)
```python
# Download endpoint supports both:
GET /vault/download?doc_id=doc_abc123  # New method
GET /vault/download?filename=lease.pdf  # Legacy method
```

### Option 2: Migrate Script
```python
# migrate_vault_structure.py
for user_id in os.listdir('uploads/vault/'):
    user_dir = f'uploads/vault/{user_id}'
    for filename in os.listdir(user_dir):
        # Generate doc_id
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        
        # Move file to new structure
        old_path = f'{user_dir}/{filename}'
        new_path = f'uploads/vault/{doc_id}/{filename}'
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(old_path, new_path)
        
        # Create certificate
        create_certificate(doc_id, filename, user_id)
        
        # Update user's document mapping
        add_to_user_mapping(user_id, doc_id, filename)
```

---

## Storage Backend (R2 or Local)

Storage structure works with **both** R2 and local filesystem:

### R2 (Cloudflare)
```
Bucket: semptify-storage
├── vault/doc_abc123/lease.pdf
├── vault/doc_abc123/lease.pdf.cert.json
├── vault/doc_xyz789/witness.pdf
└── vault/user_uuid-1234_docs.json
```

### Local (Development/Testing)
```
uploads/vault/
├── doc_abc123/lease.pdf
├── doc_abc123/lease.pdf.cert.json
├── doc_xyz789/witness.pdf
└── user_uuid-1234_docs.json
```

**Storage adapter handles both automatically** (see `storage_adapter.py`)

---

## Best Practices

### 1. Always Use Document ID
```python
# ✅ Good - use doc_id
GET /vault/download?doc_id=doc_abc123&user_token=...

# ❌ Avoid - filename ambiguous
GET /vault/download?filename=lease.pdf&user_token=...
```

### 2. Validate Ownership
```python
# Always check user owns document before access
user_docs = _get_user_documents(uid)
if doc_id not in [d['doc_id'] for d in user_docs]:
    return 404
```

### 3. Verify Integrity
```python
# Always check hash before serving
actual = _sha256_of_file(path)
if actual != cert['sha256']:
    log_event("tamper_detected")
    return 409
```

### 4. Audit Everything
```python
# Log all vault operations
log_event("vault.upload", {"user_id": uid, "doc_id": doc_id})
log_event("vault.download", {"user_id": uid, "doc_id": doc_id})
log_event("vault.tamper_detected", {"doc_id": doc_id})
```

---

## Summary

| Aspect | Implementation |
|--------|----------------|
| **Storage** | By document ID (`vault/doc_abc123/`) |
| **Access** | User token required (validates ownership) |
| **Listing** | User's document mapping (`user_<uid>_docs.json`) |
| **Security** | Token validation + ownership check + hash verification |
| **Admin** | Cannot access vaults (user privacy) |
| **Sharing** | Ready for granular per-document sharing (future) |
| **Integrity** | SHA-256 hash in certificate |
| **Audit** | All operations logged with doc_id |

---

**Status**: ✅ Implemented in `vault.py`  
**Next**: Add share token system for document sharing
