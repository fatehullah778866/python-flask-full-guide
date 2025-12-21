# Tests for Helper Functions
# Test utility functions

import pytest
from app import db, add_post

def test_add_post_helper(db_session):
    """Test the add_post helper function"""
    # Use helper function to add post
    post = add_post('Helper Post', 'Helper content', 'Helper Author')
    
    # Check post was created
    assert post.id is not None
    assert post.title == 'Helper Post'
    assert post.content == 'Helper content'
    assert post.author == 'Helper Author'
    
    # Check post was saved to database
    saved_post = db_session.session.query(db.Model).filter_by(id=post.id).first()
    assert saved_post is not None

def test_add_post_default_author(db_session):
    """Test add_post with default author"""
    # Use helper without author (should default to 'Anonymous')
    post = add_post('Test Post', 'Test content')
    
    # Check default author
    assert post.author == 'Anonymous'

