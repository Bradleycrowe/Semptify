# Clean up duplicate function definitions in Semptify.py
import re

with open('Semptify.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find line where duplicates start - look for second 'def admin():'
lines = content.split('\n')
first_admin_found = False
cutoff_line = len(lines)

for i, line in enumerate(lines):
    if line.strip().startswith('def admin():'):
        if first_admin_found:
            # Found second admin(), cut here
            cutoff_line = i
            break
        first_admin_found = True

# Keep only lines up to cutoff
clean_lines = lines[:cutoff_line]

# Make sure file ends properly with if __name__ block
if 'if __name__' not in '\n'.join(clean_lines[-50:]):
    clean_lines.append('')
    clean_lines.append('if __name__ == \"__main__\":')
    clean_lines.append('    app.run(debug=True, port=5000)')

with open('Semptify.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(clean_lines))

print(f'Cleaned file: kept {cutoff_line} lines')
