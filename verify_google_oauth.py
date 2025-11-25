"""
Google OAuth Credentials Verification Script
Run this to test if your Google OAuth credentials are correct
"""
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

print("=" * 60)
print("GOOGLE OAUTH CREDENTIALS CHECK")
print("=" * 60)
print(f"\nClient ID: {client_id}")
print(f"Client Secret: {client_secret[:20]}... (truncated)")
print("\n" + "=" * 60)
print("TO FIX INVALID_CLIENT ERROR:")
print("=" * 60)
print("\n1. Go to: https://console.cloud.google.com/apis/credentials")
print("2. Find your OAuth 2.0 Client ID")
print("3. Click on it to view details")
print("4. Copy the EXACT Client ID and Client Secret")
print("5. Update .env file with correct values")
print("\nAuthorized redirect URIs must include:")
print("  - http://localhost:5000/oauth/google/callback")
print("  - https://semptify.onrender.com/oauth/google/callback")
print("\n" + "=" * 60)
