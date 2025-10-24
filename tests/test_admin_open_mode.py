import os
from Semptify import app


def test_admin_open_mode_access():
    # Force open mode explicitly
    os.environ['SECURITY_MODE'] = 'open'
    app.config['TESTING'] = True
    with app.test_client() as client:
        rv = client.get('/admin')
        assert rv.status_code == 200
        assert b'SECURITY MODE: OPEN' in rv.data

