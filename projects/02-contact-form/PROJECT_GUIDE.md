# Complete Guide: Building a Contact Form with File Upload 📚

## Welcome! 👋

This guide will teach you EVERYTHING about building a contact form. We'll learn about forms, file uploads, and validation step by step!

## Part 1: Understanding Forms 📝

### What is a Form?

**Form** = A way for users to send you information

Think of it like:
- **Form** = A questionnaire
- **User** = Fills it out
- **Website** = Receives the information
- **You** = See what they wrote!

**Forms = Collect information from users!**

### What Information Do We Need?

For a contact form, we need:
1. **Name** - Who is contacting you
2. **Email** - How to reply
3. **Message** - What they want to say
4. **File** (optional) - They can attach something

**4 fields = Complete contact form!**

## Part 2: Understanding HTTP Methods 🔄

### GET vs POST

**GET** = Getting information (like reading a page)
**POST** = Sending information (like submitting a form)

Think of it like:
- **GET** = Looking at a menu (just viewing)
- **POST** = Ordering food (sending your order)

**Forms use POST to send data!**

### Why POST for Forms?

- **GET** = Data visible in URL (not secure!)
- **POST** = Data sent securely (better!)

**POST = Secure way to send form data!**

## Part 3: Creating the Flask App 🚀

### What is app.py?

**app.py** = The brain of your application

It will:
- Show the contact form
- Receive form data
- Save messages
- Handle file uploads

### Basic app.py Structure:

```python
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # For flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Where files go
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file

# Allowed file types
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    """Check if file type is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes will go here...

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
```

**Let's understand each part:**

1. **`from flask import ...`** = Get Flask tools we need
2. **`app = Flask(__name__)`** = Create Flask app
3. **`UPLOAD_FOLDER`** = Where uploaded files are saved
4. **`ALLOWED_EXTENSIONS`** = What file types are safe
5. **`allowed_file()`** = Check if file is safe

**Security = Only allow safe file types!**

## Part 4: Creating the Contact Form 📋

### HTML Form Structure:

**`templates/contact.html`:**
```html
{% extends "base.html" %}

{% block title %}Contact Me{% endblock %}

{% block content %}
<div class="container">
    <h1>Contact Me</h1>
    <p>Fill out the form below to send me a message!</p>
    
    <!-- Display flash messages (success/error) -->
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="flash-messages">
                {% for message in messages %}
                    <div class="flash-message">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}
    
    <!-- Contact Form -->
    <form method="POST" action="/contact" enctype="multipart/form-data" class="contact-form">
        <!-- Name Field -->
        <div class="form-group">
            <label for="name">Your Name:</label>
            <input 
                type="text" 
                id="name" 
                name="name" 
                required 
                placeholder="Enter your name"
                value="{{ request.form.name if request.form else '' }}"
            >
        </div>
        
        <!-- Email Field -->
        <div class="form-group">
            <label for="email">Your Email:</label>
            <input 
                type="email" 
                id="email" 
                name="email" 
                required 
                placeholder="your.email@example.com"
                value="{{ request.form.email if request.form else '' }}"
            >
        </div>
        
        <!-- Message Field -->
        <div class="form-group">
            <label for="message">Your Message:</label>
            <textarea 
                id="message" 
                name="message" 
                rows="5" 
                required 
                placeholder="Type your message here..."
            >{{ request.form.message if request.form else '' }}</textarea>
        </div>
        
        <!-- File Upload Field -->
        <div class="form-group">
            <label for="file">Attach File (optional):</label>
            <input 
                type="file" 
                id="file" 
                name="file"
                accept=".txt,.pdf,.png,.jpg,.jpeg,.gif,.doc,.docx"
            >
            <small>Allowed: txt, pdf, png, jpg, gif, doc, docx (max 16MB)</small>
        </div>
        
        <!-- Submit Button -->
        <button type="submit" class="btn">Send Message</button>
    </form>
</div>
{% endblock %}
```

**What's happening:**

1. **`method="POST"`** = Send data securely
2. **`enctype="multipart/form-data"`** = Needed for file uploads
3. **`required`** = Field must be filled
4. **`type="email"`** = Validates email format
5. **`accept="..."`** = Only allow certain file types

**Form = Collects all the information!**

## Part 5: Handling Form Submission 📨

### Processing the Form:

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        file = request.files.get('file')
        
        # Validate data
        errors = []
        
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Invalid email address')
        if not message:
            errors.append('Message is required')
        
        # Handle file upload
        filename = None
        if file and file.filename:
            if allowed_file(file.filename):
                # Make filename safe
                filename = secure_filename(file.filename)
                # Add timestamp to avoid duplicates
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                # Save file
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                errors.append('File type not allowed')
        
        # If there are errors, show them
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html')
        
        # Save message
        save_message(name, email, message, filename)
        
        # Success!
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    # GET request - show form
    return render_template('contact.html')
```

**What's happening:**

1. **Check method** = Is it POST (form submitted)?
2. **Get data** = Extract form fields
3. **Validate** = Check if data is correct
4. **Handle file** = Save uploaded file
5. **Save message** = Store the message
6. **Show success** = Tell user it worked!

**Validation = Make sure data is correct!**

## Part 6: Saving Messages 💾

### Saving to JSON File:

```python
def save_message(name, email, message, filename=None):
    """Save message to JSON file"""
    message_data = {
        'id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'name': name,
        'email': email,
        'message': message,
        'filename': filename,
        'timestamp': datetime.now().isoformat()
    }
    
    # Load existing messages
    messages_file = 'data/messages.json'
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            messages = json.load(f)
    else:
        messages = []
    
    # Add new message
    messages.append(message_data)
    
    # Save back to file
    with open(messages_file, 'w') as f:
        json.dump(messages, f, indent=2)
```

**JSON = Simple way to store data!**

## Part 7: Viewing Messages 📬

### Display All Messages:

```python
@app.route('/messages')
def messages():
    """Display all received messages"""
    messages_file = 'data/messages.json'
    
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            messages = json.load(f)
        # Sort by timestamp (newest first)
        messages.sort(key=lambda x: x['timestamp'], reverse=True)
    else:
        messages = []
    
    return render_template('messages.html', messages=messages)
```

### Messages Template:

**`templates/messages.html`:**
```html
{% extends "base.html" %}

{% block title %}Messages{% endblock %}

{% block content %}
<div class="container">
    <h1>Received Messages</h1>
    
    {% if messages %}
        <div class="messages-list">
            {% for msg in messages %}
                <div class="message-card">
                    <div class="message-header">
                        <h3>{{ msg.name }}</h3>
                        <span class="timestamp">{{ msg.timestamp[:19] }}</span>
                    </div>
                    <p class="email">{{ msg.email }}</p>
                    <p class="message">{{ msg.message }}</p>
                    {% if msg.filename %}
                        <p class="file">
                            <strong>Attachment:</strong> 
                            <a href="{{ url_for('static', filename='uploads/' + msg.filename) }}" target="_blank">
                                {{ msg.filename }}
                            </a>
                        </p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>No messages yet!</p>
    {% endif %}
    
    <a href="/contact" class="btn">Send New Message</a>
</div>
{% endblock %}
```

**Messages = See all received messages!**

## Part 8: File Upload Security 🔒

### Why Security Matters:

**Dangerous files** = Can harm your server!

**We protect by:**
1. **Checking file type** = Only allow safe types
2. **Renaming files** = Prevent overwriting
3. **Limiting size** = Prevent huge files
4. **Using secure_filename** = Remove dangerous characters

### Secure File Handling:

```python
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In route:
if file and file.filename:
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

**Security = Keep your server safe!**

## Part 9: Adding CSS Styling 🎨

### Beautiful Form Styling:

**`static/style.css`:**
```css
/* Form Styles */
.contact-form {
    max-width: 600px;
    margin: 2rem auto;
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #333;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #3498db;
}

.form-group small {
    display: block;
    margin-top: 0.25rem;
    color: #666;
    font-size: 0.875rem;
}

.btn {
    background-color: #3498db;
    color: white;
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #2980b9;
}

/* Flash Messages */
.flash-messages {
    margin-bottom: 1rem;
}

.flash-message {
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 0.5rem;
}

.flash-message.success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.flash-message.error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* Messages List */
.messages-list {
    display: grid;
    gap: 1.5rem;
    margin-top: 2rem;
}

.message-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.timestamp {
    color: #666;
    font-size: 0.875rem;
}

.email {
    color: #3498db;
    margin-bottom: 1rem;
}

.message {
    margin-bottom: 1rem;
    line-height: 1.6;
}

.file a {
    color: #3498db;
    text-decoration: none;
}

.file a:hover {
    text-decoration: underline;
}
```

**CSS = Makes everything beautiful!**

## Part 10: Complete app.py 🎯

### Full Application Code:

```python
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_message(name, email, message, filename=None):
    message_data = {
        'id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'name': name,
        'email': email,
        'message': message,
        'filename': filename,
        'timestamp': datetime.now().isoformat()
    }
    
    messages_file = 'data/messages.json'
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            messages = json.load(f)
    else:
        messages = []
    
    messages.append(message_data)
    
    with open(messages_file, 'w') as f:
        json.dump(messages, f, indent=2)

@app.route('/')
def home():
    return redirect(url_for('contact'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        file = request.files.get('file')
        
        errors = []
        
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Invalid email address')
        if not message:
            errors.append('Message is required')
        
        filename = None
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                errors.append('File type not allowed')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html')
        
        save_message(name, email, message, filename)
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/messages')
def messages():
    messages_file = 'data/messages.json'
    if os.path.exists(messages_file):
        with open(messages_file, 'r') as f:
            messages_list = json.load(f)
        messages_list.sort(key=lambda x: x['timestamp'], reverse=True)
    else:
        messages_list = []
    
    return render_template('messages.html', messages=messages_list)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
```

## What You've Learned! 🎓

✅ How to create HTML forms  
✅ How to handle form submissions  
✅ How to validate form data  
✅ How to handle file uploads  
✅ How to secure file uploads  
✅ How to store and display messages  
✅ How to use flash messages  

## Next Steps 🚀

1. **Customize** - Change form fields
2. **Add validation** - More checks
3. **Style** - Make it prettier
4. **Deploy** - Put it online!

---

**Congratulations! You built a contact form! 🎉**

