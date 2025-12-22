# Task Management with Teams App
# This app allows users to create teams, assign tasks, and collaborate!

# Step 1: Import Flask and Database Tools
# What is this? We're importing Flask and database tools
# Think of it like: "Get Flask tools and database tools"
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - flash = Function to show messages to users
# - session = Object for storing data between requests
# - SQLAlchemy = Database toolkit
# - datetime = Module for working with dates and times
# - generate_password_hash = Function to hash passwords securely
# - check_password_hash = Function to verify password hashes
# - We'll use SQLAlchemy to store teams, tasks, and team members!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Database
# What is this? Setting up where to store our database
# Think of it like: "Tell Flask where to save our data"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_management.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///task_management.db' = SQLite database file
# - SQLite = Simple database that stores data in a file
# - task_management.db = The file where our data will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions and flash messages to work

# Step 4: Initialize Database
# What is this? Creating the database object
# Think of it like: "Create a database manager"
db = SQLAlchemy(app)
# Explanation:
# - SQLAlchemy(app) = Creates database object
# - db = Our database manager
# - We'll use this to create tables and save data

# Step 5: Association Table for Team Members
# What is this? A table that connects users to teams
# Think of it like: "A table that says 'User X is in Team Y'"
team_members = db.Table('team_members',
    # Explanation:
    # - db.Table = Creates association table (many-to-many relationship)
    # - 'team_members' = Name of the table
    # - This table connects users to teams
    
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    # Explanation:
    # - 'user_id' = Column for user ID
    # - db.Integer = Data type (whole number)
    # - db.ForeignKey('users.id') = Links to users table
    # - primary_key=True = Part of primary key (with team_id)
    
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    # Explanation:
    # - 'team_id' = Column for team ID
    # - db.Integer = Data type (whole number)
    # - db.ForeignKey('teams.id') = Links to teams table
    # - primary_key=True = Part of primary key (with user_id)
    
    db.Column('date_joined', db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - 'date_joined' = When user joined the team
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
)
# Explanation:
# - This creates a many-to-many relationship
# - One user can be in many teams
# - One team can have many users
# - Example: User 1 is in Team 1 and Team 2

# Step 6: Create User Model
# What is this? Defining what a user looks like
class User(db.Model):
    """
    User Model
    This defines the structure of a user in the database
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Explanation:
    # - username = User's username
    # - db.String(80) = Text field, max 80 characters
    # - unique=True = No two users can have the same username
    # - nullable=False = This field is required
    
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Explanation:
    # - email = User's email address
    # - db.String(120) = Text field, max 120 characters
    # - unique=True = No two users can have the same email
    # - nullable=False = This field is required
    
    password_hash = db.Column(db.String(255), nullable=False)
    # Explanation:
    # - password_hash = Hashed password (not plain text!)
    # - db.String(255) = Text field for hash
    # - nullable=False = This field is required
    
    # Step 7: Define Relationships
    # What is this? Creating relationships to other tables
    
    teams = db.relationship('Team', secondary=team_members, backref='members', lazy='dynamic')
    # Explanation:
    # - teams = Relationship to Team model
    # - secondary=team_members = Uses team_members table for relationship
    # - backref='members' = Creates 'members' attribute on Team
    # - lazy='dynamic' = Returns query object instead of list
    # - This means: user.teams gives all teams this user is in
    
    created_tasks = db.relationship('Task', foreign_keys='Task.creator_id', backref='creator', lazy=True)
    # Explanation:
    # - created_tasks = Tasks created by this user
    # - foreign_keys='Task.creator_id' = Uses creator_id as foreign key
    # - backref='creator' = Creates 'creator' attribute on Task
    # - lazy=True = Loads tasks when accessed
    # - This means: user.created_tasks gives all tasks created by this user
    
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assignee_id', backref='assignee', lazy=True)
    # Explanation:
    # - assigned_tasks = Tasks assigned to this user
    # - foreign_keys='Task.assignee_id' = Uses assignee_id as foreign key
    # - backref='assignee' = Creates 'assignee' attribute on Task
    # - lazy=True = Loads tasks when accessed
    # - This means: user.assigned_tasks gives all tasks assigned to this user
    
    def __repr__(self):
        return f'<User {self.username}>'

# Step 8: Create Team Model
# What is this? Defining what a team looks like
class Team(db.Model):
    """
    Team Model
    This defines the structure of a team in the database
    """
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    name = db.Column(db.String(100), nullable=False)
    # Explanation:
    # - name = Team name
    # - db.String(100) = Text field, max 100 characters
    # - nullable=False = This field is required
    
    description = db.Column(db.Text)
    # Explanation:
    # - description = Team description
    # - db.Text = Text field (can hold long text)
    # - nullable=True = This field is optional
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - creator_id = ID of user who created the team
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Every team must have a creator
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When team was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    tasks = db.relationship('Task', backref='team', lazy=True, cascade='all, delete-orphan')
    # Explanation:
    # - tasks = Relationship to Task model
    # - backref='team' = Creates 'team' attribute on Task
    # - lazy=True = Loads tasks when accessed
    # - cascade = Deletes tasks when team is deleted
    # - This means: team.tasks gives all tasks in this team
    
    def __repr__(self):
        return f'<Team {self.name}>'

# Step 9: Create Task Model
# What is this? Defining what a task looks like
class Task(db.Model):
    """
    Task Model
    This defines the structure of a task in the database
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Unique identifier
    
    title = db.Column(db.String(200), nullable=False)
    # Explanation:
    # - title = Task title
    # - db.String(200) = Text field, max 200 characters
    # - nullable=False = This field is required
    
    description = db.Column(db.Text)
    # Explanation:
    # - description = Task description
    # - db.Text = Text field (can hold long text)
    # - nullable=True = This field is optional
    
    status = db.Column(db.String(20), default='pending', nullable=False)
    # Explanation:
    # - status = Task status
    # - db.String(20) = Text field, max 20 characters
    # - default='pending' = Default status is 'pending'
    # - nullable=False = This field is required
    # - Possible values: 'pending', 'in_progress', 'completed'
    
    priority = db.Column(db.String(20), default='medium', nullable=False)
    # Explanation:
    # - priority = Task priority
    # - db.String(20) = Text field, max 20 characters
    # - default='medium' = Default priority is 'medium'
    # - nullable=False = This field is required
    # - Possible values: 'low', 'medium', 'high'
    
    due_date = db.Column(db.DateTime)
    # Explanation:
    # - due_date = When task is due
    # - db.DateTime = Date and time data type
    # - nullable=True = This field is optional
    
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    # Explanation:
    # - team_id = ID of team this task belongs to
    # - db.ForeignKey('teams.id') = Links to teams table
    # - nullable=False = Every task must belong to a team
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Explanation:
    # - creator_id = ID of user who created the task
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=False = Every task must have a creator
    
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Explanation:
    # - assignee_id = ID of user assigned to the task
    # - db.ForeignKey('users.id') = Links to users table
    # - nullable=True = Task can be unassigned
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = When task was created
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    
    def __repr__(self):
        return f'<Task {self.title}>'

# Step 10: Create Database Tables
# What is this? Creating the actual database tables
with app.app_context():
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models and creates tables

# Step 11: Helper Functions
# What is this? Functions to help with authentication
def is_logged_in():
    """
    Check if user is logged in
    
    Returns:
    - True if logged in, False otherwise
    """
    return 'user_id' in session
    # Explanation:
    # - 'user_id' in session = Checks if user_id exists in session
    # - If exists, user is logged in

def get_current_user():
    """
    Get the current logged-in user
    
    Returns:
    - User object if logged in, None otherwise
    """
    if is_logged_in():
        # Explanation:
        # - if is_logged_in() = If user is logged in
        # - Only proceed if logged in
        
        return User.query.get(session['user_id'])
        # Explanation:
        # - User.query.get(session['user_id']) = Gets user by ID
        # - session['user_id'] = ID from session
        # - Returns User object
    
    return None
    # Explanation:
    # - return None = No user logged in

# Step 12: Create Home Route (GET)
# What is this? The main dashboard page
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows the dashboard with teams and tasks
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only show dashboard if logged in
        
        return redirect(url_for('login'))
        # Explanation:
        # - redirect = Sends user to login page
        # - Must be logged in to see dashboard
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 13: Get User's Teams
    # What is this? Finding all teams the user is in
    user_teams = current_user.teams.all()
    # Explanation:
    # - current_user.teams = Relationship to teams
    # - .all() = Gets all teams
    # - user_teams = List of Team objects
    
    # Step 14: Get User's Tasks
    # What is this? Finding all tasks assigned to the user
    assigned_tasks = Task.query.filter_by(assignee_id=current_user.id).all()
    # Explanation:
    # - Task.query.filter_by(assignee_id=current_user.id) = Find tasks assigned to user
    # - .all() = Get all matching tasks
    # - assigned_tasks = List of Task objects assigned to user
    
    return render_template('index.html', teams=user_teams, tasks=assigned_tasks, current_user=current_user)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = Dashboard template
    # - teams=user_teams = Passes teams to template
    # - tasks=assigned_tasks = Passes tasks to template
    # - current_user=current_user = Passes current user to template

# Step 15: Create Register Route (GET and POST)
# What is this? Page for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function handles user registration
    GET: Shows registration form
    POST: Processes registration
    """
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        # Explanation:
        # - Gets form data
        # - username, email, password = User input
        
        # Step 16: Validate Input
        if not username or not email or not password:
            # Explanation:
            # - if not username or not email or not password = If any field empty
            # - Only proceed if all fields filled
            
            flash('Please fill in all fields!', 'error')
            return render_template('register.html')
        
        # Step 17: Check if Username Exists
        if User.query.filter_by(username=username).first():
            # Explanation:
            # - User.query.filter_by(username=username) = Find user with this username
            # - .first() = Get first result (or None)
            # - If user exists, username is taken
            
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        # Step 18: Check if Email Exists
        if User.query.filter_by(email=email).first():
            # Explanation:
            # - User.query.filter_by(email=email) = Find user with this email
            # - .first() = Get first result (or None)
            # - If user exists, email is taken
            
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Step 19: Create New User
        password_hash = generate_password_hash(password)
        # Explanation:
        # - generate_password_hash(password) = Hashes password securely
        # - password_hash = Hashed password (not plain text!)
        
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        # Explanation:
        # - User() = Creates new User object
        # - Sets username, email, password_hash
        # - new_user = New user (not saved yet)
        
        db.session.add(new_user)
        db.session.commit()
        # Explanation:
        # - db.session.add(new_user) = Adds user to session
        # - db.session.commit() = Saves to database
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        # Explanation:
        # - Shows success message
        # - Redirects to login page
    
    return render_template('register.html')
    # Explanation:
    # - render_template = Shows registration form
    # - 'register.html' = Registration template

# Step 20: Create Login Route (GET and POST)
# What is this? Page for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles user login
    GET: Shows login form
    POST: Processes login
    """
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        # Explanation:
        # - Gets form data
        # - username, password = User input
        
        # Step 21: Find User
        user = User.query.filter_by(username=username).first()
        # Explanation:
        # - User.query.filter_by(username=username) = Find user with this username
        # - .first() = Get first result (or None)
        # - user = User object (or None if not found)
        
        # Step 22: Verify Password
        if user and check_password_hash(user.password_hash, password):
            # Explanation:
            # - if user = If user was found
            # - check_password_hash(user.password_hash, password) = Verifies password
            # - Only proceed if user exists and password is correct
            
            session['user_id'] = user.id
            # Explanation:
            # - session['user_id'] = user.id = Stores user ID in session
            # - This logs the user in
            
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
            # Explanation:
            # - Shows success message
            # - Redirects to dashboard
        else:
            # Explanation:
            # - else = If user not found or password incorrect
            
            flash('Invalid username or password!', 'error')
            # Explanation:
            # - Shows error message
    
    return render_template('login.html')
    # Explanation:
    # - render_template = Shows login form
    # - 'login.html' = Login template

# Step 23: Create Logout Route
# What is this? Logs user out
@app.route('/logout')
def logout():
    """
    This function logs the user out
    """
    session.pop('user_id', None)
    # Explanation:
    # - session.pop('user_id', None) = Removes user_id from session
    # - This logs the user out
    
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))
    # Explanation:
    # - Shows success message
    # - Redirects to login page

# Step 24: Create Create Team Route (GET and POST)
# What is this? Page for creating a new team
@app.route('/create-team', methods=['GET', 'POST'])
def create_team():
    """
    This function handles creating a new team
    GET: Shows create team form
    POST: Processes team creation
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can create teams
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        # Explanation:
        # - Gets form data
        # - name, description = Team information
        
        # Step 25: Validate Input
        if not name:
            # Explanation:
            # - if not name = If name is empty
            # - Only proceed if name exists
            
            flash('Team name is required!', 'error')
            return render_template('create_team.html')
        
        current_user = get_current_user()
        # Explanation:
        # - get_current_user() = Gets logged-in user
        # - current_user = User object
        
        # Step 26: Create New Team
        new_team = Team(
            name=name,
            description=description,
            creator_id=current_user.id
        )
        # Explanation:
        # - Team() = Creates new Team object
        # - name=name = Sets team name
        # - description=description = Sets team description
        # - creator_id=current_user.id = Sets creator to current user
        # - date_created = Automatically set (from model default)
        # - new_team = New team (not saved yet)
        
        db.session.add(new_team)
        db.session.commit()
        # Explanation:
        # - db.session.add(new_team) = Adds team to session
        # - db.session.commit() = Saves to database
        
        # Step 27: Add Creator to Team
        # What is this? Adding the creator as a team member
        new_team.members.append(current_user)
        # Explanation:
        # - new_team.members = Relationship to users (team members)
        # - .append(current_user) = Adds current user to team
        # - This adds the creator to the team members
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves changes
        # - This saves the team membership
        
        flash('Team created successfully!', 'success')
        return redirect(url_for('team_detail', team_id=new_team.id))
        # Explanation:
        # - Shows success message
        # - Redirects to team detail page
    
    return render_template('create_team.html')
    # Explanation:
    # - render_template = Shows create team form
    # - 'create_team.html' = Create team template

# Step 28: Create Team Detail Route (GET)
# What is this? Page showing team details and tasks
@app.route('/team/<int:team_id>')
def team_detail(team_id):
    """
    This function shows team details and tasks
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can see teams
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    team = Team.query.get_or_404(team_id)
    # Explanation:
    # - Team.query.get_or_404(team_id) = Gets team by ID
    # - team_id = ID from URL
    # - team = Team object (or 404 error if not found)
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 29: Check if User is Team Member
    # What is this? Making sure user can see this team
    if current_user not in team.members:
        # Explanation:
        # - if current_user not in team.members = If user is not in team
        # - Only team members can see team details
        
        flash('You are not a member of this team!', 'error')
        return redirect(url_for('index'))
        # Explanation:
        # - Shows error message
        # - Redirects to dashboard
    
    # Step 30: Get Team Tasks
    # What is this? Finding all tasks in this team
    tasks = Task.query.filter_by(team_id=team_id).order_by(Task.date_created.desc()).all()
    # Explanation:
    # - Task.query.filter_by(team_id=team_id) = Find tasks in this team
    # - .order_by(Task.date_created.desc()) = Sort by date, newest first
    # - .all() = Get all matching tasks
    # - tasks = List of Task objects in this team
    
    # Step 31: Get All Users for Assignment
    # What is this? Getting all users to assign tasks to
    all_users = User.query.all()
    # Explanation:
    # - User.query.all() = Gets all users
    # - all_users = List of all User objects
    
    return render_template('team_detail.html', team=team, tasks=tasks, all_users=all_users, current_user=current_user)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'team_detail.html' = Team detail template
    # - team=team = Passes team to template
    # - tasks=tasks = Passes tasks to template
    # - all_users=all_users = Passes all users to template
    # - current_user=current_user = Passes current user to template

# Step 32: Create Add Member Route (POST)
# What is this? Handles adding a user to a team
@app.route('/team/<int:team_id>/add-member', methods=['POST'])
def add_member(team_id):
    """
    This function handles adding a user to a team
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can add members
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    team = Team.query.get_or_404(team_id)
    # Explanation:
    # - Team.query.get_or_404(team_id) = Gets team by ID
    # - team = Team object (or 404 error if not found)
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 33: Check if User is Team Member
    if current_user not in team.members:
        # Explanation:
        # - if current_user not in team.members = If user is not in team
        # - Only team members can add members
        
        flash('You are not a member of this team!', 'error')
        return redirect(url_for('index'))
        # Explanation:
        # - Shows error message
        # - Redirects to dashboard
    
    user_id = int(request.form.get('user_id'))
    # Explanation:
    # - Gets user ID from form
    # - int() = Converts to integer
    # - user_id = ID of user to add
    
    user_to_add = User.query.get_or_404(user_id)
    # Explanation:
    # - User.query.get_or_404(user_id) = Gets user by ID
    # - user_to_add = User object (or 404 error if not found)
    
    # Step 34: Check if User Already in Team
    if user_to_add in team.members:
        # Explanation:
        # - if user_to_add in team.members = If user is already in team
        # - Can't add user twice!
        
        flash('User is already a member of this team!', 'error')
        return redirect(url_for('team_detail', team_id=team_id))
        # Explanation:
        # - Shows error message
        # - Redirects back to team detail
    
    # Step 35: Add User to Team
    team.members.append(user_to_add)
    # Explanation:
    # - team.members = Relationship to users (team members)
    # - .append(user_to_add) = Adds user to team
    # - This adds the user to the team members
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes
    # - This saves the team membership
    
    flash(f'{user_to_add.username} added to team!', 'success')
    return redirect(url_for('team_detail', team_id=team_id))
    # Explanation:
    # - Shows success message
    # - Redirects back to team detail

# Step 36: Create Create Task Route (POST)
# What is this? Handles creating a new task
@app.route('/team/<int:team_id>/create-task', methods=['POST'])
def create_task(team_id):
    """
    This function handles creating a new task
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can create tasks
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    team = Team.query.get_or_404(team_id)
    # Explanation:
    # - Team.query.get_or_404(team_id) = Gets team by ID
    # - team = Team object (or 404 error if not found)
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 37: Check if User is Team Member
    if current_user not in team.members:
        # Explanation:
        # - if current_user not in team.members = If user is not in team
        # - Only team members can create tasks
        
        flash('You are not a member of this team!', 'error')
        return redirect(url_for('index'))
        # Explanation:
        # - Shows error message
        # - Redirects to dashboard
    
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    status = request.form.get('status', 'pending')
    priority = request.form.get('priority', 'medium')
    assignee_id = request.form.get('assignee_id')
    due_date_str = request.form.get('due_date')
    # Explanation:
    # - Gets form data
    # - title, description, status, priority, assignee_id, due_date_str = Task information
    
    # Step 38: Validate Input
    if not title:
        # Explanation:
        # - if not title = If title is empty
        # - Only proceed if title exists
        
        flash('Task title is required!', 'error')
        return redirect(url_for('team_detail', team_id=team_id))
        # Explanation:
        # - Shows error message
        # - Redirects back to team detail
    
    # Step 39: Parse Due Date
    due_date = None
    # Explanation:
    # - due_date = None = Default (no due date)
    
    if due_date_str:
        # Explanation:
        # - if due_date_str = If due date was provided
        # - Only proceed if due date exists
        
        try:
            # Explanation:
            # - try = Attempt to parse date
            # - If parsing fails, due_date stays None
            
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            # Explanation:
            # - datetime.strptime() = Parses date string
            # - '%Y-%m-%d' = Date format (YYYY-MM-DD)
            # - due_date = Parsed date object
        except ValueError:
            # Explanation:
            # - except ValueError = If date parsing fails
            # - Invalid date format
            
            pass
            # Explanation:
            # - pass = Do nothing
            # - due_date stays None
    
    # Step 40: Create New Task
    new_task = Task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        team_id=team_id,
        creator_id=current_user.id,
        assignee_id=int(assignee_id) if assignee_id else None,
        due_date=due_date
    )
    # Explanation:
    # - Task() = Creates new Task object
    # - Sets all task fields
    # - assignee_id = Converts to int if provided, None otherwise
    # - new_task = New task (not saved yet)
    
    db.session.add(new_task)
    db.session.commit()
    # Explanation:
    # - db.session.add(new_task) = Adds task to session
    # - db.session.commit() = Saves to database
    
    flash('Task created successfully!', 'success')
    return redirect(url_for('team_detail', team_id=team_id))
    # Explanation:
    # - Shows success message
    # - Redirects back to team detail

# Step 41: Create Update Task Route (POST)
# What is this? Handles updating a task
@app.route('/task/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    This function handles updating a task
    """
    if not is_logged_in():
        # Explanation:
        # - if not is_logged_in() = If user is not logged in
        # - Only logged-in users can update tasks
        
        return redirect(url_for('login'))
        # Explanation:
        # - Redirects to login page
    
    task = Task.query.get_or_404(task_id)
    # Explanation:
    # - Task.query.get_or_404(task_id) = Gets task by ID
    # - task = Task object (or 404 error if not found)
    
    current_user = get_current_user()
    # Explanation:
    # - get_current_user() = Gets logged-in user
    # - current_user = User object
    
    # Step 42: Check if User is Team Member
    if current_user not in task.team.members:
        # Explanation:
        # - if current_user not in task.team.members = If user is not in team
        # - Only team members can update tasks
        
        flash('You are not a member of this team!', 'error')
        return redirect(url_for('index'))
        # Explanation:
        # - Shows error message
        # - Redirects to dashboard
    
    # Step 43: Update Task Fields
    task.title = request.form.get('title', task.title).strip()
    task.description = request.form.get('description', task.description).strip()
    task.status = request.form.get('status', task.status)
    task.priority = request.form.get('priority', task.priority)
    assignee_id = request.form.get('assignee_id')
    task.assignee_id = int(assignee_id) if assignee_id else None
    # Explanation:
    # - Updates task fields from form
    # - Uses existing value if form field is empty
    # - assignee_id = Converts to int if provided, None otherwise
    
    # Step 44: Update Due Date
    due_date_str = request.form.get('due_date')
    # Explanation:
    # - Gets due date from form
    # - due_date_str = Date string (or None)
    
    if due_date_str:
        # Explanation:
        # - if due_date_str = If due date was provided
        # - Only proceed if due date exists
        
        try:
            # Explanation:
            # - try = Attempt to parse date
            # - If parsing fails, due_date stays None
            
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            # Explanation:
            # - datetime.strptime() = Parses date string
            # - '%Y-%m-%d' = Date format (YYYY-MM-DD)
            # - task.due_date = Parsed date object
        except ValueError:
            # Explanation:
            # - except ValueError = If date parsing fails
            # - Invalid date format
            
            pass
            # Explanation:
            # - pass = Do nothing
            # - due_date stays unchanged
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes
    # - This saves the updated task
    
    flash('Task updated successfully!', 'success')
    return redirect(url_for('team_detail', team_id=task.team_id))
    # Explanation:
    # - Shows success message
    # - Redirects back to team detail

# Step 45: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

