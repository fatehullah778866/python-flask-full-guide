# Lesson 10.2: Background Tasks - Doing Work Without Waiting! ⏳

## What are Background Tasks? 🤔

**Background Tasks** = Work that happens without making users wait!

Think of it like:
- **Normal Task** = You wait in line at store (boring!)
- **Background Task** = Store sends package later (you go home!)
- **You** = Don't have to wait!

**Background Tasks = Work that happens in the background!**

## Why Do We Need Background Tasks? 🎯

### The Problem Without Background Tasks:

```
User clicks "Send Email"
    ↓
App sends email (takes 10 seconds!)
    ↓
User waits... 😴
    ↓
Finally done!
```

**User has to wait! Bad experience!**

### The Solution: Background Tasks

```
User clicks "Send Email"
    ↓
App says "Email queued!" ✅
    ↓
User can continue using app! 🎉
    ↓
Email sends in background (user doesn't wait!)
```

**User doesn't wait! Great experience!**

## When to Use Background Tasks 📋

### Use Background Tasks For:

1. **Sending Emails** - Takes time, user doesn't need to wait
2. **Processing Images** - Resizing, filtering
3. **Generating Reports** - Long calculations
4. **Scheduled Tasks** - Run at specific times
5. **API Calls** - External services

**Anything that takes time = Background task!**

## Celery - Task Queue System 🥬

### What is Celery?

**Celery** = System for running background tasks

Think of it like:
- **Celery** = Worker who does jobs
- **Tasks** = Jobs to do
- **Queue** = List of jobs waiting
- **You** = Give jobs to worker

**Celery = Worker system for background tasks!**

### How Celery Works:

```
Your App
    ↓
Creates Task
    ↓
Sends to Queue (Redis/RabbitMQ)
    ↓
Celery Worker
    ↓
Gets Task from Queue
    ↓
Does the Work
    ↓
Saves Result
```

**Celery = Separate worker does the job!**

## Setting Up Celery 🔧

### Step 1: Install Celery

```bash
pip install celery redis
```

### Step 2: Install Redis (Message Broker)

**Redis** = Stores tasks in queue

```bash
# Windows: Download from redis.io or use Docker
docker run -d -p 6379:6379 redis

# Linux/Mac
sudo apt-get install redis-server
# or
brew install redis
```

### Step 3: Create Celery App

**Create `celery_app.py`:**
```python
from celery import Celery

# Create Celery app
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # Where tasks are stored
    backend='redis://localhost:6379/0'   # Where results are stored
)

# Define a task
@celery.task
def send_email(to, subject, body):
    """Send email - runs in background"""
    # Simulate sending email
    import time
    time.sleep(5)  # Takes 5 seconds
    print(f"Email sent to {to}: {subject}")
    return f"Email sent to {to}"
```

### Step 4: Start Celery Worker

```bash
celery -A celery_app worker --loglevel=info
```

**Worker is now running and ready for tasks!**

## Using Celery with Flask 🚀

### Complete Example:

**`app.py`:**
```python
from flask import Flask, request, jsonify
from celery_app import celery, send_email

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email_route():
    to = request.json.get('to')
    subject = request.json.get('subject')
    body = request.json.get('body')
    
    # Send task to Celery (returns immediately!)
    task = send_email.delay(to, subject, body)
    
    return jsonify({
        'message': 'Email queued!',
        'task_id': task.id
    }), 202  # 202 = Accepted (processing)

@app.route('/task-status/<task_id>')
def task_status(task_id):
    """Check if task is done"""
    task = send_email.AsyncResult(task_id)
    
    if task.ready():
        return jsonify({
            'status': 'completed',
            'result': task.result
        })
    else:
        return jsonify({
            'status': 'pending'
        })

if __name__ == '__main__':
    app.run(debug=True)
```

**User gets response immediately! Task runs in background!**

## Task Types 📦

### 1. Fire and Forget

```python
@celery.task
def log_event(event):
    """Log event - don't need result"""
    print(f"Event: {event}")

# Use it
log_event.delay("User logged in")
```

**Fire and forget = Don't wait for result!**

### 2. Get Result Later

```python
@celery.task
def process_image(image_path):
    """Process image - get result later"""
    # Process image...
    return "processed_image.jpg"

# Start task
task = process_image.delay("photo.jpg")

# Check later
if task.ready():
    result = task.result
```

**Get result later = Check when done!**

### 3. Scheduled Tasks

```python
from celery.schedules import crontab

@celery.task
def daily_report():
    """Generate daily report"""
    print("Generating daily report...")
    return "Report generated"

# Schedule task (runs every day at midnight)
celery.conf.beat_schedule = {
    'daily-report': {
        'task': 'celery_app.daily_report',
        'schedule': crontab(hour=0, minute=0),  # Midnight
    },
}
```

**Scheduled = Runs automatically at specific times!**

## Flask-Celery Integration 🎯

### Better Integration:

**`celery_app.py`:**
```python
from celery import Celery

def make_celery(app):
    """Create Celery app from Flask app"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery
```

**`app.py`:**
```python
from flask import Flask
from celery_app import make_celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = make_celery(app)

@celery.task
def send_email(to, subject, body):
    # Can use Flask app context here!
    from flask_mail import Message, Mail
    mail = Mail(app)
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)
    return "Email sent!"
```

**Better integration = Can use Flask features in tasks!**

## Real-World Examples 🌍

### Example 1: Send Welcome Email

```python
@celery.task
def send_welcome_email(user_id):
    """Send welcome email to new user"""
    from flask import current_app
    from flask_mail import Message, Mail
    
    user = User.query.get(user_id)
    mail = Mail(current_app)
    
    msg = Message(
        'Welcome!',
        recipients=[user.email],
        body=f'Welcome {user.name}!'
    )
    mail.send(msg)
    return f"Welcome email sent to {user.email}"

# In your registration route
@app.route('/register', methods=['POST'])
def register():
    # Create user
    user = User(name=request.form.get('name'))
    db.session.add(user)
    db.session.commit()
    
    # Send email in background
    send_welcome_email.delay(user.id)
    
    return "Registration successful! Check your email!"
```

### Example 2: Process Image Upload

```python
@celery.task
def process_image(image_path):
    """Resize and optimize image"""
    from PIL import Image
    import os
    
    # Open image
    img = Image.open(image_path)
    
    # Resize
    img.thumbnail((800, 800))
    
    # Save
    output_path = image_path.replace('.jpg', '_thumb.jpg')
    img.save(output_path)
    
    return output_path

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = f'uploads/{file.filename}'
    file.save(file_path)
    
    # Process in background
    task = process_image.delay(file_path)
    
    return jsonify({
        'message': 'Image uploaded, processing...',
        'task_id': task.id
    })
```

### Example 3: Scheduled Cleanup

```python
@celery.task
def cleanup_old_files():
    """Delete files older than 30 days"""
    import os
    from datetime import datetime, timedelta
    
    cutoff = datetime.now() - timedelta(days=30)
    deleted = 0
    
    for file in os.listdir('uploads'):
        file_path = os.path.join('uploads', file)
        if os.path.getmtime(file_path) < cutoff.timestamp():
            os.remove(file_path)
            deleted += 1
    
    return f"Deleted {deleted} old files"

# Schedule to run daily
celery.conf.beat_schedule = {
    'cleanup-files': {
        'task': 'celery_app.cleanup_old_files',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
}
```

## Running Celery 🏃

### Start Worker:

```bash
celery -A celery_app worker --loglevel=info
```

### Start Beat (for scheduled tasks):

```bash
celery -A celery_app beat --loglevel=info
```

### Start Both (development):

```bash
celery -A celery_app worker --beat --loglevel=info
```

## Monitoring Tasks 📊

### Check Task Status:

```python
from celery.result import AsyncResult

task = send_email.delay("user@example.com", "Hello", "Body")
task_id = task.id

# Later, check status
result = AsyncResult(task_id, app=celery)
if result.ready():
    print(result.result)  # Task result
else:
    print("Still processing...")
```

### Task States:

- **PENDING** - Waiting to start
- **STARTED** - Currently running
- **SUCCESS** - Completed successfully
- **FAILURE** - Failed with error
- **RETRY** - Retrying after failure

## Best Practices ✨

### 1. Keep Tasks Small

```python
# ✅ Good - small, focused task
@celery.task
def send_email(to, subject, body):
    pass

# ❌ Bad - too much in one task
@celery.task
def do_everything():
    # Too many things!
    pass
```

### 2. Handle Errors

```python
@celery.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    try:
        # Send email
        pass
    except Exception as exc:
        # Retry on failure
        raise self.retry(exc=exc, countdown=60)
```

### 3. Use Appropriate Timeouts

```python
@celery.task(time_limit=300)  # 5 minute timeout
def long_task():
    pass
```

## What You Learned! 📚

✅ What background tasks are  
✅ Why we need them  
✅ When to use them  
✅ What Celery is  
✅ How to set up Celery  
✅ Using Celery with Flask  
✅ Task types  
✅ Real-world examples  
✅ Monitoring tasks  
✅ Best practices  

## Key Concepts 💡

1. **Background Tasks** = Work without waiting
2. **Celery** = Task queue system
3. **Redis** = Message broker
4. **Worker** = Does the tasks
5. **Queue** = List of tasks
6. **Scheduled Tasks** = Run at specific times

## What's Next? 🚀

Now that you know background tasks, let's learn about **WebSockets** - real-time communication!

---

**Excellent! Your apps can now do work in the background! 🎉**

