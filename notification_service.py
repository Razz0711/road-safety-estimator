"""
Notification Service for Road Safety Estimator
Handles Email notifications with SMTP integration (Gmail supported)
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
import os


class NotificationService:
    """Service for sending email notifications with PDF attachments"""
    
    def __init__(self):
        """Initialize notification service with SMTP configurations"""
        # Email SMTP Configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.smtp_from_email = os.getenv('SMTP_FROM_EMAIL', self.smtp_username)
    
    def send_email(self, to_email, subject, body, pdf_path=None):
        """
        Send email with optional PDF attachment
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body text
            pdf_path (str): Path to PDF file to attach (optional)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Check if SMTP is configured
            if not self.smtp_username or not self.smtp_password:
                return False, "SMTP credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD environment variables."
            
            # Clean password (remove any spaces)
            clean_password = self.smtp_password.replace(' ', '')
            
            print(f"📧 DEBUG: Attempting to send email to {to_email}")
            print(f"📧 DEBUG: PDF Path: {pdf_path}")
            print(f"📧 DEBUG: PDF Exists: {Path(pdf_path).exists() if pdf_path else 'No PDF'}")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body as both plain text and HTML
            msg.attach(MIMEText(body, 'plain'))
            
            # Create HTML version if body contains HTML
            if '<html>' in body.lower() or '<br>' in body.lower():
                msg.attach(MIMEText(body, 'html'))
            
            # Attach PDF if provided
            if pdf_path and Path(pdf_path).exists():
                print(f"📧 DEBUG: Attaching PDF: {Path(pdf_path).name}")
                with open(pdf_path, 'rb') as f:
                    pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
                    pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                            filename=Path(pdf_path).name)
                    msg.attach(pdf_attachment)
            else:
                print(f"📧 DEBUG: No PDF attachment (path: {pdf_path})")
            
            # Try connecting to SMTP server with timeout and retry logic
            print(f"📧 DEBUG: Connecting to {self.smtp_server}:{self.smtp_port}")
            
            try:
                # Try port 587 with STARTTLS first
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                    server.starttls()
                    print(f"📧 DEBUG: Logging in as {self.smtp_username}")
                    server.login(self.smtp_username, clean_password)
                    print(f"📧 DEBUG: Sending message...")
                    server.send_message(msg)
                print(f"📧 DEBUG: ✅ Email sent successfully!")
                return True, f"Email sent successfully to {to_email}"
                
            except Exception as port_587_error:
                print(f"📧 DEBUG: Port 587 failed: {port_587_error}")
                print(f"📧 DEBUG: Trying alternative port 465 (SSL)...")
                
                # Try port 465 with SSL as fallback
                with smtplib.SMTP_SSL(self.smtp_server, 465, timeout=30) as server:
                    print(f"📧 DEBUG: Logging in as {self.smtp_username}")
                    server.login(self.smtp_username, clean_password)
                    print(f"📧 DEBUG: Sending message...")
                    server.send_message(msg)
                
                print(f"📧 DEBUG: ✅ Email sent successfully via SSL!")
                return True, f"Email sent successfully to {to_email}"
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"📧 DEBUG: ❌ Authentication failed: {e}")
            return False, "SMTP authentication failed. Please check your email credentials."
        except smtplib.SMTPException as e:
            print(f"📧 DEBUG: ❌ SMTP error: {e}")
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            print(f"📧 DEBUG: ❌ General error: {e}")
            error_msg = str(e)
            if "10060" in error_msg or "timed out" in error_msg.lower():
                return False, "Connection timeout. Please check: 1) Your firewall/antivirus settings, 2) Network connection, 3) Try disabling VPN if active"
            return False, f"Error sending email: {error_msg}"
    
    def is_email_configured(self):
        """Check if email service is properly configured"""
        return bool(self.smtp_username and self.smtp_password)
    
    def get_configuration_instructions(self):
        """Get instructions for configuring the email service"""
        return {
            'email': {
                'configured': self.is_email_configured(),
                'instructions': """
**Email Configuration (SMTP) - FREE with Gmail:**

Create a `.env` file in the project root with:
- `SMTP_SERVER`: SMTP server address (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP port (default: 587)
- `SMTP_USERNAME`: Your Gmail address
- `SMTP_PASSWORD`: Gmail App Password (NOT your regular password)
- `SMTP_FROM_EMAIL`: Sender email (optional, defaults to SMTP_USERNAME)

**Gmail Setup Steps (100% FREE):**
1. Go to your Google Account settings
2. Enable 2-Factor Authentication (Security → 2-Step Verification)
3. Generate an App Password:
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or Other)
   - Copy the 16-character password
4. Use this App Password in your `.env` file

**Example `.env` file:**
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
```

**Important:** Add `.env` to `.gitignore` to keep credentials secure!
                """
            }
        }


# Singleton instance
_notification_service = None


def get_notification_service():
    """Get or create notification service singleton"""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
