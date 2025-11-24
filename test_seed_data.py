"""
Test Data Seeder - Create sample data for Context Ring testing
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

def seed_test_data():
    """Create test data for user ID 1"""
    
    print("=" * 70)
    print("  🌱 SEEDING TEST DATA FOR CONTEXT RING")
    print("=" * 70)
    print()
    
    # Database connection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 1. Ensure user 1 exists
    print("📊 Checking user 1...")
    cursor.execute("SELECT id FROM users WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, created_at)
            VALUES (1, 'test@example.com', 'test_hash', ?)
        """, (datetime.now().isoformat(),))
        print("   ✓ Created user 1")
    else:
        print("   ✓ User 1 exists")
    
    # 2. Create timeline_events table if needed
    print("\n📅 Setting up timeline_events table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_date TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            event_type TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 3. Add timeline events
    print("\n📅 Adding timeline events...")
    timeline_data = [
        {
            'date': (datetime.now() - timedelta(days=90)).date().isoformat(),
            'title': 'Moved into apartment',
            'description': 'Started tenancy at 123 Main St',
            'type': 'move_in'
        },
        {
            'date': (datetime.now() - timedelta(days=60)).date().isoformat(),
            'title': 'First maintenance issue reported',
            'description': 'Notified landlord about leaking faucet',
            'type': 'maintenance_request'
        },
        {
            'date': (datetime.now() - timedelta(days=45)).date().isoformat(),
            'title': 'No response from landlord',
            'description': 'Sent follow-up email, still no repair',
            'type': 'communication'
        },
        {
            'date': (datetime.now() - timedelta(days=30)).date().isoformat(),
            'title': 'Received eviction notice',
            'description': 'Notice to vacate in 30 days',
            'type': 'notice_received'
        },
        {
            'date': (datetime.now() - timedelta(days=15)).date().isoformat(),
            'title': 'Documented property condition',
            'description': 'Took photos and videos of all issues',
            'type': 'evidence_collected'
        }
    ]
    
    for event in timeline_data:
        cursor.execute("""
            INSERT INTO timeline_events (user_id, event_date, title, description, event_type)
            VALUES (1, ?, ?, ?, ?)
        """, (event['date'], event['title'], event['description'], event['type']))
    
    print(f"   ✓ Added {len(timeline_data)} timeline events")
    
    # 4. Create vault directory and sample documents
    print("\n📄 Creating sample documents in vault...")
    vault_dir = Path("uploads/vault/1")
    vault_dir.mkdir(parents=True, exist_ok=True)
    
    sample_docs = [
        {
            'filename': 'lease_agreement.pdf',
            'content': b'SAMPLE LEASE AGREEMENT - This is a test document for the lease',
            'type': 'lease'
        },
        {
            'filename': 'eviction_notice.pdf',
            'content': b'NOTICE TO VACATE - You have 30 days to vacate the premises',
            'type': 'notice'
        },
        {
            'filename': 'maintenance_email.txt',
            'content': b'Email to landlord about repairs needed - sent 60 days ago',
            'type': 'communication'
        },
        {
            'filename': 'rent_receipt_jan.pdf',
            'content': b'Rent payment receipt - January 2025 - Amount: 1200 dollars',
            'type': 'payment_record'
        },
        {
            'filename': 'apartment_photos.zip',
            'content': b'Photos of apartment condition and maintenance issues',
            'type': 'evidence'
        }
    ]
    
    for doc in sample_docs:
        doc_path = vault_dir / doc['filename']
        doc_path.write_bytes(doc['content'])
        
        # Create certificate
        sha256 = hashlib.sha256(doc['content']).hexdigest()
        timestamp = datetime.now().isoformat()
        
        cert = {
            'sha256': sha256,
            'ts': timestamp,
            'request_id': f'test_{doc["type"]}',
            'filename': doc['filename'],
            'doc_type': doc['type'],
            'size': len(doc['content'])
        }
        
        cert_path = vault_dir / f"notary_{timestamp.replace(':', '-')}_{doc['type']}.json"
        cert_path.write_text(json.dumps(cert, indent=2))
    
    print(f"   ✓ Created {len(sample_docs)} sample documents with certificates")
    
    # 5. Create cases table if needed
    print("\n⚖️ Setting up cases table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            case_type TEXT,
            jurisdiction TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add a case
    cursor.execute("""
        INSERT INTO cases (user_id, status, case_type, jurisdiction)
        VALUES (1, 'assessment', 'eviction_defense', 'minnesota')
    """)
    print("   ✓ Created case record")
    
    # 6. Create events table if needed
    print("\n📋 Setting up events table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_date TEXT NOT NULL,
            event_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            requires_action INTEGER DEFAULT 0,
            action_deadline TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add an urgent event
    deadline = (datetime.now() + timedelta(days=5)).date().isoformat()
    cursor.execute("""
        INSERT INTO events (user_id, event_date, event_type, title, description, requires_action, action_deadline)
        VALUES (1, ?, 'court_deadline', 'Answer eviction complaint', 'Response due in 5 days', 1, ?)
    """, (datetime.now().date().isoformat(), deadline))
    print("   ✓ Created urgent event")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print()
    print("=" * 70)
    print("  ✅ TEST DATA SEEDED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("User 1 now has:")
    print(f"  • {len(timeline_data)} timeline events")
    print(f"  • {len(sample_docs)} documents in vault")
    print("  • 1 active case (eviction defense)")
    print("  • 1 urgent action (court deadline in 5 days)")
    print()
    print("Ready to test Context Ring!")
    print("Try: python -c \"from semptify_core import get_context; ctx = get_context('1'); print(f'Strength: {ctx.overall_strength}%')\"")
    print()

if __name__ == "__main__":
    seed_test_data()

