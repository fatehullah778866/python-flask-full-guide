# Blog Application with Authentication
# This Flask app creates a secure blog with user authentication

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # For sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    """User Model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password, NOT plain text!
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash password before saving"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Post Model
class Post(db.Model):
    """Blog Post Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to user
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Login Required Decorator
# This protects routes so only logged-in users can access them
def login_required(f):
    """Decorator to protect routes - only logged-in users can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page - List all posts
@app.route('/')
def index():
    """Display all blog posts"""
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate form data
        errors = []
        
        if not username:
            errors.append('Username is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        # If there are errors, show them
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)  # Hash the password
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    # Show registration form
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Create session (user is now logged in)
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    # Show login form
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()  # Remove all session data
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# View single post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Display a single blog post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# Create new post (PROTECTED - requires login)
@app.route('/create', methods=['GET', 'POST'])
@login_required  # Only logged-in users can access
def create_post():
    """Create a new blog post"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Create new post
        post = Post(
            title=title,
            content=content,
            author=session['username'],  # Use logged-in user's username
            user_id=session['user_id']   # Link to logged-in user
        )
        
        # Save to database
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    
    # Show create form
    return render_template('create.html')

# Edit post (PROTECTED - requires login)
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required  # Only logged-in users can access
def edit_post(post_id):
    """Edit an existing blog post"""
    # Get post from database
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can edit
    if post.user_id != session['user_id']:
        flash('You can only edit your own posts', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Update post with new data
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.date_updated = datetime.utcnow()
        
        # Save changes
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('view_post', post_id=post.id))
    
    # Show edit form with current post data
    return render_template('edit.html', post=post)

# Delete post (PROTECTED - requires login)
@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required  # Only logged-in users can access
def delete_post(post_id):
    """Delete a blog post"""
    # Get post from database
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can delete
    if post.user_id != session['user_id']:
        flash('You can only delete your own posts', 'error')
        return redirect(url_for('index'))
    
    # Delete post
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Start the Flask development server
    app.run(debug=True)

