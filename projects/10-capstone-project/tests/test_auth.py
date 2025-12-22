# Authentication Tests
# Tests for authentication routes

import pytest
from app import db
from app.models import User

def test_register_page(client):
    """Test registration page loads"""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Create Account' in response.data

def test_user_registration(client, db_session):
    """Test user registration"""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'SecurePass123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    # Check user was created
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.email == 'newuser@example.com'
    assert user.check_password('SecurePass123!') == True

def test_duplicate_username_registration(client, db_session):
    """Test registration with duplicate username"""
    # Create first user
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    # Try to register with same username
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'Test1234!'
    })
    
    assert response.status_code == 200
    assert b'Username already exists' in response.data

def test_login_page(client):
    """Test login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_user_login(client, db_session):
    """Test user login"""
    # Create user
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    # Login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test1234!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login successful' in response.data
    
    # Check session
    with client.session_transaction() as sess:
        assert 'user_id' in sess
        assert sess['user_id'] == user.id

def test_invalid_login(client, db_session):
    """Test login with wrong password"""
    # Create user
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    # Try to login with wrong password
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'WrongPassword'
    })
    
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_logout(client, db_session):
    """Test user logout"""
    # Create and login user
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    # Login first
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test1234!'
    })
    
    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'logged out' in response.data.lower()
    
    # Check session cleared
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

