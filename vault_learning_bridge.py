"""
Phase 3: Vault-Learning Bridge
Connects document uploads to relevant learning module recommendations
"""
from typing import List, Dict, Optional
import os
import json

class VaultLearningBridge:
    """Triggers learning recommendations based on uploaded documents"""
    
    def __init__(self, learning_data_path='data/learning'):
        self.learning_path = learning_data_path
        
        # Map document types to learning modules
        self.doc_to_learning = {
            'eviction_notice': ['eviction_defense', 'court_procedures', 'tenant_rights'],
            'lease': ['lease_understanding', 'tenant_rights', 'security_deposits'],
            'repair_request': ['repair_rights', 'habitability', 'documentation'],
            'notice': ['tenant_rights', 'notice_response', 'documentation'],
            'receipt': ['rent_payments', 'documentation', 'record_keeping'],
            'inspection': ['move_in_rights', 'security_deposits', 'documentation'],
            'correspondence': ['communication_rights', 'documentation'],
            'complaint': ['filing_complaints', 'court_procedures', 'evidence']
        }
    
    def get_learning_for_upload(self, doc_type: str, filename: str) -> List[Dict]:
        """
        Recommend learning modules based on uploaded document
        
        Args:
            doc_type: Type of document uploaded
            filename: Name of uploaded file
            
        Returns:
            List of learning recommendations with reasons
        """
        recommendations = []
        
        # Detect doc type from filename if not provided
        if doc_type == 'general' or not doc_type:
            doc_type = self._detect_type_from_filename(filename)
        
        # Get learning modules for this doc type
        modules = self.doc_to_learning.get(doc_type, ['tenant_rights', 'documentation'])
        
        for module_id in modules:
            recommendations.append({
                'module_id': module_id,
                'title': self._get_module_title(module_id),
                'reason': self._get_reason(doc_type, module_id),
                'urgency': self._get_learning_urgency(doc_type),
                'estimated_time': '5-10 min'
            })
        
        return recommendations
    
    def get_learning_progress_boost(self, user_id: str, doc_type: str) -> Dict:
        """
        Check if document upload unlocks new learning content
        
        Args:
            user_id: User identifier
            doc_type: Type of document uploaded
            
        Returns:
            Dict with unlocked modules and progress update
        """
        unlocked = []
        
        # Certain docs unlock advanced modules
        if doc_type in ['eviction_notice', 'complaint']:
            unlocked.append({
                'module': 'court_procedures_advanced',
                'reason': f'Your {doc_type} upload unlocked advanced court procedures'
            })
        
        return {
            'unlocked_modules': unlocked,
            'progress_increase': len(unlocked) * 10  # 10% per unlock
        }
    
    def _detect_type_from_filename(self, filename: str) -> str:
        """Detect document type from filename"""
        filename_lower = filename.lower()
        
        keywords = {
            'eviction': 'eviction_notice',
            'notice': 'notice',
            'lease': 'lease',
            'repair': 'repair_request',
            'receipt': 'receipt',
            'inspection': 'inspection',
            'complaint': 'complaint',
            'letter': 'correspondence'
        }
        
        for keyword, doc_type in keywords.items():
            if keyword in filename_lower:
                return doc_type
        
        return 'general'
    
    def _get_module_title(self, module_id: str) -> str:
        """Get human-readable module title"""
        titles = {
            'eviction_defense': 'Eviction Defense Basics',
            'court_procedures': 'How Court Works',
            'tenant_rights': 'Know Your Rights',
            'lease_understanding': 'Understanding Your Lease',
            'security_deposits': 'Security Deposit Rights',
            'repair_rights': 'Right to Repairs',
            'habitability': 'Habitability Standards',
            'documentation': 'Evidence Documentation',
            'notice_response': 'Responding to Notices',
            'rent_payments': 'Rent Payment Records',
            'record_keeping': 'Keeping Good Records',
            'move_in_rights': 'Move-In/Move-Out Rights',
            'communication_rights': 'Communication with Landlord',
            'filing_complaints': 'Filing Formal Complaints',
            'evidence': 'Building Your Evidence Case'
        }
        return titles.get(module_id, module_id.replace('_', ' ').title())
    
    def _get_reason(self, doc_type: str, module_id: str) -> str:
        """Explain why this module is recommended"""
        reasons = {
            ('eviction_notice', 'eviction_defense'): 'Learn how to respond to eviction notices and protect your rights',
            ('eviction_notice', 'court_procedures'): 'Understand what happens if your case goes to court',
            ('repair_request', 'repair_rights'): 'Know your rights when requesting repairs',
            ('repair_request', 'habitability'): 'Learn what repairs landlords must make',
            ('lease', 'lease_understanding'): 'Understand what your lease actually means',
            ('receipt', 'rent_payments'): 'Learn how to document rent payments properly',
            ('complaint', 'filing_complaints'): 'Understand the complaint filing process',
        }
        
        return reasons.get((doc_type, module_id), f'Recommended for {doc_type} situations')
    
    def _get_learning_urgency(self, doc_type: str) -> str:
        """Determine urgency of learning recommendation"""
        urgent_types = ['eviction_notice', 'notice', 'complaint']
        return 'high' if doc_type in urgent_types else 'normal'
