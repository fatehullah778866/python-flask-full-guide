# Project 13: Contact Form with Email 📧

Welcome to Project 13! This app sends emails from a contact form!

## What is This Project? 🤔

**Contact Form with Email** = An app that sends emails when users submit a contact form!

**Think of it like:**
- **Contact Form** = Form to send messages
- **Email** = Sends message via email
- **SMTP** = Protocol for sending emails

**Email = Sending messages over the internet!**

## What You'll Learn 📚

✅ Email sending (Flask-Mail)
✅ SMTP configuration
✅ Email message creation
✅ Error handling for emails
✅ Environment variables
✅ Email security

## What This App Does 🎯

1. **Display Form** - Shows contact form
2. **Get Form Data** - Receives user input
3. **Send Email** - Sends email with form data
4. **Show Result** - Displays success or error

**Features:**
- 📧 Send emails via contact form
- ✅ Form validation
- 🔒 Secure email sending (TLS)
- 📝 Formatted email messages
- ⚠️ Error handling

## Step-by-Step Explanation 📖

### Step 1: Configure Flask-Mail
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
```
**What this does:**
- Sets up email server
- Configures port and encryption
- Enables secure email sending

**Simple explanation:**
- Configuration = Email settings
- SMTP = Email server!

### Step 2: Create Email Message
```python
msg = Message(
    subject='Contact Form: ' + subject,
    sender=app.config['MAIL_USERNAME'],
    recipients=[app.config['MAIL_USERNAME']],
    body=message_content
)
```
**What this does:**
- Creates email message
- Sets subject, sender, recipients
- Adds message body

**Simple explanation:**
- Message = Email letter
- Fill in details!

### Step 3: Send Email
```python
mail.send(msg)
```
**What this does:**
- Actually sends the email
- Through SMTP server
- Delivers to recipient

**Simple explanation:**
- Send = Deliver email
- Through server!

## Key Concepts 🎓

### 1. SMTP

**What is SMTP?**
- Simple Mail Transfer Protocol
- How emails are sent
- Server-based system

**SMTP Server:**
- Gmail: smtp.gmail.com
- Outlook: smtp-mail.outlook.com
- Yahoo: smtp.mail.yahoo.com

### 2. Flask-Mail

**What is Flask-Mail?**
- Flask extension for emails
- Easy email sending
- Handles SMTP complexity

**Features:**
- Simple API
- Secure sending
- Error handling

### 3. Email Security

**TLS Encryption:**
- Transport Layer Security
- Encrypts email transmission
- Keeps emails secure

**App Passwords:**
- Special passwords for apps
- More secure than regular passwords
- Required for Gmail

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Email
Set environment variables:
```bash
# Windows:
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-app-password

# Mac/Linux:
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password
3. Use App Password (not regular password)

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Fill in contact form
2. Click "Send Message"
3. Email is sent!

## Files in This Project 📁

```
13-contact-form-email/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Contact form
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Configure your email settings
2. ✅ Test sending emails
3. ✅ Move to Project 14: File Upload App

---

**Ready for the next project? Try Project 14: File Upload App!**

