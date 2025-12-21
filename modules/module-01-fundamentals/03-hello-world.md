# Lesson 1.3: Your First Flask App - "Hello World" 👋

## What We're Building 🎯

We're going to create the simplest website possible - one that just says "Hello World!" when you visit it.

Think of it like learning to write your first word before writing a whole story!

## Understanding How Websites Work 🌐

### The Simple Version:

1. **You (the user)** open a web browser (Chrome, Firefox, etc.)
2. **You type** a website address (like `http://localhost:5000`)
3. **Your browser asks** Flask: "Can I see a webpage?"
4. **Flask responds** with a webpage
5. **Your browser shows** you the webpage

It's like ordering food:
- You = Customer
- Browser = Waiter
- Flask = Kitchen
- Webpage = Food

## Creating Your First Flask App 📝

Let's create a file called `app.py`. This will be our Flask application!

### Step 1: Create the File

Create a new file called `app.py` in your project folder.

### Step 2: Write This Code

```python
# Import Flask - this brings Flask into our program
from flask import Flask

# Create a Flask app - this is like creating a website
app = Flask(__name__)

# Create a route - this tells Flask what to show when someone visits a page
@app.route('/')
def hello():
    return 'Hello World!'

# Run the app - this starts our website
if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding the Code Line by Line 📖

Let's break down every single line:

### Line 1: `from flask import Flask`
- **What it does**: Gets Flask from the flask package
- **Like saying**: "Hey Python, I need the Flask tool!"
- **Why**: We can't use Flask unless we import it first

### Line 2: (Empty line)
- Just for readability - makes code easier to read!

### Line 3: `app = Flask(__name__)`
- **What it does**: Creates a Flask application
- **`app`**: The name we give our Flask application (you can call it anything!)
- **`Flask(__name__)`**: Creates a new Flask app
- **`__name__`**: Tells Flask where to find files (don't worry about this yet!)
- **Like saying**: "Create a new website called 'app'"

### Line 4: (Empty line)
- Just for spacing!

### Line 5: `@app.route('/')`
- **What it does**: Creates a "route" - a path on your website
- **`@`**: This is a "decorator" - it's like a special instruction
- **`app.route`**: Tells Flask: "When someone visits this path..."
- **`'/'`**: This is the homepage (like the front door of a house)
- **Like saying**: "When someone visits the homepage..."

### Line 6: `def hello():`
- **What it does**: Creates a function (a block of code that does something)
- **`def`**: Means "define a function"
- **`hello`**: The name of our function (you can call it anything!)
- **`()`**: Empty parentheses mean it doesn't need any information
- **`:`**: Means "here's what the function does"
- **Like saying**: "Here's a function called 'hello' that does something"

### Line 7: `return 'Hello World!'`
- **What it does**: Sends "Hello World!" back to the browser
- **`return`**: Means "send this back"
- **`'Hello World!'`**: The text we want to show
- **Like saying**: "Send back the words 'Hello World!'"

### Line 8: (Empty line)
- Just for spacing!

### Line 9: `if __name__ == '__main__':`
- **What it does**: Checks if we're running this file directly
- **`if`**: Means "only do this if..."
- **`__name__ == '__main__'`**: Means "if this is the main file being run"
- **Like saying**: "Only run the website if someone runs this file directly"

### Line 10: `app.run(debug=True)`
- **What it does**: Starts the Flask website
- **`app.run`**: Starts running our Flask app
- **`debug=True`**: Shows errors if something goes wrong (very helpful!)
- **Like saying**: "Start the website, and show me if anything breaks"

## Running Your First App 🚀

### Step 1: Make Sure Your Virtual Environment is Active

You should see `(venv)` at the start of your command line.

### Step 2: Run Your App

```bash
python app.py
```

### What You Should See:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### What This Means:

- **"Serving Flask app 'app'"**: Flask found your app!
- **"Debug mode: on"**: Errors will be shown (good for learning!)
- **"Running on http://127.0.0.1:5000"**: Your website is live!
- **"Press CTRL+C to quit"**: How to stop the server

## Viewing Your Website 🌐

### Step 1: Open Your Browser

Open Chrome, Firefox, or any web browser.

### Step 2: Visit Your Website

Type this in the address bar:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

### What You Should See:

Just the text: **Hello World!**

🎉 **Congratulations! You just created your first website!** 🎉

## Understanding the URL 🔗

Let's break down `http://127.0.0.1:5000`:

- **`http://`**: The protocol (how to communicate)
- **`127.0.0.1`**: Your computer's address (localhost = your computer)
- **`:`**: Separator
- **`5000`**: The port number (like a door number)

Think of it like:
- **127.0.0.1** = Your house address
- **5000** = The door number

## What is `@app.route('/')`? 🛣️

The `@app.route('/')` is like a sign that says:
- "When someone visits the homepage (`/`), run the `hello()` function"

The `/` means "homepage" or "root" of your website.

## Making Changes 🔄

### Try This:

1. Change `'Hello World!'` to `'Hello from Flask!'`
2. Save the file
3. Refresh your browser

**Wait!** If you have `debug=True`, Flask will automatically reload! Just refresh your browser and you'll see the change!

## Stopping Your Server 🛑

Press `CTRL + C` in your terminal to stop the Flask server.

## Common Mistakes and Fixes 🔧

### Mistake 1: "ModuleNotFoundError: No module named 'flask'"
**Fix**: Make sure your virtual environment is activated and Flask is installed!

### Mistake 2: "Address already in use"
**Fix**: Another Flask app is running. Stop it first or use a different port:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Mistake 3: Nothing shows in browser
**Fix**: 
- Make sure Flask is running (check terminal)
- Make sure you're visiting `http://127.0.0.1:5000`
- Check for errors in the terminal

## Experiment Time! 🧪

Try these experiments:

1. **Change the message**:
   ```python
   return 'Welcome to my first website!'
   ```

2. **Add emojis**:
   ```python
   return 'Hello World! 🎉'
   ```

3. **Add HTML**:
   ```python
   return '<h1>Hello World!</h1>'
   ```

## What You Learned! 📚

✅ How to create a Flask app  
✅ How to create a route  
✅ How to return text  
✅ How to run a Flask server  
✅ How to view your website in a browser  

## Key Concepts to Remember 💡

1. **`@app.route('/')`**: Creates a page route
2. **Functions**: Blocks of code that do something
3. **`return`**: Sends something back to the browser
4. **`app.run()`**: Starts the website
5. **`debug=True`**: Shows errors (very helpful!)

## What's Next? 🚀

Now that you can create a simple page, let's learn how to create MULTIPLE pages! In the next lesson, we'll learn about routing - how to make different pages for different URLs!

---

**Congratulations on building your first Flask app! You're officially a web developer! 🎉**

