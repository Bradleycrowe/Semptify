from flask import Flask
import sys, os, io
os.chdir('C:\\Semptify\\Semptify')
sys.path.insert(0, os.getcwd())
old_stdout, old_stderr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = io.StringIO()
from Semptify import app
app.config['TESTING'] = True
client = app.test_client()
sys.stdout, sys.stderr = old_stdout, old_stderr
print('\n🧪 Testing /journey/...\n')
response = client.get('/journey/')
print(f'Status: {response.status_code}')
if response.status_code == 500:
    data = response.get_data(as_text=True)
    import re
    # Find the actual error
    match = re.search(r'(TemplateNotFound|NameError|KeyError|AttributeError|TypeError):\s*(.+?)(?:\n|\r)', data)
    if match:
        print(f'\n❌ ERROR: {match.group(1)}: {match.group(2)}')
    else:
        print(f'\n❌ ERROR (first 800 chars):\n{data[:800]}')
