# Lesson 4.5: Password Management - Keeping Passwords Safe! 🔐

## What is Password Management? 🎯

**Password Management** = Helping users manage their passwords safely!

This includes:
- Changing passwords
- Resetting forgotten passwords
- Security best practices
- Password strength requirements

## Why Do We Need Password Management? 🤔

### Common Scenarios:

1. **User forgets password** → Need reset functionality
2. **User wants to change password** → Need change functionality
3. **Security concerns** → Need to enforce strong passwords
4. **Account security** → Need to verify identity

## Changing Passwords 🔄

### What is Password Change?

**Password Change** = User wants to update their password (while logged in)

### Step 1: Create Change Password Form

```python
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', 
                                   validators=[DataRequired()])
    new_password = PasswordField('New Password', 
                                validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password',
                                    validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
```

### Step 2: Change Password Route

```python
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verify current password
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('Current password is incorrect!', 'error')
            return render_template_string(change_password_template, form=form)
        
        # Update password
        current_user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template_string(change_password_template, form=form)
```

## Resetting Forgotten Passwords 🔓

### What is Password Reset?

**Password Reset** = User forgot password, needs to create a new one

### The Process:

1. User enters email
2. Website sends reset link (via email)
3. User clicks link
4. User enters new password
5. Password is updated

### Step 1: Create Reset Request Form

```python
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
```

### Step 2: Generate Reset Token

We need a secure token for the reset link:

```python
import secrets
from datetime import datetime, timedelta

# Add to User model
class User(db.Model, UserMixin):
    # ... existing fields ...
    reset_token = db.Column(db.String(100))
    reset_token_expires = db.Column(db.DateTime)
    
    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        if not self.reset_token or self.reset_token != token:
            return False
        if datetime.utcnow() > self.reset_token_expires:
            return False
        return True
```

### Step 3: Reset Password Routes

```python
# Request reset
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            # In real app, send email with reset link
            reset_url = url_for('reset_password', token=token, _external=True)
            flash(f'Reset link: {reset_url}', 'info')  # For testing
            # In production: send_email(user.email, reset_url)
        else:
            # Don't reveal if email exists (security)
            flash('If that email exists, a reset link has been sent.', 'info')
        return redirect(url_for('login'))
    
    return render_template_string(reset_request_template, form=form)

# Actual reset
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Find user with this token
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset token!', 'error')
        return redirect(url_for('reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(reset_password_template, form=form)
```

## Security Best Practices 🔒

### 1. Password Strength Requirements

```python
import re

def is_strong_password(password):
    """Check if password meets strength requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"
```

### 2. Rate Limiting (Prevent Brute Force)

```python
from datetime import datetime, timedelta

# Add to User model
class User(db.Model, UserMixin):
    # ... existing fields ...
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    def is_locked(self):
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False
    
    def lock_account(self, minutes=15):
        self.locked_until = datetime.utcnow() + timedelta(minutes=minutes)
        db.session.commit()
    
    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()
```

### 3. Secure Password Reset

```python
# Don't reveal if email exists
if user:
    # Send reset email
    pass
else:
    # Still show success message (don't reveal email doesn't exist)
    flash('If that email exists, a reset link has been sent.', 'info')
```

### 4. Token Expiration

```python
# Tokens should expire (1 hour is common)
reset_token_expires = datetime.utcnow() + timedelta(hours=1)
```

## Complete Password Management Example 🎯

```python
from flask import Flask, render_template_string, redirect, url_for, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime, timedelta
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(100))
    reset_token_expires = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        if not self.reset_token or self.reset_token != token:
            return False
        if datetime.utcnow() > self.reset_token_expires:
            return False
        return True

# Forms
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password',
                                    validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# Create tables
with app.app_context():
    db.create_all()

# Change password route
@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('Current password is incorrect!', 'error')
            return render_template_string(change_password_template, form=form)
        
        current_user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template_string(change_password_template, form=form)

# Request password reset
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            reset_url = url_for('reset_password', token=token, _external=True)
            flash(f'Reset link: {reset_url}', 'info')  # For testing
        else:
            flash('If that email exists, a reset link has been sent.', 'info')
        return redirect(url_for('login'))
    
    return render_template_string(reset_request_template, form=form)

# Reset password
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset token!', 'error')
        return redirect(url_for('reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(reset_password_template, form=form)

# Templates (simplified for example)
change_password_template = '''
<h2>Change Password</h2>
<form method="POST">
    {{ form.hidden_tag() }}
    <p>{{ form.current_password.label }}<br>{{ form.current_password() }}</p>
    <p>{{ form.new_password.label }}<br>{{ form.new_password() }}</p>
    <p>{{ form.confirm_password.label }}<br>{{ form.confirm_password() }}</p>
    <p>{{ form.submit() }}</p>
</form>
'''

reset_request_template = '''
<h2>Reset Password</h2>
<p>Enter your email to receive a password reset link.</p>
<form method="POST">
    {{ form.hidden_tag() }}
    <p>{{ form.email.label }}<br>{{ form.email() }}</p>
    <p>{{ form.submit() }}</p>
</form>
'''

reset_password_template = '''
<h2>Reset Password</h2>
<form method="POST">
    {{ form.hidden_tag() }}
    <p>{{ form.password.label }}<br>{{ form.password() }}</p>
    <p>{{ form.confirm_password.label }}<br>{{ form.confirm_password() }}</p>
    <p>{{ form.submit() }}</p>
</form>
'''

if __name__ == '__main__':
    app.run(debug=True)
```

## Security Checklist ✅

### Password Storage:
- ✅ Always hash passwords (never plain text)
- ✅ Use strong hashing (Werkzeug's generate_password_hash)
- ✅ Never store passwords in plain text

### Password Reset:
- ✅ Use secure tokens (secrets.token_urlsafe)
- ✅ Set expiration times (1 hour is common)
- ✅ Don't reveal if email exists
- ✅ Verify token before allowing reset

### Password Change:
- ✅ Verify current password first
- ✅ Require strong passwords
- ✅ Confirm new password matches

### General Security:
- ✅ Use HTTPS in production
- ✅ Rate limit login attempts
- ✅ Lock accounts after failed attempts
- ✅ Log security events

## Common Mistakes 🔧

### Mistake 1: Not Hashing Passwords

```python
# ❌ DANGEROUS!
user.password = new_password

# ✅ CORRECT!
user.password_hash = generate_password_hash(new_password)
```

### Mistake 2: Revealing Email Existence

```python
# ❌ Reveals if email exists
if not user:
    flash('Email not found!', 'error')

# ✅ Doesn't reveal
flash('If that email exists, a reset link has been sent.', 'info')
```

### Mistake 3: No Token Expiration

```python
# ❌ Token never expires
reset_token = secrets.token_urlsafe(32)

# ✅ Token expires
reset_token_expires = datetime.utcnow() + timedelta(hours=1)
```

## What You Learned! 📚

✅ How to change passwords  
✅ How to reset forgotten passwords  
✅ How to generate secure tokens  
✅ How to verify reset tokens  
✅ Security best practices  
✅ Password strength requirements  
✅ Rate limiting basics  

## Key Concepts 💡

1. **Password Change** = Update password while logged in
2. **Password Reset** = Create new password when forgotten
3. **Reset Token** = Secure code for password reset
4. **Token Expiration** = Tokens should expire for security
5. **Password Strength** = Requirements for strong passwords

## What's Next? 🚀

Congratulations! You've completed Module 4! You now know:
- ✅ User registration
- ✅ User login
- ✅ Flask-Login
- ✅ Password management

**Next Module**: RESTful APIs - Learn how to build APIs for your applications!

---

**Amazing! You're now a security expert! 🎉**

