# API Tests
# Tests for RESTful API endpoints

import pytest
import json
from app import db
from app.models import User, Post

def test_api_health_check(client):
    """Test API health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_posts_api(client, db_session):
    """Test getting all posts via API"""
    # Create user and posts
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post1 = Post(title='Post 1', content='Content 1', author_id=user.id)
    post2 = Post(title='Post 2', content='Content 2', author_id=user.id)
    db.session.add_all([post1, post2])
    db.session.commit()
    
    # Get posts via API
    response = client.get('/api/posts')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] in ['Post 1', 'Post 2']

def test_get_single_post_api(client, db_session):
    """Test getting a single post via API"""
    # Create user and post
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post = Post(title='API Post', content='API Content', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    
    # Get post via API
    response = client.get(f'/api/posts/{post.id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['title'] == 'API Post'
    assert data['content'] == 'API Content'

def test_create_post_api_requires_auth(client):
    """Test that creating post via API requires authentication"""
    response = client.post('/api/posts', 
        json={'title': 'Test', 'content': 'Test'},
        content_type='application/json'
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'error' in data

def test_create_post_api(client, db_session):
    """Test creating a post via API"""
    # Create and login user
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test1234!'
    })
    
    # Create post via API
    response = client.post('/api/posts',
        json={'title': 'API Created Post', 'content': 'API Content'},
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'API Created Post'
    
    # Check post was created
    post = Post.query.filter_by(title='API Created Post').first()
    assert post is not None

def test_update_post_api(client, db_session):
    """Test updating a post via API"""
    # Create user and post
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post = Post(title='Original', content='Original content', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test1234!'
    })
    
    # Update post via API
    response = client.put(f'/api/posts/{post.id}',
        json={'title': 'Updated', 'content': 'Updated content'},
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated'
    
    # Check post was updated
    updated_post = Post.query.get(post.id)
    assert updated_post.title == 'Updated'

def test_get_users_api(client, db_session):
    """Test getting all users via API"""
    # Create users
    user1 = User(username='user1', email='user1@example.com')
    user1.set_password('Test1234!')
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('Test1234!')
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Get users via API
    response = client.get('/api/users')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 2

