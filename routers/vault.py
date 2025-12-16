"""
Vault Router - FastAPI
Document storage with attestation
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional
import os
import hashlib
import json
import time
import uuid

from routers.session import require_session, get_session_token, get_session_manager

router = APIRouter()

VAULT_DIR = "uploads/vault"
os.makedirs(VAULT_DIR, exist_ok=True)


def get_user_vault_dir(user_id: str) -> str:
    """Get user's vault directory, create if needed."""
    path = os.path.join(VAULT_DIR, user_id)
    os.makedirs(path, exist_ok=True)
    return path


@router.get("/")
async def vault_info(user_id: str = Depends(require_session)):
    """Get vault info for authenticated user."""
    vault_dir = get_user_vault_dir(user_id)
    files = []
    
    for f in os.listdir(vault_dir):
        filepath = os.path.join(vault_dir, f)
        if os.path.isfile(filepath) and not f.endswith('.json'):
            # Check for certificate
            cert_path = filepath + '.cert.json'
            has_cert = os.path.exists(cert_path)
            
            files.append({
                "filename": f,
                "size": os.path.getsize(filepath),
                "attested": has_cert,
                "uploaded_at": os.path.getmtime(filepath)
            })
    
    return {
        "user_id": user_id,
        "file_count": len(files),
        "files": files
    }


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    evidence_type: str = Form("document"),
    description: str = Form(""),
    user_id: str = Depends(require_session)
):
    """Upload file to vault with attestation."""
    vault_dir = get_user_vault_dir(user_id)
    
    # Read file content
    content = await file.read()
    
    # Generate hash
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Save file
    filename = file.filename or f"upload_{int(time.time())}"
    filepath = os.path.join(vault_dir, filename)
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Create attestation certificate
    cert = {
        "filename": filename,
        "sha256": file_hash,
        "size": len(content),
        "evidence_type": evidence_type,
        "description": description,
        "user_id": user_id,
        "timestamp": int(time.time()),
        "request_id": str(uuid.uuid4()),
        "attested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    cert_path = filepath + ".cert.json"
    with open(cert_path, "w") as f:
        json.dump(cert, f, indent=2)
    
    return {
        "status": "uploaded",
        "filename": filename,
        "sha256": file_hash,
        "certificate": cert
    }


@router.get("/file/{filename}")
async def download_file(filename: str, user_id: str = Depends(require_session)):
    """Download file from vault."""
    vault_dir = get_user_vault_dir(user_id)
    filepath = os.path.join(vault_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(filepath, filename=filename)


@router.get("/certificate/{filename}")
async def get_certificate(filename: str, user_id: str = Depends(require_session)):
    """Get attestation certificate for file."""
    vault_dir = get_user_vault_dir(user_id)
    cert_path = os.path.join(vault_dir, filename + ".cert.json")
    
    if not os.path.exists(cert_path):
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    with open(cert_path) as f:
        return json.load(f)


@router.delete("/file/{filename}")
async def delete_file(filename: str, user_id: str = Depends(require_session)):
    """Delete file from vault."""
    vault_dir = get_user_vault_dir(user_id)
    filepath = os.path.join(vault_dir, filename)
    cert_path = filepath + ".cert.json"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(filepath)
    if os.path.exists(cert_path):
        os.remove(cert_path)
    
    return {"status": "deleted", "filename": filename}


@router.get("/verify/{filename}")
async def verify_file(filename: str, user_id: str = Depends(require_session)):
    """Verify file integrity against certificate."""
    vault_dir = get_user_vault_dir(user_id)
    filepath = os.path.join(vault_dir, filename)
    cert_path = filepath + ".cert.json"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(cert_path):
        raise HTTPException(status_code=404, detail="No certificate for file")
    
    # Read current file hash
    with open(filepath, "rb") as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    
    # Read certificate
    with open(cert_path) as f:
        cert = json.load(f)
    
    original_hash = cert.get("sha256")
    
    return {
        "filename": filename,
        "verified": current_hash == original_hash,
        "current_hash": current_hash,
        "original_hash": original_hash,
        "certificate": cert
    }
