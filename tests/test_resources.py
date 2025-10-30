import os
import pytest
from Semptify import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_resources_page_lists_links(client):
    rv = client.get('/resources')
    assert rv.status_code == 200
    body = rv.data.decode('utf-8')
    assert '/resources/download/witness_statement.txt' in body
    assert '/resources/download/filing_packet_checklist.txt' in body
    assert '/resources/download/filing_packet_timeline.txt' in body

def test_download_timeline_template(client):
    rv = client.get('/resources/download/filing_packet_timeline.txt')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'].startswith('text/plain')
    assert 'Filing Packet Timeline' in rv.data.decode('utf-8')

