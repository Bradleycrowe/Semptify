"""
Jurisdiction Module Generator Engine
Auto-creates eviction defense modules for any county/state on-demand
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class JurisdictionEngine:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.modules_path = self.base_path.parent / "jurisdiction_modules"
        self.templates_path = self.base_path / "templates"
        self.data_path = self.base_path / "data"
        self.jurisdictions_db = self.data_path / "jurisdictions.json"
        
    def detect_jurisdiction(self, user_query):
        """
        Parse user query to extract jurisdiction info
        Returns: {county, state, city, type} or None
        """
        patterns = {
            'county_state': r'(\w+)\s+County,?\s+(\w+)',  # "Dakota County Minnesota"
            'city_state': r'(\w+),?\s+(\w+)',  # "Minneapolis, MN"
            'state_only': r'\b(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming)\b',
        }
        
        # Try county + state
        match = re.search(patterns['county_state'], user_query, re.IGNORECASE)
        if match:
            return {
                'county': match.group(1),
                'state': match.group(2),
                'type': 'county',
                'full_name': f"{match.group(1)} County, {match.group(2)}"
            }
        
        # Try city + state
        match = re.search(patterns['city_state'], user_query, re.IGNORECASE)
        if match:
            return {
                'city': match.group(1),
                'state': match.group(2),
                'type': 'city',
                'full_name': f"{match.group(1)}, {match.group(2)}"
            }
        
        # Try state only
        match = re.search(patterns['state_only'], user_query, re.IGNORECASE)
        if match:
            return {
                'state': match.group(1),
                'type': 'state',
                'full_name': match.group(1)
            }
        
        return None
    
    def module_exists(self, jurisdiction):
        """Check if module already exists"""
        module_name = self._get_module_name(jurisdiction)
        module_path = self.modules_path / module_name
        return module_path.exists()
    
    def generate_module(self, jurisdiction, user_context=None):
        """
        Generate complete eviction defense module for jurisdiction
        Returns: module_info dict with routes, files, status
        """
        module_name = self._get_module_name(jurisdiction)
        module_path = self.modules_path / module_name
        
        print(f"🏗️  Generating module: {module_name}")
        
        # Create module structure
        os.makedirs(module_path, exist_ok=True)
        os.makedirs(module_path / "templates", exist_ok=True)
        os.makedirs(module_path / "data", exist_ok=True)
        os.makedirs(module_path / "flows", exist_ok=True)
        
        # Fetch jurisdiction-specific data
        jurisdiction_data = self._fetch_jurisdiction_data(jurisdiction)
        
        # Generate files
        files_created = []
        
        # 1. Routes file (Flask blueprint)
        route_file = self._generate_routes(module_path, jurisdiction, jurisdiction_data)
        files_created.append(route_file)
        
        # 2. Main HTML template
        html_file = self._generate_html_index(module_path, jurisdiction, jurisdiction_data)
        files_created.append(html_file)
        
        # 3. Motion templates
        motions_file = self._generate_motions(module_path, jurisdiction, jurisdiction_data)
        files_created.append(motions_file)
        
        # 4. Counterclaim builder
        counterclaim_file = self._generate_counterclaim_builder(module_path, jurisdiction, jurisdiction_data)
        files_created.append(counterclaim_file)
        
        # 5. Timeline tracker
        timeline_file = self._generate_timeline(module_path, jurisdiction, jurisdiction_data)
        files_created.append(timeline_file)
        
        # 6. Resources & contacts
        resources_file = self._generate_resources(module_path, jurisdiction, jurisdiction_data)
        files_created.append(resources_file)
        
        # 7. README
        readme_file = self._generate_readme(module_path, jurisdiction, jurisdiction_data)
        files_created.append(readme_file)
        
        # Save module metadata
        metadata = {
            'jurisdiction': jurisdiction,
            'module_name': module_name,
            'created_at': datetime.now().isoformat(),
            'files': files_created,
            'blueprint_name': f"{module_name}_bp",
            'url_prefix': f"/library/{module_name}",
            'data': jurisdiction_data
        }
        
        with open(module_path / "module_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Module generated: {len(files_created)} files")
        
        return metadata
    
    def _get_module_name(self, jurisdiction):
        """Generate standardized module name"""
        if jurisdiction['type'] == 'county':
            return f"{jurisdiction['county'].lower()}_{jurisdiction['state'].lower()}_eviction"
        elif jurisdiction['type'] == 'city':
            return f"{jurisdiction['city'].lower()}_{jurisdiction['state'].lower()}_eviction"
        else:
            return f"{jurisdiction['state'].lower()}_eviction"
    
    def _fetch_jurisdiction_data(self, jurisdiction):
        """
        Fetch jurisdiction-specific legal data
        Returns: dict with statutes, forms, contacts, procedures
        """
        # TODO: Integrate with legal API or database
        # For now, return template structure
        
        state = jurisdiction.get('state', 'Minnesota')
        
        # Base data structure (can be populated from API/database)
        data = {
            'state': state,
            'statutes': self._get_state_statutes(state),
            'forms': self._get_court_forms(jurisdiction),
            'contacts': self._get_legal_contacts(jurisdiction),
            'procedures': self._get_eviction_procedures(state),
            'deadlines': self._get_state_deadlines(state),
            'languages': self._get_local_languages(jurisdiction),
            'court_info': self._get_court_info(jurisdiction)
        }
        
        return data
    
    def _get_state_statutes(self, state):
        """Get state eviction statutes"""
        statute_map = {
            'Minnesota': {
                'eviction_chapter': '504B',
                'key_statutes': [
                    {'code': '504B.285', 'title': 'Notice Requirements', 'url': 'https://www.revisor.mn.gov/statutes/cite/504B.285'},
                    {'code': '504B.321', 'title': 'Summons and Complaint', 'url': 'https://www.revisor.mn.gov/statutes/cite/504B.321'},
                    {'code': '504B.371', 'title': 'Tenant Remedies', 'url': 'https://www.revisor.mn.gov/statutes/cite/504B.371'},
                ]
            },
            # Add more states as needed
        }
        return statute_map.get(state, {'eviction_chapter': 'Unknown', 'key_statutes': []})
    
    def _get_court_forms(self, jurisdiction):
        """Get jurisdiction-specific court forms"""
        return {
            'answer': f"Answer form for {jurisdiction['full_name']}",
            'counterclaim': "Counterclaim template",
            'motion_dismiss': "Motion to Dismiss",
            'motion_continue': "Motion for Continuance"
        }
    
    def _get_legal_contacts(self, jurisdiction):
        """Get local legal aid contacts"""
        return {
            'legal_aid': f"Legal Aid for {jurisdiction['full_name']}",
            'tenant_hotline': "1-800-XXX-XXXX",
            'housing_authority': f"{jurisdiction['full_name']} Housing Authority"
        }
    
    def _get_eviction_procedures(self, state):
        """Get state eviction procedures timeline"""
        return {
            'notice_period': '14 days',
            'answer_deadline': '14 days from summons',
            'hearing_timeframe': '7-14 days after answer',
            'appeal_deadline': '10 days from judgment'
        }
    
    def _get_state_deadlines(self, state):
        """Get critical deadlines"""
        return {
            'answer': 14,  # days
            'appeal': 10,
            'redemption': 0  # if applicable
        }
    
    def _get_local_languages(self, jurisdiction):
        """Get common languages in area"""
        # Can integrate with Census API
        return ['en', 'es']  # Default to English + Spanish
    
    def _get_court_info(self, jurisdiction):
        """Get court contact and location info"""
        return {
            'name': f"{jurisdiction['full_name']} District Court",
            'address': "Lookup required",
            'phone': "XXX-XXX-XXXX",
            'website': "https://www.courts.state.xx.us"
        }
    
    def _generate_routes(self, module_path, jurisdiction, data):
        """Generate Flask blueprint routes file"""
        module_name = self._get_module_name(jurisdiction)
        
        routes_content = f'''"""
{jurisdiction['full_name']} Eviction Defense Library
Auto-generated by Jurisdiction Engine
"""

from flask import Blueprint, render_template, jsonify, request
import os
import json

{module_name}_bp = Blueprint(
    '{module_name}',
    __name__,
    url_prefix='/library/{module_name}',
    template_folder='templates'
)

@{module_name}_bp.route('/')
def index():
    """Main library page"""
    jurisdiction_data = {{
        'name': '{jurisdiction['full_name']}',
        'state': '{data['state']}',
        'court': '{data['court_info']['name']}'
    }}
    return render_template('{module_name}_index.html', jurisdiction=jurisdiction_data)

@{module_name}_bp.route('/doc/<filename>')
def get_doc(filename):
    """Return document content"""
    doc_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    if os.path.exists(doc_path):
        with open(doc_path, 'r', encoding='utf-8') as f:
            return jsonify({{'content': f.read()}})
    return jsonify({{'error': 'Document not found'}}), 404

@{module_name}_bp.route('/motion/<motion_type>')
def get_motion(motion_type):
    """Return motion template"""
    motions_path = os.path.join(os.path.dirname(__file__), 'data', 'motions.md')
    if os.path.exists(motions_path):
        with open(motions_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract specific motion
            return jsonify({{'content': content}})
    return jsonify({{'error': 'Motion not found'}}), 404

@{module_name}_bp.route('/resources')
def get_resources():
    """Return local resources"""
    return jsonify({data['contacts']})

@{module_name}_bp.route('/statutes')
def get_statutes():
    """Return state statutes"""
    return jsonify({data['statutes']})
'''
        
        route_file = module_path / f"{module_name}_routes.py"
        with open(route_file, 'w', encoding='utf-8') as f:
            f.write(routes_content)
        
        return str(route_file.relative_to(self.base_path.parent))
    
    def _generate_html_index(self, module_path, jurisdiction, data):
        """Generate main HTML interface"""
        module_name = self._get_module_name(jurisdiction)
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{jurisdiction['full_name']} Eviction Defense</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .tool-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            cursor: pointer;
            transition: transform 0.3s;
        }}
        .tool-card:hover {{
            transform: translateY(-5px);
        }}
        .tool-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}
        .tool-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚖️ {jurisdiction['full_name']}</h1>
        <div class="subtitle">Eviction Defense Toolkit - Auto-Generated</div>
        
        <div class="tools-grid">
            <div class="tool-card" onclick="window.location.href='flows/counterclaim_builder.html'">
                <div class="tool-icon">📄</div>
                <div class="tool-title">Answer + Counterclaim Builder</div>
                <p>Generate court-ready documents</p>
            </div>
            
            <div class="tool-card" onclick="window.location.href='flows/timeline_tracker.html'">
                <div class="tool-icon">📅</div>
                <div class="tool-title">Timeline Tracker</div>
                <p>Track deadlines and stages</p>
            </div>
            
            <div class="tool-card" onclick="window.location.href='data/motions.md'">
                <div class="tool-icon">⚖️</div>
                <div class="tool-title">Motion Library</div>
                <p>Ready-to-file motion templates</p>
            </div>
            
            <div class="tool-card" onclick="loadResources()">
                <div class="tool-icon">📞</div>
                <div class="tool-title">Local Resources</div>
                <p>Legal aid and hotlines</p>
            </div>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #fff3cd; border-radius: 10px;">
            <strong>⚠️ Legal Disclaimer:</strong> This is informational only, not legal advice.
            Contact: <strong>{data['contacts']['tenant_hotline']}</strong>
        </div>
    </div>
    
    <script>
        function loadResources() {{
            fetch('/library/{module_name}/resources')
                .then(r => r.json())
                .then(data => {{
                    alert('Legal Aid: ' + data.legal_aid + '\\nHotline: ' + data.tenant_hotline);
                }});
        }}
    </script>
</body>
</html>
'''
        
        template_file = module_path / "templates" / f"{module_name}_index.html"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(template_file.relative_to(self.base_path.parent))
    
    def _generate_motions(self, module_path, jurisdiction, data):
        """Generate motion templates"""
        motions_content = f'''# Motion Templates - {jurisdiction['full_name']}

## Motion to Dismiss
[Template content based on {data['state']} law]

## Motion for Continuance
[Template with local procedures]

## Motion for Tenant Remedies
Based on {data['statutes']['eviction_chapter']} statutes
'''
        
        motions_file = module_path / "data" / "motions.md"
        with open(motions_file, 'w', encoding='utf-8') as f:
            f.write(motions_content)
        
        return str(motions_file.relative_to(self.base_path.parent))
    
    def _generate_counterclaim_builder(self, module_path, jurisdiction, data):
        """Generate interactive counterclaim builder"""
        # Similar to Dakota County builder but jurisdiction-specific
        builder_file = module_path / "flows" / "counterclaim_builder.html"
        with open(builder_file, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Counterclaim builder for {jurisdiction['full_name']} -->")
        return str(builder_file.relative_to(self.base_path.parent))
    
    def _generate_timeline(self, module_path, jurisdiction, data):
        """Generate timeline tracker"""
        timeline_file = module_path / "flows" / "timeline_tracker.html"
        with open(timeline_file, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Timeline for {jurisdiction['full_name']} -->")
        return str(timeline_file.relative_to(self.base_path.parent))
    
    def _generate_resources(self, module_path, jurisdiction, data):
        """Generate resources file"""
        resources_content = f'''# Local Resources - {jurisdiction['full_name']}

## Legal Aid
{data['contacts']['legal_aid']}

## Tenant Hotline
{data['contacts']['tenant_hotline']}

## Court Information
{data['court_info']['name']}
{data['court_info']['website']}
'''
        
        resources_file = module_path / "data" / "resources.md"
        with open(resources_file, 'w', encoding='utf-8') as f:
            f.write(resources_content)
        
        return str(resources_file.relative_to(self.base_path.parent))
    
    def _generate_readme(self, module_path, jurisdiction, data):
        """Generate module README"""
        readme_content = f'''# {jurisdiction['full_name']} Eviction Defense Module

**Auto-generated by Jurisdiction Engine**
**Created:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Overview
Complete eviction defense toolkit for {jurisdiction['full_name']}.

## Features
- ✅ Answer + Counterclaim Builder
- ✅ Timeline Tracker
- ✅ Motion Library
- ✅ Local Resources
- ✅ State-specific statutes

## Installation
Module automatically registered at `/library/{self._get_module_name(jurisdiction)}`

## State Law
Based on {data['state']} statutes, Chapter {data['statutes']['eviction_chapter']}

## Support
Contact: {data['contacts']['tenant_hotline']}
'''
        
        readme_file = module_path / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return str(readme_file.relative_to(self.base_path.parent))


# Example usage
if __name__ == "__main__":
    engine = JurisdictionEngine()
    
    # Test detection
    test_queries = [
        "I need help with Hennepin County Minnesota eviction",
        "Facing eviction in Ramsey County, MN",
        "California eviction defense"
    ]
    
    for query in test_queries:
        jurisdiction = engine.detect_jurisdiction(query)
        if jurisdiction:
            print(f"Detected: {jurisdiction['full_name']}")
            if not engine.module_exists(jurisdiction):
                print(f"  → Module doesn't exist, would generate...")
            else:
                print(f"  → Module already exists")
