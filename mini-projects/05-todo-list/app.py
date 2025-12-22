# Simple To-Do List App
# This app lets users add, complete, and delete tasks using session storage!

# Step 1: Import Flask and session
# What is this? We're importing Flask and session object
# Think of it like: "Get Flask tools and session storage"
from flask import Flask, render_template, request, redirect, url_for, session
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - session = Object for storing data between requests
# - session = Like a temporary storage that remembers things!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Set Secret Key for Sessions
# What is this? A secret key needed for session security
# Think of it like: "A password to protect session data"
app.secret_key = 'your-secret-key-change-this-in-production'
# Explanation:
# - secret_key = Required for sessions to work
# - Sessions need encryption, and this key is used for that
# - In production, use a random, secure key
# - This is like a password that protects your session data

# Step 4: Initialize Tasks List in Session
# What is this? Helper function to set up tasks list
# Think of it like: "Make sure we have a place to store tasks"
def init_tasks():
    """
    Initialize tasks list in session if it doesn't exist
    This ensures we always have a tasks list to work with
    """
    if 'tasks' not in session:
        # Explanation:
        # - 'tasks' not in session = Check if 'tasks' key doesn't exist
        # - session = Dictionary-like object for storing data
        # - If tasks list doesn't exist, create it
        
        session['tasks'] = []
        # Explanation:
        # - session['tasks'] = Create 'tasks' key in session
        # - [] = Empty list to store tasks
        # - This list will hold all our tasks
        # - Each task will be a dictionary with 'text' and 'completed' keys

# Step 5: Create Home Route (GET)
# What is this? The main page that shows all tasks
# Think of it like: "When someone visits the home page, show the to-do list"
@app.route('/', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - methods=['GET'] = Only accepts GET requests (viewing page)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows all tasks from the session
    """
    # Step 6: Initialize Tasks
    # What is this? Make sure tasks list exists
    init_tasks()
    # Explanation:
    # - Calls our helper function
    # - Ensures session['tasks'] exists
    # - If it doesn't exist, creates empty list
    
    # Step 7: Get Tasks from Session
    # What is this? Getting all tasks from session storage
    tasks = session.get('tasks', [])
    # Explanation:
    # - session.get('tasks', []) = Get 'tasks' from session
    # - If 'tasks' doesn't exist, return empty list []
    # - tasks = Variable to hold all tasks
    # - This is a list of dictionaries, each representing a task
    
    # Step 8: Render Template with Tasks
    # What is this? Showing the HTML page with all tasks
    return render_template('index.html', tasks=tasks)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - tasks=tasks = Passes the tasks list to the template
    # - The first 'tasks' = Variable name in the template
    # - The second tasks = The actual tasks list from Python
    # - In the template, we can use tasks to display them

# Step 9: Create Add Task Route (POST)
# What is this? Handles adding a new task
# Think of it like: "When user submits form to add task, do this"
@app.route('/add', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/add' = The URL for adding tasks
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/add', Flask will run the function below

def add_task():
    """
    This function runs when a task is added
    It gets the task text from the form and adds it to the session
    """
    # Step 10: Initialize Tasks
    # What is this? Make sure tasks list exists
    init_tasks()
    # Explanation:
    # - Ensures session['tasks'] exists before we use it
    
    # Step 11: Get Task Text from Form
    # What is this? Getting the task text the user entered
    task_text = request.form.get('task', '').strip()
    # Explanation:
    # - request.form.get('task', '') = Gets value of input named 'task'
    # - If 'task' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - task_text = Variable to hold the task text
    # - Example: User enters "  Buy milk  " → becomes "Buy milk"
    
    # Step 12: Validate Task Text
    # What is this? Checking if user actually entered something
    if task_text:
        # Explanation:
        # - if task_text = If task_text is not empty
        # - Empty strings are "falsy" in Python
        # - Only add task if user entered something
        
        # Step 13: Create Task Dictionary
        # What is this? Creating a task object to store
        new_task = {
            'id': len(session['tasks']),
            # Explanation:
            # - 'id' = Unique identifier for the task
            # - len(session['tasks']) = Number of tasks currently in list
            # - This gives each task a unique ID (0, 1, 2, 3, ...)
            # - We'll use this ID to find and delete tasks later
            
            'text': task_text,
            # Explanation:
            # - 'text' = The actual task text
            # - task_text = What the user entered
            # - This is what will be displayed
            
            'completed': False
            # Explanation:
            # - 'completed' = Whether task is done or not
            # - False = Task is not completed yet
            # - When user marks it complete, we'll change this to True
        }
        
        # Step 14: Add Task to Session
        # What is this? Adding the new task to our tasks list
        session['tasks'].append(new_task)
        # Explanation:
        # - session['tasks'] = The list of tasks in session
        # - .append(new_task) = Adds new_task to the end of the list
        # - Now the task is stored in session
        # - It will persist until session ends or we delete it
        
        # Step 15: Save Session
        # What is this? Making sure session changes are saved
        session.modified = True
        # Explanation:
        # - session.modified = True = Tells Flask session was changed
        # - Flask only saves session if it detects changes
        # - Sometimes Flask doesn't detect list modifications
        # - Setting this to True forces Flask to save the session
        # - Important! Without this, changes might not be saved
    
    # Step 16: Redirect to Home Page
    # What is this? Sending user back to home page after adding task
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Function that sends user to another page
    # - url_for('index') = Generates URL for 'index' route (home page)
    # - After adding task, user is sent back to home page
    # - Home page will now show the new task

# Step 17: Create Toggle Complete Route
# What is this? Handles marking task as complete or incomplete
# Think of it like: "When user clicks complete button, toggle the status"
@app.route('/toggle/<int:task_id>', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/toggle/<int:task_id>' = Dynamic route with task ID
# - <int:task_id> = Captures task ID from URL (must be integer)
# - Example: /toggle/0 → task_id = 0
# - methods=['POST'] = Only accepts POST requests
# - When form is submitted to '/toggle/0', Flask will run the function below

def toggle_task(task_id):
    """
    This function runs when a task's complete status is toggled
    It changes the completed status of the task
    """
    # Step 18: Initialize Tasks
    # What is this? Make sure tasks list exists
    init_tasks()
    # Explanation:
    # - Ensures session['tasks'] exists
    
    # Step 19: Find and Toggle Task
    # What is this? Finding the task and changing its status
    tasks = session.get('tasks', [])
    # Explanation:
    # - Gets all tasks from session
    # - tasks = List of task dictionaries
    
    if 0 <= task_id < len(tasks):
        # Explanation:
        # - Checks if task_id is valid
        # - 0 <= task_id = task_id is 0 or greater
        # - task_id < len(tasks) = task_id is less than number of tasks
        # - This prevents errors if task_id doesn't exist
        # - Example: If we have 3 tasks (0, 1, 2), task_id must be 0, 1, or 2
        
        # Step 20: Toggle Completed Status
        # What is this? Changing the completed status
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
        # Explanation:
        # - tasks[task_id] = Gets the task at that index
        # - ['completed'] = Accesses the 'completed' field
        # - not = Logical NOT operator (flips True/False)
        # - If completed is True, becomes False
        # - If completed is False, becomes True
        # - This toggles the status!
        
        # Step 21: Save Session
        # What is this? Making sure session changes are saved
        session['tasks'] = tasks
        # Explanation:
        # - Updates session with modified tasks list
        # - session['tasks'] = The tasks list in session
        # - tasks = Our modified list
        # - This saves the changes
        
        session.modified = True
        # Explanation:
        # - Forces Flask to save the session
        # - Important for persistence
    
    # Step 22: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - After toggling, user is sent back to home page
    # - Home page will show updated task status

# Step 23: Create Delete Task Route
# What is this? Handles deleting a task
# Think of it like: "When user clicks delete button, remove the task"
@app.route('/delete/<int:task_id>', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/delete/<int:task_id>' = Dynamic route with task ID
# - <int:task_id> = Captures task ID from URL
# - Example: /delete/0 → task_id = 0
# - methods=['POST'] = Only accepts POST requests
# - When form is submitted to '/delete/0', Flask will run the function below

def delete_task(task_id):
    """
    This function runs when a task is deleted
    It removes the task from the session
    """
    # Step 24: Initialize Tasks
    # What is this? Make sure tasks list exists
    init_tasks()
    # Explanation:
    # - Ensures session['tasks'] exists
    
    # Step 25: Get Tasks and Delete
    # What is this? Getting tasks and removing the specified one
    tasks = session.get('tasks', [])
    # Explanation:
    # - Gets all tasks from session
    
    if 0 <= task_id < len(tasks):
        # Explanation:
        # - Checks if task_id is valid
        # - Prevents errors if task_id doesn't exist
        
        # Step 26: Remove Task from List
        # What is this? Deleting the task from the list
        tasks.pop(task_id)
        # Explanation:
        # - .pop(task_id) = Removes item at index task_id
        # - Also returns the removed item (but we don't need it)
        # - Example: tasks = [task0, task1, task2]
        # - tasks.pop(1) removes task1
        # - Now tasks = [task0, task2]
        # - Note: IDs of remaining tasks don't change, but indices do!
        
        # Step 27: Update IDs (Optional but Good Practice)
        # What is this? Updating task IDs to be sequential
        for i, task in enumerate(tasks):
            # Explanation:
            # - enumerate(tasks) = Gets both index and task
            # - i = Index (0, 1, 2, ...)
            # - task = The task dictionary
            # - Loop through all remaining tasks
            
            task['id'] = i
            # Explanation:
            # - Updates each task's ID to match its new index
            # - After deletion, IDs are 0, 1, 2, ... again
            # - This keeps IDs sequential and correct
        
        # Step 28: Save Session
        # What is this? Making sure session changes are saved
        session['tasks'] = tasks
        # Explanation:
        # - Updates session with modified tasks list
        # - The deleted task is now gone from session
        
        session.modified = True
        # Explanation:
        # - Forces Flask to save the session
    
    # Step 29: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - After deleting, user is sent back to home page
    # - Home page will show updated task list (without deleted task)

# Step 30: Run the Application
# What is this? This starts the web server
# Think of it like: "Turn on the website so people can visit it"
if __name__ == '__main__':
    # Explanation:
    # - if __name__ == '__main__' = Only run this if we run the file directly
    # - This prevents it from running if we import this file elsewhere
    
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)
    # - When you run this, you'll see: "Running on http://127.0.0.1:5000"
    # - You can then visit that address in your browser!

