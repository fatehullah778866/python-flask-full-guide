# Lesson 5.3: Flask-RESTful - Making APIs Easier! 🛠️

## What is Flask-RESTful? 🤔

**Flask-RESTful** is like a **helper** that makes building APIs easier!

### The Problem with Basic Flask APIs:

- ❌ More code to write
- ❌ Manual method handling
- ❌ More repetitive code
- ❌ Harder to organize

### The Solution: Flask-RESTful

- ✅ Less code
- ✅ Automatic method handling
- ✅ Better organization
- ✅ Built-in features

**Flask-RESTful makes APIs cleaner and easier!**

## Installing Flask-RESTful 📦

```bash
pip install flask-restful
```

That's it! Flask-RESTful is now installed.

## Setting Up Flask-RESTful ⚙️

```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
```

**That's it!** Now you can use Flask-RESTful.

## Creating Your First Resource 🎯

A **Resource** is like a **class** that handles one endpoint:

```python
from flask_restful import Resource

class UserResource(Resource):
    def get(self, user_id):
        # Handle GET request
        return {"id": user_id, "name": "John"}
    
    def put(self, user_id):
        # Handle PUT request
        return {"message": "User updated"}
    
    def delete(self, user_id):
        # Handle DELETE request
        return {"message": "User deleted"}
```

### Understanding Resources:

- **`Resource`** = Base class for API endpoints
- **`get()`** = Handles GET requests
- **`post()`** = Handles POST requests
- **`put()`** = Handles PUT requests
- **`delete()`** = Handles DELETE requests

## Registering Resources 🛣️

After creating a resource, register it:

```python
api.add_resource(UserResource, '/api/users/<int:user_id>')
```

**This connects the resource to a URL!**

## Complete Example 🎯

```python
from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
api = Api(app)

# Database setup
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

# User List Resource (GET all, POST create)
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return {
            "success": True,
            "count": len(users),
            "users": [user.to_dict() for user in users]
        }
    
    def post(self):
        data = request.get_json()
        
        # Validation
        if not data or 'name' not in data or 'email' not in data:
            abort(400, message="Name and email are required")
        
        # Check duplicate
        if User.query.filter_by(email=data['email']).first():
            abort(400, message="Email already exists")
        
        # Create user
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict(), 201

# User Resource (GET one, PUT update, DELETE)
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return {"success": True, "user": user.to_dict()}
    
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        data = request.get_json()
        if not data:
            abort(400, message="No data provided")
        
        # Update fields
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
                abort(400, message="Email already exists")
            user.email = data['email']
        
        db.session.commit()
        return {"success": True, "user": user.to_dict()}
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        db.session.delete(user)
        db.session.commit()
        return {"success": True, "message": "User deleted"}

# Register resources
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding `abort()` 🛑

`abort()` is like raising an error with a status code:

```python
from flask_restful import abort

# Abort with 404
abort(404, message="User not found")

# Abort with 400
abort(400, message="Invalid data")
```

**Much easier than manual error handling!**

## Request Parsing 📥

Flask-RESTful has built-in request parsing:

```python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('email', type=str, required=True, help='Email is required')
parser.add_argument('age', type=int, required=False)

class UserListResource(Resource):
    def post(self):
        args = parser.parse_args()
        # args['name'], args['email'], args['age']
        user = User(name=args['name'], email=args['email'])
        # ...
```

### Understanding Request Parsing:

- **`reqparse.RequestParser()`** = Creates parser
- **`add_argument()`** = Defines expected fields
- **`type`** = Expected data type
- **`required`** = Is field required?
- **`help`** = Error message if missing

## Field Types 📊

```python
parser.add_argument('name', type=str)      # String
parser.add_argument('age', type=int)       # Integer
parser.add_argument('price', type=float)   # Float
parser.add_argument('is_active', type=bool) # Boolean
```

## Complete Example with Parsing 🎯

```python
from flask_restful import Api, Resource, reqparse, abort
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "api.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

with app.app_context():
    db.create_all()

# Request parser
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('email', type=str, required=True, help='Email is required')

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return {"users": [user.to_dict() for user in users]}
    
    def post(self):
        args = parser.parse_args()
        
        # Check duplicate
        if User.query.filter_by(email=args['email']).first():
            abort(400, message="Email already exists")
        
        user = User(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict(), 201

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return {"user": user.to_dict()}
    
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        args = parser.parse_args()
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        
        return {"user": user.to_dict()}
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}

api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

## Benefits of Flask-RESTful ✨

### 1. Less Code

**Without Flask-RESTful:**
```python
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # GET logic
    elif request.method == 'POST':
        # POST logic
```

**With Flask-RESTful:**
```python
class UserListResource(Resource):
    def get(self):
        # GET logic
    
    def post(self):
        # POST logic
```

### 2. Better Organization

- Each resource is a class
- Easy to find and modify
- Clean separation

### 3. Built-in Features

- Request parsing
- Error handling
- Automatic method routing

## Common Mistakes 🔧

### Mistake 1: Forgetting to Register Resource

```python
# ❌ Resource created but not registered
class UserResource(Resource):
    def get(self):
        return {"message": "Hello"}

# ✅ Register the resource
api.add_resource(UserResource, '/api/users')
```

### Mistake 2: Wrong Method Names

```python
# ❌ Wrong method name
def GET(self):  # Should be lowercase!

# ✅ Correct
def get(self):
```

### Mistake 3: Not Using abort()

```python
# ❌ Manual error handling
if not user:
    return {"error": "Not found"}, 404

# ✅ Use abort
if not user:
    abort(404, message="Not found")
```

## What You Learned! 📚

✅ What Flask-RESTful is and why it's useful  
✅ How to set up Flask-RESTful  
✅ How to create resources  
✅ How to register resources  
✅ How to use request parsing  
✅ How to use abort() for errors  
✅ Benefits of Flask-RESTful  

## Key Concepts 💡

1. **Resource** = Class that handles API endpoint
2. **`get()`, `post()`, `put()`, `delete()`** = HTTP methods
3. **`api.add_resource()`** = Register resource to URL
4. **`reqparse`** = Parse and validate requests
5. **`abort()`** = Raise error with status code

## What's Next? 🚀

You now know Flask-RESTful! Next, we'll learn about **API authentication** - how to secure your APIs!

---

**Great job! You're building professional APIs! 🎉**

