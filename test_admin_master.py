import sys, os, io, re
os.chdir('C:\\Semptify\\Semptify')
sys.path.insert(0, os.getcwd())
old_stdout, old_stderr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = io.StringIO()
from Semptify import app
app.config['TESTING'] = True
client = app.test_client()
sys.stdout, sys.stderr = old_stdout, old_stderr
print('Testing /admin/master...')
try:
    response = client.get('/admin/master', follow_redirects=True)
    print(f'Status: {response.status_code}')
    if response.status_code != 200:
        data = response.get_data(as_text=True)
        if 'RecursionError' in data:
            print('ERROR: RecursionError detected')
        elif 'TemplateNotFound' in data:
            match = re.search(r'TemplateNotFound:\s*(.+?)(?:\n|\r)', data)
            if match:
                print(f'ERROR: TemplateNotFound: {match.group(1)}')
        else:
            print(f'ERROR: Status {response.status_code}')
except RecursionError as e:
    print(f'RecursionError in test: {str(e)[:100]}')
except Exception as e:
    print(f'Exception: {type(e).__name__}: {str(e)[:150]}')
