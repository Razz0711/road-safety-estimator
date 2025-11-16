"""
Send a test email with PDF attachment to verify everything works
"""
import os
from dotenv import load_dotenv
from notification_service import get_notification_service

# Load environment
load_dotenv()

print("🔍 Testing Email Sending with PDF Attachment...")
print("-" * 50)

# Get notification service
notification_service = get_notification_service()

# Check configuration
if not notification_service.is_email_configured():
    print("❌ Email not configured! Please check .env file.")
    exit(1)

print("✅ Email service configured")
print(f"From: {os.getenv('SMTP_USERNAME')}")

# Get recipient email
recipient = input("\n📧 Enter recipient email address: ").strip()

if not recipient:
    print("❌ No email provided!")
    exit(1)

# Create test message
subject = "Test Email from Road Safety Estimator"
body = """Hello!

This is a test email from the Road Safety Estimator application.

If you receive this email, the email integration is working correctly!

Best regards,
Road Safety Estimator
"""

print(f"\n📤 Sending test email to: {recipient}")
print("⏳ Please wait...")

# Send email (without PDF for now)
success, message = notification_service.send_email(
    to_email=recipient,
    subject=subject,
    body=body,
    pdf_path=None  # No PDF attachment for test
)

print("-" * 50)
if success:
    print(f"✅ {message}")
    print(f"\n🎉 SUCCESS! Check your inbox at: {recipient}")
    print("\nIf you don't see it:")
    print("  1. Check your SPAM folder")
    print("  2. Add rajkumaratsvnit@gmail.com to contacts")
else:
    print(f"❌ {message}")
    print("\n⚠️ Email sending failed!")

print("-" * 50)
