"""
Packet Builder - Court packet assembly system using SQLite
Integrates with Document Vault to help users build court packets from their uploaded documents
"""
from flask import Blueprint, jsonify, request, g
import sqlite3
import os
import json
from datetime import datetime
from user_database import DB_PATH

packet_builder_bp = Blueprint('packet_builder', __name__)

def _db_connect():
    """Connect to SQLite database"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_packet_tables():
    """Initialize packet builder tables in database"""
    conn = _db_connect()
    cur = conn.cursor()
    
    # Documents table - stores vault documents
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vault_documents (
            doc_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            category TEXT,
            upload_date TEXT NOT NULL,
            file_size INTEGER,
            sha256_hash TEXT,
            description TEXT,
            tags TEXT,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Packets table - stores assembled court packets
    cur.execute('''
        CREATE TABLE IF NOT EXISTS court_packets (
            packet_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            packet_name TEXT NOT NULL,
            packet_type TEXT NOT NULL,
            created_date TEXT NOT NULL,
            modified_date TEXT,
            status TEXT DEFAULT 'draft',
            notes TEXT,
            metadata TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Packet items junction table - links documents to packets
    cur.execute('''
        CREATE TABLE IF NOT EXISTS packet_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            packet_id TEXT NOT NULL,
            doc_id TEXT NOT NULL,
            item_order INTEGER DEFAULT 0,
            page_range TEXT,
            notes TEXT,
            added_date TEXT NOT NULL,
            FOREIGN KEY (packet_id) REFERENCES court_packets(packet_id),
            FOREIGN KEY (doc_id) REFERENCES vault_documents(doc_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[OK] Packet builder tables initialized")

def _get_user_id():
    """Get authenticated user ID from session/token"""
    # TODO: Integrate with actual auth system
    # For now, check for user_token in query params or headers
    user_token = request.args.get('user_token') or request.headers.get('X-User-Token')
    if not user_token:
        return None
    
    # Look up user by token
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE user_id = ?', (user_token,))
    result = cur.fetchone()
    conn.close()
    return result['user_id'] if result else None

@packet_builder_bp.route('/api/packet-builder/vault-items', methods=['GET'])
def get_vault_items():
    """Get all vault documents for current user, categorized"""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute('''
        SELECT doc_id, filename, file_type, category, upload_date, 
               file_size, description, tags
        FROM vault_documents
        WHERE user_id = ?
        ORDER BY upload_date DESC
    ''', (user_id,))
    
    docs = cur.fetchall()
    conn.close()
    
    # Categorize documents
    categorized = {
        'evidence': [],
        'receipts': [],
        'correspondence': [],
        'photos': [],
        'recordings': [],
        'other': []
    }
    
    for doc in docs:
        doc_dict = dict(doc)
        category = doc_dict.get('category', 'other').lower()
        if category in categorized:
            categorized[category].append(doc_dict)
        else:
            categorized['other'].append(doc_dict)
    
    return jsonify({
        'success': True,
        'items': categorized,
        'total': len(docs)
    })

@packet_builder_bp.route('/api/packet-builder/create', methods=['POST'])
def create_packet():
    """Create a new court packet from selected documents"""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    packet_name = data.get('name', 'Untitled Packet')
    packet_type = data.get('type', 'general')
    doc_ids = data.get('document_ids', [])
    notes = data.get('notes', '')
    
    # Generate packet ID
    packet_id = f"packet_{user_id}_{int(datetime.now().timestamp())}"
    created = datetime.now().isoformat()
    
    conn = _db_connect()
    cur = conn.cursor()
    
    try:
        # Create packet
        cur.execute('''
            INSERT INTO court_packets 
            (packet_id, user_id, packet_name, packet_type, created_date, modified_date, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (packet_id, user_id, packet_name, packet_type, created, created, 'draft', notes))
        
        # Add documents to packet
        for i, doc_id in enumerate(doc_ids):
            cur.execute('''
                INSERT INTO packet_items
                (packet_id, doc_id, item_order, added_date)
                VALUES (?, ?, ?, ?)
            ''', (packet_id, doc_id, i, created))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'packet_id': packet_id,
            'message': f'Packet "{packet_name}" created with {len(doc_ids)} documents'
        })
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@packet_builder_bp.route('/api/packet-builder/packets', methods=['GET'])
def list_packets():
    """List all packets for current user"""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = _db_connect()
    cur = conn.cursor()
    
    # Get packets with document count
    cur.execute('''
        SELECT cp.packet_id, cp.packet_name, cp.packet_type, 
               cp.created_date, cp.modified_date, cp.status, cp.notes,
               COUNT(pi.doc_id) as doc_count
        FROM court_packets cp
        LEFT JOIN packet_items pi ON cp.packet_id = pi.packet_id
        WHERE cp.user_id = ?
        GROUP BY cp.packet_id
        ORDER BY cp.created_date DESC
    ''', (user_id,))
    
    packets = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'packets': packets,
        'total': len(packets)
    })

@packet_builder_bp.route('/api/packet-builder/packet/<packet_id>', methods=['GET'])
def get_packet_details(packet_id):
    """Get detailed information about a specific packet"""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = _db_connect()
    cur = conn.cursor()
    
    # Get packet info
    cur.execute('''
        SELECT * FROM court_packets
        WHERE packet_id = ? AND user_id = ?
    ''', (packet_id, user_id))
    
    packet = cur.fetchone()
    if not packet:
        conn.close()
        return jsonify({'error': 'Packet not found'}), 404
    
    # Get packet documents
    cur.execute('''
        SELECT vd.*, pi.item_order, pi.page_range, pi.notes as item_notes
        FROM packet_items pi
        JOIN vault_documents vd ON pi.doc_id = vd.doc_id
        WHERE pi.packet_id = ?
        ORDER BY pi.item_order
    ''', (packet_id,))
    
    documents = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'packet': dict(packet),
        'documents': documents
    })

# Initialize tables when module loads
try:
    init_packet_tables()
except Exception as e:
    print(f"[ERROR] Failed to initialize packet tables: {e}")


