# Auth Blueprint Routes
# User registration, login, logout

from flask import render_template, request, redirect, url_for, flash, session
from app.auth import bp
from app import db
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

# Forms
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
        Length(min=8, message='Password must be at least 8 characters')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Routes
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Create user with hashed password
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)  # Hash password
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check password
        if user and user.check_password(form.password.data):
            # Create session
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

