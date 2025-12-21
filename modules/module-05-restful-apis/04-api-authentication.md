# Lesson 5.4: API Authentication - Securing Your APIs! 🔒

## Why Do We Need API Authentication? 🎯

**API Authentication** = Proving who you are when using an API

### The Problem Without Authentication:

- ❌ Anyone can access your API
- ❌ Anyone can delete data
- ❌ Anyone can modify data
- ❌ No way to track who did what

### The Solution: API Authentication

- ✅ Only authorized users can access
- ✅ Track who is using the API
- ✅ Control what users can do
- ✅ Secure your data

## Types of API Authentication 🔐

### 1. API Keys (Simple)

**API Key** = A secret code that identifies you

```
Request:
GET /api/users
Headers:
  X-API-Key: your-secret-key-123
```

### 2. Token-Based (Better)

**Token** = Temporary code that proves you're logged in

```
Request:
GET /api/users
Headers:
  Authorization: Bearer your-token-here
```

### 3. JWT (JSON Web Tokens) (Best)

**JWT** = Secure token with user information inside

```
Request:
GET /api/users
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Simple API Key Authentication 🔑

### Step 1: Store API Keys

```python
# In database or config
API_KEYS = {
    "user123": "secret-key-abc",
    "user456": "secret-key-xyz"
}
```

### Step 2: Check API Key

```python
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key not in API_KEYS.values():
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Use decorator
@app.route('/api/users')
@require_api_key
def get_users():
    return jsonify({"users": [...]})
```

## Token-Based Authentication 🎫

### Step 1: Generate Token on Login

```python
import secrets

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verify credentials
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        # Generate token
        token = secrets.token_urlsafe(32)
        user.api_token = token
        db.session.commit()
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401
```

### Step 2: Verify Token

```python
def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token required"}), 401
        
        user = User.query.filter_by(api_token=token).first()
        if not user:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function
```

## JWT (JSON Web Tokens) 🎟️

### What is JWT?

**JWT** = A secure token that contains user information

**Structure:**
```
header.payload.signature
```

### Installing PyJWT

```bash
pip install PyJWT
```

### Creating JWT Tokens

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your-secret-key'

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Expires in 24 hours
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
```

### Verifying JWT Tokens

```python
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

## Complete JWT Example 🎯

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "api.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}

with app.app_context():
    db.create_all()

# JWT Helper Functions
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

# Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        return f(*args, **kwargs)
    return decorated

# Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    user = User(
        username=data['username'],
        email=data.get('email', ''),
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User created"}), 201

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        token = generate_token(user.id)
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401

# Protected Route
@app.route('/api/users', methods=['GET'])
@token_required
def get_users():
    users = User.query.all()
    return jsonify({"users": [user.to_dict() for user in users]})

# Protected Route - Get Current User
@app.route('/api/me', methods=['GET'])
@token_required
def get_current_user():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = verify_token(token)
    user = User.query.get(user_id)
    return jsonify({"user": user.to_dict()})

if __name__ == '__main__':
    app.run(debug=True)
```

## Using the API 🔧

### Register:

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123","email":"john@email.com"}'
```

### Login:

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Use Token:

```bash
curl http://localhost:5000/api/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Security Best Practices 🔒

### 1. Use HTTPS in Production

```python
# Always use HTTPS for APIs in production!
# Never send tokens over HTTP!
```

### 2. Set Token Expiration

```python
# Tokens should expire
'exp': datetime.utcnow() + timedelta(hours=24)
```

### 3. Store Secret Keys Securely

```python
# ❌ Don't hardcode
SECRET_KEY = 'my-secret-key'

# ✅ Use environment variables
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### 4. Validate All Input

```python
# Always validate!
if not data or 'username' not in data:
    return jsonify({"error": "Invalid data"}), 400
```

## Common Mistakes 🔧

### Mistake 1: No Token Expiration

```python
# ❌ Token never expires
payload = {'user_id': user_id}

# ✅ Token expires
payload = {
    'user_id': user_id,
    'exp': datetime.utcnow() + timedelta(hours=24)
}
```

### Mistake 2: Weak Secret Key

```python
# ❌ Weak key
SECRET_KEY = 'secret'

# ✅ Strong key
SECRET_KEY = os.environ.get('SECRET_KEY')  # Long, random string
```

### Mistake 3: Not Checking Token

```python
# ❌ No verification
token = request.headers.get('Authorization')

# ✅ Verify token
user_id = verify_token(token)
if not user_id:
    return jsonify({"error": "Invalid token"}), 401
```

## What You Learned! 📚

✅ Why API authentication is needed  
✅ Types of API authentication  
✅ How to use API keys  
✅ How to use tokens  
✅ How to use JWT  
✅ How to protect API routes  
✅ Security best practices  

## Key Concepts 💡

1. **API Key** = Simple secret code
2. **Token** = Temporary authentication code
3. **JWT** = Secure token with user info
4. **Bearer Token** = Token in Authorization header
5. **Token Expiration** = Tokens should expire
6. **HTTPS** = Always use in production

## What's Next? 🚀

You now know how to secure APIs! Next, we'll learn about **API documentation** - how to document your APIs so others can use them!

---

**Excellent! Your APIs are now secure! 🎉**

