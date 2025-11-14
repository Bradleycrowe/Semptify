"""
Ollama AI integration routes for Semptify
Provides AI-powered summarization of legal and housing data sources
"""
from flask import Blueprint, jsonify, request
import requests
import json
import os

ollama_bp = Blueprint('ollama', __name__, url_prefix='/api/ollama')

def _load_sources():
    """Load data sources from config file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'ollama_data_sources.json')
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get('sources', [])
    except Exception as e:
        print(f"[WARN] Could not load data sources: {e}")
        return []

@ollama_bp.route('/sources', methods=['GET'])
def list_sources():
    """List all available AI data sources"""
    sources = _load_sources()
    return jsonify({
        "count": len(sources),
        "sources": sources
    })

@ollama_bp.route('/summarize', methods=['POST'])
def summarize_source():
    """Generate AI summary with citations and links"""
    data = request.get_json()
    source_name = data.get('name')
    model = data.get('model', 'llama3')
    
    if not source_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    # Find source details
    sources = _load_sources()
    source = next((s for s in sources if s['name'] == source_name), None)
    
    if not source:
        return jsonify({"error": f"Source '{source_name}' not found"}), 400
    
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    
    # Enhanced prompt requesting citations and details
    prompt = f"""Provide a detailed summary of {source['name']} ({source['url']}) focusing on:

1. What this resource provides for tenants and landlords
2. Key legal information available
3. How to access and use this resource
4. Most important sections or topics covered

Include specific examples and cite the source URL: {source['url']}

Format your response with:
- Overview paragraph
- Key Features (bullet points)
- How to Use (step-by-step if applicable)
- Citation with full URL

Be specific and detailed."""
    
    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            summary_text = result.get('response', 'No summary generated.')
            
            # Add structured citation footer
            citation = f"\n\n---\n**Source:** [{source['name']}]({source['url']})\n**Type:** {source.get('type', 'N/A')}\n**URL:** {source['url']}"
            
            return jsonify({
                "response": summary_text + citation,
                "source": {
                    "name": source['name'],
                    "url": source['url'],
                    "type": source.get('type')
                },
                "model": model
            })
        else:
            return jsonify({
                "error": f"Ollama request failed with status {response.status_code}",
                "ollama_url": ollama_url
            }), 502
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Could not connect to Ollama server. Please ensure Ollama is running.",
            "ollama_url": ollama_url
        }), 502
    except Exception as e:
        return jsonify({
            "error": f"Request failed: {str(e)}",
            "ollama_url": ollama_url
        }), 502
