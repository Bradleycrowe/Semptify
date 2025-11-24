# Fix Response charset and _build_evidence_prompt
lines = open("Semptify.py", "r", encoding="utf-8").readlines()

for i in range(len(lines)):
    # Fix Response charset parameter
    if 'Response("\\n".join(output), mimetype="text/plain", charset="utf-8")' in lines[i]:
        lines[i] = '        return Response("\\n".join(output), mimetype="text/plain; charset=utf-8")\n'
    
    # Fix _build_evidence_prompt to lowercase form_type
    if 'form_type_readable = form_type.replace("_", " ").title()' in lines[i]:
        lines[i] = '        form_type_readable = form_type.replace("_", " ")\n'

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
print("Fixed Response and _build_evidence_prompt")
