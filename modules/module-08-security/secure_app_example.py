# Secure Flask Application Example
# This shows security best practices in Flask

from flask import Flask, render_template_string, request, session, redirect
from flask_wtf import FlaskForm, CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import timedelta
from markupsafe import escape
import os
import re

app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = False  # True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# CSRF Protection
csrf = CSRFProtect(app)

# Database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Security Headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if not app.debug:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Input Validation Functions
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """Check if password is strong"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain a number"
    return True, "Password is strong"

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

# Routes
@app.route('/')
def home():
    return '''
    <h1>Secure Flask App</h1>
    <ul>
        <li><a href="/register">Register</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/comment?text=Hello">Test XSS Protection</a></li>
    </ul>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data
        
        # Validate email
        if not is_valid_email(email):
            return "Invalid email format", 400
        
        # Validate password strength
        is_strong, message = is_strong_password(password)
        if not is_strong:
            return message, 400
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            return "Email already registered", 400
        
        # Hash password securely
        password_hash = generate_password_hash(password)
        
        # Create user
        user = User(email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        
        return "Registration successful! Please login.", 201
    
    return render_template_string('''
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    ''', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Safe database query (SQLAlchemy prevents injection)
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect('/dashboard')
        
        return "Invalid credentials", 401
    
    return render_template_string('''
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    ''', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return f'<h1>Dashboard</h1><p>Welcome! User ID: {session["user_id"]}</p>'

# XSS Protection Example
@app.route('/comment')
def show_comment():
    # User input (automatically escaped by Jinja2)
    comment = request.args.get('text', '')
    # Manual escaping for extra safety
    safe_comment = escape(comment)
    
    return render_template_string('''
    <h1>Comment</h1>
    <p>Your comment: {{ comment }}</p>
    <p>This is automatically escaped by Jinja2!</p>
    <p>Try: /comment?text=<script>alert('XSS')</script></p>
    ''', comment=comment)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

