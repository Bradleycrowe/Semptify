"""
Seed Bootstrap Engine
Self-generates actionable tenant assistance based on user-provided context.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import re

class SeedBootstrapEngine:
    """Core engine that transforms user inputs into actionable plans and artifacts."""

    def __init__(self):
        self.context: Dict[str, Any] = {}
        self.needs: List[Dict[str, Any]] = []
        self.action_plan: List[Dict[str, Any]] = []
        self.artifacts: Dict[str, Any] = {}

    # 1. Collect user context -------------------------------------------------
    def collect_user_context(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        processed = {
            'jurisdiction': raw.get('location', 'Unknown').strip(),
            'issue_type': raw.get('issue_type', '').strip().lower(),
            'documents_provided': raw.get('documents', []),
            'deadline_text': raw.get('deadline_text', ''),
            'rent_amount': raw.get('rent_amount'),
            'court_date': raw.get('court_date'),
            'timestamp': datetime.utcnow().isoformat()
        }
        # naive deadline extraction
        if processed['deadline_text']:
            m = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', processed['deadline_text'])
            if m:
                processed['extracted_deadline'] = m.group(1)
        self.context = processed
        return processed

    # 2. Infer needs ---------------------------------------------------------
    def infer_needs(self) -> List[Dict[str, Any]]:
        issue = self.context.get('issue_type', '')
        needs = []
        if 'evict' in issue:
            needs.append({'code':'EVIDENCE_PACK','title':'Compile Rent & Notice Evidence','priority':1})
            needs.append({'code':'MOTION_STAY','title':'Prepare Motion to Stay/Delay','priority':2})
            needs.append({'code':'COURT_PREP','title':'Generate Hearing Preparation Checklist','priority':3})
        if 'repair' in issue:
            needs.append({'code':'REPAIR_DOC','title':'Document Repair Issues with Photos','priority':1})
            needs.append({'code':'NOTICE_LANDLORD','title':'Draft Formal Notice to Landlord','priority':2})
        if not needs:
            needs.append({'code':'INTAKE_BASELINE','title':'Gather Basic Tenancy Information','priority':1})
        self.needs = needs
        return needs

    # 3. Jurisdiction mapping -------------------------------------------------
    def map_jurisdiction(self) -> Dict[str, Any]:
        juris = self.context.get('jurisdiction', '').lower()
        data = {
            'raw': juris,
            'court_forms_supported': 'mn' in juris or 'minnesota' in juris,
            'special_rules': []
        }
        if 'minneapolis' in juris:
            data['special_rules'].append('Minneapolis Rent Cap Advisory')
        return data

    # 4. Build action plan ----------------------------------------------------
    def build_action_plan(self) -> List[Dict[str, Any]]:
        plan = []
        base_day = datetime.utcnow()
        for i, need in enumerate(sorted(self.needs, key=lambda n: n['priority'])):
            plan.append({
                'step_number': i+1,
                'code': need['code'],
                'title': need['title'],
                'due': (base_day + timedelta(days=i)).date().isoformat(),
                'status': 'pending',
                'instructions': self._generate_instructions_for_need(need['code'])
            })
        self.action_plan = plan
        return plan

    def _generate_instructions_for_need(self, code: str) -> List[str]:
        mapping = {
            'EVIDENCE_PACK': [
                'Collect lease, rent receipts, eviction notice',
                'Scan or photograph documents and upload to vault',
                'Summarize payment history (dates + amounts)'
            ],
            'MOTION_STAY': [
                'Generate motion draft with case caption',
                'Insert factual basis (payment efforts, hardship)',
                'Prepare signature block and certificate of service'
            ],
            'COURT_PREP': [
                'List key facts chronologically',
                'Identify statute references (habitability, notice)',
                'Draft 2-3 concise arguments'
            ],
            'REPAIR_DOC': [
                'Photograph each issue with timestamp',
                'Record impact on habitability',
                'Log prior notice attempts'
            ],
            'NOTICE_LANDLORD': [
                'Specify defects plainly',
                'Request repair timeline',
                'State potential escalation (rent escrow)'
            ],
            'INTAKE_BASELINE': [
                'Enter lease start/end dates',
                'Provide monthly rent + payment method',
                'Upload any prior notices'
            ]
        }
        return mapping.get(code, ['Describe need in detail', 'Attach supporting documents'])

    # 5. Generate artifacts ---------------------------------------------------
    def generate_artifacts(self) -> Dict[str, Any]:
        artifacts = {}
        # Evidence bundle manifest
        artifacts['evidence_manifest'] = {
            'expected_files': ['lease.pdf','rent_history.csv','eviction_notice.pdf'],
            'hashes': {},
            'status': 'pending'
        }
        # Draft motion skeleton
        if any(n['code']=='MOTION_STAY' for n in self.needs):
            artifacts['motion_draft'] = self._motion_template()
        # Checklist
        artifacts['checklist'] = [p['title'] for p in self.action_plan]
        # Calendar
        artifacts['calendar'] = [{
            'title': p['title'],
            'date': p['due'],
            'code': p['code']
        } for p in self.action_plan]
        self.artifacts = artifacts
        return artifacts

    def _motion_template(self) -> str:
        return (
            'IN COURT OF JURISDICTION\n'
            'Tenant (Defendant) Motion to Stay Eviction\n\n'
            '1. Background Facts: [AUTO-FILL]\n'
            '2. Legal Basis: [Insert local statute references]\n'
            '3. Relief Requested: Delay execution until resolution of issues.\n'
            'Signature: __________________ Date: __________\n'
        )

    # 6. Full bootstrap -------------------------------------------------------
    def bootstrap(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        self.collect_user_context(raw_input)
        self.infer_needs()
        juris = self.map_jurisdiction()
        self.build_action_plan()
        self.generate_artifacts()
        return {
            'context': self.context,
            'needs': self.needs,
            'jurisdiction': juris,
            'action_plan': self.action_plan,
            'artifacts': self.artifacts,
            'generated_at': datetime.utcnow().isoformat()
        }

# Convenience function
_engine_instance: SeedBootstrapEngine | None = None

def get_seed_bootstrap_engine() -> SeedBootstrapEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SeedBootstrapEngine()
    return _engine_instance
