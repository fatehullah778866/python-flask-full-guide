# Lesson 8.2: Flask Security Features - Built-in Protection! 🛡️

## What are Flask Security Features? 🤔

**Flask Security Features** = Tools Flask gives you to stay safe

Think of it like:
- **Flask** = A house builder
- **Security Features** = Locks, alarms, security cameras
- **You** = Use these features to protect your house

**Flask Security = Built-in tools to protect your app!**

## CSRF Protection 🔒

### What is CSRF?

**CSRF** = Cross-Site Request Forgery

**The Attack**:
1. User is logged into your site
2. Hacker sends user to bad website
3. Bad website makes request to your site
4. Your site thinks it's the user
5. Bad things happen!

**CSRF = Tricking users into doing things they don't want!**

### How Flask-WTF Protects You:

Flask-WTF automatically adds CSRF protection:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class MyForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')

# In template
<form method="POST">
    {{ form.hidden_tag() }}  # This adds CSRF token!
    {{ form.name() }}
    {{ form.submit() }}
</form>
```

**`form.hidden_tag()` = Adds secret token that prevents CSRF!**

### How CSRF Token Works:

1. **User visits form** → Flask generates secret token
2. **Token stored** → In form and session
3. **User submits** → Token is sent back
4. **Flask checks** → "Is this token valid?"
5. **If valid** → Request is accepted
6. **If invalid** → Request is rejected!

**Token = Secret code that proves request is real!**

## XSS (Cross-Site Scripting) Prevention 🚫

### What is XSS?

**XSS** = Cross-Site Scripting

**The Attack**:
```
User comment: <script>alert('Hacked!')</script>
Website shows: Bad script runs!
```

**XSS = Bad scripts running on your website!**

### How Jinja2 Protects You:

Jinja2 (Flask's template engine) automatically escapes HTML:

```python
from flask import render_template

@app.route('/comment/<comment>')
def show_comment(comment):
    # Jinja2 automatically escapes HTML!
    return render_template('comment.html', comment=comment)
```

**Jinja2 = Automatically makes HTML safe!**

### Example:

```python
# User input
comment = "<script>alert('Hacked!')</script>"

# Jinja2 renders it as:
# &lt;script&gt;alert('Hacked!')&lt;/script&gt;

# Browser shows: <script>alert('Hacked!')</script>
# But doesn't RUN it! (Safe!)
```

### Manual Escaping:

```python
from markupsafe import escape

# Escape user input manually
safe_comment = escape(comment)
```

## SQL Injection Prevention 🗄️

### What is SQL Injection?

**SQL Injection** = Hacker sends bad SQL code

**The Attack**:
```python
# ❌ DANGEROUS!
username = request.form.get('username')
query = f"SELECT * FROM users WHERE name = '{username}'"
# If username = "'; DROP TABLE users; --"
# Query becomes: SELECT * FROM users WHERE name = ''; DROP TABLE users; --'
# Database gets deleted!
```

### How SQLAlchemy Protects You:

SQLAlchemy uses **parameterized queries** (safe!):

```python
# ✅ SAFE!
username = request.form.get('username')
user = User.query.filter_by(name=username).first()
# SQLAlchemy handles it safely!
```

### Manual Protection:

```python
from sqlalchemy import text

# ✅ SAFE - parameterized query
query = text("SELECT * FROM users WHERE name = :name")
result = db.session.execute(query, {"name": username})
```

**Parameterized queries = Safe way to use user input in SQL!**

## Secure Session Management 🎫

### What Makes Sessions Secure?

1. **Secret Key** - Encrypts session data
2. **Secure Cookies** - Only sent over HTTPS
3. **HttpOnly** - JavaScript can't access
4. **SameSite** - Prevents CSRF

### Secure Session Configuration:

```python
from flask import Flask, session
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Strong secret!

# Secure session settings
app.config['SESSION_COOKIE_SECURE'] = True  # Only HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Expires
```

### Understanding Session Settings:

- **`SESSION_COOKIE_SECURE`** = Only send cookie over HTTPS
- **`SESSION_COOKIE_HTTPONLY`** = JavaScript can't read cookie
- **`SESSION_COOKIE_SAMESITE`** = Prevents CSRF attacks
- **`PERMANENT_SESSION_LIFETIME`** = How long session lasts

## Complete Security Example 🎯

```python
from flask import Flask, render_template_string, request, session
from flask_wtf import FlaskForm, CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import timedelta
import os

app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only (in production)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# CSRF Protection
csrf = CSRFProtect(app)

# Database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Safe database query (SQLAlchemy prevents injection)
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session.permanent = True
            return redirect('/dashboard')
    
    return render_template_string('''
    <form method="POST">
        {{ form.hidden_tag() }}  <!-- CSRF protection -->
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    ''', form=form)

@app.route('/comment')
def show_comment():
    # User input (automatically escaped by Jinja2)
    comment = request.args.get('comment', '')
    return render_template_string('''
    <h1>Comment</h1>
    <p>{{ comment }}</p>  <!-- Automatically escaped! -->
    ''', comment=comment)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## Input Sanitization 🧹

### What is Sanitization?

**Sanitization** = Cleaning user input to make it safe

### Sanitizing User Input:

```python
from markupsafe import escape
import re

def sanitize_input(text):
    """Remove dangerous characters"""
    # Remove HTML tags
    text = escape(text)
    # Remove special characters if needed
    text = re.sub(r'[<>]', '', text)
    return text

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Sanitize before using
    safe_query = sanitize_input(query)
    # Now safe to use!
    return f"Searching for: {safe_query}"
```

## File Upload Security 📁

### Secure File Uploads:

```python
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file", 400
    
    file = request.files['file']
    
    # Validate file type
    if not allowed_file(file.filename):
        return "Invalid file type", 400
    
    # Validate file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > 5 * 1024 * 1024:  # 5MB max
        return "File too large", 400
    
    # Secure filename
    filename = secure_filename(file.filename)
    
    # Save file
    file.save(os.path.join('uploads', filename))
    return "File uploaded!"
```

## Security Headers 🔐

### Adding Security Headers:

```python
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### What Each Header Does:

- **`X-Content-Type-Options`** = Prevents MIME type sniffing
- **`X-Frame-Options`** = Prevents clickjacking
- **`X-XSS-Protection`** = Enables XSS protection
- **`Strict-Transport-Security`** = Forces HTTPS

## What You Learned! 📚

✅ What CSRF is and how to prevent it  
✅ What XSS is and how to prevent it  
✅ What SQL injection is and how to prevent it  
✅ How to secure sessions  
✅ How to sanitize input  
✅ How to secure file uploads  
✅ How to add security headers  

## Key Concepts 💡

1. **CSRF Protection** = Prevents fake requests
2. **XSS Prevention** = Prevents bad scripts
3. **SQL Injection Prevention** = Prevents bad SQL
4. **Secure Sessions** = Protected session data
5. **Input Sanitization** = Cleaning user input
6. **Security Headers** = Extra protection

## What's Next? 🚀

You now know Flask security features! Next, we'll learn about **Authentication Security** - keeping user accounts safe!

---

**Excellent! Your apps are getting more secure! 🎉**

