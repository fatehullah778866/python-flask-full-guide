# Real-time Chat App
# This app allows users to chat in real-time using WebSockets!

# Step 1: Import Flask and SocketIO Tools
# What is this? We're importing Flask and WebSocket tools
# Think of it like: "Get Flask tools and real-time communication tools"
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains request data
# - session = Object for storing data between requests
# - SocketIO = WebSocket library for real-time communication
# - emit = Function to send messages to clients
# - join_room = Function to join a chat room
# - leave_room = Function to leave a chat room
# - datetime = Module for working with dates and times
# - WebSockets = Technology for real-time, two-way communication!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Secret Key
# What is this? Setting up secret key for sessions
# Think of it like: "Set a secret password for security"
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions to work
# - In production, use a long, random string!

# Step 4: Initialize SocketIO
# What is this? Creating the SocketIO object for WebSocket communication
# Think of it like: "Create a real-time communication manager"
socketio = SocketIO(app, cors_allowed_origins="*")
# Explanation:
# - SocketIO(app) = Creates SocketIO object connected to Flask app
# - cors_allowed_origins="*" = Allows connections from any origin
# - CORS = Cross-Origin Resource Sharing (security feature)
# - "*" = Allow all origins (for development only!)
# - socketio = Our WebSocket manager
# - This enables real-time, two-way communication!

# Step 5: Store Connected Users
# What is this? Keeping track of who is online
# Think of it like: "A list of people currently in the chat"
connected_users = {}
# Explanation:
# - connected_users = Dictionary to store online users
# - {} = Empty dictionary
# - Format: {session_id: username}
# - Example: {'abc123': 'John', 'def456': 'Jane'}
# - We'll use this to track who is online

# Step 6: Create Home Route (GET)
# What is this? The main page where users enter their name
# Think of it like: "When someone visits the home page, show login form"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows a form to enter username
    """
    # Step 7: Render Template
    # What is this? Showing the HTML page
    return render_template('index.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - This shows the login form

# Step 7: Create Chat Route (GET)
# What is this? The chat page where users can send messages
# Think of it like: "When someone visits /chat, show the chat interface"
@app.route('/chat')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/chat' = The chat page URL
# - When someone visits '/chat', Flask will run the function below

def chat():
    """
    This function runs when someone visits the chat page
    It shows the chat interface
    """
    # Step 8: Check if User is Logged In
    # What is this? Making sure user entered their name
    if 'username' not in session:
        # Explanation:
        # - if 'username' not in session = If username is not stored
        # - session = Flask session object (stores data between requests)
        # - Only proceed if user has entered their name
        
        return redirect('/')
        # Explanation:
        # - redirect('/') = Sends user back to home page
        # - User must enter their name first
    
    # Step 9: Render Chat Template
    # What is this? Showing the chat interface
    return render_template('chat.html', username=session['username'])
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'chat.html' = The template file with chat interface
    # - username=session['username'] = Passes username to template
    # - The template can use this to display the username

# Step 10: Handle Login (POST)
# What is this? Processing username when user submits form
# Think of it like: "When user enters name, save it and go to chat"
@app.route('/login', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/login' = The URL for login
# - methods=['POST'] = Only accepts POST requests (form submission)

def login():
    """
    This function runs when user submits the login form
    It saves the username and redirects to chat
    """
    # Step 11: Get Username from Form
    # What is this? Getting the username the user entered
    username = request.form.get('username', '').strip()
    # Explanation:
    # - request.form.get('username', '') = Gets value of input named 'username'
    # - If 'username' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - username = Variable to hold the username
    
    # Step 12: Validate Username
    # What is this? Making sure user entered a name
    if not username:
        # Explanation:
        # - if not username = If username is empty
        # - Empty strings are "falsy" in Python
        # - Only proceed if username is provided
        
        return redirect('/')
        # Explanation:
        # - redirect('/') = Sends user back to home page
        # - User must enter a username
    
    # Step 13: Save Username in Session
    # What is this? Storing the username so we remember it
    session['username'] = username
    # Explanation:
    # - session['username'] = Stores username in Flask session
    # - session = Dictionary-like object that persists between requests
    # - username = The username entered by user
    # - Now we can access it later with session['username']
    
    # Step 14: Redirect to Chat
    # What is this? Sending user to the chat page
    return redirect('/chat')
    # Explanation:
    # - redirect('/chat') = Sends user to chat page
    # - User is now logged in and can start chatting!

# Step 15: Handle WebSocket Connection
# What is this? When a user connects via WebSocket
# Think of it like: "When someone joins the chat, welcome them"
@socketio.on('connect')
# Explanation:
# - @socketio.on('connect') = Decorator for connection event
# - 'connect' = Event name (automatically fired when client connects)
# - When a WebSocket connection is established, this function runs

def handle_connect():
    """
    This function runs when a user connects via WebSocket
    It adds them to the chat room and notifies others
    """
    # Step 16: Get Username from Session
    # What is this? Getting the username of the person who connected
    username = session.get('username')
    # Explanation:
    # - session.get('username') = Gets username from session
    # - .get() = Safe way to get value (returns None if not found)
    # - username = The username of the connected user
    
    # Step 17: Check if Username Exists
    # What is this? Making sure user is logged in
    if not username:
        # Explanation:
        # - if not username = If username doesn't exist
        # - User must be logged in to use chat
        
        return False
        # Explanation:
        # - return False = Rejects the connection
        # - User cannot connect without username
    
    # Step 18: Join Chat Room
    # What is this? Adding user to the main chat room
    join_room('general')
    # Explanation:
    # - join_room('general') = Adds user to 'general' chat room
    # - Room = A group where messages are shared
    # - 'general' = Name of the main chat room
    # - All users join the same room (simple chat)
    # - Messages sent to 'general' are received by everyone in that room
    
    # Step 19: Store User Connection
    # What is this? Remembering that this user is connected
    connected_users[request.sid] = username
    # Explanation:
    # - request.sid = Unique session ID for this WebSocket connection
    # - Each connection gets a unique ID
    # - connected_users[request.sid] = username = Stores username with session ID
    # - Example: connected_users['abc123'] = 'John'
    # - We can now look up who is connected by their session ID
    
    # Step 20: Notify Others of New User
    # What is this? Telling everyone that someone joined
    emit('user_joined', {
        'username': username,
        'message': f'{username} joined the chat',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, room='general', include_self=False)
    # Explanation:
    # - emit() = Function to send message to clients
    # - 'user_joined' = Event name (clients listen for this)
    # - Dictionary = Data to send (username, message, timestamp)
    # - room='general' = Send to everyone in 'general' room
    # - include_self=False = Don't send to the person who just joined
    # - This notifies other users (not the new user) that someone joined
    
    # Step 21: Send Welcome Message to New User
    # What is this? Welcoming the new user
    emit('message', {
        'username': 'System',
        'message': f'Welcome to the chat, {username}!',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })
    # Explanation:
    # - emit() = Function to send message
    # - 'message' = Event name (clients listen for this)
    # - Dictionary = Welcome message data
    # - No room specified = Only sends to this user
    # - This welcomes the new user

# Step 22: Handle WebSocket Disconnection
# What is this? When a user disconnects from WebSocket
# Think of it like: "When someone leaves the chat, say goodbye"
@socketio.on('disconnect')
# Explanation:
# - @socketio.on('disconnect') = Decorator for disconnection event
# - 'disconnect' = Event name (automatically fired when client disconnects)
# - When a WebSocket connection closes, this function runs

def handle_disconnect():
    """
    This function runs when a user disconnects
    It removes them from the chat and notifies others
    """
    # Step 23: Get Username of Disconnected User
    # What is this? Finding out who left
    username = connected_users.get(request.sid)
    # Explanation:
    # - connected_users.get(request.sid) = Gets username by session ID
    # - request.sid = Session ID of the disconnected connection
    # - username = The username of the person who left (or None)
    
    # Step 24: Check if Username Exists
    # What is this? Making sure we have a username
    if username:
        # Explanation:
        # - if username = If username exists
        # - Only proceed if we found the username
        
        # Step 25: Remove User from Connected Users
        # What is this? Forgetting that this user is connected
        del connected_users[request.sid]
        # Explanation:
        # - del connected_users[request.sid] = Removes user from dictionary
        # - request.sid = Session ID of disconnected user
        # - Now this user is no longer in our connected users list
        
        # Step 26: Leave Chat Room
        # What is this? Removing user from the chat room
        leave_room('general')
        # Explanation:
        # - leave_room('general') = Removes user from 'general' room
        # - User is no longer part of the chat room
        # - They won't receive messages anymore
        
        # Step 27: Notify Others of User Leaving
        # What is this? Telling everyone that someone left
        emit('user_left', {
            'username': username,
            'message': f'{username} left the chat',
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }, room='general')
        # Explanation:
        # - emit() = Function to send message
        # - 'user_left' = Event name (clients listen for this)
        # - Dictionary = Data about user leaving
        # - room='general' = Send to everyone in 'general' room
        # - This notifies all users that someone left

# Step 28: Handle Incoming Messages
# What is this? When a user sends a chat message
# Think of it like: "When someone types a message, send it to everyone"
@socketio.on('send_message')
# Explanation:
# - @socketio.on('send_message') = Decorator for message event
# - 'send_message' = Event name (client sends this when user types message)
# - When client emits 'send_message', this function runs

def handle_message(data):
    """
    This function runs when a user sends a message
    It broadcasts the message to all users in the chat room
    """
    # Step 29: Get Username from Session
    # What is this? Finding out who sent the message
    username = session.get('username')
    # Explanation:
    # - session.get('username') = Gets username from session
    # - username = The username of the person who sent the message
    
    # Step 30: Get Message Text from Data
    # What is this? Getting the actual message text
    message = data.get('message', '').strip()
    # Explanation:
    # - data = Dictionary sent from client
    # - data.get('message', '') = Gets 'message' value from dictionary
    # - .strip() = Removes whitespace
    # - message = The message text
    
    # Step 31: Validate Message
    # What is this? Making sure message is not empty
    if not message or not username:
        # Explanation:
        # - if not message or not username = If message or username is empty
        # - Only proceed if both exist
        
        return
        # Explanation:
        # - return = Exit function early
        # - Don't send empty messages
    
    # Step 32: Broadcast Message to All Users
    # What is this? Sending the message to everyone in the chat room
    emit('message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, room='general')
    # Explanation:
    # - emit() = Function to send message
    # - 'message' = Event name (clients listen for this)
    # - Dictionary = Message data (username, message text, timestamp)
    # - room='general' = Send to everyone in 'general' room
    # - This broadcasts the message to all connected users
    # - Everyone in the chat will see this message!

# Step 33: Run the Application
# What is this? This starts the web server with WebSocket support
# Think of it like: "Turn on the website with real-time chat support"
if __name__ == '__main__':
    # Explanation:
    # - if __name__ == '__main__' = Only run this if we run the file directly
    # - This prevents it from running if we import this file elsewhere
    
    socketio.run(app, debug=True)
    # Explanation:
    # - socketio.run(app, debug=True) = Starts Flask app with SocketIO
    # - app = Our Flask application
    # - debug=True = Show errors in the browser (helpful for learning!)
    # - This starts both the web server AND WebSocket server
    # - When you run this, you'll see: "Running on http://127.0.0.1:5000"
    # - You can then visit that address in your browser!
    # - Multiple users can connect and chat in real-time!

