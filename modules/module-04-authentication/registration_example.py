# User Registration Example
# This shows how to create user accounts with secure password hashing

from flask import Flask, render_template_string, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Create tables
with app.app_context():
    db.create_all()

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!', 'error')
            return render_template_string(registration_template, form=form)
        
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered!', 'error')
            return render_template_string(registration_template, form=form)
        
        # Hash the password (IMPORTANT: Never store plain passwords!)
        password_hash = generate_password_hash(form.password.data)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash
        )
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(registration_template, form=form)

# Simple login route (placeholder)
@app.route('/login')
def login():
    return "Login page (see login_example.py for full implementation)"

# Registration template
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
        
        <p>
            {{ form.username.label }}<br>
            {{ form.username() }}
            {% if form.username.errors %}
                {% for error in form.username.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>
            {{ form.email.label }}<br>
            {{ form.email() }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>
            {{ form.password.label }}<br>
            {{ form.password() }}
            {% if form.password.errors %}
                {% for error in form.password.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>
            {{ form.confirm_password.label }}<br>
            {{ form.confirm_password() }}
            {% if form.confirm_password.errors %}
                {% for error in form.confirm_password.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        
        <p>{{ form.submit() }}</p>
    </form>
    
    <p>Already have an account? <a href="/login">Login</a></p>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)

