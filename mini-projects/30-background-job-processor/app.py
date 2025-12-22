# Background Job Processor App
# This app demonstrates background job processing with Celery!

# Step 1: Import Flask and Celery Tools
# What is this? We're importing Flask and Celery tools
# Think of it like: "Get Flask tools and background job tools"
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from celery import Celery
from celery.result import AsyncResult
import time
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains request data
# - jsonify = Function to return JSON responses
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - flash = Function to show temporary messages
# - Celery = Background job processing library
# - AsyncResult = Object for tracking async task results
# - time = Module for time-related functions
# - We'll use Celery to run tasks in the background!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Flask
# What is this? Setting up Flask configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions and flash messages

# Step 4: Configure Celery
# What is this? Setting up Celery for background jobs
# Think of it like: "Tell Celery where to find Redis"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# Explanation:
# - 'CELERY_BROKER_URL' = URL for message broker (Redis)
# - 'redis://localhost:6379/0' = Redis server address
# - Redis = In-memory database used as message queue
# - Celery uses Redis to send tasks to workers
# - Workers = Separate processes that run tasks

app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# Explanation:
# - 'CELERY_RESULT_BACKEND' = Where to store task results
# - 'redis://localhost:6379/0' = Redis server address
# - Results = Output from completed tasks
# - Stored in Redis so Flask can retrieve them

# Step 5: Initialize Celery
# What is this? Creating the Celery object
# Think of it like: "Create a background job manager"
def make_celery(app):
    """
    Create and configure Celery instance
    
    Args:
    - app: Flask application instance
    
    Returns:
    - Celery instance
    """
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    # Explanation:
    # - Celery() = Creates Celery instance
    # - app.import_name = Name of Flask app
    # - broker = Message broker (Redis) for sending tasks
    # - backend = Result backend (Redis) for storing results
    # - celery = Our background job manager
    
    celery.conf.update(app.config)
    # Explanation:
    # - celery.conf.update() = Updates Celery config with Flask config
    # - This syncs settings between Flask and Celery
    
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
        # Explanation:
        # - ContextTask = Custom task class
        # - __call__ = Method called when task runs
        # - app.app_context() = Flask application context
        # - This allows tasks to access Flask features
    
    celery.Task = ContextTask
    # Explanation:
    # - celery.Task = Sets custom task class
    # - All tasks now use ContextTask
    # - This ensures Flask context is available
    
    return celery
    # Explanation:
    # - return celery = Returns configured Celery instance
    # - This is our background job processor!

# Step 6: Create Celery Instance
# What is this? Creating the actual Celery object
celery = make_celery(app)
# Explanation:
# - make_celery(app) = Creates Celery instance
# - celery = Our background job processor
# - This handles all background tasks!

# Step 7: Import Tasks
# What is this? Importing task definitions
# Note: We'll define tasks in tasks.py, but for simplicity, we'll define them here
# In production, put tasks in a separate tasks.py file

# Step 8: Define Background Task - Long Running Task
# What is this? A task that runs in the background
@celery.task(name='app.long_running_task')
# Explanation:
# - @celery.task = Decorator that makes function a Celery task
# - name='app.long_running_task' = Unique task name
# - This function can now run in the background!

def long_running_task(duration=10):
    """
    Simulates a long-running task (like processing data or sending emails)
    
    Args:
    - duration: How long the task should run (in seconds)
    
    Returns:
    - Dictionary with task result
    """
    # Step 9: Simulate Long-Running Work
    # What is this? Doing work that takes time
    for i in range(duration):
        time.sleep(1)
        # Explanation:
        # - time.sleep(1) = Pause for 1 second
        # - This simulates work being done
        # - In real apps, this could be:
        #   - Processing large files
        #   - Sending emails
        #   - Generating reports
        #   - Any time-consuming operation
        
        # Update task state (optional, for progress tracking)
        long_running_task.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': duration, 'status': f'Processing step {i + 1}...'}
        )
        # Explanation:
        # - update_state() = Updates task status
        # - state='PROGRESS' = Task is in progress
        # - meta = Additional information (progress, status)
        # - This allows tracking task progress!
    
    # Step 10: Return Result
    # What is this? Returning the task result
    return {
        'status': 'Task completed successfully!',
        'duration': duration,
        'completed_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    # Explanation:
    # - return = Returns task result
    # - This dictionary is stored in Redis
    # - Flask can retrieve it using task ID
    # - Result includes status, duration, and completion time

# Step 11: Define Background Task - Send Email (Simulated)
# What is this? A task that sends emails in the background
@celery.task(name='app.send_email_task')
# Explanation:
# - @celery.task = Decorator that makes function a Celery task
# - name='app.send_email_task' = Unique task name
# - This simulates sending emails!

def send_email_task(to_email, subject, message):
    """
    Simulates sending an email (in real app, would use Flask-Mail or similar)
    
    Args:
    - to_email: Recipient email address
    - subject: Email subject
    - message: Email message
    
    Returns:
    - Dictionary with email result
    """
    # Step 12: Simulate Email Sending
    # What is this? Simulating email sending
    time.sleep(3)
    # Explanation:
    # - time.sleep(3) = Pause for 3 seconds
    # - This simulates time to send email
    # - In real apps, this would use Flask-Mail or SMTP
    
    return {
        'status': 'Email sent successfully!',
        'to': to_email,
        'subject': subject,
        'sent_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    # Explanation:
    # - return = Returns email result
    # - Includes recipient, subject, and sent time
    # - In real apps, this confirms email was sent

# Step 13: Create Home Route (GET)
# What is this? The main page
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows job submission forms and job status
    """
    return render_template('index.html')
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = The template file to display
    # - Shows forms for submitting jobs

# Step 14: Create Submit Long Task Route (POST)
# What is this? Route to submit a long-running task
@app.route('/submit-task', methods=['POST'])
def submit_task():
    """
    This function submits a long-running task to Celery
    It returns immediately with a task ID
    """
    # Step 15: Get Task Duration
    # What is this? Getting how long the task should run
    duration = int(request.form.get('duration', 10))
    # Explanation:
    # - request.form.get('duration', 10) = Gets duration from form
    # - int() = Converts to integer
    # - 10 = Default value if not provided
    # - duration = How long task should run (in seconds)
    
    # Step 16: Submit Task to Celery
    # What is this? Sending task to background worker
    task = long_running_task.delay(duration)
    # Explanation:
    # - long_running_task.delay(duration) = Submits task to Celery
    # - .delay() = Runs task asynchronously (in background)
    # - task = AsyncResult object with task ID
    # - This returns immediately! Task runs in background!
    # - Flask doesn't wait for task to complete
    
    flash(f'Task submitted! Task ID: {task.id}', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - task.id = Unique task ID
    # - 'success' = Message category
    # - User sees task ID immediately
    
    return redirect(url_for('task_status', task_id=task.id))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('task_status', task_id=task.id) = Generates URL
    # - User is sent to task status page
    # - They can check if task is complete!

# Step 17: Create Submit Email Route (POST)
# What is this? Route to submit an email task
@app.route('/submit-email', methods=['POST'])
def submit_email():
    """
    This function submits an email task to Celery
    Email is sent in the background
    """
    # Step 18: Get Email Data
    # What is this? Getting email information from form
    to_email = request.form.get('to_email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    # Explanation:
    # - request.form.get() = Gets form data
    # - to_email, subject, message = Email information
    # - These are the email details
    
    # Step 19: Submit Email Task to Celery
    # What is this? Sending email task to background worker
    task = send_email_task.delay(to_email, subject, message)
    # Explanation:
    # - send_email_task.delay() = Submits email task to Celery
    # - .delay() = Runs task asynchronously (in background)
    # - task = AsyncResult object with task ID
    # - Email is sent in background!
    # - Flask doesn't wait for email to send
    
    flash(f'Email task submitted! Task ID: {task.id}', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - task.id = Unique task ID
    # - User sees confirmation immediately
    
    return redirect(url_for('task_status', task_id=task.id))
    # Explanation:
    # - redirect = Sends user to task status page
    # - User can check if email was sent

# Step 20: Create Task Status Route (GET)
# What is this? Route to check task status
@app.route('/task/<task_id>')
def task_status(task_id):
    """
    This function checks the status of a task
    It shows if task is pending, in progress, or completed
    """
    # Step 21: Get Task Result
    # What is this? Getting task information from Celery
    task_result = AsyncResult(task_id, app=celery)
    # Explanation:
    # - AsyncResult(task_id, app=celery) = Gets task result object
    # - task_id = The task ID we got when submitting
    # - app=celery = Celery instance
    # - task_result = Object with task information
    
    # Step 22: Get Task State
    # What is this? Getting current task state
    if task_result.state == 'PENDING':
        # Explanation:
        # - task_result.state = Current task state
        # - 'PENDING' = Task is waiting to start
        # - Only proceed if task is pending
        
        response = {
            'state': task_result.state,
            'status': 'Task is waiting to start...'
        }
        # Explanation:
        # - response = Dictionary with task info
        # - 'state' = Current state
        # - 'status' = Human-readable status
    
    elif task_result.state == 'PROGRESS':
        # Explanation:
        # - 'PROGRESS' = Task is running
        # - Only proceed if task is in progress
        
        response = {
            'state': task_result.state,
            'status': task_result.info.get('status', 'Task is running...'),
            'current': task_result.info.get('current', 0),
            'total': task_result.info.get('total', 0)
        }
        # Explanation:
        # - response = Dictionary with task info
        # - task_result.info = Additional information (from update_state)
        # - 'current' = Current progress
        # - 'total' = Total steps
        # - This shows progress!
    
    elif task_result.state == 'SUCCESS':
        # Explanation:
        # - 'SUCCESS' = Task completed successfully
        # - Only proceed if task succeeded
        
        response = {
            'state': task_result.state,
            'status': 'Task completed successfully!',
            'result': task_result.result
        }
        # Explanation:
        # - response = Dictionary with task info
        # - task_result.result = Task result (return value)
        # - This is what the task returned!
    
    else:
        # Explanation:
        # - else = Task failed or other state
        # - Only proceed if task is in other state
        
        response = {
            'state': task_result.state,
            'status': str(task_result.info)
        }
        # Explanation:
        # - response = Dictionary with task info
        # - task_result.info = Error information
        # - This shows what went wrong
    
    return render_template('task_status.html', task_id=task_id, task=response)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'task_status.html' = Template for showing task status
    # - task_id=task_id = Passes task ID to template
    # - task=response = Passes task information to template
    # - User can see task progress!

# Step 23: Create Task Status API Route (GET)
# What is this? API endpoint to check task status (for AJAX)
@app.route('/api/task/<task_id>')
def task_status_api(task_id):
    """
    This function returns task status as JSON
    Useful for AJAX requests to check status without page reload
    """
    # Step 24: Get Task Result
    # What is this? Getting task information
    task_result = AsyncResult(task_id, app=celery)
    # Explanation:
    # - AsyncResult() = Gets task result object
    # - task_result = Object with task information
    
    # Step 25: Build Response
    # What is this? Creating JSON response
    if task_result.state == 'PENDING':
        response = {
            'state': task_result.state,
            'status': 'Task is waiting to start...'
        }
    elif task_result.state == 'PROGRESS':
        response = {
            'state': task_result.state,
            'status': task_result.info.get('status', 'Task is running...'),
            'current': task_result.info.get('current', 0),
            'total': task_result.info.get('total', 0)
        }
    elif task_result.state == 'SUCCESS':
        response = {
            'state': task_result.state,
            'status': 'Task completed successfully!',
            'result': task_result.result
        }
    else:
        response = {
            'state': task_result.state,
            'status': str(task_result.info)
        }
    # Explanation:
    # - Same logic as task_status route
    # - But returns JSON instead of HTML
    # - Useful for AJAX polling
    
    return jsonify(response)
    # Explanation:
    # - jsonify() = Returns JSON response
    # - response = Task information
    # - Client can check status programmatically

# Step 26: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)
    # - Note: You also need to run Celery worker separately!
    # - Command: celery -A app.celery worker --loglevel=info

