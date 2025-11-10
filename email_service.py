"""
Email Service for Semptify
Handles verification emails using Gmail SMTP (100% free, no time limit)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)


def send_verification_email(to_email, verification_code, user_name=None):
    """
    Send verification code via email using Gmail SMTP.
    
    Required environment variables:
        GMAIL_ADDRESS: Your Gmail address
        GMAIL_APP_PASSWORD: Gmail App Password (16-char, from Google Account security)
    
    Args:
        to_email: Recipient email address
        verification_code: 6-digit verification code
        user_name: Optional user name for personalization
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    sender = os.environ.get('GMAIL_ADDRESS')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not sender or not password:
        # Development mode - just log the code
        print(f"[DEV MODE] Verification email to {to_email}: {verification_code}")
        logger.warning("Gmail credentials not configured - running in dev mode")
        return True
    
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
        
        logger.info(f"✓ Verification email sent to {to_email}")
        print(f"✓ Verification email sent to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail authentication failed - check GMAIL_APP_PASSWORD")
        print(f"✗ Gmail auth failed. Code for {to_email}: {verification_code}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        print(f"✗ Failed to send email to {to_email}: {str(e)}")
        print(f"   Verification code: {verification_code}")
        return False


def send_password_reset_email(to_email, reset_code, user_name=None):
    """
    Send password reset code via email.
    
    Args:
        to_email: Recipient email address
        reset_code: 6-digit reset code
        user_name: Optional user name
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = os.environ.get('FROM_EMAIL', 'noreply@semptify.onrender.com')
    
    if not sendgrid_api_key:
        print(f"[DEV MODE] Password reset email to {to_email}: {reset_code}")
        return True
    
    greeting = f"Hello {user_name}" if user_name else "Hello"
    
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='Reset Your Semptify Password',
        html_content=f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #dc2626 0%, #f87171 100%); 
                   color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
        .code-box {{ background: white; border: 2px solid #dc2626; border-radius: 8px;
                     padding: 20px; text-align: center; margin: 20px 0; }}
        .code {{ font-size: 32px; font-weight: bold; color: #dc2626; letter-spacing: 8px; }}
        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #6b7280; }}
        .warning {{ background: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Password Reset</h1>
            <p>Semptify Account Security</p>
        </div>
        <div class="content">
            <h2>{greeting},</h2>
            <p>We received a request to reset your Semptify password. 
               Enter this code to create a new password:</p>
            
            <div class="code-box">
                <div class="code">{reset_code}</div>
            </div>
            
            <div class="warning">
                <strong>⚠️ Security Notice:</strong>
                <ul style="margin: 10px 0;">
                    <li>This code expires in 15 minutes</li>
                    <li>Never share this code with anyone</li>
                    <li>Semptify will never ask for your password</li>
                </ul>
            </div>
            
            <p><strong>Didn't request this?</strong><br>
               If you didn't request a password reset, please ignore this email. 
               Your account remains secure.</p>
        </div>
        <div class="footer">
            <p>© 2025 Semptify - Tenant Rights Platform</p>
            <p>This is an automated message, please do not reply.</p>
        </div>
    </div>
</body>
</html>
        '''
    )
    
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"✓ Password reset email sent to {to_email}")
            return True
        else:
            print(f"⚠ SendGrid returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to send reset email to {to_email}: {str(e)}")
        if not sendgrid_api_key:
            return True
        return False


def test_email_service():
    """Test the email service configuration"""
    print("Testing email service...")
    
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        print("⚠ SENDGRID_API_KEY not set - running in DEV MODE")
        print("  Emails will be logged to console instead of sent")
        print("  To enable email sending:")
        print("  1. Sign up at https://sendgrid.com (free tier: 100 emails/day)")
        print("  2. Create API key at https://app.sendgrid.com/settings/api_keys")
        print("  3. Add to Render: SENDGRID_API_KEY=your_key_here")
        return False
    
    print(f"✓ SENDGRID_API_KEY is set")
    print(f"✓ FROM_EMAIL: {os.environ.get('FROM_EMAIL', 'noreply@semptify.onrender.com')}")
    print("✓ Email service ready!")
    return True


if __name__ == "__main__":
    # Run test when executed directly
    test_email_service()
    
    # Test sending (will use dev mode if no API key)
    print("\nTesting verification email...")
    success = send_verification_email("test@example.com", "123456", "Test User")
    print(f"Result: {'✓ Success' if success else '✗ Failed'}")
