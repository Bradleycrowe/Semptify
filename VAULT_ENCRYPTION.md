# 🔐 Vault Encryption System

## Core Principle: Zero-Knowledge Encryption

**Your token = Your encryption key**
- Files encrypted with key derived from YOUR user token
- Without your token, files are unreadable (even by admin)
- Server never stores unencrypted encryption keys

---

## Encryption Flow

### Upload (Encrypt)
```
User uploads file.pdf with user_token
  ↓
1. Derive encryption key from user_token using PBKDF2
   - user_token + random salt → 256-bit AES key
   - 100,000 iterations (slow = secure)
  ↓
2. Encrypt file with AES-256-GCM
   - AES-256: Industry standard, unbreakable
   - GCM mode: Authenticated encryption (detects tampering)
   - Random nonce: Unique per file
  ↓
3. Store encrypted file: file.pdf.enc
  ↓
4. Store metadata in certificate:
   {
     "salt": "random 16 bytes",
     "nonce": "random 12 bytes",
     "sha256": "hash of encrypted data",
     "original_filename": "file.pdf"
   }
```

### Download (Decrypt)
```
User requests file with user_token
  ↓
1. Validate user_token (proves ownership)
  ↓
2. Load encrypted file + certificate
  ↓
3. Derive same encryption key:
   - user_token + stored salt → 256-bit AES key
  ↓
4. Decrypt file with key + nonce
   - GCM verifies authentication tag
   - If wrong token or tampered: DECRYPTION FAILS
  ↓
5. Return decrypted file to user
```

---

## Where Encryption Happens

### Storage Structure
```
vault/
  doc_abc123/
    lease.pdf.enc          ← ENCRYPTED file data
    lease.pdf.cert.json    ← Unencrypted metadata (salt, nonce, hash)
  doc_xyz789/
    witness.pdf.enc
    witness.pdf.cert.json
```

### What's Encrypted
- ✅ File contents (encrypted with AES-256-GCM)
- ❌ Filename (stored in certificate, plain text)
- ❌ Document ID (storage path, plain text)
- ❌ Certificate metadata (salt, nonce, hash - needed for decryption)

**Why some data not encrypted?**
- Need to find files (doc_id, filename)
- Need decryption parameters (salt, nonce)
- Hash of encrypted data (verify integrity)

---

## Security Properties

### 1. User Token as Key
```python
# Key derivation function
key = PBKDF2(
    password=user_token,  # Your 12-digit token
    salt=random_salt,     # Unique per file
    iterations=100000,    # Slow brute force attacks
    algorithm=SHA256
)
```

**Security:**
- 12-digit token = ~40 bits entropy
- PBKDF2 makes cracking expensive (100k iterations)
- Random salt prevents rainbow tables
- Different key for each file (unique salt)

### 2. Authenticated Encryption (GCM)
```python
encrypted_data, auth_tag = AES_GCM_encrypt(
    plaintext=file_data,
    key=derived_key,
    nonce=random_nonce
)
```

**Security:**
- Encryption + authentication in one step
- Any tampering detected during decryption
- Prevents ciphertext modification attacks

### 3. Zero-Knowledge Architecture
```
Server stores:
  ✅ Encrypted files (unreadable without token)
  ✅ Salt and nonce (needed for decryption)
  ✅ Hash of encrypted data (integrity)
  
Server NEVER stores:
  ❌ User tokens (only hash)
  ❌ Encryption keys (derived on-demand)
  ❌ Decrypted file data (only in memory during transfer)
```

---

## Encryption Algorithm Details

### AES-256-GCM
```
Algorithm: Advanced Encryption Standard
Key size: 256 bits (32 bytes)
Mode: Galois/Counter Mode (authenticated encryption)
Nonce: 96 bits (12 bytes, random per encryption)
Tag: 128 bits (16 bytes, for authentication)
```

**Why AES-256-GCM?**
- ✅ NIST approved
- ✅ Hardware accelerated (fast)
- ✅ Authenticated (detects tampering)
- ✅ Parallelizable (good performance)
- ✅ Industry standard (TLS, disk encryption)

### PBKDF2-SHA256
```
Algorithm: Password-Based Key Derivation Function 2
Hash: SHA-256
Salt: 128 bits (16 bytes, random per file)
Iterations: 100,000 (OWASP recommendation)
Output: 256 bits (32 bytes for AES-256 key)
```

**Why PBKDF2?**
- ✅ NIST approved (SP 800-132)
- ✅ Widely supported
- ✅ Configurable iterations (adjustable security)
- ✅ Salt prevents rainbow tables

---

## Example: Full Encryption Cycle

### Upload
```python
# User uploads lease.pdf with token "824691357203"

# Step 1: Generate crypto parameters
salt = secrets.token_bytes(16)  # 16 random bytes
nonce = secrets.token_bytes(12)  # 12 random bytes

# Step 2: Derive key from token
key = PBKDF2(
    password="824691357203",
    salt=salt,
    iterations=100000,
    hash=SHA256,
    output_length=32
) # → key = b'\x7f\x9e...' (32 bytes)

# Step 3: Read file
file_data = open('lease.pdf', 'rb').read()  # 50KB

# Step 4: Encrypt
cipher = AES_GCM(key, nonce)
encrypted = cipher.encrypt(file_data)  # 50KB encrypted
tag = cipher.tag  # 16 bytes

# Step 5: Store encrypted file
open('vault/doc_abc123/lease.pdf.enc', 'wb').write(encrypted + tag)

# Step 6: Store certificate
cert = {
    "doc_id": "doc_abc123",
    "original_filename": "lease.pdf",
    "salt": salt.hex(),  # Store as hex string
    "nonce": nonce.hex(),
    "sha256": hashlib.sha256(encrypted + tag).hexdigest(),
    "user_id": "uuid-1234",
    "created": "2025-11-07T12:34:56Z"
}
json.dump(cert, open('vault/doc_abc123/lease.pdf.cert.json', 'w'))
```

### Download
```python
# User requests download with token "824691357203"

# Step 1: Load certificate
cert = json.load(open('vault/doc_abc123/lease.pdf.cert.json'))
salt = bytes.fromhex(cert['salt'])
nonce = bytes.fromhex(cert['nonce'])

# Step 2: Load encrypted file
encrypted_data = open('vault/doc_abc123/lease.pdf.enc', 'rb').read()

# Step 3: Verify integrity
actual_hash = hashlib.sha256(encrypted_data).hexdigest()
if actual_hash != cert['sha256']:
    raise Error("File tampered!")

# Step 4: Derive same key
key = PBKDF2(
    password="824691357203",  # Same token
    salt=salt,  # Same salt from certificate
    iterations=100000,
    hash=SHA256,
    output_length=32
) # → Same key as upload!

# Step 5: Decrypt
tag = encrypted_data[-16:]  # Last 16 bytes
ciphertext = encrypted_data[:-16]  # Everything else

cipher = AES_GCM(key, nonce, tag)
try:
    decrypted = cipher.decrypt(ciphertext)
    # → Original file data!
except:
    raise Error("Wrong token or tampered data!")

# Step 6: Return to user
return send_file(decrypted, filename='lease.pdf')
```

---

## Attack Scenarios

### ❌ Admin Tries to Read File
```
Admin has:
  - Encrypted file (unreadable gibberish)
  - Certificate (salt, nonce, hash)
  - Storage access (R2 or local)
  
Admin CANNOT:
  - Derive encryption key (needs user token)
  - Decrypt file (key required)
  - Brute force token (100k iterations = expensive)
  
Result: File remains encrypted ✅
```

### ❌ Attacker Modifies Encrypted File
```
Attacker changes bytes in lease.pdf.enc
  ↓
User downloads with valid token
  ↓
Decryption succeeds (right key)
  BUT
GCM authentication tag verification FAILS
  ↓
Decryption throws exception
  ↓
User gets error: "File tampered!"
  ↓
Event logged for investigation
  
Result: Tampering detected ✅
```

### ❌ Stolen Database/R2 Bucket
```
Attacker steals:
  - All encrypted files
  - All certificates (salt, nonce, hash)
  
Attacker CANNOT:
  - Decrypt files (no user tokens)
  - Brute force (100k iterations per attempt)
  - Rainbow tables (unique salt per file)
  
Result: Data remains confidential ✅
```

### ❌ User Loses Token
```
User forgets token "824691357203"
  ↓
Cannot derive encryption key
  ↓
Cannot decrypt files
  
Result: Data permanently inaccessible ⚠️

**Solution**: Token recovery via registered email
(Future feature: encrypt backup key with email-derived key)
```

---

## Performance Considerations

### Encryption Overhead
```
Upload (encrypt):
  - 1 MB file → ~15ms encryption (AES hardware acceleration)
  - Key derivation: ~100ms (PBKDF2 100k iterations)
  Total: ~115ms overhead

Download (decrypt):
  - 1 MB file → ~15ms decryption
  - Key derivation: ~100ms
  Total: ~115ms overhead
```

**Optimization:**
- Cache derived keys per request (same token)
- Use hardware AES acceleration (CPU AES-NI)
- Parallel processing for multiple files

### Storage Overhead
```
Original file: 1.0 MB
Encrypted file: 1.0 MB + 16 bytes (auth tag)
Certificate: ~500 bytes (JSON metadata)

Total overhead: ~516 bytes per file (0.05%)
```

---

## Key Rotation (Future Feature)

### Re-encrypt with New Token
```python
def rotate_encryption_key(doc_id, old_token, new_token):
    # 1. Decrypt with old token
    decrypted = _decrypt_file(doc_id, old_token)
    
    # 2. Encrypt with new token
    encrypted, salt, nonce = _encrypt_file(decrypted, new_token)
    
    # 3. Update certificate
    cert['salt'] = salt.hex()
    cert['nonce'] = nonce.hex()
    cert['rotated_at'] = datetime.now().isoformat()
    
    # 4. Store re-encrypted file
    save_encrypted_file(doc_id, encrypted)
```

**When to rotate:**
- User changes token
- Security breach suspected
- Compliance requirement (annual rotation)

---

## Compliance & Legal

### GDPR Compliance
- ✅ Data encrypted at rest (Article 32)
- ✅ User controls access (Article 15)
- ✅ Right to erasure (delete encrypted file) (Article 17)
- ✅ Data breach notification (encrypted = reduced risk) (Article 33)

### Legal Evidence
- ✅ SHA-256 hash proves integrity
- ✅ Timestamp in certificate
- ✅ Authentication tag prevents tampering
- ✅ Audit trail (who accessed when)

### Court Admissibility
```
Certificate provides:
  - Hash of encrypted data (integrity)
  - Timestamp (when uploaded)
  - User ID (who uploaded)
  - Authentication tag (tamper-evident)

Can prove:
  - Document existed at specific time
  - Document not altered since upload
  - Specific user owned document
```

---

## Configuration

### Environment Variables
```bash
# Optional: Override default iterations (security vs performance)
VAULT_KDF_ITERATIONS=100000  # Default, OWASP recommended

# Optional: Disable encryption (dev/testing only!)
VAULT_ENCRYPTION_ENABLED=true  # Default
```

### Security Levels
```python
# High security (slow)
KDF_ITERATIONS = 500000  # 5x default

# Standard security (recommended)
KDF_ITERATIONS = 100000  # OWASP standard

# Fast (dev/testing only)
KDF_ITERATIONS = 10000  # 10x faster, less secure
```

---

## Summary

| Aspect | Implementation |
|--------|----------------|
| **Algorithm** | AES-256-GCM (authenticated encryption) |
| **Key Derivation** | PBKDF2-SHA256 (100k iterations) |
| **Key Source** | User token (12-digit number) |
| **Salt** | Random 16 bytes per file |
| **Nonce** | Random 12 bytes per file |
| **Integrity** | GCM authentication tag + SHA-256 hash |
| **Storage** | Encrypted file (.enc) + certificate (.cert.json) |
| **Access** | User token required for decryption |
| **Admin Access** | Cannot decrypt without user token |
| **Performance** | ~115ms overhead per MB |

---

**Status**: ✅ Encryption functions implemented in `vault.py`  
**Dependencies**: `cryptography>=41.0.0` in `requirements.txt`  
**Next**: Update upload/download endpoints to use encryption
