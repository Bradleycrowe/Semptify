"""
Veeper - Local-Only AI for Token Recovery
Verifies user identity via phone/email and recovers lost tokens
NO cloud services, all verification happens locally
"""
import os
import json
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

CWD = os.getcwd()
VEEPER_DIR = os.path.join(CWD, "security", "veeper")
BACKUP_FILE = os.path.join(VEEPER_DIR, "token_backups.enc")
RECOVERY_LOG = os.path.join(VEEPER_DIR, "recovery_log.json")

# Veeper's master key (derived from system entropy + installation)
VEEPER_KEY_FILE = os.path.join(VEEPER_DIR, "veeper.key")


def _ensure_veeper_dirs():
    """Ensure Veeper directories exist"""
    os.makedirs(VEEPER_DIR, exist_ok=True)


def _get_veeper_master_key() -> bytes:
    """Get or create Veeper's master encryption key (local only)"""
    _ensure_veeper_dirs()

    if os.path.exists(VEEPER_KEY_FILE):
        with open(VEEPER_KEY_FILE, 'rb') as f:
            return f.read()

    # Generate new master key (first time setup)
    master_key = secrets.token_bytes(32)  # 256 bits
    with open(VEEPER_KEY_FILE, 'wb') as f:
        f.write(master_key)

    # Secure the key file (permissions)
    try:
        os.chmod(VEEPER_KEY_FILE, 0o600)  # Read/write owner only
    except:
        pass

    return master_key


def _encrypt_with_veeper(data: bytes) -> tuple[bytes, bytes]:
    """Encrypt data with Veeper's master key"""
    master_key = _get_veeper_master_key()
    nonce = secrets.token_bytes(12)

    cipher = Cipher(
        algorithms.AES(master_key),
        modes.GCM(nonce),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag

    return encrypted + tag, nonce


def _decrypt_with_veeper(encrypted_data: bytes, nonce: bytes) -> bytes:
    """Decrypt data with Veeper's master key"""
    master_key = _get_veeper_master_key()

    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[:-16]

    cipher = Cipher(
        algorithms.AES(master_key),
        modes.GCM(nonce, tag),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def backup_user_token(user_id: str, user_token: str, phone: str, email: str):
    """
    Backup user token encrypted by Veeper (called during registration)

    Args:
        user_id: User's internal ID
        user_token: User's 12-digit token
        phone: User's phone number (for verification)
        email: User's email (for verification)
    """
    _ensure_veeper_dirs()

    # Load existing backups
    backups = {}
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, 'rb') as f:
                encrypted = f.read()
            if encrypted:
                # Decrypt existing backups
                nonce = encrypted[:12]
                data = encrypted[12:]
                decrypted = _decrypt_with_veeper(data, nonce)
                backups = json.loads(decrypted.decode('utf-8'))
        except:
            backups = {}

    # Add new backup
    backups[user_id] = {
        'token': user_token,
        'phone': phone,
        'email': email,
        'backed_up': datetime.utcnow().isoformat() + 'Z',
    }

    # Encrypt and save all backups
    backup_json = json.dumps(backups).encode('utf-8')
    encrypted, nonce = _encrypt_with_veeper(backup_json)

    with open(BACKUP_FILE, 'wb') as f:
        f.write(nonce + encrypted)

    print(f"✅ Veeper: Token backup created for user {user_id}")


def initiate_recovery(phone_or_email: str) -> dict:
    """
    Initiate token recovery process

    Args:
        phone_or_email: User's phone number or email

    Returns:
        {
            'recovery_id': str,
            'method': 'phone' or 'email',
            'masked_contact': str (e.g., "***-***-4567"),
            'expires': str (timestamp)
        }
    """
    _ensure_veeper_dirs()

    # Load backups
    if not os.path.exists(BACKUP_FILE):
        return {'error': 'No backups found'}

    try:
        with open(BACKUP_FILE, 'rb') as f:
            encrypted = f.read()
        nonce = encrypted[:12]
        data = encrypted[12:]
        decrypted = _decrypt_with_veeper(data, nonce)
        backups = json.loads(decrypted.decode('utf-8'))
    except:
        return {'error': 'Cannot read backups'}

    # Find user by phone or email
    user_id = None
    user_data = None
    for uid, data in backups.items():
        if data['phone'] == phone_or_email or data['email'] == phone_or_email:
            user_id = uid
            user_data = data
            break

    if not user_id:
        return {'error': 'User not found'}

    # Generate recovery ID and verification code
    recovery_id = secrets.token_hex(16)
    verification_code = secrets.token_urlsafe(32)

    # Determine method (phone or email)
    method = 'phone' if data['phone'] == phone_or_email else 'email'

    # Store recovery request
    recovery_requests = {}
    if os.path.exists(RECOVERY_LOG):
        with open(RECOVERY_LOG, 'r', encoding='utf-8') as f:
            recovery_requests = json.load(f)

    recovery_requests[recovery_id] = {
        'user_id': user_id,
        'method': method,
        'contact': phone_or_email,
        'verification_code': hashlib.sha256(verification_code.encode()).hexdigest(),
        'initiated': datetime.utcnow().isoformat() + 'Z',
        'expires': (datetime.utcnow() + timedelta(hours=1)).isoformat() + 'Z',
        'verified': False
    }

    with open(RECOVERY_LOG, 'w', encoding='utf-8') as f:
        json.dump(recovery_requests, f, indent=2)

    # Mask contact info for display
    if method == 'phone':
        masked = f"***-***-{phone_or_email[-4:]}"
    else:
        parts = phone_or_email.split('@')
        masked = f"{parts[0][:2]}***@{parts[1]}"

    print(f"🔐 Veeper: Recovery initiated for {masked}")
    print(f"   Verification code: {verification_code}")
    print(f"   (In production, this would be sent via {method})")

    return {
        'recovery_id': recovery_id,
        'method': method,
        'masked_contact': masked,
        'expires': recovery_requests[recovery_id]['expires'],
        'verification_code': verification_code  # Remove in production!
    }


def verify_and_recover(recovery_id: str, verification_code: str) -> dict:
    """
    Verify user identity and recover token

    Args:
        recovery_id: Recovery session ID
        verification_code: Code sent via phone/email

    Returns:
        {
            'token': str (recovered token),
            'user_id': str
        } or {'error': str}
    """
    # 🚨 DEV MODE BYPASS: Check for emergency breakglass code
    dev_mode = os.getenv('VEEPER_DEV_MODE', 'false').lower() == 'true'
    emergency_code = os.getenv('VEEPER_EMERGENCY_CODE', 'BREAKGLASS')

    if dev_mode and verification_code == emergency_code:
        print("⚠️ VEEPER DEV MODE: Emergency bypass activated!")
        # Return ALL user tokens (for debugging)
        if not os.path.exists(BACKUP_FILE):
            return {'error': 'No backups found'}

        try:
            with open(BACKUP_FILE, 'rb') as f:
                encrypted = f.read()
            nonce = encrypted[:12]
            data = encrypted[12:]
            decrypted = _decrypt_with_veeper(data, nonce)
            backups = json.loads(decrypted.decode('utf-8'))

            # Return list of all users and tokens (dev only!)
            users = []
            for uid, user_data in backups.items():
                users.append({
                    'user_id': uid,
                    'token': user_data['token'],
                    'phone': user_data.get('phone', 'N/A'),
                    'email': user_data.get('email', 'N/A')
                })

            print(f"🔓 Emergency access: {len(users)} tokens retrieved")
            return {'emergency_access': True, 'users': users}
        except Exception as e:
            return {'error': f'Emergency access failed: {e}'}

    # Normal verification flow
    if not os.path.exists(RECOVERY_LOG):
        return {'error': 'No recovery requests found'}

    with open(RECOVERY_LOG, 'r', encoding='utf-8') as f:
        recovery_requests = json.load(f)

    if recovery_id not in recovery_requests:
        return {'error': 'Invalid recovery ID'}

    request = recovery_requests[recovery_id]

    # Check expiration
    expires = datetime.fromisoformat(request['expires'].replace('Z', '+00:00'))
    if datetime.now(expires.tzinfo) > expires:
        return {'error': 'Recovery session expired'}

    # Check if already verified
    if request.get('verified'):
        return {'error': 'Recovery already completed'}

    # Verify code
    code_hash = hashlib.sha256(verification_code.encode()).hexdigest()
    if code_hash != request['verification_code']:
        return {'error': 'Invalid verification code'}

    # Mark as verified
    request['verified'] = True
    request['verified_at'] = datetime.utcnow().isoformat() + 'Z'

    with open(RECOVERY_LOG, 'w', encoding='utf-8') as f:
        json.dump(recovery_requests, f, indent=2)

    # Decrypt backups and retrieve token
    with open(BACKUP_FILE, 'rb') as f:
        encrypted = f.read()
    nonce = encrypted[:12]
    data = encrypted[12:]
    decrypted = _decrypt_with_veeper(data, nonce)
    backups = json.loads(decrypted.decode('utf-8'))

    user_id = request['user_id']
    if user_id not in backups:
        return {'error': 'Backup not found'}

    token = backups[user_id]['token']

    print(f"✅ Veeper: Token recovered for user {user_id}")

    return {
        'token': token,
        'user_id': user_id,
        'recovered_at': request['verified_at']
    }


def list_recovery_attempts(user_id: str = None) -> list:
    """
    List recovery attempts (admin function)

    Args:
        user_id: Optional - filter by user ID

    Returns:
        List of recovery attempts
    """
    if not os.path.exists(RECOVERY_LOG):
        return []

    with open(RECOVERY_LOG, 'r', encoding='utf-8') as f:
        recovery_requests = json.load(f)

    attempts = []
    for recovery_id, request in recovery_requests.items():
        if user_id and request['user_id'] != user_id:
            continue

        attempts.append({
            'recovery_id': recovery_id,
            'user_id': request['user_id'],
            'method': request['method'],
            'initiated': request['initiated'],
            'verified': request.get('verified', False),
            'verified_at': request.get('verified_at')
        })

    return attempts


# Flask routes for Veeper
from flask import Blueprint, request, jsonify

veeper_bp = Blueprint('veeper', __name__, url_prefix='/veeper')


@veeper_bp.route('/recover/initiate', methods=['POST'])
def api_initiate_recovery():
    """Initiate token recovery (public endpoint)"""
    data = request.get_json(force=True, silent=True) or {}

    contact = data.get('phone') or data.get('email')
    if not contact:
        return jsonify({'error': 'phone or email required'}), 400

    result = initiate_recovery(contact)

    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result), 200


@veeper_bp.route('/recover/verify', methods=['POST'])
def api_verify_recovery():
    """Verify and complete token recovery"""
    data = request.get_json(force=True, silent=True) or {}

    recovery_id = data.get('recovery_id')
    verification_code = data.get('verification_code')

    if not recovery_id or not verification_code:
        return jsonify({'error': 'recovery_id and verification_code required'}), 400

    result = verify_and_recover(recovery_id, verification_code)

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result), 200


@veeper_bp.route('/recovery/log', methods=['GET'])
def api_recovery_log():
    """List recovery attempts (admin only)"""
    from security import validate_admin_token

    token = request.headers.get('X-Admin-Token') or request.args.get('admin_token')
    if not validate_admin_token(token):
        return jsonify({'error': 'unauthorized'}), 401

    user_id = request.args.get('user_id')
    attempts = list_recovery_attempts(user_id)

    return jsonify({'attempts': attempts}), 200


@veeper_bp.route('/emergency/list-all', methods=['POST'])
def api_emergency_list_all():
    """🚨 EMERGENCY: List all backed-up tokens (DEV MODE ONLY)

    Use when locked out during development. Requires:
    1. VEEPER_DEV_MODE=true environment variable
    2. VEEPER_EMERGENCY_CODE in request body

    Returns all user tokens for recovery.
    """
    dev_mode = os.getenv('VEEPER_DEV_MODE', 'false').lower() == 'true'

    if not dev_mode:
        return jsonify({'error': 'Emergency endpoint disabled (not in dev mode)'}), 403

    data = request.get_json(force=True, silent=True) or {}
    emergency_code = data.get('emergency_code')
    expected_code = os.getenv('VEEPER_EMERGENCY_CODE', 'BREAKGLASS')

    if emergency_code != expected_code:
        return jsonify({'error': 'Invalid emergency code'}), 401

    # Use the emergency bypass in verify_and_recover
    result = verify_and_recover('emergency', emergency_code)

    if 'emergency_access' in result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Emergency access failed'}), 500
