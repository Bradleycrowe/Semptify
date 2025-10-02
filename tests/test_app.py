import os
import tempfile
import pytest
from SemptifyGUI import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"SemptifyGUI is live" in rv.data

def test_admin_with_valid_token(client):
    rv = client.get('/admin?token=devtoken')
    assert rv.status_code == 200
    assert b"Semptify Admin" in rv.data
    # Verify token is passed to template (not hardcoded)
    assert b'value="devtoken"' in rv.data

def test_admin_without_token(client):
    rv = client.get('/admin')
    assert rv.status_code == 401
    assert b"Unauthorized" in rv.data

def test_admin_with_invalid_token(client):
    rv = client.get('/admin?token=wrongtoken')
    assert rv.status_code == 401
    assert b"Unauthorized" in rv.data

def test_sbom_list_with_valid_token(client):
    rv = client.get('/sbom?token=devtoken')
    assert rv.status_code == 200
    assert b"SBOM files" in rv.data
    # Verify back link uses dynamic token
    assert b'href="/admin?token=devtoken"' in rv.data

def test_sbom_list_without_token(client):
    rv = client.get('/sbom')
    assert rv.status_code == 401
    assert b"Unauthorized" in rv.data
