import Semptify
import importlib
import os
import secrets

os.environ['SECURITY_MODE'] = 'open'
importlib.reload(Semptify)

client = Semptify.app.test_client()
Semptify.app.config['TESTING'] = True

email = f'test.{secrets.token_hex(4)}@example.com'
print(f"Testing registration with email: {email}")

r = client.post('/register', data={
    'first_name': 'Test',
    'last_name': 'User',
    'email': email,
    'phone': '555-0123',
    'address': '123 Test St',
    'city': 'Test City',
    'county': 'Test County',
    'state': 'CA',
    'zip': '12345',
    'verify_method': 'email'
})

print(f'Status: {r.status_code}')
print(f'Location: {r.location if r.status_code == 302 else "N/A"}')
if r.status_code == 200:
    print(f'Response body contains "error": {"error" in str(r.data)}')
    if "error" in str(r.data):
        print("Error in response - form validation failed")
