"""
Delivery System for Semptify
Multi-method delivery tracking: Email, USPS, Certified Mail, Hand Delivery
Based on README_DELIVERY.md specification
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class DeliveryMethodType(Enum):
    """Supported delivery methods"""
    EMAIL = "EMAIL"
    USPS = "USPS"
    CERTIFIED_MAIL = "CERTIFIED"
    HAND_DELIVERY = "HAND"
    COURIER = "COURIER"


class DeliveryStatus(Enum):
    """Delivery job statuses"""
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    PARTIALLY_DELIVERED = "PARTIALLY_DELIVERED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class MethodStatus(Enum):
    """Individual method statuses"""
    PENDING = "PENDING"
    ATTEMPTING = "ATTEMPTING"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class DeliverySystem:
    """
    Manages delivery jobs with multiple methods.
    Tracks attempts, confirmations, and proof of delivery.
    """
    
    def __init__(self, data_file='data/deliveries.json', proof_dir='uploads/delivery_proofs'):
        self.data_file = data_file
        self.proof_dir = proof_dir
        self.deliveries = self._load_deliveries()
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        os.makedirs(self.proof_dir, exist_ok=True)
    
    def _load_deliveries(self) -> List[Dict]:
        """Load delivery jobs from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_deliveries(self):
        """Save delivery jobs to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.deliveries, f, indent=2, ensure_ascii=False)
    
    def create_delivery_job(self, case_id: str, created_by: str, 
                           methods: List[Dict], priority_order: List[str],
                           user_id: Optional[str] = None,
                           metadata: Optional[Dict] = None) -> Dict:
        """
        Create a new delivery job with multiple delivery methods.
        
        Args:
            case_id: Associated case ID
            created_by: User creating the delivery
            methods: List of delivery method configs [{"id": "m1", "type": "EMAIL", ...}]
            priority_order: Order to attempt methods ["m1", "m2", ...]
            user_id: Optional user ID
            metadata: Additional data (document IDs, notes, etc.)
        
        Returns:
            Created delivery job dict
        """
        delivery_id = f"del_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Validate method IDs match priority order
        method_ids = {m['id'] for m in methods}
        priority_ids = set(priority_order)
        if method_ids != priority_ids:
            raise ValueError("Method IDs must match priority order")
        
        # Validate required fields for each method
        for method in methods:
            self._validate_method(method)
        
        delivery_job = {
            'id': delivery_id,
            'case_id': case_id,
            'created_by': created_by,
            'created_at': datetime.now().isoformat(),
            'methods': methods,
            'priority_order': priority_order,
            'status': DeliveryStatus.CREATED.value,
            'user_id': user_id,
            'metadata': metadata or {},
            'history': [
                {
                    'event': 'DELIVERY_CREATED',
                    'timestamp': datetime.now().isoformat(),
                    'actor': created_by,
                    'details': {'method_count': len(methods)}
                }
            ]
        }
        
        self.deliveries.append(delivery_job)
        self._save_deliveries()
        
        return delivery_job
    
    def _validate_method(self, method: Dict):
        """Validate delivery method has required fields"""
        required_fields = method.get('requiredFields', [])
        
        for field in required_fields:
            # Check nested fields (e.g., "recipientContact.email")
            parts = field.split('.')
            value = method
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    raise ValueError(f"Method {method['id']}: Missing required field '{field}'")
    
    def add_attempt(self, delivery_id: str, method_id: str,
                   actor: str, provider_response: Optional[str] = None,
                   tracking_number: Optional[str] = None,
                   proof_file_ids: Optional[List[str]] = None,
                   notes: Optional[str] = None) -> bool:
        """
        Record a delivery attempt for a specific method.
        
        Args:
            delivery_id: Delivery job ID
            method_id: Method ID (e.g., "m1")
            actor: User making the attempt
            provider_response: Response from email server, USPS, etc.
            tracking_number: Tracking number if applicable
            proof_file_ids: List of uploaded proof file IDs
            notes: Additional notes
        
        Returns:
            True if successful
        """
        delivery = self._get_delivery(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        method = self._get_method(delivery, method_id)
        if not method:
            raise ValueError(f"Method {method_id} not found")
        
        # Update method status
        method['status'] = MethodStatus.ATTEMPTING.value
        
        # Add attempt to history
        attempt = {
            'attempt_at': datetime.now().isoformat(),
            'actor': actor,
            'provider_response': provider_response,
            'tracking_number': tracking_number,
            'proof_file_ids': proof_file_ids or [],
            'notes': notes
        }
        
        if 'attempts' not in method:
            method['attempts'] = []
        method['attempts'].append(attempt)
        
        # Add to global history
        delivery['history'].append({
            'event': 'DELIVERY_ATTEMPTED',
            'timestamp': datetime.now().isoformat(),
            'actor': actor,
            'details': {
                'method_id': method_id,
                'method_type': method['type'],
                'tracking_number': tracking_number
            }
        })
        
        # Update delivery status
        if delivery['status'] == DeliveryStatus.CREATED.value:
            delivery['status'] = DeliveryStatus.IN_PROGRESS.value
        
        self._save_deliveries()
        return True
    
    def confirm_delivery(self, delivery_id: str, method_id: str,
                        actor: str, confirmed_at: Optional[str] = None,
                        proof_file_ids: Optional[List[str]] = None,
                        notes: Optional[str] = None) -> bool:
        """
        Confirm successful delivery for a method.
        
        Args:
            delivery_id: Delivery job ID
            method_id: Method ID
            actor: User confirming delivery
            confirmed_at: Timestamp (default: now)
            proof_file_ids: List of proof file IDs
            notes: Additional notes
        
        Returns:
            True if successful
        """
        delivery = self._get_delivery(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        method = self._get_method(delivery, method_id)
        if not method:
            raise ValueError(f"Method {method_id} not found")
        
        # Update method status
        method['status'] = MethodStatus.DELIVERED.value
        method['delivered_at'] = confirmed_at or datetime.now().isoformat()
        method['confirmed_by'] = actor
        
        if proof_file_ids:
            if 'proof_file_ids' not in method:
                method['proof_file_ids'] = []
            method['proof_file_ids'].extend(proof_file_ids)
        
        if notes:
            method['confirmation_notes'] = notes
        
        # Add to global history
        delivery['history'].append({
            'event': 'DELIVERY_CONFIRMED',
            'timestamp': datetime.now().isoformat(),
            'actor': actor,
            'details': {
                'method_id': method_id,
                'method_type': method['type'],
                'delivered_at': method['delivered_at']
            }
        })
        
        # Check if all methods delivered
        all_delivered = all(
            m['status'] == MethodStatus.DELIVERED.value
            for m in delivery['methods']
        )
        
        if all_delivered:
            delivery['status'] = DeliveryStatus.DELIVERED.value
            delivery['completed_at'] = datetime.now().isoformat()
        elif delivery['status'] == DeliveryStatus.IN_PROGRESS.value:
            delivery['status'] = DeliveryStatus.PARTIALLY_DELIVERED.value
        
        self._save_deliveries()
        return True
    
    def mark_failed(self, delivery_id: str, method_id: str,
                   actor: str, failure_reason: str) -> bool:
        """Mark a delivery method as failed"""
        delivery = self._get_delivery(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        method = self._get_method(delivery, method_id)
        if not method:
            raise ValueError(f"Method {method_id} not found")
        
        method['status'] = MethodStatus.FAILED.value
        method['failure_reason'] = failure_reason
        method['failed_at'] = datetime.now().isoformat()
        
        delivery['history'].append({
            'event': 'DELIVERY_FAILED',
            'timestamp': datetime.now().isoformat(),
            'actor': actor,
            'details': {
                'method_id': method_id,
                'method_type': method['type'],
                'reason': failure_reason
            }
        })
        
        # Check if all methods failed
        all_failed = all(
            m['status'] == MethodStatus.FAILED.value
            for m in delivery['methods']
        )
        
        if all_failed:
            delivery['status'] = DeliveryStatus.FAILED.value
        
        self._save_deliveries()
        return True
    
    def get_delivery(self, delivery_id: str) -> Optional[Dict]:
        """Get delivery job by ID"""
        return self._get_delivery(delivery_id)
    
    def get_deliveries(self, case_id: Optional[str] = None,
                      user_id: Optional[str] = None,
                      status: Optional[str] = None) -> List[Dict]:
        """
        Get filtered delivery jobs.
        
        Args:
            case_id: Filter by case
            user_id: Filter by user
            status: Filter by status
        
        Returns:
            List of matching delivery jobs
        """
        filtered = self.deliveries
        
        if case_id:
            filtered = [d for d in filtered if d.get('case_id') == case_id]
        
        if user_id:
            filtered = [d for d in filtered if d.get('user_id') == user_id]
        
        if status:
            filtered = [d for d in filtered if d['status'] == status]
        
        return sorted(filtered, key=lambda x: x['created_at'], reverse=True)
    
    def _get_delivery(self, delivery_id: str) -> Optional[Dict]:
        """Internal: Get delivery by ID"""
        for delivery in self.deliveries:
            if delivery['id'] == delivery_id:
                return delivery
        return None
    
    def _get_method(self, delivery: Dict, method_id: str) -> Optional[Dict]:
        """Internal: Get method from delivery"""
        for method in delivery['methods']:
            if method['id'] == method_id:
                return method
        return None


# Global instance
_delivery_system = None

def get_delivery_system() -> DeliverySystem:
    """Get or create delivery system instance"""
    global _delivery_system
    if _delivery_system is None:
        _delivery_system = DeliverySystem()
    return _delivery_system


if __name__ == '__main__':
    # Test delivery system
    system = get_delivery_system()
    
    print("Creating test delivery job...")
    
    delivery = system.create_delivery_job(
        case_id='CASE_123',
        created_by='user_7',
        methods=[
            {
                'id': 'm1',
                'type': 'EMAIL',
                'recipientName': 'Tenant Example',
                'recipientContact': {'email': 'tenant@example.com'},
                'instructions': 'Attach complaint PDF',
                'status': 'PENDING',
                'requiredFields': ['recipientContact.email']
            },
            {
                'id': 'm2',
                'type': 'USPS',
                'recipientName': 'Owner Example',
                'recipientContact': {'address': '123 Main St, City, ST, 00000'},
                'instructions': 'First class, keep tracking',
                'status': 'PENDING',
                'requiredFields': ['recipientContact.address']
            }
        ],
        priority_order=['m1', 'm2'],
        user_id='test_user_001'
    )
    
    print(f"✅ Created delivery: {delivery['id']}")
    print(f"   Status: {delivery['status']}")
    print(f"   Methods: {len(delivery['methods'])}")
    
    # Add attempt
    print("\nAdding email attempt...")
    system.add_attempt(
        delivery['id'],
        'm1',
        'user_7',
        provider_response='SMTP 250 OK',
        tracking_number='EMAIL_20251110_001'
    )
    
    # Confirm delivery
    print("Confirming email delivery...")
    system.confirm_delivery(
        delivery['id'],
        'm1',
        'user_7',
        proof_file_ids=['file_123']
    )
    
    # Get updated delivery
    updated = system.get_delivery(delivery['id'])
    print(f"\n📊 Delivery Status: {updated['status']}")
    print(f"   History events: {len(updated['history'])}")
    print(f"   Method m1 status: {updated['methods'][0]['status']}")
    print(f"   Method m2 status: {updated['methods'][1]['status']}")
    
    print("\n✅ Delivery system test complete!")
