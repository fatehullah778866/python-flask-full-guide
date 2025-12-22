# Application Factory
# Creates the Flask application using factory pattern

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from app.config import Config

# Create database and CSRF objects (not initialized yet)
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_class=Config):
    """
    Application Factory Function
    Creates and configures the Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Register Blueprints
    # Main blueprint (home, about pages)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Auth blueprint (login, register, logout)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Posts blueprint (blog posts)
    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    # API blueprint (RESTful API)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Security Headers
    @app.after_request
    def set_security_headers(response):
        """Add security headers to all responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Make CSRF token available in templates
    @app.context_processor
    def inject_csrf_token():
        from flask import request
        return dict(csrf_token=lambda: csrf.generate_csrf())
    
    return app

