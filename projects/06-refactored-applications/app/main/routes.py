# Main Blueprint Routes
# Home page and about page routes

from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    """Home page"""
    return render_template('main/index.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

