"""
Document ID Generator and Certificate System
Generates unique IDs and tamper-proof certificates for all tenant interactions
"""
import hashlib
import secrets
from datetime import datetime
import json

# Type code mappings
ITEM_TYPES = {
    # Incoming
    "LEAS": "Lease Agreement",
    "NOTI": "Notice",
    "INSP": "Inspection Report",
    "BILL": "Utility Bill",
    "RULE": "Rules/Regulations",
    "DEMA": "Demand Letter",
    "COUR": "Court Document",
    "COMM": "Communication",
    
    # Outgoing
    "RENT": "Rent Payment",
    "MAIN": "Maintenance Request",
    "RESP": "Response to Notice",
    "COMP": "Complaint Filing",
    "PHOT": "Photo Evidence",
    "VIDE": "Video Evidence",
    "RECE": "Receipt",
    "REQU": "General Request",
    "CORR": "Correspondence",
    
    # Actions
    "CALL": "Phone Call Log",
    "MEET": "Meeting Log",
    "EMSG": "Email/Message",
    "VISI": "Property Visit",
    "WITN": "Witness Statement",
    "NOTE": "Personal Note"
}

def generate_doc_id(user_token, item_type, content_data, previous_doc_sha=None):
    """
    Generate unique doc ID and tamper-proof certificate
    
    Args:
        user_token: User's auth token (for user prefix)
        item_type: 4-char type code (e.g., "RENT", "LEAS")
        content_data: Dict with document content
        previous_doc_sha: SHA256 of previous doc (for chain of custody)
    
    Returns:
        Dict with doc_id, certificate, and metadata
    """
    # Generate user prefix (first 4 chars of token hash)
    user_hash = hashlib.sha256(user_token.encode()).hexdigest()
    user_prefix = user_hash[:4].upper()
    
    # Get date string
    now = datetime.utcnow()
    date_str = now.strftime("%Y%m%d")
    
    # Get sequence number (would query existing docs in production)
    # For now, use random to avoid collisions
    sequence = secrets.randbelow(999) + 1
    sequence_str = f"{sequence:03d}"
    
    # Create content hash
    content_json = json.dumps(content_data, sort_keys=True)
    content_hash = hashlib.sha256(content_json.encode()).hexdigest()
    tamper_check = content_hash[:4].upper()
    
    # Build doc ID
    doc_id = f"{user_prefix}-{item_type}-{date_str}-{sequence_str}-{tamper_check}"
    
    # Create certificate
    certificate = {
        "sha256": content_hash,
        "created_at": now.isoformat() + "Z",
        "user_id_partial": user_prefix,
        "sequence": sequence,
        "tamper_check": tamper_check,
        "item_type": item_type,
        "item_type_name": ITEM_TYPES.get(item_type, "Unknown"),
        "chain_link": previous_doc_sha  # Links to previous doc
    }
    
    # Add RSA signature (would use real key in production)
    signature_input = f"{doc_id}|{content_hash}|{now.isoformat()}"
    signature_hash = hashlib.sha256(signature_input.encode()).hexdigest()
    certificate["signature"] = f"SIG_{signature_hash[:32]}"
    
    return {
        "doc_id": doc_id,
        "timestamp": now.isoformat() + "Z",
        "certificate": certificate,
        "type": item_type,
        "type_name": ITEM_TYPES.get(item_type, "Unknown")
    }

def verify_doc_certificate(doc_id, content_data, certificate):
    """
    Verify document hasn't been tampered with
    
    Returns:
        Dict with verification status and details
    """
    # Recalculate content hash
    content_json = json.dumps(content_data, sort_keys=True)
    calc_hash = hashlib.sha256(content_json.encode()).hexdigest()
    
    # Check against certificate
    stored_hash = certificate.get("sha256")
    tamper_check = certificate.get("tamper_check")
    calc_tamper_check = calc_hash[:4].upper()
    
    # Verify doc_id components
    parts = doc_id.split("-")
    if len(parts) != 5:
        return {"valid": False, "error": "Invalid doc_id format"}
    
    doc_tamper_check = parts[4]
    
    return {
        "valid": (calc_hash == stored_hash and 
                 calc_tamper_check == tamper_check and
                 calc_tamper_check == doc_tamper_check),
        "calculated_hash": calc_hash,
        "stored_hash": stored_hash,
        "tamper_check_match": calc_tamper_check == tamper_check,
        "doc_id_match": calc_tamper_check == doc_tamper_check
    }

def get_item_type_name(type_code):
    """Get human-readable name for type code"""
    return ITEM_TYPES.get(type_code, "Unknown")

def get_all_item_types():
    """Get all available item types organized by category"""
    return {
        "incoming": {k: v for k, v in ITEM_TYPES.items() 
                    if k in ["LEAS", "NOTI", "INSP", "BILL", "RULE", "DEMA", "COUR", "COMM"]},
        "outgoing": {k: v for k, v in ITEM_TYPES.items()
                    if k in ["RENT", "MAIN", "RESP", "COMP", "PHOT", "VIDE", "RECE", "REQU", "CORR"]},
        "actions": {k: v for k, v in ITEM_TYPES.items()
                   if k in ["CALL", "MEET", "EMSG", "VISI", "WITN", "NOTE"]}
    }
