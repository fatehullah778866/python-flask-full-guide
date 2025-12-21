# Application Factory Pattern Example
# This shows how to create Flask apps using the factory pattern

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create extensions outside factory
db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'development':
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
        app.config['SECRET_KEY'] = 'dev-secret-key'
    elif config_name == 'production':
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    elif config_name == 'testing':
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes
    @app.route('/')
    def home():
        return f'Hello from {config_name} app!'
    
    @app.route('/config')
    def show_config():
        return f'Debug: {app.config["DEBUG"]}, Database: {app.config["SQLALCHEMY_DATABASE_URI"]}'
    
    return app

# Create app instance
app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)

