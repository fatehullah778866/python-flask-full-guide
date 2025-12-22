# API Blueprint Routes
# RESTful API endpoints

from flask import jsonify, request, session, abort
from app.api import bp
from app import db
from app.models import Post, User
from functools import wraps

# Login Required for API
def login_required_api(f):
    """Decorator to protect API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# API Routes

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    }), 200

@bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all posts"""
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a single post"""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200

@bp.route('/posts', methods=['POST'])
@login_required_api
def create_post():
    """Create a new post via API"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    
    post = Post(
        title=data['title'],
        content=data['content'],
        author_id=session['user_id']
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@bp.route('/posts/<int:post_id>', methods=['PUT'])
@login_required_api
def update_post(post_id):
    """Update a post via API"""
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can update
    if post.author_id != session['user_id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    
    db.session.commit()
    
    return jsonify(post.to_dict()), 200

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required_api
def delete_post(post_id):
    """Delete a post via API"""
    post = Post.query.get_or_404(post_id)
    
    # Only post owner can delete
    if post.author_id != session['user_id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'}), 200

@bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a single user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

