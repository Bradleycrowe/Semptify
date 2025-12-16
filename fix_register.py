# Fix register.py to handle dict users format
with open('register.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def _load_users():
    """Load users from security/users.json"""
    users_path = os.path.join(SECURITY_DIR, 'users.json')
    if os.path.exists(users_path):
        try:
            with open(users_path, 'r') as f:
                return json.load(f)
        except:
            return []
    return []'''

new = '''def _load_users():
    """Load users from security/users.json"""
    users_path = os.path.join(SECURITY_DIR, 'users.json')
    if os.path.exists(users_path):
        try:
            with open(users_path, 'r') as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return list(data.values()) if data else []
                return []
        except:
            return []
    return []'''

content = content.replace(old, new)

with open('register.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed')
