"""
smart_autofill.py - Intelligent form auto-fill for Semptify
Learns from user input patterns and suggests contextual completions
Max 3 choices per field based on frequency and relevance
"""
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Dict, Optional

AUTOFILL_DATA_FILE = Path("data/autofill_patterns.json")
AUTOFILL_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

class SmartAutofill:
    def __init__(self):
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict:
        """Load historical input patterns"""
        if AUTOFILL_DATA_FILE.exists():
            try:
                return json.loads(AUTOFILL_DATA_FILE.read_text())
            except Exception:
                pass
        return {
            "fields": {},  # field_name -> list of values with counts
            "contexts": {},  # context -> field patterns
            "profiles": {}  # profile_id -> field preferences
        }
    
    def _save_patterns(self):
        """Persist patterns to disk"""
        try:
            AUTOFILL_DATA_FILE.write_text(json.dumps(self.patterns, indent=2))
        except Exception as e:
            print(f"[WARN] Failed to save autofill patterns: {e}")
    
    def record_input(self, field_name: str, value: str, profile_id: str = "default", context: str = "general"):
        """Record user input for learning"""
        if not value or not value.strip():
            return
        
        value = value.strip()
        
        # Update field history
        if field_name not in self.patterns["fields"]:
            self.patterns["fields"][field_name] = {}
        
        if value not in self.patterns["fields"][field_name]:
            self.patterns["fields"][field_name][value] = {"count": 0, "last_used": None}
        
        self.patterns["fields"][field_name][value]["count"] += 1
        self.patterns["fields"][field_name][value]["last_used"] = datetime.now().isoformat()
        
        # Update context patterns
        if context not in self.patterns["contexts"]:
            self.patterns["contexts"][context] = {}
        if field_name not in self.patterns["contexts"][context]:
            self.patterns["contexts"][context][field_name] = {}
        
        if value not in self.patterns["contexts"][context][field_name]:
            self.patterns["contexts"][context][field_name][value] = 0
        self.patterns["contexts"][context][field_name][value] += 1
        
        # Update profile preferences
        if profile_id not in self.patterns["profiles"]:
            self.patterns["profiles"][profile_id] = {}
        if field_name not in self.patterns["profiles"][profile_id]:
            self.patterns["profiles"][profile_id][field_name] = {}
        
        if value not in self.patterns["profiles"][profile_id][field_name]:
            self.patterns["profiles"][profile_id][field_name][value] = 0
        self.patterns["profiles"][profile_id][field_name][value] += 1
        
        self._save_patterns()
    
    def get_suggestions(self, field_name: str, partial_value: str = "", 
                       profile_id: str = "default", context: str = "general",
                       max_results: int = 3) -> List[Dict]:
        """Get top suggestions for a field (max 3 by default)"""
        suggestions = []
        
        # Gather candidates from different sources
        candidates = {}
        
        # 1. Profile-specific preferences (highest priority)
        if profile_id in self.patterns["profiles"]:
            if field_name in self.patterns["profiles"][profile_id]:
                for value, count in self.patterns["profiles"][profile_id][field_name].items():
                    if not partial_value or partial_value.lower() in value.lower():
                        candidates[value] = candidates.get(value, 0) + (count * 3)  # 3x weight
        
        # 2. Context-specific patterns (medium priority)
        if context in self.patterns["contexts"]:
            if field_name in self.patterns["contexts"][context]:
                for value, count in self.patterns["contexts"][context][field_name].items():
                    if not partial_value or partial_value.lower() in value.lower():
                        candidates[value] = candidates.get(value, 0) + (count * 2)  # 2x weight
        
        # 3. General field history (base priority)
        if field_name in self.patterns["fields"]:
            for value, data in self.patterns["fields"][field_name].items():
                if not partial_value or partial_value.lower() in value.lower():
                    candidates[value] = candidates.get(value, 0) + data["count"]
        
        # Sort by weighted score and return top N
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        
        for value, score in sorted_candidates[:max_results]:
            # Get metadata
            metadata = self.patterns["fields"].get(field_name, {}).get(value, {})
            suggestions.append({
                "value": value,
                "score": score,
                "count": metadata.get("count", 0),
                "last_used": metadata.get("last_used")
            })
        
        return suggestions
    
    def get_related_fields(self, source_field: str, source_value: str, 
                          target_field: str, profile_id: str = "default") -> Optional[str]:
        """Predict target field value based on source field (e.g., address -> city)"""
        # This can be enhanced with field relationships
        # For now, use profile patterns
        if profile_id in self.patterns["profiles"]:
            if target_field in self.patterns["profiles"][profile_id]:
                # Return most common value for target field in this profile
                counts = self.patterns["profiles"][profile_id][target_field]
                if counts:
                    return max(counts.items(), key=lambda x: x[1])[0]
        return None
    
    def clear_field_history(self, field_name: str):
        """Clear history for specific field"""
        if field_name in self.patterns["fields"]:
            del self.patterns["fields"][field_name]
        self._save_patterns()
    
    def export_patterns(self) -> Dict:
        """Export all patterns for backup"""
        return self.patterns.copy()
    
    def import_patterns(self, patterns: Dict):
        """Import patterns from backup"""
        self.patterns = patterns
        self._save_patterns()

# Global instance
_autofill = SmartAutofill()

def record(field_name: str, value: str, profile_id: str = "default", context: str = "general"):
    """Record user input"""
    _autofill.record_input(field_name, value, profile_id, context)

def suggest(field_name: str, partial: str = "", profile_id: str = "default", 
           context: str = "general", max_results: int = 3) -> List[Dict]:
    """Get suggestions (max 3)"""
    return _autofill.get_suggestions(field_name, partial, profile_id, context, max_results)

def predict(source_field: str, source_value: str, target_field: str, 
           profile_id: str = "default") -> Optional[str]:
    """Predict related field value"""
    return _autofill.get_related_fields(source_field, source_value, target_field, profile_id)
