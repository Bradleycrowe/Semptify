"""
Patch vault_bp.py to integrate Phase 2 bidirectional calendar-vault sync
"""
import re

# Read existing vault_bp.py
with open('blueprints/vault_bp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the integration code to add after successful upload
integration_code = '''
    # === PHASE 2: Auto-create calendar event from upload ===
    try:
        from calendar_vault_bridge import CalendarVaultBridge
        from datetime import datetime
        
        bridge = CalendarVaultBridge()
        document_info = {
            'doc_id': cert_id,
            'filename': uploaded_file.filename if hasattr(uploaded_file, 'filename') else 'document',
            'file_type': uploaded_file.content_type if hasattr(uploaded_file, 'content_type') else 'unknown',
            'upload_date': datetime.utcnow().isoformat(),
            'category': request.form.get('category', 'general')
        }
        
        event_data = bridge.create_event_from_upload(user_token, document_info)
        
        if event_data:
            flash(f"✓ Document uploaded + Timeline event auto-created: {event_data['title']}", 'success')
        else:
            flash("✓ Document uploaded to vault", 'success')
    except Exception as e:
        # Don't break upload if calendar integration fails
        flash("✓ Document uploaded (calendar sync unavailable)", 'warning')
        print(f"[WARN] Calendar sync failed: {e}")
    # === END PHASE 2 ===
'''

# Find the notary_upload function and identify where to inject
# Look for the return statement after successful upload
pattern = r'(def notary_upload\(\):.*?)(return\s+.*?redirect.*?notary)'
match = re.search(pattern, content, re.DOTALL)

if match:
    # Check if already patched
    if 'PHASE 2' in content:
        print("✓ vault_bp.py already contains Phase 2 integration")
    else:
        # Insert integration code before the return statement
        before = content[:match.end(1)]
        after = content[match.start(2):]
        patched = before + '\n' + integration_code + '\n    ' + after
        
        # Write patched file
        with open('blueprints/vault_bp.py', 'w', encoding='utf-8') as f:
            f.write(patched)
        
        print("✓ Patched blueprints/vault_bp.py with Phase 2 calendar integration")
        print(f"  Added {len(integration_code.split(chr(10)))} lines of integration code")
else:
    print("⚠ Could not find notary_upload function pattern")
    print("  Will create manual integration guide instead")
