import json
import requests

BASE = "http://127.0.0.1:5000"

print("Listing sources...")
r = requests.get(f"{BASE}/api/ollama/sources", timeout=10)
print(r.status_code, r.headers.get('content-type'))
print(json.dumps(r.json(), indent=2))

print("\nSummarizing 'Cornell LII' via Ollama...")
payload = { 'name': 'Cornell LII', 'model': 'llama3' }
r2 = requests.post(f"{BASE}/api/ollama/summarize", json=payload, timeout=70)
print(r2.status_code, r2.headers.get('content-type'))
print(json.dumps(r2.json(), indent=2))
