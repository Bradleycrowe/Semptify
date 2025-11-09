"""
Setup test user in database for manual testing
"""

from user_database import _get_db, init_database

# Initialize database (creates tables and migrations)
init_database()

# Create test user with specific stage and issue type
db = _get_db()
cursor = db.cursor()

# Insert test user
user_id = "test_user_001"
cursor.execute("""
INSERT OR REPLACE INTO users 
(user_id, first_name, last_name, email, phone, address, city, county, state, zip, 
 verified_at, location, issue_type, stage, created_at, last_login)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    user_id,
    "Test",
    "User",
    "test@example.com",
    "555-1234",
    "123 Test St",
    "Minneapolis",
    "Hennepin",
    "MN",
    "55401",
    "2025-11-09",
    "Minneapolis, MN",
    "maintenance",
    "HAVING_TROUBLE",
    "2025-11-09",
    "2025-11-09"
))

db.commit()
db.close()

print(f"✅ Created test user: {user_id}")
print("   Email: test@example.com")
print("   Location: Minneapolis, MN")
print("   Issue: maintenance")
print("   Stage: HAVING_TROUBLE")
print("\nTo test:")
print("1. Register at /register")
print("2. Or sign in with: email=test@example.com")
print("3. Navigate to /dashboard to see the dynamic dashboard")
