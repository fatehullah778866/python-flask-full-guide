# Production-Ready Flask Application
# Ready for deployment to Heroku, Railway, Render, etc.

from flask import Flask, render_template, jsonify
import os

# Create Flask app
app = Flask(__name__)

# Production Configuration
# Use environment variables for secrets
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

# Security settings (for production)
if not app.config['DEBUG']:
    app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Routes

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running!',
        'environment': 'production' if not app.config['DEBUG'] else 'development'
    }), 200

@app.route('/api/info')
def info():
    """Application information"""
    return jsonify({
        'name': 'Deployed Flask App',
        'version': '1.0.0',
        'status': 'online'
    }), 200

# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message='Internal server error'), 500

# Run the application
if __name__ == '__main__':
    # Get port from environment (platforms set this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run app
    # In production, use: gunicorn app:app
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])

