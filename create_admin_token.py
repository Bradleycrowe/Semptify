#!/usr/bin/env python3
"""Generate a new admin token"""

import sys
import os
import secrets

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from security import save_admin_token

try:
    # Generate a new secure token
    token = secrets.token_urlsafe(16)

    # Save it
    save_admin_token(token, breakglass=False)

    print()
    print("=" * 60)
    print("✅ ADMIN TOKEN GENERATED")
    print("=" * 60)
    print(f"Admin Token: {token}")
    print("=" * 60)
    print()
    print("📋 USE THIS TOKEN:")
    print(f"   URL: http://localhost:5000/admin?token={token}")
    print(f"   Header: X-Admin-Token: {token}")
    print(f"   Query Param: ?admin_token={token}")
    print()
    print("💾 Stored in: security/admin_tokens.json")
    print()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
