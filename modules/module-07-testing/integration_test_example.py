# Integration Testing Example
# This shows how to test complete flows in Flask applications

from flask import Flask, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pytest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SECRET_KEY'] = 'test-secret-key'
app.config['TESTING'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return '''
    <form method="POST">
        <input name="username" placeholder="Username" required>
        <input name="email" placeholder="Email" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Register</button>
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect('/dashboard')
        return 'Invalid credentials!', 401
    return '''
    <form method="POST">
        <input name="username" placeholder="Username" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    return f'<h1>Dashboard</h1><p>Welcome, {user.username}!</p>'

@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        post = Post(title=request.form['title'], content=request.form['content'], user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')
    return '''
    <form method="POST">
        <input name="title" placeholder="Title" required>
        <textarea name="content" placeholder="Content" required></textarea>
        <button type="submit">Create Post</button>
    </form>
    '''

@app.route('/posts')
def list_posts():
    posts = Post.query.all()
    result = '<h1>All Posts</h1><ul>'
    for post in posts:
        result += f'<li>{post.title}</li>'
    result += '</ul>'
    return result

# Test fixtures
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# Integration tests
def test_registration_flow(client):
    """Test complete registration flow"""
    # Get registration page
    response = client.get('/register')
    assert response.status_code == 200
    
    # Register
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@email.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Check user was created
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'test@email.com'

def test_login_flow(client):
    """Test complete login flow"""
    # Create user first
    with app.app_context():
        user = User(username='john', email='john@email.com', password_hash=generate_password_hash('secret'))
        db.session.add(user)
        db.session.commit()
    
    # Get login page
    response = client.get('/login')
    assert response.status_code == 200
    
    # Login
    response = client.post('/login', data={
        'username': 'john',
        'password': 'secret'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data
    assert b'john' in response.data
    
    # Check session
    with client.session_transaction() as sess:
        assert 'user_id' in sess

def test_create_post_flow(client):
    """Test creating a post after login"""
    # Create user and login
    with app.app_context():
        user = User(username='john', email='john@email.com', password_hash=generate_password_hash('secret'))
        db.session.add(user)
        db.session.commit()
    
    # Login
    client.post('/login', data={'username': 'john', 'password': 'secret'}, follow_redirects=True)
    
    # Get create post page
    response = client.get('/posts/create')
    assert response.status_code == 200
    
    # Create post
    response = client.post('/posts/create', data={
        'title': 'My First Post',
        'content': 'This is my first post!'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Check post was created
    with app.app_context():
        post = Post.query.first()
        assert post is not None
        assert post.title == 'My First Post'
        assert post.user_id == 1
    
    # Check post appears in list
    response = client.get('/posts')
    assert b'My First Post' in response.data

def test_protected_route_redirect(client):
    """Test that protected routes redirect to login"""
    # Try to access dashboard without login
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302  # Redirect
    assert '/login' in response.location

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

