"""
Patch vault_bp.py with Phase 2 calendar integration
Adds auto-event creation after document upload
"""
import re

# Read vault_bp.py
with open('blueprints/vault_bp.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already patched
if 'PHASE 2' in content or 'calendar_vault_bridge' in content:
    print("✓ vault_bp.py already contains Phase 2 integration")
    exit(0)

# Find the imports section and add bridge import
import_pattern = r'(from flask import .*?\n)'
import_addition = '''from calendar_vault_bridge import CalendarVaultBridge
from datetime import datetime
'''

# Find first Flask import and add our imports after
match = re.search(r'(from flask import [^\n]+\n)', content)
if match:
    pos = match.end()
    content = content[:pos] + import_addition + content[pos:]
    print("✓ Added imports")
else:
    print("⚠ Could not find Flask imports, adding at top")
    content = import_addition + content

# Find the notary_upload function and add Phase 2 integration
# Look for successful upload completion (typically before return/redirect)
notary_pattern = r'(def notary_upload\(\):.*?)(flash\(["\'].*?uploaded.*?["\'].*?\).*?return)'

match = re.search(notary_pattern, content, re.DOTALL | re.IGNORECASE)

if match:
    integration_code = '''
    
    # === PHASE 2: Auto-create calendar event ===
    try:
        bridge = CalendarVaultBridge()
        doc_info = {
            'doc_id': cert_id if 'cert_id' in locals() else str(hash(uploaded_filename)),
            'filename': uploaded_filename if 'uploaded_filename' in locals() else 'document',
            'file_type': request.files.get('file').content_type if request.files.get('file') else 'unknown',
            'upload_date': datetime.utcnow().isoformat(),
            'category': request.form.get('category', request.form.get('doc_type', 'general'))
        }
        event = bridge.create_event_from_upload(user_token, doc_info)
        if event:
            flash(f"✓ Document + Timeline event created: {event['title']}", 'success')
    except Exception as e:
        print(f"[PHASE2] Calendar sync error: {e}")
    # === END PHASE 2 ===
    
    '''
    
    # Insert before the flash/return
    before = content[:match.start(2)]
    after = content[match.start(2):]
    content = before + integration_code + after
    print("✓ Added Phase 2 integration to notary_upload()")
else:
    print("⚠ Could not find notary_upload pattern, adding manual integration point")
    # Add a marker for manual integration
    content += '''

# === PHASE 2 INTEGRATION POINT ===
# Add this code after successful upload in your upload functions:
#
# from calendar_vault_bridge import CalendarVaultBridge
# bridge = CalendarVaultBridge()
# doc_info = {'doc_id': doc_id, 'filename': filename, 'file_type': filetype, 
#             'upload_date': datetime.utcnow().isoformat(), 'category': category}
# event = bridge.create_event_from_upload(user_token, doc_info)
# if event: flash(f"Document + Event created: {event['title']}", 'success')
'''

# Write patched file
with open('blueprints/vault_bp.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ vault_bp.py patched with Phase 2 integration")
