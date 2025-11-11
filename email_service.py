"""
Email Service for Semptify
Handles verification emails using Resend (3000 free/month) or Gmail SMTP
Priority: Resend > Gmail > Dev Mode
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import requests

logger = logging.getLogger(__name__)


def send_verification_email(to_email, verification_code, user_name=None):
    """
    Send verification code via email.

    Priority order:
    1. Resend API (if RESEND_API_KEY set) - 3000/month FREE
    2. Gmail SMTP (if GMAIL_ADDRESS set)
    3. Dev mode (just log)

    Args:
        to_email: Recipient email address
        verification_code: 6-digit verification code
        user_name: Optional user name for personalization

    Returns:
        bool: True if sent successfully, False otherwise
    """

    # Try Resend first (best option)
    resend_key = os.environ.get('RESEND_API_KEY')
    if resend_key:
        return _send_via_resend(to_email, verification_code, user_name, resend_key)

    # Fall back to Gmail
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    if gmail_address and gmail_password:
        return _send_via_gmail(to_email, verification_code, user_name, gmail_address, gmail_password)

    # Dev mode - just log
    print(f"[DEV MODE] Verification email to {to_email}: {verification_code}")
    logger.warning("No email service configured - running in dev mode")
    return True


def _send_via_resend(to_email, verification_code, user_name, api_key):
    """Send email using Resend API (3000 free/month)"""
    greeting = f"Hello {user_name}" if user_name else "Welcome"

    try:
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'from': 'Semptify <onboarding@resend.dev>',  # Change after domain verified
                'to': [to_email],
                'subject': 'Verify Your Semptify Account',
                'html': f'''
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #667eea;">{greeting}!</h2>
                        <p>Your Semptify verification code is:</p>
                        <div style="background: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0;">
                            <h1 style="color: #333; font-size: 36px; letter-spacing: 8px; margin: 0;">
                                {verification_code}
                            </h1>
                        </div>
                        <p style="color: #666;">This code expires in 10 minutes.</p>
                        <p style="color: #999; font-size: 12px; margin-top: 30px;">
                            If you didn't request this code, please ignore this email.
                        </p>
                    </div>
                '''
            },
            timeout=10
        )

        if response.status_code == 200:
            logger.info("Verification email sent via Resend to %s", to_email)
            return True
        else:
            logger.error("Resend API error: %s - %s", response.status_code, response.text)
            return False

    except requests.exceptions.RequestException as e:
        logger.error("Failed to send email via Resend: %s", e)
        return False


def _send_via_gmail(to_email, verification_code, user_name, sender, password):
    """Send email using Gmail SMTP (legacy fallback)"""
    greeting = f"Hello {user_name}" if user_name else "Welcome"

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Verify Your Semptify Account'
        msg['From'] = f"Semptify <{sender}>"
        msg['To'] = to_email

        # HTML email content
        html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                   color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
        .code-box {{ background: white; border: 2px solid #3b82f6; border-radius: 8px;
                     padding: 20px; text-align: center; margin: 20px 0; }}
        .code {{ font-size: 32px; font-weight: bold; color: #1e3a8a; letter-spacing: 8px; }}
        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #6b7280; }}
        .button {{ display: inline-block; background: #3b82f6; color: white;
                   padding: 12px 30px; text-decoration: none; border-radius: 6px;
                   margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 Semptify</h1>
            <p>Tenant Rights & Housing Assistance</p>
        </div>
        <div class="content">
            <h2>{greeting}!</h2>
            <p>Thank you for registering with Semptify. To complete your registration,
               please enter the verification code below:</p>

            <div class="code-box">
                <div class="code">{verification_code}</div>
            </div>

            <p><strong>Important:</strong></p>
            <ul>
                <li>This code expires in 15 minutes</li>
                <li>Never share this code with anyone</li>
                <li>If you didn't request this, please ignore this email</li>
            </ul>

            <p>Once verified, you'll have access to:</p>
            <ul>
                <li>📋 Document vault for secure file storage</li>
                <li>⚖️ Legal information and procedures</li>
                <li>🏛️ Court filing assistance</li>
                <li>📞 Agency contact information</li>
                <li>💰 Funding and legal aid resources</li>
            </ul>

            <p>Need help? Visit <a href="https://semptify.onrender.com">semptify.onrender.com</a></p>
        </div>
        <div class="footer">
            <p>© 2025 Semptify - Empowering Tenants Through Information</p>
            <p>This is an automated message, please do not reply.</p>
        </div>
    </div>
</body>
</html>
        '''

        # Plain text fallback
        text_content = f'''
{greeting}!

Thank you for registering with Semptify.

Your verification code is: {verification_code}

This code expires in 15 minutes.
Never share this code with anyone.

Once verified, you'll have access to:
- Document vault for secure file storage
- Legal information and procedures
- Court filing assistance
- Agency contact information
- Funding and legal aid resources

Need help? Visit https://semptify.onrender.com

© 2025 Semptify - Empowering Tenants Through Information
This is an automated message, please do not reply.
        '''

        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())

        logger.info("✓ Verification email sent to %s", to_email)
        print(f"✓ Verification email sent to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail authentication failed - check GMAIL_APP_PASSWORD")
        print(f"✗ Gmail auth failed. Code for {to_email}: {verification_code}")
        return False
    except (smtplib.SMTPException, OSError) as e:
        logger.error("Failed to send email: %s", e)
        print(f"✗ Failed to send email to {to_email}: {str(e)}")
        print(f"   Verification code: {verification_code}")
        return False


def send_password_reset_email(to_email, reset_code, user_name=None):
    """
    Send a password reset email to the user.
    
    NOTE: Currently in dev mode only. To enable real email delivery:
    - Configure Resend API or SendGrid in your environment
    - Use send_verification_code() function for full email functionality
    
    Args:
        to_email: Email address to send reset code
        reset_code: Password reset code
        user_name: Optional user name for personalization (currently unused in dev mode)
    """
    logger.info("send_password_reset_email called for %s (dev mode, code: %s)", 
                to_email, reset_code)


def test_email_service():
    """Test the email service configuration"""
    print("Testing email service...")

    # Check for Resend API key (preferred)
    resend_key = os.environ.get('RESEND_API_KEY')
    if resend_key:
        print("✓ RESEND_API_KEY is set - using Resend (3000 emails/month free)")
        return True
    
    # Check for Gmail credentials (fallback)
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    if gmail_address and gmail_password:
        print("✓ Gmail credentials configured")
        print(f"  GMAIL_ADDRESS: {gmail_address}")
        return True
    
    # Dev mode
    print("⚠ No email service configured - running in DEV MODE")
    print("  Emails will be logged to console instead of sent")
    print("  To enable email sending:")
    print("  Option 1 (Recommended): Resend API")
    print("    1. Sign up at https://resend.com (3000 emails/month free)")
    print("    2. Get API key from dashboard")
    print("    3. Add to environment: RESEND_API_KEY=re_xxx")
    print("  Option 2: Gmail SMTP")
    print("    1. Enable 2FA on your Gmail account")
    print("    2. Generate app password: https://myaccount.google.com/apppasswords")
    print("    3. Add to environment: GMAIL_ADDRESS=your@gmail.com")
    print("    4. Add to environment: GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
    return False


if __name__ == "__main__":
    # Run test when executed directly
    test_email_service()

    # Test sending (will use dev mode if no API key)
    print("\nTesting verification email...")
    success = send_verification_email("test@example.com", "123456", "Test User")
    print(f"Result: {'✓ Success' if success else '✗ Failed'}")
