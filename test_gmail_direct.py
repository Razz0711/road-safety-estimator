"""
Direct SMTP test without .env to verify credentials
"""
import smtplib

print("Testing Gmail SMTP Authentication...")
print("-" * 50)

# Your credentials
username = "rajkumaratsvnit@gmail.com"
password = "twht bmqx xtts wxbh"  # With spaces
password_no_spaces = "twhtbmqxxttswxbh"  # Without spaces

print(f"Email: {username}")
print(f"Password (with spaces): {password}")
print(f"Password (no spaces): {password_no_spaces}")
print("-" * 50)

# Try with spaces
print("\n🔍 Attempt 1: Testing with spaces...")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    print("✅ SUCCESS with spaces!")
    server.quit()
except Exception as e:
    print(f"❌ Failed with spaces: {e}")

# Try without spaces
print("\n🔍 Attempt 2: Testing without spaces...")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password_no_spaces)
    print("✅ SUCCESS without spaces!")
    server.quit()
except Exception as e:
    print(f"❌ Failed without spaces: {e}")

print("\n" + "-" * 50)
print("\n⚠️ If BOTH failed, please:")
print("1. Check 2FA is enabled: https://myaccount.google.com/security")
print("2. Generate NEW App Password: https://myaccount.google.com/apppasswords")
print("3. OR enable Less Secure Apps: https://myaccount.google.com/lesssecureapps")
