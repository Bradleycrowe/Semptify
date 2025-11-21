"""
OAuth Setup Diagnostic - Run this to check what's configured
"""
import os

print("=== OAUTH CONFIGURATION CHECK ===\n")

# Check environment variables
google_id = os.getenv('GOOGLE_CLIENT_ID')
google_secret = os.getenv('GOOGLE_CLIENT_SECRET')
dropbox_key = os.getenv('DROPBOX_APP_KEY')
dropbox_secret = os.getenv('DROPBOX_APP_SECRET')
flask_secret = os.getenv('FLASK_SECRET_KEY')

print(f"Google Client ID: {'✓ SET' if google_id else '✗ MISSING'}")
print(f"Google Client Secret: {'✓ SET' if google_secret else '✗ MISSING'}")
print(f"Dropbox App Key: {'✓ SET' if dropbox_key else '✗ MISSING'}")
print(f"Dropbox App Secret: {'✓ SET' if dropbox_secret else '✗ MISSING'}")
print(f"Flask Secret Key: {'✓ SET' if flask_secret else '✗ MISSING'}")

print("\n=== REQUIRED REDIRECT URIs ===")
print("Google Console: https://semptify.onrender.com/oauth/google/callback")
print("Dropbox Console: https://semptify.onrender.com/oauth/dropbox/callback")

print("\n=== NEXT STEPS ===")
if not all([google_id, google_secret, dropbox_key, dropbox_secret, flask_secret]):
    print("1. Go to Render Dashboard → Semptify → Environment")
    print("2. Add missing environment variables")
    print("3. Redeploy")
else:
    print("All environment variables are set.")
    print("If OAuth still fails, verify redirect URIs in Google/Dropbox consoles match exactly.")
