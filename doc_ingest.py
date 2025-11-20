"""Document ingestion pipeline (Phase 1).
Accepts various source types, normalizes to bytes, builds metadata, stores sidecar.
Future: OCR (images/PDF), transcription (audio/video), email MIME parse, NLP classifier.
"""
import os, base64, email
from typing import Optional, Dict, Any, Tuple
from document_processor import process_and_build_metadata, create_sidecar
from document_model import DocumentMetadata

STORAGE_ROOT = 'uploads/drepo'

os.makedirs(STORAGE_ROOT, exist_ok=True)

class IngestResult:
    def __init__(self, meta: DocumentMetadata, sidecar_path: str, stored_file_path: str):
        self.meta = meta
        self.sidecar_path = sidecar_path
        self.stored_file_path = stored_file_path

    def to_dict(self):
        return {
            'doc_id': self.meta.doc_id,
            'stored_file': self.stored_file_path,
            'sidecar': self.sidecar_path,
            'category': self.meta.category,
            'deadlines': self.meta.deadlines,
            'entities': self.meta.entities.__dict__,
        }


def _ensure_user_dir(user_token: str) -> str:
    # Hash token to avoid exposing raw token path
    import hashlib
    safe_bucket = hashlib.sha256(user_token.encode()).hexdigest()[:24]
    path = os.path.join(STORAGE_ROOT, safe_bucket)
    os.makedirs(path, exist_ok=True)
    return path


def ingest_document(user_token: str, filename: str, source_type: str, payload: bytes | str) -> IngestResult:
    """Ingest a document from various sources.
    source_type: upload|image|audio|video|email|text|call|photo
    payload: raw bytes or text
    """
    # Normalize payload to bytes
    if isinstance(payload, str):
        file_bytes = payload.encode('utf-8', errors='replace')
    else:
        file_bytes = payload

    # Build metadata
    meta = process_and_build_metadata(file_bytes, filename, user_token, source_type=source_type)

    # Store original file (preserve exact bytes) using doc_id for uniqueness
    user_dir = _ensure_user_dir(user_token)
    stored_filename = f"{meta.doc_id}{os.path.splitext(filename)[1].lower() or '.bin'}"
    stored_path = os.path.join(user_dir, stored_filename)
    with open(stored_path, 'wb') as f:
        f.write(file_bytes)

    # Update stored filename in metadata (sidecar will reflect)
    meta.stored_filename = stored_filename

    # Write sidecar JSON
    sidecar_path = create_sidecar(meta, user_dir)

    return IngestResult(meta, sidecar_path, stored_path)

# Placeholder advanced ingestion helpers

def ingest_email(user_token: str, raw_email: str) -> IngestResult:
    msg = email.message_from_string(raw_email)
    subject = msg.get('Subject', 'email')
    payload_parts = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    payload_parts.append(part.get_payload(decode=True).decode(errors='replace'))
                except Exception:
                    pass
    else:
        try:
            payload_parts.append(msg.get_payload(decode=True).decode(errors='replace'))
        except Exception:
            pass
    body = '\n'.join(payload_parts)
    return ingest_document(user_token, subject + '.txt', 'email', body)


def ingest_text(user_token: str, text: str, hint_filename: str = 'note.txt') -> IngestResult:
    return ingest_document(user_token, hint_filename, 'text', text)


def ingest_base64_image(user_token: str, b64: str, hint_filename: str = 'image.png') -> IngestResult:
    try:
        raw = base64.b64decode(b64.split(',')[-1])
    except Exception:
        raw = b''
    return ingest_document(user_token, hint_filename, 'image', raw)

# Future: ingest_audio, ingest_video (transcription), ingest_call(log transcript)
