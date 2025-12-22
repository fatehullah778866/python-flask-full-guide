# Posts Tests
# Tests for blog post routes

import pytest
from app import db
from app.models import User, Post

def test_posts_list_page(client):
    """Test posts list page loads"""
    response = client.get('/posts/')
    assert response.status_code == 200
    assert b'All Blog Posts' in response.data

def test_create_post_requires_login(client):
    """Test that creating post requires login"""
    response = client.get('/posts/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please login' in response.data

def test_create_post(client, db_session):
    """Test creating a post"""
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
    
    # Create post
    response = client.post('/posts/create', data={
        'title': 'My First Post',
        'content': 'This is the content of my first post'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Post created successfully' in response.data
    
    # Check post was created
    post = Post.query.filter_by(title='My First Post').first()
    assert post is not None
    assert post.content == 'This is the content of my first post'
    assert post.author_id == user.id

def test_view_post(client, db_session):
    """Test viewing a post"""
    # Create user and post
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post = Post(title='Test Post', content='Test content', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    
    # View post
    response = client.get(f'/posts/{post.id}')
    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'Test content' in response.data

def test_edit_post(client, db_session):
    """Test editing a post"""
    # Create user and post
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post = Post(title='Original Title', content='Original content', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test1234!'
    })
    
    # Edit post
    response = client.post(f'/posts/{post.id}/edit', data={
        'title': 'Updated Title',
        'content': 'Updated content'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Post updated successfully' in response.data
    
    # Check post was updated
    updated_post = Post.query.get(post.id)
    assert updated_post.title == 'Updated Title'
    assert updated_post.content == 'Updated content'

def test_delete_post(client, db_session):
    """Test deleting a post"""
    # Create user and post
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post = Post(title='To Delete', content='This will be deleted', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    post_id = post.id
    
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Test1234!'
    })
    
    # Delete post (need to handle CSRF token)
    response = client.post(f'/posts/{post_id}/delete', follow_redirects=True)
    
    # Check post was deleted
    deleted_post = Post.query.get(post_id)
    assert deleted_post is None

