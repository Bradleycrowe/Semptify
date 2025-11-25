"""
Handwriting Recognition Module
Uses EasyOCR for handwriting detection in uploaded documents
"""
import os

try:
    import easyocr
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False

def extract_handwriting(image_path, languages=['en']):
    """
    Extract handwritten text from image
    
    Args:
        image_path: Path to image file
        languages: List of language codes (default: English)
        
    Returns:
        dict with 'text', 'confidence', 'boxes' keys
    """
    if not HAS_EASYOCR:
        return {'error': 'EasyOCR not installed. Run: pip install easyocr'}
    
    try:
        reader = easyocr.Reader(languages, gpu=False)
        results = reader.readtext(image_path)
        
        # Parse results
        text_lines = []
        boxes = []
        confidences = []
        
        for (bbox, text, conf) in results:
            text_lines.append(text)
            boxes.append(bbox)
            confidences.append(conf)
        
        return {
            'text': '\n'.join(text_lines),
            'full_text': ' '.join(text_lines),
            'lines': text_lines,
            'boxes': boxes,
            'confidences': confidences,
            'avg_confidence': sum(confidences) / len(confidences) if confidences else 0
        }
        
    except Exception as e:
        return {'error': str(e)}

def is_likely_handwritten(image_path):
    """
    Quick check if image contains handwriting
    Returns confidence score 0-1
    """
    # Placeholder - would use ML model
    # For now, just try to extract and check confidence
    result = extract_handwriting(image_path)
    if 'error' in result:
        return 0.0
    return result.get('avg_confidence', 0.0)

