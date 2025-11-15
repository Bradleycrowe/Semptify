"""
CLI for explicit feature scaffolding
Usage: python scaffold.py feature_name --type=search
"""
import argparse
import sys
from pathlib import Path
from validated_engine_generator import get_validated_generator
from feature_registry import get_feature_registry, FeatureStatus

def main():
    parser = argparse.ArgumentParser(description='Scaffold a new Semptify feature')
    parser.add_argument('name', help='Feature name (e.g., attorney_finder)')
    parser.add_argument('--type', choices=['search', 'calculator', 'form', 'validator', 'generator', 'generic'],
                       default='generic', help='Feature type')
    parser.add_argument('--require-db', action='store_true', help='Feature requires database')
    parser.add_argument('--require-api', nargs='+', help='Required APIs (e.g., openai github)')
    parser.add_argument('--require-packages', nargs='+', help='Required Python packages')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    
    args = parser.parse_args()
    
    print(f"🔧 Scaffolding feature: {args.name} (type: {args.type})")
    
    # Build requirements dict
    requirements = {}
    if args.require_db:
        requirements['database'] = {'required': True}
    if args.require_api:
        requirements['apis'] = args.require_api
    if args.require_packages:
        requirements['packages'] = args.require_packages
    
    # Validate and generate
    generator = get_validated_generator()
    engine_name = f"{args.name}_engine"
    
    try:
        # Check if exists
        engine_path = Path(f"generated/engines/{engine_name}.py")
        if engine_path.exists() and not args.force:
            print(f"❌ Engine already exists: {engine_path}")
            print("   Use --force to overwrite")
            return 1
        
        # Validate requirements
        validation = generator.validate_requirements(engine_name, requirements)
        
        if not validation['can_generate']:
            print("❌ Cannot generate feature due to missing requirements:")
            for error in validation['errors']:
                print(f"   - {error}")
            return 1
        
        if validation['warnings']:
            print("⚠️  Warnings:")
            for warning in validation['warnings']:
                print(f"   - {warning}")
        
        # Generate the feature
        generator._generate_engine(engine_name, args.type)
        
        # Generate route file
        route_code = f'''from flask import Blueprint, render_template, request, jsonify
from generated.engines.{engine_name} import {args.name}_logic

{args.name}_bp = Blueprint('{args.name}', __name__)

@{args.name}_bp.route('/{args.name}')
def {args.name}_page():
    return render_template('{args.name}.html')

@{args.name}_bp.route('/api/{args.name}', methods=['POST'])
def {args.name}_api():
    data = request.get_json()
    result = {args.name}_logic(data)
    return jsonify(result)
'''
        route_path = Path(f"generated/routes/{args.name}_routes.py")
        with open(route_path, 'w') as f:
            f.write(route_code)
        print(f"✓ Created route: {route_path}")
        
        # Register in feature registry
        registry = get_feature_registry()
        registry.register_feature(
            args.name,
            args.type,
            status=FeatureStatus.DEVELOPMENT,
            engine_path=str(engine_path),
            blueprint_path=str(route_path),
            requires_config=requirements
        )
        
        print(f"\n✅ Feature '{args.name}' scaffolded successfully!")
        print(f"\nNext steps:")
        print(f"1. Implement business logic in: generated/engines/{engine_name}.py")
        print(f"2. Create template: templates/{args.name}.html")
        print(f"3. Register blueprint in Semptify.py:")
        print(f"   from generated.routes.{args.name}_routes import {args.name}_bp")
        print(f"   app.register_blueprint({args.name}_bp)")
        print(f"4. Write tests in: tests/test_{args.name}.py")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
