# STEP 4: Fix registration flow to redirect to /verify
# First add /verify route
verify_route = """

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    '''Verify user registration via email or phone'''
    if request.method == 'GET':
        return render_template('verify.html')
    # Process verification
    return redirect(url_for('index'))
"""

lines = open("Semptify.py", "r", encoding="utf-8").readlines()

# Add verify route after register
for i in range(len(lines)):
    if "@app.route('/register')" in lines[i]:
        j = i + 1
        while j < len(lines) and (lines[j].startswith('    ') or lines[j].strip() == ''):
            j += 1
        lines.insert(j, verify_route)
        break

# Fix register.py to redirect
reg_lines = open("register.py", "r", encoding="utf-8").readlines()
for i in range(len(reg_lines)):
    if "return render_template(" in reg_lines[i] and "register_success.html" in reg_lines[i]:
        reg_lines[i] = "    return redirect('/verify', code=302)\n"
        break

open("Semptify.py", "w", encoding="utf-8").writelines(lines)
open("register.py", "w", encoding="utf-8").writelines(reg_lines)
print("✓ Step 4: Fixed registration flow with /verify redirect")
