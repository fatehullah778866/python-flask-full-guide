# Lesson 7.2: Unit Testing - Testing Small Pieces! 🔬

## What is Unit Testing? 🎯

**Unit Testing** = Testing one small piece of code at a time

Think of it like:
- **Unit** = One ingredient in a recipe
- **Unit Test** = Testing if that one ingredient is good
- **Example**: Testing if salt is salty (not testing the whole dish!)

**Unit Test = Testing one function, one route, one small piece!**

## Why Unit Testing? ✨

### Benefits:

1. **Fast** - Tests run quickly
2. **Isolated** - Test one thing at a time
3. **Easy to Debug** - Know exactly what's wrong
4. **Confidence** - Know each piece works

## Installing pytest 📦

**pytest** = A tool for running tests (better than unittest!)

```bash
pip install pytest
```

**That's it!** pytest is now installed.

## Your First Unit Test 🎯

### Step 1: Create a Function to Test

```python
# calculator.py
def add(a, b):
    """Add two numbers"""
    return a + b

def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
```

### Step 2: Create a Test File

```python
# test_calculator.py
from calculator import add, divide

def test_add():
    """Test the add function"""
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(10, 20) == 30

def test_divide():
    """Test the divide function"""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(1, 1) == 1

def test_divide_by_zero():
    """Test that dividing by zero raises an error"""
    try:
        divide(10, 0)
        assert False, "Should have raised an error!"
    except ValueError:
        assert True  # Expected error!
```

### Step 3: Run Tests

```bash
pytest test_calculator.py
```

**Output:**
```
test_calculator.py::test_add PASSED
test_calculator.py::test_divide PASSED
test_calculator.py::test_divide_by_zero PASSED
```

## Testing Flask Routes 🛣️

### Setting Up Flask Test Client

```python
from flask import Flask
import pytest

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'

# Test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

### Testing Routes

```python
def test_home(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello World!' in response.data

def test_user(client):
    """Test the user route"""
    response = client.get('/user/John')
    assert response.status_code == 200
    assert b'Hello, John!' in response.data
```

## Understanding Test Client 🔧

### What is a Test Client?

**Test Client** = A fake browser for testing

- **Real Browser** = You visit website
- **Test Client** = Code visits website (for testing)

### Test Client Methods:

```python
# GET request
response = client.get('/')

# POST request
response = client.post('/login', data={'username': 'john'})

# Check response
assert response.status_code == 200
assert b'Hello' in response.data
```

## Testing POST Requests 📤

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'secret':
        return 'Login successful!'
    return 'Invalid credentials!', 401

# Test
def test_login_success(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'secret'
    })
    assert response.status_code == 200
    assert b'Login successful!' in response.data

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'wrong'
    })
    assert response.status_code == 401
    assert b'Invalid credentials!' in response.data
```

## Testing JSON APIs 📄

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify({"id": 1, "name": data['name']}), 201

# Test
def test_create_user(client):
    response = client.post('/api/users',
                          json={'name': 'John'},
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'John'
    assert data['id'] == 1
```

## Testing Database Operations 🗄️

### Setting Up Test Database

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Test fixture
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
```

### Testing Database Operations

```python
def test_create_user(client):
    """Test creating a user"""
    with app.app_context():
        user = User(name='John')
        db.session.add(user)
        db.session.commit()
        
        # Check if user was created
        user = User.query.first()
        assert user.name == 'John'
        assert user.id == 1
```

## Using Fixtures 🎁

### What is a Fixture?

**Fixture** = Setup code that runs before tests

```python
@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    return User(name='Test User', email='test@email.com')

def test_user_name(sample_user):
    """Test using the fixture"""
    assert sample_user.name == 'Test User'
```

### Common Fixtures:

```python
@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_session():
    """Database session fixture"""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
```

## Complete Unit Testing Example 🎯

```python
# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({"users": [{"id": u.id, "name": u.name} for u in users]})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name}), 201

# test_app.py
import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_get_users_empty(client):
    """Test getting users when none exist"""
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data['users'] == []

def test_create_user(client):
    """Test creating a user"""
    response = client.post('/api/users',
                          json={'name': 'John', 'email': 'john@email.com'},
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'John'
    assert 'id' in data

def test_get_users(client):
    """Test getting users after creating one"""
    # Create user first
    with app.app_context():
        user = User(name='John', email='john@email.com')
        db.session.add(user)
        db.session.commit()
    
    # Get users
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['users']) == 1
    assert data['users'][0]['name'] == 'John'
```

## Running Tests 🚀

### Run All Tests:

```bash
pytest
```

### Run Specific Test File:

```bash
pytest test_app.py
```

### Run Specific Test:

```bash
pytest test_app.py::test_create_user
```

### Run with Verbose Output:

```bash
pytest -v
```

## Common Mistakes 🔧

### Mistake 1: Not Using Test Database

```python
# ❌ Uses production database!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# ✅ Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

### Mistake 2: Not Cleaning Up

```python
# ❌ Data persists between tests
def test_one():
    user = User(name='John')
    db.session.add(user)
    db.session.commit()

# ✅ Clean up after each test
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()  # Clean up!
```

### Mistake 3: Testing Too Much at Once

```python
# ❌ Testing everything at once
def test_everything():
    # Create user, login, post, comment, etc.
    pass

# ✅ Test one thing at a time
def test_create_user():
    # Only test creating user
    pass
```

## What You Learned! 📚

✅ What unit testing is  
✅ How to install and use pytest  
✅ How to test Flask routes  
✅ How to test POST requests  
✅ How to test JSON APIs  
✅ How to test database operations  
✅ How to use fixtures  
✅ How to run tests  

## Key Concepts 💡

1. **Unit Test** = Test one small piece
2. **pytest** = Tool for running tests
3. **Test Client** = Fake browser for testing
4. **Fixture** = Setup code for tests
5. **Assert** = Check if something is true
6. **Test Database** = Separate database for testing

## What's Next? 🚀

You now know unit testing! Next, we'll learn about **Integration Testing** - testing how different parts work together!

---

**Excellent! You can now write unit tests! 🎉**

