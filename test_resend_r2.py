"""
Test Resend Email and Cloudflare R2 Storage
Run with: python test_resend_r2.py
"""

import os
import requests
from datetime import datetime

def test_resend_email():
    """Test Resend email service"""
    print("\n=== Testing Resend Email ===")

    api_key = os.environ.get('RESEND_API_KEY')
    if not api_key:
        print("❌ RESEND_API_KEY not set")
        print("Set it with: $env:RESEND_API_KEY='re_xxxxx'")
        return False

    print(f"✓ API Key found: {api_key[:10]}...")

    # Test email
    test_email = input("Enter email to test (or press Enter for default): ").strip()
    if not test_email:
        test_email = "test@example.com"

    print(f"\nSending test email to: {test_email}")

    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'from': 'Semptify <onboarding@resend.dev>',
                'to': [test_email],
                'subject': f'Semptify Test Email - {datetime.now().strftime("%H:%M:%S")}',
                'html': '''
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #667eea;">🎉 Resend is Working!</h2>
                        <p>This is a test email from Semptify.</p>
                        <div style="background: #f5f5f5; padding: 20px; margin: 20px 0; border-left: 4px solid #667eea;">
                            <p><strong>Service:</strong> Resend</p>
                            <p><strong>Status:</strong> ✅ Connected</p>
                            <p><strong>Free Tier:</strong> 3,000 emails/month</p>
                        </div>
                        <p style="color: #666;">If you received this email, Semptify can now send verification codes!</p>
                    </div>
                '''
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Email sent successfully!")
            print(f"   Email ID: {data.get('id')}")
            print(f"\nCheck {test_email} for the test email!")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_cloudflare_r2():
    """Test Cloudflare R2 storage"""
    print("\n=== Testing Cloudflare R2 Storage ===")

    # Check for R2 credentials
    account_id = os.environ.get('R2_ACCOUNT_ID')
    access_key = os.environ.get('R2_ACCESS_KEY_ID')
    secret_key = os.environ.get('R2_SECRET_ACCESS_KEY')
    bucket = os.environ.get('R2_BUCKET_NAME', 'semptify-storage')

    if not all([account_id, access_key, secret_key]):
        print("❌ R2 credentials not set")
        print("\nRequired environment variables:")
        print("  - R2_ACCOUNT_ID")
        print("  - R2_ACCESS_KEY_ID")
        print("  - R2_SECRET_ACCESS_KEY")
        print("  - R2_BUCKET_NAME (optional, defaults to 'semptify-storage')")
        return False

    print(f"✓ Account ID: {account_id[:8]}...")
    print(f"✓ Access Key: {access_key[:8]}...")
    print(f"✓ Bucket: {bucket}")

    try:
        import boto3
        from botocore.exceptions import ClientError

        # Create R2 client
        s3 = boto3.client(
            's3',
            endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='auto'
        )

        # Test 1: List buckets
        print("\n📦 Testing bucket access...")
        try:
            response = s3.list_buckets()
            buckets = [b['Name'] for b in response['Buckets']]
            print(f"✅ Connected! Found {len(buckets)} bucket(s):")
            for b in buckets:
                print(f"   - {b}")
        except ClientError as e:
            print(f"❌ Cannot list buckets: {e}")
            return False

        # Test 2: Upload a test file
        print(f"\n📤 Testing file upload to '{bucket}'...")
        test_content = f"Semptify R2 Test - {datetime.now().isoformat()}"
        test_key = f"test/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        try:
            s3.put_object(
                Bucket=bucket,
                Key=test_key,
                Body=test_content.encode('utf-8'),
                ContentType='text/plain'
            )
            print(f"✅ File uploaded: {test_key}")
        except ClientError as e:
            print(f"❌ Upload failed: {e}")
            return False

        # Test 3: Download the file
        print(f"\n📥 Testing file download...")
        try:
            response = s3.get_object(Bucket=bucket, Key=test_key)
            downloaded = response['Body'].read().decode('utf-8')
            if downloaded == test_content:
                print(f"✅ File downloaded and verified!")
            else:
                print(f"⚠️ Downloaded content doesn't match")
        except ClientError as e:
            print(f"❌ Download failed: {e}")
            return False

        # Test 4: Delete test file
        print(f"\n🗑️ Cleaning up test file...")
        try:
            s3.delete_object(Bucket=bucket, Key=test_key)
            print(f"✅ Test file deleted")
        except ClientError as e:
            print(f"⚠️ Cleanup failed: {e}")

        print(f"\n✅ R2 Storage is fully functional!")
        print(f"   Free tier: 10GB storage, 10M read/month, 1M write/month")
        return True

    except ImportError:
        print("❌ boto3 not installed")
        print("Install with: pip install boto3")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("=" * 60)
    print("Semptify - Service Testing")
    print("=" * 60)

    # Test Resend
    resend_ok = test_resend_email()

    # Test R2
    r2_ok = test_cloudflare_r2()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Resend Email: {'✅ PASS' if resend_ok else '❌ FAIL'}")
    print(f"Cloudflare R2: {'✅ PASS' if r2_ok else '❌ FAIL'}")
    print()

    if resend_ok and r2_ok:
        print("🎉 All services working! Ready for production!")
    elif resend_ok:
        print("📧 Email working. Set up R2 for document storage.")
    elif r2_ok:
        print("💾 Storage working. Set up Resend for emails.")
    else:
        print("⚠️ Services need configuration. See messages above.")


if __name__ == '__main__':
    main()
