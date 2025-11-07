import os
from waitress import serve
from Semptify import app
from datetime import datetime, timedelta
import hashlib
import secrets

# Token Configuration
TOKEN_EXPIRY_HOURS = 24
ADMIN_TOKEN_EXPIRY = None  # Admin tokens never expire

# Generate a secure token
def generate_token():
    return secrets.token_hex(16)  # 32-character hex token

# Hash a token for secure storage
def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

# Check if a token is expired
def is_token_expired(token_creation_time, is_admin=False):
    if is_admin:
        return False  # Admin tokens never expire
    expiry_time = token_creation_time + timedelta(hours=TOKEN_EXPIRY_HOURS)
    return datetime.now() > expiry_time

# Break-glass procedure for admin tokens
def break_glass_procedure():
    print("Break-glass procedure initiated. Admin must manually reset tokens.")
    # Additional logging or notification logic can be added here

# Example usage
def main():
    user_token = generate_token()
    admin_token = generate_token()

    print("User Token:", user_token)
    print("Admin Token:", admin_token)

    hashed_user_token = hash_token(user_token)
    hashed_admin_token = hash_token(admin_token)

    print("Hashed User Token:", hashed_user_token)
    print("Hashed Admin Token:", hashed_admin_token)

    # Simulate token creation time
    token_creation_time = datetime.now()

    print("Is User Token Expired?", is_token_expired(token_creation_time))
    print("Is Admin Token Expired?", is_token_expired(token_creation_time, is_admin=True))

if __name__ == '__main__':
    # Read host/port from environment with sane defaults
    # Accept both custom SEMPTIFY_PORT and platform-provided PORT (Render/Heroku style)
    host = os.environ.get('SEMPTIFY_HOST', '0.0.0.0')
    port = int(os.environ.get('SEMPTIFY_PORT') or os.environ.get('PORT', '8080'))

    # Ensure runtime folders exist (app already does this on import but keep-safe)
    folders = ["uploads", "logs", "copilot_sync", "final_notices", "security"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    threads = int(os.environ.get('SEMPTIFY_THREADS', '8'))
    backlog = int(os.environ.get('SEMPTIFY_BACKLOG', '1024'))
    print(f"Starting Semptify (production) on {host}:{port} threads={threads} backlog={backlog} (PORT env fallback supported)")
    serve(app, host=host, port=port, threads=threads, backlog=backlog)

