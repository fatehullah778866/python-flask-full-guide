# Tests for Flask Routes
# Test if routes work correctly

import pytest
import json
from app import db
from app.models import Post

def test_index_route(client):
    """Test home page route"""
    # Make GET request to home page
    response = client.get('/')
    
    # Check response
    assert response.status_code == 200
    assert b'Welcome' in response.data or response.data  # Page loaded

def test_get_posts_api(client, db_session):
    """Test GET /api/posts endpoint"""
    # Create some test posts
    post1 = Post(title='Post 1', content='Content 1')
    post2 = Post(title='Post 2', content='Content 2')
    
    db_session.session.add_all([post1, post2])
    db_session.session.commit()
    
    # Make GET request
    response = client.get('/api/posts')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['title'] == 'Post 1'
    assert data[1]['title'] == 'Post 2'

def test_get_single_post_api(client, db_session):
    """Test GET /api/posts/<id> endpoint"""
    # Create a post
    post = Post(title='Test Post', content='Test content')
    db_session.session.add(post)
    db_session.session.commit()
    
    # Make GET request
    response = client.get(f'/api/posts/{post.id}')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Post'
    assert data['content'] == 'Test content'

def test_create_post_api(client, db_session):
    """Test POST /api/posts endpoint"""
    # Post data
    post_data = {
        'title': 'New Post',
        'content': 'New content',
        'author': 'Test Author'
    }
    
    # Make POST request
    response = client.post(
        '/api/posts',
        data=json.dumps(post_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Post'
    
    # Check post was saved to database
    post = Post.query.first()
    assert post.title == 'New Post'
    assert post.content == 'New content'

def test_create_post_missing_title(client):
    """Test POST /api/posts without title (should fail)"""
    # Post data without title
    post_data = {
        'content': 'Some content'
    }
    
    # Make POST request
    response = client.post(
        '/api/posts',
        data=json.dumps(post_data),
        content_type='application/json'
    )
    
    # Should return error
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_update_post_api(client, db_session):
    """Test PUT /api/posts/<id> endpoint"""
    # Create a post
    post = Post(title='Old Title', content='Old content')
    db_session.session.add(post)
    db_session.session.commit()
    
    # Update data
    update_data = {
        'title': 'New Title',
        'content': 'New content'
    }
    
    # Make PUT request
    response = client.put(
        f'/api/posts/{post.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'New Title'
    assert data['content'] == 'New content'
    
    # Check database was updated
    updated_post = Post.query.get(post.id)
    assert updated_post.title == 'New Title'

def test_delete_post_api(client, db_session):
    """Test DELETE /api/posts/<id> endpoint"""
    # Create a post
    post = Post(title='To Delete', content='Will be deleted')
    db_session.session.add(post)
    db_session.session.commit()
    post_id = post.id
    
    # Make DELETE request
    response = client.delete(f'/api/posts/{post_id}')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    
    # Check post was deleted from database
    deleted_post = Post.query.get(post_id)
    assert deleted_post is None

def test_get_nonexistent_post(client):
    """Test GET /api/posts/<id> with non-existent ID"""
    # Make GET request for non-existent post
    response = client.get('/api/posts/999')
    
    # Should return 404
    assert response.status_code == 404

def test_delete_nonexistent_post(client):
    """Test DELETE /api/posts/<id> with non-existent ID"""
    # Make DELETE request for non-existent post
    response = client.delete('/api/posts/999')
    
    # Should return 404
    assert response.status_code == 404

