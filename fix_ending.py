# Fix file structure - remove code after if __name__
with open('Semptify.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find if __name__ line and cut there
cutoff = len(lines)
for i, line in enumerate(lines):
    if "if __name__ == '__main__':" in line or 'if __name__ == "__main__":' in line:
        # Include the if block (2 more lines)
        cutoff = i + 2
        break

clean_lines = lines[:cutoff]

# Ensure proper ending
if clean_lines and not clean_lines[-1].endswith('\n'):
    clean_lines[-1] = clean_lines[-1] + '\n'

with open('Semptify.py', 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print(f'Fixed: kept {cutoff} lines')
