# Add _build_evidence_prompt function
function_code = '''

def _build_evidence_prompt(prompt: str, location: str, timestamp: str, form_type: str, form_data: dict) -> str:
    """Build an AI prompt for evidence collection guidance."""
    parts = [
        "You are a helpful assistant for tenant rights and evidence collection.",
        f"User request: {prompt}",
    ]
    
    if location:
        parts.append(f"Location: {location}")
    
    if timestamp:
        parts.append(f"Timestamp: {timestamp}")
    
    if form_type:
        form_type_readable = form_type.replace("_", " ").title()
        parts.append(f"Form type: {form_type_readable}")
    
    if form_data:
        parts.append(f"Form data provided: {', '.join(form_data.keys())}")
        for key, value in form_data.items():
            if value and len(str(value)) < 100:
                parts.append(f"  - {key}: {value}")
    
    parts.append("What evidence to collect and how to document it properly?")
    
    return "\\n".join(parts)

'''

lines = open("Semptify.py", "r", encoding="utf-8").readlines()

# Find a good place to insert - after imports, before routes
# Look for "app = Flask(__name__)"
for i, line in enumerate(lines):
    if "app = Flask(__name__)" in line:
        # Insert after the app creation and config
        # Skip forward to find a blank line
        j = i + 1
        while j < len(lines) and lines[j].strip() != "":
            j += 1
        lines.insert(j, function_code)
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("✓ Added _build_evidence_prompt function")
