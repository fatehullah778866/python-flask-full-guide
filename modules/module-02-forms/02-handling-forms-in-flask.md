# Lesson 2.2: Handling Forms in Flask - Receiving User Information 📥

## What We're Learning 🎯

Now that you know how to create HTML forms, let's learn how Flask receives and uses that information!

Think of it like this:
- **HTML Form** = The mailbox (where users put information)
- **Flask** = The mail carrier (who receives and processes it)

## How Flask Receives Form Data 📬

When a user submits a form, Flask receives the data in a special object called `request`.

### The `request` Object

The `request` object is like a box that contains everything the user sent:
- Form data
- URL parameters
- Files
- Headers
- And more!

## Importing Request 🔌

First, we need to import `request` from Flask:

```python
from flask import Flask, request
```

- **`Flask`** = The Flask framework
- **`request`** = The object that holds user's data

## Creating a Form Route 🛣️

Let's create a route that shows a form:

```python
from flask import Flask, request

app = Flask(__name__)

# Route to show the form
@app.route('/contact', methods=['GET'])
def contact_form():
    return '''
    <form method="POST" action="/contact">
        <label>Name:</label>
        <input type="text" name="name" required><br>
        
        <label>Email:</label>
        <input type="email" name="email" required><br>
        
        <label>Message:</label>
        <textarea name="message" required></textarea><br>
        
        <button type="submit">Send</button>
    </form>
    '''
```

### Breaking It Down:

- **`methods=['GET']`** = This route only accepts GET requests (viewing the form)
- **`action="/contact"`** = When submitted, send to `/contact` route
- **`method="POST"`** = Form will use POST method

## Handling Form Submission 📤

Now let's create a route that receives the form data:

```python
# Route to handle form submission
@app.route('/contact', methods=['POST'])
def contact_submit():
    # Get data from the form
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Do something with the data (for now, just show it)
    return f'''
    <h1>Thank you, {name}!</h1>
    <p>We received your message:</p>
    <p>{message}</p>
    <p>We'll reply to: {email}</p>
    '''
```

### Understanding `request.form`:

- **`request.form`** = Dictionary containing all form data
- **`request.form['name']`** = Gets the value from the field named "name"
- **`request.form['email']`** = Gets the value from the field named "email"

## Complete Example 🎯

Let's put it all together:

```python
from flask import Flask, request

app = Flask(__name__)

# Show the form (GET request)
@app.route('/contact', methods=['GET'])
def contact_form():
    return '''
    <html>
    <head><title>Contact Us</title></head>
    <body>
        <h1>Contact Us</h1>
        <form method="POST" action="/contact">
            <label>Your Name:</label><br>
            <input type="text" name="name" required><br><br>
            
            <label>Your Email:</label><br>
            <input type="email" name="email" required><br><br>
            
            <label>Your Message:</label><br>
            <textarea name="message" rows="5" required></textarea><br><br>
            
            <button type="submit">Send Message</button>
        </form>
    </body>
    </html>
    '''

# Handle form submission (POST request)
@app.route('/contact', methods=['POST'])
def contact_submit():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Process the data (you could save to database, send email, etc.)
    
    # Show a thank you message
    return f'''
    <html>
    <head><title>Thank You!</title></head>
    <body>
        <h1>Thank you, {name}!</h1>
        <p>We received your message and will reply to <strong>{email}</strong></p>
        <p>Your message: <em>{message}</em></p>
        <a href="/contact">Send another message</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

## Two Ways to Get Form Data 🔍

### Method 1: Direct Access (Can Cause Errors)
```python
name = request.form['name']  # ❌ Error if 'name' doesn't exist
```

### Method 2: Using `.get()` (Safer)
```python
name = request.form.get('name')  # ✅ Returns None if doesn't exist
```

**Always use `.get()` - it's safer!**

## Handling Both GET and POST in One Route 🎯

You can handle both in the same function:

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        return f'Thank you, {name}! We received your message.'
    else:
        # Show the form
        return '''
        <form method="POST">
            <input type="text" name="name" placeholder="Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <textarea name="message" placeholder="Message" required></textarea>
            <button type="submit">Send</button>
        </form>
        '''
```

### How It Works:

- **`if request.method == 'POST'`** = If form was submitted
- **`else`** = If just viewing the page (GET request)

## Getting Query Parameters (GET Method) 🔗

When using GET method, data comes in the URL:

```
http://example.com/search?q=flask&page=1
```

To get this data:

```python
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')  # Gets 'q' from URL
    page = request.args.get('page', 1)  # Gets 'page', default is 1
    
    return f'Searching for: {query}, Page: {page}'
```

### Key Difference:

- **`request.form`** = Data from POST forms
- **`request.args`** = Data from URL (GET method)

## Form Validation Basics ✅

Validation means checking if the data is correct before using it:

```python
@app.route('/contact', methods=['POST'])
def contact_submit():
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    
    # Validate (check if data is good)
    errors = []
    
    if not name:
        errors.append('Name is required')
    
    if not email or '@' not in email:
        errors.append('Valid email is required')
    
    if not message or len(message) < 10:
        errors.append('Message must be at least 10 characters')
    
    # If there are errors, show them
    if errors:
        return f'Errors: {", ".join(errors)}'
    
    # If no errors, process the data
    return f'Thank you, {name}! Message received.'
```

### What We're Doing:

1. **Get data** from form
2. **`.strip()`** = Remove extra spaces
3. **Check** if data is valid
4. **Collect errors** if any
5. **Show errors** or process data

## Real-World Example: Login Form 🔐

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple validation
        if not username or not password:
            return 'Username and password required!'
        
        # Check credentials (simplified - we'll learn proper auth later)
        if username == 'admin' and password == 'secret':
            return f'Welcome, {username}!'
        else:
            return 'Invalid username or password!'
    else:
        # Show login form
        return '''
        <form method="POST">
            <h2>Login</h2>
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        '''
```

## Practice Exercise 🏋️

Create a registration form that:
1. Shows a form with name, email, password, and confirm password
2. Validates that passwords match
3. Shows success message if valid
4. Shows error if passwords don't match

**Try it yourself!**

## Solution 💡

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        
        # Validation
        if not name:
            return 'Name is required!'
        
        if not email or '@' not in email:
            return 'Valid email is required!'
        
        if not password:
            return 'Password is required!'
        
        if password != confirm:
            return 'Passwords do not match!'
        
        return f'Registration successful! Welcome, {name}!'
    
    else:
        return '''
        <form method="POST">
            <h2>Register</h2>
            <input type="text" name="name" placeholder="Full Name" required><br><br>
            <input type="email" name="email" placeholder="Email" required><br><br>
            <input type="password" name="password" placeholder="Password" required><br><br>
            <input type="password" name="confirm" placeholder="Confirm Password" required><br><br>
            <button type="submit">Register</button>
        </form>
        '''

if __name__ == '__main__':
    app.run(debug=True)
```

## Common Mistakes 🔧

### Mistake 1: Forgetting to Import `request`
```python
from flask import Flask  # ❌ Missing request!
from flask import Flask, request  # ✅ Correct
```

### Mistake 2: Wrong Method
```python
@app.route('/contact')  # ❌ Only GET by default
@app.route('/contact', methods=['POST'])  # ✅ Correct
```

### Mistake 3: Using Wrong Dictionary
```python
name = request.args['name']  # ❌ Wrong for POST forms
name = request.form['name']  # ✅ Correct for POST forms
```

### Mistake 4: Not Handling Missing Data
```python
name = request.form['name']  # ❌ Error if missing
name = request.form.get('name')  # ✅ Safe
```

## Security Note 🔒

**Important**: The forms we're creating now are basic. In real applications, you need:
- CSRF protection (we'll learn this with Flask-WTF)
- Input sanitization (cleaning user input)
- Password hashing (for passwords)
- SQL injection prevention (when using databases)

We'll learn these in later lessons!

## What You Learned! 📚

✅ How Flask receives form data  
✅ Using `request.form` to get form values  
✅ Handling both GET and POST in one route  
✅ Basic form validation  
✅ Difference between `request.form` and `request.args`  
✅ Creating complete form handling systems  

## Key Concepts 💡

1. **`request.form`** = Dictionary of POST form data
2. **`request.args`** = Dictionary of URL parameters (GET)
3. **`.get()`** = Safe way to get values (returns None if missing)
4. **`methods=['GET', 'POST']`** = Route accepts both methods
5. **Validation** = Checking if data is correct before using

## What's Next? 🚀

You can now handle forms, but we're putting HTML directly in Python (not ideal). Next, we'll learn about **Flask-WTF** - a better way to handle forms with validation, security, and templates!

---

**Excellent work! You can now receive and process form data in Flask! 🎉**

