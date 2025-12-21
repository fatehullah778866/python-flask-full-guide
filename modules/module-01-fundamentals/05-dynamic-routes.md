# Lesson 1.5: Dynamic Routes - Routes That Change! 🔄

## What are Dynamic Routes? 🎭

Think of dynamic routes like a template:

- **Static route**: `/about` - Always shows the same page
- **Dynamic route**: `/user/john` - Shows different content based on the name

It's like having a form letter where you fill in the name:
- "Hello, **John**!" 
- "Hello, **Sarah**!"
- "Hello, **Mike**!"

The route changes, but the structure stays the same!

## Why Use Dynamic Routes? 🤔

Imagine you have 1000 users. Without dynamic routes, you'd need:
```python
@app.route('/user/john')
@app.route('/user/sarah')
@app.route('/user/mike')
# ... 997 more routes! 😱
```

With dynamic routes, you just need:
```python
@app.route('/user/<name>')
```

One route handles ALL users! 🎉

## Creating Your First Dynamic Route 🎯

### Example 1: User Profiles

```python
from flask import Flask

app = Flask(__name__)

@app.route('/user/<name>')
def user_profile(name):
    return f'Hello, {name}!'
```

### Breaking It Down:

- **`<name>`**: This is a variable! It captures whatever comes after `/user/`
- **`def user_profile(name):`**: The `name` parameter receives the value
- **`f'Hello, {name}!'`**: Shows the name in the message

### Testing:

- Visit `http://127.0.0.1:5000/user/john` → Shows "Hello, john!"
- Visit `http://127.0.0.1:5000/user/sarah` → Shows "Hello, sarah!"
- Visit `http://127.0.0.1:5000/user/mike` → Shows "Hello, mike!"

## Understanding Variables in Routes 📦

### The `<variable>` Syntax:

```python
@app.route('/user/<name>')
```

- **`<` and `>`**: These brackets mean "this is a variable"
- **`name`**: The name of the variable (you can call it anything!)

### Using the Variable:

```python
def user_profile(name):  # name is the variable from the route
    return f'Hello, {name}!'
```

The variable from the route (`<name>`) automatically becomes a parameter in your function!

## Multiple Variables 🎪

You can have multiple variables in one route:

```python
@app.route('/user/<username>/post/<post_id>')
def show_post(username, post_id):
    return f'User {username} - Post {post_id}'
```

### Testing:

- Visit `http://127.0.0.1:5000/user/john/post/123`
- Shows: "User john - Post 123"

**Order matters!** The variables in the route must match the function parameters in order.

## Variable Types 🔢

By default, variables are strings (text). But you can specify types!

### String (Default - Text):
```python
@app.route('/user/<name>')  # name is a string
def user(name):
    return f'User: {name}'
```

### Integer (Numbers):
```python
@app.route('/post/<int:post_id>')  # post_id is a number
def post(post_id):
    return f'Post ID: {post_id}'
```

**Why use `int:`?**
- Without `int:`: `post_id` is "123" (text)
- With `int:`: `post_id` is 123 (number)

### Float (Decimal Numbers):
```python
@app.route('/price/<float:amount>')
def price(amount):
    return f'Price: ${amount}'
```

### Path (Can Include Slashes):
```python
@app.route('/file/<path:filepath>')
def file(filepath):
    return f'File: {filepath}'
```

This allows URLs like: `/file/folder/subfolder/file.txt`

## Type Converters Reference 📋

| Type | Example | What It Does |
|------|---------|--------------|
| `string` | `<name>` | Text (default) |
| `int` | `<int:id>` | Whole numbers |
| `float` | `<float:price>` | Decimal numbers |
| `path` | `<path:file>` | Text with slashes |
| `uuid` | `<uuid:id>` | UUID format |

## Real-World Examples 🌍

### Example 1: Blog Posts
```python
@app.route('/blog/<int:year>/<int:month>/<slug>')
def blog_post(year, month, slug):
    return f'Blog post from {year}/{month}: {slug}'
```

**URL**: `/blog/2024/12/my-first-post`  
**Shows**: "Blog post from 2024/12: my-first-post"

### Example 2: Product Pages
```python
@app.route('/product/<int:product_id>')
def product(product_id):
    return f'Product #{product_id}'
```

**URL**: `/product/456`  
**Shows**: "Product #456"

### Example 3: User Dashboard
```python
@app.route('/dashboard/<username>/<section>')
def dashboard(username, section):
    return f'{username}\'s {section} dashboard'
```

**URL**: `/dashboard/john/settings`  
**Shows**: "john's settings dashboard"

## Combining Static and Dynamic Routes 🎨

You can mix static and dynamic parts:

```python
@app.route('/')  # Static
def home():
    return 'Home'

@app.route('/about')  # Static
def about():
    return 'About'

@app.route('/user/<name>')  # Dynamic
def user(name):
    return f'User: {name}'
```

## Error Handling with Dynamic Routes ⚠️

### What Happens with Wrong Types?

```python
@app.route('/post/<int:post_id>')
def post(post_id):
    return f'Post: {post_id}'
```

- ✅ `/post/123` → Works! (123 is a number)
- ❌ `/post/abc` → 404 Error! (abc is not a number)

Flask automatically returns a 404 if the type doesn't match!

## Practice Exercises 🏋️

### Exercise 1: User Profiles
Create a route that shows: "Welcome, [name]! Your profile ID is [id]"

**Solution:**
```python
@app.route('/profile/<name>/<int:user_id>')
def profile(name, user_id):
    return f'Welcome, {name}! Your profile ID is {user_id}'
```

### Exercise 2: Shopping Categories
Create routes for:
- `/shop/category/electronics`
- `/shop/category/books`
- `/shop/category/clothing`

**Solution:**
```python
@app.route('/shop/category/<category_name>')
def category(category_name):
    return f'Browsing {category_name} category'
```

## Advanced: Optional Variables 🎁

You can make variables optional using defaults:

```python
@app.route('/user/<name>')
@app.route('/user/<name>/<int:page>')
def user(name, page=1):
    return f'User: {name}, Page: {page}'
```

- `/user/john` → Shows "User: john, Page: 1"
- `/user/john/5` → Shows "User: john, Page: 5"

## Best Practices ✨

### 1. Use Descriptive Variable Names
✅ **Good**: `<username>`, `<post_id>`, `<category_name>`  
❌ **Bad**: `<x>`, `<a>`, `<data>`

### 2. Use Appropriate Types
✅ **Good**: `<int:user_id>` for IDs  
❌ **Bad**: `<user_id>` when you know it's always a number

### 3. Keep Routes Simple
✅ **Good**: `/user/<name>`  
❌ **Bad**: `/user/<name>/<id>/<email>/<phone>/<address>`

## Common Mistakes 🔧

### Mistake 1: Variable Name Mismatch
```python
@app.route('/user/<name>')
def user(username):  # ❌ Wrong! Should be 'name'
    return f'Hello {username}'
```

**Fix**: Make sure the variable name matches!

### Mistake 2: Wrong Order
```python
@app.route('/user/<name>/<id>')
def user(id, name):  # ❌ Wrong order!
    return f'{name}: {id}'
```

**Fix**: Parameters must match route order!

### Mistake 3: Forgetting Type Conversion
```python
@app.route('/post/<post_id>')
def post(post_id):
    return post_id + 1  # ❌ Error! Can't add to string
```

**Fix**: Use `<int:post_id>` if you need a number!

## Complete Example 🎯

```python
from flask import Flask

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return 'Welcome!'

# User profile (dynamic)
@app.route('/user/<username>')
def user_profile(username):
    return f'Profile of {username}'

# Blog post (multiple variables)
@app.route('/blog/<int:year>/<slug>')
def blog_post(year, slug):
    return f'Post from {year}: {slug}'

# Product page (with type)
@app.route('/product/<int:product_id>')
def product(product_id):
    return f'Product #{product_id}'

if __name__ == '__main__':
    app.run(debug=True)
```

## What You Learned! 📚

✅ How to create dynamic routes  
✅ How to use variables in routes  
✅ Different variable types (string, int, float, path)  
✅ How to combine static and dynamic routes  
✅ Best practices for dynamic routes  

## Key Concepts 💡

1. **`<variable>`** = Captures part of the URL
2. **Type converters** = `int:`, `float:`, `path:` specify the type
3. **Function parameters** = Receive the variable values
4. **Multiple variables** = Can have many in one route

## What's Next? 🚀

Now you can create routes that change! Next, we'll learn about **requests and responses** - how to get information from users and send different types of data back!

---

**Awesome! You now know how to make routes that adapt to different users and content! 🎉**

