# Pytest Configuration
# Sets up test fixtures for all tests

import pytest
from app import create_app, db
from app.config import DevelopmentConfig

@pytest.fixture
def app():
    """Create test application"""
    app = create_app(DevelopmentConfig)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Database session for tests"""
    with app.app_context():
        yield db

