import os
os.environ['R2_ACCOUNT_ID'] = 'be2a39cd3624261169fa8e800d75923f'
os.environ['R2_ACCESS_KEY_ID'] = 'c994035322007ef21464f670821c0e3d'
os.environ['R2_SECRET_ACCESS_KEY'] = '3b05227e537b441eb62b2d633fe969e74faa532d404d2c89cb5ab8f6e57f0ff7'
os.environ['R2_BUCKET_NAME'] = 'semptify'
os.environ['R2_ENDPOINT_URL'] = 'https://be2a39cd3624261169fa8e800d75923f.r2.cloudflarestorage.com'

import boto3
client = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
    region_name="auto"
)

print("Testing direct boto3 R2 access...")
print(f"Bucket: {os.getenv('R2_BUCKET_NAME')}")

try:
    # List buckets
    response = client.list_buckets()
    print(f"\nBuckets available: {[b['Name'] for b in response.get('Buckets', [])]}")
    
    # Try to upload
    test_key = "test/direct_upload.txt"
    test_data = b"Direct R2 test"
    client.put_object(Bucket='semptify', Key=test_key, Body=test_data)
    print(f"✓ Uploaded to {test_key}")
    
    # Try to list
    response = client.list_objects_v2(Bucket='semptify', Prefix='test/')
    print(f"✓ Listed objects: {[o['Key'] for o in response.get('Contents', [])]}")
    
    # Try to download
    response = client.get_object(Bucket='semptify', Key=test_key)
    content = response['Body'].read()
    print(f"✓ Downloaded: {content.decode('utf-8')}")
    
except Exception as e:
    print(f"ERROR: {e}")
