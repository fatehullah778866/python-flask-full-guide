# Lesson 6.5: Context and Request Lifecycle - How Flask Works! ⚙️

## What is a Context? 🤔

**Context** = Information Flask needs to handle a request

Think of it like:
- **Context** = A workspace with all the tools you need
- **Request** = A job you need to do
- **Context** = Gives you everything you need for the job

**Context = Flask's workspace for each request!**

## Types of Contexts 📦

### 1. Application Context

**Application Context** = Information about your Flask app

- Database connections
- Configuration
- Extensions

### 2. Request Context

**Request Context** = Information about the current request

- Request data
- Session
- Current user

## Understanding the Request Lifecycle 🔄

### Step-by-Step:

```
1. User makes request
   ↓
2. Flask creates request context
   ↓
3. Flask creates application context
   ↓
4. Your route function runs
   ↓
5. Flask sends response
   ↓
6. Contexts are destroyed
```

## Application Context 🏠

### What is Application Context?

**Application Context** = Flask's way of keeping track of your app

### When Do You Need It?

You need application context when:
- Working outside a request (like in a script)
- Working in background tasks
- Working in shell

### Creating Application Context:

```python
from flask import Flask, current_app

app = Flask(__name__)

# Outside a request, you need context
with app.app_context():
    # Now you can use current_app
    print(current_app.config['SECRET_KEY'])
```

## Request Context 📨

### What is Request Context?

**Request Context** = Flask's way of keeping track of the current request

### Automatically Created:

```python
@app.route('/')
def home():
    # Request context is automatically created!
    # You can use request, session, etc.
    return request.method  # Works!
```

### Accessing Request Context:

```python
from flask import request, session, g

@app.route('/')
def home():
    # All of these work because request context exists
    method = request.method
    data = request.get_json()
    user_id = session.get('user_id')
    return "Home"
```

## The `g` Object 🎁

### What is `g`?

**`g`** = A special object that stores data for one request

Think of it like:
- **`g`** = A temporary storage box
- **One request** = One box
- **Next request** = New box (old one is gone)

### Using `g`:

```python
from flask import g

@app.before_request
def before_request():
    # Store data in g
    g.user = get_current_user()
    g.start_time = time.time()

@app.route('/')
def home():
    # Use data from g
    user = g.user
    return f"Hello, {user.name}!"
```

## Understanding Context Stack 📚

### How Contexts Work:

Flask uses a **stack** (like a stack of plates):

```
Request Context (top)
Application Context (bottom)
```

### Why a Stack?

- Multiple contexts can exist
- Each request gets its own context
- Contexts are pushed and popped

## Working Outside Request Context 🔧

### Problem:

```python
# This won't work outside a request!
user = User.query.all()  # Error! No application context
```

### Solution:

```python
from flask import Flask

app = Flask(__name__)

# Create application context
with app.app_context():
    users = User.query.all()  # Works!
```

## Background Tasks 🎯

### Problem:

```python
def send_email_async(user_id):
    # This runs outside request context!
    user = User.query.get(user_id)  # Error!
    send_email(user.email)
```

### Solution:

```python
from flask import Flask, copy_current_request_context

@app.route('/send-email/<int:user_id>')
def send_email_route(user_id):
    @copy_current_request_context
    def send_email_async():
        # Now has request context!
        user = User.query.get(user_id)
        send_email(user.email)
    
    # Run in background
    thread = threading.Thread(target=send_email_async)
    thread.start()
    return "Email sending..."
```

## Complete Context Example 🎯

```python
from flask import Flask, g, request, current_app
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

# Before each request
@app.before_request
def before_request():
    g.start_time = time.time()
    g.user = None  # Will be set if user is logged in

# After each request
@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    print(f"Request took {duration:.2f} seconds")
    return response

@app.route('/')
def home():
    # All contexts available here
    app_name = current_app.name
    method = request.method
    user = g.user
    
    return f"App: {app_name}, Method: {method}"

# Working outside request
def create_user_outside_request():
    with app.app_context():
        # Now we have application context
        user = User(name="John", email="john@email.com")
        db.session.add(user)
        db.session.commit()
```

## Context Best Practices ✨

### 1. Use `g` for Request-Specific Data

```python
# ✅ Good - use g
@app.before_request
def load_user():
    g.user = get_current_user()

@app.route('/profile')
def profile():
    return f"Hello, {g.user.name}"
```

### 2. Create Context When Needed

```python
# ✅ Good - create context
with app.app_context():
    users = User.query.all()
```

### 3. Don't Store in `g` Between Requests

```python
# ❌ Bad - g is cleared after each request
g.data = expensive_operation()  # Will be lost!

# ✅ Good - use cache or database
cache.set('data', expensive_operation())
```

## Common Mistakes 🔧

### Mistake 1: Using Outside Context

```python
# ❌ No context
users = User.query.all()

# ✅ Create context
with app.app_context():
    users = User.query.all()
```

### Mistake 2: Storing in `g` for Later

```python
# ❌ g is cleared after request
g.important_data = data
# Next request: g.important_data is gone!

# ✅ Use database or cache
db.session.add(data)
```

## What You Learned! 📚

✅ What contexts are  
✅ Application context vs request context  
✅ How request lifecycle works  
✅ How to use `g` object  
✅ How to work outside request context  
✅ How to handle background tasks  
✅ Context best practices  

## Key Concepts 💡

1. **Context** = Flask's workspace for handling requests
2. **Application Context** = App-level information
3. **Request Context** = Request-level information
4. **`g` object** = Temporary storage for one request
5. **Context Stack** = How Flask manages contexts
6. **`app.app_context()`** = Create application context

## What's Next? 🚀

Congratulations! You've completed Module 6! You now know:
- ✅ Application Factory Pattern
- ✅ Blueprints
- ✅ Error Handling
- ✅ Flask Extensions
- ✅ Context and Lifecycle

**Next Module**: Testing - Learn how to test your Flask applications!

---

**Amazing! You're mastering advanced Flask concepts! 🎉**

