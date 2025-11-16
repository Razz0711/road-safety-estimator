"""
Test Email Configuration
Run this to check if your email setup is working
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)

# Check if .env file exists
if not os.path.exists('.env'):
    print("\n❌ ERROR: .env file NOT FOUND!")
    print("\n📝 TO FIX THIS:")
    print("1. Copy .env.example to .env:")
    print("   copy .env.example .env")
    print("\n2. Open .env file and add your Gmail credentials:")
    print("   SMTP_SERVER=smtp.gmail.com")
    print("   SMTP_PORT=587")
    print("   SMTP_USERNAME=your-email@gmail.com")
    print("   SMTP_PASSWORD=your-16-char-app-password")
    print("\n3. Get Gmail App Password:")
    print("   - Enable 2FA: https://myaccount.google.com/security")
    print("   - Get App Password: https://myaccount.google.com/apppasswords")
    print("\n")
else:
    print("\n✅ .env file found!")
    
    # Check configuration
    smtp_server = os.getenv('SMTP_SERVER', '')
    smtp_port = os.getenv('SMTP_PORT', '')
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    print("\n📧 Configuration Check:")
    print(f"   SMTP Server: {smtp_server if smtp_server else '❌ NOT SET'}")
    print(f"   SMTP Port: {smtp_port if smtp_port else '❌ NOT SET'}")
    print(f"   Username: {smtp_username if smtp_username else '❌ NOT SET'}")
    print(f"   Password: {'✅ SET (' + '*' * len(smtp_password) + ')' if smtp_password else '❌ NOT SET'}")
    
    if not all([smtp_server, smtp_port, smtp_username, smtp_password]):
        print("\n❌ ERROR: Some credentials are missing!")
        print("\n📝 Please edit .env file and fill all fields")
    else:
        print("\n✅ All credentials are configured!")
        
        # Test connection
        print("\n🔌 Testing SMTP connection...")
        try:
            import smtplib
            
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.quit()
            
            print("✅ SUCCESS! Email connection works perfectly!")
            print("\n🎉 You can now send emails from the app!")
            
        except smtplib.SMTPAuthenticationError:
            print("❌ AUTHENTICATION FAILED!")
            print("\n📝 Possible issues:")
            print("   1. Wrong email or password")
            print("   2. Need to use App Password (not regular password)")
            print("   3. 2-Factor Authentication not enabled")
            print("\n🔧 Fix:")
            print("   - Go to: https://myaccount.google.com/apppasswords")
            print("   - Generate new App Password")
            print("   - Update SMTP_PASSWORD in .env file")
            
        except Exception as e:
            print(f"❌ CONNECTION ERROR: {str(e)}")
            print("\n📝 Check your internet connection and credentials")

print("\n" + "=" * 60)
