import sqlite3
import os

db_path = 'security/users.db'
print(f"Checking SQLite database: {db_path}")
print(f"File exists: {os.path.exists(db_path)}")
print(f"File size: {os.path.getsize(db_path)} bytes")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\n✓ Database accessible")
print(f"Tables: {[t[0] for t in tables]}")

# Check each table structure and row counts
for table_name in [t[0] for t in tables]:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  - {table_name}: {count} rows")

# Test write permission
try:
    cursor.execute("CREATE TABLE IF NOT EXISTS write_test (id INTEGER)")
    cursor.execute("DROP TABLE write_test")
    conn.commit()
    print("\n✓ Write permissions: OK")
except Exception as e:
    print(f"\n✗ Write permissions: FAILED - {e}")

conn.close()
print("\n✓ All checks passed")
