# Notification System App
# This app allows users to receive and manage notifications!

# Step 1: Import Flask and Database Tools
# What is this? We're importing Flask and database tools
# Think of it like: "Get Flask tools and database tools"
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - flash = Function to show messages to users
# - session = Object for storing data between requests
# - jsonify = Function to return JSON responses (for API endpoints)
# - SQLAlchemy = Database toolkit
# - datetime = Module for working with dates and times
# - generate_password_hash = Function to hash passwords securely
# - check_password_hash = Function to verify password hashes
# - We'll use SQLAlchemy to store users and notifications!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///notifications.db' = SQLite database file
# - SQLite = Simple database that stores data in a file
# - notifications.db = The file where our data will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions and flash messages to work

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
class User(db.Model):
    """
    User Model
    This defines the structure of a user in the database
    """
    __tablename__ = 'users'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'users' = Name of the table in database
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    # - db.Column = Creates a column
    # - db.Integer = Data type (whole number)
    # - primary_key=True = This is the unique identifier
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Explanation:
    # - username = User's username
    # - db.String(80) = Text field, max 80 characters
    # - unique=True = No two users can have the same username
    # - nullable=False = This field is required
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Explanation:
    # - email = User's email address
    # - db.String(120) = Text field, max 120 characters
    # - unique=True = No two users can have the same email
    # - nullable=False = This field is required
    
    password_hash = db.Column(db.String(255), nullable=False)
    # Explanation:
    # - password_hash = Hashed password (not plain text!)
    # - db.String(255) = Text field for hash
    # - nullable=False = This field is required
    
    # Step 6: Define Relationship to Notifications
    # What is this? Creating relationship to notifications
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - notifications = Relationship to Notification model
    # - backref='user' = Creates 'user' attribute on Notification
    # - lazy=True = Loads notifications when accessed
    # - cascade = Deletes notifications when user is deleted
    # - This means: user.notifications gives all notifications for this user
    
    def __repr__(self):
        return f'<User {self.username}>'

# Step 7: Create Notification Model
# What is this? Defining what a notification looks like
class Notification(db.Model):
    """
    Notification Model
    This defines the structure of a notification in the database
    """
    __tablename__ = 'notifications'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'notifications' = Name of the table in database
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - user_id = ID of user who receives this notification
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Every notification must have a user
    # - This creates relationship: Notification → User
    
    title = db.Column(db.String(200), nullable=False)
    # Explanation:
    # - title = Notification title
    # - db.String(200) = Text field, max 200 characters
    # - nullable=False = This field is required
    # - Example: "New Message", "Task Assigned"
    
    message = db.Column(db.Text, nullable=False)
    # Explanation:
    # - message = Notification message/content
    # - db.Text = Text field (can hold long text)
    # - nullable=False = This field is required
    # - Example: "You have a new message from John"
    
    notification_type = db.Column(db.String(50), default='info', nullable=False)
    # Explanation:
    # - notification_type = Type of notification
    # - db.String(50) = Text field, max 50 characters
    # - default='info' = Default type is 'info'
    # - nullable=False = This field is required
    # - Possible values: 'info', 'success', 'warning', 'error'
    # - Used for styling and categorization
    
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    # Explanation:
    # - is_read = Whether notification has been read
    # - db.Boolean = True/False data type
    # - default=False = Default is unread
    # - nullable=False = This field is required
    # - False = Unread, True = Read
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When notification was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.title}>'

# Step 8: Create Database Tables
# What is this? Creating the actual database tables
with app.app_context():
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models and creates tables

# Step 9: Helper Functions
# What is this? Functions to help with authentication
def is_logged_in():
    """
    Check if user is logged in
    
    Returns:
    - True if logged in, False otherwise
    """
    return 'user_id' in session
    # Explanation:
    # - 'user_id' in session = Checks if user_id exists in session
    # - If exists, user is logged in

def get_current_user():
    """
    Get the current logged-in user
    
    Returns:
    - User object if logged in, None otherwise
    """
    if is_logged_in():
        # Explanation:
        # - if is_logged_in() = If user is logged in
        # - Only proceed if logged in
        
        return User.query.get(session['user_id'])
        # Explanation:
        # - User.query.get(session['user_id']) = Gets user by ID
        # - session['user_id'] = ID from session
        # - Returns User object
    
    return None
    # Explanation:
    # - return None = No user logged in

# Step 10: Helper Function to Create Notification
# What is this? Function to create notifications easily
def create_notification(user_id, title, message, notification_type='info'):
    """
    Create a new notification for a user
    
    Parameters:
    - user_id: ID of user to notify
    - title: Notification title
    - message: Notification message
    - notification_type: Type of notification (default: 'info')
    
    Returns:
    - Notification object
    """
    # Step 11: Create Notification Object
    # What is this? Creating a new notification
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )
    # Explanation:
    # - Notification() = Creates new Notification object
    # - user_id=user_id = Sets user who receives notification
    # - title=title = Sets notification title
    # - message=message = Sets notification message
    # - notification_type=notification_type = Sets notification type
    # - is_read = Automatically set to False (default)
    # - date_created = Automatically set (from model default)
    # - notification = New notification (not saved yet)
    
    # Step 12: Save to Database
    # What is this? Saving the notification
    db.session.add(notification)
    # Explanation:
    # - db.session.add(notification) = Adds notification to session
    # - Stages it for saving
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes to database
    # - Actually writes the notification to the database file
    
    return notification
    # Explanation:
    # - return notification = Returns the created notification
    # - This allows us to use it later if needed

# Step 13: Create Home Route (GET)
# What is this? The main dashboard page
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows the dashboard with notifications
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only show dashboard if logged in
        
        return redirect(url_for('login'))
        # Explanation:
        # - redirect = Sends user to login page
        # - Must be logged in to see dashboard
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 14: Get Unread Notifications Count
    # What is this? Counting unread notifications
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    # Explanation:
    # - Notification.query.filter_by(user_id=current_user.id, is_read=False) = Find unread notifications
    # - .count() = Counts how many match
    # - unread_count = Number of unread notifications
    # - Example: 5 unread notifications
    
    # Step 15: Get Recent Notifications
    # What is this? Getting recent notifications to display
    recent_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc()).limit(10).all()
    # Explanation:
    # - Notification.query.filter_by(user_id=current_user.id) = Find notifications for user
    # - .order_by(Notification.date_created.desc()) = Sort by date, newest first
    # - .limit(10) = Get only 10 most recent
    # - .all() = Get all matching notifications
    # - recent_notifications = List of 10 most recent notifications
    
    return render_template('index.html', unread_count=unread_count, recent_notifications=recent_notifications, current_user=current_user)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = Dashboard template
    # - unread_count=unread_count = Passes unread count to template
    # - recent_notifications=recent_notifications = Passes recent notifications to template
    # - current_user=current_user = Passes current user to template

# Step 16: Create Register Route (GET and POST)
# What is this? Page for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function handles user registration
    GET: Shows registration form
    POST: Processes registration
    """
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        # Explanation:
        # - Gets form data
        # - username, email, password = User input
        
        # Step 17: Validate Input
        if not username or not email or not password:
            # Explanation:
            # - if not username or not email or not password = If any field empty
            # - Only proceed if all fields filled
            
            flash('Please fill in all fields!', 'error')
            return render_template('register.html')
        
        # Step 18: Check if Username Exists
        if User.query.filter_by(username=username).first():
            # Explanation:
            # - User.query.filter_by(username=username) = Find user with this username
            # - .first() = Get first result (or None)
            # - If user exists, username is taken
            
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        # Step 19: Check if Email Exists
        if User.query.filter_by(email=email).first():
            # Explanation:
            # - User.query.filter_by(email=email) = Find user with this email
            # - .first() = Get first result (or None)
            # - If user exists, email is taken
            
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Step 20: Create New User
        password_hash = generate_password_hash(password)
        # Explanation:
        # - generate_password_hash(password) = Hashes password securely
        # - password_hash = Hashed password (not plain text!)
        
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        # Explanation:
        # - User() = Creates new User object
        # - Sets username, email, password_hash
        # - new_user = New user (not saved yet)
        
        db.session.add(new_user)
        db.session.commit()
        # Explanation:
        # - db.session.add(new_user) = Adds user to session
        # - db.session.commit() = Saves to database
        
        # Step 21: Create Welcome Notification
        # What is this? Creating a welcome notification for new user
        create_notification(
            user_id=new_user.id,
            title='Welcome!',
            message=f'Welcome to the notification system, {username}!',
            notification_type='success'
        )
        # Explanation:
        # - create_notification() = Our helper function
        # - user_id=new_user.id = Notify the new user
        # - title='Welcome!' = Welcome notification title
        # - message = Welcome message with username
        # - notification_type='success' = Success type (green)
        # - This creates a welcome notification when user registers
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        # Explanation:
        # - Shows success message
        # - Redirects to login page
    
    return render_template('register.html')
    # Explanation:
    # - render_template = Shows registration form
    # - 'register.html' = Registration template

# Step 22: Create Login Route (GET and POST)
# What is this? Page for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles user login
    GET: Shows login form
    POST: Processes login
    """
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        # Explanation:
        # - Gets form data
        # - username, password = User input
        
        # Step 23: Find User
        user = User.query.filter_by(username=username).first()
        # Explanation:
        # - User.query.filter_by(username=username) = Find user with this username
        # - .first() = Get first result (or None)
        # - user = User object (or None if not found)
        
        # Step 24: Verify Password
        if user and check_password_hash(user.password_hash, password):
            # Explanation:
            # - if user = If user was found
            # - check_password_hash(user.password_hash, password) = Verifies password
            # - Only proceed if user exists and password is correct
            
            session['user_id'] = user.id
            # Explanation:
            # - session['user_id'] = user.id = Stores user ID in session
            # - This logs the user in
            
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
            # Explanation:
            # - Shows success message
            # - Redirects to dashboard
        else:
            # Explanation:
            # - else = If user not found or password incorrect
            
            flash('Invalid username or password!', 'error')
            # Explanation:
            # - Shows error message
    
    return render_template('login.html')
    # Explanation:
    # - render_template = Shows login form
    # - 'login.html' = Login template

# Step 25: Create Logout Route
# What is this? Logs user out
@app.route('/logout')
def logout():
    """
    This function logs the user out
    """
    session.pop('user_id', None)
    # Explanation:
    # - session.pop('user_id', None) = Removes user_id from session
    # - This logs the user out
    
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))
    # Explanation:
    # - Shows success message
    # - Redirects to login page

# Step 26: Create Notifications Route (GET)
# What is this? Page showing all notifications
@app.route('/notifications')
def notifications():
    """
    This function shows all notifications for the current user
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can see notifications
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 27: Get All Notifications
    # What is this? Getting all notifications for the user
    all_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc()).all()
    # Explanation:
    # - Notification.query.filter_by(user_id=current_user.id) = Find notifications for user
    # - .order_by(Notification.date_created.desc()) = Sort by date, newest first
    # - .all() = Get all matching notifications
    # - all_notifications = List of all notifications for user
    
    # Step 28: Get Unread Count
    # What is this? Counting unread notifications
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    # Explanation:
    # - Notification.query.filter_by(user_id=current_user.id, is_read=False) = Find unread notifications
    # - .count() = Counts how many match
    # - unread_count = Number of unread notifications
    
    return render_template('notifications.html', notifications=all_notifications, unread_count=unread_count, current_user=current_user)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'notifications.html' = Notifications list template
    # - notifications=all_notifications = Passes notifications to template
    # - unread_count=unread_count = Passes unread count to template
    # - current_user=current_user = Passes current user to template

# Step 29: Create Mark as Read Route (POST)
# What is this? Marks a notification as read
@app.route('/notification/<int:notification_id>/read', methods=['POST'])
def mark_as_read(notification_id):
    """
    This function marks a notification as read
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can mark notifications as read
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    notification = Notification.query.get_or_404(notification_id)
    # Explanation:
    # - Notification.query.get_or_404(notification_id) = Gets notification by ID
    # - notification_id = ID from URL
    # - notification = Notification object (or 404 error if not found)
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 30: Check if Notification Belongs to User
    # What is this? Making sure user can only mark their own notifications as read
    if notification.user_id != current_user.id:
        # Explanation:
        # - if notification.user_id != current_user.id = If notification doesn't belong to user
        # - Users can only mark their own notifications as read
        
        flash('You cannot mark this notification as read!', 'error')
        return redirect(url_for('notifications'))
        # Explanation:
        # - Shows error message
        # - Redirects back to notifications
    
    # Step 31: Mark as Read
    # What is this? Updating the notification status
    notification.is_read = True
    # Explanation:
    # - notification.is_read = True = Sets notification as read
    # - Changes from False (unread) to True (read)
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes to database
    # - This saves the updated notification
    
    flash('Notification marked as read!', 'success')
    return redirect(url_for('notifications'))
    # Explanation:
    # - Shows success message
    # - Redirects back to notifications

# Step 32: Create Mark All as Read Route (POST)
# What is this? Marks all notifications as read
@app.route('/notifications/mark-all-read', methods=['POST'])
def mark_all_as_read():
    """
    This function marks all notifications as read
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can mark notifications as read
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 33: Get All Unread Notifications
    # What is this? Finding all unread notifications
    unread_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    # Explanation:
    # - Notification.query.filter_by(user_id=current_user.id, is_read=False) = Find unread notifications
    # - .all() = Get all matching notifications
    # - unread_notifications = List of all unread notifications
    
    # Step 34: Mark All as Read
    # What is this? Updating all unread notifications
    for notification in unread_notifications:
        # Explanation:
        # - for notification in unread_notifications = Loop through each unread notification
        # - notification = Current notification object
        
        notification.is_read = True
        # Explanation:
        # - notification.is_read = True = Sets notification as read
        # - Changes from False (unread) to True (read)
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes to database
    # - This saves all updated notifications
    
    flash('All notifications marked as read!', 'success')
    return redirect(url_for('notifications'))
    # Explanation:
    # - Shows success message
    # - Redirects back to notifications

# Step 35: Create Create Notification Route (POST)
# What is this? Creates a test notification
@app.route('/create-notification', methods=['POST'])
def create_test_notification():
    """
    This function creates a test notification
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can create notifications
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    title = request.form.get('title', 'Test Notification')
    message = request.form.get('message', 'This is a test notification')
    notification_type = request.form.get('type', 'info')
    # Explanation:
    # - Gets form data
    # - title, message, notification_type = Notification information
    # - Default values if not provided
    
    # Step 36: Create Notification
    # What is this? Creating the notification
    create_notification(
        user_id=current_user.id,
        title=title,
        message=message,
        notification_type=notification_type
    )
    # Explanation:
    # - create_notification() = Our helper function
    # - user_id=current_user.id = Notify current user
    # - title=title = Sets notification title
    # - message=message = Sets notification message
    # - notification_type=notification_type = Sets notification type
    
    flash('Notification created!', 'success')
    return redirect(url_for('index'))
    # Explanation:
    # - Shows success message
    # - Redirects back to dashboard

# Step 37: Create API Endpoint for Notification Count (GET)
# What is this? API endpoint to get unread notification count
@app.route('/api/notifications/count')
def get_notification_count():
    """
    This function returns the unread notification count as JSON
    Used for real-time updates via AJAX
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can get notification count
        
        return jsonify({'error': 'Not logged in'}), 401
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': 'Not logged in'} = Error message
        # - 401 = Unauthorized status code
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 38: Get Unread Count
    # What is this? Counting unread notifications
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    # Explanation:
    # - Notification.query.filter_by(user_id=current_user.id, is_read=False) = Find unread notifications
    # - .count() = Counts how many match
    # - unread_count = Number of unread notifications
    
    return jsonify({'count': unread_count})
    # Explanation:
    # - jsonify() = Returns JSON response
    # - {'count': unread_count} = JSON object with count
    # - This can be used by JavaScript to update the UI in real-time

# Step 39: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

