# Model Tests
# Tests for database models

import pytest
from app import db
from app.models import User, Post
from datetime import datetime

def test_user_creation(db_session):
    """Test creating a user"""
    user = User(
        username='testuser',
        email='test@example.com'
    )
    user.set_password('Test1234!')
    
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.password_hash != 'Test1234!'  # Should be hashed
    assert user.check_password('Test1234!') == True
    assert user.check_password('WrongPassword') == False

def test_post_creation(db_session):
    """Test creating a post"""
    # Create user first
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    # Create post
    post = Post(
        title='Test Post',
        content='This is a test post',
        author_id=user.id
    )
    
    db.session.add(post)
    db.session.commit()
    
    assert post.id is not None
    assert post.title == 'Test Post'
    assert post.content == 'This is a test post'
    assert post.author_id == user.id
    assert post.author == user

def test_user_to_dict(db_session):
    """Test user to_dict method"""
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    user_dict = user.to_dict()
    
    assert user_dict['id'] == user.id
    assert user_dict['username'] == 'testuser'
    assert user_dict['email'] == 'test@example.com'
    assert 'password_hash' not in user_dict  # Should not include password

def test_post_to_dict(db_session):
    """Test post to_dict method"""
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    
    post = Post(title='Test Post', content='Content', author_id=user.id)
    db.session.add(post)
    db.session.commit()
    
    post_dict = post.to_dict()
    
    assert post_dict['id'] == post.id
    assert post_dict['title'] == 'Test Post'
    assert post_dict['author'] == 'testuser'

