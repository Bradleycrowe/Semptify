"""
AI Blueprint
Handles AI-powered assistance using local Ollama models
"""

from flask import Blueprint, request, jsonify, session
from security import log_event
import requests
import os

# Create blueprint
ai_bp = Blueprint('ai', __name__, url_prefix='/api')


@ai_bp.route('/copilot', methods=['POST'])
def copilot_api():
    """Copilot API endpoint for AI assistance - powered by Ollama (local AI)"""
    data = request.get_json(force=True, silent=True)
    if not data or 'prompt' not in data:
        return jsonify({"error": "missing_prompt"}), 400
    
    user_prompt = data['prompt']
    context = data.get('context', {})
    
    # Get AI model preference from environment (default: llama3.2)
    model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    
    # Build system prompt for tenant rights assistance
    system_prompt = """You are a knowledgeable tenant rights legal assistant specializing in Minnesota housing law. 

Your role:
- Provide accurate, actionable advice on tenant rights and landlord-tenant disputes
- Focus on Minnesota-specific laws and procedures
- Help users understand eviction defense, rent disputes, habitability issues
- Be empathetic and supportive while maintaining legal accuracy
- Cite specific statutes when relevant (e.g., MN Statutes § 504B)
- Always recommend consulting a lawyer for complex legal matters

Key areas of expertise:
- Eviction notices and defense strategies
- Security deposits and return rights
- Rent withholding for uninhabitable conditions
- Discrimination and harassment protections
- Lease termination procedures
- Court filing procedures and deadlines"""

    try:
        # Call local Ollama API
        ollama_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": model,
                "prompt": f"{system_prompt}\n\nUser question: {user_prompt}\n\nProvide helpful, accurate advice:",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 512  # Max response length
                }
            },
            timeout=30
        )
        
        if ollama_response.status_code == 200:
            ai_response = ollama_response.json().get('response', '')
            
            # Log AI usage
            log_event("copilot_used", {
                "user_id": session.get('user_id', 'anonymous'),
                "model": model,
                "prompt_length": len(user_prompt),
                "response_length": len(ai_response),
                "provider": "ollama_local"
            })
            
            return jsonify({
                "status": "ok",
                "response": ai_response,
                "model": model,
                "provider": "ollama",
                "cost": 0  # FREE!
            }), 200
        else:
            # Ollama error
            return jsonify({
                "status": "error",
                "error": "ollama_unavailable",
                "message": "Local AI service is not responding. Please check if Ollama is running.",
                "help": "Run 'ollama serve' in terminal to start Ollama"
            }), 503
            
    except requests.exceptions.ConnectionError:
        # Ollama not running
        return jsonify({
            "status": "error",
            "error": "ollama_not_running",
            "message": "Ollama is not running. Start it with 'ollama serve'",
            "fallback": "AI assistance temporarily unavailable"
        }), 503
    except Exception as e:
        # Unexpected error
        log_event("copilot_error", {
            "error": str(e),
            "model": model
        })
        return jsonify({
            "status": "error",
            "error": "unexpected_error",
            "message": f"AI service error: {str(e)}"
        }), 500
