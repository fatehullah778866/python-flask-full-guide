# Flask-SocketIO Example
# Real-time chat application

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
users = {}

@socketio.on('connect')
def on_connect():
    """When user connects"""
    print('User connected')
    emit('status', {'msg': 'Connected to chat server!'})

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
    username = data.get('username', 'Anonymous')
    users[request.sid] = username
    emit('status', {'msg': f'{username} joined the chat!'}, broadcast=True)
    emit('user_joined', {'username': username}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    """Handle chat message"""
    username = users.get(request.sid, 'Anonymous')
    message = data.get('message', '')
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    if message:
        # Send to everyone
        emit('message', {
            'username': username,
            'message': message,
            'timestamp': timestamp
        }, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    username = users.get(request.sid, 'Anonymous')
    emit('typing', {'username': username}, broadcast=True, include_self=False)

@app.route('/')
def index():
    return render_template('chat.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)

