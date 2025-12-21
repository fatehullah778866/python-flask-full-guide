# Lesson 5.2: Building REST APIs - Creating Your First API! 🏗️

## What We're Building 🎯

We're going to create a **REST API** that:
- Returns data in JSON format
- Uses proper HTTP methods
- Returns proper status codes
- Handles errors gracefully

## Step 1: Returning JSON in Flask 📄

Flask makes it easy to return JSON:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users')
def get_users():
    users = [
        {"id": 1, "name": "John", "email": "john@email.com"},
        {"id": 2, "name": "Sarah", "email": "sarah@email.com"}
    ]
    return jsonify(users)
```

### Understanding `jsonify()`:

- **`jsonify()`** = Converts Python data to JSON
- **Automatically sets** Content-Type to application/json
- **Returns** proper JSON response

## Step 2: Creating API Endpoints 🛣️

Let's create a complete API for users:

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

# Create tables
with app.app_context():
    db.create_all()

# GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# GET one user
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404

# POST create user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate data
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and email are required"}), 400
    
    # Check if email exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    # Create user
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

# PUT update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update fields
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify(user.to_dict())

# DELETE user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding Request Data 📥

### Getting JSON Data:

```python
data = request.get_json()
```

**This gets JSON data from the request body.**

### Example Request:

```json
POST /api/users
Content-Type: application/json

{
  "name": "John",
  "email": "john@email.com"
}
```

### Accessing Data:

```python
name = data['name']
email = data['email']
```

## Understanding Response Status Codes 📊

### Success Responses:

```python
# 200 OK - Standard success
return jsonify(data), 200

# 201 Created - Resource created
return jsonify(data), 201

# 204 No Content - Success, no content
return '', 204
```

### Error Responses:

```python
# 400 Bad Request - Invalid request
return jsonify({"error": "Invalid data"}), 400

# 404 Not Found - Resource doesn't exist
return jsonify({"error": "Not found"}), 404

# 500 Internal Server Error - Server error
return jsonify({"error": "Server error"}), 500
```

## Request Validation ✅

Always validate incoming data:

```python
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Check if data exists
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Check required fields
    if 'name' not in data or not data['name']:
        return jsonify({"error": "Name is required"}), 400
    
    if 'email' not in data or not data['email']:
        return jsonify({"error": "Email is required"}), 400
    
    # Validate email format (simple check)
    if '@' not in data['email']:
        return jsonify({"error": "Invalid email format"}), 400
    
    # Continue with creation...
```

## Error Handling 🛡️

### Method 1: Try-Except Blocks

```python
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        # Update user...
        db.session.commit()
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Method 2: Error Handlers

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

## Converting Models to JSON 📄

### Method 1: to_dict() Method

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

# Usage
user = User.query.get(1)
return jsonify(user.to_dict())
```

### Method 2: List Comprehension

```python
users = User.query.all()
return jsonify([user.to_dict() for user in users])
```

## Complete API Example 🎯

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "api.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

# GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        "success": True,
        "count": len(users),
        "users": [user.to_dict() for user in users]
    })

# GET one user
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "success": True,
            "user": user.to_dict()
        })
    return jsonify({
        "success": False,
        "error": "User not found"
    }), 404

# POST create user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validation
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    if 'name' not in data or not data['name']:
        return jsonify({"success": False, "error": "Name is required"}), 400
    
    if 'email' not in data or not data['email']:
        return jsonify({"success": False, "error": "Email is required"}), 400
    
    # Check duplicate
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"success": False, "error": "Email already exists"}), 400
    
    # Create user
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 201

# PUT update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    # Update fields
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            return jsonify({"success": False, "error": "Email already exists"}), 400
        user.email = data['email']
    
    db.session.commit()
    return jsonify({
        "success": True,
        "user": user.to_dict()
    })

# DELETE user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## Testing Your API 🧪

### Using curl (Command Line):

```bash
# GET all users
curl http://localhost:5000/api/users

# GET one user
curl http://localhost:5000/api/users/1

# POST create user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@email.com"}'

# PUT update user
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated"}'

# DELETE user
curl -X DELETE http://localhost:5000/api/users/1
```

### Using Python requests:

```python
import requests

# GET all users
response = requests.get('http://localhost:5000/api/users')
print(response.json())

# POST create user
data = {"name": "John", "email": "john@email.com"}
response = requests.post('http://localhost:5000/api/users', json=data)
print(response.json())
```

## Best Practices ✨

### 1. Consistent Response Format

```python
# Success
{
  "success": True,
  "data": {...}
}

# Error
{
  "success": False,
  "error": "Error message"
}
```

### 2. Use Proper Status Codes

```python
200 OK
201 Created
400 Bad Request
404 Not Found
500 Server Error
```

### 3. Validate All Input

```python
# Always validate!
if not data or 'name' not in data:
    return jsonify({"error": "Invalid data"}), 400
```

### 4. Handle Errors Gracefully

```python
try:
    # API logic
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

## Common Mistakes 🔧

### Mistake 1: Not Using jsonify()

```python
# ❌ Returns string, not JSON
return {"name": "John"}

# ✅ Returns proper JSON
return jsonify({"name": "John"})
```

### Mistake 2: Wrong Status Codes

```python
# ❌ Wrong status code
return jsonify({"error": "Not found"}), 200

# ✅ Correct status code
return jsonify({"error": "Not found"}), 404
```

### Mistake 3: No Validation

```python
# ❌ No validation
user = User(name=data['name'])

# ✅ Validate first
if 'name' not in data:
    return jsonify({"error": "Name required"}), 400
```

## What You Learned! 📚

✅ How to return JSON in Flask  
✅ How to create API endpoints  
✅ How to handle GET, POST, PUT, DELETE  
✅ How to validate requests  
✅ How to handle errors  
✅ How to use status codes  
✅ How to test APIs  

## Key Concepts 💡

1. **`jsonify()`** = Converts Python to JSON
2. **`request.get_json()`** = Gets JSON from request
3. **Status Codes** = Tell client what happened
4. **Validation** = Check data before using
5. **Error Handling** = Handle errors gracefully

## What's Next? 🚀

You now know how to build basic APIs! Next, we'll learn about **Flask-RESTful** - a tool that makes building APIs even easier!

---

**Excellent! You can now build REST APIs! 🎉**

