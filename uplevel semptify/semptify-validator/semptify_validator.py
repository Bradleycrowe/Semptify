"""
Semptify Link Validation Engine
Comprehensive validator for all routes, templates, and API endpoints
"""
import requests
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import sys

class SemptifyValidator:
    def __init__(self, base_url='http://127.0.0.1:5000', semptify_path='C:/Semptify/Semptify'):
        self.base_url = base_url
        self.semptify_path = Path(semptify_path)
        self.results = {
            'routes': {},
            'templates': {},
            'broken_links': [],
            'working_links': [],
            'api_endpoints': {},
            'summary': {}
        }
    
    def discover_routes_from_code(self) -> Set[str]:
        """Extract all @route decorators from Python files"""
        routes = set()
        for py_file in self.semptify_path.glob('*_routes.py'):
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            # Match @blueprint.route('/path') or @app.route('/path')
            matches = re.findall(r"@\w+\.route\(['\"]([^'\"]+)['\"]", content)
            routes.update(matches)
        
        # Also check main app file
        main_file = self.semptify_path / 'Semptify.py'
        if main_file.exists():
            content = main_file.read_text(encoding='utf-8', errors='ignore')
            matches = re.findall(r"@app\.route\(['\"]([^'\"]+)['\"]", content)
            routes.update(matches)
        
        return routes
    
    def discover_links_from_templates(self) -> Set[str]:
        """Extract all href links from HTML templates"""
        links = set()
        templates_dir = self.semptify_path / 'templates'
        if templates_dir.exists():
            for html_file in templates_dir.rglob('*.html'):
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                # Match href="/path" or href="{{ url_for('...') }}"
                href_matches = re.findall(r'href=["\']([^"\']+)["\']', content)
                for match in href_matches:
                    if not match.startswith('http') and not match.startswith('#') and not match.startswith('{{'):
                        links.add(match)
        return links
    
    def test_endpoint(self, path: str) -> Tuple[int, str]:
        """Test a single endpoint"""
        try:
            url = urljoin(self.base_url, path)
            response = requests.get(url, timeout=5, allow_redirects=False)
            return response.status_code, response.reason
        except requests.exceptions.RequestException as e:
            return 0, str(e)
    
    def crawl_page(self, path: str) -> List[str]:
        """Crawl a page and extract all internal links"""
        try:
            url = urljoin(self.base_url, path)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('/') and not href.startswith('//'):
                        links.append(href)
                return links
        except Exception as e:
            print(f"Error crawling {path}: {e}")
        return []
    
    def validate_all(self) -> Dict:
        """Run complete validation"""
        print("[SEARCH] Semptify Validator - Starting comprehensive check\\n")
        
        # 1. Discover routes from code
        print("[FILES] Discovering routes from Python files...")
        code_routes = self.discover_routes_from_code()
        print(f"   Found {len(code_routes)} routes in code\\n")
        
        # 2. Discover links from templates
        print("[TEMPLATES] Discovering links from templates...")
        template_links = self.discover_links_from_templates()
        print(f"   Found {len(template_links)} links in templates\\n")
        
        # 3. Test all discovered routes
        print("[TEST] Testing all routes...")
        all_paths = code_routes.union(template_links)
        for path in sorted(all_paths):
            status, reason = self.test_endpoint(path)
            self.results['routes'][path] = {
                'status': status,
                'reason': reason,
                'working': status in [200, 302]
            }
            icon = "[OK]" if status in [200, 302] else "[FAIL]"
            print(f"   {icon} {path:50} → {status} {reason}")
            
            if status in [200, 302]:
                self.results['working_links'].append(path)
            else:
                self.results['broken_links'].append(path)
        
        # 4. Test common API endpoints
        print("\\n[API] Testing API endpoints...")
        api_paths = [
            '/api/copilot',
            '/api/complaint/identify-venues',
            '/api/context/patterns',
            '/api/timeline/events',
            '/api/ollama/models',
            '/metrics',
            '/readyz'
        ]
        for path in api_paths:
            status, reason = self.test_endpoint(path)
            self.results['api_endpoints'][path] = {
                'status': status,
                'reason': reason
            }
            icon = "[OK]" if status in [200, 302, 401, 405] else "[FAIL]"  # 401/405 expected for some
            print(f"   {icon} {path:40} → {status} {reason}")
        
        # 5. Generate summary
        total = len(self.results['routes'])
        working = len(self.results['working_links'])
        broken = len(self.results['broken_links'])
        
        self.results['summary'] = {
            'total_routes': total,
            'working': working,
            'broken': broken,
            'success_rate': f"{(working/total*100):.1f}%" if total > 0 else "N/A"
        }
        
        print("\\n" + "="*70)
        print("[SUMMARY] VALIDATION SUMMARY")
        print("="*70)
        print(f"Total Routes:  {total}")
        print(f"[OK] Working:     {working}")
        print(f"[FAIL] Broken:      {broken}")
        print(f"Success Rate:  {self.results['summary']['success_rate']}")
        print("="*70)
        
        # Save results
        output_file = Path('validation_report.json')
        output_file.write_text(json.dumps(self.results, indent=2))
        print(f"\\n[SAVE] Full report saved to: {output_file.absolute()}")
        
        return self.results

if __name__ == '__main__':
    validator = SemptifyValidator()
    results = validator.validate_all()
    
    # Exit with error code if broken links found
    sys.exit(0 if len(results['broken_links']) == 0 else 1)
