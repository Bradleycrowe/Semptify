"""
DOCUMENT INTELLIGENCE ENGINE
=============================

Reads documents holistically (like a lawyer) and extracts ALL details:
- Legal validity (signatures, dates, witnesses)
- Contact information (parties, attorneys, managers)
- Contract details (terms, amounts, dates, policies)
- Jurisdiction (state, county, governing law)
- Signatures & validation (who, when, valid?)

The "little things" that are HUGE in contracts.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

# PDF and image reading (install if needed: pip install pypdf2 pillow pytesseract)
try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class ValidityStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    INCOMPLETE = "incomplete"
    SUSPICIOUS = "suspicious"
    UNKNOWN = "unknown"

@dataclass
class ContactInfo:
    """Extracted contact information"""
    role: str  # landlord, tenant, manager, attorney, witness
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None

@dataclass
class SignatureInfo:
    """Signature validation details"""
    signer_name: Optional[str] = None
    signature_date: Optional[str] = None
    is_present: bool = False
    is_witnessed: bool = False
    witness_name: Optional[str] = None
    is_notarized: bool = False
    notary_stamp: bool = False
    is_electronic: bool = False
    matches_name: Optional[bool] = None  # Does signature match stated name?

@dataclass
class ContractTerms:
    """Contract/lease terms"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    rent_amount: Optional[float] = None
    rent_due_day: Optional[int] = None
    security_deposit: Optional[float] = None
    late_fee: Optional[float] = None
    utilities_included: List[str] = field(default_factory=list)
    pets_allowed: Optional[bool] = None
    pet_deposit: Optional[float] = None
    maintenance_terms: List[str] = field(default_factory=list)
    termination_notice_days: Optional[int] = None

@dataclass
class JurisdictionInfo:
    """Legal jurisdiction details"""
    state: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    governing_law: Optional[str] = None
    court_jurisdiction: Optional[str] = None
    dispute_resolution: Optional[str] = None  # arbitration, mediation, court
    arbitration_clause: bool = False

@dataclass
class LegalValidation:
    """Overall legal validity assessment"""
    status: ValidityStatus = ValidityStatus.UNKNOWN
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    required_signatures: int = 0
    present_signatures: int = 0
    all_parties_signed: bool = False
    dates_valid: bool = True
    has_legal_language: bool = False

@dataclass
class DocumentIntelligence:
    """Complete document intelligence extracted"""
    # Document metadata
    filepath: str
    doc_type: str
    processed_at: str
    
    # Extracted content
    full_text: str = ""
    
    # Legal validity
    legal_validation: LegalValidation = field(default_factory=LegalValidation)
    
    # Contacts
    contacts: List[ContactInfo] = field(default_factory=list)
    
    # Signatures
    signatures: List[SignatureInfo] = field(default_factory=list)
    
    # Contract terms (if applicable)
    contract_terms: Optional[ContractTerms] = None
    
    # Jurisdiction
    jurisdiction: JurisdictionInfo = field(default_factory=JurisdictionInfo)
    
    # Key dates extracted
    important_dates: List[Dict[str, str]] = field(default_factory=list)
    
    # Key amounts extracted
    important_amounts: List[Dict[str, float]] = field(default_factory=list)
    
    # Confidence scores
    confidence: float = 0.0  # 0-1 confidence in extraction quality

# ============================================================================
# DOCUMENT INTELLIGENCE ENGINE
# ============================================================================

class DocumentIntelligenceEngine:
    """
    Smart document processor that reads holistically and extracts ALL details.
    
    Like a lawyer reading a contract - understands context, extracts details,
    validates requirements, flags issues.
    """
    
    def __init__(self):
        self.us_states = [
            "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
            "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
            "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
            "maine", "maryland", "massachusetts", "michigan", "minnesota",
            "mississippi", "missouri", "montana", "nebraska", "nevada",
            "new hampshire", "new jersey", "new mexico", "new york",
            "north carolina", "north dakota", "ohio", "oklahoma", "oregon",
            "pennsylvania", "rhode island", "south carolina", "south dakota",
            "tennessee", "texas", "utah", "vermont", "virginia", "washington",
            "west virginia", "wisconsin", "wyoming"
        ]
    
    # ========================================================================
    # MAIN PROCESSING
    # ========================================================================
    
    def process_document(self, filepath: str, doc_type: str = "unknown") -> DocumentIntelligence:
        """
        Process document holistically - extract ALL intelligence.
        
        This is the main entry point. Reads entire document, understands context,
        extracts all details, validates requirements.
        """
        filepath = Path(filepath)
        
        # Initialize result
        intel = DocumentIntelligence(
            filepath=str(filepath),
            doc_type=doc_type,
            processed_at=datetime.now().isoformat()
        )
        
        # Step 1: Read document content
        intel.full_text = self._read_document(filepath)
        
        if not intel.full_text:
            intel.confidence = 0.0
            return intel
        
        # Step 2: Extract contacts (parties involved)
        intel.contacts = self._extract_contacts(intel.full_text)
        
        # Step 3: Extract signatures and validate
        intel.signatures = self._extract_signatures(intel.full_text)
        
        # Step 4: Extract contract terms (if lease/contract)
        if doc_type in ["lease", "contract", "agreement"]:
            intel.contract_terms = self._extract_contract_terms(intel.full_text)
        
        # Step 5: Extract jurisdiction
        intel.jurisdiction = self._extract_jurisdiction(intel.full_text)
        
        # Step 6: Extract important dates
        intel.important_dates = self._extract_dates(intel.full_text)
        
        # Step 7: Extract important amounts
        intel.important_amounts = self._extract_amounts(intel.full_text)
        
        # Step 8: Validate legal requirements
        intel.legal_validation = self._validate_legal_requirements(intel, doc_type)
        
        # Step 9: Calculate confidence
        intel.confidence = self._calculate_confidence(intel)
        
        return intel
    
    # ========================================================================
    # DOCUMENT READING
    # ========================================================================
    
    def _read_document(self, filepath: Path) -> str:
        """Read document content (PDF, image, or text)"""
        suffix = filepath.suffix.lower()
        
        # Text files
        if suffix in ['.txt', '.md']:
            return filepath.read_text(encoding='utf-8', errors='ignore')
        
        # PDF files
        if suffix == '.pdf' and HAS_PDF:
            return self._read_pdf(filepath)
        
        # Image files (OCR)
        if suffix in ['.jpg', '.jpeg', '.png', '.tiff'] and HAS_OCR:
            return self._read_image_ocr(filepath)
        
        # Unknown/unsupported
        return ""
    
    def _read_pdf(self, filepath: Path) -> str:
        """Extract text from PDF"""
        try:
            text = ""
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"PDF read error: {e}")
            return ""
    
    def _read_image_ocr(self, filepath: Path) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"OCR error: {e}")
            return ""
    
    # ========================================================================
    # CONTACT EXTRACTION
    # ========================================================================
    
    def _extract_contacts(self, text: str) -> List[ContactInfo]:
        """Extract all contact information from document"""
        contacts = []
        
        # Landlord/Owner
        landlord = self._extract_contact_by_role(text, "landlord", 
            ["landlord", "lessor", "owner", "property owner"])
        if landlord:
            contacts.append(landlord)
        
        # Tenant
        tenant = self._extract_contact_by_role(text, "tenant",
            ["tenant", "lessee", "renter"])
        if tenant:
            contacts.append(tenant)
        
        # Property Manager
        manager = self._extract_contact_by_role(text, "manager",
            ["property manager", "manager", "management company"])
        if manager:
            contacts.append(manager)
        
        # Attorney
        attorney = self._extract_contact_by_role(text, "attorney",
            ["attorney", "lawyer", "legal counsel", "law firm"])
        if attorney:
            contacts.append(attorney)
        
        return contacts
    
    def _extract_contact_by_role(self, text: str, role: str, keywords: List[str]) -> Optional[ContactInfo]:
        """Extract contact info for specific role"""
        contact = ContactInfo(role=role)
        
        # Find section mentioning this role
        for keyword in keywords:
            pattern = f"{keyword}[:\\s]+([^\n]+)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                section = match.group(1)
                
                # Extract name (capitalized words)
                name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', section)
                if name_match:
                    contact.name = name_match.group(1)
                
                # Extract phone
                phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', section)
                if phone_match:
                    contact.phone = phone_match.group(1)
                
                # Extract email
                email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', section)
                if email_match:
                    contact.email = email_match.group(1)
                
                # Extract address (street address pattern)
                addr_match = re.search(r'(\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd))', section, re.IGNORECASE)
                if addr_match:
                    contact.address = addr_match.group(1)
                
                if contact.name or contact.phone or contact.email:
                    return contact
        
        return None
    
    # ========================================================================
    # SIGNATURE EXTRACTION
    # ========================================================================
    
    def _extract_signatures(self, text: str) -> List[SignatureInfo]:
        """Extract and validate signatures"""
        signatures = []
        
        # Find signature sections
        sig_patterns = [
            r'signature[:\s]+([^\n]+)',
            r'signed[:\s]+([^\n]+)',
            r'(?:landlord|tenant|party)\s+signature[:\s]+([^\n]+)',
            r'executed\s+by[:\s]+([^\n]+)'
        ]
        
        for pattern in sig_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                sig_section = match.group(1)
                
                sig_info = SignatureInfo(is_present=True)
                
                # Extract signer name
                name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', sig_section)
                if name_match:
                    sig_info.signer_name = name_match.group(1)
                
                # Extract date
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', sig_section)
                if date_match:
                    sig_info.signature_date = date_match.group(1)
                
                # Check for witness
                if re.search(r'witness', sig_section, re.IGNORECASE):
                    sig_info.is_witnessed = True
                
                # Check for notary
                if re.search(r'notary|notarized', text, re.IGNORECASE):
                    sig_info.is_notarized = True
                
                if sig_info.signer_name or sig_info.signature_date:
                    signatures.append(sig_info)
        
        return signatures
    
    # ========================================================================
    # CONTRACT TERMS EXTRACTION
    # ========================================================================
    
    def _extract_contract_terms(self, text: str) -> ContractTerms:
        """Extract lease/contract terms"""
        terms = ContractTerms()
        
        # Rent amount
        rent_patterns = [
            r'rent[:\s]+\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'monthly\s+rent[:\s]+\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)\s+per\s+month'
        ]
        for pattern in rent_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                terms.rent_amount = float(match.group(1).replace(',', ''))
                break
        
        # Security deposit
        deposit_patterns = [
            r'security\s+deposit[:\s]+\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'deposit[:\s]+\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        for pattern in deposit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                terms.security_deposit = float(match.group(1).replace(',', ''))
                break
        
        # Lease dates
        date_patterns = [
            r'lease\s+term[:\s]+(\d{1,2}/\d{1,2}/\d{2,4})\s+to\s+(\d{1,2}/\d{1,2}/\d{2,4})',
            r'from\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+to\s+(\d{1,2}/\d{1,2}/\d{2,4})'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                terms.start_date = match.group(1)
                terms.end_date = match.group(2)
                break
        
        # Pets
        if re.search(r'pets?\s+allowed', text, re.IGNORECASE):
            terms.pets_allowed = True
        elif re.search(r'no\s+pets?', text, re.IGNORECASE):
            terms.pets_allowed = False
        
        # Utilities
        utilities = ['water', 'electric', 'gas', 'trash', 'sewer', 'internet']
        for utility in utilities:
            if re.search(f'{utility}.*included', text, re.IGNORECASE):
                terms.utilities_included.append(utility)
        
        return terms
    
    # ========================================================================
    # JURISDICTION EXTRACTION
    # ========================================================================
    
    def _extract_jurisdiction(self, text: str) -> JurisdictionInfo:
        """Extract jurisdiction and governing law"""
        jurisdiction = JurisdictionInfo()
        
        # State
        for state in self.us_states:
            if re.search(f'\\b{state}\\b', text, re.IGNORECASE):
                jurisdiction.state = state.title()
                break
        
        # Governing law clause
        gov_law_match = re.search(r'governed?\s+by\s+(?:the\s+)?laws?\s+of\s+([^,\.\n]+)', text, re.IGNORECASE)
        if gov_law_match:
            jurisdiction.governing_law = gov_law_match.group(1).strip()
        
        # Court jurisdiction
        court_match = re.search(r'jurisdiction\s+of\s+([^,\.\n]+court[^,\.\n]*)', text, re.IGNORECASE)
        if court_match:
            jurisdiction.court_jurisdiction = court_match.group(1).strip()
        
        # Arbitration
        if re.search(r'arbitration', text, re.IGNORECASE):
            jurisdiction.arbitration_clause = True
            jurisdiction.dispute_resolution = "arbitration"
        elif re.search(r'mediation', text, re.IGNORECASE):
            jurisdiction.dispute_resolution = "mediation"
        
        return jurisdiction
    
    # ========================================================================
    # DATE & AMOUNT EXTRACTION
    # ========================================================================
    
    def _extract_dates(self, text: str) -> List[Dict[str, str]]:
        """Extract all important dates"""
        dates = []
        
        # Date patterns
        patterns = [
            (r'(\d{1,2}/\d{1,2}/\d{2,4})', 'mm/dd/yyyy'),
            (r'(\d{4}-\d{2}-\d{2})', 'yyyy-mm-dd'),
            (r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})', 'month day, year')
        ]
        
        for pattern, format_type in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                dates.append({
                    'date': match.group(1),
                    'format': format_type,
                    'context': text[max(0, match.start()-30):min(len(text), match.end()+30)]
                })
        
        return dates
    
    def _extract_amounts(self, text: str) -> List[Dict[str, float]]:
        """Extract all important dollar amounts"""
        amounts = []
        
        # Money patterns
        pattern = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'
        
        for match in re.finditer(pattern, text):
            amount = float(match.group(1).replace(',', ''))
            amounts.append({
                'amount': amount,
                'context': text[max(0, match.start()-30):min(len(text), match.end()+30)]
            })
        
        return amounts
    
    # ========================================================================
    # LEGAL VALIDATION
    # ========================================================================
    
    def _validate_legal_requirements(self, intel: DocumentIntelligence, doc_type: str) -> LegalValidation:
        """Validate document meets legal requirements"""
        validation = LegalValidation()
        
        # Check signatures
        validation.present_signatures = len(intel.signatures)
        
        if doc_type in ["lease", "contract", "agreement"]:
            validation.required_signatures = 2  # Landlord + Tenant minimum
            
            # Check if all parties signed
            has_landlord_sig = any(s.signer_name and "landlord" in intel.full_text.lower() for s in intel.signatures)
            has_tenant_sig = any(s.signer_name for s in intel.signatures)
            validation.all_parties_signed = has_landlord_sig and has_tenant_sig
            
            # Validate dates
            if intel.contract_terms and intel.contract_terms.start_date:
                # Check date format and validity
                validation.dates_valid = True  # TODO: Add actual date validation
            
            # Check for legal language
            legal_keywords = ["hereby", "whereas", "covenant", "agreement", "parties", "binding"]
            validation.has_legal_language = any(kw in intel.full_text.lower() for kw in legal_keywords)
            
            # Determine status
            if validation.all_parties_signed and validation.dates_valid and validation.has_legal_language:
                validation.status = ValidityStatus.VALID
            elif validation.present_signatures < validation.required_signatures:
                validation.status = ValidityStatus.INCOMPLETE
                validation.issues.append("Missing required signatures")
            else:
                validation.status = ValidityStatus.SUSPICIOUS
                validation.warnings.append("Document may have issues")
            
            # Specific issues
            if not validation.all_parties_signed:
                validation.issues.append("Not all parties have signed")
            
            if not intel.jurisdiction.state:
                validation.warnings.append("No jurisdiction/governing law found")
            
            if not intel.contract_terms or not intel.contract_terms.rent_amount:
                validation.warnings.append("Rent amount not clearly stated")
        
        return validation
    
    # ========================================================================
    # CONFIDENCE CALCULATION
    # ========================================================================
    
    def _calculate_confidence(self, intel: DocumentIntelligence) -> float:
        """Calculate confidence in extraction quality (0-1)"""
        score = 0.0
        max_score = 0.0
        
        # Text extracted (20 points)
        max_score += 20
        if len(intel.full_text) > 100:
            score += 20
        elif len(intel.full_text) > 0:
            score += 10
        
        # Contacts found (20 points)
        max_score += 20
        score += min(20, len(intel.contacts) * 10)
        
        # Signatures found (20 points)
        max_score += 20
        score += min(20, len(intel.signatures) * 10)
        
        # Contract terms (if applicable) (20 points)
        if intel.contract_terms:
            max_score += 20
            if intel.contract_terms.rent_amount:
                score += 10
            if intel.contract_terms.start_date:
                score += 10
        
        # Jurisdiction (10 points)
        max_score += 10
        if intel.jurisdiction.state:
            score += 10
        
        # Dates and amounts (10 points)
        max_score += 10
        if intel.important_dates:
            score += 5
        if intel.important_amounts:
            score += 5
        
        return score / max_score if max_score > 0 else 0.0

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def process_document(filepath: str, doc_type: str = "unknown") -> DocumentIntelligence:
    """Process a document and extract all intelligence"""
    engine = DocumentIntelligenceEngine()
    return engine.process_document(filepath, doc_type)

# ============================================================================
# MAIN - Testing
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  🧠 DOCUMENT INTELLIGENCE ENGINE")
    print("=" * 70)
    print()
    print("Smart document processor that reads holistically.")
    print("Extracts: contacts, signatures, terms, jurisdiction, validity")
    print()
    print("Ready to process documents!")
    print()
