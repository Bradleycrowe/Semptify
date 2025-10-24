import pytest
import json
import os
from modules.verify.verify_module import fetch_manifest, validate_manifest, download_artifact, compute_sha256

@pytest.fixture
def setup_environment(monkeypatch):
    monkeypatch.setenv("VERIFY_ENDPOINT", "http://example.com/manifest")
    monkeypatch.setenv("VERIFY_API_KEY", "test_api_key")
    monkeypatch.setenv("VERIFY_LOG_PATH", "./logs")
    os.makedirs("./logs", exist_ok=True)

@pytest.fixture
def good_manifest():
    return {
        "artifacts": [
            {"name": "artifact1", "hash": "abc123"},
            {"name": "artifact2", "hash": "def456"}
        ]
    }

@pytest.fixture
def bad_manifest():
    return {
        "artifacts": [
            {"name": "artifact1", "hash": "abc123"},
            {"name": "artifact2"}  # Missing hash
        ]
    }

@pytest.fixture
def missing_field_manifest():
    return {
        "artifacts": [
            {"hash": "abc123"}  # Missing name
        ]
    }

def test_fetch_manifest(setup_environment, requests_mock, good_manifest):
    requests_mock.get(os.environ["VERIFY_ENDPOINT"], json=good_manifest)
    manifest = fetch_manifest()
    assert manifest == good_manifest

def test_validate_manifest(good_manifest):
    schema_path = os.path.join(os.path.dirname(__file__), '../verify_schema.json')
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    is_valid = validate_manifest(good_manifest, schema)
    assert is_valid is True

def test_validate_manifest_bad_hash(bad_manifest):
    schema_path = os.path.join(os.path.dirname(__file__), '../verify_schema.json')
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    is_valid = validate_manifest(bad_manifest, schema)
    assert is_valid is False

def test_download_artifact(good_manifest, tmp_path):
    artifact = good_manifest["artifacts"][0]
    # Simulate downloading the artifact
    download_path = download_artifact(artifact["name"], tmp_path)
    assert os.path.exists(download_path)

def test_compute_sha256(good_manifest, tmp_path):
    artifact = good_manifest["artifacts"][0]
    test_file_path = os.path.join(tmp_path, artifact["name"])
    with open(test_file_path, 'w') as f:
        f.write("test content")
    computed_hash = compute_sha256(test_file_path)
    assert computed_hash == "expected_sha256_hash"  # Replace with actual expected hash

def test_missing_field_validation(missing_field_manifest):
    schema_path = os.path.join(os.path.dirname(__file__), '../verify_schema.json')
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    is_valid = validate_manifest(missing_field_manifest, schema)
    assert is_valid is False

def test_network_failure_handling(setup_environment, requests_mock):
    requests_mock.get(os.environ["VERIFY_ENDPOINT"], status_code=500)
    with pytest.raises(Exception):
        fetch_manifest()  # Ensure it raises an exception on network failure
