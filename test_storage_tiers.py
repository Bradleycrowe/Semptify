# test_storage_tiers.py - Test both R2 and Google Drive storage
from storage_manager import storage_available, upload_file, download_file, list_files, save_json, load_json

print("\n=== Storage Availability ===")
status = storage_available()
for backend, available in status.items():
    symbol = "[OK]" if available else "[--]"
    print(f"{symbol} {backend.upper()}: {available}")

profile_id = "test_client_001"

print(f"\n=== Testing Upload (profile: {profile_id}) ===")
test_data = b"Hello from Semptify - Multi-tier storage test"
results = upload_file(profile_id, "test_document.txt", test_data)
print(f"Upload results: {results}")

print(f"\n=== Testing JSON Save ===")
test_obj = {"client": "Test Client", "case_id": "001", "documents": 5}
json_results = save_json(profile_id, "case_metadata.json", test_obj)
print(f"JSON save results: {json_results}")

print(f"\n=== Testing Download ===")
downloaded = download_file(profile_id, "test_document.txt")
if downloaded:
    print(f"Downloaded: {downloaded.decode('utf-8')}")
else:
    print("Download failed")

print(f"\n=== Testing JSON Load ===")
loaded = load_json(profile_id, "case_metadata.json")
print(f"Loaded JSON: {loaded}")

print(f"\n=== Listing Files ===")
files = list_files(profile_id)
print(f"Files in profile '{profile_id}': {files}")

print("\n=== Test Complete ===")
