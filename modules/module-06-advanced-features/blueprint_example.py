# Blueprints Example
# This shows how to organize Flask apps using blueprints

from flask import Flask, Blueprint

# Create main app
app = Flask(__name__)

# ===== AUTH BLUEPRINT =====
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return '''
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <button type="submit">Login</button>
    </form>
    '''

@auth_bp.route('/register')
def register():
    return '''
    <h2>Register</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="email" name="email" placeholder="Email"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <button type="submit">Register</button>
    </form>
    '''

@auth_bp.route('/logout')
def logout():
    return 'Logged out!'

# ===== POSTS BLUEPRINT =====
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/')
def list_posts():
    return '''
    <h2>All Posts</h2>
    <ul>
        <li>Post 1</li>
        <li>Post 2</li>
        <li>Post 3</li>
    </ul>
    '''

@posts_bp.route('/<int:post_id>')
def show_post(post_id):
    return f'<h2>Post {post_id}</h2><p>This is post number {post_id}</p>'

# ===== COMMENTS BLUEPRINT =====
comments_bp = Blueprint('comments', __name__, url_prefix='/posts/<int:post_id>/comments')

@comments_bp.route('/')
def list_comments(post_id):
    return f'<h2>Comments for Post {post_id}</h2><p>No comments yet.</p>'

@comments_bp.route('/<int:comment_id>')
def show_comment(post_id, comment_id):
    return f'<h2>Comment {comment_id} for Post {post_id}</h2>'

# ===== MAIN APP =====
@app.route('/')
def home():
    return '''
    <h1>Blog Homepage</h1>
    <ul>
        <li><a href="/auth/login">Login</a></li>
        <li><a href="/auth/register">Register</a></li>
        <li><a href="/posts">All Posts</a></li>
    </ul>
    '''

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)

if __name__ == '__main__':
    app.run(debug=True)

