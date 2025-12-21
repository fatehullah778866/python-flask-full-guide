# Lesson 7.3: Integration Testing - Testing How Things Work Together! 🔗

## What is Integration Testing? 🎯

**Integration Testing** = Testing how different parts work together

Think of it like:
- **Unit Test** = Testing if the engine works
- **Integration Test** = Testing if engine + wheels + steering work together

**Integration Test = Testing the whole system working together!**

## Why Integration Testing? ✨

### Unit Tests vs Integration Tests:

- **Unit Test**: Tests one function in isolation
- **Integration Test**: Tests how functions work together

### Example:

**Unit Test**: Test login function
```python
def test_login_function():
    result = login('john', 'password')
    assert result == True
```

**Integration Test**: Test complete login flow
```python
def test_login_flow():
    # 1. User visits login page
    # 2. User enters credentials
    # 3. Form is submitted
    # 4. Database is checked
    # 5. Session is created
    # 6. User is redirected
```

## Testing Authentication Flow 🔐

### Complete Login Flow Test:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import pytest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SECRET_KEY'] = 'test-secret-key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect('/dashboard')
    return render_template_string('<form method="POST">...</form>')

# Integration test
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # Create test user
        user = User(username='john', password_hash=generate_password_hash('secret'))
        db.session.add(user)
        db.session.commit()
        yield app.test_client()
        db.drop_all()

def test_login_flow(client):
    """Test complete login flow"""
    # Step 1: Get login page
    response = client.get('/login')
    assert response.status_code == 200
    
    # Step 2: Submit login form
    response = client.post('/login', data={
        'username': 'john',
        'password': 'secret'
    }, follow_redirects=True)
    
    # Step 3: Check if redirected to dashboard
    assert response.status_code == 200
    assert b'dashboard' in response.data.lower()
    
    # Step 4: Check if session was created
    with client.session_transaction() as sess:
        assert 'user_id' in sess
```

## Testing API Endpoints 📡

### Complete API Flow Test:

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({"id": post.id, "title": post.title}), 201

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify({"id": post.id, "title": post.title})
    return jsonify({"error": "Not found"}), 404

# Integration test
def test_create_and_get_post(client):
    """Test creating a post and then getting it"""
    # Step 1: Create post
    response = client.post('/api/posts',
                          json={'title': 'Test Post', 'content': 'Test content'},
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    post_id = data['id']
    
    # Step 2: Get the post we just created
    response = client.get(f'/api/posts/{post_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Post'
```

## Testing Database Operations with Routes 🗄️

### Complete Database + Route Test:

```python
def test_user_registration_flow(client):
    """Test complete user registration"""
    # Step 1: Get registration page
    response = client.get('/register')
    assert response.status_code == 200
    
    # Step 2: Submit registration form
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@email.com',
        'password': 'secret123',
        'confirm_password': 'secret123'
    }, follow_redirects=True)
    
    # Step 3: Check if user was created in database
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@email.com'
    
    # Step 4: Check if redirected to login
    assert b'login' in response.data.lower() or b'success' in response.data.lower()
```

## Testing Multiple Steps 🔄

### Example: Blog Post Creation Flow

```python
def test_create_post_flow(client):
    """Test creating a post with all steps"""
    # Step 1: Login
    client.post('/login', data={'username': 'john', 'password': 'secret'})
    
    # Step 2: Get create post page
    response = client.get('/posts/create')
    assert response.status_code == 200
    
    # Step 3: Create post
    response = client.post('/posts/create', data={
        'title': 'My Post',
        'content': 'Post content here'
    }, follow_redirects=True)
    
    # Step 4: Check post appears in list
    response = client.get('/posts')
    assert b'My Post' in response.data
    
    # Step 5: Check post detail page
    with app.app_context():
        post = Post.query.filter_by(title='My Post').first()
        response = client.get(f'/posts/{post.id}')
        assert b'My Post' in response.data
        assert b'Post content here' in response.data
```

## Using Test Database 🗄️

### Setting Up Test Database:

```python
import pytest
import os
import tempfile

@pytest.fixture
def client():
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)
```

### Or Use In-Memory Database:

```python
@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
```

## Complete Integration Test Example 🎯

```python
import pytest
from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SECRET_KEY'] = 'test-secret'
app.config['TESTING'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return '<form method="POST"><input name="username"><input name="password"><button>Register</button></form>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect('/dashboard')
    return '<form method="POST"><input name="username"><input name="password"><button>Login</button></form>'

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return f'<h1>Dashboard</h1><p>Welcome, user {session["user_id"]}!</p>'

@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        post = Post(title=request.form['title'], content=request.form['content'], user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')
    return '<form method="POST"><input name="title"><textarea name="content"></textarea><button>Create</button></form>'

# Test fixtures
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# Integration tests
def test_registration_and_login_flow(client):
    """Test complete registration and login flow"""
    # Register
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Login
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_create_post_flow(client):
    """Test creating a post after login"""
    # Create user and login
    with app.app_context():
        user = User(username='john', password_hash=generate_password_hash('secret'))
        db.session.add(user)
        db.session.commit()
    
    # Login
    client.post('/login', data={'username': 'john', 'password': 'secret'}, follow_redirects=True)
    
    # Create post
    response = client.post('/posts/create', data={
        'title': 'Test Post',
        'content': 'Test content'
    }, follow_redirects=True)
    
    # Check post was created
    with app.app_context():
        post = Post.query.first()
        assert post is not None
        assert post.title == 'Test Post'
```

## Testing with Sessions 🎫

### Testing Session Data:

```python
def test_session_after_login(client):
    """Test that session is created after login"""
    # Login
    with client.session_transaction() as sess:
        # Before login
        assert 'user_id' not in sess
    
    client.post('/login', data={'username': 'john', 'password': 'secret'})
    
    with client.session_transaction() as sess:
        # After login
        assert 'user_id' in sess
        assert sess['user_id'] == 1
```

## Best Practices ✨

### 1. Test Complete Flows

```python
# ✅ Good - tests complete flow
def test_user_can_register_and_login():
    # Register → Login → Access dashboard
    pass

# ❌ Bad - tests are too isolated
def test_register():
    # Only registration
    pass
```

### 2. Use Realistic Data

```python
# ✅ Good - realistic data
client.post('/register', data={
    'username': 'john_doe',
    'email': 'john@example.com',
    'password': 'SecurePass123!'
})

# ❌ Bad - unrealistic data
client.post('/register', data={
    'username': 'a',
    'email': 'b',
    'password': 'c'
})
```

### 3. Clean Up After Tests

```python
# ✅ Good - clean up
@pytest.fixture
def client():
    db.create_all()
    yield app.test_client()
    db.drop_all()  # Clean up!
```

## What You Learned! 📚

✅ What integration testing is  
✅ How to test complete flows  
✅ How to test authentication flows  
✅ How to test API endpoints  
✅ How to test database operations with routes  
✅ How to test multiple steps  
✅ How to test sessions  

## Key Concepts 💡

1. **Integration Test** = Test how parts work together
2. **Flow** = Complete process from start to finish
3. **Test Client** = Fake browser for testing
4. **Session Testing** = Testing session data
5. **Follow Redirects** = Follow redirects in tests

## What's Next? 🚀

You now know integration testing! Next, we'll learn about **Test Coverage** - making sure you test everything!

---

**Great job! You can test complete features! 🎉**

