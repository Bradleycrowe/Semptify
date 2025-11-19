"""
Calendar Master View - Central hub for vault documents, events, and packet assembly
"""
from flask import Blueprint, render_template, request, jsonify
from calendar_vault_bridge import CalendarVaultBridge
from functools import wraps
import sqlite3
from user_database import DB_PATH

calendar_master_bp = Blueprint('calendar_master', __name__)

def _get_user_token():
    """Extract user token from request"""
    return request.args.get('user_token') or request.headers.get('X-User-Token') or request.form.get('user_token')

@calendar_master_bp.route('/calendar')
def calendar_master():
    """Master calendar view - visual reference to documented journey"""
    user_token = _get_user_token()
    return render_template('calendar_master.html', user_token=user_token)

@calendar_master_bp.route('/api/calendar/vault-items')
def vault_items():
    """Get all vault items organized by date from SQLite"""
    user_token = _get_user_token()
    if not user_token:
        return jsonify({"error": "Authentication required"}), 401
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            '''SELECT doc_id, filename, file_type, category, upload_date, file_size, description, tags
               FROM vault_documents WHERE user_id = ? ORDER BY upload_date DESC''',
            (user_token,)
        )
        rows = cur.fetchall()
        items = [dict(r) for r in rows]
        return jsonify({
            "items": items,
            "categories": ["evidence","receipts","correspondence","photos","recordings","other"],
            "timeline": []
        })
    except Exception as e:
        return jsonify({"error": str(e), "items": [], "categories": [], "timeline": []}), 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

@calendar_master_bp.route('/api/calendar/packet-builder')
def packet_builder():
    """Get available items for court packet assembly"""
    return jsonify({
        "available_items": [],
        "packet_types": ["eviction_defense", "repair_claim", "discrimination", "security_deposit"],
        "templates": []
    })





# === PHASE 2 CALENDAR INTEGRATION ===
# After event creation, add:
#   bridge = CalendarVaultBridge()
#   suggestions = bridge.suggest_documents_for_event(event_type, event_data)
#   if suggestions:
#       doc_list = ', '.join([s['doc_type'] for s in suggestions])
#       flash(f"💡 Recommended uploads: {doc_list}", 'info')
