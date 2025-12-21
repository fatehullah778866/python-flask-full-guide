# Lesson 4.4: Flask-Login - The Easy Way! 🎁

## What is Flask-Login? 🤔

**Flask-Login** is like a **helper** that makes authentication much easier!

### The Problem with Basic Sessions:

- ❌ Manual session management
- ❌ Checking login in every route
- ❌ More code to write
- ❌ Easy to make mistakes

### The Solution: Flask-Login

- ✅ Automatic session management
- ✅ Easy route protection
- ✅ Less code to write
- ✅ Built-in security features

**Flask-Login makes authentication simple!**

## Installing Flask-Login 📦

```bash
pip install flask-login
```

That's it! Flask-Login is now installed.

## Setting Up Flask-Login ⚙️

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Where to redirect if not logged in
```

### Breaking It Down:

- **`LoginManager()`** = Creates the login manager
- **`init_app(app)`** = Connects to Flask app
- **`login_view = 'login'`** = Redirect here if not logged in

## Updating User Model 👤

Flask-Login needs your User model to have certain methods:

```python
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

### What Changed:

- **`UserMixin`** = Adds required methods automatically
- Flask-Login needs: `is_authenticated`, `is_active`, `get_id()`
- **`UserMixin`** provides all of these!

## User Loader Function 🔄

Flask-Login needs a function to load users:

```python
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### What This Does:

- **`@login_manager.user_loader`** = Tells Flask-Login how to load users
- **`load_user(user_id)`** = Gets user from database by ID
- Flask-Login calls this automatically!

## Logging Users In and Out 🔓

### Login:

```python
from flask_login import login_user

# After verifying password
if user and check_password_hash(user.password_hash, password):
    login_user(user)  # That's it!
    return redirect(url_for('dashboard'))
```

### Logout:

```python
from flask_login import logout_user

@app.route('/logout')
def logout():
    logout_user()  # That's it!
    return redirect(url_for('login'))
```

**Much simpler than manual sessions!**

## Protecting Routes 🔒

### Using `@login_required`:

```python
from flask_login import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard"
```

**That's it!** Flask-Login automatically:
- Checks if user is logged in
- Redirects to login if not
- Shows flash message

## Accessing Current User 👤

### Using `current_user`:

```python
from flask_login import current_user

@app.route('/profile')
@login_required
def profile():
    # current_user is automatically the logged-in user!
    return f"Hello, {current_user.username}!"
```

**No need to get user from session!**

## Complete Flask-Login Example 🎯

```python
from flask import Flask, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model with UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

# Create tables
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return '<h1>Welcome! <a href="/login">Login</a> or <a href="/register">Register</a></h1>'

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!', 'error')
            return render_template_string(registration_template, form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered!', 'error')
            return render_template_string(registration_template, form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(registration_template, form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template_string(login_template, form=form)

# Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return f'''
    <h1>Dashboard</h1>
    <p>Welcome, {current_user.username}!</p>
    <p>Email: {current_user.email}</p>
    <a href="/profile">Profile</a> | 
    <a href="/logout">Logout</a>
    '''

# Profile (protected)
@app.route('/profile')
@login_required
def profile():
    return f'''
    <h1>Profile</h1>
    <p>Username: {current_user.username}</p>
    <p>Email: {current_user.email}</p>
    <p>Member since: {current_user.created_at.strftime("%Y-%m-%d")}</p>
    <a href="/dashboard">Back</a> | 
    <a href="/logout">Logout</a>
    '''

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Templates
login_template = '''
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {% if category == 'error' %}red{% else %}green{% endif %};">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    <p>Don't have an account? <a href="/register">Register</a></p>
</body>
</html>
'''

registration_template = '''
<html>
<head><title>Register</title></head>
<body>
    <h2>Register</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {% if category == 'error' %}red{% else %}green{% endif %};">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.username.label }}<br>{{ form.username() }}</p>
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    <p>Already have an account? <a href="/register">Login</a></p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding `current_user` 👤

### Properties of `current_user`:

```python
# Check if user is logged in
if current_user.is_authenticated:
    # User is logged in!
    username = current_user.username

# Check if user is active
if current_user.is_active:
    # User account is active

# Get user ID
user_id = current_user.id
```

### Using in Templates:

```python
# In your route
return render_template('dashboard.html', user=current_user)

# In template
{% if current_user.is_authenticated %}
    <p>Hello, {{ current_user.username }}!</p>
{% endif %}
```

## Remember Me with Flask-Login 💾

```python
from flask_login import login_user

# Login with remember me
if form.remember_me.data:
    login_user(user, remember=True)  # Remember for 1 year
else:
    login_user(user, remember=False)  # Forget when browser closes
```

## Benefits of Flask-Login ✨

### 1. Less Code

**Without Flask-Login:**
```python
if not session.get('logged_in'):
    return redirect(url_for('login'))
user = User.query.get(session['user_id'])
```

**With Flask-Login:**
```python
@login_required
def dashboard():
    return f"Hello, {current_user.username}!"
```

### 2. Automatic Protection

```python
@login_required  # That's it! Route is protected!
def protected():
    return "Protected content"
```

### 3. Easy User Access

```python
current_user.username  # No need to query database!
```

## Common Mistakes 🔧

### Mistake 1: Forgetting UserMixin

```python
# ❌ Missing UserMixin
class User(db.Model):

# ✅ Include UserMixin
class User(db.Model, UserMixin):
```

### Mistake 2: Forgetting User Loader

```python
# ❌ Flask-Login doesn't know how to load users!
# ✅ Must have user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### Mistake 3: Not Using login_user()

```python
# ❌ Manual session
session['user_id'] = user.id

# ✅ Use Flask-Login
login_user(user)
```

## What You Learned! 📚

✅ What Flask-Login is and why it's better  
✅ How to set up Flask-Login  
✅ How to use UserMixin  
✅ How to create user loader  
✅ How to log users in and out  
✅ How to protect routes  
✅ How to access current user  
✅ How to use remember me  

## Key Concepts 💡

1. **Flask-Login** = Extension that makes authentication easier
2. **UserMixin** = Adds required methods to User model
3. **user_loader** = Function to load users from database
4. **login_user()** = Logs user in
5. **logout_user()** = Logs user out
6. **@login_required** = Protects routes
7. **current_user** = Currently logged-in user

## What's Next? 🚀

You now know professional authentication! Next, we'll learn about **password management** - resetting passwords, changing passwords, and security best practices!

---

**Excellent! You're using professional authentication tools! 🎉**

