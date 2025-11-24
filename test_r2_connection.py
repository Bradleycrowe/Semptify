# Test script for R2 connectivity
import os
from r2_storage_layer import r2_available, list_profile_files, upload_bytes, download_bytes

profile_id = "default"
print("R2 available:", r2_available())
if r2_available():
    # Try a small test file
    if upload_bytes(profile_id, "r2_test.txt", b"hello-r2"):
        print("Upload OK")
        files = list_profile_files(profile_id)
        print("Files:", files)
        data = download_bytes(profile_id, "r2_test.txt")
        print("Downloaded:", data)
    else:
        print("Upload failed")
else:
    print("R2 not configured (will fall back if not in R2_ONLY mode)")
