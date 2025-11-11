"""
OCR Document Recognition Service for Semptify
Extracts text from images and PDFs using Tesseract OCR
Supports lease agreements, notices, receipts, and court documents
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess
import json

try:
    from PIL import Image
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ Warning: pytesseract or PIL not installed. OCR will not work.")

try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("⚠️ Warning: PyPDF2 not installed. PDF text extraction limited.")


class OCRService:
    """
    OCR service for extracting text from document images and PDFs.
    Supports automatic document type classification.
    """
    
    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize OCR service.
        
        Args:
            tesseract_cmd: Path to tesseract executable (auto-detected if None)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf']
        
        # Document type patterns
        self.doc_patterns = {
            'lease': [
                r'lease agreement',
                r'rental agreement',
                r'lessor.*lessee',
                r'term of lease',
                r'monthly rent'
            ],
            'eviction_notice': [
                r'eviction notice',
                r'notice to vacate',
                r'30.day notice',
                r'60.day notice',
                r'termination of tenancy',
                r'unlawful detainer'
            ],
            'rent_receipt': [
                r'rent receipt',
                r'payment received',
                r'receipt.*rent',
                r'paid in full'
            ],
            'court_document': [
                r'case.*number',
                r'plaintiff.*defendant',
                r'court.*county',
                r'hearing.*date',
                r'summons'
            ],
            'maintenance_request': [
                r'maintenance request',
                r'repair request',
                r'work order',
                r'service request'
            ],
            'inspection_report': [
                r'inspection report',
                r'property inspection',
                r'move.in inspection',
                r'move.out inspection'
            ]
        }
    
    def is_available(self) -> bool:
        """Check if OCR service is available"""
        return TESSERACT_AVAILABLE
    
    def extract_text_from_image(self, image_path: str, lang: str = 'eng') -> str:
        """
        Extract text from an image file using Tesseract OCR.
        
        Args:
            image_path: Path to image file
            lang: Language code (default: 'eng')
        
        Returns:
            Extracted text
        """
        if not TESSERACT_AVAILABLE:
            raise RuntimeError("Tesseract OCR not available. Install pytesseract and Pillow.")
        
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"OCR extraction failed: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.
        Tries native text extraction first, falls back to OCR if needed.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Extracted text
        """
        # Try native PDF text extraction first
        if PDF_SUPPORT:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    
                    if text.strip():
                        return text.strip()
            except Exception as e:
                print(f"PDF text extraction failed, trying OCR: {e}")
        
        # Fallback to OCR if native extraction failed
        if TESSERACT_AVAILABLE:
            # Convert PDF pages to images and OCR each page
            # Note: Requires pdf2image library for production use
            raise NotImplementedError("PDF to OCR conversion requires pdf2image library")
        
        raise RuntimeError("Cannot extract text from PDF: no extraction method available")
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from file (auto-detects format).
        
        Args:
            file_path: Path to document file
        
        Returns:
            Extracted text
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        else:
            return self.extract_text_from_image(file_path)
    
    def classify_document(self, text: str) -> Tuple[str, float]:
        """
        Classify document type based on extracted text.
        
        Args:
            text: Extracted text from document
        
        Returns:
            Tuple of (document_type, confidence_score)
        """
        text_lower = text.lower()
        
        scores = {}
        for doc_type, patterns in self.doc_patterns.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    matches += 1
            
            # Calculate confidence score (0.0 to 1.0)
            scores[doc_type] = matches / len(patterns)
        
        if not scores or max(scores.values()) == 0:
            return ('unknown', 0.0)
        
        best_type = max(scores, key=scores.get)
        return (best_type, scores[best_type])
    
    def extract_dates(self, text: str) -> List[str]:
        """
        Extract dates from text using various date patterns.
        
        Args:
            text: Text to extract dates from
        
        Returns:
            List of date strings found
        """
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY or M/D/YY
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b'  # DD Month YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))  # Remove duplicates
    
    def extract_amounts(self, text: str) -> List[float]:
        """
        Extract dollar amounts from text.
        
        Args:
            text: Text to extract amounts from
        
        Returns:
            List of dollar amounts found
        """
        # Pattern for dollar amounts like $1,234.56 or $1234.56
        pattern = r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        
        matches = re.findall(pattern, text)
        amounts = []
        
        for match in matches:
            # Remove commas and convert to float
            amount_str = match.replace(',', '')
            try:
                amounts.append(float(amount_str))
            except ValueError:
                continue
        
        return amounts
    
    def extract_key_info(self, text: str, doc_type: str) -> Dict:
        """
        Extract key information based on document type.
        
        Args:
            text: Extracted text
            doc_type: Document type
        
        Returns:
            Dict of extracted information
        """
        info = {
            'dates': self.extract_dates(text),
            'amounts': self.extract_amounts(text)
        }
        
        # Type-specific extraction
        if doc_type == 'lease':
            # Extract lease-specific info
            info['landlord'] = self._extract_party(text, 'lessor|landlord')
            info['tenant'] = self._extract_party(text, 'lessee|tenant')
            info['property_address'] = self._extract_address(text)
        
        elif doc_type in ['eviction_notice', 'court_document']:
            # Extract case numbers
            case_pattern = r'case\s*(?:no|number|#)?[:\s]*([A-Z0-9\-]+)'
            case_match = re.search(case_pattern, text, re.IGNORECASE)
            if case_match:
                info['case_number'] = case_match.group(1)
        
        elif doc_type == 'rent_receipt':
            # Extract payment info
            info['receipt_number'] = self._extract_receipt_number(text)
        
        return info
    
    def _extract_party(self, text: str, party_type: str) -> Optional[str]:
        """Extract party name (landlord/tenant) from text"""
        pattern = f'{party_type}[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_address(self, text: str) -> Optional[str]:
        """Extract address from text"""
        # Simple pattern for US addresses
        pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[,\s]+[A-Za-z\s]+,?\s+[A-Z]{2}\s+\d{5}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def _extract_receipt_number(self, text: str) -> Optional[str]:
        """Extract receipt number from text"""
        pattern = r'receipt\s*(?:no|number|#)?[:\s]*([A-Z0-9\-]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def process_document(self, file_path: str) -> Dict:
        """
        Full document processing pipeline: OCR → classify → extract info.
        
        Args:
            file_path: Path to document file
        
        Returns:
            Dict with extracted text, classification, and key info
        """
        # Extract text
        text = self.extract_text(file_path)
        
        # Classify document
        doc_type, confidence = self.classify_document(text)
        
        # Extract key information
        key_info = self.extract_key_info(text, doc_type)
        
        return {
            'file_path': file_path,
            'text': text,
            'document_type': doc_type,
            'confidence': confidence,
            'key_info': key_info,
            'processed_at': datetime.now().isoformat(),
            'text_length': len(text)
        }


# Global instance
_ocr_service = None

def get_ocr_service() -> OCRService:
    """Get or create OCR service instance"""
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service


if __name__ == '__main__':
    # Test OCR service
    service = get_ocr_service()
    
    if not service.is_available():
        print("❌ OCR service not available")
        print("\nTo enable OCR, install required packages:")
        print("  pip install pytesseract Pillow PyPDF2")
        print("\nAnd install Tesseract OCR:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Mac: brew install tesseract")
        print("  Linux: sudo apt-get install tesseract-ocr")
    else:
        print("✅ OCR service initialized and ready")
        print(f"Supported formats: {', '.join(service.supported_formats)}")
        print(f"Document types: {', '.join(service.doc_patterns.keys())}")
        
        # Test text classification
        test_text = """
        EVICTION NOTICE
        
        Case Number: CV-2025-12345
        
        This is to notify you that your tenancy is terminated effective
        30 days from the date of this notice. Rent due: $1,200.00
        
        Court hearing scheduled for December 15, 2025.
        """
        
        doc_type, confidence = service.classify_document(test_text)
        print(f"\n📄 Test classification:")
        print(f"  Document type: {doc_type}")
        print(f"  Confidence: {confidence:.1%}")
        
        key_info = service.extract_key_info(test_text, doc_type)
        print(f"\n🔍 Extracted information:")
        print(f"  Dates: {key_info['dates']}")
        print(f"  Amounts: ${key_info['amounts']}")
        if 'case_number' in key_info:
            print(f"  Case number: {key_info['case_number']}")
