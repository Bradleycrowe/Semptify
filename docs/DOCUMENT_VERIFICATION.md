# Document Verification & Binding System

## Overview

SemptifyGUI implements a comprehensive document verification system that provides cryptographic binding and official verification for all user-created documents. This system ensures document integrity, non-repudiation, and complete audit trails.

## Key Features

### 1. Cryptographic Binding
Every document saved through the system receives a SHA-256 hash that cryptographically binds the content to its metadata. This ensures:
- **Integrity**: Any modification to the document will change its hash
- **Verification**: The original document can be verified against its certificate
- **Non-repudiation**: The hash proves the document existed at a specific point in time

### 2. Timestamping
Documents are timestamped using UTC ISO 8601 format with millisecond precision:
- **Creation timestamp**: When the document was saved
- **Evidence timestamp**: When the evidence was collected (may differ from creation)
- All timestamps are in UTC to avoid timezone confusion

### 3. Evidence Collection System
The Evidence Collection System (`static/js/evidence-system.js`) provides:
- **GPS Location Tracking**: Captures latitude, longitude, and accuracy
- **Audio Recording**: Records and downloads evidence with metadata
- **Voice Commands**: Hands-free operation for evidence collection
- **AI Assistance**: Context-aware help via `/api/evidence-copilot`

### 4. Certificate Structure

Each document is accompanied by a JSON certificate containing:

```json
{
  "type": "witness_statement",
  "file": "witness_20251011_123045.txt",
  "sha256": "abc123...",
  "user_id": "user_12345",
  "executed_date": "2025-10-11",
  "sig_name": "John Doe",
  "sig_consented": true,
  "ts": "2025-10-11T12:30:45.123Z",
  "ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "request_id": "req_xyz789",
  "evidence_collection": {
    "timestamp": "2025-10-11T12:30:00.000Z",
    "location": "40.7128,-74.0060 (±10m)",
    "location_accuracy": "10",
    "collection_user_agent": "Mozilla/5.0...",
    "has_location_data": true,
    "collection_method": "semptify_evidence_system"
  }
}
```

## Document Types Supported

1. **Witness Statements** (`/resources/witness_statement`)
   - Full name, contact, statement text
   - Unsworn declaration (28 U.S.C. § 1746)
   - Electronic signature with consent

2. **Filing Packets** (`/resources/filing_packet`)
   - Title, date, parties involved
   - Summary and key issues
   - Standard checklist for completeness

3. **Service Animal Requests** (`/resources/service_animal`)
   - Tenant and landlord details
   - Property address
   - Animal description and necessity

4. **Move Checklists** (`/resources/move_checklist`)
   - Move type (in/out)
   - Property address and date
   - Checklist items with photos, keys, walkthrough, etc.

## Evidence Panel Integration

Forms that support evidence collection include the `evidence_panel.html` template:

```html
{% include 'evidence_panel.html' %}
```

This provides:
- Real-time timestamp display
- Location tracking status
- Audio recording controls
- Voice command activation
- AI assistance button
- Location update button

## API Endpoints

### `/api/evidence-copilot` (POST)
Specialized endpoint for evidence collection AI assistance.

**Request:**
```json
{
  "prompt": "Help me document noise complaints",
  "location": "40.7128,-74.0060 (±10m)",
  "timestamp": "2025-10-11T12:30:00Z",
  "form_type": "witness_statement",
  "form_data": {
    "full_name": "John Doe",
    "statement": "Loud noise from upstairs..."
  }
}
```

**Response:**
```json
{
  "provider": "openai",
  "output": "For documenting noise complaints, you should:\n1. Record exact times and durations\n2. Capture audio evidence if possible\n3. Note specific details about the disturbance\n..."
}
```

## Verification Workflow

1. **Document Creation**
   - User fills out form with required information
   - Evidence system captures location and timestamp automatically
   - User provides electronic signature consent

2. **Preview**
   - User reviews formatted document
   - Evidence data is included in hidden form fields

3. **Save with Verification**
   - System generates SHA-256 hash of content
   - Creates certificate JSON with all metadata
   - Saves both document and certificate to user's vault
   - Logs event to structured event log

4. **Verification (Future)**
   - User or third party can verify document integrity
   - Compare SHA-256 hash of document with certificate
   - Review complete audit trail including evidence collection data

## Security Considerations

- **User Authentication**: All save operations require valid user token
- **CSRF Protection**: All form submissions include CSRF token validation
- **Rate Limiting**: Evidence copilot API is rate-limited to prevent abuse
- **Secure Storage**: Documents stored in per-user vault directories
- **Integrity**: SHA-256 hash ensures content hasn't been tampered with

## Legal Implications

### Unsworn Declarations
Witness statements include the unsworn declaration format per 28 U.S.C. § 1746:
> "I declare under penalty of perjury that the foregoing is true and correct."

This has the same legal weight as a sworn affidavit in many jurisdictions.

### Electronic Signatures
All documents require:
- Explicit consent checkbox for electronic signature use
- Typed full name as signature
- Timestamp of signature

This complies with the ESIGN Act and UETA for electronic signature validity.

### Evidence Chain of Custody
The certificate provides:
- Who created the document (user_id)
- When it was created (timestamp)
- Where it was created (IP, location)
- How it was created (user agent, collection method)
- What was created (SHA-256 hash of exact content)

This establishes a chain of custody for the evidence.

## Best Practices for Agents

When implementing document creation features:

1. **Always include evidence panel** in forms that benefit from verification
2. **Create certificate JSON** with all required fields
3. **Use `_sha256_hex(content)`** to hash document content
4. **Extract evidence fields** from form submission:
   - `evidence_timestamp`
   - `evidence_location`
   - `location_accuracy`
   - `evidence_user_agent`
5. **Log the event** using `_event_log()`
6. **Save to user vault** using `_vault_user_dir(user['id'])`

Example:
```python
cert = {
    'type': 'document_type',
    'file': filename,
    'sha256': _sha256_hex(content),
    'user_id': user['id'],
    'ts': _utc_now_iso(),
    'ip': request.remote_addr,
    'user_agent': request.headers.get('User-Agent'),
    'request_id': getattr(request, 'request_id', None),
    'evidence_collection': {
        'timestamp': evidence_timestamp or _utc_now_iso(),
        'location': evidence_location or 'Not provided',
        'location_accuracy': location_accuracy or 'Unknown',
        'collection_user_agent': evidence_user_agent or request.headers.get('User-Agent'),
        'has_location_data': bool(evidence_location),
        'collection_method': 'semptify_evidence_system'
    }
}
```

## Testing

The verification system is tested in:
- `tests/test_evidence_collection.py`: Evidence collection system
- `tests/test_evidence_system.py`: Evidence integration in forms
- `tests/test_vault.py`: Document storage and retrieval

Run all tests: `python -m pytest tests/ -v`

## Future Enhancements

Potential improvements to the verification system:
1. **Blockchain anchoring**: Store document hashes on blockchain for immutable proof
2. **Third-party timestamping**: Use RFC 3161 timestamp authorities
3. **Digital signatures**: Add cryptographic signatures using private keys
4. **Verification endpoint**: API to verify document certificates
5. **PDF generation**: Create verifiable PDFs with embedded certificates
6. **QR codes**: Add QR codes to documents linking to verification data
