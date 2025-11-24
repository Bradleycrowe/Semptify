import os
os.environ['R2_ACCOUNT_ID'] = 'be2a39cd3624261169fa8e800d75923f'
os.environ['R2_ACCESS_KEY_ID'] = 'c994035322007ef21464f670821c0e3d'
os.environ['R2_SECRET_ACCESS_KEY'] = '3b05227e537b441eb62b2d633fe969e74faa532d404d2c89cb5ab8f6e57f0ff7'
os.environ['R2_BUCKET_NAME'] = 'semptify'
os.environ['R2_ENDPOINT_URL'] = 'https://be2a39cd3624261169fa8e800d75923f.r2.cloudflarestorage.com'

import sys
sys.path.insert(0, 'C:/Semptify/Semptify')

from storage_manager import upload_file, download_file, list_files
import datetime

print("=== R2 Storage Manager Test ===")
test_data = f"R2 via storage_manager at {datetime.datetime.now().isoformat()}".encode('utf-8')
test_profile = "brad_test"
test_filename = "persistence_test.txt"

print(f"\n1. Uploading {len(test_data)} bytes to {test_profile}/{test_filename}...")
result = upload_file(test_profile, test_filename, test_data)
print(f"   Upload result: {result}")

if result.get('r2'):
    print(f"\n2. Listing files in profile '{test_profile}'...")
    files = list_files(test_profile)
    print(f"   Files found: {files}")

    print(f"\n3. Downloading {test_filename}...")
    downloaded = download_file(test_profile, test_filename)
    if downloaded:
        print(f"   Downloaded {len(downloaded)} bytes")
        print(f"   Content: {downloaded.decode('utf-8')}")
        print(f"\n✓✓✓ R2 PERSISTENCE FULLY OPERATIONAL ✓✓✓")
    else:
        print("   ERROR: Download failed")
else:
    print("\nERROR: R2 upload failed, check credentials/bucket")
