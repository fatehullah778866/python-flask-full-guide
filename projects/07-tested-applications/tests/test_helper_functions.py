# Tests for Helper Functions
# Test utility functions

import pytest
from app import db, add_post, Post

def test_add_post_helper(test_app):
    """Test the add_post helper function"""
    with test_app.app_context():
        # Use helper function to add post
        post = add_post('Helper Post', 'Helper content', 'Helper Author')
        
        # Check post was created
        assert post.id is not None
        assert post.title == 'Helper Post'
        assert post.content == 'Helper content'
        assert post.author == 'Helper Author'
        
        # Check post was saved to database
        saved_post = Post.query.get(post.id)
        assert saved_post is not None
        assert saved_post.title == 'Helper Post'

def test_add_post_default_author(test_app):
    """Test add_post with default author"""
    with test_app.app_context():
        # Use helper without author (should default to 'Anonymous')
        post = add_post('Test Post', 'Test content')
        
        # Check default author
        assert post.author == 'Anonymous'
        
        # Check post was saved
        saved_post = Post.query.get(post.id)
        assert saved_post is not None

