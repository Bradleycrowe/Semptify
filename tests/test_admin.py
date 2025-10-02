import os
import json
import pytest
from unittest.mock import patch

import requests

from SemptifyGUI import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_admin_unauthorized(client):
    # Ensure ADMIN_TOKEN not set
    if 'ADMIN_TOKEN' in os.environ:
        del os.environ['ADMIN_TOKEN']
    rv = client.get('/admin')
    assert rv.status_code == 401

@patch('SemptifyGUI.requests.get')
@patch('SemptifyGUI.requests.post')
def test_release_now_and_trigger_workflow(mock_post, mock_get, client, tmp_path):
    # Set ADMIN_TOKEN
    os.environ['ADMIN_TOKEN'] = 'testtoken'
    os.environ['GITHUB_TOKEN'] = 'ghp_test'
    os.environ['GITHUB_OWNER'] = 'owner'
    os.environ['GITHUB_REPO'] = 'repo'

    # Mock get ref
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = { 'object': { 'sha': 'deadbeef' } }

    # Mock create ref success
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {}

    # Call release_now
    rv = client.post('/release_now', data={'token': 'testtoken'})
    # redirect to releases page on success
    assert rv.status_code in (302, 303)

    # Trigger workflow dispatch (mock returns 204)
    mock_post.return_value.status_code = 204
    rv = client.post('/trigger_workflow', data={'token': 'testtoken', 'workflow': 'ci.yml', 'ref': 'main'})
    assert rv.status_code in (302, 303)

    # Cleanup
    del os.environ['ADMIN_TOKEN']
    del os.environ['GITHUB_TOKEN']
    del os.environ['GITHUB_OWNER']
    del os.environ['GITHUB_REPO']
