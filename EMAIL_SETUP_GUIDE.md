# 📧 Email Integration Setup Guide

## Overview
The Road Safety Estimator now includes **FREE email integration** using Gmail SMTP. You can send PDF reports directly via email with automatic PDF attachment!

## ✅ Features
- ✉️ Send PDF reports via email with one click
- 📎 Automatic PDF attachment
- 🆓 **100% FREE** - uses Gmail SMTP (no paid APIs)
- 🔐 Secure - credentials stored in `.env` file
- ⚡ Easy setup - takes only 2 minutes!

## 🚀 Quick Setup (5 Steps)

### Step 1: Enable 2-Factor Authentication on Gmail
1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security**
3. Enable **2-Step Verification**

### Step 2: Generate Gmail App Password
1. Visit: https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Windows Computer" (or Other)
4. Click **Generate**
5. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 3: Create `.env` File
1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` and add your credentials:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop
   SMTP_FROM_EMAIL=your-email@gmail.com
   ```

### Step 4: Add `.env` to `.gitignore`
Make sure `.env` is in your `.gitignore` file to keep credentials secure:
```
.env
```

### Step 5: Test the Integration
1. Run the application
2. Generate a report
3. Enter recipient email address
4. Click "📨 Send Email with PDF Attachment"
5. Check your email!

## 📝 Example Configuration

**`.env` file:**
```env
# Gmail SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=myproject@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
SMTP_FROM_EMAIL=myproject@gmail.com
```

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` by default
2. **Use App Passwords** - Never use your regular Gmail password
3. **Rotate passwords** - Change app passwords periodically
4. **Revoke unused** - Remove app passwords you no longer use

## 🛠️ Troubleshooting

### "SMTP authentication failed"
- ✅ Check that 2-Factor Authentication is enabled
- ✅ Generate a new App Password
- ✅ Copy the password correctly (no spaces)

### "SMTP error: Connection refused"
- ✅ Check your internet connection
- ✅ Verify SMTP_SERVER=smtp.gmail.com
- ✅ Verify SMTP_PORT=587

### "Email not configured"
- ✅ Make sure `.env` file exists in project root
- ✅ Check all fields are filled correctly
- ✅ Restart the application after creating `.env`

## 📧 Other Email Providers

### Outlook/Hotmail
```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Yahoo Mail
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

### Custom SMTP Server
```env
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
```

## 💡 Tips

- **Test emails** go to spam? Add your email to contacts
- **Large attachments** (>10MB) may take longer to send
- **Multiple recipients**: Use CC/BCC in Gmail after receiving
- **Email templates**: Customize the email body in `app.py`

## 🎉 Success!

Once configured, you'll see:
- ✅ Green "Email service configured and ready!" message
- ✅ Ability to send emails with PDF attachments
- ✅ Confirmation message when email is sent

---

**Need help?** Check the configuration status in the app's "Email Setup Instructions" section.

**Cost:** $0 - Completely FREE with Gmail!
