# Lesson 4.2: User Registration - Letting Users Sign Up! 📝

## What is User Registration? 🎯

**User Registration** = Creating a new account on your website!

Think of it like:
- **Registration** = Getting a library card (first time)
- **Login** = Using your library card (every time after)

## What We Need for Registration 📋

To register a user, we need:

1. **User Model** - Database table to store users
2. **Registration Form** - Form for users to fill out
3. **Password Hashing** - Secure way to store passwords
4. **Validation** - Check if data is correct
5. **Save to Database** - Store the new user

## Step 1: Create User Model 👤

First, let's create a database model to store users:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

### Breaking It Down:

- **`username`** = User's chosen name (unique - no duplicates!)
- **`email`** = User's email (unique - no duplicates!)
- **`password_hash`** = Hashed password (NOT the actual password!)
- **`created_at`** = When account was created

**Important**: We store `password_hash`, NOT the actual password!

## Step 2: Understanding Password Hashing 🔒

### Why Hash Passwords?

**NEVER store passwords in plain text!**

❌ **Dangerous**:
```python
password = "mypassword123"  # Anyone can see this!
```

✅ **Safe**:
```python
password_hash = "$2b$12$abc123...xyz789"  # Secret code!
```

### How Hashing Works:

```
User enters: "mypassword123"
    ↓
Website hashes it: "$2b$12$abc123...xyz789"
    ↓
Website saves hash (NOT the password!)
```

**Even if someone sees the hash, they can't get the password back!**

## Step 3: Install Werkzeug (Password Hashing) 📦

Werkzeug is a tool that helps hash passwords:

```bash
pip install werkzeug
```

**Werkzeug** = Tool for password hashing (comes with Flask, but we'll use it directly)

## Step 4: Hash Passwords 🔐

Let's learn how to hash passwords:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash a password
password = "mypassword123"
password_hash = generate_password_hash(password)
print(password_hash)
# Output: $2b$12$abc123...xyz789 (secret code!)

# Check if password matches hash
is_correct = check_password_hash(password_hash, "mypassword123")
print(is_correct)  # True

is_wrong = check_password_hash(password_hash, "wrongpassword")
print(is_wrong)  # False
```

### Understanding the Functions:

- **`generate_password_hash(password)`** = Converts password to hash
- **`check_password_hash(hash, password)`** = Checks if password matches hash

## Step 5: Create Registration Form 📝

Let's create a form for registration:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
```

### Form Fields Explained:

- **`username`** = User's chosen name (3-20 characters)
- **`email`** = Must be valid email format
- **`password`** = Must be at least 8 characters
- **`confirm_password`** = Must match password

## Step 6: Complete Registration Route 🛣️

Now let's put it all together:

```python
from flask import Flask, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Create tables
with app.app_context():
    db.create_all()

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!', 'error')
            return render_template_string(registration_template, form=form)
        
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered!', 'error')
            return render_template_string(registration_template, form=form)
        
        # Hash the password
        password_hash = generate_password_hash(form.password.data)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash
        )
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(registration_template, form=form)

# Simple login route (we'll improve this later)
@app.route('/login')
def login():
    return "Login page (coming in next lesson!)"

# Registration template
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
        
        <p>
            {{ form.username.label }}<br>
            {{ form.username() }}
            {% if form.username.errors %}
                {% for error in form.username.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>
            {{ form.email.label }}<br>
            {{ form.email() }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>
            {{ form.password.label }}<br>
            {{ form.password() }}
            {% if form.password.errors %}
                {% for error in form.password.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>
            {{ form.confirm_password.label }}<br>
            {{ form.confirm_password() }}
            {% if form.confirm_password.errors %}
                {% for error in form.confirm_password.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>{{ form.submit() }}</p>
    </form>
    
    <p>Already have an account? <a href="/login">Login</a></p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding the Registration Process 🔄

### Step-by-Step:

1. **User visits `/register`**
   - Sees registration form

2. **User fills form and submits**
   - Enters username, email, password, confirm password

3. **Form validation**
   - Checks if all fields are filled
   - Checks if email is valid
   - Checks if password is long enough
   - Checks if passwords match

4. **Check for duplicates**
   - Is username already taken?
   - Is email already registered?

5. **Hash password**
   - Convert password to hash
   - Never store actual password!

6. **Create user**
   - Save to database
   - Commit changes

7. **Success!**
   - Show success message
   - Redirect to login page

## Security Best Practices 🔒

### 1. Always Hash Passwords

```python
# ❌ NEVER do this!
user.password = form.password.data

# ✅ Always do this!
user.password_hash = generate_password_hash(form.password.data)
```

### 2. Validate Input

```python
# Check if username exists
if User.query.filter_by(username=form.username.data).first():
    flash('Username taken!', 'error')
```

### 3. Use Strong Passwords

```python
# Require minimum length
validators=[Length(min=8)]
```

### 4. Check Email Format

```python
# Validate email
validators=[Email()]
```

## Common Mistakes 🔧

### Mistake 1: Storing Plain Password

```python
# ❌ DANGEROUS!
user.password = form.password.data

# ✅ CORRECT!
user.password_hash = generate_password_hash(form.password.data)
```

### Mistake 2: Not Checking for Duplicates

```python
# ❌ Allows duplicate usernames
user = User(username=form.username.data, ...)

# ✅ Check first!
if User.query.filter_by(username=form.username.data).first():
    return "Username taken!"
```

### Mistake 3: Not Validating Password Match

```python
# ❌ No check
password = form.password.data
confirm = form.confirm_password.data

# ✅ Use EqualTo validator
confirm_password = PasswordField('Confirm Password',
                                validators=[EqualTo('password')])
```

## Practice Exercise 🏋️

Create a registration system that:

1. Has username, email, password fields
2. Validates all inputs
3. Checks for duplicate usernames/emails
4. Hashes passwords before saving
5. Shows success/error messages

**Try it yourself!**

## What You Learned! 📚

✅ How to create a user model  
✅ Why we hash passwords  
✅ How to hash passwords with Werkzeug  
✅ How to create registration forms  
✅ How to validate user input  
✅ How to check for duplicate users  
✅ How to save users to database securely  

## Key Concepts 💡

1. **Password Hashing** = Converting password to secret code
2. **`generate_password_hash()`** = Creates hash from password
3. **`check_password_hash()`** = Verifies password matches hash
4. **Validation** = Checking if data is correct
5. **Unique constraints** = No duplicate usernames/emails

## What's Next? 🚀

Now that users can register, let's learn how to **log them in** - authenticating users and creating sessions!

---

**Excellent! You can now create user accounts securely! 🎉**

