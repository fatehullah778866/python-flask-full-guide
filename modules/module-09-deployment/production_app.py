# Production-Ready Flask Application Example
# This shows how to configure Flask for production

from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production Configuration
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security Settings
app.config['SESSION_COOKIE_SECURE'] = not app.config['DEBUG']  # HTTPS only in production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Database
db = SQLAlchemy(app)

# Logging Configuration (Production only)
if not app.config['DEBUG']:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f'404 error: {request.url}')
    return render_template_string('''
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <a href="/">Go Home</a>
    '''), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'500 error: {error}', exc_info=True)
    return render_template_string('''
    <h1>500 - Internal Server Error</h1>
    <p>Something went wrong. We're working on it!</p>
    <a href="/">Go Home</a>
    '''), 500

# Routes
@app.route('/')
def home():
    app.logger.info('Home page accessed')
    return render_template_string('''
    <h1>Production Flask App</h1>
    <p>This is a production-ready Flask application!</p>
    <ul>
        <li>Debug mode: {{ debug }}</li>
        <li>Environment: {{ env }}</li>
    </ul>
    ''', debug=app.config['DEBUG'], env=os.environ.get('FLASK_ENV', 'production'))

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return {'status': 'healthy', 'version': '1.0.0'}, 200

# Database Model Example
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Only run development server if DEBUG is True
    if app.config['DEBUG']:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("=" * 50)
        print("Production Mode!")
        print("Use a WSGI server to run this app:")
        print("  gunicorn -c gunicorn_config.py app:app")
        print("=" * 50)

