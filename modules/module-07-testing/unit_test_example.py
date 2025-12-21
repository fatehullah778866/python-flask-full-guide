# Unit Testing Example
# This shows how to write unit tests for Flask applications

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pytest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({"users": [{"id": u.id, "name": u.name} for u in users]})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email required"}), 400
    
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name}), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name})
    return jsonify({"error": "User not found"}), 404

# Test fixtures
@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# Unit tests
def test_home(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello World!' in response.data

def test_get_users_empty(client):
    """Test getting users when none exist"""
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data['users'] == []

def test_create_user(client):
    """Test creating a user"""
    response = client.post('/api/users',
                          json={'name': 'John', 'email': 'john@email.com'},
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'John'
    assert 'id' in data

def test_create_user_missing_data(client):
    """Test creating user with missing data"""
    response = client.post('/api/users',
                          json={'name': 'John'},
                          content_type='application/json')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_get_user(client):
    """Test getting a specific user"""
    # Create user first
    with app.app_context():
        user = User(name='John', email='john@email.com')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # Get user
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John'

def test_get_user_not_found(client):
    """Test getting non-existent user"""
    response = client.get('/api/users/999')
    assert response.status_code == 404
    assert 'error' in response.get_json()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

