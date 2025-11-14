"""
AI integration routes for Semptify - Groq (primary) with Ollama fallback
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

def _summarize_with_groq(source, model='llama-3.1-70b-versatile'):
    """Use Groq API for fast, free AI summarization"""
    try:
        from groq import Groq
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return None, "GROQ_API_KEY not set"
        
        client = Groq(api_key=api_key)
        
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

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.7,
            max_tokens=1024
        )
        
        response_text = chat_completion.choices[0].message.content
        citation = f"\n\n---\n**Source:** [{source['name']}]({source['url']})\n**Type:** {source.get('type', 'N/A')}\n**URL:** {source['url']}\n**Powered by:** Groq AI"
        
        return response_text + citation, None
        
    except Exception as e:
        return None, f"Groq error: {str(e)}"

def _summarize_with_ollama(source, model='llama3'):
    """Fallback to Ollama for summarization"""
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    
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
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            summary_text = result.get('response', 'No summary generated.')
            citation = f"\n\n---\n**Source:** [{source['name']}]({source['url']})\n**Type:** {source.get('type', 'N/A')}\n**URL:** {source['url']}\n**Powered by:** Ollama ({model})"
            return summary_text + citation, None
        else:
            return None, f"Ollama returned status {response.status_code}"
            
    except Exception as e:
        return None, f"Ollama error: {str(e)}"

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
    """Generate AI summary with citations - tries Groq first, falls back to Ollama"""
    data = request.get_json()
    source_name = data.get('name')
    
    if not source_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    sources = _load_sources()
    source = next((s for s in sources if s['name'] == source_name), None)
    
    if not source:
        return jsonify({"error": f"Source '{source_name}' not found"}), 400
    
    # Try Groq first (fast & free)
    response_text, groq_error = _summarize_with_groq(source)
    
    if response_text:
        return jsonify({
            "response": response_text,
            "source": {"name": source['name'], "url": source['url'], "type": source.get('type')},
            "provider": "groq",
            "model": "llama-3.1-70b-versatile"
        })
    
    # Fallback to Ollama
    print(f"[INFO] Groq failed ({groq_error}), falling back to Ollama")
    response_text, ollama_error = _summarize_with_ollama(source)
    
    if response_text:
        return jsonify({
            "response": response_text,
            "source": {"name": source['name'], "url": source['url'], "type": source.get('type')},
            "provider": "ollama",
            "model": "llama3"
        })
    
    # Both failed
    return jsonify({
        "error": "All AI providers failed",
        "groq_error": groq_error,
        "ollama_error": ollama_error,
        "help": "Set GROQ_API_KEY or ensure Ollama is running"
    }), 502
