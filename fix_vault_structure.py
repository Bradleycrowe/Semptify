import re

# Read vault.py
with open('vault.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where _cert_path function starts
cert_path_start = content.find('def _cert_path(user_id, filename):')
if cert_path_start == -1:
    print("ERROR: _cert_path function not found")
    exit(1)

# Find the nested Blueprint definition inside _cert_path
nested_bp_match = re.search(r'(\s+)from flask import Blueprint.*?vault_bp = Blueprint\(', content[cert_path_start:], re.DOTALL)
if not nested_bp_match:
    print("ERROR: Nested Blueprint not found")
    exit(1)

# Calculate actual position in file
nested_start = cert_path_start + nested_bp_match.start()

# Find end of _cert_path (next function at same indentation level or end of nested code)
# Look for next 'def ' at column 0 after the nested Blueprint
search_from = nested_start + 200
next_func_match = re.search(r'\n(def |class |if __name__|$)', content[search_from:])
if next_func_match:
    nested_end = search_from + next_func_match.start()
else:
    nested_end = len(content)

# Extract the nested code block
nested_code = content[nested_start:nested_end]

# Remove the extra indentation (should be 4 spaces)
lines = nested_code.split('\n')
fixed_lines = []
for line in lines:
    if line.startswith('    ') and len(line) > 4:
        fixed_lines.append(line[4:])  # Remove 4 spaces
    elif line.strip() == '':
        fixed_lines.append('')
    else:
        fixed_lines.append(line)

fixed_nested_code = '\n'.join(fixed_lines)

# Build new file: everything before _cert_path + fixed nested code + everything after
before_cert_path = content[:cert_path_start]

# Make _cert_path a simple function
simple_cert_path = '''def _cert_path(user_id, filename):
    user_dir = os.path.join(UPLOAD_ROOT, user_id)
    return os.path.join(user_dir, filename)

'''

after_nested = content[nested_end:] if nested_end < len(content) else ''

# Combine
new_content = before_cert_path + simple_cert_path + fixed_nested_code + after_nested

# Write back
with open('vault.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ Fixed vault.py structure - extracted routes to module level")
print(f"  - Removed nested Blueprint from inside _cert_path (was at char {nested_start})")
print(f"  - Simplified _cert_path to 3-line helper function")
print(f"  - Moved {len(fixed_lines)} lines of route code to module level")
