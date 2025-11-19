"""
INTEGRATED VAULT UPLOAD HANDLER - Example Code
Add this to vault_bp.py upload route after successful document save:
"""

# After document is saved to Dropbox/Google Drive and certificate created:

# 1. AUTO-CREATE TIMELINE EVENT (Phase 2)
try:
    from calendar_vault_bridge import create_event_from_upload
    
    doc_info = {
        'filename': filename,
        'doc_type': doc_type,  # 'eviction_notice', 'lease', 'repair_request', etc.
        'upload_date': datetime.now().isoformat(),
        'doc_id': doc_id,
        'certificate_hash': sha256_hash
    }
    
    event_result = create_event_from_upload(user_token, doc_info)
    if event_result:
        flash(f"✓ Timeline event created: {event_result['title']}", "success")
except Exception as e:
    print(f"[WARN] Could not create timeline event: {e}")

# 2. RECOMMEND LEARNING MODULES (Phase 3)
try:
    from vault_learning_bridge import get_learning_for_upload
    
    learning_recommendations = get_learning_for_upload(doc_type, filename)
    if learning_recommendations:
        # Store recommendations to show on success page
        session['learning_recommendations'] = learning_recommendations
except Exception as e:
    print(f"[WARN] Could not get learning recommendations: {e}")

# 3. UPDATE JOURNEY PROGRESS (Phase 5)
try:
    from journey_automation import check_and_advance
    
    journey_result = check_and_advance(user_token, 'upload')
    if journey_result.get('advanced'):
        flash(f"🎉 You advanced to {journey_result['new_stage']} stage!", "success")
except Exception as e:
    print(f"[WARN] Could not update journey: {e}")

# Return success with all integration results
return render_template('vault_success.html',
                     document=doc_info,
                     event_created=event_result,
                     learning_modules=learning_recommendations,
                     journey_update=journey_result,
                     user_token=user_token)
