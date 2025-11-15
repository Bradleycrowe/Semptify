"""
Enhanced Engine Generator with Validation
Checks dependencies, security, and requirements before generating code.
"""
import os
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from engine_generator import EngineGenerator
from feature_registry import get_feature_registry, FeatureStatus

class ValidatedEngineGenerator(EngineGenerator):
    """Engine generator with pre-generation validation."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registry = get_feature_registry()
        self.security_patterns = self._load_security_patterns()
    
    def find_or_create_engine(self, engine_name: str, feature_type: Optional[str] = None,
                            requirements: Optional[Dict] = None):
        """Generate engine only after validation passes."""
        try:
            return super().find_or_create_engine(engine_name, feature_type)
        except ImportError:
            # Before generating, validate requirements
            validation_results = self.validate_requirements(engine_name, requirements or {})
            
            if not validation_results['can_generate']:
                error_msg = f"Cannot generate {engine_name}: " + \
                           ", ".join(validation_results['errors'])
                self.registry.register_feature(
                    engine_name.replace('_engine', ''),
                    feature_type or self._infer_feature_type(engine_name),
                    status=FeatureStatus.STUB
                )
                raise ImportError(error_msg)
            
            # Generate with warnings logged
            if validation_results['warnings']:
                for warning in validation_results['warnings']:
                    print(f"⚠️  {warning}")
            
            # Proceed with generation
            if not feature_type:
                feature_type = self._infer_feature_type(engine_name)
            
            self._generate_engine(engine_name, feature_type)
            
            # Register in feature registry
            self.registry.register_feature(
                engine_name.replace('_engine', ''),
                feature_type,
                status=FeatureStatus.STUB,
                engine_path=str(self.engines_dir / f"{engine_name}.py"),
                requires_config=requirements
            )
            
            # Record dependencies
            if requirements:
                for dep_type, deps in requirements.items():
                    if isinstance(deps, list):
                        for dep in deps:
                            is_met = self._check_dependency(dep_type, dep)
                            self.registry.add_dependency(
                                engine_name.replace('_engine', ''),
                                dep_type, dep, is_met
                            )
            
            return super().find_or_create_engine(engine_name, feature_type)
    
    def validate_requirements(self, engine_name: str, requirements: Dict) -> Dict:
        """
        Validate all requirements before code generation.
        
        Returns:
            {
                'can_generate': bool,
                'errors': List[str],  # Blocking issues
                'warnings': List[str]  # Non-blocking issues
            }
        """
        errors = []
        warnings = []
        
        # Check database requirements
        if requirements.get('database'):
            db_errors = self._validate_database(requirements['database'])
            errors.extend(db_errors)
        
        # Check API requirements
        if requirements.get('apis'):
            api_errors, api_warnings = self._validate_apis(requirements['apis'])
            errors.extend(api_errors)
            warnings.extend(api_warnings)
        
        # Check config requirements
        if requirements.get('config'):
            config_errors = self._validate_config(requirements['config'])
            errors.extend(config_errors)
        
        # Check Python dependencies
        if requirements.get('packages'):
            pkg_errors, pkg_warnings = self._validate_packages(requirements['packages'])
            errors.extend(pkg_errors)
            warnings.extend(pkg_warnings)
        
        # Security validation (always runs)
        security_warnings = self._validate_engine_name(engine_name)
        warnings.extend(security_warnings)
        
        return {
            'can_generate': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_database(self, db_requirements: Dict) -> List[str]:
        """Check if required database tables/columns exist."""
        errors = []
        # TODO: Connect to actual database and check schema
        # For now, just check if database file exists
        if db_requirements.get('required') and not Path('security/users.db').exists():
            errors.append("Database not initialized")
        return errors
    
    def _validate_apis(self, api_requirements: List[str]) -> Tuple[List[str], List[str]]:
        """Check if required APIs are configured."""
        errors = []
        warnings = []
        
        env_vars = {
            'openai': 'OPENAI_API_KEY',
            'azure': 'AZURE_OPENAI_KEY',
            'github': 'GITHUB_TOKEN',
            'google_maps': 'GOOGLE_MAPS_API_KEY',
            'twilio': 'TWILIO_AUTH_TOKEN'
        }
        
        for api in api_requirements:
            env_var = env_vars.get(api.lower())
            if env_var and not os.getenv(env_var):
                warnings.append(f"API {api} not configured ({env_var} missing)")
        
        return errors, warnings
    
    def _validate_config(self, config_requirements: List[str]) -> List[str]:
        """Check if required configuration exists."""
        errors = []
        for config_key in config_requirements:
            if not os.getenv(config_key):
                errors.append(f"Required config missing: {config_key}")
        return errors
    
    def _validate_packages(self, packages: List[str]) -> Tuple[List[str], List[str]]:
        """Check if required Python packages are installed."""
        errors = []
        warnings = []
        
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                warnings.append(f"Package '{package}' not installed - feature may not work")
        
        return errors, warnings
    
    def _validate_engine_name(self, engine_name: str) -> List[str]:
        """Check for suspicious patterns in engine names."""
        warnings = []
        
        # Check for path traversal attempts
        if '..' in engine_name or '/' in engine_name or '\\' in engine_name:
            warnings.append(f"Suspicious path characters in engine name: {engine_name}")
        
        # Check for dangerous keywords
        dangerous = ['eval', 'exec', 'compile', '__import__', 'subprocess', 'os.system']
        if any(danger in engine_name.lower() for danger in dangerous):
            warnings.append(f"Engine name contains potentially dangerous keyword")
        
        return warnings
    
    def _check_dependency(self, dep_type: str, dep_name: str) -> bool:
        """Check if a dependency is satisfied."""
        if dep_type == 'package':
            try:
                __import__(dep_name)
                return True
            except ImportError:
                return False
        elif dep_type == 'api':
            # Check for API key
            env_mappings = {
                'openai': 'OPENAI_API_KEY',
                'github': 'GITHUB_TOKEN'
            }
            return bool(os.getenv(env_mappings.get(dep_name, f"{dep_name.upper()}_API_KEY")))
        elif dep_type == 'config':
            return bool(os.getenv(dep_name))
        return False
    
    def _load_security_patterns(self) -> Dict:
        """Load security validation patterns."""
        return {
            'sql_injection': [
                r'execute\s*\([^?]',  # Raw execute without params
                r'f".*SELECT.*{',      # F-string in SQL
                r'%s.*SELECT',         # String formatting in SQL
            ],
            'xss': [
                r'render_template_string\(',
                r'\.innerHTML\s*=',
                r'document\.write\(',
            ],
            'unsafe_imports': [
                'pickle', 'marshal', 'shelve', 'eval', 'exec',
                'compile', '__import__', 'subprocess', 'os.system'
            ]
        }
    
    def validate_generated_code(self, code: str, engine_name: str) -> Dict:
        """Validate generated code for security issues."""
        issues = []
        
        # Parse AST for security analysis
        try:
            tree = ast.parse(code)
            
            # Check for dangerous imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in self.security_patterns['unsafe_imports']:
                            issues.append(f"Unsafe import: {alias.name}")
                
                # Check for eval/exec
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec', 'compile']:
                            issues.append(f"Dangerous function call: {node.func.id}")
        
        except SyntaxError as e:
            issues.append(f"Syntax error in generated code: {e}")
        
        # Check regex patterns
        for pattern_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                if re.search(pattern, code):
                    issues.append(f"Potential {pattern_type} vulnerability detected")
        
        # Record validation
        self.registry.validate_feature(
            engine_name.replace('_engine', ''),
            'security_scan',
            len(issues) == 0,
            f"Found {len(issues)} security issues" if issues else "No security issues"
        )
        
        return {
            'safe': len(issues) == 0,
            'issues': issues
        }
    
    def _generate_engine(self, engine_name: str, feature_type: str):
        """Override to add security validation."""
        # Generate code using parent method
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
        
        # Validate security
        validation = self.validate_generated_code(code, engine_name)
        if not validation['safe']:
            print(f"⚠️  Security issues in generated {engine_name}:")
            for issue in validation['issues']:
                print(f"   - {issue}")
        
        # Write file
        engine_file = self.engines_dir / f"{engine_name}.py"
        with open(engine_file, 'w') as f:
            f.write(code)
        
        print(f"✓ Generated {engine_file} (type: {feature_type})")
        self._log_generation(engine_name, feature_type)


# Global validated generator
_validated_generator = None

def get_validated_generator() -> ValidatedEngineGenerator:
    """Get or create the global validated generator."""
    global _validated_generator
    if _validated_generator is None:
        _validated_generator = ValidatedEngineGenerator()
    return _validated_generator
