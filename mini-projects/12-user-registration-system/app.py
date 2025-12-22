# User Registration System
# This app allows users to register and login!

# Step 1: Import Flask and Security Tools
# What is this? We're importing Flask and password security tools
# Think of it like: "Get Flask tools and password security tools"
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - flash = Function to show messages to users
# - session = Object for storing data between requests
# - SQLAlchemy = Database toolkit
# - generate_password_hash = Function to hash passwords (make them secure)
# - check_password_hash = Function to verify passwords
# - datetime = Module for working with dates and times
# - We'll use password hashing to keep passwords secure!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Database
# What is this? Setting up where to store our database
# Think of it like: "Tell Flask where to save our data"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///users.db' = SQLite database file named 'users.db'
# - SQLite = Simple database that stores data in a file
# - users.db = The file where our user data will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
# - Required for sessions and flash messages to work
# - In production, use a long, random, secret key

# Step 4: Initialize Database
# What is this? Creating the database object
# Think of it like: "Create a database manager"
db = SQLAlchemy(app)
# Explanation:
# - SQLAlchemy(app) = Creates database object
# - db = Our database manager
# - We'll use this to create tables and save data

# Step 5: Create User Model
# What is this? Defining what a user looks like
# Think of it like: "Creating a template for users"
class User(db.Model):
    """
    User Model
    This defines the structure of a user in the database
    """
    # Step 6: Define Table Name
    # What is this? Name of the database table
    __tablename__ = 'users'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'users' = Name of the table in database
    # - Table = Like a spreadsheet with rows and columns
    # - This table will store all our users
    
    # Step 7: Define Columns (Fields)
    # What is this? Defining what data each user will have
    # Think of it like: "What information does each user need?"
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Column name (unique identifier)
    # - db.Column = Creates a column in the database table
    # - db.Integer = Data type (whole number)
    # - primary_key=True = This is the unique identifier
    # - Each user gets a unique ID (1, 2, 3, ...)
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Explanation:
    # - username = Column name (user's username)
    # - db.String(80) = Text field, max 80 characters
    # - unique=True = No two users can have the same username
    # - nullable=False = This field is required (can't be empty)
    # - Every user must have a unique username
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Explanation:
    # - email = Column name (user's email)
    # - db.String(120) = Text field, max 120 characters
    # - unique=True = No two users can have the same email
    # - nullable=False = This field is required
    # - Every user must have a unique email
    
    password_hash = db.Column(db.String(255), nullable=False)
    # Explanation:
    # - password_hash = Column name (hashed password)
    # - db.String(255) = Text field, max 255 characters
    # - nullable=False = This field is required
    # - We store the HASHED password, not the actual password!
    # - Hash = Encrypted version of password (one-way encryption)
    # - We can't get the original password from the hash
    # - This keeps passwords secure!
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = Column name (when user registered)
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    # - When we create a user, it automatically gets the current date/time
    
    # Step 8: Define String Representation
    # What is this? How to display the user when printed
    def __repr__(self):
        """
        String representation of the User object
        This is what you see when you print a user
        """
        return f'<User {self.id}: {self.username}>'
        # Explanation:
        # - __repr__ = Special method for string representation
        # - f'...' = f-string (formatted string)
        # - {self.id} = User's ID number
        # - {self.username} = User's username
        # - Example: "<User 1: john_doe>"

# Step 9: Create Database Tables
# What is this? Creating the actual database tables
# Think of it like: "Build the database structure"
with app.app_context():
    # Explanation:
    # - with app.app_context() = Flask application context
    # - Needed to access database within Flask app
    
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models (like User) and creates tables
    # - If tables already exist, does nothing
    # - This builds the database structure

# Step 10: Create Home Route (GET)
# What is this? The main page
# Think of it like: "When someone visits the home page, show welcome"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page

def index():
    """
    This function runs when someone visits the home page
    It shows a welcome page
    """
    # Step 11: Check if User is Logged In
    # What is this? Checking if user is logged in
    logged_in = 'user_id' in session
    # Explanation:
    # - 'user_id' in session = Checks if 'user_id' exists in session
    # - session = Dictionary-like object for storing data between requests
    # - If user logged in, 'user_id' will be in session
    # - logged_in = True if logged in, False if not
    
    username = None
    # Explanation:
    # - username = Variable to hold username
    # - Starts as None (no username)
    
    if logged_in:
        # Explanation:
        # - if logged_in = If user is logged in
        # - Only get username if logged in
        
        user = User.query.get(session['user_id'])
        # Explanation:
        # - User.query.get(session['user_id']) = Gets user by ID from database
        # - session['user_id'] = User's ID stored in session
        # - user = User object from database
        
        if user:
            # Explanation:
            # - if user = If user exists in database
            # - Safety check (user might have been deleted)
            
            username = user.username
            # Explanation:
            # - username = User's username
            # - We'll display this in the template
    
    # Step 12: Render Template
    # What is this? Showing the HTML page
    return render_template('index.html', logged_in=logged_in, username=username)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - logged_in=logged_in = Passes login status to template
    # - username=username = Passes username to template

# Step 13: Create Register Route (GET and POST)
# What is this? Page to register a new user
# Think of it like: "When someone visits /register, show registration form"
@app.route('/register', methods=['GET', 'POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/register' = The URL for registration
# - methods=['GET', 'POST'] = Accepts both GET (view form) and POST (submit form)

def register():
    """
    This function runs when someone visits /register
    GET: Shows registration form
    POST: Creates new user account
    """
    # Step 14: Handle Form Submission (POST)
    # What is this? Processing the form when user submits it
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        # - POST = Form submission
        
        # Step 15: Get Form Data
        # What is this? Getting the data from the form
        username = request.form.get('username', '').strip()
        # Explanation:
        # - request.form.get('username', '') = Gets value of input named 'username'
        # - .strip() = Removes whitespace
        # - username = Variable to hold the username
        
        email = request.form.get('email', '').strip()
        # Explanation:
        # - request.form.get('email', '') = Gets value of input named 'email'
        # - .strip() = Removes whitespace
        # - email = Variable to hold the email
        
        password = request.form.get('password', '')
        # Explanation:
        # - request.form.get('password', '') = Gets value of input named 'password'
        # - password = Variable to hold the password
        # - We don't strip passwords (spaces might be intentional)
        
        confirm_password = request.form.get('confirm_password', '')
        # Explanation:
        # - request.form.get('confirm_password', '') = Gets value of input named 'confirm_password'
        # - confirm_password = Variable to hold the password confirmation
        # - User types password twice to make sure they typed it correctly
        
        # Step 16: Validate Form Data
        # What is this? Checking if user entered valid data
        if not username or not email or not password:
            # Explanation:
            # - if not username or not email or not password = If any field is empty
            # - Empty strings are "falsy" in Python
            # - Only proceed if all fields are filled
            
            flash('Please fill in all fields!', 'error')
            # Explanation:
            # - flash() = Function to show temporary message
            # - 'Please fill in all fields!' = Error message
            # - 'error' = Message category
            
            return render_template('register.html')
            # Explanation:
            # - Shows form again with error message
        
        if password != confirm_password:
            # Explanation:
            # - if password != confirm_password = If passwords don't match
            # - != = Not equal operator
            # - User must type password correctly twice
            
            flash('Passwords do not match!', 'error')
            # Explanation:
            # - Shows error message
            
            return render_template('register.html')
            # Explanation:
            # - Shows form again
        
        if len(password) < 6:
            # Explanation:
            # - if len(password) < 6 = If password is less than 6 characters
            # - len() = Length of string
            # - We require minimum 6 characters for security
            
            flash('Password must be at least 6 characters long!', 'error')
            # Explanation:
            # - Shows error message
            
            return render_template('register.html')
            # Explanation:
            # - Shows form again
        
        # Step 17: Check if Username or Email Already Exists
        # What is this? Making sure username and email are unique
        existing_user = User.query.filter_by(username=username).first()
        # Explanation:
        # - User.query = Query object for User model
        # - .filter_by(username=username) = Filter users where username matches
        # - .first() = Get first result (or None if not found)
        # - existing_user = User object if found, None if not found
        
        if existing_user:
            # Explanation:
            # - if existing_user = If user with this username exists
            # - Username must be unique!
            
            flash('Username already exists! Please choose a different one.', 'error')
            # Explanation:
            # - Shows error message
            
            return render_template('register.html')
            # Explanation:
            # - Shows form again
        
        existing_email = User.query.filter_by(email=email).first()
        # Explanation:
        # - User.query.filter_by(email=email) = Filter users where email matches
        # - .first() = Get first result (or None if not found)
        # - existing_email = User object if found, None if not found
        
        if existing_email:
            # Explanation:
            # - if existing_email = If user with this email exists
            # - Email must be unique!
            
            flash('Email already exists! Please use a different email.', 'error')
            # Explanation:
            # - Shows error message
            
            return render_template('register.html')
            # Explanation:
            # - Shows form again
        
        # Step 18: Hash Password
        # What is this? Converting password to secure hash
        password_hash = generate_password_hash(password)
        # Explanation:
        # - generate_password_hash() = Function to hash password
        # - password = The original password
        # - password_hash = Hashed version of password
        # - Hash = One-way encryption (can't get original password back)
        # - This keeps passwords secure!
        # - Example: "mypassword123" → "$2b$12$..." (long hash string)
        
        # Step 19: Create New User Object
        # What is this? Creating a new user
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        # Explanation:
        # - User() = Creates new User object
        # - username=username = Sets the username
        # - email=email = Sets the email
        # - password_hash=password_hash = Sets the hashed password (NOT the original!)
        # - date_created = Automatically set (from model default)
        # - new_user = The new User object (not saved yet)
        
        # Step 20: Save to Database
        # What is this? Adding the user to the database
        db.session.add(new_user)
        # Explanation:
        # - db.session = Database session
        # - .add(new_user) = Adds user to session (stages it for saving)
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves changes to database
        # - Actually writes the user to the database file
        # - This is when the user is permanently saved
        
        # Step 21: Show Success Message
        # What is this? Telling user registration was successful
        flash('Registration successful! Please login.', 'success')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Registration successful! Please login.' = Success message
        # - 'success' = Message category
        
        # Step 22: Redirect to Login Page
        # What is this? Sending user to login page
        return redirect(url_for('login'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('login') = Generates URL for 'login' route
        # - User can now login with their new account
    
    # Step 23: Handle Form Display (GET)
    # What is this? Showing the form when user first visits
    return render_template('register.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'register.html' = The template file with the registration form
    # - This shows the form to register a new user

# Step 24: Create Login Route (GET and POST)
# What is this? Page to login
# Think of it like: "When someone visits /login, show login form"
@app.route('/login', methods=['GET', 'POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/login' = The URL for login
# - methods=['GET', 'POST'] = Accepts both GET (view form) and POST (submit form)

def login():
    """
    This function runs when someone visits /login
    GET: Shows login form
    POST: Authenticates user and logs them in
    """
    # Step 25: Handle Form Submission (POST)
    # What is this? Processing the form when user submits it
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        
        # Step 26: Get Form Data
        # What is this? Getting the data from the form
        username = request.form.get('username', '').strip()
        # Explanation:
        # - request.form.get('username', '') = Gets value of input named 'username'
        # - .strip() = Removes whitespace
        # - username = Variable to hold the username
        
        password = request.form.get('password', '')
        # Explanation:
        # - request.form.get('password', '') = Gets value of input named 'password'
        # - password = Variable to hold the password
        
        # Step 27: Validate Form Data
        # What is this? Checking if user entered data
        if not username or not password:
            # Explanation:
            # - if not username or not password = If any field is empty
            # - Only proceed if both fields are filled
            
            flash('Please fill in both username and password!', 'error')
            # Explanation:
            # - Shows error message
            
            return render_template('login.html')
            # Explanation:
            # - Shows form again
        
        # Step 28: Find User in Database
        # What is this? Looking for user with this username
        user = User.query.filter_by(username=username).first()
        # Explanation:
        # - User.query = Query object for User model
        # - .filter_by(username=username) = Filter users where username matches
        # - .first() = Get first result (or None if not found)
        # - user = User object if found, None if not found
        
        # Step 29: Verify Password
        # What is this? Checking if password is correct
        if user and check_password_hash(user.password_hash, password):
            # Explanation:
            # - if user = If user exists in database
            # - check_password_hash() = Function to verify password
            # - user.password_hash = Hashed password from database
            # - password = Password user entered
            # - Returns True if password matches, False if not
            # - Only proceed if user exists AND password is correct
            
            # Step 30: Create Session
            # What is this? Logging the user in
            session['user_id'] = user.id
            # Explanation:
            # - session['user_id'] = Stores user ID in session
            # - user.id = User's ID from database
            # - Session = Data stored between requests
            # - This is how we know user is logged in
            # - Session persists until user logs out or browser closes
            
            # Step 31: Show Success Message
            # What is this? Telling user login was successful
            flash(f'Welcome back, {user.username}!', 'success')
            # Explanation:
            # - flash() = Shows temporary message
            # - f'Welcome back, {user.username}!' = Personalized success message
            # - {user.username} = User's username
            # - 'success' = Message category
            
            # Step 32: Redirect to Home Page
            # What is this? Sending user to home page
            return redirect(url_for('index'))
            # Explanation:
            # - redirect = Sends user to another page
            # - url_for('index') = Generates URL for 'index' route (home page)
            # - User is now logged in!
        else:
            # Explanation:
            # - else = If user doesn't exist OR password is wrong
            
            flash('Invalid username or password!', 'error')
            # Explanation:
            # - Shows error message
            # - We don't say which one is wrong (security best practice)
            
            return render_template('login.html')
            # Explanation:
            # - Shows form again
    
    # Step 33: Handle Form Display (GET)
    # What is this? Showing the form when user first visits
    return render_template('login.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'login.html' = The template file with the login form
    # - This shows the form to login

# Step 34: Create Logout Route
# What is this? Route to logout
# Think of it like: "When someone visits /logout, log them out"
@app.route('/logout')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/logout' = The URL for logout

def logout():
    """
    This function runs when someone visits /logout
    It logs the user out by clearing the session
    """
    # Step 35: Clear Session
    # What is this? Removing user data from session
    session.pop('user_id', None)
    # Explanation:
    # - session.pop('user_id', None) = Removes 'user_id' from session
    # - .pop() = Removes item from dictionary
    # - 'user_id' = Key to remove
    # - None = Default value if key doesn't exist
    # - This logs the user out
    
    # Step 36: Show Success Message
    # What is this? Telling user logout was successful
    flash('You have been logged out successfully!', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - 'You have been logged out successfully!' = Success message
    # - 'success' = Message category
    
    # Step 37: Redirect to Home Page
    # What is this? Sending user to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is now logged out!

# Step 38: Run the Application
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

