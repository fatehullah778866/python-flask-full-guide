# Contact Form with Email App
# This app sends emails from a contact form!

# Step 1: Import Flask and Email Tools
# What is this? We're importing Flask and email sending tools
# Think of it like: "Get Flask tools and email tools"
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - flash = Function to show messages to users
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - Mail = Flask-Mail extension for sending emails
# - Message = Class for creating email messages
# - os = Module for accessing environment variables
# - We'll use Flask-Mail to send emails!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Flask-Mail
# What is this? Setting up email configuration
# Think of it like: "Tell Flask how to send emails"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'MAIL_SERVER' = Setting name for email server
# - 'smtp.gmail.com' = Gmail's SMTP server address
# - SMTP = Simple Mail Transfer Protocol (how emails are sent)
# - This tells Flask where to send emails from
# - You can use other email providers too!

app.config['MAIL_PORT'] = 587
# Explanation:
# - 'MAIL_PORT' = Port number for email server
# - 587 = Standard port for SMTP with TLS encryption
# - Port = Like a door number for the server
# - 587 = Secure port for sending emails

app.config['MAIL_USE_TLS'] = True
# Explanation:
# - 'MAIL_USE_TLS' = Use TLS encryption
# - True = Enable TLS (Transport Layer Security)
# - TLS = Encryption for secure email sending
# - This keeps your emails secure during transmission
# - Like sending a letter in a locked box!

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
# Explanation:
# - 'MAIL_USERNAME' = Your email address
# - os.environ.get() = Gets value from environment variable
# - 'MAIL_USERNAME' = Name of environment variable
# - 'your-email@gmail.com' = Default value if not found
# - This is your email address (the sender)
# - Better to use environment variable for security!

app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
# Explanation:
# - 'MAIL_PASSWORD' = Your email password or app password
# - os.environ.get() = Gets value from environment variable
# - 'MAIL_PASSWORD' = Name of environment variable
# - 'your-app-password' = Default value if not found
# - For Gmail, you need an "App Password" (not your regular password)
# - App Password = Special password for apps to access your email
# - Better to use environment variable for security!

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
# - Required for flash messages to work
# - In production, use a long, random, secret key

# Step 4: Initialize Flask-Mail
# What is this? Creating the mail object
# Think of it like: "Create an email manager"
mail = Mail(app)
# Explanation:
# - Mail(app) = Creates mail object with app configuration
# - mail = Our email manager
# - We'll use this to send emails
# - This connects Flask-Mail to our Flask app

# Step 5: Create Home Route (GET)
# What is this? The main page that shows the contact form
# Think of it like: "When someone visits the home page, show the form"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows the contact form
    """
    # Step 6: Render Template
    # What is this? Showing the HTML page with the form
    return render_template('index.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - Flask looks for templates in the 'templates' folder
    # - This will show a contact form

# Step 7: Create Contact Route (POST)
# What is this? Handles form submission to send email
# Think of it like: "When user submits form, send email"
@app.route('/contact', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/contact' = The URL for sending contact emails
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/contact', Flask will run the function below

def contact():
    """
    This function runs when the contact form is submitted
    It sends an email with the form data
    """
    # Step 8: Get Form Data
    # What is this? Getting the data from the form
    name = request.form.get('name', '').strip()
    # Explanation:
    # - request.form.get('name', '') = Gets value of input named 'name'
    # - If 'name' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - name = Variable to hold the sender's name
    
    email = request.form.get('email', '').strip()
    # Explanation:
    # - request.form.get('email', '') = Gets value of input named 'email'
    # - .strip() = Removes whitespace
    # - email = Variable to hold the sender's email address
    
    subject = request.form.get('subject', '').strip()
    # Explanation:
    # - request.form.get('subject', '') = Gets value of input named 'subject'
    # - .strip() = Removes whitespace
    # - subject = Variable to hold the email subject
    
    message = request.form.get('message', '').strip()
    # Explanation:
    # - request.form.get('message', '') = Gets value of textarea named 'message'
    # - .strip() = Removes whitespace
    # - message = Variable to hold the email message content
    
    # Step 9: Validate Form Data
    # What is this? Checking if user entered valid data
    if not name or not email or not subject or not message:
        # Explanation:
        # - if not name or not email or not subject or not message = If any field is empty
        # - Empty strings are "falsy" in Python
        # - Only proceed if all fields are filled
        
        flash('Please fill in all fields!', 'error')
        # Explanation:
        # - flash() = Function to show temporary message
        # - 'Please fill in all fields!' = Error message
        # - 'error' = Message category (for styling)
        
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route (home page)
        # - User is sent back to form to try again
    
    # Step 10: Create Email Message
    # What is this? Building the email to send
    # Think of it like: "Create an email letter"
    msg = Message(
        subject=f'Contact Form: {subject}',
        # Explanation:
        # - subject = Email subject line
        # - f'Contact Form: {subject}' = Formatted string
        # - {subject} = User's subject from form
        # - Example: "Contact Form: Question about product"
        
        sender=app.config['MAIL_USERNAME'],
        # Explanation:
        # - sender = Email address of sender
        # - app.config['MAIL_USERNAME'] = Your email address (from config)
        # - This is who the email is from
        
        recipients=[app.config['MAIL_USERNAME']],
        # Explanation:
        # - recipients = List of email addresses to send to
        # - [app.config['MAIL_USERNAME']] = List with your email address
        # - You'll receive the contact form emails
        # - Can add multiple recipients: ['email1@example.com', 'email2@example.com']
        
        body=f'''
        You have received a new contact form submission:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        '''
        # Explanation:
        # - body = Email body (content)
        # - f'''...''' = Multi-line formatted string
        # - {name}, {email}, {subject}, {message} = Form data inserted into email
        # - This creates a nicely formatted email with all the form data
    )
    # Explanation:
    # - Message() = Creates email message object
    # - msg = The email message (not sent yet)
    
    # Step 11: Send Email
    # What is this? Actually sending the email
    # Think of it like: "Send the email letter"
    try:
        # Explanation:
        # - try = Attempt to do something
        # - If it fails, catch the error (except block)
        # - This handles email sending errors
        
        mail.send(msg)
        # Explanation:
        # - mail.send(msg) = Sends the email message
        # - mail = Our Flask-Mail object
        # - .send() = Method to send email
        # - msg = The email message we created
        # - This actually sends the email through the SMTP server!
        
        # Step 12: Show Success Message
        # What is this? Telling user the email was sent
        flash('Thank you! Your message has been sent successfully.', 'success')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Thank you! Your message has been sent successfully.' = Success message
        # - 'success' = Message category
        
    except Exception as e:
        # Explanation:
        # - except = If an error occurs
        # - Exception = Catches any error
        # - as e = Stores error in variable 'e'
        # - This catches email sending errors (network issues, wrong credentials, etc.)
        
        # Step 13: Show Error Message
        # What is this? Telling user there was an error
        flash(f'Error sending email: {str(e)}. Please try again later.', 'error')
        # Explanation:
        # - flash() = Shows temporary message
        # - f'...' = f-string with error message
        # - {str(e)} = Converts error to string and inserts it
        # - 'error' = Message category
        # - User sees what went wrong
    
    # Step 14: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is sent back to contact form
    # - They'll see the success or error message

# Step 15: Run the Application
# What is this? This starts the web server
# Think of it like: "Turn on the website so people can visit it"
if __name__ == '__main__':
    # Explanation:
    # - if __name__ == '__main__' = Only run this if we run the file directly
    # - This prevents it from running if we import this file elsewhere
    
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)
    # - When you run this, you'll see: "Running on http://127.0.0.1:5000"
    # - You can then visit that address in your browser!

