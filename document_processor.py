"""
Document Processor (Dprocessor)
All documents going to the Drepo (Document Repo) pass through here.
Future: OCR, categorization, AI analysis, metadata extraction, etc.
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional


def process_document(file_data: bytes, filename: str, user_token: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process a document before storage in the Document Repo.
    
    Args:
        file_data: Raw file bytes
        filename: Original filename
        user_token: User's anonymous token
        metadata: Optional metadata dict
    
    Returns:
        Dict with processed file info and any extracted metadata
    """
    result = {
        'original_filename': filename,
        'processed_at': datetime.utcnow().isoformat(),
        'size_bytes': len(file_data),
        'user_token': user_token,
        'processor_version': '1.0.0',
        'metadata': metadata or {}
    }
    
    # Future enhancements:
    # - OCR for scanned documents
    # - AI categorization (lease, notice, receipt, etc.)
    # - Metadata extraction (dates, landlord names, amounts)
    # - Text extraction for search
    # - Thumbnail generation
    # - Virus scanning
    
    # For now, just pass through with basic info
    result['processed_data'] = file_data
    result['processing_status'] = 'pass_through'
    
    return result


def validate_document(filename: str, file_size: int) -> tuple[bool, Optional[str]]:
    """
    Validate document before processing.
    
    Returns:
        (is_valid, error_message)
    """
    # Check file extension
    allowed_extensions = {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif',
        '.doc', '.docx', '.txt', '.rtf',
        '.xls', '.xlsx', '.csv'
    }
    
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        return False, f"File type {ext} not allowed. Allowed: {', '.join(allowed_extensions)}"
    
    # Check file size (50MB max)
    max_size = 50 * 1024 * 1024
    if file_size > max_size:
        return False, f"File too large ({file_size / 1024 / 1024:.1f}MB). Maximum: 50MB"
    
    return True, None


def categorize_document(filename: str) -> str:
    """
    Simple filename-based categorization.
    Future: Use AI to analyze content.
    """
    filename_lower = filename.lower()
    
    if any(word in filename_lower for word in ['lease', 'rental', 'agreement']):
        return 'lease'
    elif any(word in filename_lower for word in ['notice', 'eviction', 'warning']):
        return 'notice'
    elif any(word in filename_lower for word in ['receipt', 'payment', 'rent']):
        return 'receipt'
    elif any(word in filename_lower for word in ['photo', 'image', 'picture', 'damage']):
        return 'evidence'
    else:
        return 'other'


# Future: Add integration points for:
# - Complaint filing system (auto-populate from processed docs)
# - Timeline events (extract dates from documents)
# - Learning system (suggest relevant resources based on doc type)
# - AI Copilot (answer questions about uploaded documents)

# ================== Phase 1 Extensions (ID, Extraction, Sidecar) ==================
import re, json, hashlib
from document_model import build_metadata, DocumentMetadata, ExtractionEntities

_PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_DATE_RE = re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b")
_MONEY_RE = re.compile(r"\b\$\d{1,4}(?:,\d{3})*(?:\.\d{2})?\b")

CATEGORY_HINTS = {
    'late_fee': ['late fee', 'fee applied', 'past due'],
    'rent_due': ['rent due', 'due on', 'monthly rent'],
    'notice': ['notice', 'eviction', 'vacate'],
    'thank_you': ['thank you', 'appreciate', 'gratitude'],
    'maintenance': ['repair', 'maintenance', 'fix', 'work order'],
}


def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext in ('.txt', '.csv', '.rtf'):  # naive
        try:
            return file_bytes.decode(errors='replace')
        except Exception:
            return ''
    # Future: PDF text, OCR images, docx parsing
    return ''


def smart_category(initial: str, text: str) -> str:
    if not text:
        return initial
    lowered = text.lower()
    for cat, hints in CATEGORY_HINTS.items():
        for h in hints:
            if h in lowered:
                return cat
    return initial


def extract_entities(text: str) -> ExtractionEntities:
    ents = ExtractionEntities()
    if not text:
        return ents
    for m in _PHONE_RE.findall(text):
        ents.contacts.append({'type': 'phone', 'value': m})
    for m in _EMAIL_RE.findall(text):
        ents.contacts.append({'type': 'email', 'value': m})
    for m in _DATE_RE.findall(text):
        # naive; future: parse to ISO
        ents.dates.append({'value': m, 'role': 'mentioned'})
    for m in _MONEY_RE.findall(text):
        amt = m.replace('$','').replace(',','')
        ents.amounts.append({'value': amt, 'currency': 'USD', 'context': 'mentioned'})
    return ents


def derive_deadlines(entities: ExtractionEntities, text: str) -> list[dict]:
    deadlines = []
    if not text:
        return deadlines
    lower = text.lower()
    if 'due on' in lower or 'rent due' in lower:
        # naive pick first date
        if entities.dates:
            deadlines.append({'due_date': entities.dates[0]['value'], 'label': 'rent_due'})
    if 'pay by' in lower and entities.dates:
        deadlines.append({'due_date': entities.dates[0]['value'], 'label': 'payment_deadline'})
    return deadlines


def create_sidecar(meta: DocumentMetadata, storage_path: str):
    sidecar_path = os.path.join(storage_path, f"{meta.doc_id}.json")
    with open(sidecar_path, 'w', encoding='utf-8') as f:
        json.dump(meta.to_dict(), f, indent=2)
    return sidecar_path


def process_and_build_metadata(file_bytes: bytes, filename: str, user_token: str, source_type: str = 'upload') -> DocumentMetadata:
    # Keep existing categorize logic
    base_category = categorize_document(filename)
    text = extract_text(file_bytes, filename)
    refined_category = smart_category(base_category, text)
    entities = extract_entities(text)
    deadlines = derive_deadlines(entities, text)

    stored_filename = filename  # future: sanitized unique path
    meta = build_metadata(file_bytes, filename, stored_filename, refined_category, source_type=source_type)
    meta.entities = entities
    meta.deadlines = deadlines
    # user_token not stored in metadata for privacy
    return meta
