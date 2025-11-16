from typing import Dict, Any, List, Optional

class AssumptionEngine:
    """Lightweight assumption engine to infer likely values from multiple weak/strong signals.
    Phase 1: jurisdiction inference only; extensible via pluggable detectors.
    """
    def __init__(self):
        self.detectors = {}
        try:
            from jurisdiction_detector import detect_jurisdiction
            self.detectors['jurisdiction'] = detect_jurisdiction
        except Exception:
            pass

    def register(self, key: str, func):
        self.detectors[key] = func

    def detect(self, key: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        func = self.detectors.get(key)
        if not func:
            return None
        try:
            return func(context)
        except Exception:
            return None
