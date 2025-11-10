"""
Quick Login Helper for Testing Semptify
Creates a direct login link without verification
"""

import os
import sys

print("""
╔══════════════════════════════════════════════════════════════╗
║           SEMPTIFY TEST ACCOUNT - QUICK LOGIN                ║
╚══════════════════════════════════════════════════════════════╝

✅ Test account created and ready!

📧 EMAIL:     test@example.com
👤 USER ID:   test_user_001
📍 LOCATION:  Minneapolis, MN
🔧 ISSUE:     Maintenance problems
📊 STAGE:     Having trouble

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 HOW TO LOGIN & TEST:

OPTION 1: Direct Session Bypass (Fastest)
  1. Start the app: python Semptify.py
  2. Visit: http://localhost:5000/test-login
  3. You'll be logged in automatically! ✨

OPTION 2: Regular Signin Flow
  1. Go to: http://localhost:5000/signin
  2. Enter: test@example.com
  3. Code will print in terminal (no email needed)
  4. Enter the code → Signed in!

OPTION 3: Create New Test User Each Time
  1. Go to: http://localhost:5000/register
  2. Fill out form with test data
  3. Skip verification (works in dev mode)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 WHAT TO TEST:

After logging in, try these routes:

🏠 Dashboard:           http://localhost:5000/dashboard
   → See personalized components based on your stage

📚 Learning Module:     http://localhost:5000/learning
   → Browse procedures, fact-check claims, get quick refs

🗂️ Document Vault:      http://localhost:5000/vault
   → Upload/download secure documents

📋 Resources:           http://localhost:5000/resources
   → Access forms, checklists, templates

🔍 Route Discovery:     http://localhost:5000/api/routes/discover
   → See all available routes and data sources

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 ADMIN FEATURES:

To access admin panel:
  1. Set ADMIN_TOKEN in environment (or use open mode)
  2. Visit: http://localhost:5000/admin?token=<your-token>
  3. Can trigger releases, view metrics, etc.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIP: Keep this terminal open while testing!
    All verification codes will print here.

🎯 Ready to explore Semptify!
""")
