"""
Complaint Filing + Context Integration
Auto-fills complaint forms using Context Data System intelligence.

This module bridges complaint_filing_routes.py and the Context API to:
1. Auto-populate complaint forms from uploaded documents
2. Extract party information (landlord, tenant) from lease documents
3. Suggest best evidence based on case strength analysis
4. Include perspective analysis in court packets
5. Rank evidence by legal significance

Usage:
    from complaint_filing_context_integration import auto_fill_complaint, suggest_evidence
    
    # Auto-fill complaint form for user 1
    filled_data = auto_fill_complaint(user_id='1', issue_type='eviction_defense')
    
    # Get ranked evidence suggestions
    evidence = suggest_evidence(user_id='1', case_type='eviction_defense')
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class ComplaintFormData:
    """Auto-filled complaint form data from Context System"""
    # Party information
    tenant_name: Optional[str] = None
    tenant_phone: Optional[str] = None
    tenant_email: Optional[str] = None
    tenant_address: Optional[str] = None
    
    landlord_name: Optional[str] = None
    landlord_company: Optional[str] = None
    landlord_phone: Optional[str] = None
    landlord_address: Optional[str] = None
    
    # Property information
    rental_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    
    # Financial information
    monthly_rent: Optional[float] = None
    security_deposit: Optional[float] = None
    amount_owed: Optional[float] = None
    
    # Timeline
    lease_start_date: Optional[str] = None
    lease_end_date: Optional[str] = None
    issue_start_date: Optional[str] = None
    notice_date: Optional[str] = None
    
    # Case details
    issue_description: Optional[str] = None
    case_strength: float = 0.0
    win_probability: float = 50.0
    
    # Evidence
    key_documents: List[str] = None
    timeline_events: List[Dict] = None
    
    # Confidence
    data_confidence: float = 0.0  # 0-100, how complete is the data
    extraction_source: str = "context_system"
    
    def __post_init__(self):
        if self.key_documents is None:
            self.key_documents = []
        if self.timeline_events is None:
            self.timeline_events = []


@dataclass
class EvidenceRecommendation:
    """Recommended evidence with ranking"""
    document_id: str
    filename: str
    doc_type: str
    relevance_score: float  # 0-100
    legal_significance: str
    reason: str
    perspective_scores: Optional[Dict] = None


def auto_fill_complaint(user_id: str, issue_type: str = 'eviction_defense') -> ComplaintFormData:
    """
    Auto-fill complaint form using Context Data System.
    
    Extracts information from:
    - Lease documents (parties, amounts, dates)
    - Timeline events (issue chronology)
    - Case strength analysis
    - Document intelligence
    
    Args:
        user_id: User ID to get context for
        issue_type: Type of complaint (eviction_defense, habitability, discrimination, etc.)
        
    Returns:
        ComplaintFormData with auto-filled fields
    """
    from semptify_core import get_context
    from document_intelligence import DocumentIntelligenceEngine
    import os
    
    # Get full context for user
    context = get_context(user_id)
    
    if not context:
        return ComplaintFormData()
    
    form_data = ComplaintFormData()
    form_data.case_strength = context.overall_strength
    
    # Extract timeline for issue description
    form_data.timeline_events = [
        {
            'date': e.event_date,
            'type': e.event_type,
            'title': e.title,
            'description': e.description
        }
        for e in sorted(context.timeline, key=lambda x: x.event_date)
    ]
    
    # Build issue description from timeline
    if form_data.timeline_events:
        descriptions = []
        for event in form_data.timeline_events[:5]:  # Top 5 most relevant
            descriptions.append(f"{event['date']}: {event['title']}")
        form_data.issue_description = "\n".join(descriptions)
        
        # Get key dates
        if form_data.timeline_events:
            # Find move-in date
            move_in = next((e for e in form_data.timeline_events if e['type'] == 'move_in'), None)
            if move_in:
                form_data.lease_start_date = move_in['date']
            
            # Find notice date
            notice = next((e for e in form_data.timeline_events if e['type'] == 'notice_received'), None)
            if notice:
                form_data.notice_date = notice['date']
            
            # Find first issue date
            issue_event = next((e for e in form_data.timeline_events 
                               if e['type'] in ['maintenance_request', 'complaint_filed', 'violation']), None)
            if issue_event:
                form_data.issue_start_date = issue_event['date']
    
    # Extract party information from lease documents
    lease_docs = [doc for doc in context.documents if doc.doc_type == 'lease']
    
    for lease in lease_docs:
        # Load intelligence.json if it exists
        intel_path = os.path.join(os.path.dirname(lease.filepath), f"{lease.id}_intelligence.json")
        
        if os.path.exists(intel_path):
            import json
            with open(intel_path, 'r') as f:
                intel = json.load(f)
            
            # Extract contacts (landlord/tenant)
            contacts = intel.get('contacts', [])
            for contact in contacts:
                role = contact.get('role', '').lower()
                if 'landlord' in role or 'lessor' in role or 'owner' in role:
                    form_data.landlord_name = contact.get('name')
                    form_data.landlord_phone = contact.get('phone')
                    form_data.landlord_address = contact.get('address')
                    if ',' in (form_data.landlord_name or ''):
                        # Might be "Company, Name" format
                        parts = form_data.landlord_name.split(',', 1)
                        form_data.landlord_company = parts[0].strip()
                        form_data.landlord_name = parts[1].strip() if len(parts) > 1 else form_data.landlord_name
                
                elif 'tenant' in role or 'lessee' in role or 'renter' in role:
                    form_data.tenant_name = contact.get('name')
                    form_data.tenant_phone = contact.get('phone')
                    form_data.tenant_email = contact.get('email')
            
            # Extract financial terms
            financial_terms = intel.get('financial_terms', [])
            for term in financial_terms:
                term_type = term.get('type', '').lower()
                if 'rent' in term_type and 'monthly' in term_type:
                    form_data.monthly_rent = term.get('amount')
                elif 'deposit' in term_type or 'security' in term_type:
                    form_data.security_deposit = term.get('amount')
            
            # Extract property address
            property_addr = intel.get('property_address')
            if property_addr:
                form_data.rental_address = property_addr.get('street')
                form_data.city = property_addr.get('city')
                form_data.state = property_addr.get('state')
                form_data.zip_code = property_addr.get('zip')
        
        else:
            # Fallback: Parse lease document directly
            try:
                with open(lease.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lease_text = f.read()
                
                # Extract rent amount ($X,XXX or $XXX)
                rent_match = re.search(r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', lease_text)
                if rent_match and not form_data.monthly_rent:
                    form_data.monthly_rent = float(rent_match.group(1).replace(',', ''))
                
                # Extract addresses (look for ZIP codes)
                zip_pattern = r'(\d{5}(?:-\d{4})?)'
                zips = re.findall(zip_pattern, lease_text)
                if zips and not form_data.zip_code:
                    form_data.zip_code = zips[0]
                
                # Extract names (look for "Tenant:" or "Landlord:")
                tenant_match = re.search(r'Tenant:?\s*([A-Z][a-z]+ [A-Z][a-z]+)', lease_text)
                if tenant_match and not form_data.tenant_name:
                    form_data.tenant_name = tenant_match.group(1)
                
                landlord_match = re.search(r'Landlord:?\s*([A-Z][a-z]+ [A-Z][a-z]+)', lease_text)
                if landlord_match and not form_data.landlord_name:
                    form_data.landlord_name = landlord_match.group(1)
            
            except Exception:
                pass
    
    # Calculate data confidence (how complete is the extraction)
    fields_filled = 0
    total_fields = 15
    
    if form_data.tenant_name: fields_filled += 1
    if form_data.landlord_name: fields_filled += 1
    if form_data.rental_address: fields_filled += 1
    if form_data.monthly_rent: fields_filled += 1
    if form_data.security_deposit: fields_filled += 1
    if form_data.lease_start_date: fields_filled += 1
    if form_data.issue_start_date: fields_filled += 1
    if form_data.issue_description: fields_filled += 1
    if form_data.landlord_phone: fields_filled += 1
    if form_data.tenant_phone: fields_filled += 1
    if form_data.city: fields_filled += 1
    if form_data.state: fields_filled += 1
    if form_data.zip_code: fields_filled += 1
    if form_data.timeline_events: fields_filled += 1
    if context.documents: fields_filled += 1
    
    form_data.data_confidence = (fields_filled / total_fields) * 100
    
    # Get case strength from perspective analysis if available
    form_data.key_documents = [doc.filename for doc in context.documents]
    
    return form_data


def suggest_evidence(user_id: str, case_type: str = 'eviction_defense', limit: int = 10) -> List[EvidenceRecommendation]:
    """
    Suggest and rank evidence documents for complaint filing.
    
    Uses:
    - Document intelligence (legal_significance, doc_type)
    - Perspective analysis scores
    - Timeline relevance
    
    Args:
        user_id: User ID
        case_type: Type of case
        limit: Maximum number of recommendations
        
    Returns:
        List of EvidenceRecommendation objects, sorted by relevance
    """
    from semptify_core import get_context
    import os
    
    context = get_context(user_id)
    
    if not context or not context.documents:
        return []
    
    recommendations = []
    
    # Document type priority for eviction defense
    type_priority = {
        'lease': 95,
        'notice': 90,
        'payment_record': 85,
        'communication': 80,
        'evidence': 75,
        'repair_request': 80,
        'inspection_report': 85,
        'code_violation': 90
    }
    
    for doc in context.documents:
        # Base score from document type
        base_score = type_priority.get(doc.doc_type, 50)
        
        # Check if perspective analysis exists
        perspective_scores = None
        try:
            from perspective_reasoning import analyze_perspectives
            
            doc_path = os.path.join("uploads", "vault", user_id, doc.filename)
            if os.path.exists(doc_path):
                result = analyze_perspectives(doc_path, doc.doc_type)
                perspective_scores = {
                    'tenant': result.tenant_view.score,
                    'landlord': result.landlord_view.score,
                    'legal': result.legal_view.score,
                    'judge': result.judge_view.score,
                    'tenant_advantage': result.comparative.tenant_advantage
                }
                
                # Boost score if tenant advantage is positive
                if result.comparative.tenant_advantage > 0:
                    base_score += min(result.comparative.tenant_advantage / 2, 15)  # Up to +15 points
        
        except Exception:
            pass
        
        # Generate recommendation reason
        reason = f"{doc.doc_type.replace('_', ' ').title()} document"
        if doc.legal_significance and doc.legal_significance != 'informational':
            reason += f" - {doc.legal_significance}"
            if doc.legal_significance == 'critical':
                base_score += 10
        
        recommendations.append(EvidenceRecommendation(
            document_id=doc.id,
            filename=doc.filename,
            doc_type=doc.doc_type,
            relevance_score=min(base_score, 100),
            legal_significance=doc.legal_significance or 'informational',
            reason=reason,
            perspective_scores=perspective_scores
        ))
    
    # Sort by relevance score (descending)
    recommendations.sort(key=lambda r: r.relevance_score, reverse=True)
    
    return recommendations[:limit]


def generate_context_enhanced_packet(user_id: str, case_type: str = 'eviction_defense') -> Dict[str, Any]:
    """
    Generate a court packet with Context System intelligence.
    
    Combines:
    - Auto-filled complaint data
    - Ranked evidence
    - Timeline visualization
    - Perspective analysis summary
    - Case strength assessment
    
    Args:
        user_id: User ID
        case_type: Type of case
        
    Returns:
        Dict with packet data ready for PDF generation
    """
    form_data = auto_fill_complaint(user_id, case_type)
    evidence = suggest_evidence(user_id, case_type)
    
    return {
        'complaint_data': {
            'tenant': {
                'name': form_data.tenant_name,
                'phone': form_data.tenant_phone,
                'email': form_data.tenant_email,
                'address': form_data.tenant_address
            },
            'landlord': {
                'name': form_data.landlord_name,
                'company': form_data.landlord_company,
                'phone': form_data.landlord_phone,
                'address': form_data.landlord_address
            },
            'property': {
                'address': form_data.rental_address,
                'city': form_data.city,
                'state': form_data.state,
                'zip': form_data.zip_code
            },
            'financial': {
                'monthly_rent': form_data.monthly_rent,
                'security_deposit': form_data.security_deposit,
                'amount_owed': form_data.amount_owed
            },
            'dates': {
                'lease_start': form_data.lease_start_date,
                'lease_end': form_data.lease_end_date,
                'issue_start': form_data.issue_start_date,
                'notice_date': form_data.notice_date
            },
            'issue_description': form_data.issue_description
        },
        'evidence_list': [
            {
                'filename': ev.filename,
                'type': ev.doc_type,
                'relevance': ev.relevance_score,
                'significance': ev.legal_significance,
                'reason': ev.reason,
                'perspective_scores': ev.perspective_scores
            }
            for ev in evidence
        ],
        'timeline': form_data.timeline_events,
        'case_assessment': {
            'overall_strength': form_data.case_strength,
            'win_probability': form_data.win_probability,
            'data_confidence': form_data.data_confidence,
            'total_documents': len(form_data.key_documents),
            'total_events': len(form_data.timeline_events)
        },
        'generated_at': datetime.now().isoformat(),
        'source': form_data.extraction_source
    }


# Quick test function
if __name__ == "__main__":
    print("Testing Context Integration...")
    
    # Test with user 1
    form = auto_fill_complaint('1')
    print(f"\n✓ Auto-filled {form.data_confidence:.1f}% of form fields")
    print(f"  Tenant: {form.tenant_name or '(not found)'}")
    print(f"  Landlord: {form.landlord_name or '(not found)'}")
    print(f"  Rent: ${form.monthly_rent or 0}")
    print(f"  Events: {len(form.timeline_events)}")
    
    evidence = suggest_evidence('1')
    print(f"\n✓ Found {len(evidence)} evidence documents")
    for i, ev in enumerate(evidence[:3], 1):
        print(f"  {i}. {ev.filename} ({ev.relevance_score:.0f}% relevant)")
    
    packet = generate_context_enhanced_packet('1')
    print(f"\n✓ Generated court packet")
    print(f"  Case strength: {packet['case_assessment']['overall_strength']:.1f}%")
    print(f"  Evidence items: {len(packet['evidence_list'])}")
    print(f"  Timeline events: {len(packet['timeline'])}")