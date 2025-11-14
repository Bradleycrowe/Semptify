"""
Court Packet Wizard - Step-by-step flow to assemble evidence packets for court.
Guides users through gathering documents, organizing evidence, and creating shareable PDF.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List
import hashlib


# Checklist for different court case types
PACKET_TEMPLATES = {
    'eviction_defense': {
        'name': 'Eviction Defense Packet',
        'required_docs': [
            'Lease agreement',
            'Rent payment records',
            'Communication with landlord',
            'Photos of property condition',
            'Repair requests (if applicable)'
        ],
        'optional_docs': [
            'Witness statements',
            'Code violation reports',
            'Medical documentation (if relevant)'
        ],
        'sections': [
            'Cover Page',
            'Summary of Facts',
            'Timeline of Events',
            'Evidence Documents',
            'Witness Information',
            'Legal Arguments'
        ]
    },
    'small_claims': {
        'name': 'Small Claims Packet',
        'required_docs': [
            'Contract or agreement',
            'Proof of payment',
            'Communication records',
            'Photos of damages (if applicable)'
        ],
        'optional_docs': [
            'Receipts',
            'Expert opinions',
            'Witness statements'
        ],
        'sections': [
            'Cover Page',
            'Claim Summary',
            'Evidence',
            'Supporting Documents',
            'Witness List'
        ]
    },
    'housing_discrimination': {
        'name': 'Housing Discrimination Packet',
        'required_docs': [
            'Application documents',
            'Communication records',
            'Photos/videos (if applicable)',
            'Witness statements'
        ],
        'optional_docs': [
            'Comparable listings',
            'Expert testimony',
            'Policy documents'
        ],
        'sections': [
            'Cover Page',
            'Discrimination Summary',
            'Timeline of Events',
            'Evidence',
            'Witness Information',
            'Legal Basis'
        ]
    },
    'general': {
        'name': 'General Court Packet',
        'required_docs': [
            'Relevant documents',
            'Communication records',
            'Evidence photos'
        ],
        'optional_docs': [
            'Witness statements',
            'Expert opinions'
        ],
        'sections': [
            'Cover Page',
            'Case Summary',
            'Evidence',
            'Supporting Documents'
        ]
    }
}


def create_packet(user_id: str, case_type: str, case_info: Dict[str, Any], 
                 data_dir: str = 'data') -> Dict[str, Any]:
    """
    Create a new court packet.
    
    Args:
        user_id: Anonymous user ID
        case_type: Type of case (eviction_defense, small_claims, etc.)
        case_info: Dict with case_name, case_number, court_name, hearing_date, summary
        data_dir: Base data directory
    
    Returns:
        Dict with packet_id, packet_path, template
    """
    packet_id = hashlib.sha256(
        f"{user_id}{case_type}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    
    template = PACKET_TEMPLATES.get(case_type, PACKET_TEMPLATES['general'])
    
    packet_data = {
        'packet_id': packet_id,
        'user_id': user_id,
        'case_type': case_type,
        'case_name': case_info.get('case_name', 'Untitled Case'),
        'case_number': case_info.get('case_number', ''),
        'court_name': case_info.get('court_name', ''),
        'hearing_date': case_info.get('hearing_date', ''),
        'summary': case_info.get('summary', ''),
        'template': template,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'status': 'draft',  # draft, review, finalized, submitted
        'documents': [],
        'checklist_progress': {doc: False for doc in template['required_docs']},
        'sections_completed': {section: False for section in template['sections']}
    }
    
    # Save packet
    packets_dir = os.path.join(data_dir, 'court_packets', user_id)
    os.makedirs(packets_dir, exist_ok=True)
    
    packet_path = os.path.join(packets_dir, f"{packet_id}.json")
    with open(packet_path, 'w') as f:
        json.dump(packet_data, f, indent=2)
    
    return {
        'packet_id': packet_id,
        'packet_path': packet_path,
        'packet_data': packet_data
    }


def add_document_to_packet(packet_id: str, user_id: str, document: Dict[str, Any], 
                           data_dir: str = 'data') -> bool:
    """
    Add a document to an existing packet.
    
    Args:
        packet_id: Packet ID
        user_id: User ID
        document: Dict with file_path, doc_type, description, tags
        data_dir: Base data directory
    
    Returns:
        True if successful
    """
    packet_path = os.path.join(data_dir, 'court_packets', user_id, f"{packet_id}.json")
    
    if not os.path.exists(packet_path):
        return False
    
    with open(packet_path, 'r') as f:
        packet_data = json.load(f)
    
    # Add document
    doc_entry = {
        'doc_id': hashlib.sha256(
            f"{document['file_path']}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8],
        'file_path': document['file_path'],
        'doc_type': document.get('doc_type', 'general'),
        'description': document.get('description', ''),
        'tags': document.get('tags', []),
        'added_at': datetime.now().isoformat()
    }
    packet_data['documents'].append(doc_entry)
    
    # Update checklist if doc_type matches required doc
    doc_type_lower = document.get('doc_type', '').lower()
    for req_doc in packet_data['checklist_progress'].keys():
        if doc_type_lower in req_doc.lower():
            packet_data['checklist_progress'][req_doc] = True
    
    packet_data['updated_at'] = datetime.now().isoformat()
    
    with open(packet_path, 'w') as f:
        json.dump(packet_data, f, indent=2)
    
    return True


def update_section_status(packet_id: str, user_id: str, section: str, 
                         completed: bool, data_dir: str = 'data') -> bool:
    """Mark a section as completed or incomplete."""
    packet_path = os.path.join(data_dir, 'court_packets', user_id, f"{packet_id}.json")
    
    if not os.path.exists(packet_path):
        return False
    
    with open(packet_path, 'r') as f:
        packet_data = json.load(f)
    
    if section in packet_data['sections_completed']:
        packet_data['sections_completed'][section] = completed
        packet_data['updated_at'] = datetime.now().isoformat()
        
        with open(packet_path, 'w') as f:
            json.dump(packet_data, f, indent=2)
        
        return True
    
    return False


def get_packet(packet_id: str, user_id: str, data_dir: str = 'data') -> Dict[str, Any]:
    """Retrieve a packet by ID."""
    packet_path = os.path.join(data_dir, 'court_packets', user_id, f"{packet_id}.json")
    
    if not os.path.exists(packet_path):
        return None
    
    with open(packet_path, 'r') as f:
        return json.load(f)


def list_packets(user_id: str, data_dir: str = 'data', 
                status_filter: str = None) -> List[Dict[str, Any]]:
    """List all packets for a user, optionally filtered by status."""
    packets_dir = os.path.join(data_dir, 'court_packets', user_id)
    
    if not os.path.exists(packets_dir):
        return []
    
    packets = []
    for filename in os.listdir(packets_dir):
        if filename.endswith('.json'):
            with open(os.path.join(packets_dir, filename), 'r') as f:
                packet_data = json.load(f)
            
            if status_filter:
                if packet_data.get('status') == status_filter:
                    packets.append(packet_data)
            else:
                packets.append(packet_data)
    
    # Sort by updated_at descending
    packets.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    return packets


def get_packet_progress(packet_id: str, user_id: str, data_dir: str = 'data') -> Dict[str, Any]:
    """Calculate packet completion progress."""
    packet = get_packet(packet_id, user_id, data_dir)
    if not packet:
        return None
    
    checklist = packet['checklist_progress']
    sections = packet['sections_completed']
    
    checklist_complete = sum(1 for v in checklist.values() if v)
    checklist_total = len(checklist)
    
    sections_complete = sum(1 for v in sections.values() if v)
    sections_total = len(sections)
    
    overall_progress = (checklist_complete + sections_complete) / (checklist_total + sections_total) * 100
    
    return {
        'packet_id': packet_id,
        'status': packet['status'],
        'checklist_progress': f"{checklist_complete}/{checklist_total}",
        'sections_progress': f"{sections_complete}/{sections_total}",
        'overall_progress': round(overall_progress, 1),
        'is_ready': overall_progress >= 80  # 80% complete = ready for review
    }


# Demo/test
if __name__ == "__main__":
    print("Court Packet Wizard - Demo\n")
    
    test_user_id = 'user123'
    
    # Create eviction defense packet
    packet = create_packet(
        user_id=test_user_id,
        case_type='eviction_defense',
        case_info={
            'case_name': 'Smith v. Jones Landlord LLC',
            'case_number': 'CV-2025-001234',
            'court_name': 'District Court - Housing Division',
            'hearing_date': '2025-03-15',
            'summary': 'Eviction defense due to uninhabitable conditions'
        }
    )
    
    print(f"Packet Created: {packet['packet_id']}")
    print(f"Case: {packet['packet_data']['case_name']}")
    print(f"Required Documents: {len(packet['packet_data']['template']['required_docs'])}")
    print(f"Sections: {len(packet['packet_data']['template']['sections'])}\n")
    
    # Add document
    add_document_to_packet(
        packet_id=packet['packet_id'],
        user_id=test_user_id,
        document={
            'file_path': '/uploads/lease_agreement.pdf',
            'doc_type': 'Lease agreement',
            'description': 'Original lease showing terms',
            'tags': ['lease', 'contract']
        }
    )
    print("Document added: Lease agreement\n")
    
    # Check progress
    progress = get_packet_progress(packet['packet_id'], test_user_id)
    print(f"Progress: {progress['overall_progress']}%")
    print(f"Checklist: {progress['checklist_progress']}")
    print(f"Sections: {progress['sections_progress']}")
    print(f"Ready for Review: {progress['is_ready']}")
