"""
Dakota County Eviction Defense - PDF Generation Service
Uses WeasyPrint for high-quality court-ready PDF documents.
"""

import io
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Try WeasyPrint, fallback to basic HTML export
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("[WARN] WeasyPrint not installed - PDF generation will use fallback")


def generate_pdf_from_html(html_content: str, css_content: Optional[str] = None) -> bytes:
    """Generate PDF from HTML string."""
    if not WEASYPRINT_AVAILABLE:
        # Fallback: return HTML as bytes
        return html_content.encode('utf-8')
    
    stylesheets = []
    if css_content:
        stylesheets.append(CSS(string=css_content))
    
    # Add default court document styling
    stylesheets.append(CSS(string=COURT_DOCUMENT_CSS))
    
    html = HTML(string=html_content)
    return html.write_pdf(stylesheets=stylesheets)


def generate_answer_pdf(data: Dict[str, Any], lang: str = "en") -> bytes:
    """Generate Answer to Eviction PDF."""
    html = render_answer_html(data, lang)
    return generate_pdf_from_html(html)


def generate_counterclaim_pdf(data: Dict[str, Any], lang: str = "en") -> bytes:
    """Generate Counterclaim PDF."""
    html = render_counterclaim_html(data, lang)
    return generate_pdf_from_html(html)


def generate_motion_pdf(motion_type: str, data: Dict[str, Any], lang: str = "en") -> bytes:
    """Generate Motion PDF (dismiss, continuance, stay, etc.)."""
    html = render_motion_html(motion_type, data, lang)
    return generate_pdf_from_html(html)


def generate_hearing_prep_pdf(data: Dict[str, Any], lang: str = "en") -> bytes:
    """Generate Hearing Preparation checklist PDF."""
    html = render_hearing_prep_html(data, lang)
    return generate_pdf_from_html(html)


# ============================================================================
# HTML Rendering Functions
# ============================================================================

def render_answer_html(data: Dict[str, Any], lang: str = "en") -> str:
    """Render Answer to Eviction HTML."""
    tenant_name = data.get("tenant_name", "")
    landlord_name = data.get("landlord_name", "")
    case_number = data.get("case_number", "")
    address = data.get("address", "")
    served_date = data.get("served_date", "")
    defenses = data.get("defenses", [])
    defense_details = data.get("defense_details", "")
    
    defenses_html = ""
    for defense in defenses:
        defenses_html += f'<li class="defense-item">{defense}</li>'
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <title>Answer to Eviction Complaint</title>
    </head>
    <body>
        <header class="court-header">
            <div class="court-info">
                STATE OF MINNESOTA<br>
                COUNTY OF DAKOTA<br>
                FOURTH JUDICIAL DISTRICT
            </div>
            <div class="case-info">
                Case No: {case_number}
            </div>
        </header>
        
        <h1 class="document-title">ANSWER TO EVICTION COMPLAINT</h1>
        
        <section class="parties">
            <p><strong>{landlord_name}</strong>, Plaintiff(s)</p>
            <p>vs.</p>
            <p><strong>{tenant_name}</strong>, Defendant(s)</p>
        </section>
        
        <section class="content">
            <p>The Defendant(s), residing at <strong>{address}</strong>, hereby responds to the Eviction Complaint as follows:</p>
            
            <h2>DEFENSES</h2>
            <ol class="defenses-list">
                {defenses_html}
            </ol>
            
            <h2>STATEMENT OF FACTS</h2>
            <p>{defense_details}</p>
            
            <h2>RELIEF REQUESTED</h2>
            <p>Defendant respectfully requests that this Court:</p>
            <ol>
                <li>Dismiss the eviction complaint with prejudice;</li>
                <li>Award Defendant costs and disbursements;</li>
                <li>Grant such other relief as the Court deems just and equitable.</li>
            </ol>
        </section>
        
        <section class="signature">
            <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
            <br><br>
            <p>_______________________________</p>
            <p>{tenant_name}, Defendant</p>
            <p>{address}</p>
        </section>
        
        <footer class="filing-info">
            <p><strong>Date Served:</strong> {served_date}</p>
            <p><em>This Answer must be filed with the Court within 7 days of service.</em></p>
        </footer>
    </body>
    </html>
    """


def render_counterclaim_html(data: Dict[str, Any], lang: str = "en") -> str:
    """Render Counterclaim HTML."""
    tenant_name = data.get("tenant_name", "")
    landlord_name = data.get("landlord_name", "")
    case_number = data.get("case_number", "")
    address = data.get("address", "")
    claims = data.get("claims", [])
    damages_requested = data.get("damages_requested", "")
    claim_details = data.get("claim_details", "")
    
    claims_html = ""
    for i, claim in enumerate(claims, 1):
        claims_html += f'<li><strong>Count {i}:</strong> {claim}</li>'
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <title>Tenant Counterclaim</title>
    </head>
    <body>
        <header class="court-header">
            <div class="court-info">
                STATE OF MINNESOTA<br>
                COUNTY OF DAKOTA<br>
                FOURTH JUDICIAL DISTRICT
            </div>
            <div class="case-info">
                Case No: {case_number}
            </div>
        </header>
        
        <h1 class="document-title">TENANT COUNTERCLAIM</h1>
        
        <section class="parties">
            <p><strong>{tenant_name}</strong>, Counter-Plaintiff</p>
            <p>vs.</p>
            <p><strong>{landlord_name}</strong>, Counter-Defendant</p>
        </section>
        
        <section class="content">
            <p>The Counter-Plaintiff (Tenant), residing at <strong>{address}</strong>, hereby files this Counterclaim against the Counter-Defendant (Landlord) and states as follows:</p>
            
            <h2>CLAIMS</h2>
            <ol class="claims-list">
                {claims_html}
            </ol>
            
            <h2>STATEMENT OF FACTS</h2>
            <p>{claim_details}</p>
            
            <h2>DAMAGES</h2>
            <p>Counter-Plaintiff has suffered damages in the amount of: <strong>{damages_requested}</strong></p>
            
            <h2>RELIEF REQUESTED</h2>
            <p>Counter-Plaintiff respectfully requests that this Court:</p>
            <ol>
                <li>Enter judgment against Counter-Defendant for the amount of damages stated;</li>
                <li>Award Counter-Plaintiff costs and attorney fees if applicable;</li>
                <li>Grant such other relief as the Court deems just and equitable.</li>
            </ol>
        </section>
        
        <section class="signature">
            <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
            <br><br>
            <p>_______________________________</p>
            <p>{tenant_name}, Counter-Plaintiff</p>
            <p>{address}</p>
        </section>
        
        <footer class="filing-info">
            <p><em>File this Counterclaim with your Answer within 7 days of service.</em></p>
        </footer>
    </body>
    </html>
    """


def render_motion_html(motion_type: str, data: Dict[str, Any], lang: str = "en") -> str:
    """Render Motion HTML (dismiss, continuance, stay)."""
    tenant_name = data.get("tenant_name", "")
    landlord_name = data.get("landlord_name", "")
    case_number = data.get("case_number", "")
    grounds = data.get("grounds", "")
    hearing_date = data.get("hearing_date", "")
    
    motion_titles = {
        "dismiss": "MOTION TO DISMISS",
        "continuance": "MOTION FOR CONTINUANCE",
        "stay": "MOTION TO STAY WRIT OF RECOVERY",
        "fee_waiver": "APPLICATION FOR WAIVER OF FILING FEES"
    }
    
    title = motion_titles.get(motion_type, "MOTION")
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        <header class="court-header">
            <div class="court-info">
                STATE OF MINNESOTA<br>
                COUNTY OF DAKOTA<br>
                FOURTH JUDICIAL DISTRICT
            </div>
            <div class="case-info">
                Case No: {case_number}
            </div>
        </header>
        
        <h1 class="document-title">{title}</h1>
        
        <section class="parties">
            <p><strong>{landlord_name}</strong>, Plaintiff(s)</p>
            <p>vs.</p>
            <p><strong>{tenant_name}</strong>, Defendant(s)</p>
        </section>
        
        <section class="content">
            <p>Defendant <strong>{tenant_name}</strong> respectfully moves this Court for the following relief:</p>
            
            <h2>GROUNDS FOR MOTION</h2>
            <p>{grounds}</p>
            
            <h2>RELIEF REQUESTED</h2>
            <p>Defendant requests that this Court grant the motion and provide appropriate relief.</p>
        </section>
        
        <section class="signature">
            <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
            <p>Hearing Date: {hearing_date}</p>
            <br><br>
            <p>_______________________________</p>
            <p>{tenant_name}, Defendant</p>
        </section>
    </body>
    </html>
    """


def render_hearing_prep_html(data: Dict[str, Any], lang: str = "en") -> str:
    """Render Hearing Preparation checklist HTML."""
    tenant_name = data.get("tenant_name", "")
    hearing_date = data.get("hearing_date", "")
    hearing_time = data.get("hearing_time", "")
    is_zoom = data.get("is_zoom", False)
    checklist_items = data.get("checklist_items", [])
    documents_needed = data.get("documents_needed", [])
    
    checklist_html = ""
    for item in checklist_items:
        checklist_html += f'<li>☐ {item}</li>'
    
    docs_html = ""
    for doc in documents_needed:
        docs_html += f'<li>☐ {doc}</li>'
    
    zoom_section = ""
    if is_zoom:
        zoom_section = """
        <h2>ZOOM COURT PREPARATION</h2>
        <ul>
            <li>☐ Test your internet connection</li>
            <li>☐ Install Zoom (if not already installed)</li>
            <li>☐ Test your camera and microphone</li>
            <li>☐ Find a quiet, well-lit location</li>
            <li>☐ Have your documents ready to screen share</li>
            <li>☐ Join 15 minutes early</li>
            <li>☐ Dress professionally</li>
            <li>☐ Keep phone number ready as backup audio</li>
        </ul>
        """
    
    return f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <title>Hearing Preparation Checklist</title>
    </head>
    <body>
        <h1 class="document-title">HEARING PREPARATION CHECKLIST</h1>
        
        <section class="hearing-info">
            <p><strong>Tenant:</strong> {tenant_name}</p>
            <p><strong>Hearing Date:</strong> {hearing_date}</p>
            <p><strong>Hearing Time:</strong> {hearing_time}</p>
            <p><strong>Format:</strong> {"Zoom (Virtual)" if is_zoom else "In-Person"}</p>
        </section>
        
        <section class="checklist">
            <h2>GENERAL CHECKLIST</h2>
            <ul>
                {checklist_html}
            </ul>
            
            <h2>DOCUMENTS TO BRING</h2>
            <ul>
                {docs_html}
            </ul>
            
            {zoom_section}
        </section>
        
        <section class="tips">
            <h2>IMPORTANT REMINDERS</h2>
            <ul>
                <li>Arrive/connect 15 minutes early</li>
                <li>Address the judge as "Your Honor"</li>
                <li>Speak clearly and only when asked</li>
                <li>Do not interrupt the landlord or judge</li>
                <li>Stick to the facts - avoid emotional arguments</li>
                <li>If you don't understand something, ask for clarification</li>
            </ul>
        </section>
        
        <footer>
            <p><em>Generated by Semptify Dakota County Eviction Defense System</em></p>
            <p><em>Date: {datetime.now().strftime('%B %d, %Y')}</em></p>
        </footer>
    </body>
    </html>
    """


# ============================================================================
# Default Court Document CSS
# ============================================================================

COURT_DOCUMENT_CSS = """
@page {
    size: letter;
    margin: 1in;
}

body {
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000;
}

.court-header {
    text-align: center;
    margin-bottom: 24pt;
    border-bottom: 2px solid #000;
    padding-bottom: 12pt;
}

.court-info {
    font-weight: bold;
    margin-bottom: 8pt;
}

.case-info {
    font-size: 10pt;
    margin-top: 8pt;
}

.document-title {
    text-align: center;
    font-size: 14pt;
    font-weight: bold;
    text-transform: uppercase;
    margin: 24pt 0;
}

.parties {
    margin: 24pt 0;
    padding: 12pt;
    border: 1px solid #ccc;
}

.parties p {
    margin: 8pt 0;
}

.content {
    margin: 24pt 0;
}

.content h2 {
    font-size: 12pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 18pt;
    margin-bottom: 8pt;
}

.content ol, .content ul {
    margin-left: 24pt;
}

.content li {
    margin-bottom: 8pt;
}

.signature {
    margin-top: 48pt;
}

.filing-info {
    margin-top: 24pt;
    padding-top: 12pt;
    border-top: 1px solid #ccc;
    font-size: 10pt;
}

footer {
    margin-top: 36pt;
    font-size: 10pt;
    color: #666;
}

/* RTL support for Arabic */
[dir="rtl"] {
    direction: rtl;
    text-align: right;
}

[dir="rtl"] .content ol, [dir="rtl"] .content ul {
    margin-left: 0;
    margin-right: 24pt;
}
"""
