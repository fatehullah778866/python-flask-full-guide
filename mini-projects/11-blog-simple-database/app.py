# Blog Application (Simple with Database)
# This app creates a simple blog with database storage!

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
# - SQLAlchemy = Database toolkit (helps us work with databases)
# - datetime = Module for working with dates and times
# - We'll use SQLAlchemy to store blog posts in a database!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///blog.db' = SQLite database file named 'blog.db'
# - SQLite = Simple database that stores data in a file
# - blog.db = The file where our data will be stored
# - This is like telling Flask: "Save data in blog.db file"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)
# - This is a performance setting

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
# - Required for flash messages to work
# - In production, use a long, random, secret key

# Step 4: Initialize Database
# What is this? Creating the database object
# Think of it like: "Create a database manager"
db = SQLAlchemy(app)
# Explanation:
# - SQLAlchemy(app) = Creates database object
# - db = Our database manager
# - We'll use this to create tables and save data
# - This is like having a helper to manage our database

# Step 5: Create Blog Post Model
# What is this? Defining what a blog post looks like
# Think of it like: "Creating a template for blog posts"
class Post(db.Model):
    """
    Blog Post Model
    This defines the structure of a blog post in the database
    """
    # Step 6: Define Table Name
    # What is this? Name of the database table
    __tablename__ = 'posts'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'posts' = Name of the table in database
    # - Table = Like a spreadsheet with rows and columns
    # - This table will store all our blog posts
    
    # Step 7: Define Columns (Fields)
    # What is this? Defining what data each post will have
    # Think of it like: "What information does each post need?"
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Column name (unique identifier)
    # - db.Column = Creates a column in the database table
    # - db.Integer = Data type (whole number)
    # - primary_key=True = This is the unique identifier
    # - Each post gets a unique ID (1, 2, 3, ...)
    # - Like a serial number for each post
    
    title = db.Column(db.String(200), nullable=False)
    # Explanation:
    # - title = Column name (post title)
    # - db.String(200) = Text field, max 200 characters
    # - nullable=False = This field is required (can't be empty)
    # - Every post must have a title
    
    content = db.Column(db.Text, nullable=False)
    # Explanation:
    # - content = Column name (post content/body)
    # - db.Text = Text field (can hold long text)
    # - nullable=False = This field is required
    # - Every post must have content
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = Column name (when post was created)
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    # - When we create a post, it automatically gets the current date/time
    # - datetime.utcnow = Current date and time
    
    # Step 8: Define String Representation
    # What is this? How to display the post when printed
    def __repr__(self):
        """
        String representation of the Post object
        This is what you see when you print a post
        """
        return f'<Post {self.id}: {self.title}>'
        # Explanation:
        # - __repr__ = Special method for string representation
        # - f'...' = f-string (formatted string)
        # - {self.id} = Post's ID number
        # - {self.title} = Post's title
        # - Example: "<Post 1: My First Post>"
        # - This is helpful for debugging

# Step 9: Create Database Tables
# What is this? Creating the actual database tables
# Think of it like: "Build the database structure"
with app.app_context():
    # Explanation:
    # - with app.app_context() = Flask application context
    # - Needed to access database within Flask app
    # - Context = Environment where Flask operations happen
    
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models (like Post) and creates tables
    # - If tables already exist, does nothing
    # - This builds the database structure
    # - Like creating an empty spreadsheet with column headers

# Step 10: Create Home Route (GET)
# What is this? The main page that shows all blog posts
# Think of it like: "When someone visits the home page, show all posts"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows all blog posts from the database
    """
    # Step 11: Get All Posts from Database
    # What is this? Fetching all blog posts from the database
    posts = Post.query.order_by(Post.date_created.desc()).all()
    # Explanation:
    # - Post.query = Query object for Post model
    # - .order_by(Post.date_created.desc()) = Sort by date, newest first
    # - .desc() = Descending order (newest to oldest)
    # - .all() = Get all posts (returns a list)
    # - posts = List of all Post objects
    # - This is like saying: "Get all posts, sorted by date, newest first"
    
    # Step 12: Render Template with Posts
    # What is this? Showing the HTML page with all posts
    return render_template('index.html', posts=posts)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - posts=posts = Passes the posts list to the template
    # - The first 'posts' = Variable name in the template
    # - The second posts = The actual posts list from Python
    # - In the template, we can use posts to display them

# Step 13: Create Post Route (GET)
# What is this? Page to view a single blog post
# Think of it like: "When someone visits /post/1, show post with ID 1"
@app.route('/post/<int:post_id>')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/post/<int:post_id>' = Dynamic route with post ID
# - <int:post_id> = Captures post ID from URL (must be integer)
# - Example: /post/1 → post_id = 1
# - Example: /post/5 → post_id = 5

def view_post(post_id):
    """
    This function runs when someone visits a specific post
    It shows a single blog post by its ID
    """
    # Step 14: Get Post from Database
    # What is this? Finding the specific post by ID
    post = Post.query.get_or_404(post_id)
    # Explanation:
    # - Post.query = Query object for Post model
    # - .get_or_404(post_id) = Get post by ID, or show 404 error if not found
    # - post_id = The ID from the URL
    # - post = The Post object (or 404 error if not found)
    # - This is like saying: "Find post with this ID, or show error"
    
    # Step 15: Render Template with Post
    # What is this? Showing the HTML page with the post
    return render_template('post.html', post=post)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'post.html' = The template file to display
    # - post=post = Passes the post object to the template
    # - In the template, we can use post.title, post.content, etc.

# Step 16: Create Create Post Route (GET and POST)
# What is this? Page to create a new blog post
# Think of it like: "When someone visits /create, show form to create post"
@app.route('/create', methods=['GET', 'POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/create' = The URL for creating posts
# - methods=['GET', 'POST'] = Accepts both GET (view form) and POST (submit form)
# - GET = When you first visit the page (show form)
# - POST = When you submit the form (save post)

def create_post():
    """
    This function runs when someone visits /create
    GET: Shows form to create a post
    POST: Saves the new post to database
    """
    # Step 17: Handle Form Submission (POST)
    # What is this? Processing the form when user submits it
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        # - POST = Form submission
        # - Only do this if user submitted the form
        
        # Step 18: Get Form Data
        # What is this? Getting the data from the form
        title = request.form.get('title', '').strip()
        # Explanation:
        # - request.form.get('title', '') = Gets value of input named 'title'
        # - If 'title' doesn't exist, returns empty string ''
        # - .strip() = Removes whitespace from beginning and end
        # - title = Variable to hold the post title
        
        content = request.form.get('content', '').strip()
        # Explanation:
        # - request.form.get('content', '') = Gets value of textarea named 'content'
        # - .strip() = Removes whitespace
        # - content = Variable to hold the post content
        
        # Step 19: Validate Form Data
        # What is this? Checking if user entered valid data
        if not title or not content:
            # Explanation:
            # - if not title or not content = If title or content is empty
            # - Empty strings are "falsy" in Python
            # - Only proceed if both are filled
            
            flash('Please fill in both title and content!', 'error')
            # Explanation:
            # - flash() = Function to show temporary message
            # - 'Please fill in both title and content!' = Message text
            # - 'error' = Message category (for styling)
            
            return render_template('create.html')
            # Explanation:
            # - Shows form again with error message
            # - User can try again
        
        # Step 20: Create New Post Object
        # What is this? Creating a new blog post
        new_post = Post(
            title=title,
            content=content
        )
        # Explanation:
        # - Post() = Creates new Post object
        # - title=title = Sets the title
        # - content=content = Sets the content
        # - date_created = Automatically set (from model default)
        # - new_post = The new Post object (not saved yet)
        
        # Step 21: Save to Database
        # What is this? Adding the post to the database
        db.session.add(new_post)
        # Explanation:
        # - db.session = Database session (like a transaction)
        # - .add(new_post) = Adds post to session (stages it for saving)
        # - Not saved yet, just staged
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves changes to database
        # - Actually writes the post to the database file
        # - This is when the post is permanently saved
        # - Like clicking "Save" in a document
        
        # Step 22: Show Success Message
        # What is this? Telling user the post was created
        flash('Post created successfully!', 'success')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Post created successfully!' = Success message
        # - 'success' = Message category
        
        # Step 23: Redirect to Home Page
        # What is this? Sending user back to home page
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route (home page)
        # - User sees the new post in the list
    
    # Step 24: Handle Form Display (GET)
    # What is this? Showing the form when user first visits
    return render_template('create.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'create.html' = The template file with the form
    # - This shows the form to create a new post

# Step 25: Run the Application
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

