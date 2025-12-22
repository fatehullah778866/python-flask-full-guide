# Comment System App
# This app allows users to add and view comments!

# Step 1: Import Flask and Database Tools
# What is this? We're importing Flask and database tools
# Think of it like: "Get Flask tools and database tools"
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - flash = Function to show messages to users
# - SQLAlchemy = Database toolkit
# - datetime = Module for working with dates and times
# - We'll use SQLAlchemy to store comments in a database!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///comments.db' = SQLite database file named 'comments.db'
# - SQLite = Simple database that stores data in a file
# - comments.db = The file where our comments will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
# - Required for flash messages to work

# Step 4: Initialize Database
# What is this? Creating the database object
# Think of it like: "Create a database manager"
db = SQLAlchemy(app)
# Explanation:
# - SQLAlchemy(app) = Creates database object
# - db = Our database manager
# - We'll use this to create tables and save data

# Step 5: Create Comment Model
# What is this? Defining what a comment looks like
# Think of it like: "Creating a template for comments"
class Comment(db.Model):
    """
    Comment Model
    This defines the structure of a comment in the database
    """
    # Step 6: Define Table Name
    # What is this? Name of the database table
    __tablename__ = 'comments'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'comments' = Name of the table in database
    # - Table = Like a spreadsheet with rows and columns
    # - This table will store all our comments
    
    # Step 7: Define Columns (Fields)
    # What is this? Defining what data each comment will have
    # Think of it like: "What information does each comment need?"
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Column name (unique identifier)
    # - db.Column = Creates a column in the database table
    # - db.Integer = Data type (whole number)
    # - primary_key=True = This is the unique identifier
    # - Each comment gets a unique ID (1, 2, 3, ...)
    
    name = db.Column(db.String(100), nullable=False)
    # Explanation:
    # - name = Column name (commenter's name)
    # - db.String(100) = Text field, max 100 characters
    # - nullable=False = This field is required (can't be empty)
    # - Every comment must have a name
    
    email = db.Column(db.String(120), nullable=False)
    # Explanation:
    # - email = Column name (commenter's email)
    # - db.String(120) = Text field, max 120 characters
    # - nullable=False = This field is required
    # - Every comment must have an email
    
    comment_text = db.Column(db.Text, nullable=False)
    # Explanation:
    # - comment_text = Column name (the actual comment)
    # - db.Text = Text field (can hold long text)
    # - nullable=False = This field is required
    # - Every comment must have text
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = Column name (when comment was created)
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    # - When we create a comment, it automatically gets the current date/time
    
    # Step 8: Define String Representation
    # What is this? How to display the comment when printed
    def __repr__(self):
        """
        String representation of the Comment object
        This is what you see when you print a comment
        """
        return f'<Comment {self.id}: {self.name}>'
        # Explanation:
        # - __repr__ = Special method for string representation
        # - f'...' = f-string (formatted string)
        # - {self.id} = Comment's ID number
        # - {self.name} = Commenter's name
        # - Example: "<Comment 1: John Doe>"

# Step 9: Create Database Tables
# What is this? Creating the actual database tables
# Think of it like: "Build the database structure"
with app.app_context():
    # Explanation:
    # - with app.app_context() = Flask application context
    # - Needed to access database within Flask app
    
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models (like Comment) and creates tables
    # - If tables already exist, does nothing
    # - This builds the database structure

# Step 10: Create Home Route (GET)
# What is this? The main page that shows all comments
# Think of it like: "When someone visits the home page, show all comments"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows all comments from the database
    """
    # Step 11: Get All Comments from Database
    # What is this? Fetching all comments from the database
    comments = Comment.query.order_by(Comment.date_created.desc()).all()
    # Explanation:
    # - Comment.query = Query object for Comment model
    # - .order_by(Comment.date_created.desc()) = Sort by date, newest first
    # - .desc() = Descending order (newest to oldest)
    # - .all() = Get all comments (returns a list)
    # - comments = List of all Comment objects
    # - This is like saying: "Get all comments, sorted by date, newest first"
    
    # Step 12: Render Template with Comments
    # What is this? Showing the HTML page with all comments
    return render_template('index.html', comments=comments)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - comments=comments = Passes the comments list to the template
    # - The first 'comments' = Variable name in the template
    # - The second comments = The actual comments list from Python
    # - In the template, we can use comments to display them

# Step 13: Create Add Comment Route (POST)
# What is this? Handles form submission to add a comment
# Think of it like: "When user submits comment form, save it"
@app.route('/add-comment', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/add-comment' = The URL for adding comments
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/add-comment', Flask will run the function below

def add_comment():
    """
    This function runs when a comment is submitted
    It saves the comment to the database
    """
    # Step 14: Get Form Data
    # What is this? Getting the data from the form
    name = request.form.get('name', '').strip()
    # Explanation:
    # - request.form.get('name', '') = Gets value of input named 'name'
    # - If 'name' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - name = Variable to hold the commenter's name
    
    email = request.form.get('email', '').strip()
    # Explanation:
    # - request.form.get('email', '') = Gets value of input named 'email'
    # - .strip() = Removes whitespace
    # - email = Variable to hold the commenter's email
    
    comment_text = request.form.get('comment', '').strip()
    # Explanation:
    # - request.form.get('comment', '') = Gets value of textarea named 'comment'
    # - .strip() = Removes whitespace
    # - comment_text = Variable to hold the comment text
    
    # Step 15: Validate Form Data
    # What is this? Checking if user entered valid data
    if not name or not email or not comment_text:
        # Explanation:
        # - if not name or not email or not comment_text = If any field is empty
        # - Empty strings are "falsy" in Python
        # - Only proceed if all fields are filled
        
        flash('Please fill in all fields!', 'error')
        # Explanation:
        # - flash() = Function to show temporary message
        # - 'Please fill in all fields!' = Error message
        # - 'error' = Message category
        
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route (home page)
        # - User is sent back to home page to try again
    
    # Step 16: Create New Comment Object
    # What is this? Creating a new comment
    new_comment = Comment(
        name=name,
        email=email,
        comment_text=comment_text
    )
    # Explanation:
    # - Comment() = Creates new Comment object
    # - name=name = Sets the commenter's name
    # - email=email = Sets the commenter's email
    # - comment_text=comment_text = Sets the comment text
    # - date_created = Automatically set (from model default)
    # - new_comment = The new Comment object (not saved yet)
    
    # Step 17: Save to Database
    # What is this? Adding the comment to the database
    db.session.add(new_comment)
    # Explanation:
    # - db.session = Database session
    # - .add(new_comment) = Adds comment to session (stages it for saving)
    # - Not saved yet, just staged
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes to database
    # - Actually writes the comment to the database file
    # - This is when the comment is permanently saved
    
    # Step 18: Show Success Message
    # What is this? Telling user the comment was added
    flash('Comment added successfully!', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - 'Comment added successfully!' = Success message
    # - 'success' = Message category
    
    # Step 19: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is sent back to home page
    # - They'll see their new comment in the list!

# Step 20: Run the Application
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

