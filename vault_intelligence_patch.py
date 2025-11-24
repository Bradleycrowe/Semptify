"""
Add this code to vault.py after the certificate is saved.

Insert after the line: _write_json(cert_path, cert)
"""

INTELLIGENCE_PROCESSING_CODE = '''
    # ====================================================================
    # DOCUMENT INTELLIGENCE PROCESSING (Auto-extract legal details)
    # ====================================================================
    try:
        from document_intelligence import DocumentIntelligenceEngine
        import tempfile
        
        # Create temp file for analysis (decrypt temporarily)
        with tempfile.NamedTemporaryFile(mode='wb', suffix=f'_{filename}', delete=False) as tmp:
            tmp.write(file_data)  # Use original unencrypted data
            tmp_path = tmp.name
        
        # Process document
        intel_engine = DocumentIntelligenceEngine()
        doc_intel = intel_engine.process_document(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        if doc_intel:
            # Save intelligence results
            intel_data = {
                "doc_id": doc_id,
                "doc_type": doc_intel.doc_type,
                "confidence": doc_intel.confidence,
                "contacts": [
                    {
                        "name": c.name,
                        "address": c.address,
                        "phone": c.phone,
                        "email": c.email,
                        "role": c.role
                    } for c in doc_intel.contacts
                ],
                "signatures": [
                    {
                        "signer_name": s.signer_name,
                        "date_signed": s.date_signed,
                        "is_notarized": s.is_notarized,
                        "is_witnessed": s.is_witnessed
                    } for s in doc_intel.signatures
                ],
                "contract_terms": {
                    "rent_amount": doc_intel.contract_terms.rent_amount if doc_intel.contract_terms else None,
                    "security_deposit": doc_intel.contract_terms.security_deposit if doc_intel.contract_terms else None,
                    "start_date": doc_intel.contract_terms.start_date if doc_intel.contract_terms else None,
                    "end_date": doc_intel.contract_terms.end_date if doc_intel.contract_terms else None,
                } if doc_intel.contract_terms else None,
                "jurisdiction": {
                    "state": doc_intel.jurisdiction.state,
                    "county": doc_intel.jurisdiction.county,
                    "governing_law": doc_intel.jurisdiction.governing_law,
                } if doc_intel.jurisdiction else None,
                "legal_validation": {
                    "status": doc_intel.legal_validation.status.value if doc_intel.legal_validation else "unknown",
                    "issues": doc_intel.legal_validation.issues if doc_intel.legal_validation else [],
                    "warnings": doc_intel.legal_validation.warnings if doc_intel.legal_validation else []
                } if doc_intel.legal_validation else None,
                "extracted_dates": doc_intel.extracted_dates,
                "extracted_amounts": doc_intel.extracted_amounts,
                "processed_at": datetime.now().isoformat()
            }
            
            # Save to intelligence.json
            intel_path = os.path.join(doc_dir, "intelligence.json")
            _write_json(intel_path, intel_data)
            
            # Add intelligence summary to certificate
            cert["intelligence"] = {
                "available": True,
                "doc_type": doc_intel.doc_type,
                "confidence": doc_intel.confidence,
                "contacts_found": len(doc_intel.contacts),
                "signatures_found": len(doc_intel.signatures),
                "legal_status": doc_intel.legal_validation.status.value if doc_intel.legal_validation else "unknown"
            }
            
            # Re-save certificate with intelligence info
            _write_json(cert_path, cert)
            
    except Exception as e:
        # Log error but don't fail upload
        print(f"[WARN] Document intelligence processing failed: {e}")
        cert["intelligence"] = {"available": False, "error": str(e)}
        _write_json(cert_path, cert)
'''

print("=" * 70)
print("DOCUMENT INTELLIGENCE INTEGRATION CODE")
print("=" * 70)
print("\nAdd this to vault.py after: _write_json(cert_path, cert)")
print(INTELLIGENCE_PROCESSING_CODE)
