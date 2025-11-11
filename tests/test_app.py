import os
import tempfile
import pytest
from Semptify import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    # Homepage has "Semptify" and "Get Started" button
    assert b"Semptify" in rv.data
    assert b"Get Started" in rv.data

