# Basic Database Example
# This shows how to set up and use SQLite with Flask-SQLAlchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database created!")

# Route to add a user
@app.route('/add-user/<name>/<email>/<int:age>')
def add_user(name, email, age):
    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return f'User with email {email} already exists!'
    
    # Create new user
    user = User(name=name, email=email, age=age)
    db.session.add(user)
    db.session.commit()
    return f'User {name} added with ID: {user.id}'

# Route to get all users
@app.route('/users')
def get_users():
    users = User.query.all()
    if not users:
        return 'No users found!'
    
    result = []
    for user in users:
        result.append(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Age: {user.age}")
    return '<br>'.join(result)

# Route to get user by ID
@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return f"User: {user.name}, Email: {user.email}, Age: {user.age}"
    return 'User not found!'

# Route to update user
@app.route('/update/<int:user_id>/<new_name>')
def update_user(user_id, new_name):
    user = User.query.get(user_id)
    if user:
        user.name = new_name
        db.session.commit()
        return f'User updated to: {new_name}'
    return 'User not found!'

# Route to delete user
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        name = user.name
        db.session.delete(user)
        db.session.commit()
        return f'User {name} deleted!'
    return 'User not found!'

# Route to filter users
@app.route('/users/age/<int:min_age>')
def users_by_age(min_age):
    users = User.query.filter(User.age >= min_age).all()
    if not users:
        return f'No users found with age >= {min_age}'
    
    result = [f"Users with age >= {min_age}:"]
    for user in users:
        result.append(f"  - {user.name} (Age: {user.age})")
    return '<br>'.join(result)

if __name__ == '__main__':
    app.run(debug=True)

