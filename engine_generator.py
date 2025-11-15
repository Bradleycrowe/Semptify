"""
Dynamic Engine Generator
Creates missing engine modules on-demand when blueprints fail to import them.
"""
import os
import json
import importlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class EngineGenerator:
    """Generates missing engine modules based on feature requirements."""
    
    def __init__(self, engines_dir='engines', templates_dir='engine_templates'):
        self.engines_dir = Path(engines_dir)
        self.templates_dir = Path(templates_dir)
        self.engines_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
    def find_or_create_engine(self, engine_name: str, feature_type: Optional[str] = None):
        """Try to import engine. If not found, generate it based on feature type."""
        try:
            return importlib.import_module(engine_name)
        except ImportError:
            logger.info(f"Engine {engine_name} not found, generating...")
            if not feature_type:
                feature_type = self._infer_feature_type(engine_name)
            self._generate_engine(engine_name, feature_type)
            return importlib.import_module(engine_name)
    
    def _infer_feature_type(self, engine_name: str) -> str:
        """Infer feature type from engine name."""
        name_lower = engine_name.lower()
        if any(x in name_lower for x in ['find', 'search', 'lookup', 'directory']):
            return 'search'
        elif any(x in name_lower for x in ['calc', 'compute', 'estimate']):
            return 'calculator'
        elif any(x in name_lower for x in ['form', 'submit', 'file', 'wizard']):
            return 'form'
        elif any(x in name_lower for x in ['validate', 'check', 'verify']):
            return 'validator'
        elif any(x in name_lower for x in ['generate', 'create', 'build']):
            return 'generator'
        else:
            return 'generic'
    
    def _generate_engine(self, engine_name: str, feature_type: str):
        """Generate engine code based on feature type."""
        templates = {
            'search': self._search_template,
            'calculator': self._calculator_template,
            'form': self._form_template,
            'validator': self._validator_template,
            'generator': self._generator_template,
            'generic': self._generic_template
        }
        template_func = templates.get(feature_type, self._generic_template)
        code = template_func(engine_name)
        engine_file = self.engines_dir / f"{engine_name}.py"
        with open(engine_file, 'w') as f:
            f.write(code)
        logger.info(f"✓ Generated {engine_file} (type: {feature_type})")
        self._log_generation(engine_name, feature_type)
    
    def _search_template(self, name: str) -> str:
        func_name = name.replace('_engine', '') + '_logic'
        return f'''"""Auto-generated search engine"""

def {func_name}(query):
    """Search logic."""
    search_term = query.get('search', '')
    location = query.get('location', '')
    results = [{{"id": 1, "title": f"Result for {{search_term}}", "location": location}}] if search_term else []
    return {{"status": "success", "results": results, "count": len(results)}}
'''
    
    def _calculator_template(self, name: str) -> str:
        func_name = name.replace('_engine', '') + '_logic'
        return f'''"""Auto-generated calculator engine"""

def {func_name}(data):
    """Calculation logic."""
    value = data.get('value', 0)
    result = value * 1.0
    return {{"status": "success", "result": result, "input": data}}
'''
    
    def _form_template(self, name: str) -> str:
        func_name = name.replace('_engine', '') + '_logic'
        return f'''"""Auto-generated form processing engine"""

def {func_name}(form_data):
    """Form processing logic."""
    errors = []
    if not form_data.get('required_field'):
        errors.append('Required field missing')
    if errors:
        return {{"status": "error", "errors": errors}}
    return {{"status": "success", "data": form_data}}
'''
    
    def _validator_template(self, name: str) -> str:
        func_name = name.replace('_engine', '') + '_logic'
        return f'''"""Auto-generated validator engine"""

def {func_name}(data):
    """Validation logic."""
    errors = []
    if not data:
        errors.append('No data provided')
    is_valid = len(errors) == 0
    return {{"status": "valid" if is_valid else "invalid", "valid": is_valid, "errors": errors}}
'''
    
    def _generator_template(self, name: str) -> str:
        func_name = name.replace('_engine', '') + '_logic'
        return f'''"""Auto-generated generator engine"""

def {func_name}(params):
    """Generation logic."""
    output = {{"generated_at": "now", "content": "Generated content", "params": params}}
    return {{"status": "success", "output": output}}
'''
    
    def _generic_template(self, name: str) -> str:
        func_name = name.replace('_engine', '') + '_logic'
        feature_name = name.replace('_engine', '').replace('_', ' ').title()
        return f'''"""Auto-generated generic engine"""

def {func_name}(data):
    """Generic business logic for {feature_name}."""
    return {{"status": "success", "data": data, "message": "{feature_name} processed"}}
'''
    
    def _log_generation(self, engine_name: str, feature_type: str):
        """Log engine generation event."""
        log_file = Path('data/engine_generations.json')
        if log_file.exists():
            with open(log_file) as f:
                log = json.load(f)
        else:
            log = {'generations': []}
        log['generations'].append({
            'engine_name': engine_name,
            'feature_type': feature_type,
            'generated_at': datetime.now().isoformat(),
            'status': 'active'
        })
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(log, f, indent=2)

_generator = None

def get_engine_generator():
    """Get or create the global engine generator instance."""
    global _generator
    if _generator is None:
        _generator = EngineGenerator()
    return _generator

def find_or_create_engine(engine_name: str, feature_type: Optional[str] = None):
    """Convenience function to find or create an engine."""
    return get_engine_generator().find_or_create_engine(engine_name, feature_type)
