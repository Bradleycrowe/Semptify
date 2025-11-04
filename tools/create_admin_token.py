#!/usr/bin/env python3
"""Create a test admin token and print JSON with admin_id and token.

Usage:
    python tools/create_admin_token.py
"""
from security import save_admin_token
import json

if __name__ == '__main__':
    t = save_admin_token(breakglass=True)
    print(json.dumps(t))
