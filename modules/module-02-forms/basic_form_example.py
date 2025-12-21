# Basic Form Handling Example
# This shows how to handle HTML forms in Flask

from flask import Flask, request

app = Flask(__name__)

# Route to show the contact form
@app.route('/contact', methods=['GET'])
def show_form():
    return '''
    <html>
    <head><title>Contact Us</title></head>
    <body>
        <h1>Contact Us</h1>
        <form method="POST" action="/contact">
            <label>Your Name:</label><br>
            <input type="text" name="name" required><br><br>
            
            <label>Your Email:</label><br>
            <input type="email" name="email" required><br><br>
            
            <label>Your Message:</label><br>
            <textarea name="message" rows="5" required></textarea><br><br>
            
            <button type="submit">Send Message</button>
        </form>
    </body>
    </html>
    '''

# Route to handle form submission
@app.route('/contact', methods=['POST'])
def handle_form():
    # Get data from form using request.form
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Simple validation
    if not name or not email or not message:
        return 'All fields are required!'
    
    # In a real app, you'd save this to a database or send an email
    return f'''
    <html>
    <head><title>Thank You!</title></head>
    <body>
        <h1>Thank you, {name}!</h1>
        <p>We received your message and will reply to <strong>{email}</strong></p>
        <p>Your message: <em>{message}</em></p>
        <a href="/contact">Send another message</a>
    </body>
    </html>
    '''

# Alternative: Handle both GET and POST in one route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters')
        
        if errors:
            return f'Errors: {", ".join(errors)}'
        
        return f'Registration successful! Welcome, {name}!'
    
    else:
        # Show the form
        return '''
        <html>
        <head><title>Register</title></head>
        <body>
            <h2>Register</h2>
            <form method="POST">
                <label>Full Name:</label><br>
                <input type="text" name="name" required><br><br>
                
                <label>Email:</label><br>
                <input type="email" name="email" required><br><br>
                
                <label>Password:</label><br>
                <input type="password" name="password" required><br><br>
                
                <button type="submit">Register</button>
            </form>
        </body>
        </html>
        '''

if __name__ == '__main__':
    app.run(debug=True)

