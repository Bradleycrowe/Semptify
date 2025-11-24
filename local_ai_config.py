"""
Local AI Configuration - Ollama setup for self-hosted AI
Use your PC as AI backend instead of external APIs
"""
import os
import requests
from flask import current_app

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

def check_ollama_status():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return {
                "status": "online",
                "url": OLLAMA_BASE_URL,
                "models": [m["name"] for m in models],
                "model_count": len(models)
            }
    except Exception as e:
        return {
            "status": "offline",
            "url": OLLAMA_BASE_URL,
            "error": str(e)
        }
    
    return {"status": "unknown"}

def ollama_generate(prompt, model=None, system_prompt=None, max_tokens=2000):
    """Generate text using local Ollama"""
    model = model or OLLAMA_DEFAULT_MODEL
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.7
        }
    }
    
    if system_prompt:
        payload["system"] = system_prompt
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            "success": True,
            "response": result.get("response", ""),
            "model": model,
            "eval_count": result.get("eval_count", 0),
            "eval_duration": result.get("eval_duration", 0)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model
        }

def ollama_chat(messages, model=None, max_tokens=2000):
    """Chat completion using local Ollama"""
    model = model or OLLAMA_DEFAULT_MODEL
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            "success": True,
            "message": result.get("message", {}),
            "model": model,
            "eval_count": result.get("eval_count", 0)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model
        }

def list_ollama_models():
    """Get all available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        models = data.get("models", [])
        
        return {
            "success": True,
            "models": [
                {
                    "name": m["name"],
                    "size": m.get("size", 0),
                    "modified": m.get("modified_at", "")
                }
                for m in models
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "models": []
        }

def pull_ollama_model(model_name):
    """Pull/download a model from Ollama registry"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/pull",
            json={"name": model_name},
            timeout=300  # 5 min timeout for large models
        )
        response.raise_for_status()
        
        return {"success": True, "model": model_name}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Recommended models for legal/tenant rights work
RECOMMENDED_MODELS = {
    "llama3.2": "Fast, general-purpose (1.3GB)",
    "mistral": "Excellent reasoning (4.1GB)",
    "phi3": "Small but capable (2.3GB)",
    "llama3.1:8b": "Larger, more accurate (4.7GB)",
    "codellama": "Good for document analysis (3.8GB)"
}

def get_setup_instructions():
    """Return setup instructions for local AI"""
    return {
        "windows": [
            "1. Download Ollama from https://ollama.com/download",
            "2. Install and run Ollama (runs as background service)",
            "3. Open PowerShell and run: ollama pull llama3.2",
            "4. Verify: curl http://localhost:11434/api/tags",
            "5. Restart Semptify - AI features will auto-connect"
        ],
        "env_vars": {
            "OLLAMA_BASE_URL": "http://localhost:11434 (or remote PC IP)",
            "OLLAMA_MODEL": "llama3.2 (or any pulled model)",
            "OLLAMA_TIMEOUT": "120 (seconds)"
        },
        "remote_pc": [
            "To use another PC on your network as AI server:",
            "1. Install Ollama on that PC",
            "2. Set OLLAMA_HOST=0.0.0.0 on that PC",
            "3. In Semptify .env: OLLAMA_BASE_URL=http://<pc-ip>:11434"
        ],
        "recommended_models": RECOMMENDED_MODELS
    }
