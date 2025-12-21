# Secured Flask Application
# This app demonstrates security best practices

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import escape
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from datetime import datetime, timedelta
import os
import re

# Create Flask app
app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secure Session Settings
app.config['SESSION_COOKIE_SECURE'] = False  # True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # JavaScript can't access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# CSRF Protection
csrf = CSRFProtect(app)

# Database
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    """User Model with secure password storage"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed, NOT plain text!
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and store password"""
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Custom Validators
def validate_strong_password(form, field):
    """Validate password strength"""
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain uppercase letter')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain lowercase letter')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain a number')

# Forms with CSRF Protection
class RegisterForm(FlaskForm):
    """Registration form with validation"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be 3-80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        validate_strong_password
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """Login form with CSRF protection"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    """Post creation form"""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200, message='Title must be less than 200 characters')
    ])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')

# Security Headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME sniffing
    response.headers['X-Frame-Options'] = 'DENY'  # Prevent clickjacking
    response.headers['X-XSS-Protection'] = '1; mode=block'  # XSS protection
    if not app.debug:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Input Validation Functions
def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ''
    # Remove dangerous characters
    text = escape(text)  # Escape HTML
    # Remove script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    return text

# Routes

@app.route('/')
def index():
    """Home page"""
    posts = Post.query.order_by(Post.date_created.desc()).limit(10).all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with security"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Check if username already exists (prevent duplicates)
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        # Create user with hashed password
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)  # Hash password before saving
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with secure password checking"""
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user (SQLAlchemy prevents SQL injection)
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            # Create secure session
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()  # Clear all session data
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create new post (protected route)"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to create posts', 'error')
        return redirect(url_for('login'))
    
    form = PostForm()
    
    if form.validate_on_submit():
        # Sanitize input (extra safety)
        title = sanitize_input(form.title.data)
        content = sanitize_input(form.content.data)
        
        # Create post
        post = Post(
            title=title,
            content=content,
            author=session['username'],
            user_id=session['user_id']
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create.html', form=form)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View a single post"""
    post = Post.query.get_or_404(post_id)
    # Jinja2 automatically escapes content (XSS protection)
    return render_template('post.html', post=post)

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

