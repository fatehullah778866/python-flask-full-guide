# Contact Form with File Upload
# This Flask app handles contact forms and file uploads

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # For flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Where uploaded files are saved
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size: 16MB

# Allowed file extensions (for security)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_message(name, email, message, filename=None):
    """Save message to JSON file"""
    # Create message data
    message_data = {
        'id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'name': name,
        'email': email,
        'message': message,
        'filename': filename,
        'timestamp': datetime.now().isoformat()
    }
    
    # Load existing messages
    messages_file = 'data/messages.json'
    if os.path.exists(messages_file):
        with open(messages_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    else:
        messages = []
    
    # Add new message
    messages.append(message_data)
    
    # Save back to file
    with open(messages_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

# Home route - redirects to contact form
@app.route('/')
def home():
    return redirect(url_for('contact'))

# Contact form route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # If form was submitted (POST request)
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        file = request.files.get('file')  # Get uploaded file
        
        # Validate form data
        errors = []
        
        # Check if name is provided
        if not name:
            errors.append('Name is required')
        
        # Check if email is provided and valid
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Invalid email address')
        
        # Check if message is provided
        if not message:
            errors.append('Message is required')
        
        # Handle file upload
        filename = None
        if file and file.filename:
            # Check if file type is allowed
            if allowed_file(file.filename):
                # Make filename safe (remove dangerous characters)
                filename = secure_filename(file.filename)
                # Add timestamp to prevent overwriting
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                # Save file
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                errors.append('File type not allowed. Allowed types: txt, pdf, png, jpg, jpeg, gif, doc, docx')
        
        # If there are errors, show them and return form
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html')
        
        # Save the message
        save_message(name, email, message, filename)
        
        # Show success message
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    # GET request - show the form
    return render_template('contact.html')

# Messages page - view all received messages
@app.route('/messages')
def messages():
    """Display all received messages"""
    messages_file = 'data/messages.json'
    
    # Load messages from file
    if os.path.exists(messages_file):
        with open(messages_file, 'r', encoding='utf-8') as f:
            messages_list = json.load(f)
        # Sort by timestamp (newest first)
        messages_list.sort(key=lambda x: x['timestamp'], reverse=True)
    else:
        messages_list = []
    
    return render_template('messages.html', messages=messages_list)

# Run the app
if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Start the Flask development server
    app.run(debug=True)

