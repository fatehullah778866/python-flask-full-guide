# Tests for Database Models
# Test if models work correctly

import pytest
from app import db
from app.models import Post
from datetime import datetime

def test_create_post(test_app):
    """Test creating a post"""
    with test_app.app_context():
        # Create a post
        post = Post(
            title='Test Post',
            content='This is a test post',
            author='Test Author'
        )
        
        # Add to database
        db.session.add(post)
        db.session.commit()
        
        # Check if post was saved
        saved_post = Post.query.first()
        assert saved_post is not None
        assert saved_post.title == 'Test Post'
        assert saved_post.content == 'This is a test post'
        assert saved_post.author == 'Test Author'

def test_post_to_dict(test_app):
    """Test converting post to dictionary"""
    with test_app.app_context():
        # Create a post
        post = Post(
            title='Test Post',
            content='Test content',
            author='Test Author'
        )
        
        db.session.add(post)
        db.session.commit()
        
        # Convert to dictionary
        post_dict = post.to_dict()
        
        # Check dictionary structure
        assert 'id' in post_dict
        assert 'title' in post_dict
        assert 'content' in post_dict
        assert 'author' in post_dict
        assert 'date_created' in post_dict
        assert post_dict['title'] == 'Test Post'

def test_post_defaults(test_app):
    """Test post default values"""
    with test_app.app_context():
        # Create post without author (should default to 'Anonymous')
        post = Post(
            title='Test Post',
            content='Test content'
        )
        
        db.session.add(post)
        db.session.commit()
        
        # Check defaults
        assert post.author == 'Anonymous'
        assert post.date_created is not None

def test_multiple_posts(test_app):
    """Test creating multiple posts"""
    with test_app.app_context():
        # Create multiple posts
        post1 = Post(title='Post 1', content='Content 1')
        post2 = Post(title='Post 2', content='Content 2')
        post3 = Post(title='Post 3', content='Content 3')
        
        db.session.add_all([post1, post2, post3])
        db.session.commit()
        
        # Check all posts were saved
        posts = Post.query.all()
        assert len(posts) == 3
        assert posts[0].title == 'Post 1'
        assert posts[1].title == 'Post 2'
        assert posts[2].title == 'Post 3'

def test_delete_post(test_app):
    """Test deleting a post"""
    with test_app.app_context():
        # Create a post
        post = Post(title='Test Post', content='Test content')
        db.session.add(post)
        db.session.commit()
        
        # Delete the post
        db.session.delete(post)
        db.session.commit()
        
        # Check post was deleted
        posts = Post.query.all()
        assert len(posts) == 0

