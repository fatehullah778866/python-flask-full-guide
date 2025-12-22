# API with JWT Authentication App
# This app demonstrates JWT (JSON Web Token) authentication for APIs!

# Step 1: Import Flask and JWT Tools
# What is this? We're importing Flask and JWT authentication tools
# Think of it like: "Get Flask tools and security tools"
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, 
    create_refresh_token, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
# Explanation:
# - Flask = The main Flask class
# - request = Object that contains request data
# - jsonify = Function to return JSON responses
# - SQLAlchemy = Database toolkit
# - JWTManager = JWT manager for Flask
# - jwt_required = Decorator to protect routes (requires valid JWT token)
# - create_access_token = Function to create JWT access token
# - create_refresh_token = Function to create JWT refresh token
# - get_jwt_identity = Function to get user ID from JWT token
# - get_jwt = Function to get JWT token data
# - generate_password_hash = Function to hash passwords securely
# - check_password_hash = Function to verify password hashes
# - datetime = Module for working with dates and times
# - timedelta = For date calculations
# - We'll use JWT for secure API authentication!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwt_api.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///jwt_api.db' = SQLite database file
# - SQLite = Simple database that stores data in a file
# - jwt_api.db = The file where our data will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

# Step 4: Configure JWT
# What is this? Setting up JWT authentication
# Think of it like: "Set up security for API"
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'JWT_SECRET_KEY' = Secret key for signing JWT tokens
# - This is used to sign and verify tokens
# - In production, use a long, random, secure string!
# - Never share this key publicly!

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# Explanation:
# - 'JWT_ACCESS_TOKEN_EXPIRES' = How long access tokens are valid
# - timedelta(hours=1) = 1 hour
# - After 1 hour, access token expires and user must refresh
# - Access tokens = Short-lived tokens for API access

app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
# Explanation:
# - 'JWT_REFRESH_TOKEN_EXPIRES' = How long refresh tokens are valid
# - timedelta(days=30) = 30 days
# - After 30 days, refresh token expires and user must login again
# - Refresh tokens = Long-lived tokens for getting new access tokens

# Step 5: Initialize Database and JWT
# What is this? Creating the database and JWT objects
db = SQLAlchemy(app)
# Explanation:
# - SQLAlchemy(app) = Creates database object
# - db = Our database manager

jwt = JWTManager(app)
# Explanation:
# - JWTManager(app) = Creates JWT manager
# - jwt = Our JWT manager
# - This enables JWT authentication!

# Step 6: Create User Model
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
    
    def __repr__(self):
        return f'<User {self.username}>'

# Step 7: Create Resource Model (Example Data)
# What is this? Example data to protect with JWT
class Resource(db.Model):
    """
    Resource Model
    Example data that requires authentication to access
    """
    __tablename__ = 'resources'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'resources' = Name of the table in database
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    name = db.Column(db.String(100), nullable=False)
    # Explanation:
    # - name = Resource name
    # - db.String(100) = Text field, max 100 characters
    # - nullable=False = This field is required
    
    description = db.Column(db.Text)
    # Explanation:
    # - description = Resource description
    # - db.Text = Text field (can hold long text)
    # - nullable=True = This field is optional
    
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - owner_id = ID of user who owns this resource
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Every resource must have an owner
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When resource was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    def to_dict(self):
        """
        Convert resource to dictionary for JSON response
        
        Returns:
        - Dictionary representation of resource
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'date_created': self.date_created.isoformat()
        }
        # Explanation:
        # - to_dict() = Method to convert object to dictionary
        # - Returns dictionary with all resource fields
        # - isoformat() = Converts date to ISO format string
        # - This makes it easy to return as JSON
    
    def __repr__(self):
        return f'<Resource {self.name}>'

# Step 8: Create Database Tables
# What is this? Creating the actual database tables
with app.app_context():
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models and creates tables

# Step 9: Create Register Endpoint (POST)
# What is this? API endpoint for user registration
@app.route('/api/register', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/register' = The URL for registration
# - methods=['POST'] = Only accepts POST requests
# - This is an API endpoint (returns JSON, not HTML)

def register():
    """
    This function handles user registration via API
    It creates a new user and returns JSON response
    """
    # Step 10: Get JSON Data from Request
    # What is this? Getting registration data from request
    data = request.get_json()
    # Explanation:
    # - request.get_json() = Gets JSON data from request body
    # - data = Dictionary with registration information
    # - Example: {'username': 'john', 'email': 'john@example.com', 'password': 'secret'}
    
    # Step 11: Validate Input
    # What is this? Checking if required fields are provided
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        # Explanation:
        # - if not data = If no data was sent
        # - not data.get('username') = If username is missing
        # - not data.get('email') = If email is missing
        # - not data.get('password') = If password is missing
        # - Only proceed if all fields are provided
        
        return jsonify({'error': 'Username, email, and password are required'}), 400
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': '...'} = Error message
        # - 400 = Bad Request status code
        # - This tells the client what went wrong
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # Explanation:
    # - Gets values from data dictionary
    # - username, email, password = User input
    
    # Step 12: Check if Username Exists
    if User.query.filter_by(username=username).first():
        # Explanation:
        # - User.query.filter_by(username=username) = Find user with this username
        # - .first() = Get first result (or None)
        # - If user exists, username is taken
        
        return jsonify({'error': 'Username already exists'}), 400
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': '...'} = Error message
        # - 400 = Bad Request status code
    
    # Step 13: Check if Email Exists
    if User.query.filter_by(email=email).first():
        # Explanation:
        # - User.query.filter_by(email=email) = Find user with this email
        # - .first() = Get first result (or None)
        # - If user exists, email is taken
        
        return jsonify({'error': 'Email already exists'}), 400
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': '...'} = Error message
        # - 400 = Bad Request status code
    
    # Step 14: Create New User
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
    
    # Step 15: Return Success Response
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }
    }), 201
    # Explanation:
    # - jsonify() = Returns JSON response
    # - {'message': '...'} = Success message
    # - 'user' = User information (without password!)
    # - 201 = Created status code
    # - This tells the client registration was successful

# Step 16: Create Login Endpoint (POST)
# What is this? API endpoint for user login
@app.route('/api/login', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/login' = The URL for login
# - methods=['POST'] = Only accepts POST requests

def login():
    """
    This function handles user login via API
    It validates credentials and returns JWT tokens
    """
    # Step 17: Get JSON Data from Request
    # What is this? Getting login data from request
    data = request.get_json()
    # Explanation:
    # - request.get_json() = Gets JSON data from request body
    # - data = Dictionary with login information
    # - Example: {'username': 'john', 'password': 'secret'}
    
    # Step 18: Validate Input
    # What is this? Checking if required fields are provided
    if not data or not data.get('username') or not data.get('password'):
        # Explanation:
        # - if not data = If no data was sent
        # - not data.get('username') = If username is missing
        # - not data.get('password') = If password is missing
        # - Only proceed if both fields are provided
        
        return jsonify({'error': 'Username and password are required'}), 400
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': '...'} = Error message
        # - 400 = Bad Request status code
    
    username = data.get('username')
    password = data.get('password')
    # Explanation:
    # - Gets values from data dictionary
    # - username, password = User input
    
    # Step 19: Find User
    user = User.query.filter_by(username=username).first()
    # Explanation:
    # - User.query.filter_by(username=username) = Find user with this username
    # - .first() = Get first result (or None)
    # - user = User object (or None if not found)
    
    # Step 20: Verify Password
    if not user or not check_password_hash(user.password_hash, password):
        # Explanation:
        # - if not user = If user was not found
        # - check_password_hash(user.password_hash, password) = Verifies password
        # - Only proceed if user exists and password is correct
        
        return jsonify({'error': 'Invalid username or password'}), 401
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': '...'} = Error message
        # - 401 = Unauthorized status code
        # - This tells the client login failed
    
    # Step 21: Create JWT Access Token
    # What is this? Creating a JWT token for API access
    access_token = create_access_token(identity=user.id)
    # Explanation:
    # - create_access_token() = Creates JWT access token
    # - identity=user.id = User ID to encode in token
    # - access_token = JWT token string
    # - Token contains user ID and expiration time
    # - Client will send this token with API requests
    
    # Step 22: Create JWT Refresh Token
    # What is this? Creating a refresh token for getting new access tokens
    refresh_token = create_refresh_token(identity=user.id)
    # Explanation:
    # - create_refresh_token() = Creates JWT refresh token
    # - identity=user.id = User ID to encode in token
    # - refresh_token = JWT token string
    # - Refresh token lasts longer (30 days)
    # - Used to get new access tokens when they expire
    
    # Step 23: Return Tokens
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200
    # Explanation:
    # - jsonify() = Returns JSON response
    # - 'access_token' = Short-lived token for API access
    # - 'refresh_token' = Long-lived token for refreshing
    # - 'user' = User information
    # - 200 = OK status code
    # - Client will use these tokens for authenticated requests

# Step 24: Create Refresh Token Endpoint (POST)
# What is this? API endpoint to get new access token
@app.route('/api/refresh', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/refresh' = The URL for token refresh
# - methods=['POST'] = Only accepts POST requests

@jwt_required(refresh=True)
# Explanation:
# - @jwt_required(refresh=True) = Requires valid refresh token
# - refresh=True = Expects refresh token (not access token)
# - Only users with valid refresh token can access this

def refresh():
    """
    This function handles token refresh
    It creates a new access token using a refresh token
    """
    # Step 25: Get User ID from Token
    # What is this? Getting the user ID from the refresh token
    current_user_id = get_jwt_identity()
    # Explanation:
    # - get_jwt_identity() = Gets user ID from JWT token
    # - current_user_id = User ID from token
    # - This is the user who sent the refresh token
    
    # Step 26: Create New Access Token
    # What is this? Creating a new access token
    new_access_token = create_access_token(identity=current_user_id)
    # Explanation:
    # - create_access_token() = Creates new JWT access token
    # - identity=current_user_id = User ID to encode in token
    # - new_access_token = New JWT token string
    # - This is a fresh access token (valid for 1 hour)
    
    return jsonify({
        'access_token': new_access_token
    }), 200
    # Explanation:
    # - jsonify() = Returns JSON response
    # - 'access_token' = New access token
    # - 200 = OK status code
    # - Client can use this new token for API requests

# Step 27: Create Protected Resource Endpoint (GET)
# What is this? API endpoint that requires authentication
@app.route('/api/resources', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/resources' = The URL for resources
# - methods=['GET'] = Only accepts GET requests

@jwt_required()
# Explanation:
# - @jwt_required() = Requires valid JWT access token
# - No parameters = Expects access token
# - Only authenticated users can access this endpoint
# - If no token or invalid token, returns 401 Unauthorized

def get_resources():
    """
    This function returns all resources
    Requires valid JWT access token
    """
    # Step 28: Get User ID from Token
    # What is this? Getting the user ID from the access token
    current_user_id = get_jwt_identity()
    # Explanation:
    # - get_jwt_identity() = Gets user ID from JWT token
    # - current_user_id = User ID from token
    # - This is the user who sent the request
    
    # Step 29: Get User's Resources
    # What is this? Finding resources owned by this user
    resources = Resource.query.filter_by(owner_id=current_user_id).all()
    # Explanation:
    # - Resource.query.filter_by(owner_id=current_user_id) = Find resources for user
    # - .all() = Get all matching resources
    # - resources = List of Resource objects
    
    # Step 30: Convert to JSON
    # What is this? Converting resources to JSON format
    resources_list = [resource.to_dict() for resource in resources]
    # Explanation:
    # - for resource in resources = Loop through resources
    # - resource.to_dict() = Converts resource to dictionary
    # - List comprehension = Creates list of dictionaries
    # - resources_list = List of resource dictionaries
    # - Example: [{'id': 1, 'name': 'Resource 1', ...}, {'id': 2, ...}]
    
    return jsonify({
        'resources': resources_list,
        'count': len(resources_list)
    }), 200
    # Explanation:
    # - jsonify() = Returns JSON response
    # - 'resources' = List of resources
    # - 'count' = Number of resources
    # - 200 = OK status code
    # - Client receives JSON data

# Step 31: Create Create Resource Endpoint (POST)
# What is this? API endpoint to create a new resource
@app.route('/api/resources', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/resources' = The URL for creating resources
# - methods=['POST'] = Only accepts POST requests

@jwt_required()
# Explanation:
# - @jwt_required() = Requires valid JWT access token
# - Only authenticated users can create resources

def create_resource():
    """
    This function creates a new resource
    Requires valid JWT access token
    """
    # Step 32: Get User ID from Token
    # What is this? Getting the user ID from the access token
    current_user_id = get_jwt_identity()
    # Explanation:
    # - get_jwt_identity() = Gets user ID from JWT token
    # - current_user_id = User ID from token
    
    # Step 33: Get JSON Data from Request
    # What is this? Getting resource data from request
    data = request.get_json()
    # Explanation:
    # - request.get_json() = Gets JSON data from request body
    # - data = Dictionary with resource information
    # - Example: {'name': 'My Resource', 'description': 'Description'}
    
    # Step 34: Validate Input
    # What is this? Checking if required fields are provided
    if not data or not data.get('name'):
        # Explanation:
        # - if not data = If no data was sent
        # - not data.get('name') = If name is missing
        # - Only proceed if name is provided
        
        return jsonify({'error': 'Resource name is required'}), 400
        # Explanation:
        # - jsonify() = Returns JSON response
        # - {'error': '...'} = Error message
        # - 400 = Bad Request status code
    
    name = data.get('name')
    description = data.get('description', '')
    # Explanation:
    # - Gets values from data dictionary
    # - name, description = Resource information
    
    # Step 35: Create New Resource
    new_resource = Resource(
        name=name,
        description=description,
        owner_id=current_user_id
    )
    # Explanation:
    # - Resource() = Creates new Resource object
    # - name=name = Sets resource name
    # - description=description = Sets resource description
    # - owner_id=current_user_id = Sets owner to current user
    # - date_created = Automatically set (from model default)
    # - new_resource = New resource (not saved yet)
    
    db.session.add(new_resource)
    db.session.commit()
    # Explanation:
    # - db.session.add(new_resource) = Adds resource to session
    # - db.session.commit() = Saves to database
    
    return jsonify({
        'message': 'Resource created successfully',
        'resource': new_resource.to_dict()
    }), 201
    # Explanation:
    # - jsonify() = Returns JSON response
    # - 'message' = Success message
    # - 'resource' = Created resource information
    # - 201 = Created status code

# Step 36: Create API Documentation Route (GET)
# What is this? Page showing API documentation
@app.route('/')
def api_docs():
    """
    This function shows API documentation
    """
    return render_template('api_docs.html')
    # Explanation:
    # - render_template = Displays HTML template
    # - 'api_docs.html' = API documentation template
    # - This shows how to use the API

# Step 37: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

