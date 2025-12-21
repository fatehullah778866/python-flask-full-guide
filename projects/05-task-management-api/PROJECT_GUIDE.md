# Complete Guide: Building a Task Management API 📚

## Welcome! 👋

This guide will teach you EVERYTHING about building RESTful APIs. We'll learn about APIs, REST, JSON, and HTTP methods step by step!

## Part 1: Understanding APIs 🌐

### What is an API?

**API** = Application Programming Interface

Think of it like:
- **API** = A menu at a restaurant
- **Menu** = Lists what you can order
- **You order** = Make a request
- **Food comes** = Get response
- **No need to cook** = API does the work!

**API = A way to get data or do things without seeing the code!**

### Why Do We Need APIs?

**Without API:**
- Programs can't talk to each other
- Can't share data
- Each app is isolated

**With API:**
- Programs can communicate
- Share data easily
- Build mobile apps, web apps, etc.

**API = Enables communication between programs!**

## Part 2: Understanding REST 🎯

### What is REST?

**REST** = Representational State Transfer

Think of it like:
- **REST** = Rules for how APIs should work
- **Like grammar** = Rules for language
- **Everyone follows** = Makes APIs consistent
- **Easy to understand** = Standard way

**REST = Rules for building APIs!**

### REST Principles:

1. **Use HTTP Methods** - GET, POST, PUT, DELETE
2. **Use URLs** - Different URLs for different things
3. **Return JSON** - Data in JSON format
4. **Stateless** - Each request is independent

**REST = Simple and standard!**

## Part 3: Understanding HTTP Methods 📡

### What are HTTP Methods?

**HTTP Methods** = Different types of requests

Think of it like:
- **GET** = "Give me that" (reading)
- **POST** = "Here's something new" (creating)
- **PUT** = "Change this" (updating)
- **DELETE** = "Remove this" (deleting)

**HTTP Methods = Different actions you can do!**

### HTTP Methods Explained:

#### GET - Read Data
```
GET /tasks
= "Give me all tasks"
```

#### POST - Create Data
```
POST /tasks
= "Create a new task"
```

#### PUT - Update Data
```
PUT /tasks/1
= "Update task number 1"
```

#### DELETE - Delete Data
```
DELETE /tasks/1
= "Delete task number 1"
```

**Each method = Different action!**

## Part 4: Understanding JSON 📄

### What is JSON?

**JSON** = JavaScript Object Notation

Think of it like:
- **JSON** = A way to write data
- **Like a list** = Organized information
- **Easy to read** = Both humans and computers
- **Standard format** = Everyone uses it

**JSON = Standard way to send data!**

### JSON Example:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false
}
```

**JSON = Organized data in key-value pairs!**

## Part 5: Creating the API Structure 🏗️

### Basic API Setup:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

**Setup = Prepare Flask for API!**

## Part 6: Creating the Task Model 📝

### Task Model:

```python
class Task(db.Model):
    """Task Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert task to dictionary (for JSON)"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'date_created': self.date_created.isoformat()
        }
```

**Model = Structure for tasks!**

## Part 7: Creating API Endpoints 🛣️

### Endpoint 1: GET All Tasks

```python
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])
```

**What's happening:**
1. **Route** = `/api/tasks`
2. **Method** = GET
3. **Get tasks** = From database
4. **Convert to JSON** = Return as JSON

**GET = Read all tasks!**

### Endpoint 2: GET Single Task

```python
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())
```

**GET = Read one task!**

### Endpoint 3: POST Create Task

```python
@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()  # Get JSON data from request
    
    # Validate
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Create task
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201  # 201 = Created
```

**POST = Create new task!**

### Endpoint 4: PUT Update Task

```python
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    
    db.session.commit()
    return jsonify(task.to_dict())
```

**PUT = Update existing task!**

### Endpoint 5: DELETE Task

```python
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200
```

**DELETE = Remove task!**

## Part 8: Error Handling ⚠️

### Handling Errors:

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

**Error Handling = Return proper error messages!**

## Part 9: Complete app.py 🎯

### Full API Code:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'date_created': self.date_created.isoformat()
        }

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# GET single task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

# POST create task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )
    
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# PUT update task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    
    db.session.commit()
    return jsonify(task.to_dict())

# DELETE task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

## Part 10: Testing the API 🧪

### Using curl (Command Line):

```bash
# GET all tasks
curl http://localhost:5000/api/tasks

# GET single task
curl http://localhost:5000/api/tasks/1

# POST create task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description"}'

# PUT update task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# DELETE task
curl -X DELETE http://localhost:5000/api/tasks/1
```

### Using Python requests:

```python
import requests

# GET all tasks
response = requests.get('http://localhost:5000/api/tasks')
print(response.json())

# POST create task
response = requests.post('http://localhost:5000/api/tasks', json={
    'title': 'New Task',
    'description': 'Task description'
})
print(response.json())
```

## What You've Learned! 🎓

✅ What APIs are  
✅ What REST is  
✅ HTTP methods (GET, POST, PUT, DELETE)  
✅ JSON format  
✅ How to create API endpoints  
✅ How to handle requests  
✅ How to return JSON responses  
✅ Error handling  

## Next Steps 🚀

1. **Test API** - Use Postman or curl
2. **Add authentication** - Protect your API
3. **Add pagination** - For many tasks
4. **Add filtering** - Filter by completed, etc.

---

**Congratulations! You built a RESTful API! 🎉**

