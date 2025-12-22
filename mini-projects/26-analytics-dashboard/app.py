# Analytics Dashboard App
# This app tracks user actions and displays analytics!

# Step 1: Import Flask and Database Tools
# What is this? We're importing Flask and database tools
# Think of it like: "Get Flask tools and database tools"
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from collections import Counter
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
# - timedelta = For date calculations (adding/subtracting days)
# - generate_password_hash = Function to hash passwords securely
# - check_password_hash = Function to verify password hashes
# - Counter = For counting occurrences (from collections module)
# - We'll use SQLAlchemy to store users and events!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///analytics.db' = SQLite database file
# - SQLite = Simple database that stores data in a file
# - analytics.db = The file where our data will be stored

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
    
    # Step 6: Define Relationship to Events
    # What is this? Creating relationship to events
    events = db.relationship('Event', backref='user', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - events = Relationship to Event model
    # - backref='user' = Creates 'user' attribute on Event
    # - lazy=True = Loads events when accessed
    # - cascade = Deletes events when user is deleted
    # - This means: user.events gives all events for this user
    
    def __repr__(self):
        return f'<User {self.username}>'

# Step 7: Create Event Model
# What is this? Defining what an event (user action) looks like
class Event(db.Model):
    """
    Event Model
    This defines the structure of an event in the database
    Events track user actions for analytics
    """
    __tablename__ = 'events'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'events' = Name of the table in database
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - user_id = ID of user who performed the action
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Every event must have a user
    # - This creates relationship: Event → User
    
    event_type = db.Column(db.String(100), nullable=False)
    # Explanation:
    # - event_type = Type of event/action
    # - db.String(100) = Text field, max 100 characters
    # - nullable=False = This field is required
    # - Example: 'page_view', 'button_click', 'form_submit', 'download'
    # - Used to categorize different types of actions
    
    event_data = db.Column(db.Text)
    # Explanation:
    # - event_data = Additional data about the event (JSON string)
    # - db.Text = Text field (can hold long text)
    # - nullable=True = This field is optional
    # - Example: '{"page": "/dashboard", "duration": 120}'
    # - Stores extra information about the event
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When event occurred
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    def __repr__(self):
        return f'<Event {self.id}: {self.event_type}>'

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

# Step 10: Helper Function to Track Event
# What is this? Function to record user actions
def track_event(user_id, event_type, event_data=None):
    """
    Track a user event/action
    
    Parameters:
    - user_id: ID of user who performed the action
    - event_type: Type of event (e.g., 'page_view', 'button_click')
    - event_data: Additional data about the event (optional)
    
    Returns:
    - Event object
    """
    # Step 11: Create Event Object
    # What is this? Creating a new event
    event = Event(
        user_id=user_id,
        event_type=event_type,
        event_data=event_data
    )
    # Explanation:
    # - Event() = Creates new Event object
    # - user_id=user_id = Sets user who performed action
    # - event_type=event_type = Sets event type
    # - event_data=event_data = Sets additional data (or None)
    # - date_created = Automatically set (from model default)
    # - event = New event (not saved yet)
    
    # Step 12: Save to Database
    # What is this? Saving the event
    db.session.add(event)
    # Explanation:
    # - db.session.add(event) = Adds event to session
    # - Stages it for saving
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes to database
    # - Actually writes the event to the database file
    
    return event
    # Explanation:
    # - return event = Returns the created event
    # - This allows us to use it later if needed

# Step 13: Create Home Route (GET)
# What is this? The main dashboard page
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows the analytics dashboard
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
    
    # Step 14: Track Page View Event
    # What is this? Recording that user viewed the dashboard
    track_event(current_user.id, 'page_view', '{"page": "/dashboard"}')
    # Explanation:
    # - track_event() = Our helper function
    # - current_user.id = User who viewed the page
    # - 'page_view' = Type of event
    # - '{"page": "/dashboard"}' = Additional data (JSON string)
    # - This records that user visited the dashboard
    
    # Step 15: Get Date Range from Query Parameters
    # What is this? Getting date filter from URL
    days = int(request.args.get('days', 7))
    # Explanation:
    # - request.args.get('days', 7) = Gets 'days' parameter from URL
    # - request.args = Dictionary of URL query parameters
    # - 'days' = Parameter name
    # - 7 = Default value if 'days' doesn't exist (last 7 days)
    # - int() = Converts to integer
    # - days = Number of days to look back
    # - Example: /?days=30 → days = 30 (last 30 days)
    
    # Step 16: Calculate Date Range
    # What is this? Figuring out the start date
    end_date = datetime.utcnow()
    # Explanation:
    # - datetime.utcnow() = Current date and time
    # - end_date = Today (end of date range)
    
    start_date = end_date - timedelta(days=days)
    # Explanation:
    # - timedelta(days=days) = Time difference of 'days' days
    # - end_date - timedelta(days=days) = Start date
    # - start_date = Beginning of date range
    # - Example: If days=7, start_date = 7 days ago
    
    # Step 17: Get Events in Date Range
    # What is this? Finding events within the date range
    events = Event.query.filter(
        Event.date_created >= start_date,
        Event.date_created <= end_date
    ).order_by(Event.date_created.desc()).all()
    # Explanation:
    # - Event.query = Query object for Event model
    # - .filter(Event.date_created >= start_date, Event.date_created <= end_date) = Filter by date
    # - Gets events between start_date and end_date
    # - .order_by(Event.date_created.desc()) = Sort by date, newest first
    # - .all() = Get all matching events
    # - events = List of Event objects in date range
    
    # Step 18: Calculate Statistics
    # What is this? Computing analytics statistics
    
    # Total Events
    total_events = len(events)
    # Explanation:
    # - len(events) = Counts number of events
    # - total_events = Total number of events in date range
    
    # Events by Type
    event_types = [event.event_type for event in events]
    # Explanation:
    # - for event in events = Loop through events
    # - event.event_type = Type of each event
    # - List comprehension = Creates list of event types
    # - event_types = List of all event types
    # - Example: ['page_view', 'button_click', 'page_view', ...]
    
    events_by_type = dict(Counter(event_types))
    # Explanation:
    # - Counter(event_types) = Counts occurrences of each type
    # - dict() = Converts Counter to dictionary
    # - events_by_type = Dictionary with counts
    # - Example: {'page_view': 10, 'button_click': 5, 'form_submit': 3}
    
    # Events by Day
    events_by_day = {}
    # Explanation:
    # - events_by_day = Empty dictionary to store daily counts
    # - {} = Empty dictionary
    # - Format: {'2024-01-01': 5, '2024-01-02': 8, ...}
    
    for event in events:
        # Explanation:
        # - for event in events = Loop through events
        # - event = Current event object
        
        day_key = event.date_created.strftime('%Y-%m-%d')
        # Explanation:
        # - event.date_created.strftime('%Y-%m-%d') = Formats date as YYYY-MM-DD
        # - strftime() = String format time (converts date to string)
        # - '%Y-%m-%d' = Format: Year-Month-Day
        # - day_key = Date string (e.g., '2024-01-01')
        
        events_by_day[day_key] = events_by_day.get(day_key, 0) + 1
        # Explanation:
        # - events_by_day.get(day_key, 0) = Gets count for this day (or 0 if not exists)
        # - + 1 = Increments count
        # - events_by_day[day_key] = Sets count for this day
        # - This counts events per day
        # - Example: events_by_day['2024-01-01'] = 5
    
    # Step 19: Get Top Event Types
    # What is this? Finding most common event types
    top_event_types = sorted(events_by_type.items(), key=lambda x: x[1], reverse=True)[:5]
    # Explanation:
    # - events_by_type.items() = Gets key-value pairs from dictionary
    # - sorted(..., key=lambda x: x[1], reverse=True) = Sorts by value (count), descending
    # - lambda x: x[1] = Gets the value (count) from each pair
    # - reverse=True = Descending order (highest first)
    # - [:5] = Gets first 5 items
    # - top_event_types = List of top 5 event types with counts
    # - Example: [('page_view', 10), ('button_click', 5), ...]
    
    return render_template('index.html', 
                         total_events=total_events,
                         events_by_type=events_by_type,
                         events_by_day=events_by_day,
                         top_event_types=top_event_types,
                         days=days,
                         current_user=current_user)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = Dashboard template
    # - total_events=total_events = Passes total count to template
    # - events_by_type=events_by_type = Passes event type counts to template
    # - events_by_day=events_by_day = Passes daily counts to template
    # - top_event_types=top_event_types = Passes top event types to template
    # - days=days = Passes date range to template
    # - current_user=current_user = Passes current user to template

# Step 20: Create Track Event Route (POST)
# What is this? API endpoint to track events
@app.route('/api/track-event', methods=['POST'])
def track_event_api():
    """
    This function handles tracking events via API
    Used by JavaScript to track user actions
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can track events
        
        return jsonify({'error': 'Not logged in'}), 401
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': 'Not logged in'} = Error message
        # - 401 = Unauthorized status code
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 21: Get Event Data from Request
    # What is this? Getting event information from request
    data = request.get_json()
    # Explanation:
    # - request.get_json() = Gets JSON data from request body
    # - data = Dictionary with event information
    # - Example: {'event_type': 'button_click', 'event_data': '{"button": "submit"}'}
    
    event_type = data.get('event_type', 'unknown')
    # Explanation:
    # - data.get('event_type', 'unknown') = Gets event type from data
    # - 'unknown' = Default value if 'event_type' doesn't exist
    # - event_type = Type of event
    
    event_data = data.get('event_data')
    # Explanation:
    # - data.get('event_data') = Gets additional data from data
    # - event_data = Additional event data (or None)
    
    # Step 22: Track the Event
    # What is this? Recording the event
    track_event(current_user.id, event_type, event_data)
    # Explanation:
    # - track_event() = Our helper function
    # - current_user.id = User who performed action
    # - event_type=event_type = Type of event
    # - event_data=event_data = Additional data
    
    return jsonify({'success': True, 'message': 'Event tracked'})
    # Explanation:
    # - jsonify() = Returns JSON response
    # - {'success': True, 'message': 'Event tracked'} = Success message
    # - This confirms the event was tracked

# Step 23: Create Register Route (GET and POST)
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
        
        # Step 24: Validate Input
        if not username or not email or not password:
            # Explanation:
            # - if not username or not email or not password = If any field empty
            # - Only proceed if all fields filled
            
            flash('Please fill in all fields!', 'error')
            return render_template('register.html')
        
        # Step 25: Check if Username Exists
        if User.query.filter_by(username=username).first():
            # Explanation:
            # - User.query.filter_by(username=username) = Find user with this username
            # - .first() = Get first result (or None)
            # - If user exists, username is taken
            
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        # Step 26: Check if Email Exists
        if User.query.filter_by(email=email).first():
            # Explanation:
            # - User.query.filter_by(email=email) = Find user with this email
            # - .first() = Get first result (or None)
            # - If user exists, email is taken
            
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Step 27: Create New User
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
        
        # Step 28: Track Registration Event
        # What is this? Recording that user registered
        track_event(new_user.id, 'user_registered', f'{{"username": "{username}"}}')
        # Explanation:
        # - track_event() = Our helper function
        # - new_user.id = User who registered
        # - 'user_registered' = Type of event
        # - f'{{"username": "{username}"}}' = Additional data (JSON string)
        # - This records the registration event
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        # Explanation:
        # - Shows success message
        # - Redirects to login page
    
    return render_template('register.html')
    # Explanation:
    # - render_template = Shows registration form
    # - 'register.html' = Registration template

# Step 29: Create Login Route (GET and POST)
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
        
        # Step 30: Find User
        user = User.query.filter_by(username=username).first()
        # Explanation:
        # - User.query.filter_by(username=username) = Find user with this username
        # - .first() = Get first result (or None)
        # - user = User object (or None if not found)
        
        # Step 31: Verify Password
        if user and check_password_hash(user.password_hash, password):
            # Explanation:
            # - if user = If user was found
            # - check_password_hash(user.password_hash, password) = Verifies password
            # - Only proceed if user exists and password is correct
            
            session['user_id'] = user.id
            # Explanation:
            # - session['user_id'] = user.id = Stores user ID in session
            # - This logs the user in
            
            # Step 32: Track Login Event
            # What is this? Recording that user logged in
            track_event(user.id, 'user_login', f'{{"username": "{username}"}}')
            # Explanation:
            # - track_event() = Our helper function
            # - user.id = User who logged in
            # - 'user_login' = Type of event
            # - f'{{"username": "{username}"}}' = Additional data (JSON string)
            # - This records the login event
            
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

# Step 33: Create Logout Route
# What is this? Logs user out
@app.route('/logout')
def logout():
    """
    This function logs the user out
    """
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 34: Track Logout Event
    # What is this? Recording that user logged out
    if current_user:
        # Explanation:
        # - if current_user = If user is logged in
        # - Only track if user exists
        
        track_event(current_user.id, 'user_logout')
        # Explanation:
        # - track_event() = Our helper function
        # - current_user.id = User who logged out
        # - 'user_logout' = Type of event
        # - This records the logout event
    
    session.pop('user_id', None)
    # Explanation:
    # - session.pop('user_id', None) = Removes user_id from session
    # - This logs the user out
    
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))
    # Explanation:
    # - Shows success message
    # - Redirects to login page

# Step 35: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

