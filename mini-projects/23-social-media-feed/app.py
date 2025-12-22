# Social Media Feed App
# This app allows users to create posts, follow users, and see a personalized feed!

# Step 1: Import Flask and Database Tools
# What is this? We're importing Flask and database tools
# Think of it like: "Get Flask tools and database tools"
from flask import Flask, render_template, request, redirect, url_for, flash, session
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
# - SQLAlchemy = Database toolkit
# - datetime = Module for working with dates and times
# - generate_password_hash = Function to hash passwords securely
# - check_password_hash = Function to verify password hashes
# - We'll use SQLAlchemy to store users, posts, follows, and likes!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///social_media.db' = SQLite database file named 'social_media.db'
# - SQLite = Simple database that stores data in a file
# - social_media.db = The file where our data will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
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
# Think of it like: "Creating a template for users"
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
    # - We store hashed passwords, never plain text!
    
    # Step 6: Define Relationships
    # What is this? Creating relationships to other tables
    # Think of it like: "Connecting users to their posts and follows"
    
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - posts = Relationship to Post model
    # - backref='author' = Creates 'author' attribute on Post
    # - lazy=True = Loads posts when accessed
    # - cascade='all, delete-orphan' = Deletes posts when user is deleted
    # - This means: user.posts gives all posts by this user
    
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - following = Relationship to Follow model (users this user follows)
    # - foreign_keys='Follow.follower_id' = Uses follower_id as foreign key
    # - backref='follower' = Creates 'follower' attribute on Follow
    # - lazy=True = Loads follows when accessed
    # - cascade = Deletes follows when user is deleted
    # - This means: user.following gives all users this user follows
    
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - followers = Relationship to Follow model (users who follow this user)
    # - foreign_keys='Follow.followed_id' = Uses followed_id as foreign key
    # - backref='followed' = Creates 'followed' attribute on Follow
    # - lazy=True = Loads follows when accessed
    # - cascade = Deletes follows when user is deleted
    # - This means: user.followers gives all users who follow this user
    
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - likes = Relationship to Like model
    # - backref='user' = Creates 'user' attribute on Like
    # - lazy=True = Loads likes when accessed
    # - cascade = Deletes likes when user is deleted
    # - This means: user.likes gives all likes by this user
    
    def __repr__(self):
        return f'<User {self.username}>'

# Step 7: Create Post Model
# What is this? Defining what a post looks like
class Post(db.Model):
    """
    Post Model
    This defines the structure of a post in the database
    """
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    content = db.Column(db.Text, nullable=False)
    # Explanation:
    # - content = Post content (the actual text)
    # - db.Text = Text field (can hold long text)
    # - nullable=False = This field is required
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - author_id = ID of the user who created this post
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Every post must have an author
    # - This creates relationship: Post → User
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When post was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - likes = Relationship to Like model
    # - backref='post' = Creates 'post' attribute on Like
    # - lazy=True = Loads likes when accessed
    # - cascade = Deletes likes when post is deleted
    # - This means: post.likes gives all likes on this post
    
    def __repr__(self):
        return f'<Post {self.id}>'

# Step 8: Create Follow Model
# What is this? Defining what a follow relationship looks like
class Follow(db.Model):
    """
    Follow Model
    This defines the structure of a follow relationship
    """
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - follower_id = ID of user who is following
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Required
    # - Example: User 1 follows User 2 → follower_id = 1
    
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - followed_id = ID of user being followed
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Required
    # - Example: User 1 follows User 2 → followed_id = 2
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When follow relationship was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),)
    # Explanation:
    # - __table_args__ = Table constraints
    # - UniqueConstraint = Prevents duplicate follows
    # - 'follower_id', 'followed_id' = Columns that must be unique together
    # - This ensures: User can only follow another user once!
    
    def __repr__(self):
        return f'<Follow {self.follower_id} -> {self.followed_id}>'

# Step 9: Create Like Model
# What is this? Defining what a like looks like
class Like(db.Model):
    """
    Like Model
    This defines the structure of a like in the database
    """
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - user_id = ID of user who liked
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Required
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    # Explanation:
    # - post_id = ID of post being liked
    # - db.ForeignKey('posts.id') = Links to posts table
    # - nullable=False = Required
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When like was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_like'),)
    # Explanation:
    # - UniqueConstraint = Prevents duplicate likes
    # - 'user_id', 'post_id' = Columns that must be unique together
    # - This ensures: User can only like a post once!
    
    def __repr__(self):
        return f'<Like {self.user_id} -> {self.post_id}>'

# Step 10: Create Database Tables
# What is this? Creating the actual database tables
with app.app_context():
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models and creates tables

# Step 11: Helper Function to Check if User is Logged In
# What is this? Function to check if user is authenticated
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
    # - If not, user is not logged in

# Step 12: Helper Function to Get Current User
# What is this? Function to get the logged-in user
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

# Step 13: Create Home Route (GET)
# What is this? The main page that shows the feed
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows the personalized feed
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only show feed if logged in
        
        return redirect(url_for('login'))
        # Explanation:
        # - redirect = Sends user to login page
        # - Must be logged in to see feed
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 14: Get Followed User IDs
    # What is this? Finding which users the current user follows
    followed_ids = [follow.followed_id for follow in current_user.following]
    # Explanation:
    # - current_user.following = All follow relationships
    # - for follow in current_user.following = Loop through follows
    # - follow.followed_id = ID of followed user
    # - List comprehension = Creates list of IDs
    # - followed_ids = List of user IDs that current user follows
    # - Example: [2, 3, 5] = Following users 2, 3, and 5
    
    # Step 15: Add Current User's ID
    # What is this? Including current user's own posts in feed
    followed_ids.append(current_user.id)
    # Explanation:
    # - followed_ids.append(current_user.id) = Adds own ID
    # - This ensures user sees their own posts too
    # - Example: [2, 3, 5, 1] = Following 2, 3, 5, and self (1)
    
    # Step 16: Get Posts from Followed Users
    # What is this? Getting posts from users in the feed
    posts = Post.query.filter(Post.author_id.in_(followed_ids)).order_by(Post.date_created.desc()).all()
    # Explanation:
    # - Post.query = Query object for Post model
    # - .filter(Post.author_id.in_(followed_ids)) = Filter by author ID
    # - .in_(followed_ids) = Author ID must be in followed_ids list
    # - .order_by(Post.date_created.desc()) = Sort by date, newest first
    # - .all() = Get all matching posts
    # - posts = List of Post objects from followed users (and self)
    
    # Step 17: Get User's Likes
    # What is this? Finding which posts the user has liked
    user_likes = [like.post_id for like in current_user.likes]
    # Explanation:
    # - current_user.likes = All likes by current user
    # - for like in current_user.likes = Loop through likes
    # - like.post_id = ID of liked post
    # - List comprehension = Creates list of post IDs
    # - user_likes = List of post IDs that user has liked
    # - Example: [1, 3, 7] = Liked posts 1, 3, and 7
    
    return render_template('index.html', posts=posts, user_likes=user_likes, current_user=current_user)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = Feed template
    # - posts=posts = Passes posts to template
    # - user_likes=user_likes = Passes liked post IDs to template
    # - current_user=current_user = Passes current user to template

# Step 18: Create Register Route (GET and POST)
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
        
        # Step 19: Validate Input
        if not username or not email or not password:
            # Explanation:
            # - if not username or not email or not password = If any field empty
            # - Only proceed if all fields filled
            
            flash('Please fill in all fields!', 'error')
            return render_template('register.html')
        
        # Step 20: Check if Username Exists
        if User.query.filter_by(username=username).first():
            # Explanation:
            # - User.query.filter_by(username=username) = Find user with this username
            # - .first() = Get first result (or None)
            # - If user exists, username is taken
            
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        # Step 21: Check if Email Exists
        if User.query.filter_by(email=email).first():
            # Explanation:
            # - User.query.filter_by(email=email) = Find user with this email
            # - .first() = Get first result (or None)
            # - If user exists, email is taken
            
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Step 22: Create New User
        password_hash = generate_password_hash(password)
        # Explanation:
        # - generate_password_hash(password) = Hashes password securely
        # - password_hash = Hashed password (not plain text!)
        # - Never store plain text passwords!
        
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
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        # Explanation:
        # - Shows success message
        # - Redirects to login page
    
    return render_template('register.html')
    # Explanation:
    # - render_template = Shows registration form
    # - 'register.html' = Registration template

# Step 23: Create Login Route (GET and POST)
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
        
        # Step 24: Find User
        user = User.query.filter_by(username=username).first()
        # Explanation:
        # - User.query.filter_by(username=username) = Find user with this username
        # - .first() = Get first result (or None)
        # - user = User object (or None if not found)
        
        # Step 25: Verify Password
        if user and check_password_hash(user.password_hash, password):
            # Explanation:
            # - if user = If user was found
            # - check_password_hash(user.password_hash, password) = Verifies password
            # - Only proceed if user exists and password is correct
            
            session['user_id'] = user.id
            # Explanation:
            # - session['user_id'] = user.id = Stores user ID in session
            # - This logs the user in
            # - Session persists across requests
            
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
            # Explanation:
            # - Shows success message
            # - Redirects to home page (feed)
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

# Step 26: Create Logout Route
# What is this? Logs user out
@app.route('/logout')
def logout():
    """
    This function logs the user out
    """
    session.pop('user_id', None)
    # Explanation:
    # - session.pop('user_id', None) = Removes user_id from session
    # - .pop() = Removes key from dictionary
    # - None = Default if key doesn't exist
    # - This logs the user out
    
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))
    # Explanation:
    # - Shows success message
    # - Redirects to login page

# Step 27: Create Create Post Route (POST)
# What is this? Handles creating a new post
@app.route('/create-post', methods=['POST'])
def create_post():
    """
    This function handles creating a new post
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can create posts
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    content = request.form.get('content', '').strip()
    # Explanation:
    # - Gets post content from form
    # - content = Post text
    
    if not content:
        # Explanation:
        # - if not content = If content is empty
        # - Only proceed if content exists
        
        flash('Post content cannot be empty!', 'error')
        return redirect(url_for('index'))
        # Explanation:
        # - Shows error message
        # - Redirects back to feed
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 28: Create New Post
    new_post = Post(
        content=content,
        author_id=current_user.id
    )
    # Explanation:
    # - Post() = Creates new Post object
    # - content=content = Sets post content
    # - author_id=current_user.id = Sets author to current user
    # - date_created = Automatically set (from model default)
    # - new_post = New post (not saved yet)
    
    db.session.add(new_post)
    db.session.commit()
    # Explanation:
    # - db.session.add(new_post) = Adds post to session
    # - db.session.commit() = Saves to database
    
    flash('Post created successfully!', 'success')
    return redirect(url_for('index'))
    # Explanation:
    # - Shows success message
    # - Redirects back to feed

# Step 29: Create Like/Unlike Route (POST)
# What is this? Handles liking/unliking a post
@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """
    This function handles liking/unliking a post
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can like posts
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    post = Post.query.get_or_404(post_id)
    # Explanation:
    # - Post.query.get_or_404(post_id) = Gets post by ID
    # - post_id = ID from URL
    # - post = Post object (or 404 error if not found)
    
    # Step 30: Check if Already Liked
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    # Explanation:
    # - Like.query.filter_by(user_id=current_user.id, post_id=post_id) = Find like
    # - .first() = Get first result (or None)
    # - existing_like = Like object (or None if not liked)
    
    if existing_like:
        # Explanation:
        # - if existing_like = If user already liked this post
        # - User wants to unlike
        
        db.session.delete(existing_like)
        # Explanation:
        # - db.session.delete(existing_like) = Deletes like
        # - Removes like from database
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves changes
        
        flash('Post unliked!', 'success')
        # Explanation:
        # - Shows success message
    else:
        # Explanation:
        # - else = If user hasn't liked this post
        # - User wants to like
        
        new_like = Like(
            user_id=current_user.id,
            post_id=post_id
        )
        # Explanation:
        # - Like() = Creates new Like object
        # - user_id=current_user.id = Sets user who liked
        # - post_id=post_id = Sets post being liked
        # - date_created = Automatically set (from model default)
        # - new_like = New like (not saved yet)
        
        db.session.add(new_like)
        db.session.commit()
        # Explanation:
        # - db.session.add(new_like) = Adds like to session
        # - db.session.commit() = Saves to database
        
        flash('Post liked!', 'success')
        # Explanation:
        # - Shows success message
    
    return redirect(url_for('index'))
    # Explanation:
    # - Redirects back to feed

# Step 31: Create Follow/Unfollow Route (POST)
# What is this? Handles following/unfollowing a user
@app.route('/follow/<int:user_id>', methods=['POST'])
def follow_user(user_id):
    """
    This function handles following/unfollowing a user
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can follow others
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    current_user = get_current_user()
    # Explanation:
        # - get_current_user() = Gets logged-in user
        # - current_user = User object
    
    if user_id == current_user.id:
        # Explanation:
        # - if user_id == current_user.id = If trying to follow self
        # - Can't follow yourself!
        
        flash('You cannot follow yourself!', 'error')
        return redirect(url_for('index'))
        # Explanation:
        # - Shows error message
        # - Redirects back to feed
    
    user_to_follow = User.query.get_or_404(user_id)
    # Explanation:
    # - User.query.get_or_404(user_id) = Gets user by ID
    # - user_id = ID from URL
    # - user_to_follow = User object (or 404 error if not found)
    
    # Step 32: Check if Already Following
    existing_follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    # Explanation:
    # - Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id) = Find follow
    # - .first() = Get first result (or None)
    # - existing_follow = Follow object (or None if not following)
    
    if existing_follow:
        # Explanation:
        # - if existing_follow = If user already follows this user
        # - User wants to unfollow
        
        db.session.delete(existing_follow)
        # Explanation:
        # - db.session.delete(existing_follow) = Deletes follow
        # - Removes follow from database
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves changes
        
        flash(f'Unfollowed {user_to_follow.username}!', 'success')
        # Explanation:
        # - Shows success message
    else:
        # Explanation:
        # - else = If user doesn't follow this user
        # - User wants to follow
        
        new_follow = Follow(
            follower_id=current_user.id,
            followed_id=user_id
        )
        # Explanation:
        # - Follow() = Creates new Follow object
        # - follower_id=current_user.id = Sets user who is following
        # - followed_id=user_id = Sets user being followed
        # - date_created = Automatically set (from model default)
        # - new_follow = New follow (not saved yet)
        
        db.session.add(new_follow)
        db.session.commit()
        # Explanation:
        # - db.session.add(new_follow) = Adds follow to session
        # - db.session.commit() = Saves to database
        
        flash(f'Following {user_to_follow.username}!', 'success')
        # Explanation:
        # - Shows success message
    
    return redirect(url_for('index'))
    # Explanation:
    # - Redirects back to feed

# Step 33: Create Users Route (GET)
# What is this? Page showing all users
@app.route('/users')
def users():
    """
    This function shows all users
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can see users list
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    all_users = User.query.all()
    # Explanation:
    # - User.query.all() = Gets all users
    # - all_users = List of all User objects
    
    # Step 34: Get Following IDs
    following_ids = [follow.followed_id for follow in current_user.following]
    # Explanation:
    # - current_user.following = All follow relationships
    # - for follow in current_user.following = Loop through follows
    # - follow.followed_id = ID of followed user
    # - List comprehension = Creates list of IDs
    # - following_ids = List of user IDs that current user follows
    
    return render_template('users.html', users=all_users, current_user=current_user, following_ids=following_ids)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'users.html' = Users list template
    # - users=all_users = Passes all users to template
    # - current_user=current_user = Passes current user to template
    # - following_ids=following_ids = Passes following IDs to template

# Step 34: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

