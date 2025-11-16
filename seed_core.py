"""Self-Growing Seed Core
The seed lives in user's bucket, generates its own engines based on needs.
"""
from __future__ import annotations
import json
import secrets
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

@dataclass
class SeedCapability:
    """A capability the seed has learned."""
    name: str
    engine_file: str
    description: str
    learned_from: str  # What user interaction triggered this
    created_at: str
    usage_count: int = 0
    success_rate: float = 1.0

@dataclass
class SeedCore:
    """The seed's brain - tracks capabilities, patterns, evolution."""
    seed_id: str
    created_at: str
    user_context: Dict[str, Any]
    capabilities: List[SeedCapability]
    interaction_count: int = 0
    learning_patterns: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.learning_patterns is None:
            self.learning_patterns = {
                'common_needs': [],
                'jurisdiction': None,
                'case_type': None,
                'confidence_scores': {}
            }
    
    @classmethod
    def plant_new_seed(cls, user_context: Dict[str, Any] = None) -> 'SeedCore':
        """Plant a new seed with minimal bootstrap."""
        return cls(
            seed_id=f"seed_{secrets.token_hex(8)}",
            created_at=datetime.utcnow().isoformat(),
            user_context=user_context or {},
            capabilities=[],
            interaction_count=0
        )
    
    def has_capability(self, capability_name: str) -> bool:
        """Check if seed has grown this capability."""
        return any(c.name == capability_name for c in self.capabilities)
    
    def add_capability(self, capability: SeedCapability):
        """Seed grows a new capability."""
        if not self.has_capability(capability.name):
            self.capabilities.append(capability)
    
    def record_interaction(self, need: str):
        """Learn from user interaction."""
        self.interaction_count += 1
        if need not in self.learning_patterns['common_needs']:
            self.learning_patterns['common_needs'].append(need)
    
    def update_capability_stats(self, capability_name: str, success: bool):
        """Update success rate for a capability."""
        for cap in self.capabilities:
            if cap.name == capability_name:
                cap.usage_count += 1
                # Running average
                cap.success_rate = (
                    (cap.success_rate * (cap.usage_count - 1) + (1.0 if success else 0.0))
                    / cap.usage_count
                )
    
    def to_json(self) -> str:
        """Serialize to JSON for bucket storage."""
        data = {
            'seed_id': self.seed_id,
            'created_at': self.created_at,
            'user_context': self.user_context,
            'capabilities': [asdict(c) for c in self.capabilities],
            'interaction_count': self.interaction_count,
            'learning_patterns': self.learning_patterns
        }
        return json.dumps(data, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SeedCore':
        """Load seed from bucket."""
        data = json.loads(json_str)
        capabilities = [SeedCapability(**c) for c in data['capabilities']]
        return cls(
            seed_id=data['seed_id'],
            created_at=data['created_at'],
            user_context=data['user_context'],
            capabilities=capabilities,
            interaction_count=data['interaction_count'],
            learning_patterns=data['learning_patterns']
        )

class SeedGrowthEngine:
    """Generates new engine code when seed needs it."""
    
    def __init__(self, seed: SeedCore):
        self.seed = seed
    
    def analyze_need(self, user_input: str) -> Optional[str]:
        """Determine what capability is needed from user input."""
        user_lower = user_input.lower()
        
        if any(kw in user_lower for kw in ['eviction', 'evicted', 'notice to vacate']):
            return 'eviction_defense'
        elif any(kw in user_lower for kw in ['rent', 'overcharge', 'increase']):
            return 'rent_calculator'
        elif any(kw in user_lower for kw in ['motion', 'file', 'court']):
            return 'motion_writer'
        elif any(kw in user_lower for kw in ['evidence', 'document', 'proof']):
            return 'evidence_organizer'
        elif any(kw in user_lower for kw in ['repair', 'maintenance', 'habitability']):
            return 'habitability_checker'
        
        return None
    
    def generate_engine_code(self, capability_name: str) -> str:
        """Generate Python engine code for this capability."""
        templates = {
            'eviction_defense': self._gen_eviction_engine,
            'rent_calculator': self._gen_rent_engine,
            'motion_writer': self._gen_motion_engine,
            'evidence_organizer': self._gen_evidence_engine,
            'habitability_checker': self._gen_habitability_engine
        }
        
        generator = templates.get(capability_name)
        if generator:
            return generator()
        return self._gen_generic_engine(capability_name)
    
    def _gen_eviction_engine(self) -> str:
        return '''"""Eviction Defense Engine - Generated by Seed"""
from typing import Dict, List

def analyze_eviction_notice(notice_text: str, jurisdiction: str) -> Dict:
    """Analyze eviction notice for defenses."""
    defenses = []
    
    # Check notice period
    if 'three day' in notice_text.lower() or '3 day' in notice_text.lower():
        defenses.append({
            'type': 'procedural',
            'defense': 'Insufficient notice period',
            'strength': 'high' if jurisdiction == 'CA' else 'medium'
        })
    
    # Check rent control
    if jurisdiction in ['SF', 'Oakland', 'LA']:
        defenses.append({
            'type': 'substantive',
            'defense': 'Rent control violation',
            'strength': 'high'
        })
    
    return {
        'defenses': defenses,
        'next_steps': [
            'File answer within 5 days',
            'Request discovery',
            'Gather rent payment evidence'
        ],
        'urgency': 'high'
    }

def generate_answer(case_info: Dict) -> str:
    """Generate answer to eviction complaint."""
    return f"""ANSWER TO UNLAWFUL DETAINER COMPLAINT

Case No: {case_info.get('case_number', '[CASE NUMBER]')}

COMES NOW the Defendant and states:

1. Defendant denies each allegation in Plaintiff's Complaint.
2. Defendant asserts the following affirmative defenses:
   - Failure to provide proper notice
   - Rent control violation
   - Retaliation for habitability complaints

WHEREFORE, Defendant requests judgment dismissing this action.

Dated: [DATE]
"""
'''
    
    def _gen_rent_engine(self) -> str:
        return '''"""Rent Calculator Engine - Generated by Seed"""
from typing import Dict

def calculate_rent_increase_legality(
    old_rent: float,
    new_rent: float,
    jurisdiction: str,
    year: int
) -> Dict:
    """Check if rent increase is legal."""
    increase_pct = ((new_rent - old_rent) / old_rent) * 100
    
    # Jurisdiction limits
    limits = {
        'CA': 10.0,  # AB 1482
        'SF': 7.0,
        'Oakland': 'CPI + 5%'
    }
    
    limit = limits.get(jurisdiction, float('inf'))
    is_legal = increase_pct <= limit if isinstance(limit, float) else True
    
    return {
        'old_rent': old_rent,
        'new_rent': new_rent,
        'increase_amount': new_rent - old_rent,
        'increase_percent': round(increase_pct, 2),
        'legal_limit': limit,
        'is_legal': is_legal,
        'recommendation': 'Dispute increase' if not is_legal else 'Increase is within limits'
    }
'''
    
    def _gen_motion_engine(self) -> str:
        return '''"""Motion Writer Engine - Generated by Seed"""

def generate_motion(motion_type: str, case_info: dict) -> str:
    """Generate court motion."""
    templates = {
        'continuance': _motion_continuance,
        'discovery': _motion_discovery,
        'summary_judgment': _motion_summary_judgment
    }
    
    generator = templates.get(motion_type, _motion_generic)
    return generator(case_info)

def _motion_continuance(info: dict) -> str:
    return f"""NOTICE OF MOTION FOR CONTINUANCE

Case No: {info['case_number']}

TO ALL PARTIES:
PLEASE TAKE NOTICE that on {info['hearing_date']}, Defendant will move for a continuance of trial.

This motion is made on grounds that additional time is needed to:
1. Complete discovery
2. Retain expert witnesses
3. Prepare defense

DATED: [DATE]
"""

def _motion_discovery(info: dict) -> str:
    return "MOTION TO COMPEL DISCOVERY..."

def _motion_summary_judgment(info: dict) -> str:
    return "MOTION FOR SUMMARY JUDGMENT..."

def _motion_generic(info: dict) -> str:
    return "MOTION [TYPE]..."
'''
    
    def _gen_evidence_engine(self) -> str:
        return '''"""Evidence Organizer Engine - Generated by Seed"""

def organize_evidence(documents: list) -> dict:
    """Organize evidence by type and relevance."""
    organized = {
        'rent_payments': [],
        'communications': [],
        'photos': [],
        'witnesses': [],
        'other': []
    }
    
    for doc in documents:
        doc_type = doc.get('type', 'other')
        if doc_type in organized:
            organized[doc_type].append(doc)
        else:
            organized['other'].append(doc)
    
    return organized
'''
    
    def _gen_holdover_engine(self) -> str:
        """Generate engine for holdover tenant situations."""
        return '''"""
Holdover Tenant Rights Engine
Analyzes end-of-lease holdover situations and tenant rights.
"""

def analyze_holdover_rights(lease_end_date: str = None, notice_received: bool = False, 
                            notice_type: str = None, state: str = "MN") -> dict:
    """
    Analyze holdover tenant situation and rights.
    
    Args:
        lease_end_date: When lease expired (YYYY-MM-DD)
        notice_received: Whether landlord gave notice
        notice_type: Type of notice (e.g., "non-renewal", "eviction")
        state: State code (default MN)
    
    Returns:
        Analysis with tenant rights and options
    """
    from datetime import datetime, timedelta
    
    analysis = {
        "status": "holdover_tenant",
        "rights": [],
        "options": [],
        "risks": [],
        "urgency": "medium"
    }
    
    # Parse lease end date
    if lease_end_date:
        try:
            end_date = datetime.strptime(lease_end_date, "%Y-%m-%d")
            days_since = (datetime.now() - end_date).days
            analysis["days_since_lease_end"] = days_since
            
            if days_since < 30:
                analysis["urgency"] = "low"
            elif days_since < 90:
                analysis["urgency"] = "medium"
            else:
                analysis["urgency"] = "high"
        except:
            pass
    
    # MN-specific holdover rights
    if state == "MN":
        analysis["rights"].extend([
            "Month-to-month tenancy may have been created automatically",
            "Landlord must give proper notice to terminate (typically 30 days for month-to-month)",
            "Cannot be locked out without court order",
            "Must receive formal eviction notice for non-payment or violation",
            "Right to remain until proper legal process completed"
        ])
        
        if not notice_received:
            analysis["options"].extend([
                "Negotiate new lease or month-to-month agreement",
                "Request written terms for holdover period",
                "Seek rent assistance if needed",
                "Look for alternative housing while protected by holdover rights"
            ])
            analysis["risks"].append("Landlord may file eviction if you refuse to leave after proper notice")
        else:
            if notice_type and 'eviction' in notice_type.lower():
                analysis["urgency"] = "high"
                analysis["options"].extend([
                    "Respond to eviction notice immediately",
                    "Seek legal aid - you have defenses",
                    "File answer with court if summons received",
                    "Document all communications with landlord"
                ])
                analysis["risks"].append("Eviction judgment can make future housing difficult")
            else:
                analysis["options"].extend([
                    "Comply with notice terms if reasonable",
                    "Negotiate move-out date if you need more time",
                    "Request notice in writing if only verbal",
                    "Understand you have time to find new housing"
                ])
    
    # Next steps
    analysis["next_steps"] = [
        "Document your lease end date and any notices received",
        "Do NOT ignore court papers if served",
        "Contact legal aid if landlord threatens illegal eviction",
        "Keep paying rent to maintain tenancy rights",
        "Get any agreements in writing"
    ]
    
    return analysis

if __name__ == "__main__":
    # Test the engine
    result = analyze_holdover_rights(
        lease_end_date="2025-10-31",
        notice_received=False,
        state="MN"
    )
    print(f"Status: {result['status']}")
    print(f"\\nRights ({len(result['rights'])}):")
    for right in result['rights']:
        print(f"  • {right}")
    print(f"\\nOptions:")
    for opt in result['options']:
        print(f"  • {opt}")
    print(f"\\nUrgency: {result['urgency']}")
'''

    def _gen_habitability_engine(self) -> str:
        return '''"""Habitability Checker Engine - Generated by Seed"""

def check_habitability_violations(issues: list, jurisdiction: str) -> dict:
    """Check for habitability violations."""
    violations = []
    
    serious_issues = ['no heat', 'no water', 'mold', 'pest infestation']
    
    for issue in issues:
        if any(s in issue.lower() for s in serious_issues):
            violations.append({
                'issue': issue,
                'severity': 'high',
                'remedy': 'Repair and abate rent or withhold rent'
            })
    
    return {
        'violations': violations,
        'total_count': len(violations),
        'can_withhold_rent': len(violations) > 0
    }
'''
    
    def _gen_generic_engine(self, name: str) -> str:
        return f'''"""Generic Engine: {name} - Generated by Seed"""

def process_{name}(data: dict) -> dict:
    """Process {name} request."""
    return {{
        'status': 'processed',
        'message': '{name} engine needs customization',
        'data': data
    }}
'''

# Singleton accessor
_seed_core: Optional[SeedCore] = None

def get_seed() -> SeedCore:
    global _seed_core
    if _seed_core is None:
        _seed_core = SeedCore.plant_new_seed()
    return _seed_core




