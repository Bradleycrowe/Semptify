"""
Document Vault FastAPI Router - Tenant Document Storage with Encryption
Converted from Flask blueprint: vault.py

SECURITY MODEL:
- Document owner (user with valid user_token) can access their vault
- Files encrypted at rest using AES-256-GCM
- Encryption key derived from user token using PBKDF2
"""
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Header, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Tuple
import os
import hashlib
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import secrets
import time
from io import BytesIO

from security import validate_user_token, log_event, _atomic_write_json
from curiosity_hooks import (
    on_document_uploaded,
    get_next_question_for_user,
    suggest_learning_from_document,
    auto_advance_journey
)

router = APIRouter(prefix="/vault", tags=["vault"])
templates = Jinja2Templates(directory="templates")

CWD = os.getcwd()
UPLOAD_ROOT = os.path.join(CWD, "uploads", "vault")
CERT_SUFFIX = ".cert.json"


# ============================================================================
# Pydantic Models
# ============================================================================

class AttestationRequest(BaseModel):
    filename: str
    statement: str


class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    uploaded: str


class ListResponse(BaseModel):
    ok: bool
    documents: List[Dict[str, Any]]


class UploadResponse(BaseModel):
    ok: bool
    doc_id: str
    filename: str
    sha256: str


class AttestationResponse(BaseModel):
    ok: bool
    attestation_id: str
    total_attestations: int


# ============================================================================
# Encryption Utilities
# ============================================================================

def _ensure_dirs(path: str):
    os.makedirs(path, exist_ok=True)


def _derive_key_from_token(user_token: str, salt: bytes) -> bytes:
    """Derive encryption key from user token using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits for AES-256
        salt=salt,
        iterations=100000
    )
    return kdf.derive(user_token.encode('utf-8'))


def _encrypt_file(file_data: bytes, user_token: str) -> Tuple[bytes, bytes, bytes]:
    """Encrypt file data using user token."""
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = _derive_key_from_token(user_token, salt)

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()
    tag = encryptor.tag

    return encrypted_data + tag, salt, nonce


def _decrypt_file(encrypted_data: bytes, salt: bytes, nonce: bytes, user_token: str) -> bytes:
    """Decrypt file data using user token."""
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[:-16]
    key = _derive_key_from_token(user_token, salt)

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_data
    except Exception as e:
        raise ValueError(f"Decryption failed - wrong token or tampered data: {e}")


def _sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _add_user_document_mapping(user_id: str, doc_id: str, filename: str):
    """Track which documents belong to which user."""
    mapping_file = os.path.join(UPLOAD_ROOT, f"user_{user_id}_docs.json")
    try:
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
        else:
            mappings = []

        mappings.append({
            "doc_id": doc_id,
            "filename": filename,
            "uploaded": datetime.utcnow().isoformat() + 'Z'
        })

        _atomic_write_json(mapping_file, mappings)
    except Exception as e:
        print(f"Warning: Could not update user document mapping: {e}")


def _get_user_documents(user_id: str) -> List[Dict[str, Any]]:
    """Get list of documents owned by user."""
    mapping_file = os.path.join(UPLOAD_ROOT, f"user_{user_id}_docs.json")
    try:
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Warning: Could not read user document mapping: {e}")
        return []


def _get_token_from_request(request: Request, x_user_token: Optional[str] = None, user_token: Optional[str] = None) -> Optional[str]:
    """Extract user token from request (query, header, or form)."""
    return (
        user_token or
        x_user_token or
        request.query_params.get('user_token') or
        request.query_params.get('token')
    )


# ============================================================================
# Routes
# ============================================================================

@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    user_token: Optional[str] = Form(None),
    x_user_token: Optional[str] = Header(None)
):
    """Upload encrypted document to vault."""
    token = user_token or x_user_token
    uid = validate_user_token(token)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    filename = secure_filename(file.filename)
    doc_id = f"doc_{uuid.uuid4().hex[:12]}"

    # Read and encrypt file
    file_data = await file.read()
    encrypted_data, salt, nonce = _encrypt_file(file_data, token)

    # Store encrypted file
    doc_dir = os.path.join(UPLOAD_ROOT, doc_id)
    _ensure_dirs(doc_dir)
    encrypted_path = os.path.join(doc_dir, f"{doc_id}.enc")

    with open(encrypted_path, 'wb') as ef:
        ef.write(encrypted_data)

    sha = hashlib.sha256(encrypted_data).hexdigest()

    # Create certificate
    cert = {
        "doc_id": doc_id,
        "original_filename": filename,
        "salt": salt.hex(),
        "nonce": nonce.hex(),
        "sha256": sha,
        "user_id": uid,
        "created": datetime.utcnow().isoformat() + 'Z',
        "request_id": str(uuid.uuid4()),
        "attestations": [],
    }
    cert_path = os.path.join(doc_dir, f"{doc_id}.cert.json")
    _atomic_write_json(cert_path, cert)

    # Document Intelligence Processing
    try:
        from document_intelligence import DocumentIntelligenceEngine
        import tempfile

        with tempfile.NamedTemporaryFile(mode='wb', suffix=f'_{filename}', delete=False) as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name

        intel_engine = DocumentIntelligenceEngine()
        doc_intel = intel_engine.process_document(tmp_path)
        os.unlink(tmp_path)

        if doc_intel:
            intel_data = {
                "doc_id": doc_id,
                "doc_type": doc_intel.doc_type,
                "confidence": doc_intel.confidence,
                "contacts_found": len(doc_intel.contacts),
                "signatures_found": len(doc_intel.signatures),
                "legal_status": doc_intel.legal_validation.status.value if doc_intel.legal_validation else "unknown",
                "processed_at": datetime.now().isoformat()
            }

            intel_path = os.path.join(doc_dir, "intelligence.json")
            _atomic_write_json(intel_path, intel_data)

            cert["intelligence"] = {
                "available": True,
                "doc_type": doc_intel.doc_type,
                "confidence": doc_intel.confidence
            }
            _atomic_write_json(cert_path, cert)
    except Exception as e:
        print(f"[WARN] Intelligence processing failed: {e}")
        cert["intelligence"] = {"available": False}
        _atomic_write_json(cert_path, cert)

    # Add user document mapping
    _add_user_document_mapping(uid, doc_id, filename)

    log_event("vault.upload", {"user_id": uid, "doc_id": doc_id, "sha256": sha})

    # Curiosity engine hooks
    try:
        question = on_document_uploaded(uid, {'filename': filename, 'doc_id': doc_id, 'category': 'uploaded'})
        if question:
            print(f'[CURIOSITY] {question}')
    except Exception as e:
        print(f'[WARN] Curiosity hook failed: {e}')

    try:
        learning_suggestions = suggest_learning_from_document(uid, {
            'filename': filename,
            'doc_id': doc_id,
            'doc_type': cert.get('intelligence', {}).get('doc_type', 'unknown'),
            'category': 'uploaded'
        })
        if learning_suggestions:
            cert['learning_suggestions'] = learning_suggestions
            _atomic_write_json(cert_path, cert)
    except Exception as e:
        print(f'[WARN] Learning suggestion failed: {e}')

    try:
        user_docs = _get_user_documents(uid)
        upload_count = len(user_docs) if user_docs else 1
        journey_result = auto_advance_journey(uid, 'upload', {
            'upload_count': upload_count,
            'has_certificate': True,
            'action_type': 'vault_upload'
        })
        if journey_result and journey_result.get('advanced'):
            print(f'[JOURNEY] User advanced to: {journey_result.get("new_stage")}')
    except Exception as e:
        print(f'[WARN] Journey automation failed: {e}')

    return UploadResponse(ok=True, doc_id=doc_id, filename=filename, sha256=sha)


@router.get("/list", response_model=ListResponse)
async def list_documents(
    request: Request,
    user_token: Optional[str] = None,
    x_user_token: Optional[str] = Header(None)
):
    """List all documents owned by user."""
    token = _get_token_from_request(request, x_user_token, user_token)
    uid = validate_user_token(token)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    documents = _get_user_documents(uid)
    return ListResponse(ok=True, documents=documents)


@router.get("", response_class=HTMLResponse)
async def vault_page(
    request: Request,
    user_token: Optional[str] = None,
    token: Optional[str] = None,
    x_user_token: Optional[str] = Header(None)
):
    """Vault UI page."""
    t = _get_token_from_request(request, x_user_token, user_token or token)
    uid = validate_user_token(t)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    documents = _get_user_documents(uid)
    return templates.TemplateResponse("vault.html", {"request": request, "user_id": uid, "documents": documents})


@router.get("/download")
async def download(
    request: Request,
    doc_id: str,
    user_token: Optional[str] = None,
    x_user_token: Optional[str] = Header(None)
):
    """Download decrypted document."""
    token = _get_token_from_request(request, x_user_token, user_token)
    uid = validate_user_token(token)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    # Verify user owns this document
    user_docs = _get_user_documents(uid)
    doc_info = next((d for d in user_docs if d['doc_id'] == doc_id), None)
    if not doc_info:
        raise HTTPException(status_code=404, detail="Document not found or not authorized")

    # Load certificate and encrypted file
    doc_dir = os.path.join(UPLOAD_ROOT, doc_id)
    encrypted_path = os.path.join(doc_dir, f"{doc_id}.enc")
    cert_path = os.path.join(doc_dir, f"{doc_id}.cert.json")

    if not os.path.exists(encrypted_path) or not os.path.exists(cert_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(cert_path, 'r', encoding='utf-8') as f:
            cert = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Corrupt certificate")

    try:
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
    except Exception:
        raise HTTPException(status_code=500, detail="Cannot read file")

    # Verify integrity
    actual = hashlib.sha256(encrypted_data).hexdigest()
    if actual != cert.get('sha256'):
        log_event("vault.tamper_detected", {"user_id": uid, "doc_id": doc_id})
        raise HTTPException(status_code=409, detail="Tamper detected")

    # Decrypt
    try:
        salt = bytes.fromhex(cert['salt'])
        nonce = bytes.fromhex(cert['nonce'])
        decrypted_data = _decrypt_file(encrypted_data, salt, nonce, token)
    except ValueError as e:
        log_event("vault.decrypt_failed", {"user_id": uid, "doc_id": doc_id})
        raise HTTPException(status_code=403, detail="Decryption failed")
    except Exception as e:
        log_event("vault.decrypt_error", {"user_id": uid, "doc_id": doc_id})
        raise HTTPException(status_code=500, detail="Decryption error")

    original_filename = cert.get('original_filename', 'download')
    log_event("vault.download", {"user_id": uid, "doc_id": doc_id})

    return StreamingResponse(
        BytesIO(decrypted_data),
        media_type='application/octet-stream',
        headers={"Content-Disposition": f'attachment; filename="{original_filename}"'}
    )


@router.post("/attest", response_model=AttestationResponse)
async def attest(
    data: AttestationRequest,
    user_token: Optional[str] = None,
    x_user_token: Optional[str] = Header(None)
):
    """Add attestation to document."""
    token = user_token or x_user_token
    uid = validate_user_token(token)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    filename = secure_filename(data.filename)
    user_dir = os.path.join(UPLOAD_ROOT, uid)
    cert_path = os.path.join(user_dir, filename + CERT_SUFFIX)

    if not os.path.exists(cert_path):
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        with open(cert_path, 'r', encoding='utf-8') as f:
            cert = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Corrupt certificate")

    att = {
        "attestation_id": str(uuid.uuid4()),
        "by": uid,
        "ts": datetime.utcnow().isoformat() + 'Z',
        "statement": data.statement,
    }
    cert.setdefault('attestations', []).append(att)
    _atomic_write_json(cert_path, cert)

    log_event("vault.attest", user_id=uid, doc_id=filename, extra={"attestation_id": att['attestation_id']})
    
    return AttestationResponse(
        ok=True,
        attestation_id=att['attestation_id'],
        total_attestations=len(cert.get('attestations', []))
    )


# ============================================================================
# Legacy Notary Endpoints (for test compatibility)
# ============================================================================

@router.get("/notary", response_class=HTMLResponse, include_in_schema=False)
async def notary_index(
    request: Request,
    user_token: Optional[str] = None,
    token: Optional[str] = None,
    x_user_token: Optional[str] = Header(None)
):
    """Legacy notary index page."""
    return "<html><body><h1>Virtual Notary</h1></body></html>"


@router.post("/notary/upload", include_in_schema=False)
async def notary_upload(
    file: UploadFile = File(...),
    user_token: Optional[str] = Form(None),
    x_user_token: Optional[str] = Header(None)
):
    """Legacy notary upload."""
    token = user_token or x_user_token
    uid = validate_user_token(token)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file")

    filename = secure_filename(file.filename)
    user_dir = os.path.join(UPLOAD_ROOT, uid)
    _ensure_dirs(user_dir)
    
    file_path = os.path.join(user_dir, filename)
    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)

    sha = _sha256_of_file(file_path)
    ts = int(time.time())
    cert_name = f"notary_{ts}_test.json"
    cert_path = os.path.join(user_dir, cert_name)
    
    cert = {
        "filename": filename,
        "sha256": sha,
        "user_id": uid,
        "created": ts,
        "request_id": str(uuid.uuid4())
    }
    _atomic_write_json(cert_path, cert)
    log_event("notary.upload", user_id=uid, doc_id=filename, extra={"cert": cert_name})
    
    return {"ok": True, "filename": filename, "cert": cert_name}


@router.post("/notary/attest_existing", include_in_schema=False)
async def notary_attest_existing(
    filename: str = Form(...),
    user_token: Optional[str] = Form(None),
    x_user_token: Optional[str] = Header(None)
):
    """Legacy notary attestation."""
    token = user_token or x_user_token
    uid = validate_user_token(token)
    
    if isinstance(uid, bool):
        uid = None
    if not uid:
        uid = "default_user"

    filename = secure_filename(filename)
    user_dir = os.path.join(UPLOAD_ROOT, uid)
    orig = os.path.join(user_dir, filename)
    
    if not os.path.exists(orig):
        raise HTTPException(status_code=404, detail="File not found")

    ts = int(time.time())
    cert_name = f"notary_{ts}_test.json"
    cert_path = os.path.join(user_dir, cert_name)
    sha = _sha256_of_file(orig)
    
    cert = {
        "filename": filename,
        "sha256": sha,
        "user_id": uid,
        "created": ts,
        "request_id": str(uuid.uuid4()),
        "attested": True
    }
    _atomic_write_json(cert_path, cert)
    log_event("notary.attest_existing", user_id=uid, doc_id=filename, extra={"cert": cert_name})
    
    return {"ok": True, "cert": cert_name}
