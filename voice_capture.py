"""
Voice Capture Manager - Record audio, save to vault, log calls.
Uses simple file storage; can be upgraded with speech-to-text transcription.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List
import hashlib


def save_voice_memo(user_id: str, audio_data: bytes, filename: str, 
                    metadata: Dict[str, Any], data_dir: str = 'data') -> Dict[str, Any]:
    """
    Save voice memo with metadata.
    
    Args:
        user_id: Anonymous user ID
        audio_data: Raw audio bytes
        filename: Original filename
        metadata: Additional metadata (title, notes, tags, etc.)
        data_dir: Base data directory
    
    Returns:
        Dict with memo_id, file_path, metadata_path
    """
    # Generate memo ID
    memo_id = hashlib.sha256(
        f"{user_id}{filename}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    
    # Create user voice directory
    voice_dir = os.path.join(data_dir, 'voice', user_id)
    os.makedirs(voice_dir, exist_ok=True)
    
    # Save audio file
    file_ext = os.path.splitext(filename)[1] or '.webm'
    audio_path = os.path.join(voice_dir, f"{memo_id}{file_ext}")
    with open(audio_path, 'wb') as f:
        f.write(audio_data)
    
    # Save metadata
    full_metadata = {
        'memo_id': memo_id,
        'user_id': user_id,
        'filename': filename,
        'file_path': audio_path,
        'recorded_at': datetime.now().isoformat(),
        'duration_seconds': metadata.get('duration_seconds'),
        'title': metadata.get('title', 'Untitled Memo'),
        'notes': metadata.get('notes', ''),
        'tags': metadata.get('tags', []),
        'location': metadata.get('location', ''),
        'related_documents': metadata.get('related_documents', []),
        'file_size': len(audio_data)
    }
    
    metadata_path = os.path.join(voice_dir, f"{memo_id}_metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(full_metadata, f, indent=2)
    
    return {
        'memo_id': memo_id,
        'file_path': audio_path,
        'metadata_path': metadata_path,
        'metadata': full_metadata
    }


def log_call(user_id: str, call_metadata: Dict[str, Any], data_dir: str = 'data') -> Dict[str, Any]:
    """
    Log a phone call with details.
    
    Args:
        user_id: Anonymous user ID
        call_metadata: Dict with phone_number, direction (incoming/outgoing), 
                      duration, timestamp, notes, recording_path (optional)
        data_dir: Base data directory
    
    Returns:
        Dict with call_id and saved metadata
    """
    call_id = hashlib.sha256(
        f"{user_id}{call_metadata.get('phone_number')}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    
    call_log_dir = os.path.join(data_dir, 'call_logs', user_id)
    os.makedirs(call_log_dir, exist_ok=True)
    
    full_metadata = {
        'call_id': call_id,
        'user_id': user_id,
        'phone_number': call_metadata.get('phone_number', 'Unknown'),
        'direction': call_metadata.get('direction', 'outgoing'),  # incoming/outgoing
        'duration_seconds': call_metadata.get('duration_seconds'),
        'timestamp': call_metadata.get('timestamp', datetime.now().isoformat()),
        'notes': call_metadata.get('notes', ''),
        'tags': call_metadata.get('tags', []),
        'recording_path': call_metadata.get('recording_path'),
        'outcome': call_metadata.get('outcome', ''),  # resolved, escalated, etc.
        'logged_at': datetime.now().isoformat()
    }
    
    log_path = os.path.join(call_log_dir, f"{call_id}.json")
    with open(log_path, 'w') as f:
        json.dump(full_metadata, f, indent=2)
    
    return {
        'call_id': call_id,
        'log_path': log_path,
        'metadata': full_metadata
    }


def get_voice_memos(user_id: str, data_dir: str = 'data', 
                    tag_filter: str = None) -> List[Dict[str, Any]]:
    """Retrieve all voice memos for a user, optionally filtered by tag."""
    voice_dir = os.path.join(data_dir, 'voice', user_id)
    if not os.path.exists(voice_dir):
        return []
    
    memos = []
    for filename in os.listdir(voice_dir):
        if filename.endswith('_metadata.json'):
            with open(os.path.join(voice_dir, filename), 'r') as f:
                metadata = json.load(f)
            
            if tag_filter:
                if tag_filter.lower() in [t.lower() for t in metadata.get('tags', [])]:
                    memos.append(metadata)
            else:
                memos.append(metadata)
    
    # Sort by recorded_at descending
    memos.sort(key=lambda x: x.get('recorded_at', ''), reverse=True)
    return memos


def get_call_logs(user_id: str, data_dir: str = 'data', 
                  direction_filter: str = None) -> List[Dict[str, Any]]:
    """Retrieve call logs for a user, optionally filtered by direction."""
    call_log_dir = os.path.join(data_dir, 'call_logs', user_id)
    if not os.path.exists(call_log_dir):
        return []
    
    logs = []
    for filename in os.listdir(call_log_dir):
        if filename.endswith('.json'):
            with open(os.path.join(call_log_dir, filename), 'r') as f:
                metadata = json.load(f)
            
            if direction_filter:
                if metadata.get('direction') == direction_filter:
                    logs.append(metadata)
            else:
                logs.append(metadata)
    
    # Sort by timestamp descending
    logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return logs


def search_voice_memos(user_id: str, query: str, data_dir: str = 'data') -> List[Dict[str, Any]]:
    """Search voice memos by title, notes, or tags."""
    memos = get_voice_memos(user_id, data_dir)
    query_lower = query.lower()
    
    results = []
    for memo in memos:
        if (query_lower in memo.get('title', '').lower() or
            query_lower in memo.get('notes', '').lower() or
            any(query_lower in tag.lower() for tag in memo.get('tags', []))):
            results.append(memo)
    
    return results


# Demo/test
if __name__ == "__main__":
    print("Voice Capture Manager - Demo\n")
    
    # Simulate voice memo
    test_user_id = 'user123'
    test_audio = b'fake audio data for demo'
    
    memo_result = save_voice_memo(
        user_id=test_user_id,
        audio_data=test_audio,
        filename='landlord_call.webm',
        metadata={
            'title': 'Landlord Call About Repairs',
            'notes': 'Called landlord about broken heater. He said he would send someone next week.',
            'tags': ['repair', 'heater', 'landlord'],
            'duration_seconds': 180
        }
    )
    print(f"Voice Memo Saved: {memo_result['memo_id']}")
    print(f"File Path: {memo_result['file_path']}")
    print(f"Metadata: {memo_result['metadata']}\n")
    
    # Simulate call log
    call_result = log_call(
        user_id=test_user_id,
        call_metadata={
            'phone_number': '555-1234',
            'direction': 'outgoing',
            'duration_seconds': 180,
            'notes': 'Discussed repair timeline',
            'tags': ['landlord', 'repair'],
            'outcome': 'scheduled'
        }
    )
    print(f"Call Logged: {call_result['call_id']}")
    print(f"Log Path: {call_result['log_path']}")
    print(f"Metadata: {call_result['metadata']}\n")
    
    # Retrieve memos
    memos = get_voice_memos(test_user_id, tag_filter='repair')
    print(f"Found {len(memos)} memos with 'repair' tag")
    
    # Retrieve call logs
    logs = get_call_logs(test_user_id, direction_filter='outgoing')
    print(f"Found {len(logs)} outgoing calls")
