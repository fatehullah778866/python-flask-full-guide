# Auth Blueprint Routes
# Authentication routes (login, register, logout)

from flask import render_template, request, redirect, url_for, flash, session
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash

# Simple user storage (in real app, use database)
# This is just for demonstration
users = {}

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate
        errors = []
        if not username:
            errors.append('Username is required')
        if not password:
            errors.append('Password is required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if username in users:
            errors.append('Username already exists')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        # Create user (hash password)
        users[username] = {
            'password_hash': generate_password_hash(password),
            'username': username
        }
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        
        # Check if user exists
        if username in users:
            user = users[username]
            # Check password
            if check_password_hash(user['password_hash'], password):
                # Create session
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('main.index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

