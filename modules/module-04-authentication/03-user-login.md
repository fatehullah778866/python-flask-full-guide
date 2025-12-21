# Lesson 4.3: User Login - Letting Users Sign In! 🔓

## What is User Login? 🎯

**User Login** = Proving you already have an account!

Think of it like:
- **Registration** = Getting a library card (first time)
- **Login** = Showing your library card (every time)

## The Login Process 🔄

### Step-by-Step:

1. **User visits login page**
   - Sees login form (email, password)

2. **User enters credentials**
   - Email and password

3. **Website checks**
   - Does this email exist?
   - Is the password correct?

4. **If correct**
   - Create session (remember user)
   - Redirect to dashboard

5. **If wrong**
   - Show error message
   - Stay on login page

## Understanding Sessions 🎫

### What is a Session?

A **session** is like a temporary ID card:

```
Login → Website creates session → You're logged in!
  ↓
Session remembers: "This is John"
  ↓
You can access protected pages
  ↓
Logout → Session deleted → You're logged out!
```

### How Sessions Work:

1. **User logs in** → Website creates session
2. **Session stored** → In a cookie (small file)
3. **Website remembers** → "This session = John's account"
4. **User stays logged in** → Until logout or session expires

## Step 1: Create Login Form 📝

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
```

### Form Fields:

- **`email`** = User's email address
- **`password`** = User's password
- **`remember_me`** = Stay logged in longer (optional)

## Step 2: Verify Password 🔐

To check if password is correct:

```python
from werkzeug.security import check_password_hash

# Get user from database
user = User.query.filter_by(email=form.email.data).first()

# Check if password matches
if user and check_password_hash(user.password_hash, form.password.data):
    # Password is correct!
    return "Login successful!"
else:
    # Password is wrong!
    return "Invalid email or password!"
```

### Understanding:

- **`User.query.filter_by(email=...)`** = Find user by email
- **`check_password_hash()`** = Compare password with hash
- **Returns True** = Password matches!
- **Returns False** = Password wrong!

## Step 3: Create Session 🎫

After successful login, create a session:

```python
from flask import session

# After password is verified
session['user_id'] = user.id
session['username'] = user.username
session['logged_in'] = True
```

### What This Does:

- **`session['user_id']`** = Stores user's ID
- **`session['username']`** = Stores username
- **`session['logged_in']`** = Marks user as logged in

**Now the website remembers you!**

## Step 4: Complete Login Route 🛣️

Let's put it all together:

```python
from flask import Flask, render_template_string, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup (same as registration)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model (same as before)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, form.password.data):
            # Create session
            session['user_id'] = user.id
            session['username'] = user.username
            session['logged_in'] = True
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template_string(login_template, form=form)

# Dashboard route (protected - requires login)
@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    username = session.get('username')
    return f'''
    <h1>Welcome, {username}!</h1>
    <p>You are logged in!</p>
    <a href="/logout">Logout</a>
    '''

# Logout route
@app.route('/logout')
def logout():
    # Clear session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Login template
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
            {{ form.remember_me() }} {{ form.remember_me.label }}
        </p>
        
        <p>{{ form.submit() }}</p>
    </form>
    
    <p>Don't have an account? <a href="/register">Register</a></p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding Session Management 🎫

### Checking if User is Logged In:

```python
# Check if logged in
if session.get('logged_in'):
    # User is logged in!
    username = session.get('username')
else:
    # User is not logged in
    return redirect(url_for('login'))
```

### Getting Current User:

```python
# Get user ID from session
user_id = session.get('user_id')

# Get user from database
user = User.query.get(user_id)
```

### Clearing Session (Logout):

```python
# Clear all session data
session.clear()

# Or clear specific items
session.pop('user_id', None)
session.pop('username', None)
session.pop('logged_in', None)
```

## Protecting Routes (Login Required) 🔒

### Method 1: Check in Each Route

```python
@app.route('/protected')
def protected():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Protected content here
    return "This is protected!"
```

### Method 2: Create Decorator (Better!)

```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Use decorator
@app.route('/protected')
@login_required
def protected():
    return "This is protected!"
```

## Remember Me Functionality 💾

"Remember Me" keeps users logged in longer:

```python
if form.remember_me.data:
    # Make session permanent (lasts longer)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)  # 30 days
else:
    # Normal session (expires when browser closes)
    session.permanent = False
```

## Complete Example with Protected Routes 🎯

```python
from flask import Flask, render_template_string, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from functools import wraps
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page (public)
@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return '<h1>Welcome! <a href="/login">Login</a> or <a href="/register">Register</a></h1>'

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['logged_in'] = True
            
            # Remember me
            if form.remember_me.data:
                session.permanent = True
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template_string(login_template, form=form)

# Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')
    return f'''
    <h1>Dashboard</h1>
    <p>Welcome, {username}!</p>
    <p>You are logged in.</p>
    <a href="/profile">View Profile</a> | 
    <a href="/logout">Logout</a>
    '''

# Profile (protected)
@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return f'''
    <h1>Profile</h1>
    <p>Username: {user.username}</p>
    <p>Email: {user.email}</p>
    <a href="/dashboard">Back to Dashboard</a> | 
    <a href="/logout">Logout</a>
    '''

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Login template (same as before)
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
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    
    <p>Don't have an account? <a href="/register">Register</a></p>
</body>
</html>
'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## Common Mistakes 🔧

### Mistake 1: Not Checking if User Exists

```python
# ❌ Error if user doesn't exist!
user = User.query.filter_by(email=email).first()
check_password_hash(user.password_hash, password)

# ✅ Check first!
user = User.query.filter_by(email=email).first()
if user and check_password_hash(user.password_hash, password):
    # Login successful
```

### Mistake 2: Not Using Session

```python
# ❌ Website doesn't remember you!
return "Login successful!"

# ✅ Create session!
session['logged_in'] = True
return redirect(url_for('dashboard'))
```

### Mistake 3: Not Protecting Routes

```python
# ❌ Anyone can access!
@app.route('/dashboard')
def dashboard():
    return "Dashboard"

# ✅ Protect it!
@app.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard"
```

## What You Learned! 📚

✅ How to create login forms  
✅ How to verify passwords  
✅ How to create sessions  
✅ How to check if user is logged in  
✅ How to protect routes  
✅ How to implement logout  
✅ How to use "Remember Me"  

## Key Concepts 💡

1. **Session** = Website remembering you're logged in
2. **`session['key']`** = Store data in session
3. **`check_password_hash()`** = Verify password
4. **Login Required** = Decorator to protect routes
5. **Remember Me** = Keep logged in longer

## What's Next? 🚀

You now know basic login! Next, we'll learn about **Flask-Login** - a better, easier way to handle authentication!

---

**Great job! You can now log users in and out! 🎉**

