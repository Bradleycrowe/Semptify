import json
import os
from flask import Blueprint, jsonify, request
import requests

ollama_bp = Blueprint('ollama', __name__)

CONFIG_PATH = os.path.join(os.getcwd(), 'config', 'ollama_data_sources.json')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
DEFAULT_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')


def _load_sources():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('sources', [])
    except Exception:
        return []

@ollama_bp.get('/api/ollama/sources')
def list_sources():
    sources = _load_sources()
    return jsonify({ 'count': len(sources), 'sources': sources })

@ollama_bp.post('/api/ollama/summarize')
def summarize_source():
    payload = request.get_json(silent=True) or {}
    sources = _load_sources()

    # Resolve source by name or URL
    src_name = payload.get('name')
    src_url = payload.get('url')
    src = None
    if src_name:
        src = next((s for s in sources if s.get('name') == src_name), None)
    if not src and src_url:
        src = next((s for s in sources if s.get('url') == src_url), None)

    # Fallback: accept ad-hoc source
    if not src and (src_name or src_url):
        src = { 'name': src_name or src_url, 'url': src_url or src_name, 'type': payload.get('type', 'unknown') }

    if not src:
        return jsonify({ 'error': 'Source not found. Provide name or url that matches config.' }), 400

    model = payload.get('model', DEFAULT_MODEL)
    prompt = payload.get('prompt') or (
        f"Summarize the main legal and housing concepts from {src.get('name')} ({src.get('url')}). "
        "Use plain language. List 5 bullet points with links if available."
    )

    # Non-streaming Ollama generate request
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={ 'model': model, 'prompt': prompt, 'stream': False },
            timeout=60
        )
        r.raise_for_status()
        data = r.json() if r.headers.get('content-type','').startswith('application/json') else { 'response': r.text }
        return jsonify({
            'model': model,
            'source': src,
            'response': data.get('response')
        })
    except Exception as e:
        return jsonify({ 'error': str(e), 'ollama_url': OLLAMA_URL }), 502
