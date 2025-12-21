# Simple Blog Application
# This app will be tested

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# Post Model
class Post(db.Model):
    """Blog Post Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Anonymous')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'date_created': self.date_created.isoformat()
        }
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Routes

@app.route('/')
def index():
    """Home page"""
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts as JSON"""
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get single post as JSON"""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    post = Post(
        title=data['title'],
        content=data.get('content', ''),
        author=data.get('author', 'Anonymous')
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a post"""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'author' in data:
        post.author = data['author']
    
    db.session.commit()
    return jsonify(post.to_dict())

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'}), 200

# Helper function for testing
def add_post(title, content, author='Anonymous'):
    """Helper function to add a post"""
    post = Post(title=title, content=content, author=author)
    db.session.add(post)
    db.session.commit()
    return post

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

