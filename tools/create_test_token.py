#!/usr/bin/env python3
"""Create a test user token and print JSON with user_id and token.

Usage:
    python tools/create_test_token.py
"""
from security import save_user_token
import json

if __name__ == '__main__':
    t = save_user_token()
    print(json.dumps(t))
