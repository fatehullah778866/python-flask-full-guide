# Project 5: Simple To-Do List 📝

Welcome to Project 5! This app lets users add, complete, and delete tasks using session storage!

## What is This Project? 🤔

**Simple To-Do List** = An app to manage your tasks!

**Think of it like:**
- **Paper List** = Write tasks on paper
- **Digital List** = Same thing, but on your computer!
- **Session Storage** = Remembers your tasks (until you close browser)

**Session = Temporary storage that remembers things!**

## What You'll Learn 📚

✅ Session management in Flask
✅ Storing data in sessions
✅ List manipulation (add, remove, modify)
✅ Form handling (multiple forms)
✅ Dynamic routes with IDs
✅ CRUD operations (Create, Read, Update, Delete)
✅ Conditional rendering in templates

## What This App Does 🎯

1. **Add Tasks** - Enter task and click "Add Task"
2. **View Tasks** - See all your tasks in a list
3. **Mark Complete** - Toggle task completion status
4. **Delete Tasks** - Remove tasks from the list
5. **Session Storage** - Tasks persist during browser session

**Features:**
- ➕ Add new tasks
- ✅ Mark tasks as complete/incomplete
- 🗑️ Delete tasks
- 💾 Session-based storage
- 📱 Responsive design

## Step-by-Step Explanation 📖

### Step 1: Import Flask and session
```python
from flask import Flask, render_template, request, redirect, url_for, session
```
**What this does:**
- Gets Flask (for web app)
- Gets session (for storing data)
- Gets request (for form data)
- Gets redirect (for navigation)

**Simple explanation:**
- `session` = Temporary storage
- Like a notepad that remembers things!

### Step 2: Set Secret Key
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```
**What this does:**
- Required for sessions to work
- Encrypts session data
- Must be set!

**Simple explanation:**
- Secret key = Password for session
- Protects your data!

### Step 3: Initialize Tasks
```python
def init_tasks():
    if 'tasks' not in session:
        session['tasks'] = []
```
**What this does:**
- Checks if tasks list exists
- Creates empty list if it doesn't
- Ensures we always have a list

**Simple explanation:**
- Make sure we have a place to store tasks!

### Step 4: Home Route
```python
@app.route('/', methods=['GET'])
def index():
    init_tasks()
    tasks = session.get('tasks', [])
    return render_template('index.html', tasks=tasks)
```
**What this does:**
- Shows home page
- Gets tasks from session
- Displays them in template

**Simple explanation:**
- When someone visits `/`, show all tasks!

### Step 5: Add Task Route
```python
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task', '').strip()
    if task_text:
        new_task = {'id': len(session['tasks']), 'text': task_text, 'completed': False}
        session['tasks'].append(new_task)
        session.modified = True
    return redirect(url_for('index'))
```
**What this does:**
- Gets task text from form
- Creates task dictionary
- Adds to session
- Redirects to home

**Simple explanation:**
- Get task → Create task object → Save it → Show updated list!

### Step 6: Toggle Complete Route
```python
@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    tasks = session.get('tasks', [])
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
        session['tasks'] = tasks
        session.modified = True
    return redirect(url_for('index'))
```
**What this does:**
- Gets task by ID
- Toggles completed status
- Saves to session
- Redirects to home

**Simple explanation:**
- Find task → Flip completed status → Save → Show updated list!

### Step 7: Delete Task Route
```python
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = session.get('tasks', [])
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        session['tasks'] = tasks
        session.modified = True
    return redirect(url_for('index'))
```
**What this does:**
- Gets task by ID
- Removes from list
- Saves to session
- Redirects to home

**Simple explanation:**
- Find task → Remove it → Save → Show updated list!

## Key Concepts 🎓

### 1. Session Storage

**What is session?**
- Temporary storage in Flask
- Stores data between requests
- Persists during browser session
- Lost when browser closes

**How it works:**
```python
session['tasks'] = []  # Store data
tasks = session.get('tasks', [])  # Get data
```

**Simple explanation:**
- Session = Temporary notepad
- Stores data during visit
- Clears when you leave!

### 2. List Manipulation

**Adding items:**
```python
session['tasks'].append(new_task)
```

**Removing items:**
```python
tasks.pop(task_id)
```

**Modifying items:**
```python
tasks[task_id]['completed'] = True
```

**Simple explanation:**
- Lists = Collections of items
- Can add, remove, modify!

### 3. Dynamic Routes with IDs

**What are dynamic routes?**
- Routes with parameters
- Capture values from URL
- Use `<int:task_id>` syntax

**Example:**
```python
@app.route('/toggle/<int:task_id>')
```
- `/toggle/0` → task_id = 0
- `/toggle/1` → task_id = 1

**Simple explanation:**
- Dynamic = Changes based on URL
- ID = Which task to work with!

### 4. CRUD Operations

**Create:**
- Add new tasks
- `add_task()` function

**Read:**
- View all tasks
- `index()` function

**Update:**
- Toggle completion
- `toggle_task()` function

**Delete:**
- Remove tasks
- `delete_task()` function

**Simple explanation:**
- CRUD = Create, Read, Update, Delete
- All basic operations!

## How to Run 🚀

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**What you'll see:**
- To-do list interface
- Input field to add tasks
- List of tasks (empty at first)
- Buttons to complete/delete

**How to use:**
1. Enter task in input field
2. Click "Add Task"
3. Task appears in list
4. Click "✅ Mark Complete" to mark done
5. Click "🗑️ Delete" to remove task

## Understanding the Flow 🔄

### Complete Flow:

1. **User visits home page** (`/`)
   - Flask gets tasks from session
   - Shows them in template

2. **User adds task**
   - Fills form and submits
   - Flask creates task object
   - Adds to session
   - Redirects to home

3. **User marks task complete**
   - Clicks toggle button
   - Flask finds task by ID
   - Toggles completed status
   - Saves to session
   - Redirects to home

4. **User deletes task**
   - Clicks delete button
   - Flask finds task by ID
   - Removes from list
   - Saves to session
   - Redirects to home

**Simple explanation:**
- Add → Save → Show
- Toggle → Save → Show
- Delete → Save → Show!

## Files in This Project 📁

```
05-todo-list/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # To-do list page
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Key Differences from Previous Projects 🆚

### Project 1-3:
- No data persistence
- Each request independent

### Project 4:
- Lists and random selection
- No user input

### Project 5 (To-Do List):
- **Session storage** (data persists)
- **CRUD operations** (full functionality)
- **Multiple forms** (add, toggle, delete)
- **Dynamic routes** (with task IDs)
- **List manipulation** (add, remove, modify)

**Progress = You're building full-featured apps!**

## Common Questions ❓

### Q: What is session storage?
**A:** Temporary storage that remembers data during your browser session. Lost when you close the browser.

### Q: Why do I need secret_key?
**A:** Sessions need encryption. The secret key is used to encrypt/decrypt session data.

### Q: How long does session last?
**A:** Until you close the browser. Sessions are temporary!

### Q: Can I make tasks persist forever?
**A:** Yes! Use a database instead of session. We'll learn that later!

### Q: What if I refresh the page?
**A:** Tasks stay! Session persists across page refreshes.

## Practice Exercises 💪

### Exercise 1: Add Edit Functionality
Allow users to edit task text.

### Exercise 2: Add Due Dates
Add due date field to tasks.

### Exercise 3: Add Priorities
Add priority levels (high, medium, low).

### Exercise 4: Add Categories
Organize tasks by categories.

## Next Steps 🎯

After completing this project:

1. ✅ Try adding, completing, and deleting tasks
2. ✅ Refresh the page (tasks should stay!)
3. ✅ Close and reopen browser (tasks will be gone - that's normal!)
4. ✅ Move to Project 6: Weather Display App

## Congratulations! 🎉

You've learned:
- ✅ Session management
- ✅ List manipulation
- ✅ CRUD operations
- ✅ Dynamic routes with IDs
- ✅ Multiple form handling
- ✅ Data persistence (temporary)

**You're building full-featured web applications!** 🚀

---

**Ready for the next project? Try Project 6: Weather Display App!**

