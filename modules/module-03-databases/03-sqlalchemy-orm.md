# Lesson 3.3: SQLAlchemy ORM - Making Databases Easy! 🛠️

## What is SQLAlchemy ORM? 🤔

**SQLAlchemy** is like a **translator** between Python and databases!

### The Problem:

Writing SQL can be hard:
```sql
SELECT * FROM users WHERE age > 25 AND email LIKE '%@gmail.com' ORDER BY name
```

### The Solution: SQLAlchemy ORM

Write Python instead:
```python
User.query.filter(User.age > 25, User.email.contains('@gmail.com')).order_by(User.name).all()
```

**Much easier!** You write Python, SQLAlchemy writes SQL for you!

## What Does ORM Stand For? 📖

**ORM** = Object-Relational Mapping

- **Object** = Python objects (like `User`, `Post`)
- **Relational** = Database tables
- **Mapping** = Connecting them together

**ORM maps Python objects to database tables!**

## Why Use SQLAlchemy? ✨

### Benefits:

1. **Write Python, not SQL** - Easier and more familiar
2. **Type Safety** - Python catches errors
3. **Automatic** - Handles connections, queries, etc.
4. **Portable** - Works with SQLite, MySQL, PostgreSQL
5. **Relationships** - Easy to connect tables

## Installing Flask-SQLAlchemy 📦

```bash
pip install flask-sqlalchemy
```

That's it! Flask-SQLAlchemy includes SQLAlchemy.

## Setting Up SQLAlchemy ⚙️

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)
```

### Configuration Explained:

- **`SQLALCHEMY_DATABASE_URI`** = Where to save database
- **`sqlite:///`** = Use SQLite database
- **`SQLALCHEMY_TRACK_MODIFICATIONS`** = Set to False (saves resources)

## Creating Models (Tables) 📋

Models are Python classes that become database tables:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # Table name (optional - uses class name by default)
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Special method (for debugging)
    def __repr__(self):
        return f'<User {self.name}>'
```

### Breaking It Down:

- **`class User(db.Model)`** = Creates a User model (table)
- **`__tablename__`** = Name of table in database (optional)
- **`db.Column(...)`** = Creates a column
- **`primary_key=True`** = Unique identifier
- **`nullable=False`** = Required field
- **`unique=True`** = No duplicates allowed
- **`default=...`** = Default value

## Understanding Column Options 🔧

### Common Column Options:

1. **primary_key=True** - Unique ID
   ```python
   id = db.Column(db.Integer, primary_key=True)
   ```

2. **nullable=False** - Required field
   ```python
   name = db.Column(db.String(100), nullable=False)
   ```

3. **unique=True** - No duplicates
   ```python
   email = db.Column(db.String(100), unique=True)
   ```

4. **default=value** - Default value
   ```python
   is_active = db.Column(db.Boolean, default=True)
   ```

5. **index=True** - Faster searches
   ```python
   email = db.Column(db.String(100), index=True)
   ```

## Creating the Database 🏗️

After defining models, create the database:

```python
from datetime import datetime

# ... (app and db setup) ...

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create all tables
with app.app_context():
    db.create_all()
    print("✅ Database created!")
```

**Run this once to create tables!**

## Basic Queries (Reading Data) 📖

### Get All Records

```python
# Get all users
users = User.query.all()
for user in users:
    print(user.name, user.email)
```

### Get One Record by ID

```python
# Get user with ID = 1
user = User.query.get(1)
if user:
    print(user.name)
```

### Get First Record

```python
# Get first user
user = User.query.first()
```

### Filter Records

```python
# Get users with age > 25
users = User.query.filter(User.age > 25).all()

# Get user with specific email
user = User.query.filter_by(email="john@email.com").first()

# Multiple conditions
users = User.query.filter(User.age > 25, User.name.startswith('J')).all()
```

## Common Query Methods 🔍

### .all() - Get All Results
```python
users = User.query.all()  # Returns list of all users
```

### .first() - Get First Result
```python
user = User.query.first()  # Returns first user or None
```

### .get(id) - Get by ID
```python
user = User.query.get(1)  # Returns user with id=1 or None
```

### .filter() - Filter Results
```python
# Single condition
users = User.query.filter(User.age > 25).all()

# Multiple conditions (AND)
users = User.query.filter(User.age > 25, User.name == "John").all()

# OR condition
from sqlalchemy import or_
users = User.query.filter(or_(User.age > 25, User.name == "John")).all()
```

### .filter_by() - Simple Filtering
```python
# Simpler syntax for equality
user = User.query.filter_by(email="john@email.com").first()
```

### .order_by() - Sort Results
```python
# Sort by name (ascending)
users = User.query.order_by(User.name).all()

# Sort by age (descending)
users = User.query.order_by(User.age.desc()).all()
```

### .limit() - Limit Results
```python
# Get only first 5 users
users = User.query.limit(5).all()
```

## Creating Records (Adding Data) ➕

```python
# Create a new user
user = User(
    name="John Doe",
    email="john@email.com",
    age=25
)

# Add to session
db.session.add(user)

# Save to database
db.session.commit()

print(f"User created with ID: {user.id}")
```

### Adding Multiple Records

```python
# Create multiple users
user1 = User(name="John", email="john@email.com")
user2 = User(name="Sarah", email="sarah@email.com")
user3 = User(name="Mike", email="mike@email.com")

# Add all at once
db.session.add_all([user1, user2, user3])

# Save all
db.session.commit()
```

## Updating Records (Changing Data) ✏️

```python
# Get user
user = User.query.get(1)

# Change data
user.name = "John Updated"
user.age = 26

# Save changes
db.session.commit()
```

### Updating Multiple Records

```python
# Update all users with age < 18
users = User.query.filter(User.age < 18).all()
for user in users:
    user.age = 18

db.session.commit()
```

## Deleting Records (Removing Data) 🗑️

```python
# Get user
user = User.query.get(1)

# Delete
db.session.delete(user)

# Save changes
db.session.commit()
```

### Deleting Multiple Records

```python
# Delete all users with age > 100
users = User.query.filter(User.age > 100).all()
for user in users:
    db.session.delete(user)

db.session.commit()
```

## Query Operators 🔢

### Comparison Operators

```python
# Greater than
User.query.filter(User.age > 25).all()

# Less than
User.query.filter(User.age < 18).all()

# Equal to
User.query.filter(User.age == 25).all()

# Not equal to
User.query.filter(User.age != 25).all()

# Greater than or equal
User.query.filter(User.age >= 25).all()

# Less than or equal
User.query.filter(User.age <= 18).all()
```

### String Operators

```python
# Contains
User.query.filter(User.email.contains('@gmail.com')).all()

# Starts with
User.query.filter(User.name.startswith('J')).all()

# Ends with
User.query.filter(User.email.endswith('.com')).all()

# Like (pattern matching)
User.query.filter(User.name.like('J%')).all()  # Names starting with J
```

## Complete Example 🎯

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'

# Create tables
with app.app_context():
    db.create_all()

# Route to add user
@app.route('/add/<name>/<email>/<int:age>')
def add_user(name, email, age):
    user = User(name=name, email=email, age=age)
    db.session.add(user)
    db.session.commit()
    return f'User {name} added with ID: {user.id}'

# Route to get all users
@app.route('/users')
def get_users():
    users = User.query.all()
    if not users:
        return 'No users found!'
    result = []
    for user in users:
        result.append(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Age: {user.age}")
    return '<br>'.join(result)

# Route to get user by ID
@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return f"User: {user.name}, Email: {user.email}, Age: {user.age}"
    return 'User not found!'

# Route to update user
@app.route('/update/<int:user_id>/<new_name>')
def update_user(user_id, new_name):
    user = User.query.get(user_id)
    if user:
        user.name = new_name
        db.session.commit()
        return f'User updated to: {new_name}'
    return 'User not found!'

# Route to delete user
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return f'User {user.name} deleted!'
    return 'User not found!'

if __name__ == '__main__':
    app.run(debug=True)
```

## Common Mistakes 🔧

### Mistake 1: Forgetting to Commit
```python
db.session.add(user)
# ❌ Missing commit!
db.session.commit()  # ✅ Must commit!
```

### Mistake 2: Using .all() When You Need One
```python
user = User.query.filter_by(email="john@email.com").all()  # ❌ Returns list
user = User.query.filter_by(email="john@email.com").first()  # ✅ Returns one
```

### Mistake 3: Not Checking for None
```python
user = User.query.get(1)
print(user.name)  # ❌ Error if user doesn't exist!

user = User.query.get(1)
if user:  # ✅ Check first!
    print(user.name)
```

## What You Learned! 📚

✅ What SQLAlchemy ORM is and why it's useful  
✅ How to set up SQLAlchemy in Flask  
✅ How to create models (tables)  
✅ How to query data (read)  
✅ How to create records (add)  
✅ How to update records (change)  
✅ How to delete records (remove)  
✅ Query operators and methods  

## Key Concepts 💡

1. **ORM** = Object-Relational Mapping (Python to SQL translator)
2. **Model** = Python class that becomes a database table
3. **Query** = Asking database for data
4. **Session** = Group of database changes
5. **Commit** = Save changes to database
6. **Filter** = Narrow down results
7. **.all()** = Get all results
8. **.first()** = Get first result
9. **.get(id)** = Get by ID

## What's Next? 🚀

You now know how to work with single tables! Next, we'll learn about **relationships** - how to connect tables together (like connecting Users to Posts)!

---

**Amazing! You're becoming a database expert! 🎉**

