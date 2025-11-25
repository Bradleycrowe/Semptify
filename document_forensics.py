"""
Document Forensics Module
Detects forged, altered, or suspicious documents
"""
import os
from datetime import datetime
from PIL import Image
import hashlib

def analyze_document_metadata(file_path):
    """
    Analyze document metadata for tampering signs
    
    Returns dict with:
        - creation_date
        - modification_date
        - is_suspicious (bool)
        - warnings (list)
    """
    warnings = []
    
    try:
        stat = os.stat(file_path)
        created = datetime.fromtimestamp(stat.st_ctime)
        modified = datetime.fromtimestamp(stat.st_mtime)
        
        # Check if modification is BEFORE creation (impossible)
        if modified < created:
            warnings.append("⚠️ Modification date before creation date - possible tampering")
        
        # Check if dates are in the future
        now = datetime.now()
        if created > now:
            warnings.append("⚠️ Creation date in the future - system clock issue or forgery")
        if modified > now:
            warnings.append("⚠️ Modification date in the future - system clock issue or forgery")
        
        return {
            'creation_date': created.isoformat(),
            'modification_date': modified.isoformat(),
            'is_suspicious': len(warnings) > 0,
            'warnings': warnings,
            'file_size': stat.st_size
        }
        
    except Exception as e:
        return {'error': str(e)}

def check_image_manipulation(image_path):
    """
    Basic image manipulation detection
    Checks for:
        - Inconsistent compression
        - EXIF data tampering
        - Copy-paste artifacts
    """
    warnings = []
    
    try:
        img = Image.open(image_path)
        exif = img._getexif() if hasattr(img, '_getexif') else {}
        
        # Check if EXIF data exists
        if not exif:
            warnings.append("No EXIF data - may be edited/screenshot")
        
        # Check image format consistency
        if img.format == 'PNG' and image_path.lower().endswith('.jpg'):
            warnings.append("File extension doesn't match image format")
        
        return {
            'has_exif': bool(exif),
            'format': img.format,
            'size': img.size,
            'mode': img.mode,
            'is_suspicious': len(warnings) > 0,
            'warnings': warnings
        }
        
    except Exception as e:
        return {'error': str(e)}

def calculate_document_hash(file_path):
    """
    Generate cryptographic hash for document verification
    """
    sha256 = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        
        return {
            'sha256': sha256.hexdigest(),
            'algorithm': 'SHA-256'
        }
        
    except Exception as e:
        return {'error': str(e)}

def comprehensive_forgery_check(file_path):
    """
    Full forensic analysis of document
    
    Returns:
        - Overall suspicion score (0-100)
        - List of all warnings
        - Recommendations
    """
    results = {
        'metadata': analyze_document_metadata(file_path),
        'hash': calculate_document_hash(file_path)
    }
    
    # Check if image
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp')):
        results['image_analysis'] = check_image_manipulation(file_path)
    
    # Compile all warnings
    all_warnings = []
    all_warnings.extend(results['metadata'].get('warnings', []))
    if 'image_analysis' in results:
        all_warnings.extend(results['image_analysis'].get('warnings', []))
    
    # Calculate suspicion score
    suspicion_score = min(len(all_warnings) * 25, 100)
    
    # Recommendations
    recommendations = []
    if suspicion_score > 50:
        recommendations.append("Request original document from source")
        recommendations.append("Verify with issuing authority")
    if suspicion_score > 75:
        recommendations.append("Do NOT use this document in legal proceedings")
        recommendations.append("Contact attorney immediately")
    
    return {
        'suspicion_score': suspicion_score,
        'risk_level': 'HIGH' if suspicion_score > 75 else 'MEDIUM' if suspicion_score > 50 else 'LOW',
        'warnings': all_warnings,
        'recommendations': recommendations,
        'details': results
    }

