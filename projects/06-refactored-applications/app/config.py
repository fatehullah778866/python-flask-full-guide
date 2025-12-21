# Configuration
# Separate configuration settings for different environments

import os

class Config:
    """Base configuration - common settings"""
    # Secret key for sessions (change in production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///blog.db'
    
    # Disable SQLAlchemy event system (not needed)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True  # Show errors in browser

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False  # Hide errors from users
    
    # In production, use environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

