"""
PHASE 2 INTEGRATION EXAMPLE
Shows how to integrate enhanced calendar_vault_bridge into vault and calendar routes
"""

# ===== IN VAULT UPLOAD ROUTES (blueprints/vault_bp.py) =====
# After successful file upload, auto-create calendar event

from calendar_vault_bridge import CalendarVaultBridge

@vault_bp.route('/upload', methods=['POST'])
def vault_upload():
    # ... existing upload code ...
    # file saved, certificate created
    
    # NEW: Auto-create calendar event from upload
    bridge = CalendarVaultBridge()
    
    document_info = {
        'doc_id': doc_id,
        'filename': secure_filename(file.filename),
        'file_type': file.content_type,
        'upload_date': datetime.utcnow().isoformat(),
        'category': request.form.get('category', 'general')
    }
    
    # Let bridge detect if this upload should create an event
    event_data = bridge.create_event_from_upload(user_id, document_info)
    
    if event_data:
        # Event auto-created! Show user a notification
        flash(f"✓ Document uploaded + Timeline event created: {event_data['title']}", 'success')
        
        # Optional: Save event to calendar system
        # from calendar_master import save_event
        # save_event(user_id, event_data)
    else:
        flash(f"✓ Document uploaded to vault", 'success')
    
    return redirect(url_for('vault_bp.vault', user_token=user_id))


# ===== IN CALENDAR ROUTES (calendar_master.py or calendar_timeline_routes.py) =====
# When user creates event, suggest what documents to upload

@calendar_timeline_bp.route('/event/create', methods=['POST'])
def create_event():
    # ... existing event creation code ...
    # event saved to calendar
    
    event_type = request.form.get('event_type', 'general')
    event_data = {
        'event_id': event_id,
        'title': request.form.get('title'),
        'event_date': request.form.get('event_date'),
        'event_type': event_type
    }
    
    # NEW: Get document suggestions for this event
    bridge = CalendarVaultBridge()
    suggestions = bridge.suggest_documents_for_event(event_type, event_data)
    
    if suggestions:
        # Show user what to upload
        suggestion_text = ", ".join([s['doc_type'] for s in suggestions])
        flash(f"💡 Tip: Upload these documents: {suggestion_text}", 'info')
        
        # Optional: Store suggestions in session for upload page
        session['pending_suggestions'] = suggestions
    
    return redirect(url_for('calendar_timeline_bp.timeline'))


# ===== NEW ROUTE: Show events needing documents =====

@calendar_timeline_bp.route('/needs_documents')
def events_needing_documents():
    '''Dashboard showing which events are missing recommended documents'''
    user_id = request.args.get('user_token')
    
    bridge = CalendarVaultBridge()
    needs_docs = bridge.get_events_needing_documents(user_id)
    
    # Sort by urgency
    high_priority = [e for e in needs_docs if e['urgency'] == 'high']
    normal_priority = [e for e in needs_docs if e['urgency'] != 'high']
    
    return render_template('calendar/needs_documents.html',
                          high_priority=high_priority,
                          normal_priority=normal_priority)


# ===== BENEFITS OF PHASE 2 =====
'''
BEFORE Phase 2:
1. User uploads document → nothing happens
2. User creates event → no guidance on what to upload
3. User must remember which events need documents

AFTER Phase 2:
1. User uploads "repair_request.pdf" → Calendar auto-creates "Repair Issue" event
2. User creates "Notice Received" event → System suggests: "Upload notice document and envelope photo"
3. User sees dashboard: "3 events missing recommended documents (2 high priority)"

SPEED IMPROVEMENT:
- Manual: Upload doc (1 min) + Create event (1 min) + Link them (30 sec) = 2.5 min
- Auto: Upload doc (1 min) + Auto-event created + Auto-linked = 1 min
- Savings: 60% faster, 0% chance of forgetting to link

DATA FLOW:
Upload → Bridge detects type → Creates event → Links document → User sees complete timeline
Event → Bridge suggests docs → User uploads → Auto-links → Complete evidence chain
'''
