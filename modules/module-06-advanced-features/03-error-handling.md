# Lesson 6.3: Error Handling - Making Errors Friendly! 🛡️

## What is Error Handling? 🤔

**Error Handling** = What happens when something goes wrong

Think of it like:
- **Without Error Handling**: App crashes, user sees scary error
- **With Error Handling**: App shows friendly message, keeps working

**Error Handling = Making errors user-friendly!**

## Why Do We Need Error Handling? 🎯

### The Problem Without Error Handling:

```
User visits: /users/999
User sees: "Internal Server Error 500"
User thinks: "This website is broken!"
```

### The Solution: Error Handling

```
User visits: /users/999
User sees: "User not found. Please try again."
User thinks: "Okay, I'll try a different ID."
```

**Error handling = Better user experience!**

## Common HTTP Error Codes 📊

### 404 - Not Found

**When**: User tries to access something that doesn't exist

```python
@app.errorhandler(404)
def not_found(error):
    return "Page not found!", 404
```

### 500 - Internal Server Error

**When**: Something goes wrong on the server

```python
@app.errorhandler(500)
def internal_error(error):
    return "Something went wrong!", 500
```

### 403 - Forbidden

**When**: User doesn't have permission

```python
@app.errorhandler(403)
def forbidden(error):
    return "You don't have permission!", 403
```

## Creating Custom Error Pages 🎨

### Method 1: Simple Error Handlers

```python
from flask import Flask, render_template_string

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template_string('''
    <h1>404 - Page Not Found</h1>
    <p>Sorry, the page you're looking for doesn't exist.</p>
    <a href="/">Go Home</a>
    '''), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template_string('''
    <h1>500 - Server Error</h1>
    <p>Something went wrong on our end. Please try again later.</p>
    <a href="/">Go Home</a>
    '''), 500
```

### Method 2: Using Templates

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
```

## Handling Specific Errors 🔧

### Handling Database Errors

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

@app.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    return "Database error occurred!", 500
```

### Handling Validation Errors

```python
from wtforms import ValidationError

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return f"Validation error: {error}", 400
```

## Try-Except Blocks 🛡️

### Basic Try-Except

```python
@app.route('/users/<int:user_id>')
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return "User not found", 404
        return f"User: {user.name}"
    except Exception as e:
        return f"Error: {str(e)}", 500
```

### Specific Exception Handling

```python
@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    try:
        result = a / b
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Cannot divide by zero!", 400
    except Exception as e:
        return f"Error: {str(e)}", 500
```

## Logging Errors 📝

### Setting Up Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Logging Errors

```python
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return "Something went wrong!", 500
```

## Complete Error Handling Example 🎯

```python
from flask import Flask, render_template_string, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Database setup
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    logger.warning(f'404 Error: {request.url}')
    return render_template_string('''
    <html>
    <head><title>404 - Not Found</title></head>
    <body>
        <h1>404 - Page Not Found</h1>
        <p>Sorry, the page you're looking for doesn't exist.</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    '''), 404

# 500 Error Handler
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 Error: {error}', exc_info=True)
    return render_template_string('''
    <html>
    <head><title>500 - Server Error</title></head>
    <body>
        <h1>500 - Server Error</h1>
        <p>Something went wrong on our end. We're working on it!</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    '''), 500

# 403 Error Handler
@app.errorhandler(403)
def forbidden(error):
    return render_template_string('''
    <html>
    <head><title>403 - Forbidden</title></head>
    <body>
        <h1>403 - Forbidden</h1>
        <p>You don't have permission to access this page.</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    '''), 403

# Route with error handling
@app.route('/users/<int:user_id>')
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return "User not found", 404
        return f"User: {user.name}"
    except Exception as e:
        logger.error(f'Error getting user {user_id}: {e}')
        return "An error occurred", 500

# API Error Handler (for JSON APIs)
@app.errorhandler(404)
def api_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource not found"}), 404
    return not_found(error)

if __name__ == '__main__':
    app.run(debug=True)
```

## User-Friendly Error Messages 💬

### Bad Error Message:

```
Error: <class 'sqlalchemy.exc.IntegrityError'>
```

**User thinks**: "What does this mean?!"

### Good Error Message:

```
Sorry, that email is already registered. Please use a different email.
```

**User thinks**: "Oh, I need to use a different email!"

### Example:

```python
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return "Registration successful!"
    except IntegrityError:
        return "Email already exists. Please use a different email.", 400
    except KeyError:
        return "Missing required fields. Please provide name and email.", 400
    except Exception as e:
        logger.error(f'Registration error: {e}')
        return "An error occurred. Please try again later.", 500
```

## Error Handling Best Practices ✨

### 1. Always Handle Errors

```python
# ❌ No error handling
user = User.query.get(user_id)
return user.name

# ✅ With error handling
try:
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    return user.name
except Exception as e:
    return "Error occurred", 500
```

### 2. Log Errors

```python
# Always log errors for debugging
logger.error(f'Error: {error}', exc_info=True)
```

### 3. User-Friendly Messages

```python
# ❌ Technical error
return f"Error: {str(e)}", 500

# ✅ User-friendly
return "Something went wrong. Please try again later.", 500
```

### 4. Different Errors for Web vs API

```python
@app.errorhandler(404)
def handle_404(error):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not found"}), 404
    return render_template('404.html'), 404
```

## Common Mistakes 🔧

### Mistake 1: Not Returning Status Code

```python
# ❌ Missing status code
@app.errorhandler(404)
def not_found(error):
    return "Not found"

# ✅ Include status code
@app.errorhandler(404)
def not_found(error):
    return "Not found", 404
```

### Mistake 2: Exposing Technical Errors

```python
# ❌ Shows technical details
return f"Error: {str(e)}", 500

# ✅ User-friendly message
return "An error occurred. Please try again.", 500
```

### Mistake 3: Not Logging Errors

```python
# ❌ No logging
@app.errorhandler(500)
def error(error):
    return "Error", 500

# ✅ Log the error
@app.errorhandler(500)
def error(error):
    logger.error(f'Error: {error}')
    return "Error", 500
```

## What You Learned! 📚

✅ Why error handling is important  
✅ How to create custom error pages  
✅ How to handle different error types  
✅ How to use try-except blocks  
✅ How to log errors  
✅ How to create user-friendly messages  
✅ Best practices for error handling  

## Key Concepts 💡

1. **Error Handler** = Function that handles errors
2. **`@app.errorhandler()`** = Decorator for error handlers
3. **Status Codes** = 404, 500, 403, etc.
4. **Try-Except** = Catch and handle errors
5. **Logging** = Record errors for debugging
6. **User-Friendly** = Messages users can understand

## What's Next? 🚀

You now know how to handle errors! Next, we'll learn about **Flask Extensions** - powerful tools that extend Flask's functionality!

---

**Great job! Your apps are now more robust! 🎉**

