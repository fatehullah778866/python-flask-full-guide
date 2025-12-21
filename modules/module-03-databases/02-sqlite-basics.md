# Lesson 3.2: SQLite Basics - Your First Database! 🗄️

## What is SQLite? 🧪

**SQLite** is like a **tiny, simple database** that lives in a single file on your computer!

### Why SQLite is Perfect for Learning:

- ✅ **Simple** - No server needed, just a file!
- ✅ **Built-in** - Comes with Python (no extra installation!)
- ✅ **Fast** - Perfect for small to medium projects
- ✅ **Free** - Completely free and open source
- ✅ **Portable** - Just copy the file to move your database

### Think of SQLite Like:

- **Big databases** (MySQL, PostgreSQL) = Big warehouses
- **SQLite** = A filing cabinet in your room

**Perfect for learning and small projects!**

## How SQLite Works 📁

SQLite stores everything in **one file**:

```
my_database.db  ← This file contains everything!
```

Inside this file:
- All your tables
- All your data
- Everything organized

**That's it!** Just one file!

## Setting Up SQLite in Flask ⚙️

### Step 1: Install Flask-SQLAlchemy

Flask-SQLAlchemy is a tool that makes databases easy in Flask:

```bash
pip install flask-sqlalchemy
```

### Step 2: Configure Flask for Database

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)
```

### Breaking It Down:

- **`SQLALCHEMY_DATABASE_URI`** = Where to save the database file
- **`sqlite:///`** = Tells Flask to use SQLite
- **`database.db`** = Name of the database file
- **`SQLAlchemy(app)`** = Creates the database connection

## Understanding the Database File 📂

When you run your Flask app, SQLite creates a file:

```
your_project/
  ├── app.py
  ├── database.db  ← Created automatically!
  └── ...
```

**The `.db` file is your database!** All your data is stored there.

## Creating Your First Table (Model) 📋

In Flask-SQLAlchemy, we create **models** (which become tables):

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<User {self.name}>'
```

### Breaking It Down:

- **`class User(db.Model)`** = Creates a User table
- **`id = db.Column(...)`** = Creates an id column
- **`primary_key=True`** = Makes this the unique identifier
- **`db.String(100)`** = Text field, max 100 characters
- **`db.Integer`** = Number field
- **`nullable=False`** = This field is required
- **`unique=True`** = No two users can have the same email

## Understanding Column Types 📊

### Common Column Types:

1. **String** - Text
   ```python
   name = db.Column(db.String(100))  # Text, max 100 characters
   ```

2. **Integer** - Whole numbers
   ```python
   age = db.Column(db.Integer)  # Numbers like 25, 30, 100
   ```

3. **Float** - Decimal numbers
   ```python
   price = db.Column(db.Float)  # Numbers like 19.99, 100.50
   ```

4. **Boolean** - True/False
   ```python
   is_active = db.Column(db.Boolean, default=True)  # True or False
   ```

5. **DateTime** - Dates and times
   ```python
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   ```

6. **Text** - Long text
   ```python
   content = db.Column(db.Text)  # For long text (like blog posts)
   ```

## Creating the Database Tables 🏗️

After defining your models, create the tables:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Create all tables
with app.app_context():
    db.create_all()
    print("Database created!")

if __name__ == '__main__':
    app.run(debug=True)
```

### What `db.create_all()` Does:

- Looks at all your models (User, Post, etc.)
- Creates tables in the database
- Only creates if they don't exist (safe to run multiple times!)

## Your First Complete Example 🎯

Let's create a simple user database:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<User {self.name}>'

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database and tables created!")

# Route to add a user
@app.route('/add-user/<name>/<email>')
def add_user(name, email):
    user = User(name=name, email=email, age=25)
    db.session.add(user)
    db.session.commit()
    return f'User {name} added!'

# Route to get all users
@app.route('/users')
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    return '<br>'.join(result) if result else 'No users found!'

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding Database Sessions 🔄

### What is a Session?

A **session** is like a **transaction** - a group of changes you want to make together:

```python
# Start a transaction
user1 = User(name="John", email="john@email.com")
user2 = User(name="Sarah", email="sarah@email.com")

# Add to session (not saved yet!)
db.session.add(user1)
db.session.add(user2)

# Commit (save everything!)
db.session.commit()
```

### Why Use Sessions?

- **Atomicity** - All changes happen together, or none do
- **Safety** - If something fails, nothing is saved
- **Efficiency** - Batch multiple changes

## Basic CRUD Operations 📝

### Create (Add New Data)

```python
# Create a new user
user = User(name="John", email="john@email.com", age=25)
db.session.add(user)
db.session.commit()
print(f"User {user.name} created with ID: {user.id}")
```

### Read (Get Data)

```python
# Get all users
all_users = User.query.all()

# Get one user by ID
user = User.query.get(1)

# Get one user by email
user = User.query.filter_by(email="john@email.com").first()
```

### Update (Change Data)

```python
# Get user
user = User.query.get(1)

# Change data
user.name = "John Updated"
user.age = 26

# Save changes
db.session.commit()
```

### Delete (Remove Data)

```python
# Get user
user = User.query.get(1)

# Delete
db.session.delete(user)
db.session.commit()
```

## Viewing Your Database 🔍

### Method 1: Using Python

```python
# Get all users
users = User.query.all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
```

### Method 2: Using SQLite Browser (Optional)

Download DB Browser for SQLite (free tool):
- Open `database.db` file
- View all tables and data
- Run SQL queries

## Common Mistakes 🔧

### Mistake 1: Forgetting to Import
```python
from flask_sqlalchemy import SQLAlchemy  # ✅ Don't forget!
```

### Mistake 2: Forgetting to Create Tables
```python
db.create_all()  # ✅ Must run this first!
```

### Mistake 3: Forgetting to Commit
```python
db.session.add(user)
# ❌ Missing commit!
db.session.commit()  # ✅ Must commit to save!
```

### Mistake 4: Wrong App Context
```python
# ❌ Wrong - outside app context
db.create_all()

# ✅ Correct - inside app context
with app.app_context():
    db.create_all()
```

## Practice Exercise 🏋️

Create a simple blog database:

1. **Post Model** with:
   - id (primary key)
   - title (string, required)
   - content (text, required)
   - created_at (datetime)

2. **Routes**:
   - `/add-post/<title>/<content>` - Add a post
   - `/posts` - Show all posts
   - `/post/<id>` - Show one post

**Try it yourself!**

## What You Learned! 📚

✅ What SQLite is and why it's great for learning  
✅ How to set up SQLite in Flask  
✅ How to create models (tables)  
✅ Understanding column types  
✅ How to create database tables  
✅ Basic CRUD operations  
✅ Understanding database sessions  

## Key Concepts 💡

1. **SQLite** = Simple database in a file
2. **Model** = Python class that becomes a database table
3. **Column** = Field in a table (name, email, etc.)
4. **Primary Key** = Unique ID for each row
5. **Session** = Group of database changes
6. **Commit** = Save changes to database
7. **Query** = Asking database for data

## What's Next? 🚀

You now know the basics! Next, we'll learn about **SQLAlchemy ORM** - a better way to work with databases that makes everything easier!

---

**Excellent work! You've created your first database! 🎉**

