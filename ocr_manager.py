"""
OCR Document Manager - Extract text from images and PDFs, auto-tag documents.
Uses simple pattern matching for now; can be upgraded to ML-based OCR.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List
import hashlib
import re


def extract_text_placeholder(file_path: str) -> str:
    """
    Placeholder for OCR extraction. In production, use pytesseract or cloud OCR.
    For now, returns empty string to demonstrate flow.
    """
    # TODO: Implement actual OCR with pytesseract or Azure OCR
    # import pytesseract
    # from PIL import Image
    # return pytesseract.image_to_string(Image.open(file_path))
    return ""


def detect_document_type(text: str, filename: str = '') -> str:
    """Detect document type from text and filename."""
    text_lower = text.lower()
    filename_lower = filename.lower()
    
    if any(kw in text_lower for kw in ['lease', 'tenancy agreement', 'rental agreement']):
        return 'lease'
    elif any(kw in text_lower for kw in ['eviction', 'notice to vacate', 'termination']):
        return 'eviction_notice'
    elif any(kw in text_lower for kw in ['receipt', 'payment', 'rent paid']):
        return 'receipt'
    elif any(kw in text_lower for kw in ['repair', 'maintenance', 'work order']):
        return 'repair_request'
    elif 'invoice' in text_lower or 'invoice' in filename_lower:
        return 'invoice'
    elif any(kw in text_lower for kw in ['court', 'summons', 'complaint', 'petition']):
        return 'court_document'
    else:
        return 'general'


def extract_key_info(text: str) -> Dict[str, Any]:
    """Extract key information like dates, amounts, addresses."""
    info = {}
    
    # Extract dates (YYYY-MM-DD or MM/DD/YYYY)
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',
        r'\d{1,2}/\d{1,2}/\d{4}'
    ]
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))
    if dates:
        info['dates'] = dates[:3]  # First 3 dates found
    
    # Extract dollar amounts
    amounts = re.findall(r'\$[\d,]+\.?\d*', text)
    if amounts:
        info['amounts'] = amounts[:5]
    
    # Extract addresses (simple pattern)
    address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Way|Boulevard|Blvd)'
    addresses = re.findall(address_pattern, text, re.IGNORECASE)
    if addresses:
        info['addresses'] = addresses[:2]
    
    return info


def auto_tag_document(text: str, filename: str = '') -> List[str]:
    """Generate tags for a document based on content."""
    tags = []
    
    doc_type = detect_document_type(text, filename)
    tags.append(doc_type)
    
    text_lower = text.lower()
    
    # Add relevant tags
    if 'urgent' in text_lower or 'immediate' in text_lower:
        tags.append('urgent')
    if any(kw in text_lower for kw in ['repair', 'maintenance', 'fix']):
        tags.append('maintenance')
    if any(kw in text_lower for kw in ['rent', 'payment']):
        tags.append('payment')
    if any(kw in text_lower for kw in ['notice', 'violation']):
        tags.append('notice')
    if any(kw in text_lower for kw in ['lease', 'agreement']):
        tags.append('lease')
    
    return list(set(tags))  # Remove duplicates


def process_document(file_path: str, user_id: str, data_dir: str = 'data') -> Dict[str, Any]:
    """
    Process a document: extract text, detect type, tag, and save metadata.
    
    Returns:
        Dict with extracted_text, doc_type, tags, key_info, metadata_path
    """
    filename = os.path.basename(file_path)
    
    # Extract text (placeholder for now)
    extracted_text = extract_text_placeholder(file_path)
    
    # For demo, use filename as text if OCR returns empty
    if not extracted_text:
        extracted_text = filename
    
    doc_type = detect_document_type(extracted_text, filename)
    tags = auto_tag_document(extracted_text, filename)
    key_info = extract_key_info(extracted_text)
    
    # Generate document ID
    doc_id = hashlib.sha256(
        f"{user_id}{filename}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    
    metadata = {
        'doc_id': doc_id,
        'user_id': user_id,
        'filename': filename,
        'file_path': file_path,
        'doc_type': doc_type,
        'tags': tags,
        'key_info': key_info,
        'processed_at': datetime.now().isoformat(),
        'text_length': len(extracted_text),
        'has_ocr': len(extracted_text) > 0
    }
    
    # Save metadata
    ocr_dir = os.path.join(data_dir, 'ocr', user_id)
    os.makedirs(ocr_dir, exist_ok=True)
    
    metadata_path = os.path.join(ocr_dir, f"{doc_id}_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Save extracted text
    text_path = os.path.join(ocr_dir, f"{doc_id}_text.txt")
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    
    return metadata


def search_documents(user_id: str, query: str, data_dir: str = 'data') -> List[Dict[str, Any]]:
    """Search documents by text or tags."""
    ocr_dir = os.path.join(data_dir, 'ocr', user_id)
    if not os.path.exists(ocr_dir):
        return []
    
    results = []
    query_lower = query.lower()
    
    for filename in os.listdir(ocr_dir):
        if filename.endswith('_metadata.json'):
            with open(os.path.join(ocr_dir, filename), 'r') as f:
                metadata = json.load(f)
            
            # Check if query matches tags or doc_type
            if query_lower in metadata.get('doc_type', '').lower():
                results.append(metadata)
            elif any(query_lower in tag.lower() for tag in metadata.get('tags', [])):
                results.append(metadata)
            else:
                # Search in extracted text
                text_path = os.path.join(ocr_dir, f"{metadata['doc_id']}_text.txt")
                if os.path.exists(text_path):
                    with open(text_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    if query_lower in text.lower():
                        results.append(metadata)
    
    return results


# Demo/test
if __name__ == "__main__":
    print("OCR Document Manager - Demo\n")
    
    # Simulate document processing
    test_text = """
    LEASE AGREEMENT
    Property Address: 123 Main Street, Apt 4B
    Tenant: John Doe
    Monthly Rent: $1,200
    Lease Start Date: 2025-01-01
    Lease End Date: 2025-12-31
    """
    
    doc_type = detect_document_type(test_text)
    tags = auto_tag_document(test_text)
    key_info = extract_key_info(test_text)
    
    print(f"Document Type: {doc_type}")
    print(f"Tags: {', '.join(tags)}")
    print(f"Key Info: {key_info}")
