# Complete Guide: Building a Blog with Authentication 📚

## Welcome! 👋

This guide will teach you EVERYTHING about adding authentication to your blog. We'll learn about passwords, sessions, and protecting routes step by step!

## Part 1: Understanding Authentication 🔐

### What is Authentication?

**Authentication** = Verifying who someone is

Think of it like:
- **Authentication** = Showing ID to prove who you are
- **Username** = Your name
- **Password** = Your secret code
- **System** = Checks if you're really you

**Authentication = Proving you are who you say you are!**

### Why Do We Need Authentication?

**Without Authentication:**
- Anyone can create/edit posts
- No way to know who wrote what
- No security

**With Authentication:**
- Only logged-in users can post
- Know who wrote each post
- Secure and protected

**Authentication = Security and control!**

## Part 2: Understanding Password Hashing 🔒

### What is Password Hashing?

**Hashing** = Converting password to secret code

Think of it like:
- **Password** = "mypassword123"
- **Hash** = "xK9#mP2$vL8@qR5" (secret code)
- **Database** = Stores the hash, NOT the password
- **Even hackers** = Can't get your password back!

**Hashing = One-way encryption (can't reverse it!)**

### Why Hash Passwords?

**Without Hashing:**
- Password stored as: "mypassword123"
- Hacker sees: "mypassword123" 😱
- Your account is hacked!

**With Hashing:**
- Password stored as: "xK9#mP2$vL8@qR5"
- Hacker sees: "xK9#mP2$vL8@qR5" (can't use it!)
- Your account is safe! ✅

**Hashing = Keeps passwords safe!**

## Part 3: Understanding Sessions 🎫

### What is a Session?

**Session** = Keeping track of logged-in users

Think of it like:
- **Session** = A wristband at an event
- **You get wristband** = When you log in
- **You show wristband** = To prove you're allowed
- **You remove wristband** = When you log out

**Session = Proof that you're logged in!**

### How Sessions Work:

1. **User logs in** → System creates session
2. **Session stored** → In browser cookie
3. **User visits pages** → System checks session
4. **If session valid** → User is logged in
5. **User logs out** → Session deleted

**Session = Remembers you're logged in!**

## Part 4: Creating the User Model 👤

### What is a User Model?

**User Model** = Structure for user accounts

Think of it like:
- **User Model** = A form for creating accounts
- **Fields** = Username, email, password
- **Each user** = One record in database

**User Model = Defines what a user account looks like!**

### Creating the User Model:

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
```

**What's happening:**

1. **`username`** = User's name (unique, required)
2. **`email`** = User's email (unique, required)
3. **`password_hash`** = Hashed password (NOT plain text!)
4. **`set_password()`** = Hash password before saving
5. **`check_password()`** = Verify password when logging in

**User Model = Stores user accounts securely!**

## Part 5: User Registration 📝

### Creating Registration Route:

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate
        errors = []
        if not username:
            errors.append('Username is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)  # Hash password
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')
```

**What's happening:**

1. **Get form data** = Username, email, password
2. **Validate** = Check if everything is correct
3. **Check duplicates** = Username/email already exists?
4. **Create user** = New User object
5. **Hash password** = Convert to secret code
6. **Save to database** = Store user account

**Registration = Creating new user accounts!**

## Part 6: User Login 🔑

### Creating Login Route:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Create session
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')
```

**What's happening:**

1. **Get credentials** = Username and password
2. **Find user** = Look in database
3. **Check password** = Verify it's correct
4. **Create session** = Store user ID in session
5. **Redirect** = Send to home page

**Login = Verifying user and creating session!**

## Part 7: Protecting Routes 🛡️

### What are Protected Routes?

**Protected Routes** = Pages only logged-in users can access

Think of it like:
- **Protected Route** = VIP area
- **Check session** = Do you have a wristband?
- **If yes** = Let them in
- **If no** = Send to login

**Protected Routes = Only for logged-in users!**

### Creating Protection Function:

```python
def login_required(f):
    """Decorator to protect routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

### Using Protection:

```python
@app.route('/create', methods=['GET', 'POST'])
@login_required  # Protect this route!
def create_post():
    if request.method == 'POST':
        # Only logged-in users can get here!
        post = Post(
            title=request.form.get('title'),
            content=request.form.get('content'),
            author=session['username']  # Use logged-in user
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')
```

**Protection = Keeps routes safe!**

## Part 8: User Logout 🚪

### Creating Logout Route:

```python
@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()  # Remove all session data
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))
```

**What's happening:**

1. **Clear session** = Remove all session data
2. **Show message** = Tell user they're logged out
3. **Redirect** = Send to home page

**Logout = End user session!**

## Part 9: Updating Post Model 📝

### Adding User Relationship:

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
```

**What's happening:**

1. **`user_id`** = Links post to user
2. **`ForeignKey`** = Database relationship
3. **`relationship`** = Easy access to user from post

**Relationship = Connect posts to users!**

## Part 10: Complete app.py 🎯

### Full Application Code:

```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        errors = []
        if not username or not email or not password:
            errors.append('All fields are required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        post = Post(
            title=request.form.get('title'),
            content=request.form.get('content'),
            author=session['username'],
            user_id=session['user_id']
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can edit
    if post.user_id != session['user_id']:
        flash('You can only edit your own posts', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.date_updated = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('view_post', post_id=post.id))
    
    return render_template('edit.html', post=post)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can delete
    if post.user_id != session['user_id']:
        flash('You can only delete your own posts', 'error')
        return redirect(url_for('index'))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## What You've Learned! 🎓

✅ What authentication is  
✅ How password hashing works  
✅ How sessions work  
✅ How to create user accounts  
✅ How to handle login  
✅ How to protect routes  
✅ How to manage sessions  
✅ How to link posts to users  

## Next Steps 🚀

1. **Customize** - Add more user fields
2. **Add roles** - Admin, moderator, etc.
3. **Password reset** - Let users reset passwords
4. **Deploy** - Put it online!

---

**Congratulations! You built a secure blog! 🎉**

