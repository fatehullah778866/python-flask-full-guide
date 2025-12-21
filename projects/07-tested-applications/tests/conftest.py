# Test Configuration
# Fixtures and setup for all tests

import pytest
from app import app, db

@pytest.fixture
def test_app():
    """Create test application"""
    # Use in-memory database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Create test client"""
    return test_app.test_client()

@pytest.fixture
def db_session(test_app):
    """Database session for tests"""
    with test_app.app_context():
        yield db

