# Voting/Polling System App
# This app allows users to vote on polls!

# Step 1: Import Flask and Database Tools
# What is this? We're importing Flask and database tools
# Think of it like: "Get Flask tools and database tools"
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
# - We'll use SQLAlchemy to store polls and votes in a database!

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SQLALCHEMY_DATABASE_URI' = Setting name for database location
# - 'sqlite:///polls.db' = SQLite database file named 'polls.db'
# - SQLite = Simple database that stores data in a file
# - polls.db = The file where our polls and votes will be stored

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Explanation:
# - 'SQLALCHEMY_TRACK_MODIFICATIONS' = Setting to track changes
# - False = Don't track modifications (saves memory)

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
# - Required for sessions and flash messages to work

# Step 4: Initialize Database
# What is this? Creating the database object
# Think of it like: "Create a database manager"
db = SQLAlchemy(app)
# Explanation:
# - SQLAlchemy(app) = Creates database object
# - db = Our database manager
# - We'll use this to create tables and save data

# Step 5: Create Poll Model
# What is this? Defining what a poll looks like
# Think of it like: "Creating a template for polls"
class Poll(db.Model):
    """
    Poll Model
    This defines the structure of a poll in the database
    """
    # Step 6: Define Table Name
    # What is this? Name of the database table
    __tablename__ = 'polls'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'polls' = Name of the table in database
    # - Table = Like a spreadsheet with rows and columns
    # - This table will store all our polls
    
    # Step 7: Define Columns (Fields)
    # What is this? Defining what data each poll will have
    # Think of it like: "What information does each poll need?"
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Column name (unique identifier)
    # - db.Column = Creates a column in the database table
    # - db.Integer = Data type (whole number)
    # - primary_key=True = This is the unique identifier
    # - Each poll gets a unique ID (1, 2, 3, ...)
    
    question = db.Column(db.String(200), nullable=False)
    # Explanation:
    # - question = Column name (poll question)
    # - db.String(200) = Text field, max 200 characters
    # - nullable=False = This field is required (can't be empty)
    # - Every poll must have a question
    # - Example: "What is your favorite programming language?"
    
    option1 = db.Column(db.String(100), nullable=False)
    # Explanation:
    # - option1 = Column name (first voting option)
    # - db.String(100) = Text field, max 100 characters
    # - nullable=False = This field is required
    # - Every poll must have at least one option
    # - Example: "Python"
    
    option2 = db.Column(db.String(100), nullable=False)
    # Explanation:
    # - option2 = Column name (second voting option)
    # - db.String(100) = Text field, max 100 characters
    # - nullable=False = This field is required
    # - Every poll must have a second option
    # - Example: "JavaScript"
    
    votes_option1 = db.Column(db.Integer, default=0)
    # Explanation:
    # - votes_option1 = Column name (votes for option 1)
    # - db.Integer = Data type (whole number)
    # - default=0 = Starts at 0 votes
    # - This counts how many votes option 1 has
    # - Example: 5 votes for "Python"
    
    votes_option2 = db.Column(db.Integer, default=0)
    # Explanation:
    # - votes_option2 = Column name (votes for option 2)
    # - db.Integer = Data type (whole number)
    # - default=0 = Starts at 0 votes
    # - This counts how many votes option 2 has
    # - Example: 3 votes for "JavaScript"
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = Column name (when poll was created)
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    # - When we create a poll, it automatically gets the current date/time
    
    # Step 8: Define String Representation
    # What is this? How to display the poll when printed
    def __repr__(self):
        """
        String representation of the Poll object
        This is what you see when you print a poll
        """
        return f'<Poll {self.id}: {self.question}>'
        # Explanation:
        # - __repr__ = Special method for string representation
        # - f'...' = f-string (formatted string)
        # - {self.id} = Poll's ID number
        # - {self.question} = Poll's question
        # - Example: "<Poll 1: What is your favorite language?>"

# Step 9: Create Vote Model
# What is this? Defining what a vote looks like
# Think of it like: "Creating a template for votes"
class Vote(db.Model):
    """
    Vote Model
    This defines the structure of a vote in the database
    """
    # Step 10: Define Table Name
    # What is this? Name of the database table
    __tablename__ = 'votes'
    # Explanation:
    # - __tablename__ = Special variable for table name
    # - 'votes' = Name of the table in database
    # - This table will store all votes
    # - We'll use this to prevent duplicate votes (one vote per user per poll)
    
    id = db.Column(db.Integer, primary_key=True)
    # Explanation:
    # - id = Column name (unique identifier)
    # - db.Column = Creates a column in the database table
    # - db.Integer = Data type (whole number)
    # - primary_key=True = This is the unique identifier
    # - Each vote gets a unique ID
    
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    # Explanation:
    # - poll_id = Column name (which poll this vote is for)
    # - db.Integer = Data type (whole number)
    # - db.ForeignKey('polls.id') = Links to polls table
    # - ForeignKey = Relationship to another table
    # - 'polls.id' = References the id column in polls table
    # - nullable=False = This field is required
    # - Every vote must belong to a poll
    # - This creates a relationship: Vote → Poll
    
    voter_ip = db.Column(db.String(50), nullable=False)
    # Explanation:
    # - voter_ip = Column name (voter's IP address)
    # - db.String(50) = Text field, max 50 characters
    # - nullable=False = This field is required
    # - We'll use IP address to prevent duplicate votes
    # - In a real app, you'd use user accounts, but IP is simpler for learning
    # - IP address = Unique identifier for each user's computer
    
    option = db.Column(db.Integer, nullable=False)
    # Explanation:
    # - option = Column name (which option was voted for)
    # - db.Integer = Data type (whole number)
    # - nullable=False = This field is required
    # - 1 = Voted for option 1
    # - 2 = Voted for option 2
    # - Example: option = 1 means voted for "Python"
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Explanation:
    # - date_created = Column name (when vote was cast)
    # - db.DateTime = Date and time data type
    # - default=datetime.utcnow = Automatically set to current time
    # - When we create a vote, it automatically gets the current date/time
    
    # Step 11: Define Unique Constraint
    # What is this? Preventing duplicate votes from same IP
    # Think of it like: "One vote per IP address per poll"
    __table_args__ = (db.UniqueConstraint('poll_id', 'voter_ip', name='unique_vote'),)
    # Explanation:
    # - __table_args__ = Special variable for table constraints
    # - db.UniqueConstraint() = Creates unique constraint
    # - 'poll_id', 'voter_ip' = Columns that must be unique together
    # - name='unique_vote' = Name of the constraint
    # - This ensures one vote per IP address per poll
    # - Prevents someone from voting multiple times on the same poll!
    
    # Step 12: Define String Representation
    # What is this? How to display the vote when printed
    def __repr__(self):
        """
        String representation of the Vote object
        This is what you see when you print a vote
        """
        return f'<Vote {self.id}: Poll {self.poll_id}, Option {self.option}>'
        # Explanation:
        # - __repr__ = Special method for string representation
        # - f'...' = f-string (formatted string)
        # - {self.id} = Vote's ID number
        # - {self.poll_id} = Poll ID
        # - {self.option} = Option voted for
        # - Example: "<Vote 1: Poll 1, Option 1>"

# Step 13: Create Database Tables
# What is this? Creating the actual database tables
# Think of it like: "Build the database structure"
with app.app_context():
    # Explanation:
    # - with app.app_context() = Flask application context
    # - Needed to access database within Flask app
    
    db.create_all()
    # Explanation:
    # - db.create_all() = Creates all database tables
    # - Looks at our models (like Poll, Vote) and creates tables
    # - If tables already exist, does nothing
    # - This builds the database structure

# Step 14: Initialize Sample Polls
# What is this? Creating some sample polls to start with
# Think of it like: "Add some example polls so we have data"
with app.app_context():
    # Explanation:
    # - with app.app_context() = Flask application context
    
    if Poll.query.count() == 0:
        # Explanation:
        # - Poll.query.count() = Counts how many polls exist
        # - == 0 = If no polls exist
        # - Only create sample polls if database is empty
        
        sample_polls = [
            Poll(question='What is your favorite programming language?', 
                 option1='Python', option2='JavaScript'),
            Poll(question='Do you prefer frontend or backend development?', 
                 option1='Frontend', option2='Backend'),
            Poll(question='What is your favorite database?', 
                 option1='PostgreSQL', option2='MongoDB')
        ]
        # Explanation:
        # - sample_polls = List of Poll objects
        # - Each Poll has question, option1, option2
        # - votes_option1 and votes_option2 start at 0 (default)
        # - date_created is automatically set
        
        for poll in sample_polls:
            # Explanation:
            # - for poll in sample_polls = Loop through each poll
            # - poll = Current poll object
            
            db.session.add(poll)
            # Explanation:
            # - db.session.add(poll) = Adds poll to session
            # - Stages it for saving
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves all polls to database
        # - Actually writes them to the database file

# Step 15: Helper Function to Get Voter IP
# What is this? Function to get the user's IP address
# Think of it like: "Find out who is voting"
def get_voter_ip():
    """
    Get the IP address of the voter
    Used to prevent duplicate votes
    
    Returns:
    - IP address string
    """
    # Step 16: Get IP from Request
    # What is this? Getting the user's IP address
    if request.headers.get('X-Forwarded-For'):
        # Explanation:
        # - request.headers.get('X-Forwarded-For') = Gets IP from proxy header
        # - X-Forwarded-For = Header set by proxies/load balancers
        # - Contains the original IP address
        # - Only exists if request went through a proxy
        
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        # Explanation:
        # - .split(',') = Splits by comma (can have multiple IPs)
        # - [0] = Gets first IP (the original one)
        # - .strip() = Removes whitespace
        # - ip = User's IP address
    else:
        # Explanation:
        # - else = If no X-Forwarded-For header
        # - Request didn't go through proxy
        
        ip = request.remote_addr
        # Explanation:
        # - request.remote_addr = Direct IP address from request
        # - ip = User's IP address
        # - This is the IP address of the user's computer
    
    return ip
    # Explanation:
    # - return ip = Returns the IP address
    # - This will be used to track who voted

# Step 17: Create Home Route (GET)
# What is this? The main page that shows all polls
# Think of it like: "When someone visits the home page, show all polls"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows all polls from the database
    """
    # Step 18: Get All Polls from Database
    # What is this? Fetching all polls from the database
    polls = Poll.query.order_by(Poll.date_created.desc()).all()
    # Explanation:
    # - Poll.query = Query object for Poll model
    # - .order_by(Poll.date_created.desc()) = Sort by date, newest first
    # - .desc() = Descending order (newest to oldest)
    # - .all() = Get all polls (returns a list)
    # - polls = List of all Poll objects
    # - This is like saying: "Get all polls, sorted by date, newest first"
    
    # Step 19: Get Voter IP
    # What is this? Getting the current user's IP address
    voter_ip = get_voter_ip()
    # Explanation:
    # - get_voter_ip() = Our helper function to get IP
    # - voter_ip = User's IP address
    # - We'll use this to check if user already voted
    
    # Step 20: Check Which Polls User Has Voted On
    # What is this? Finding which polls the user already voted on
    voted_polls = {}
    # Explanation:
    # - voted_polls = Empty dictionary to store vote information
    # - {} = Empty dictionary
    # - We'll store: {poll_id: option_voted} (which option they voted for)
    
    for poll in polls:
        # Explanation:
        # - for poll in polls = Loop through each poll
        # - poll = Current poll object
        
        vote = Vote.query.filter_by(poll_id=poll.id, voter_ip=voter_ip).first()
        # Explanation:
        # - Vote.query = Query object for Vote model
        # - .filter_by(poll_id=poll.id, voter_ip=voter_ip) = Filter votes
        # - Finds vote for this poll from this IP address
        # - .first() = Get first result (or None if not found)
        # - vote = Vote object if user voted, None if not
        
        if vote:
            # Explanation:
            # - if vote = If user voted on this poll
            # - Only proceed if vote exists
            
            voted_polls[poll.id] = vote.option
            # Explanation:
            # - voted_polls[poll.id] = Stores vote option for this poll
            # - vote.option = Which option they voted for (1 or 2)
            # - Example: voted_polls[1] = 1 (voted for option 1 on poll 1)
            # - This tells us which option the user voted for on each poll
    
    # Step 21: Render Template with Polls
    # What is this? Showing the HTML page with all polls
    return render_template('index.html', polls=polls, voted_polls=voted_polls, voter_ip=voter_ip)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - polls=polls = Passes the polls list to template
    # - voted_polls=voted_polls = Passes vote information to template
    # - voter_ip=voter_ip = Passes IP address to template
    # - In the template, we can use these to display polls and show vote status

# Step 22: Create Vote Route (POST)
# What is this? Handles voting on a poll
# Think of it like: "When user votes, save the vote"
@app.route('/vote/<int:poll_id>', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/vote/<int:poll_id>' = Dynamic route with poll ID
# - <int:poll_id> = Captures poll ID from URL (must be integer)
# - methods=['POST'] = Only accepts POST requests (form submission)
# - Example: /vote/1 → poll_id = 1

def vote(poll_id):
    """
    This function runs when someone votes on a poll
    It saves the vote to the database
    """
    # Step 23: Get Poll from Database
    # What is this? Finding the poll being voted on
    poll = Poll.query.get_or_404(poll_id)
    # Explanation:
    # - Poll.query = Query object for Poll model
    # - .get_or_404(poll_id) = Get poll by ID, or show 404 error if not found
    # - poll_id = The ID from the URL
    # - poll = The Poll object (or 404 error if not found)
    
    # Step 24: Get Selected Option from Form
    # What is this? Getting which option the user voted for
    option = request.form.get('option')
    # Explanation:
    # - request.form.get('option') = Gets value of input/radio named 'option'
    # - option = Which option was selected ('1' or '2')
    # - Example: User clicks "Python" → option = '1'
    # - Example: User clicks "JavaScript" → option = '2'
    
    # Step 25: Validate Option
    # What is this? Checking if a valid option was selected
    if not option or option not in ['1', '2']:
        # Explanation:
        # - if not option = If no option was selected
        # - option not in ['1', '2'] = If option is not 1 or 2
        # - Only proceed if valid option selected
        
        flash('Please select an option!', 'error')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Please select an option!' = Error message
        # - 'error' = Message category
        
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route
        # - User is sent back to home page
    
    # Step 26: Convert Option to Integer
    # What is this? Converting option string to number
    option = int(option)
    # Explanation:
    # - int(option) = Converts string to integer
    # - option = Now an integer (1 or 2)
    # - Example: '1' → 1, '2' → 2
    
    # Step 27: Get Voter IP
    # What is this? Getting the user's IP address
    voter_ip = get_voter_ip()
    # Explanation:
    # - get_voter_ip() = Our helper function
    # - voter_ip = User's IP address
    # - We'll use this to check for duplicate votes
    
    # Step 28: Check if User Already Voted
    # What is this? Preventing duplicate votes
    existing_vote = Vote.query.filter_by(poll_id=poll_id, voter_ip=voter_ip).first()
    # Explanation:
    # - Vote.query = Query object for Vote model
    # - .filter_by(poll_id=poll_id, voter_ip=voter_ip) = Filter votes
    # - Finds vote for this poll from this IP address
    # - .first() = Get first result (or None if not found)
    # - existing_vote = Vote object if user already voted, None if not
    
    if existing_vote:
        # Explanation:
        # - if existing_vote = If user already voted on this poll
        # - Can't vote twice on the same poll!
        
        flash('You have already voted on this poll!', 'error')
        # Explanation:
        # - Shows error message
        # - Tells user they can't vote again
        
        return redirect(url_for('index'))
        # Explanation:
        # - Sends user back to home page
    
    # Step 29: Create New Vote Object
    # What is this? Creating a new vote
    new_vote = Vote(
        poll_id=poll_id,
        voter_ip=voter_ip,
        option=option
    )
    # Explanation:
    # - Vote() = Creates new Vote object
    # - poll_id=poll_id = Sets which poll this vote is for
    # - voter_ip=voter_ip = Sets the voter's IP address
    # - option=option = Sets which option was voted for (1 or 2)
    # - date_created = Automatically set (from model default)
    # - new_vote = The new Vote object (not saved yet)
    
    # Step 30: Update Poll Vote Count
    # What is this? Incrementing the vote count for the selected option
    if option == 1:
        # Explanation:
        # - if option == 1 = If user voted for option 1
        # - Only proceed if option 1 was selected
        
        poll.votes_option1 += 1
        # Explanation:
        # - poll.votes_option1 = Current vote count for option 1
        # - += 1 = Increment by 1
        # - Same as: poll.votes_option1 = poll.votes_option1 + 1
        # - Adds one vote to option 1
    else:
        # Explanation:
        # - else = If user voted for option 2
        # - option must be 2 (we validated it's 1 or 2)
        
        poll.votes_option2 += 1
        # Explanation:
        # - poll.votes_option2 = Current vote count for option 2
        # - += 1 = Increment by 1
        # - Adds one vote to option 2
    
    # Step 31: Save Vote and Update Poll
    # What is this? Saving the vote and updated poll to database
    db.session.add(new_vote)
    # Explanation:
    # - db.session.add(new_vote) = Adds vote to session
    # - Stages it for saving
    
    db.session.commit()
    # Explanation:
    # - db.session.commit() = Saves changes to database
    # - Saves the new vote AND the updated poll vote counts
    # - This is when everything is permanently saved
    
    # Step 32: Show Success Message
    # What is this? Telling user the vote was recorded
    flash('Your vote has been recorded!', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - 'Your vote has been recorded!' = Success message
    # - 'success' = Message category
    
    # Step 33: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is sent back to home page
    # - They'll see updated vote counts!

# Step 34: Create Create Poll Route (GET and POST)
# What is this? Page to create a new poll
# Think of it like: "When someone visits /create-poll, show form to create poll"
@app.route('/create-poll', methods=['GET', 'POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/create-poll' = The URL for creating polls
# - methods=['GET', 'POST'] = Accepts both GET (view form) and POST (submit form)

def create_poll():
    """
    This function runs when someone visits /create-poll
    GET: Shows form to create a poll
    POST: Saves the new poll to database
    """
    # Step 35: Handle Form Submission (POST)
    # What is this? Processing the form when user submits it
    if request.method == 'POST':
        # Explanation:
        # - if request.method == 'POST' = If form was submitted
        # - POST = Form submission
        
        # Step 36: Get Form Data
        # What is this? Getting the data from the form
        question = request.form.get('question', '').strip()
        # Explanation:
        # - request.form.get('question', '') = Gets value of input named 'question'
        # - .strip() = Removes whitespace
        # - question = Variable to hold the poll question
        
        option1 = request.form.get('option1', '').strip()
        # Explanation:
        # - request.form.get('option1', '') = Gets value of input named 'option1'
        # - .strip() = Removes whitespace
        # - option1 = Variable to hold the first option
        
        option2 = request.form.get('option2', '').strip()
        # Explanation:
        # - request.form.get('option2', '') = Gets value of input named 'option2'
        # - .strip() = Removes whitespace
        # - option2 = Variable to hold the second option
        
        # Step 37: Validate Form Data
        # What is this? Checking if user entered valid data
        if not question or not option1 or not option2:
            # Explanation:
            # - if not question or not option1 or not option2 = If any field is empty
            # - Only proceed if all fields are filled
            
            flash('Please fill in all fields!', 'error')
            # Explanation:
            # - Shows error message
            
            return render_template('create_poll.html')
            # Explanation:
            # - Shows form again with error message
        
        # Step 38: Create New Poll Object
        # What is this? Creating a new poll
        new_poll = Poll(
            question=question,
            option1=option1,
            option2=option2
        )
        # Explanation:
        # - Poll() = Creates new Poll object
        # - question=question = Sets the poll question
        # - option1=option1 = Sets the first option
        # - option2=option2 = Sets the second option
        # - votes_option1 and votes_option2 = Automatically set to 0 (default)
        # - date_created = Automatically set (from model default)
        # - new_poll = The new Poll object (not saved yet)
        
        # Step 39: Save to Database
        # What is this? Adding the poll to the database
        db.session.add(new_poll)
        # Explanation:
        # - db.session.add(new_poll) = Adds poll to session
        # - Stages it for saving
        
        db.session.commit()
        # Explanation:
        # - db.session.commit() = Saves changes to database
        # - Actually writes the poll to the database file
        
        # Step 40: Show Success Message
        # What is this? Telling user the poll was created
        flash('Poll created successfully!', 'success')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Poll created successfully!' = Success message
        # - 'success' = Message category
        
        # Step 41: Redirect to Home Page
        # What is this? Sending user back to home page
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route
        # - User is sent back to home page
        # - They'll see the new poll in the list!
    
    # Step 42: Handle Form Display (GET)
    # What is this? Showing the form when user first visits
    return render_template('create_poll.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'create_poll.html' = The template file with the form
    # - This shows the form to create a new poll

# Step 43: Run the Application
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

