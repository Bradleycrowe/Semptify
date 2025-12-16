"""
Storage-as-Identity Router - FastAPI
Persistent storage via Cloudflare R2 (or local fallback)
"""
from fastapi import APIRouter, HTTPException, Depends, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
import os
import hashlib
import json
import time
import secrets
import uuid
import io

router = APIRouter()

# ============================================================================
# STORAGE CONFIG
# ============================================================================

STORAGE_TYPE = os.environ.get("STORAGE_TYPE", "r2")  # "r2" or "local"

# R2 config
R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY = os.environ.get("R2_ACCESS_KEY", "")
R2_SECRET_KEY = os.environ.get("R2_SECRET_KEY", "")
R2_BUCKET = os.environ.get("R2_BUCKET", "semptify-storage")
R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com" if R2_ACCOUNT_ID else ""

# Local fallback
LOCAL_STORAGE_ROOT = "uploads/user_storage"
os.makedirs(LOCAL_STORAGE_ROOT, exist_ok=True)


def get_r2_client():
    """Get R2 client (S3-compatible)."""
    import boto3
    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        region_name='auto'
    )


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def storage_key(storage_id: str, path: str = "") -> str:
    """Build R2 key: storage_id/path"""
    if path:
        return f"{storage_id}/{path}"
    return f"{storage_id}/"


# ============================================================================
# R2 OPERATIONS
# ============================================================================

def r2_put(key: str, data: bytes, content_type: str = "application/octet-stream"):
    """Put object to R2."""
    client = get_r2_client()
    client.put_object(Bucket=R2_BUCKET, Key=key, Body=data, ContentType=content_type)


def r2_get(key: str) -> bytes:
    """Get object from R2."""
    client = get_r2_client()
    response = client.get_object(Bucket=R2_BUCKET, Key=key)
    return response['Body'].read()


def r2_delete(key: str):
    """Delete object from R2."""
    client = get_r2_client()
    client.delete_object(Bucket=R2_BUCKET, Key=key)


def r2_exists(key: str) -> bool:
    """Check if object exists in R2."""
    try:
        client = get_r2_client()
        client.head_object(Bucket=R2_BUCKET, Key=key)
        return True
    except:
        return False


def r2_list(prefix: str) -> list:
    """List objects with prefix."""
    client = get_r2_client()
    response = client.list_objects_v2(Bucket=R2_BUCKET, Prefix=prefix)
    return response.get('Contents', [])


# ============================================================================
# LOCAL FALLBACK OPERATIONS
# ============================================================================

def local_path(storage_id: str, path: str = "") -> str:
    base = os.path.join(LOCAL_STORAGE_ROOT, storage_id)
    os.makedirs(base, exist_ok=True)
    if path:
        return os.path.join(base, path)
    return base


def local_put(storage_id: str, path: str, data: bytes):
    fpath = local_path(storage_id, path)
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, 'wb') as f:
        f.write(data)


def local_get(storage_id: str, path: str) -> bytes:
    fpath = local_path(storage_id, path)
    with open(fpath, 'rb') as f:
        return f.read()


def local_exists(storage_id: str, path: str) -> bool:
    return os.path.exists(local_path(storage_id, path))


def local_delete(storage_id: str, path: str):
    fpath = local_path(storage_id, path)
    if os.path.exists(fpath):
        os.remove(fpath)


def local_list(storage_id: str, folder: str = "") -> list:
    base = local_path(storage_id, folder)
    if not os.path.exists(base):
        return []
    items = []
    for name in os.listdir(base):
        if name.startswith('.'):
            continue
        fpath = os.path.join(base, name)
        items.append({
            'name': name,
            'type': 'folder' if os.path.isdir(fpath) else 'file',
            'size': os.path.getsize(fpath) if os.path.isfile(fpath) else 0,
            'modified': os.path.getmtime(fpath)
        })
    return items


# ============================================================================
# UNIFIED STORAGE INTERFACE
# ============================================================================

def storage_put(storage_id: str, path: str, data: bytes, content_type: str = "application/octet-stream"):
    if STORAGE_TYPE == "r2" and R2_ACCOUNT_ID:
        r2_put(storage_key(storage_id, path), data, content_type)
    else:
        local_put(storage_id, path, data)


def storage_get(storage_id: str, path: str) -> bytes:
    if STORAGE_TYPE == "r2" and R2_ACCOUNT_ID:
        return r2_get(storage_key(storage_id, path))
    else:
        return local_get(storage_id, path)


def storage_exists(storage_id: str, path: str) -> bool:
    if STORAGE_TYPE == "r2" and R2_ACCOUNT_ID:
        return r2_exists(storage_key(storage_id, path))
    else:
        return local_exists(storage_id, path)


def storage_delete(storage_id: str, path: str):
    if STORAGE_TYPE == "r2" and R2_ACCOUNT_ID:
        r2_delete(storage_key(storage_id, path))
    else:
        local_delete(storage_id, path)


def storage_list(storage_id: str, folder: str = "") -> list:
    if STORAGE_TYPE == "r2" and R2_ACCOUNT_ID:
        prefix = storage_key(storage_id, folder)
        objects = r2_list(prefix)
        items = []
        for obj in objects:
            key = obj['Key']
            name = key.replace(prefix, '').strip('/')
            if '/' in name:
                continue  # Skip nested
            if name and not name.startswith('.'):
                items.append({
                    'name': name,
                    'type': 'file',
                    'size': obj.get('Size', 0),
                    'modified': obj.get('LastModified', '').isoformat() if obj.get('LastModified') else ''
                })
        return items
    else:
        return local_list(storage_id, folder)


# ============================================================================
# VERIFY STORAGE ACCESS
# ============================================================================

def verify_storage_access(storage_id: str, token: str) -> bool:
    """Verify token by checking hash in user's storage."""
    try:
        stored_hash = storage_get(storage_id, ".token").decode().strip()
        return stored_hash == hash_token(token)
    except:
        return False


def extract_credentials(request: Request) -> tuple:
    storage_id = request.headers.get("X-Storage-ID") or request.query_params.get("storage_id")
    token = request.headers.get("X-Storage-Token") or request.query_params.get("token")
    return storage_id, token


async def require_storage_access(request: Request) -> str:
    storage_id, token = extract_credentials(request)
    if not storage_id or not token:
        raise HTTPException(status_code=401, detail="Missing credentials")
    if not verify_storage_access(storage_id, token):
        raise HTTPException(status_code=401, detail="Invalid access")
    return storage_id


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/config")
async def get_config():
    """Show storage configuration (no secrets)."""
    return {
        "storage_type": STORAGE_TYPE,
        "r2_configured": bool(R2_ACCOUNT_ID and R2_ACCESS_KEY),
        "r2_bucket": R2_BUCKET if R2_ACCOUNT_ID else None,
        "local_root": LOCAL_STORAGE_ROOT if STORAGE_TYPE == "local" else None
    }


@router.post("/provision")
async def provision_storage():
    """Create new storage - returns credentials (token NOT stored by us)."""
    storage_id = f"store_{uuid.uuid4().hex[:12]}"
    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)
    
    # Store ONLY the hash in user's storage
    storage_put(storage_id, ".token", token_hash.encode())
    
    # Welcome file
    welcome = {
        "storage_id": storage_id,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "storage_type": STORAGE_TYPE,
        "message": "Your secure storage. Token = access."
    }
    storage_put(storage_id, "welcome.json", json.dumps(welcome, indent=2).encode(), "application/json")
    
    return {
        "storage_id": storage_id,
        "token": token,
        "storage_type": STORAGE_TYPE,
        "message": "SAVE THESE CREDENTIALS. Token is NOT stored - only YOU have it.",
        "usage": {
            "headers": {"X-Storage-ID": storage_id, "X-Storage-Token": "<your-token>"},
            "query": f"?storage_id={storage_id}&token=<your-token>"
        }
    }


@router.get("/info")
async def storage_info(storage_id: str = Depends(require_storage_access)):
    """List storage contents."""
    files = storage_list(storage_id)
    total_size = sum(f.get('size', 0) for f in files)
    return {
        "storage_id": storage_id,
        "storage_type": STORAGE_TYPE,
        "file_count": len(files),
        "total_size": total_size,
        "files": files
    }




@router.post("/json-upload")
async def upload_json(
    request: Request,
    path: str,
    storage_id: str = Depends(require_storage_access)
):
    """Upload JSON data directly."""
    body = await request.body()
    file_hash = hashlib.sha256(body).hexdigest()
    storage_put(storage_id, path, body, "application/json")
    
    return {
        "status": "uploaded",
        "filename": path.split('/')[-1],
        "path": path,
        "size": len(body),
        "sha256": file_hash,
        "storage_type": STORAGE_TYPE
    }

@router.post("/upload")
async def upload_flexible(
    request: Request,
    path: str = None,
    storage_id: str = Depends(require_storage_access)
):
    """Flexible upload - handles JSON body or multipart form data."""
    content_type = request.headers.get('content-type', '')
    
    # JSON upload (for profile.json, settings, etc)
    if 'application/json' in content_type:
        body = await request.body()
        if not path:
            raise HTTPException(400, "path query parameter required for JSON uploads")
        
        file_hash = hashlib.sha256(body).hexdigest()
        storage_put(storage_id, path, body, "application/json")
        
        return {
            "status": "uploaded",
            "filename": path.split('/')[-1],
            "path": path,
            "size": len(body),
            "sha256": file_hash,
            "storage_type": STORAGE_TYPE
        }
    
    # Multipart form upload (original behavior)
    form = await request.form()
    file = form.get('file')
    folder = form.get('folder', '')
    
    if not file:
        raise HTTPException(400, "No file provided. Use multipart form with 'file' field or JSON body with 'path' param")
    
    file_content = await file.read()
    file_path = f"{folder}/{file.filename}" if folder else file.filename
    file_hash = hashlib.sha256(file_content).hexdigest()
    
    storage_put(storage_id, file_path, file_content, getattr(file, 'content_type', None) or "application/octet-stream")
    
    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": file_path,
        "size": len(file_content),
        "sha256": file_hash,
        "storage_type": STORAGE_TYPE
    }


@router.post("/upload-multipart")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Form(""),
    storage_id: str = Depends(require_storage_access)
):
    """Upload file."""
    content = await file.read()
    path = f"{folder}/{file.filename}" if folder else file.filename
    file_hash = hashlib.sha256(content).hexdigest()
    
    storage_put(storage_id, path, content, file.content_type or "application/octet-stream")
    
    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": path,
        "size": len(content),
        "sha256": file_hash,
        "storage_type": STORAGE_TYPE
    }


@router.get("/download/{filepath:path}")
async def download_file(filepath: str, storage_id: str = Depends(require_storage_access)):
    """Download file."""
    if not storage_exists(storage_id, filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    content = storage_get(storage_id, filepath)
    filename = os.path.basename(filepath)
    
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.delete("/delete/{filepath:path}")
async def delete_file(filepath: str, storage_id: str = Depends(require_storage_access)):
    """Delete file."""
    if not storage_exists(storage_id, filepath):
        raise HTTPException(status_code=404, detail="File not found")
    storage_delete(storage_id, filepath)
    return {"status": "deleted", "path": filepath}


@router.get("/list/{folder:path}")
async def list_folder(folder: str = "", storage_id: str = Depends(require_storage_access)):
    """List folder contents."""
    items = storage_list(storage_id, folder)
    return {"folder": folder or "/", "items": items}


# ============================================================================
# VAULT (attested storage)
# ============================================================================

@router.post("/vault/upload")
async def vault_upload(
    file: UploadFile = File(...),
    evidence_type: str = Form("document"),
    description: str = Form(""),
    storage_id: str = Depends(require_storage_access)
):
    """Upload to vault with attestation."""
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    timestamp = int(time.time())
    
    vault_path = f"vault/{file.filename}"
    storage_put(storage_id, vault_path, content, file.content_type or "application/octet-stream")
    
    cert = {
        "filename": file.filename,
        "sha256": file_hash,
        "size": len(content),
        "evidence_type": evidence_type,
        "description": description,
        "timestamp": timestamp,
        "attested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "request_id": str(uuid.uuid4()),
        "storage_type": STORAGE_TYPE
    }
    
    cert_path = f"vault/{file.filename}.cert.json"
    storage_put(storage_id, cert_path, json.dumps(cert, indent=2).encode(), "application/json")
    
    return {"status": "attested", "filename": file.filename, "certificate": cert}


@router.get("/vault/list")
async def vault_list(storage_id: str = Depends(require_storage_access)):
    """List vault contents."""
    items = storage_list(storage_id, "vault")
    files = []
    
    for item in items:
        if item['name'].endswith('.cert.json'):
            continue
        
        cert = None
        cert_path = f"vault/{item['name']}.cert.json"
        if storage_exists(storage_id, cert_path):
            cert = json.loads(storage_get(storage_id, cert_path).decode())
        
        files.append({
            "filename": item['name'],
            "size": item.get('size', 0),
            "attested": cert is not None,
            "certificate": cert
        })
    
    return {"files": files}


@router.get("/vault/verify/{filename}")
async def vault_verify(filename: str, storage_id: str = Depends(require_storage_access)):
    """Verify file integrity."""
    file_path = f"vault/{filename}"
    cert_path = f"vault/{filename}.cert.json"
    
    if not storage_exists(storage_id, file_path):
        raise HTTPException(status_code=404, detail="File not found")
    if not storage_exists(storage_id, cert_path):
        raise HTTPException(status_code=404, detail="No certificate")
    
    content = storage_get(storage_id, file_path)
    current_hash = hashlib.sha256(content).hexdigest()
    cert = json.loads(storage_get(storage_id, cert_path).decode())
    
    return {
        "filename": filename,
        "verified": current_hash == cert["sha256"],
        "current_hash": current_hash,
        "original_hash": cert["sha256"],
        "certificate": cert
    }


@router.get("/vault/download/{filename}")
async def vault_download(filename: str, storage_id: str = Depends(require_storage_access)):
    """Download vault file."""
    file_path = f"vault/{filename}"
    if not storage_exists(storage_id, file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    content = storage_get(storage_id, file_path)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


