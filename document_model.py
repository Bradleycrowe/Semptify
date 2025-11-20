"""Document metadata model and ID / integrity utilities.
Phase 1: Deterministic ID, tamper hash, optional HMAC signature.
Future: chain-of-custody, hash graph, CRDT merges.
"""
from __future__ import annotations
import hashlib, hmac, os, json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional, Any

DOCUMENT_SIGNATURE_KEY_ENV = 'DOCUMENT_SIGNATURE_KEY'


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate_document_id(content_bytes: bytes, original_filename: str) -> str:
    """Deterministic base ID: first 16 hex of sha256 + 4 char slug from filename.
    Keeps stable across re-uploads of identical content.
    """
    h = _sha256(content_bytes)
    stem = os.path.splitext(original_filename)[0].lower().replace(' ', '-')[:8]
    if not stem:
        stem = 'doc'
    stem = ''.join(c for c in stem if c.isalnum() or c == '-')
    return f"{h[:16]}-{stem}"  # base id


def hmac_sign(payload: Dict[str, Any]) -> Optional[str]:
    key = os.getenv(DOCUMENT_SIGNATURE_KEY_ENV)
    if not key:
        return None
    raw = json.dumps(payload, sort_keys=True).encode()
    return hmac.new(key.encode(), raw, hashlib.sha256).hexdigest()


def verify_hmac(payload: Dict[str, Any], signature: str) -> bool:
    key = os.getenv(DOCUMENT_SIGNATURE_KEY_ENV)
    if not key:
        return False
    raw = json.dumps(payload, sort_keys=True).encode()
    expected = hmac.new(key.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

@dataclass
class ExtractionEntities:
    contacts: List[Dict[str, str]] = field(default_factory=list)  # {'type': 'email|phone', 'value': '...'}
    dates: List[Dict[str, str]] = field(default_factory=list)      # {'value': iso, 'role': 'deadline|mentioned'}
    amounts: List[Dict[str, str]] = field(default_factory=list)    # {'value': '850.00', 'currency': 'USD', 'context': 'rent'}
    addresses: List[str] = field(default_factory=list)
    parties: List[str] = field(default_factory=list)

@dataclass
class DocumentMetadata:
    doc_id: str
    original_filename: str
    stored_filename: str
    sha256: str
    size_bytes: int
    category: str
    created_utc: str
    processor_version: str = '2.0.0'
    source_type: str = 'upload'  # upload|image|audio|video|email|text|call
    integrity_chain: List[str] = field(default_factory=list)  # previous version hashes
    entities: ExtractionEntities = field(default_factory=ExtractionEntities)
    deadlines: List[Dict[str, str]] = field(default_factory=list)  # {'due_date': iso, 'label': 'rent due'}
    related_docs: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    hmac_signature: Optional[str] = None  # optional integrity signature

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # flatten nested dataclass properly
        return d

    def sign(self):
        payload = self.to_dict().copy()
        payload.pop('hmac_signature', None)
        sig = hmac_sign(payload)
        if sig:
            self.hmac_signature = sig

    def verify(self) -> bool:
        if not self.hmac_signature:
            return False
        payload = self.to_dict().copy()
        payload.pop('hmac_signature', None)
        return verify_hmac(payload, self.hmac_signature)


def build_metadata(content_bytes: bytes, original_filename: str, stored_filename: str, category: str, source_type: str = 'upload') -> DocumentMetadata:
    sha = _sha256(content_bytes)
    doc_id = generate_document_id(content_bytes, original_filename)
    meta = DocumentMetadata(
        doc_id=doc_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        sha256=sha,
        size_bytes=len(content_bytes),
        category=category,
        created_utc=datetime.utcnow().isoformat() + 'Z',
        source_type=source_type,
    )
    meta.sign()  # sign if key present
    return meta

