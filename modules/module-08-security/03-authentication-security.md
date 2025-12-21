# Lesson 8.3: Authentication Security - Keeping User Accounts Safe! 🔐

## Why Authentication Security? 🎯

**Authentication Security** = Making sure user accounts are safe

Think of it like:
- **User Account** = A safe with valuable things
- **Authentication Security** = Strong lock and alarm
- **Without Security** = Anyone can open the safe!

**Authentication Security = Protecting user accounts!**

## Password Security Best Practices 🔑

### Rule 1: Always Hash Passwords

```python
# ❌ NEVER do this!
user.password = "mypassword123"

# ✅ ALWAYS do this!
from werkzeug.security import generate_password_hash
user.password_hash = generate_password_hash("mypassword123")
```

**Hashing = Converting password to secret code that can't be reversed!**

### Rule 2: Require Strong Passwords

```python
import re

def is_strong_password(password):
    """Check if password is strong"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain a number"
    
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain special character"
    
    return True, "Password is strong"
```

### Rule 3: Never Store Passwords

```python
# ❌ DANGEROUS - stores password
class User(db.Model):
    password = db.Column(db.String(255))  # NO!

# ✅ SAFE - stores hash
class User(db.Model):
    password_hash = db.Column(db.String(255))  # YES!
```

## Secure Password Storage 💾

### Using Werkzeug (Built-in):

```python
from werkzeug.security import generate_password_hash, check_password_hash

# When creating user
password = "mypassword123"
password_hash = generate_password_hash(password)
# Stores: $2b$12$abc123...xyz789 (secret code!)

# When checking password
if check_password_hash(password_hash, "mypassword123"):
    # Password is correct!
    pass
```

### How Hashing Works:

```
User enters: "mypassword123"
    ↓
Website hashes: "$2b$12$abc123...xyz789"
    ↓
Website saves: Hash (NOT the password!)
    ↓
Even if hacker sees hash, they can't get password back!
```

**Hashing = One-way encryption (can't reverse it!)**

## Session Security 🎫

### What is Session Hijacking?

**Session Hijacking** = Stealing someone's session to pretend to be them

**The Attack**:
1. User logs in (gets session cookie)
2. Hacker steals cookie
3. Hacker uses cookie to access user's account
4. User's account is compromised!

### How to Prevent Session Hijacking:

```python
from flask import Flask, session
from datetime import timedelta
import secrets

app = Flask(__name__)

# Strong secret key
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Secure session settings
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Regenerate session ID on login (prevents fixation)
@app.route('/login', methods=['POST'])
def login():
    # Verify credentials...
    session.permanent = True
    session.regenerate()  # New session ID
    return redirect('/dashboard')
```

### Session Best Practices:

1. **Use HTTPS** - Encrypts session cookies
2. **HttpOnly Cookies** - JavaScript can't access
3. **Short Expiration** - Sessions expire quickly
4. **Regenerate on Login** - New session ID
5. **Strong Secret Key** - Hard to guess

## Rate Limiting (Prevent Brute Force) 🚦

### What is Brute Force?

**Brute Force** = Trying many passwords until one works

**The Attack**:
```
Hacker tries:
- password123
- password124
- password125
... (millions of tries!)
```

### How to Prevent:

```python
from flask import Flask, request
from datetime import datetime, timedelta
from functools import wraps

# Store failed attempts
failed_attempts = {}

def rate_limit(max_attempts=5, window=300):
    """Limit login attempts"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            now = datetime.utcnow()
            
            # Clean old attempts
            if ip in failed_attempts:
                failed_attempts[ip] = [
                    attempt for attempt in failed_attempts[ip]
                    if now - attempt < timedelta(seconds=window)
                ]
            
            # Check if too many attempts
            if ip in failed_attempts and len(failed_attempts[ip]) >= max_attempts:
                return "Too many login attempts. Please try again later.", 429
            
            # Try login
            result = f(*args, **kwargs)
            
            # If failed, record attempt
            if result and hasattr(result, 'status_code') and result.status_code == 401:
                if ip not in failed_attempts:
                    failed_attempts[ip] = []
                failed_attempts[ip].append(now)
            
            return result
        return decorated_function
    return decorator

@app.route('/login', methods=['POST'])
@rate_limit(max_attempts=5, window=300)  # 5 attempts per 5 minutes
def login():
    # Login logic...
    pass
```

## Account Lockout 🔒

### Locking Accounts After Failed Attempts:

```python
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)

    def is_locked(self):
        """Check if account is locked"""
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False
    
    def lock_account(self, minutes=15):
        """Lock account for specified minutes"""
        self.locked_until = datetime.utcnow() + timedelta(minutes=minutes)
        db.session.commit()
    
    def reset_failed_attempts(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return "Invalid credentials", 401
    
    # Check if account is locked
    if user.is_locked():
        return "Account is locked. Please try again later.", 403
    
    # Check password
    if check_password_hash(user.password_hash, password):
        # Success - reset attempts
        user.reset_failed_attempts()
        session['user_id'] = user.id
        return redirect('/dashboard')
    else:
        # Failed - increment attempts
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.lock_account(minutes=15)
            return "Too many failed attempts. Account locked for 15 minutes.", 403
        db.session.commit()
        return "Invalid credentials", 401
```

## Two-Factor Authentication (2FA) 🔐🔐

### What is 2FA?

**2FA** = Two-Factor Authentication

**Two factors**:
1. **Something you know** = Password
2. **Something you have** = Phone, authenticator app

**2FA = Extra layer of security!**

### Simple 2FA Example:

```python
import pyotp  # pip install pyotp
import qrcode  # pip install qrcode

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    two_factor_secret = db.Column(db.String(32))  # Secret for 2FA
    two_factor_enabled = db.Column(db.Boolean, default=False)

@app.route('/enable-2fa')
@login_required
def enable_2fa():
    user = User.query.get(current_user.id)
    
    # Generate secret
    secret = pyotp.random_base32()
    user.two_factor_secret = secret
    user.two_factor_enabled = True
    db.session.commit()
    
    # Generate QR code
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        user.username,
        issuer_name="MyApp"
    )
    
    return f'''
    <h2>Scan this QR code with your authenticator app:</h2>
    <img src="https://api.qrserver.com/v1/create-qr-code/?data={totp_uri}" />
    <p>Secret: {secret}</p>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    code = request.form.get('code')  # 2FA code
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        # Check 2FA if enabled
        if user.two_factor_enabled:
            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(code):
                return "Invalid 2FA code", 401
        
        session['user_id'] = user.id
        return redirect('/dashboard')
    
    return "Invalid credentials", 401
```

## Password Reset Security 🔄

### Secure Password Reset:

```python
import secrets
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(100))
    reset_token_expires = db.Column(db.DateTime)

    def generate_reset_token(self):
        """Generate secure reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify reset token"""
        if not self.reset_token or self.reset_token != token:
            return False
        if datetime.utcnow() > self.reset_token_expires:
            return False
        return True

@app.route('/reset-password', methods=['POST'])
def reset_password_request():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    
    if user:
        token = user.generate_reset_token()
        # Send email with reset link (we'll learn this later)
        reset_url = url_for('reset_password', token=token, _external=True)
        # send_email(user.email, reset_url)
    
    # Don't reveal if email exists (security!)
    return "If that email exists, a reset link has been sent.", 200

@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        return "Invalid or expired token", 400
    
    new_password = request.form.get('password')
    
    # Validate password strength
    is_strong, message = is_strong_password(new_password)
    if not is_strong:
        return message, 400
    
    # Update password
    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.session.commit()
    
    return "Password reset successful!", 200
```

## Security Best Practices Checklist ✅

### Password Security:
- [ ] Always hash passwords
- [ ] Require strong passwords
- [ ] Never store plain passwords
- [ ] Use Werkzeug's password hashing

### Session Security:
- [ ] Use HTTPS
- [ ] HttpOnly cookies
- [ ] Short expiration times
- [ ] Regenerate session on login
- [ ] Strong secret key

### Account Protection:
- [ ] Rate limit login attempts
- [ ] Lock accounts after failures
- [ ] Enable 2FA (optional but recommended)
- [ ] Secure password reset

## What You Learned! 📚

✅ Password security best practices  
✅ How to securely store passwords  
✅ How to secure sessions  
✅ How to prevent session hijacking  
✅ How to implement rate limiting  
✅ How to lock accounts  
✅ How to implement 2FA  
✅ Secure password reset  

## Key Concepts 💡

1. **Password Hashing** = One-way encryption
2. **Strong Passwords** = Mix of letters, numbers, symbols
3. **Session Security** = Protected session data
4. **Rate Limiting** = Prevent brute force
5. **Account Lockout** = Lock after failed attempts
6. **2FA** = Two-factor authentication

## What's Next? 🚀

You now know authentication security! Next, we'll learn about **HTTPS and Security Headers** - protecting data in transit!

---

**Great job! User accounts are now secure! 🎉**

