"""
Dakota County Eviction Defense - ZIP Bundle Service
Creates court packet bundles with all forms and generated documents.
"""

import io
import os
import json
import zipfile
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


def create_defense_packet_zip(
    documents: List[Dict[str, Any]],
    forms: List[Dict[str, Any]],
    case_info: Dict[str, Any],
    include_instructions: bool = True
) -> bytes:
    """
    Create a ZIP bundle containing all defense documents.
    
    Args:
        documents: List of {"filename": str, "content": bytes, "type": str}
        forms: List of form metadata to include
        case_info: Case information dictionary
        include_instructions: Whether to include README with filing instructions
    
    Returns:
        ZIP file as bytes
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add case manifest
        manifest = {
            "case_number": case_info.get("case_number", ""),
            "tenant_name": case_info.get("tenant_name", ""),
            "landlord_name": case_info.get("landlord_name", ""),
            "generated_at": datetime.now().isoformat(),
            "documents": [
                {"filename": d["filename"], "type": d.get("type", "unknown")}
                for d in documents
            ],
            "forms_included": [f.get("id", "") for f in forms]
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))
        
        # Add generated documents
        for doc in documents:
            filename = doc.get("filename", "document.pdf")
            content = doc.get("content", b"")
            zf.writestr(f"generated/{filename}", content)
        
        # Add form references (URLs since we can't redistribute court forms)
        forms_readme = generate_forms_readme(forms)
        zf.writestr("forms/README.txt", forms_readme)
        
        # Add filing instructions
        if include_instructions:
            instructions = generate_filing_instructions(case_info)
            zf.writestr("FILING_INSTRUCTIONS.txt", instructions)
        
        # Add checklist
        checklist = generate_checklist(documents, forms, case_info)
        zf.writestr("CHECKLIST.txt", checklist)
    
    zip_buffer.seek(0)
    return zip_buffer.read()


def generate_forms_readme(forms: List[Dict[str, Any]]) -> str:
    """Generate README with links to official court forms."""
    lines = [
        "=" * 60,
        "OFFICIAL MINNESOTA COURT FORMS",
        "Dakota County - Fourth Judicial District",
        "=" * 60,
        "",
        "The following official court forms may be needed for your case.",
        "Download them from the Minnesota Judicial Branch website:",
        "",
    ]
    
    for form in forms:
        lines.append(f"Form {form.get('id', 'Unknown')}:")
        lines.append(f"  Name: {form.get('name', 'Unknown')}")
        lines.append(f"  URL: {form.get('url', 'N/A')}")
        if form.get('instructions'):
            lines.append(f"  Instructions: {form.get('instructions')}")
        if form.get('deadline_days'):
            lines.append(f"  Deadline: {form.get('deadline_days')} days from service")
        lines.append("")
    
    lines.extend([
        "",
        "IMPORTANT:",
        "- Download forms directly from mncourts.gov for the most current versions",
        "- Forms may be updated periodically",
        "- If a link doesn't work, search for the form number on mncourts.gov",
        "",
        "For assistance: Dakota County Court Administration",
        "Phone: 651-438-4325",
    ])
    
    return "\n".join(lines)


def generate_filing_instructions(case_info: Dict[str, Any]) -> str:
    """Generate step-by-step filing instructions."""
    tenant_name = case_info.get("tenant_name", "Tenant")
    case_number = case_info.get("case_number", "[Case Number]")
    hearing_date = case_info.get("hearing_date", "[Hearing Date]")
    
    return f"""
================================================================================
                        FILING INSTRUCTIONS
                    Dakota County Eviction Defense
================================================================================

Case Number: {case_number}
Tenant: {tenant_name}
Hearing Date: {hearing_date}

STEP 1: REVIEW YOUR DOCUMENTS
-----------------------------
Before filing, carefully review all documents in this packet:
- Check that your name and address are correct
- Verify the case number matches your eviction notice
- Read through all defenses and claims - make sure they are accurate

STEP 2: MAKE COPIES
-------------------
Make at least THREE copies of each document:
- Original (for the Court)
- Copy 1 (for the Landlord/Plaintiff)
- Copy 2 (for your records)

STEP 3: SIGN ALL DOCUMENTS
--------------------------
Sign and date each document where indicated. Use blue or black ink.

STEP 4: FILE WITH THE COURT
---------------------------
File your documents with:

    Dakota County Judicial Center
    1560 Highway 55
    Hastings, MN 55033
    
    OR
    
    Dakota County Western Service Center
    14955 Galaxie Ave
    Apple Valley, MN 55124

Court Hours: Monday-Friday, 8:00 AM - 4:30 PM

STEP 5: SERVE THE LANDLORD
--------------------------
After filing, you must serve a copy on the landlord or their attorney.
- Serve by mail (add 3 days to deadline)
- Serve in person (recommended)
- Keep proof of service

STEP 6: COMPLETE AFFIDAVIT OF SERVICE
--------------------------------------
Complete the Affidavit of Service form to prove you served the landlord.
File the completed affidavit with the Court.

DEADLINES - VERY IMPORTANT!
===========================
- Answer must be filed within 7 DAYS of being served
- Motions should be filed at least 3 DAYS before hearing
- Fee waiver should be filed FIRST if you cannot afford fees

NEED HELP?
==========
Free Legal Help:
- HomeLine Tenant Hotline: 612-728-5767
- Southern Minnesota Regional Legal Services: 651-222-5863
- Minnesota Legal Aid: lawhelpmn.org

Court Administration:
- Dakota County: 651-438-4325

================================================================================
This packet was generated by Semptify Dakota County Eviction Defense System.
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

DISCLAIMER: This provides legal information, not legal advice.
For legal advice specific to your situation, consult an attorney.
================================================================================
"""


def generate_checklist(
    documents: List[Dict[str, Any]],
    forms: List[Dict[str, Any]],
    case_info: Dict[str, Any]
) -> str:
    """Generate a filing checklist."""
    lines = [
        "=" * 50,
        "FILING CHECKLIST",
        "=" * 50,
        "",
        f"Case: {case_info.get('case_number', 'N/A')}",
        f"Hearing: {case_info.get('hearing_date', 'N/A')}",
        "",
        "DOCUMENTS IN THIS PACKET:",
        "-" * 30,
    ]
    
    for doc in documents:
        lines.append(f"[ ] {doc.get('filename', 'Unknown')}")
    
    lines.extend([
        "",
        "FORMS TO DOWNLOAD:",
        "-" * 30,
    ])
    
    for form in forms:
        lines.append(f"[ ] {form.get('id', '')}: {form.get('name', 'Unknown')}")
    
    lines.extend([
        "",
        "BEFORE FILING:",
        "-" * 30,
        "[ ] Review all documents for accuracy",
        "[ ] Sign and date all documents",
        "[ ] Make 3 copies of each document",
        "[ ] Gather filing fee or fee waiver",
        "",
        "AT THE COURTHOUSE:",
        "-" * 30,
        "[ ] File original with Court Clerk",
        "[ ] Get file-stamped copies back",
        "[ ] Serve copy on landlord/attorney",
        "[ ] Complete Affidavit of Service",
        "[ ] File Affidavit of Service with Court",
        "",
        "AFTER FILING:",
        "-" * 30,
        "[ ] Keep all file-stamped copies safe",
        "[ ] Note hearing date on calendar",
        "[ ] Prepare for hearing (see Hearing Prep guide)",
        "[ ] Gather evidence and witnesses",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ])
    
    return "\n".join(lines)


def create_single_document_download(
    content: bytes,
    filename: str,
    content_type: str = "application/pdf"
) -> Dict[str, Any]:
    """Prepare a single document for download."""
    return {
        "content": content,
        "filename": filename,
        "content_type": content_type,
        "size": len(content),
        "generated_at": datetime.now().isoformat()
    }
