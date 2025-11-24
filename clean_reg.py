# Remove problematic blueprint registrations from Semptify.py
lines = open("Semptify.py", "r", encoding="utf-8").readlines()
new_lines = []

# Skip these problematic entries
skip_patterns = [
    "attorney_finder_routes",  # We have routes/attorney_finder
    "register_new",  # We use register.py
    "rent_calculator.*rent_calculator_alt",  # Duplicate
    "vault_bp",  # We use vault.py's vault_blueprint
    "storage_setup_routes_OLD",
    "_backup_storage_setup",
]

for line in lines:
    skip = False
    for pattern in skip_patterns:
        if pattern in line and ("'" in line or '"' in line):
            skip = True
            break
    if not skip:
        new_lines.append(line)

open("Semptify.py", "w", encoding="utf-8").writelines(new_lines)
print("✓ Removed duplicate blueprint registrations from Semptify.py")
