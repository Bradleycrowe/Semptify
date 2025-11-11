"""Test Ollama AI integration"""
import requests
import json

print("🤖 Testing Ollama AI Integration\n")

# Test 1: Direct Ollama API
print("1️⃣ Testing direct Ollama connection...")
try:
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "llama3.2",
            "prompt": "What are tenant rights in Minnesota? Respond in 2 sentences.",
            "stream": False
        },
        timeout=30
    )
    
    if response.status_code == 200:
        ai_response = response.json().get('response', '')
        print(f"✅ Ollama is working!\n")
        print(f"Response: {ai_response[:200]}...\n")
    else:
        print(f"❌ Ollama returned status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Ollama is not running. Start it with: ollama serve")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: Semptify /api/copilot endpoint
print("\n2️⃣ Testing Semptify /api/copilot endpoint...")
print("Starting Flask app in test mode...\n")

try:
    import Semptify as sempt
    sempt.app.config['TESTING'] = True
    client = sempt.app.test_client()
    
    # Test with legal question
    test_prompt = "My landlord is trying to evict me with only 7 days notice in Minnesota. Is this legal?"
    
    copilot_response = client.post('/api/copilot', 
        data=json.dumps({'prompt': test_prompt}),
        content_type='application/json'
    )
    
    if copilot_response.status_code == 200:
        data = copilot_response.get_json()
        print(f"✅ /api/copilot works!\n")
        print(f"Model: {data.get('model')}")
        print(f"Provider: {data.get('provider')}")
        print(f"Cost: ${data.get('cost', 0)}\n")
        print(f"AI Response:\n{data.get('response', 'No response')[:300]}...\n")
    else:
        print(f"❌ Endpoint returned status {copilot_response.status_code}")
        print(copilot_response.get_json())
        
except Exception as e:
    print(f"❌ Error testing endpoint: {e}")
    import traceback
    traceback.print_exc()

print("\n✨ Test complete!")
print("\n💡 Usage in frontend:")
print("""
fetch('/api/copilot', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        prompt: 'How do I respond to an eviction notice?'
    })
})
.then(r => r.json())
.then(data => console.log(data.response));
""")
