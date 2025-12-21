# Blog Application with Database
# This Flask app creates a complete blog with CRUD operations

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)

# Database configuration
# SQLite database stored in a file called blog.db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# Blog Post Model
# This defines what a blog post looks like in the database
class Post(db.Model):
    """Blog Post Model"""
    # Primary key - unique ID for each post
    id = db.Column(db.Integer, primary_key=True)
    
    # Post title (required, max 200 characters)
    title = db.Column(db.String(200), nullable=False)
    
    # Post content (required, can be very long)
    content = db.Column(db.Text, nullable=False)
    
    # Author name (required, max 100 characters)
    author = db.Column(db.String(100), nullable=False)
    
    # Date when post was created (automatically set)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Date when post was last updated (automatically updated)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """How to display the post object"""
        return f'<Post {self.title}>'

# Home page - List all posts
@app.route('/')
def index():
    """Display all blog posts"""
    # Get all posts from database, newest first
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)

# View single post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Display a single blog post"""
    # Get post by ID, show 404 if not found
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# Create new post
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create a new blog post"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        
        # Create new post object
        post = Post(
            title=title,
            content=content,
            author=author
        )
        
        # Add to database session
        db.session.add(post)
        # Save to database
        db.session.commit()
        
        # Redirect to home page
        return redirect(url_for('index'))
    
    # Show create form
    return render_template('create.html')

# Edit existing post
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit an existing blog post"""
    # Get post from database
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        # Update post with new data
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.author = request.form.get('author')
        post.date_updated = datetime.utcnow()
        
        # Save changes to database
        db.session.commit()
        
        # Redirect to view the updated post
        return redirect(url_for('view_post', post_id=post.id))
    
    # Show edit form with current post data
    return render_template('edit.html', post=post)

# Delete post
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete a blog post"""
    # Get post from database
    post = Post.query.get_or_404(post_id)
    
    # Delete post from database
    db.session.delete(post)
    # Save changes
    db.session.commit()
    
    # Redirect to home page
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Start the Flask development server
    app.run(debug=True)

