# Error Handling Example
# This shows how to handle errors gracefully in Flask

from flask import Flask, render_template_string, jsonify, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== CUSTOM ERROR PAGES =====

@app.errorhandler(404)
def not_found(error):
    logger.warning(f'404 Error: {request.url}')
    return render_template_string('''
    <html>
    <head><title>404 - Not Found</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>Sorry, the page you're looking for doesn't exist.</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    '''), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 Error: {error}', exc_info=True)
    return render_template_string('''
    <html>
    <head><title>500 - Server Error</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>500 - Server Error</h1>
        <p>Something went wrong on our end. We're working on it!</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    '''), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template_string('''
    <html>
    <head><title>403 - Forbidden</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>403 - Forbidden</h1>
        <p>You don't have permission to access this page.</p>
        <a href="/">Go Home</a>
    </body>
    </html>
    '''), 403

# ===== ROUTES WITH ERROR HANDLING =====

@app.route('/')
def home():
    return '''
    <h1>Error Handling Demo</h1>
    <ul>
        <li><a href="/divide/10/2">Divide 10 by 2</a></li>
        <li><a href="/divide/10/0">Divide 10 by 0 (Error!)</a></li>
        <li><a href="/nonexistent">Non-existent page (404)</a></li>
    </ul>
    '''

@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    try:
        if b == 0:
            return "Cannot divide by zero!", 400
        result = a / b
        return f"Result: {a} / {b} = {result}"
    except Exception as e:
        logger.error(f'Division error: {e}')
        return "An error occurred during division", 500

# ===== API ERROR HANDLING =====

@app.route('/api/data')
def api_data():
    try:
        data = {"message": "Success", "data": [1, 2, 3]}
        return jsonify(data)
    except Exception as e:
        logger.error(f'API error: {e}')
        return jsonify({"error": "Internal server error"}), 500

# Handle 404 for API routes
@app.errorhandler(404)
def api_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource not found"}), 404
    return not_found(error)

if __name__ == '__main__':
    app.run(debug=True)

