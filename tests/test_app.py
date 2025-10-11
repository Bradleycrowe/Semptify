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
    # Homepage content should include key navigation links
    assert b"Register" in rv.data
    assert b"Resources" in rv.data
    assert b"Health" in rv.data
