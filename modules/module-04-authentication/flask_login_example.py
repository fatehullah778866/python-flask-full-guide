# Flask-Login Complete Example
# This shows a complete authentication system using Flask-Login

from flask import Flask, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model with UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

# Create tables
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return '<h1>Welcome! <a href="/login">Login</a> or <a href="/register">Register</a></h1>'

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!', 'error')
            return render_template_string(registration_template, form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered!', 'error')
            return render_template_string(registration_template, form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(registration_template, form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template_string(login_template, form=form)

# Dashboard (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return f'''
    <h1>Dashboard</h1>
    <p>Welcome, {current_user.username}!</p>
    <p>Email: {current_user.email}</p>
    <p>Member since: {current_user.created_at.strftime("%Y-%m-%d")}</p>
    <a href="/profile">View Profile</a> | 
    <a href="/logout">Logout</a>
    '''

# Profile (protected)
@app.route('/profile')
@login_required
def profile():
    return f'''
    <h1>Profile</h1>
    <p>Username: {current_user.username}</p>
    <p>Email: {current_user.email}</p>
    <p>Account created: {current_user.created_at.strftime("%Y-%m-%d %H:%M")}</p>
    <a href="/dashboard">Back to Dashboard</a> | 
    <a href="/logout">Logout</a>
    '''

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Templates
login_template = '''
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {% if category == 'error' %}red{% else %}green{% endif %};">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    <p>Don't have an account? <a href="/register">Register</a></p>
</body>
</html>
'''

registration_template = '''
<html>
<head><title>Register</title></head>
<body>
    <h2>Register</h2>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {% if category == 'error' %}red{% else %}green{% endif %};">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.username.label }}<br>{{ form.username() }}</p>
        <p>{{ form.email.label }}<br>{{ form.email() }}</p>
        <p>{{ form.password.label }}<br>{{ form.password() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    <p>Already have an account? <a href="/login">Login</a></p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)

