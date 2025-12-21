# Lesson 10.3: WebSockets - Real-Time Communication! 💬

## What are WebSockets? 🤔

**WebSockets** = Two-way communication between browser and server

Think of it like:
- **Normal HTTP** = Phone call (you call, they answer, hang up)
- **WebSocket** = Walkie-talkie (always connected, can talk anytime!)
- **Real-time** = Instant communication!

**WebSocket = Always-on connection for real-time chat!**

## Why Do We Need WebSockets? 🎯

### The Problem with Normal HTTP:

```
Browser: "Any new messages?"
Server: "No"
    ↓
Browser waits...
    ↓
Browser: "Any new messages?"
Server: "No"
    ↓
Browser waits...
    ↓
(Keeps asking over and over - inefficient!)
```

**Normal HTTP = One-way, have to keep asking!**

### The Solution: WebSocket

```
Browser ←→ Server (connected!)
    ↓
Server: "New message!" (sends instantly!)
    ↓
Browser: "Got it!" (receives instantly!)
    ↓
(Always connected, instant communication!)
```

**WebSocket = Two-way, instant communication!**

## When to Use WebSockets 📋

### Use WebSockets For:

1. **Chat Applications** - Real-time messaging
2. **Live Updates** - Stock prices, scores
3. **Notifications** - Instant alerts
4. **Collaboration** - Multiple users editing
5. **Gaming** - Real-time game updates

**Anything real-time = WebSocket!**

## Flask-SocketIO - Easy WebSockets! 🚀

### What is Flask-SocketIO?

**Flask-SocketIO** = Extension that makes WebSockets easy

Think of it like:
- **Flask-SocketIO** = Helper for WebSockets
- **You** = Just write simple code
- **It** = Handles all the complex stuff!

**Flask-SocketIO = Easy WebSockets for Flask!**

### Installing Flask-SocketIO:

```bash
pip install flask-socketio
```

### Basic WebSocket Example:

```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """When client connects"""
    print('Client connected!')
    emit('message', {'data': 'Welcome!'})

@socketio.on('disconnect')
def handle_disconnect():
    """When client disconnects"""
    print('Client disconnected!')

@socketio.on('message')
def handle_message(data):
    """Handle incoming message"""
    print(f'Received: {data}')
    # Send to all clients
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
```

**That's it! WebSocket server is ready!**

## Client-Side (JavaScript) 💻

### HTML Template:

**`templates/index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
</head>
<body>
    <div id="messages"></div>
    <input type="text" id="messageInput">
    <button onclick="sendMessage()">Send</button>

    <script>
        // Connect to server
        const socket = io();
        
        // Listen for messages
        socket.on('message', function(data) {
            const div = document.createElement('div');
            div.textContent = data.data || data;
            document.getElementById('messages').appendChild(div);
        });
        
        // Send message
        function sendMessage() {
            const input = document.getElementById('messageInput');
            socket.emit('message', {data: input.value});
            input.value = '';
        }
    </script>
</body>
</html>
```

**Client connects and can send/receive messages!**

## WebSocket Events 📡

### Server Events:

```python
@socketio.on('connect')
def on_connect():
    """Client connected"""
    print('User connected')
    emit('status', {'msg': 'Connected!'})

@socketio.on('disconnect')
def on_disconnect():
    """Client disconnected"""
    print('User disconnected')

@socketio.on('message')
def handle_message(data):
    """Handle custom event"""
    emit('response', {'data': f'You said: {data}'})
```

### Client Events (JavaScript):

```javascript
// Connect
socket.on('connect', function() {
    console.log('Connected!');
});

// Disconnect
socket.on('disconnect', function() {
    console.log('Disconnected!');
});

// Custom event
socket.on('response', function(data) {
    console.log('Response:', data);
});

// Send event
socket.emit('message', {data: 'Hello!'});
```

## Broadcasting Messages 📢

### Send to All Clients:

```python
@socketio.on('message')
def handle_message(data):
    # Send to everyone (including sender)
    emit('message', data, broadcast=True)
```

### Send to Everyone Except Sender:

```python
@socketio.on('message')
def handle_message(data):
    # Send to everyone except sender
    emit('message', data, broadcast=True, include_self=False)
```

### Send to Specific Room:

```python
@socketio.on('join')
def on_join(data):
    """Join a room"""
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'Joined room: {room}'})

@socketio.on('message')
def handle_message(data):
    room = data['room']
    # Send only to this room
    emit('message', data, room=room)
```

## Chat Application Example 💬

### Complete Chat App:

**`app.py`:**
```python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
users = {}

@socketio.on('connect')
def on_connect():
    """When user connects"""
    print('User connected')
    emit('status', {'msg': 'Connected to chat!'})

@socketio.on('disconnect')
def on_disconnect():
    """When user disconnects"""
    username = users.get(request.sid)
    if username:
        del users[request.sid]
        emit('user_left', {'username': username}, broadcast=True)
    print('User disconnected')

@socketio.on('join')
def on_join(data):
    """User joins chat"""
    username = data['username']
    users[request.sid] = username
    emit('status', {'msg': f'{username} joined!'}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    """Handle chat message"""
    username = users.get(request.sid, 'Anonymous')
    message = data['message']
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Send to everyone
    emit('message', {
        'username': username,
        'message': message,
        'timestamp': timestamp
    }, broadcast=True)

@app.route('/')
def index():
    return render_template('chat.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
```

**`templates/chat.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Chat Room</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        #messages { height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; }
        .message { margin: 5px 0; }
        .username { font-weight: bold; color: blue; }
        .timestamp { color: gray; font-size: 0.8em; }
    </style>
</head>
<body>
    <h1>Chat Room</h1>
    <div id="messages"></div>
    <input type="text" id="username" placeholder="Your name">
    <input type="text" id="messageInput" placeholder="Type a message...">
    <button onclick="joinChat()">Join</button>
    <button onclick="sendMessage()">Send</button>

    <script>
        const socket = io();
        let username = '';
        
        socket.on('connect', function() {
            console.log('Connected!');
        });
        
        socket.on('status', function(data) {
            addMessage('System', data.msg, 'system');
        });
        
        socket.on('message', function(data) {
            addMessage(data.username, data.message, 'user', data.timestamp);
        });
        
        function joinChat() {
            username = document.getElementById('username').value;
            if (username) {
                socket.emit('join', {username: username});
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value;
            if (message && username) {
                socket.emit('message', {message: message});
                input.value = '';
            }
        }
        
        function addMessage(user, msg, type, timestamp) {
            const div = document.createElement('div');
            div.className = 'message';
            const time = timestamp ? `[${timestamp}] ` : '';
            div.innerHTML = `<span class="timestamp">${time}</span><span class="username">${user}:</span> ${msg}`;
            document.getElementById('messages').appendChild(div);
            document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
        }
    </script>
</body>
</html>
```

**Complete real-time chat application!**

## Rooms - Group Chat 🏠

### Creating Rooms:

```python
@socketio.on('join_room')
def on_join_room(data):
    """Join a specific room"""
    room = data['room']
    username = data['username']
    join_room(room)
    emit('status', {
        'msg': f'{username} joined room {room}'
    }, room=room)

@socketio.on('leave_room')
def on_leave_room(data):
    """Leave a room"""
    room = data['room']
    username = data['username']
    leave_room(room)
    emit('status', {
        'msg': f'{username} left room {room}'
    }, room=room)

@socketio.on('room_message')
def handle_room_message(data):
    """Send message to specific room"""
    room = data['room']
    message = data['message']
    emit('message', {
        'message': message
    }, room=room)
```

**Rooms = Separate chat groups!**

## Namespaces - Organizing Events 📦

### Using Namespaces:

```python
# Default namespace
@socketio.on('message')
def handle_message(data):
    emit('response', data)

# Custom namespace
@socketio.on('message', namespace='/chat')
def handle_chat_message(data):
    emit('response', data)

@socketio.on('message', namespace='/notifications')
def handle_notification(data):
    emit('alert', data)
```

**Client connects to namespace:**
```javascript
const chatSocket = io('/chat');
const notificationSocket = io('/notifications');
```

**Namespaces = Organize different features!**

## Best Practices ✨

### 1. Handle Errors

```python
@socketio.on_error_default
def default_error_handler(e):
    print(f'Error: {e}')
    emit('error', {'msg': 'An error occurred'})
```

### 2. Use Rooms for Organization

```python
# Better organization
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
```

### 3. Validate Data

```python
@socketio.on('message')
def handle_message(data):
    if not data or 'message' not in data:
        emit('error', {'msg': 'Invalid message'})
        return
    # Process message
```

### 4. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app)

@socketio.on('message')
@limiter.limit("10 per minute")
def handle_message(data):
    emit('message', data, broadcast=True)
```

## What You Learned! 📚

✅ What WebSockets are  
✅ Why we need them  
✅ When to use them  
✅ Flask-SocketIO setup  
✅ WebSocket events  
✅ Broadcasting messages  
✅ Chat application  
✅ Rooms and namespaces  
✅ Best practices  

## Key Concepts 💡

1. **WebSocket** = Two-way real-time connection
2. **Flask-SocketIO** = Easy WebSocket extension
3. **Events** = Messages between client and server
4. **Broadcast** = Send to all clients
5. **Rooms** = Group clients together
6. **Namespaces** = Organize events

## What's Next? 🚀

Now that you know WebSockets, let's learn about **Performance Optimization** - making your apps super fast!

---

**Amazing! You can now build real-time apps! 🎉**

