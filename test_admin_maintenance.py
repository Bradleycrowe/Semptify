import sys, os, io, re
os.chdir('C:\\Semptify\\Semptify')
sys.path.insert(0, os.getcwd())
old_stdout, old_stderr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = io.StringIO()
from Semptify import app
app.config['TESTING'] = True
client = app.test_client()
sys.stdout, sys.stderr = old_stdout, old_stderr

routes = [('/admin/master', 'Admin Master'), ('/maintenance/', 'Maintenance')]
for url, name in routes:
    try:
        response = client.get(url)
        if response.status_code == 500:
            data = response.get_data(as_text=True)
            match = re.search(r'(TemplateNotFound|NameError|KeyError|AttributeError|TypeError|RecursionError):\s*(.+?)(?:\n|\r)', data)
            if match:
                print(f'{name}: {match.group(1)}: {match.group(2)}')
            else:
                print(f'{name}: 500 (unknown error)')
        else:
            print(f'{name}: {response.status_code} ✓')
    except Exception as e:
        print(f'{name}: Exception - {str(e)[:100]}')
