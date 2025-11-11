"""
Route Testing Script
Tests all possible navigation paths from homepage on Render
Reports broken routes and navigation issues
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

# Base URL - change to your Render URL
BASE_URL = "https://semptify.onrender.com"  # Update with your actual Render URL
# For local testing:
# BASE_URL = "http://localhost:5000"

visited_urls = set()
broken_routes = []
working_routes = []
routes_with_errors = []

def extract_links(html_content, current_url):
    """Extract all clickable links from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    # Find all <a> tags with href
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        
        # Skip external links, anchors, javascript
        if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
            continue
            
        # Convert relative URLs to absolute
        full_url = urljoin(current_url, href)
        
        # Only include links from same domain
        if urlparse(full_url).netloc == urlparse(BASE_URL).netloc or not urlparse(full_url).netloc:
            links.append(full_url)
    
    # Find forms and their actions
    for form in soup.find_all('form'):
        action = form.get('action', '')
        if action and not action.startswith('#'):
            full_url = urljoin(current_url, action)
            if urlparse(full_url).netloc == urlparse(BASE_URL).netloc or not urlparse(full_url).netloc:
                links.append(full_url)
    
    return list(set(links))

def test_route(url, method='GET', follow_redirects=True):
    """Test a single route and return status"""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10, allow_redirects=follow_redirects)
        else:
            response = requests.post(url, timeout=10, allow_redirects=follow_redirects)
        
        return {
            'url': url,
            'status_code': response.status_code,
            'success': 200 <= response.status_code < 400,
            'redirect': response.history if response.history else None,
            'content_type': response.headers.get('Content-Type', ''),
            'content': response.text if response.status_code == 200 else None
        }
    except requests.exceptions.Timeout:
        return {
            'url': url,
            'status_code': 'TIMEOUT',
            'success': False,
            'error': 'Request timeout after 10 seconds'
        }
    except requests.exceptions.ConnectionError:
        return {
            'url': url,
            'status_code': 'CONNECTION_ERROR',
            'success': False,
            'error': 'Could not connect to server'
        }
    except Exception as e:
        return {
            'url': url,
            'status_code': 'ERROR',
            'success': False,
            'error': str(e)
        }

def crawl_from_homepage(start_url, max_depth=3):
    """Recursively crawl all routes starting from homepage"""
    queue = [(start_url, 0)]  # (url, depth)
    
    while queue:
        current_url, depth = queue.pop(0)
        
        # Skip if already visited or max depth reached
        if current_url in visited_urls or depth > max_depth:
            continue
        
        print(f"\n{'  ' * depth}🔍 Testing: {current_url} (depth {depth})")
        visited_urls.add(current_url)
        
        # Test the route
        result = test_route(current_url)
        
        if result['success']:
            working_routes.append(result)
            print(f"{'  ' * depth}✅ Status {result['status_code']} - OK")
            
            # Extract links if HTML response
            if result.get('content') and 'text/html' in result.get('content_type', ''):
                links = extract_links(result['content'], current_url)
                print(f"{'  ' * depth}   Found {len(links)} links")
                
                # Add new links to queue
                for link in links:
                    if link not in visited_urls:
                        queue.append((link, depth + 1))
        else:
            if result['status_code'] == 404:
                broken_routes.append(result)
                print(f"{'  ' * depth}❌ 404 NOT FOUND")
            elif result['status_code'] in [401, 403]:
                print(f"{'  ' * depth}🔒 {result['status_code']} AUTH REQUIRED")
                working_routes.append(result)  # Not broken, just protected
            elif result['status_code'] == 500:
                routes_with_errors.append(result)
                print(f"{'  ' * depth}💥 500 SERVER ERROR")
            else:
                routes_with_errors.append(result)
                print(f"{'  ' * depth}⚠️  {result['status_code']} - {result.get('error', 'Unknown error')}")
        
        # Be nice to the server
        time.sleep(0.5)

def test_known_routes():
    """Test all known routes from Semptify.py"""
    known_routes = [
        '/',
        '/register',
        '/login',
        '/signin',
        '/verify',
        '/dashboard',
        '/dashboard-grid',
        '/recover',
        '/vault',
        '/vault/upload',
        '/vault/download',
        '/notary',
        '/certified_post',
        '/court_clerk',
        '/calendar-timeline',
        '/calendar-timeline-horizontal',
        '/timeline-simple',
        '/timeline',
        '/timeline-ruler',
        '/ledger-calendar',
        '/calendar-widgets',
        '/learning-dashboard',
        '/resources',
        '/resources/witness_statement',
        '/resources/filing_packet',
        '/resources/service_animal',
        '/resources/move_checklist',
        '/library',
        '/tools',
        '/tools/complaint-generator',
        '/tools/statute-calculator',
        '/tools/court-packet',
        '/tools/rights-explorer',
        '/know-your-rights',
        '/evidence/gallery',
        '/settings',
        '/help',
        '/office',
        '/about',
        '/privacy',
        '/terms',
        '/faq',
        '/how-it-works',
        '/features',
        '/get-started',
        '/admin',
        '/metrics',
        '/health',
        '/healthz',
        '/readyz',
    ]
    
    print("\n" + "="*70)
    print("TESTING ALL KNOWN ROUTES")
    print("="*70)
    
    for route in known_routes:
        url = BASE_URL + route
        if url not in visited_urls:
            result = test_route(url)
            visited_urls.add(url)
            
            if result['success']:
                working_routes.append(result)
                print(f"✅ {route} - Status {result['status_code']}")
            elif result['status_code'] == 404:
                broken_routes.append(result)
                print(f"❌ {route} - 404 NOT FOUND")
            elif result['status_code'] in [401, 403]:
                working_routes.append(result)
                print(f"🔒 {route} - Status {result['status_code']} (AUTH REQUIRED)")
            else:
                routes_with_errors.append(result)
                print(f"⚠️  {route} - Status {result['status_code']}")
            
            time.sleep(0.3)

def generate_report():
    """Generate final test report"""
    print("\n" + "="*70)
    print("ROUTE TESTING REPORT")
    print("="*70)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Routes Tested: {len(visited_urls)}")
    print(f"   ✅ Working Routes: {len(working_routes)}")
    print(f"   ❌ Broken Routes (404): {len(broken_routes)}")
    print(f"   💥 Routes with Errors (500): {len(routes_with_errors)}")
    
    if broken_routes:
        print(f"\n❌ BROKEN ROUTES (404):")
        for route in broken_routes:
            print(f"   • {route['url']}")
    
    if routes_with_errors:
        print(f"\n💥 ROUTES WITH ERRORS:")
        for route in routes_with_errors:
            print(f"   • {route['url']} - {route['status_code']}")
            if 'error' in route:
                print(f"     Error: {route['error']}")
    
    # Save detailed report to JSON
    report = {
        'base_url': BASE_URL,
        'total_tested': len(visited_urls),
        'working_routes': len(working_routes),
        'broken_routes': len(broken_routes),
        'routes_with_errors': len(routes_with_errors),
        'all_tested_urls': list(visited_urls),
        'broken_details': broken_routes,
        'error_details': routes_with_errors
    }
    
    with open('route_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: route_test_report.json")
    
    # Return exit code
    return 1 if (broken_routes or routes_with_errors) else 0

def main():
    """Main test runner"""
    print("="*70)
    print("SEMPTIFY ROUTE TESTING TOOL")
    print("="*70)
    print(f"Testing base URL: {BASE_URL}")
    print("="*70)
    
    # Test 1: Crawl from homepage
    print("\n[1/2] Crawling from homepage...")
    crawl_from_homepage(BASE_URL, max_depth=2)
    
    # Test 2: Test all known routes
    print("\n[2/2] Testing all known routes...")
    test_known_routes()
    
    # Generate report
    exit_code = generate_report()
    
    return exit_code

if __name__ == '__main__':
    import sys
    
    # Allow command line argument for base URL
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1].rstrip('/')
    
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        generate_report()
        sys.exit(1)
