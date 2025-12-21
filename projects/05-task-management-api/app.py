# Task Management API
# A RESTful API for managing tasks

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    """Task Model for the database"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert task object to dictionary (for JSON response)"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'date_created': self.date_created.isoformat()
        }
    
    def __repr__(self):
        return f'<Task {self.title}>'

# API Endpoints

# GET /api/tasks - Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# GET /api/tasks/<id> - Get a single task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

# POST /api/tasks - Create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    # Get JSON data from request
    data = request.get_json()
    
    # Validate that title is provided
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Create new task
    task = Task(
        title=data['title'],
        description=data.get('description', ''),  # Optional field
        completed=data.get('completed', False)     # Optional field, defaults to False
    )
    
    # Save to database
    db.session.add(task)
    db.session.commit()
    
    # Return created task with 201 status code (Created)
    return jsonify(task.to_dict()), 201

# PUT /api/tasks/<id> - Update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    # Get task from database
    task = Task.query.get_or_404(task_id)
    
    # Get JSON data from request
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'title' in data:
        task.title = data['title']
    
    if 'description' in data:
        task.description = data['description']
    
    if 'completed' in data:
        task.completed = data['completed']
    
    # Save changes
    db.session.commit()
    
    # Return updated task
    return jsonify(task.to_dict())

# DELETE /api/tasks/<id> - Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    # Get task from database
    task = Task.query.get_or_404(task_id)
    
    # Delete task
    db.session.delete(task)
    db.session.commit()
    
    # Return success message
    return jsonify({'message': 'Task deleted successfully'}), 200

# Error Handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

# Run the application
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Start the Flask development server
    app.run(debug=True)

