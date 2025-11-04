#!/usr/bin/env python
"""Generate a new admin token"""

from security import save_admin_token

import secrets

try:
    token = secrets.token_hex(32)
    save_admin_token(token)
    print(f"\n✅ NEW ADMIN TOKEN CREATED")
    print(f"{'='*50}")
    print(f"Admin Token: {token}")
    print(f"{'='*50}")
    print(f"\n📋 How to use:")
    print(f"  - URL: http://localhost:5000/admin?token={token}")
    print(f"  - Header: X-Admin-Token: {token}")
    print(f"  - Save this token somewhere safe!")
    print(f"\n✅ Token saved to: security/admin_tokens.json")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
