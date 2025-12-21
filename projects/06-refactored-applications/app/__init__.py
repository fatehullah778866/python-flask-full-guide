# Application Factory
# This creates the Flask application using the factory pattern

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Create database object (not initialized yet)
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Application Factory Function
    Creates and configures the Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize database with app
    db.init_app(app)
    
    # Register Blueprints
    # Main blueprint (home, about pages)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Posts blueprint (blog posts)
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    # Auth blueprint (login, register)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app

