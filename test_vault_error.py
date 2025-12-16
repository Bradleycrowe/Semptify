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
print('\n🧪 Testing /app/vault...\n')
response = client.get('/app/vault')
print(f'Status: {response.status_code}')
if response.status_code == 500:
    print(f'\n❌ ERROR:\n{response.get_data(as_text=True)[:1500]}')
else:
    print(f'✓ WORKS! Length: {len(response.data)} bytes')
