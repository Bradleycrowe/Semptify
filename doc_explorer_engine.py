# doc_explorer_engine.py
import ast
import json
from pathlib import Path
from typing import Dict, List, Any

class SemptifyDocExplorer:
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.documentation = {
            "blueprints": [],
            "routes": [],
            "apis": [],
            "utilities": [],
            "templates": []
        }
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
            return {
                "name": file_path.stem,
                "path": str(file_path.relative_to(self.base_path)),
                "docstring": ast.get_docstring(tree),
                "functions": [],
                "classes": []
            }
        except Exception as e:
            return {"name": file_path.stem, "error": str(e)}
    
    def scan_application(self):
        for route_file in self.base_path.glob("*_routes.py"):
            analysis = self.analyze_file(route_file)
            self.documentation["routes"].append(analysis)
        for api_file in self.base_path.glob("*_api.py"):
            analysis = self.analyze_file(api_file)
            self.documentation["apis"].append(analysis)
        blueprints_path = self.base_path / "blueprints"
        if blueprints_path.exists():
            for bp_file in blueprints_path.glob("*.py"):
                if bp_file.stem != "__init__":
                    analysis = self.analyze_file(bp_file)
                    self.documentation["blueprints"].append(analysis)
        return self.documentation
    
    def get_feature_map(self) -> Dict[str, Any]:
        return {
            "User Management": {"description": "Registration, login, authentication", "components": ["auth_bp"], "routes": ["/register", "/login"], "icon": "👤"},
            "Document Vault": {"description": "Secure document storage with notarization", "components": ["vault_bp"], "routes": ["/vault"], "icon": "🔐"},
            "Rent & Ledger": {"description": "Track rent payments and receipts", "components": ["ledger_tracking"], "routes": ["/ledger"], "icon": "💰"},
            "AI Assistant": {"description": "Local and cloud AI integration", "components": ["ai_bp"], "routes": ["/api/copilot"], "icon": "🤖"},
            "Learning System": {"description": "Adaptive learning engine", "components": ["learning_routes"], "routes": ["/learning"], "icon": "📚"},
            "Admin": {"description": "System administration", "components": ["security"], "routes": ["/admin", "/metrics"], "icon": "⚙️"}
        }
    
    def get_navigation_structure(self) -> Dict[str, Any]:
        return {
            "For Tenants": {"icon": "👥", "sections": [{"name": "Get Started", "link": "/register", "description": "Create account"}]},
            "Documentation": {"icon": "📖", "sections": [{"name": "Overview", "link": "/docs/overview", "description": "How it works"}]}
        }
    
    def export_to_json(self, output_path: str = "data/documentation.json"):
        output_file = self.base_path / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        full_doc = {
            "components": self.documentation,
            "features": self.get_feature_map(),
            "navigation": self.get_navigation_structure()
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(full_doc, f, indent=2)
        return output_file

def generate_documentation(base_path: str = None) -> Dict[str, Any]:
    explorer = SemptifyDocExplorer(base_path)
    doc = explorer.scan_application()
    explorer.export_to_json()
    return {"documentation": doc, "features": explorer.get_feature_map(), "navigation": explorer.get_navigation_structure()}
