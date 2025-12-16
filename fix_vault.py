import re

with open('vault.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the vault() function and fix the auth logic
in_vault_func = False
fixed = False
new_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    
    if 'def vault():' in line:
        in_vault_func = True
    
    if in_vault_func and 'if not uid:' in line and not fixed:
        # Check if next line has default_user
        if i+1 < len(lines) and 'default_user' in lines[i+1]:
            # Replace with 401 return
            new_lines.append('    if not uid:\n')
            new_lines.append('        return jsonify({\"error\": \"unauthorized\", \"message\": \"Valid user token required\"}), 401\n')
            # Skip the next 3 lines (uid = default_user, if not uid, uid = default_user)
            skip_next = 3
            fixed = True
            in_vault_func = False
            continue
    
    new_lines.append(line)

with open('vault.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Fixed vault auth' if fixed else 'No changes made')
