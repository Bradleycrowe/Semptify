"""
Quick test to verify R2 adapter configuration and status.
Run: python test_r2_status.py
"""
import os
import sys

# Set test mode to avoid side effects
os.environ.setdefault('TESTING', '1')

print("\n=== R2 Database Adapter Status ===\n")

# Check boto3
try:
    import boto3
    print("✓ boto3 installed:", boto3.__version__)
except ImportError:
    print("✗ boto3 NOT installed - run: pip install boto3")
    sys.exit(1)

# Check env vars
required_vars = ['R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY']
print("\nEnvironment variables:")
for var in required_vars:
    val = os.getenv(var)
    if val:
        print(f"  ✓ {var} = {val[:8]}...")
    else:
        print(f"  ⚠ {var} = NOT SET")

bucket = os.getenv('R2_BUCKET_NAME', 'semptify-storage')
print(f"  • R2_BUCKET_NAME = {bucket}")

# Test adapter initialization
print("\nInitializing R2 adapter...")
try:
    from r2_database_adapter import get_r2_adapter
    adapter = get_r2_adapter()
    
    print(f"\n{'='*40}")
    print(f"Adapter Status: {'✓ ENABLED' if adapter.enabled else '⚠ DISABLED (local only)'}")
    print(f"Bucket: {adapter.bucket}")
    print(f"Last sync: {adapter.last_sync}")
    print(f"{'='*40}\n")
    
    if adapter.enabled:
        print("✅ R2 persistence is ACTIVE")
        print("   • Database will sync to R2 automatically")
        print("   • Data persists across Render deploys")
    else:
        print("⚠️  R2 persistence is INACTIVE")
        print("   • Using local-only database (ephemeral)")
        print("   • Set R2 env vars to enable persistence")
        print("\nTo enable R2:")
        print("  1. See R2_QUICK_START.md")
        print("  2. Set 4 env vars in Render")
        print("  3. Redeploy\n")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ Test complete\n")
