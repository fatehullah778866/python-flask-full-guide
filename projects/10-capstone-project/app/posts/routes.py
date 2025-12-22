# Posts Blueprint Routes
# Create, read, update, delete blog posts

from flask import render_template, request, redirect, url_for, flash, session, abort
from app.posts import bp
from app import db
from app.models import Post, User
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from functools import wraps

# Login Required Decorator
def login_required(f):
    """Decorator to protect routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Forms
class PostForm(FlaskForm):
    """Post creation/editing form"""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200, message='Title must be less than 200 characters')
    ])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Post')

# Routes
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
@login_required
def create_post():
    """Create a new blog post"""
    form = PostForm()
    
    if form.validate_on_submit():
        # Create post
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author_id=session['user_id']
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    
    return render_template('posts/create.html', form=form)

@bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can edit
    if post.author_id != session['user_id']:
        abort(403)  # Forbidden
    
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        # Update post
        post.title = form.title.data
        post.content = form.content.data
        
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    
    return render_template('posts/edit.html', form=form, post=post)

@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post"""
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can delete
    if post.author_id != session['user_id']:
        abort(403)  # Forbidden
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts.list_posts'))

