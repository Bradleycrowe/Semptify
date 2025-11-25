"""Quick test for AI Copilot route"""
import requests
import json

# Test if server is running
try:
    response = requests.get("http://localhost:8080/", timeout=2)
    print(f"✅ Server is running (status: {response.status_code})")
except:
    print("❌ Server not running. Start with: python run_prod.py")
    exit(1)

# Test AI Copilot route
print("\n🤖 Testing AI Copilot route...")
try:
    test_payload = {
        "messages": [{"role": "user", "content": "Hello, test message"}],
        "provider": "test"
    }
    
    response = requests.post(
        "http://localhost:8080/api/copilot",
        json=test_payload,
        timeout=5
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ AI Copilot route is working!")
        print(f"Response: {response.text[:200]}")
    elif response.status_code == 404:
        print("⚠️  Route not found - needs to be created")
    else:
        print(f"⚠️  Unexpected response: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("⚠️  Request timed out - route may be processing")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
