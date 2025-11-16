# 📧📱 Email & WhatsApp Integration Setup Guide

## Overview

The Road Safety Estimator now supports **automated report sharing** via:
- **Email (SMTP)** - Send PDF reports via email with automatic attachment
- **WhatsApp Business API** - Send reports via WhatsApp with PDF attachment

## Quick Start

### 1. Copy Environment Template

```bash
copy .env.example .env
```

### 2. Configure Your Credentials

Edit the `.env` file with your credentials.

---

## 📧 Email (SMTP) Setup

### Option A: Gmail (Recommended)

1. **Enable 2-Factor Authentication** in your Google Account
2. **Generate App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Update .env file:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
SMTP_FROM_EMAIL=your-email@gmail.com
```

### Option B: Outlook/Hotmail

```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_FROM_EMAIL=your-email@outlook.com
```

### Option C: Other SMTP Services

**SendGrid:**
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=your-verified-email@yourdomain.com
```

**Mailgun:**
```env
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

---

## 📱 WhatsApp Business API Setup

### Option A: Meta (Facebook) WhatsApp Business API

1. **Create Facebook Business Account:**
   - Visit: https://business.facebook.com/
   - Create or select a business

2. **Set Up WhatsApp Business API:**
   - Go to: https://developers.facebook.com/apps
   - Create a new app
   - Add "WhatsApp" product
   - Get Phone Number ID and Access Token

3. **Update .env file:**
```env
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-permanent-access-token
WHATSAPP_PHONE_ID=your-phone-number-id
```

### Option B: Twilio WhatsApp API (Easier Setup)

1. **Create Twilio Account:**
   - Visit: https://www.twilio.com/try-twilio
   - Sign up and verify your account

2. **Enable WhatsApp:**
   - Go to: https://www.twilio.com/console/sms/whatsapp/learn
   - Follow the WhatsApp Sandbox setup
   - Get your Account SID and Auth Token

3. **Update .env file:**
```env
WHATSAPP_API_URL=https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID
WHATSAPP_API_TOKEN=your-auth-token
WHATSAPP_PHONE_ID=whatsapp:+14155238886
```

### Option C: Other WhatsApp Providers

- **360Dialog:** https://www.360dialog.com/
- **MessageBird:** https://messagebird.com/
- **Vonage (Nexmo):** https://www.vonage.com/communications-apis/messages/

---

## ✅ Verify Configuration

1. **Run the application:**
```bash
venv\Scripts\python.exe -m streamlit run app.py
```

2. **Go to Report Tab**

3. **Click "Configuration Status & Setup Instructions" expander**
   - ✅ Green checkmark = Configured correctly
   - ❌ Red X = Not configured (see instructions)

---

## 🧪 Testing

### Test Email:
1. Generate a report
2. Enter your own email address
3. Click "Send via Email"
4. Check your inbox

### Test WhatsApp:
1. Generate a report
2. Enter your phone number (with country code)
3. Click "Send via WhatsApp"
4. Check WhatsApp

---

## 🔒 Security Best Practices

1. **Never commit `.env` file to Git** (already in `.gitignore`)
2. **Use App-Specific Passwords** for Gmail
3. **Rotate credentials** regularly
4. **Use environment variables** in production
5. **Restrict API access** to your IP if possible

---

## 🆘 Troubleshooting

### Email Not Sending

**Error: "SMTP authentication failed"**
- ✅ Check username/password
- ✅ For Gmail, ensure 2FA is enabled and use App Password
- ✅ Verify SMTP server and port

**Error: "Connection refused"**
- ✅ Check firewall settings
- ✅ Try port 465 (SSL) instead of 587 (TLS)

### WhatsApp Not Sending

**Error: "WhatsApp API not configured"**
- ✅ Ensure all three variables are set: API_URL, API_TOKEN, PHONE_ID
- ✅ Verify API token is valid
- ✅ Check Phone Number ID format

**Error: "401 Unauthorized"**
- ✅ Generate new access token
- ✅ Verify token has correct permissions

---

## 💡 Tips

- **Free Tier Limits:**
  - Gmail: 500 emails/day
  - Twilio WhatsApp Sandbox: Limited to pre-approved numbers
  - SendGrid: 100 emails/day (free)

- **Production Use:**
  - Consider using dedicated SMTP service (SendGrid, Mailgun)
  - Upgrade to WhatsApp Business API official account
  - Implement rate limiting

- **Bulk Sending:**
  - Add delay between messages to avoid rate limits
  - Use queue system for large-scale sending

---

## 📞 Support

For issues or questions:
- Check configuration status in the app
- Review error messages carefully
- Refer to provider's documentation:
  - [Gmail SMTP](https://support.google.com/mail/answer/7126229)
  - [Meta WhatsApp API](https://developers.facebook.com/docs/whatsapp)
  - [Twilio WhatsApp](https://www.twilio.com/docs/whatsapp)

---

## 🎯 Quick Reference

**Minimum Required for Email:**
```env
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Minimum Required for WhatsApp:**
```env
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-token
WHATSAPP_PHONE_ID=your-phone-id
```

**Both configured = Full automation with PDF attachments! 🎉**
