"""
Smart Inbox - Auto-capture emails, texts, and voicemails related to rental issues.
Uses keyword matching and user preferences to suggest items for the vault.
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
import hashlib
ary up to da
    
    return min(score, 100)


def scan_messages(messages: List[Dict[str, Any]], threshold: int = 30) -> List[Dict[str, Any]]:
    """
    Scan messages and return those above relevance threshold.
    
    Args:
        messages: List of dicts with 'subject', 'body', 'sender', 'date', 'type'
        threshold: Minimum score (0-100) to include
    
    Returns:
        List of messages with scores, sorted by relevance
    """
    scored = []
    for msg in messages:
        score = score_message(
            msg.get('subject', ''),
            msg.get('body', ''),
            msg.get('sender', '')
        )
        if score >= threshold:
            msg['relevance_score'] = score
            msg['suggested'] = True
            scored.append(msg)
    
    return sorted(scored, key=lambda m: m['relevance_score'], reverse=True)


def save_to_inbox(user_id: str, message: Dict[str, Any], data_dir: str = 'data') -> str:
    """Save a captured message to user's smart inbox."""
    inbox_dir = os.path.join(data_dir, 'smart_inbox', user_id)
    os.makedirs(inbox_dir, exist_ok=True)
    
    msg_id = hashlib.sha256(
        f"{message.get('date')}{message.get('sender')}{message.get('subject')}".encode()
    ).hexdigest()[:12]
    
    message['message_id'] = msg_id
    message['captured_at'] = datetime.now().isoformat()
    message['status'] = 'pending'  # pending, saved, dismissed
    
    filepath = os.path.join(inbox_dir, f"{msg_id}.json")
    with open(filepath, 'w') as f:
        json.dump(message, f, indent=2)
    
    return msg_id


def get_inbox_messages(user_id: str, status: str = None, data_dir: str = 'data') -> List[Dict[str, Any]]:
    """Get all messages from user's smart inbox."""
    inbox_dir = os.path.join(data_dir, 'smart_inbox', user_id)
    if not os.path.exists(inbox_dir):
        return []
    
    messages = []
    for filename in os.listdir(inbox_dir):
        if filename.endswith('.json'):
            with open(os.path.join(inbox_dir, filename), 'r') as f:
                msg = json.load(f)
                if status is None or msg.get('status') == status:
                    messages.append(msg)
    
    return sorted(messages, key=lambda m: m.get('captured_at', ''), reverse=True)


def update_message_status(user_id: str, message_id: str, status: str, data_dir: str = 'data') -> bool:
    """Update the status of a message (saved to vault, dismissed, etc.)."""
    inbox_dir = os.path.join(data_dir, 'smart_inbox', user_id)
    filepath = os.path.join(inbox_dir, f"{message_id}.json")
    
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r') as f:
        message = json.load(f)
    
    message['status'] = status
    message['updated_at'] = datetime.now().isoformat()
    
    with open(filepath, 'w') as f:
        json.dump(message, f, indent=2)
    
    return True


# Demo/test function
if __name__ == "__main__":
    test_messages = [
        {
            "subject": "Rent Payment Confirmation",
            "body": "Your rent payment of $1200 has been received for Unit 4B.",
            "sender": "landlord@property.com",
            "date": "2025-11-10",
            "type": "email"
        },
        {
            "subject": "Weekend Plans",
            "body": "Hey, want to grab dinner this weekend?",
            "sender": "friend@example.com",
            "date": "2025-11-11",
            "type": "email"
        },
        {
            "subject": "EVICTION NOTICE",
            "body": "You are hereby notified that your tenancy will be terminated...",
            "sender": "property_mgmt@landlord.com",
            "date": "2025-11-09",
            "type": "email"
        },
        {
            "subject": "Maintenance Request Follow-up",
            "body": "Regarding your repair request for the leaking faucet in your apartment...",
            "sender": "maintenance@property.com",
            "date": "2025-11-08",
            "type": "email"
        }
    ]
    
    print("Smart Inbox - Message Scanner\n")
    relevant = scan_messages(test_messages, threshold=30)
    
    print(f"Found {len(relevant)} relevant messages:\n")
    for msg in relevant:
        print(f"Score: {msg['relevance_score']} | {msg['subject']}")
        print(f"  From: {msg['sender']}")
        print(f"  Date: {msg['date']}")
        print()
