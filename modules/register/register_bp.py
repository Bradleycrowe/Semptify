from flask import Blueprint, render_template, request, current_app, url_for
import os
import json
import time
import hashlib
import secrets

from security import _get_or_create_csrf_token

register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Simple user registration that issues a one-time numeric token.

    Stores a sha256-hash of the token in `security/users.json` under `tokens`.
    Returns a success page showing the one-time token (display only).
    """
    if request.method == 'GET':
        csrf = _get_or_create_csrf_token()
        return render_template('register.html', csrf_token=csrf)

    # POST
    form_csrf = request.form.get('csrf_token') or request.headers.get('X-Csrf-Token')
    if not form_csrf or form_csrf != _get_or_create_csrf_token():
        return "CSRF token missing or invalid", 400

    # Collect full contact information
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    address = request.form.get('address', '').strip()
    city = request.form.get('city', '').strip()
    county = request.form.get('county', '').strip()
    state = request.form.get('state', '').strip()
    zip_code = request.form.get('zip_code', '').strip()
    phone = request.form.get('phone', '').strip()  # 10 digits
    email = request.form.get('email', '').strip()

    # Validation
    if not first_name or not last_name:
        return "First and last name are required", 400
    if not phone or len(phone.replace('-', '').replace(' ', '')) != 10:
        return "Valid 10-digit phone number required", 400
    if not email or '@' not in email:
        return "Valid email address required", 400

    # Create an 8-digit numeric token for user to copy (one-time)
    token = ''.join(secrets.choice('0123456789') for _ in range(8))
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    stored_hash = f"sha256:{token_hash}"

    # Path to security/users.json inside app root
    users_path = os.path.join(current_app.root_path, 'security', 'users.json')
    users = {'tokens': []}
    try:
        if os.path.exists(users_path):
            with open(users_path, 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f) or {'tokens': []}
                except Exception:
                    users = {'tokens': []}
        else:
            # Ensure security folder exists
            os.makedirs(os.path.dirname(users_path), exist_ok=True)

        user_id = secrets.token_hex(8)
        entry = {
            'id': user_id,
            'hash': stored_hash,
            'ts': int(time.time()),
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'city': city,
            'county': county,
            'state': state,
            'zip_code': zip_code,
            'phone': phone,
            'email': email,
            'note': 'one-time registration token'
        }

        tokens = users.get('tokens') or []
        tokens.insert(0, entry)
        users['tokens'] = tokens

        with open(users_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)

        # 🤖 VEEPER: Backup token for recovery
        try:
            from veeper import backup_user_token
            backup_user_token(user_id, token, phone, email)
            current_app.logger.info(f"✅ Veeper backup created for user {user_id}")
        except Exception as e:
            current_app.logger.warning(f"⚠️ Veeper backup failed: {e}")
            # Don't fail registration if backup fails

    except Exception as e:
        current_app.logger.exception('Failed to save registration token')
        return "Internal server error", 500

    # Return a page showing the token (one-time), with a link to the vault including token
    vault_link = f"/vault?user_token={token}"
    return render_template('register_success.html', token=token, vault_link=vault_link)
