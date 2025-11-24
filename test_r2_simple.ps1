$env:R2_ENDPOINT_URL='https://be2a39cd3624261169fa8e800d75923f.r2.cloudflarestorage.com'
$env:R2_ACCESS_KEY_ID='c994035322007ef21464f670821c0e3d'
$env:R2_SECRET_ACCESS_KEY='3b05227e537b441eb62b2d633fe969e74faa532d404d2c89cb5ab8f6e57f0ff7'
$env:R2_BUCKET_NAME='semptify'
& 'C:\Semptify\Semptify\.venv\Scripts\python.exe' -c "
import boto3
import os
client = boto3.client(
    's3',
    endpoint_url=os.getenv('R2_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
    region_name='auto'
)
try:
    buckets = client.list_buckets()
    print('Buckets:', buckets)
except Exception as e:
    print('Error:', e)
"
