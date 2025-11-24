"""
Seed Brad GUI with initial clients:
- User #1: Brad Crowe (client #1)
- User #2: Dena Sazama (client #2)
Each client gets a unique document_id and client_number.
"""
import json
import os
from datetime import datetime
from pathlib import Path

CLIENTS_FILE = Path(__file__).parent / 'data' / 'brad_clients' / 'clients.json'

def seed_clients():
    """Add user_number, client_number, and document_id to existing clients."""
    CLIENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing data
    if CLIENTS_FILE.exists():
        with open(CLIENTS_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                data = {'clients': [], 'active_client_id': None}
    else:
        data = {'clients': [], 'active_client_id': None}
    
    clients = data.get('clients', [])
    
    # Update Bradley Crowe if exists
    brad_found = False
    for idx, client in enumerate(clients):
        if 'Bradley' in client.get('name', '') or 'Brad' in client.get('name', ''):
            client['client_number'] = 1
            client['user_number'] = 1
            client['document_id'] = 'DOC-BC-001'
            print(f'[SEED] Updated {client["name"]} -> user#1, client#1, DOC-BC-001')
            brad_found = True
            break
    
    # Add Brad if not found
    if not brad_found:
        now = datetime.utcnow().isoformat()
        brad = {
            'id': 'client_001',
            'client_number': 1,
            'user_number': 1,
            'document_id': 'DOC-BC-001',
            'name': 'Brad Crowe',
            'contact': 'Bradcowe45@gmail.com',
            'address': '2977 Lexington Ave S, Eagan, MN 55121',
            'case_number': '',
            'created_at': now,
            'status': 'active',
            'notes': 'Primary user - eviction case'
        }
        clients.insert(0, brad)
        data['active_client_id'] = 'client_001'
        print('[SEED] Created Brad Crowe -> user#1, client#1, DOC-BC-001')
    
    # Add Dena Sazama if not exists
    dena_found = any('Dena' in c.get('name', '') for c in clients)
    if not dena_found:
        now = datetime.utcnow().isoformat()
        dena = {
            'id': 'client_002',
            'client_number': 2,
            'user_number': 2,
            'document_id': 'DOC-DS-002',
            'name': 'Dena Sazama',
            'contact': 'dena.sazama@example.com',
            'address': '456 Oak Ave, Minneapolis, MN 55403',
            'case_number': '',
            'created_at': now,
            'status': 'active',
            'notes': 'Secondary user - eviction case'
        }
        clients.append(dena)
        print('[SEED] Created Dena Sazama -> user#2, client#2, DOC-DS-002')
    
    data['clients'] = clients
    
    with open(CLIENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f'[SEED] ✓ Total clients: {len(clients)}')

if __name__ == '__main__':
    seed_clients()
