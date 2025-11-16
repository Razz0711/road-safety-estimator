"""
Quick test script to verify Gmail SMTP configuration
"""
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

print("🔍 Checking Email Configuration...")
print("-" * 50)

# Check if .env values are loaded
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_from_email = os.getenv('SMTP_FROM_EMAIL')

print(f"SMTP Server: {smtp_server}")
print(f"SMTP Port: {smtp_port}")
print(f"Username: {smtp_username}")
print(f"Password: {'*' * len(smtp_password) if smtp_password else 'NOT SET'}")
print(f"From Email: {smtp_from_email}")
print("-" * 50)

# Test connection
if not smtp_username or not smtp_password:
    print("❌ ERROR: SMTP credentials not configured!")
    print("Please edit the .env file with your Gmail credentials.")
else:
    print("\n📧 Testing SMTP Connection...")
    try:
        # Remove spaces from password (in case they were copied with spaces)
        clean_password = smtp_password.replace(' ', '')
        
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            print("✅ Connected to SMTP server")
            
            server.login(smtp_username, clean_password)
            print("✅ Authentication successful!")
            
            print("\n🎉 Email configuration is WORKING!")
            print("You can now send emails from the application.")
            
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed!")
        print("Please check:")
        print("  1. Gmail 2-Factor Authentication is enabled")
        print("  2. You're using an App Password (not regular password)")
        print("  3. Generate new password at: https://myaccount.google.com/apppasswords")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n" + "-" * 50)
print("Test complete!")
