# Posts Blueprint Routes
# All routes related to blog posts

from flask import render_template, request, redirect, url_for, flash
from app.posts import bp
from app import db
from app.models import Post

@bp.route('/')
def list_posts():
    """List all blog posts"""
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('posts/list.html', posts=posts)

@bp.route('/<int:post_id>')
def view_post(post_id):
    """View a single blog post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view.html', post=post)

@bp.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create a new blog post"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author', 'Anonymous')
        
        # Validate
        if not title or not content:
            flash('Title and content are required', 'error')
            return render_template('posts/create.html')
        
        # Create post
        post = Post(
            title=title,
            content=content,
            author=author
        )
        
        # Save to database
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.list_posts'))
    
    return render_template('posts/create.html')

@bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit an existing blog post"""
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        # Update post
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.author = request.form.get('author', 'Anonymous')
        
        # Save changes
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    
    return render_template('posts/edit.html', post=post)

@bp.route('/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Delete post
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts.list_posts'))

