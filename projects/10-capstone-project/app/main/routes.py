# Main Blueprint Routes
# Home page, about page, user profiles

from flask import render_template
from app.main import bp
from app import db
from app.models import User, Post

@bp.route('/')
def index():
    """Home page - shows recent posts"""
    posts = Post.query.order_by(Post.date_created.desc()).limit(10).all()
    return render_template('main/index.html', posts=posts)

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@bp.route('/user/<username>')
def user_profile(username):
    """User profile page"""
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author_id=user.id).order_by(Post.date_created.desc()).all()
    return render_template('main/profile.html', user=user, posts=posts)

