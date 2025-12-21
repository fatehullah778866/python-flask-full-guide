# Lesson 1.4: Routing Basics - Creating Multiple Pages 🛣️

## What is Routing? 🗺️

Think of routing like creating a map for your website:

- **Route** = A path on your website (like `/about` or `/contact`)
- **Routing** = Telling Flask what to show when someone visits each path

It's like having different rooms in a house:
- `/` = Front door (homepage)
- `/about` = Living room (about page)
- `/contact` = Kitchen (contact page)

## Understanding URLs 🔗

Let's break down a URL:

```
http://www.example.com/about
```

- **`http://`** = How to communicate (protocol)
- **`www.example.com`** = The website address (domain)
- **`/about`** = The route (which page to show)

In Flask, we focus on the route part (`/about`).

## Creating Your First Route 🎯

Let's add more pages to your Flask app!

### Update Your `app.py`:

```python
from flask import Flask

app = Flask(__name__)

# Homepage route
@app.route('/')
def hello():
    return 'Hello World!'

# About page route
@app.route('/about')
def about():
    return 'This is the about page!'

# Contact page route
@app.route('/contact')
def contact():
    return 'This is the contact page!'
```

## Understanding the Code 📖

### The Homepage Route:
```python
@app.route('/')
def hello():
    return 'Hello World!'
```

- **`@app.route('/')`**: When someone visits the homepage
- **`def hello():`**: Run this function
- **`return 'Hello World!'`**: Show this text

### The About Route:
```python
@app.route('/about')
def about():
    return 'This is the about page!'
```

- **`@app.route('/about')`**: When someone visits `/about`
- **`def about():`**: Run this function
- **`return 'This is the about page!'`**: Show this text

## Testing Your Routes 🧪

1. **Start your Flask app**: `python app.py`
2. **Visit these URLs in your browser**:
   - `http://127.0.0.1:5000/` → Shows "Hello World!"
   - `http://127.0.0.1:5000/about` → Shows "This is the about page!"
   - `http://127.0.0.1:5000/contact` → Shows "This is the contact page!"

## Route Patterns 📐

### Pattern 1: Simple Routes
```python
@app.route('/home')
def home():
    return 'Home Page'
```

**URL**: `http://127.0.0.1:5000/home`

### Pattern 2: Nested Routes (Sub-pages)
```python
@app.route('/products/laptops')
def laptops():
    return 'Laptop Products'
```

**URL**: `http://127.0.0.1:5000/products/laptops`

Think of it like folders:
- `/products` = Main folder
- `/products/laptops` = Sub-folder inside products

### Pattern 3: Dynamic Routes (Coming Soon!)
We'll learn this in the next lesson - routes that change based on user input!

## Function Names Don't Matter! 🎭

The function name can be anything! These all work the same:

```python
@app.route('/about')
def about():
    return 'About Page'

@app.route('/about')
def show_about():
    return 'About Page'

@app.route('/about')
def my_cool_function():
    return 'About Page'
```

**What matters is the route (`/about`), not the function name!**

## Multiple Routes, One Function 🔄

You can have multiple routes point to the same function:

```python
@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return 'Home Page'
```

Now all three URLs show the same page:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/home`
- `http://127.0.0.1:5000/index`

## HTTP Methods Explained 📡

### What are HTTP Methods?

HTTP methods are like different types of requests:

- **GET** = "Give me information" (like reading a book)
- **POST** = "Here's new information" (like submitting a form)
- **PUT** = "Update this information" (like editing a document)
- **DELETE** = "Remove this information" (like deleting a file)

### Default Method: GET

By default, all routes use GET:

```python
@app.route('/about')  # This is a GET request
def about():
    return 'About Page'
```

### Specifying Methods:

```python
@app.route('/submit', methods=['POST'])
def submit():
    return 'Form submitted!'
```

**For now, we'll mostly use GET. We'll learn POST when we do forms!**

## Common Route Patterns 🎨

### Pattern 1: Simple Pages
```python
@app.route('/')
def index():
    return 'Homepage'

@app.route('/about')
def about():
    return 'About Us'

@app.route('/services')
def services():
    return 'Our Services'
```

### Pattern 2: Organized Sections
```python
@app.route('/blog')
def blog():
    return 'Blog Home'

@app.route('/blog/post1')
def post1():
    return 'First Post'

@app.route('/blog/post2')
def post2():
    return 'Second Post'
```

### Pattern 3: User Pages
```python
@app.route('/user/profile')
def profile():
    return 'User Profile'

@app.route('/user/settings')
def settings():
    return 'User Settings'
```

## Best Practices ✨

### 1. Use Clear Route Names
✅ **Good**: `/about`, `/contact`, `/products`  
❌ **Bad**: `/a`, `/page1`, `/stuff`

### 2. Use Lowercase
✅ **Good**: `/about-us`  
❌ **Bad**: `/About-Us` (can cause confusion)

### 3. Use Hyphens, Not Underscores
✅ **Good**: `/about-us`  
❌ **Bad**: `/about_us` (hyphens are more web-friendly)

### 4. Keep It Simple
✅ **Good**: `/contact`  
❌ **Bad**: `/contact-us-now-here` (too long!)

## Practice Exercise 🏋️

Create a simple website with these pages:

1. Homepage (`/`) - "Welcome to my website!"
2. About (`/about`) - "Learn about us!"
3. Services (`/services`) - "Our services"
4. Contact (`/contact`) - "Contact us!"

**Try it yourself before looking at the solution!**

## Solution 💡

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to my website!'

@app.route('/about')
def about():
    return 'Learn about us!'

@app.route('/services')
def services():
    return 'Our services'

@app.route('/contact')
def contact():
    return 'Contact us!'

if __name__ == '__main__':
    app.run(debug=True)
```

## What You Learned! 📚

✅ How to create multiple routes  
✅ How different URLs show different pages  
✅ Understanding route patterns  
✅ HTTP methods basics  
✅ Best practices for routes  

## Key Concepts 💡

1. **Route** = A path on your website (`/about`)
2. **Function** = What happens when someone visits that route
3. **Multiple routes** = Multiple pages on your website
4. **GET method** = Default method for viewing pages

## Common Mistakes 🔧

### Mistake 1: Forgetting the `/` at the start
```python
@app.route('about')  # ❌ Wrong - missing /
@app.route('/about')  # ✅ Correct
```

### Mistake 2: Same route name twice
```python
@app.route('/about')
def about():
    return 'About'

@app.route('/about')  # ❌ Error! Can't have two routes with same path
def about2():
    return 'About 2'
```

### Mistake 3: Forgetting to return something
```python
@app.route('/about')
def about():
    print('About page')  # ❌ This won't show in browser!
    return 'About page'  # ✅ This will show!
```

## What's Next? 🚀

Now you can create multiple pages! Next, we'll learn about **dynamic routes** - routes that change based on what the user wants (like showing different user profiles)!

---

**Great job! You now know how to create multiple pages on your website! 🎉**

