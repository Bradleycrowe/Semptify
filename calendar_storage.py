from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import json, os, base64
from datetime import datetime
from doc_id_generator import generate_doc_id, verify_doc_certificate

class EncryptedCalendarStorage:
    def __init__(self, cloud_client, user_token):
        self.cloud_client = cloud_client
        self.user_token = user_token
        self.encryption_key = None
        self.calendar_file = '.semptify/calendar.enc'
    
    def _derive_encryption_key(self):
        if self.encryption_key:
            return self.encryption_key
        salt = os.urandom(32)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        self.encryption_key = kdf.derive(self.user_token.encode())
        return self.encryption_key
    
    def encrypt_data(self, data_dict):
        key = self._derive_encryption_key()
        json_data = json.dumps(data_dict, sort_keys=True)
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(json_data.encode()) + encryptor.finalize()
        encrypted = nonce + encryptor.tag + ciphertext
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_b64):
        key = self._derive_encryption_key()
        encrypted = base64.b64decode(encrypted_b64)
        nonce, tag, ciphertext = encrypted[:12], encrypted[12:28], encrypted[28:]
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return json.loads(plaintext.decode())
    
    def load_calendar(self):
        try:
            encrypted = self.cloud_client.download(self.calendar_file)
            return self.decrypt_data(encrypted)
        except:
            return {"version": "1.0", "created_at": datetime.utcnow().isoformat() + "Z", "events": []}
    
    def save_calendar(self, calendar_data):
        encrypted = self.encrypt_data(calendar_data)
        self.cloud_client.upload(self.calendar_file, encrypted)
    
    def add_event(self, item_type, content_data, direction="outgoing"):
        calendar = self.load_calendar()
        previous_sha = calendar["events"][-1].get("certificate", {}).get("sha256") if calendar["events"] else None
        doc_info = generate_doc_id(self.user_token, item_type, content_data, previous_sha)
        event = {
            "doc_id": doc_info["doc_id"],
            "timestamp": doc_info["timestamp"],
            "direction": direction,
            "type": doc_info["type"],
            "type_name": doc_info["type_name"],
            "content": content_data,
            "certificate": doc_info["certificate"]
        }
        calendar["events"].append(event)
        calendar["last_modified"] = datetime.utcnow().isoformat() + "Z"
        self.save_calendar(calendar)
        return doc_info["doc_id"]
    
    def get_events(self, start_date=None, end_date=None, item_type=None):
        calendar = self.load_calendar()
        events = calendar["events"]
        if item_type:
            events = [e for e in events if e["type"] == item_type]
        events.sort(key=lambda e: e["timestamp"])
        return events
    
    def verify_event(self, doc_id):
        calendar = self.load_calendar()
        event = next((e for e in calendar["events"] if e["doc_id"] == doc_id), None)
        if not event:
            return {"valid": False, "error": "Event not found"}
        return verify_doc_certificate(doc_id, event["content"], event["certificate"])
