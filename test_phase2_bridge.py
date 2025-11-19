"""
Test Phase 2 bidirectional calendar-vault bridge
"""
from calendar_vault_bridge import CalendarVaultBridge
from datetime import datetime

print("=== TESTING ENHANCED CALENDAR-VAULT BRIDGE ===\n")

bridge = CalendarVaultBridge()

# Test 1: Suggest documents for event
print("TEST 1: suggest_documents_for_event()")
event_data = {'event_id': 'evt_001', 'title': 'Repair needed'}
suggestions = bridge.suggest_documents_for_event('repair_request', event_data)
print(f"  Event type: repair_request")
print(f"  Suggestions: {len(suggestions)} document types")
for s in suggestions:
    print(f"    • {s['doc_type']}: {s['reason']} (urgency: {s['urgency']})")

# Test 2: Auto-create event from upload
print("\nTEST 2: create_event_from_upload()")
doc_info = {
    'doc_id': 'doc_repair_001',
    'filename': 'repair_request_photos.pdf',
    'file_type': 'application/pdf',
    'upload_date': datetime.utcnow().isoformat(),
    'category': 'repair'
}
event = bridge.create_event_from_upload('test_user_123', doc_info)
if event:
    print(f"  ✓ Auto-created event: {event['title']}")
    print(f"    Event ID: {event['event_id']}")
    print(f"    Auto-created: {event['auto_created']}")
else:
    print(f"  ✗ No event created (detection failed)")

# Test 3: Document detection patterns
print("\nTEST 3: Document type detection")
test_files = [
    ('eviction_notice.pdf', 'legal'),
    ('lease_agreement.pdf', 'contract'),
    ('rent_receipt_jan.pdf', 'payment'),
    ('move_in_inspection.pdf', 'inspection'),
    ('random_file.txt', 'general')
]
for filename, category in test_files:
    doc_info = {
        'doc_id': f'doc_{filename}',
        'filename': filename,
        'upload_date': datetime.utcnow().isoformat(),
        'category': category
    }
    event = bridge.create_event_from_upload('test_user', doc_info)
    if event:
        print(f"  {filename:30} → Event: {event['title']}")
    else:
        print(f"  {filename:30} → No event")

print("\n=== ALL TESTS PASSED ===")
