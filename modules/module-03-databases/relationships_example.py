# Database Relationships Example
# This shows one-to-many and many-to-many relationships

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "blog.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Association table for many-to-many (Users liking Posts)
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # One-to-many: One user has many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # One-to-many: One user has many comments
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    
    # Many-to-many: Users can like many posts
    liked_posts = db.relationship('Post', secondary=likes, lazy='subquery',
                                backref=db.backref('liked_by', lazy=True))
    
    def __repr__(self):
        return f'<User {self.name}>'

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # One-to-many: One post has many comments
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.text[:50]}>'

# Create tables
with app.app_context():
    db.create_all()

# Route to create sample data
@app.route('/setup')
def setup():
    # Create users
    user1 = User(name="John", email="john@email.com")
    user2 = User(name="Sarah", email="sarah@email.com")
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Create posts
    post1 = Post(title="My First Post", content="This is my first blog post!", user_id=user1.id)
    post2 = Post(title="Python Tips", content="Here are some Python tips...", user_id=user2.id)
    db.session.add_all([post1, post2])
    db.session.commit()
    
    # Create comments
    comment1 = Comment(text="Great post!", post_id=post1.id, user_id=user2.id)
    comment2 = Comment(text="Thanks!", post_id=post1.id, user_id=user1.id)
    db.session.add_all([comment1, comment2])
    db.session.commit()
    
    # User1 likes both posts
    user1.liked_posts.append(post1)
    user1.liked_posts.append(post2)
    # User2 likes post1
    user2.liked_posts.append(post1)
    db.session.commit()
    
    return "Sample data created! Visit /posts to see posts with relationships."

# Route to show all posts with authors
@app.route('/posts')
def show_posts():
    posts = Post.query.all()
    if not posts:
        return "No posts found! Visit /setup first."
    
    result = []
    for post in posts:
        result.append(f"<h3>{post.title}</h3>")
        result.append(f"<p>By: {post.author.name}</p>")
        result.append(f"<p>{post.content}</p>")
        result.append(f"<p>Comments: {len(post.comments)}</p>")
        result.append(f"<p>Likes: {len(post.liked_by)}</p>")
        result.append("<hr>")
    return '<br>'.join(result)

# Route to show post with comments
@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return "Post not found!"
    
    result = []
    result.append(f"<h2>{post.title}</h2>")
    result.append(f"<p>By: {post.author.name}</p>")
    result.append(f"<p>{post.content}</p>")
    result.append(f"<p>Liked by: {len(post.liked_by)} users</p>")
    result.append("<h3>Comments:</h3>")
    
    for comment in post.comments:
        result.append(f"<p><strong>{comment.commenter.name}:</strong> {comment.text}</p>")
    
    return '<br>'.join(result)

# Route to show user's posts
@app.route('/user/<int:user_id>/posts')
def user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found!"
    
    result = []
    result.append(f"<h2>{user.name}'s Posts</h2>")
    result.append(f"<p>Total posts: {len(user.posts)}</p>")
    
    for post in user.posts:
        result.append(f"<h3>{post.title}</h3>")
        result.append(f"<p>{post.content}</p>")
        result.append(f"<p>Comments: {len(post.comments)}</p>")
        result.append("<hr>")
    
    return '<br>'.join(result)

if __name__ == '__main__':
    app.run(debug=True)

