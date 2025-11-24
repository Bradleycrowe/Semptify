"""
AI Development Assistant - GitHub Copilot integration for building new features
"""
from flask import Blueprint, render_template, request, jsonify
from local_ai_config import ollama_chat, ollama_generate
import json

ai_dev_bp = Blueprint("ai_dev", __name__, url_prefix="/gui")

@ai_dev_bp.route("/ai-dev")
def ai_development_ui():
    """AI development assistant interface"""
    return render_template("ai_dev_assistant.html")

@ai_dev_bp.route("/ai-dev/generate", methods=["POST"])
def generate_feature():
    """Generate code for new feature using AI"""
    data = request.get_json()
    feature_description = data.get("description", "")
    
    system_prompt = """You are an expert Python/Flask developer building features for Semptify, 
    a tenant rights protection platform. Generate production-ready code with:
    - Flask blueprints and routes
    - Proper error handling
    - Security best practices
    - Integration with existing profile system
    - Comments explaining the code
    """
    
    prompt = f"""Create a new feature: {feature_description}

Include:
1. Flask blueprint file (*_routes.py)
2. Business logic file (*_engine.py if needed)
3. HTML template
4. How to register the blueprint in Semptify.py

Format as JSON with keys: blueprint_code, engine_code, template_code, registration_code"""
    
    result = ollama_generate(prompt, system_prompt=system_prompt, max_tokens=3000)
    
    if result.get("success"):
        try:
            # Try to parse as JSON
            code = json.loads(result["response"])
            return jsonify({"success": True, "code": code})
        except:
            # Return as plain text if not JSON
            return jsonify({"success": True, "code": {"raw": result["response"]}})
    else:
        return jsonify({"success": False, "error": result.get("error")}), 500

@ai_dev_bp.route("/ai-dev/chat", methods=["POST"])
def ai_chat():
    """Chat with AI about development"""
    data = request.get_json()
    messages = data.get("messages", [])
    
    # Add system context about Semptify
    system_message = {
        "role": "system",
        "content": """You are helping develop Semptify, a Flask tenant rights platform.
        
Current architecture:
- Single user, multiple client profiles (/profiles)
- Profile system for case isolation
- Ollama local AI integration
- R2 cloud storage
- 43+ modules including vault, ledger, complaints, timeline, learning

Tech stack: Flask, SQLite, Jinja2, Waitress, Ollama, boto3 (R2)
"""
    }
    
    full_messages = [system_message] + messages
    result = ollama_chat(full_messages, max_tokens=2000)
    
    if result.get("success"):
        return jsonify({"success": True, "message": result["message"]})
    else:
        return jsonify({"success": False, "error": result.get("error")}), 500

@ai_dev_bp.route("/ai-dev/analyze-code", methods=["POST"])
def analyze_code():
    """Analyze existing code and suggest improvements"""
    data = request.get_json()
    code = data.get("code", "")
    
    prompt = f"""Analyze this Python/Flask code and provide:
1. Security issues
2. Performance improvements
3. Best practices violations
4. Suggested refactoring

Code:
```python
{code}
```

Format response as JSON with keys: security, performance, best_practices, refactoring"""
    
    result = ollama_generate(prompt, max_tokens=2000)
    
    if result.get("success"):
        return jsonify({"success": True, "analysis": result["response"]})
    else:
        return jsonify({"success": False, "error": result.get("error")}), 500
