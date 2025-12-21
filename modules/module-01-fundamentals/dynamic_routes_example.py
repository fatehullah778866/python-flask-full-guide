# Dynamic Routes Example
# This shows how to create routes that change based on the URL

from flask import Flask

app = Flask(__name__)

# Static route - always the same
@app.route('/')
def home():
    return 'Welcome to my website!'

# Dynamic route - changes based on the name
@app.route('/user/<name>')
def user_profile(name):
    return f'Hello, {name}! Welcome to your profile!'

# Multiple variables in one route
@app.route('/user/<username>/post/<int:post_id>')
def show_post(username, post_id):
    return f'User {username} - Post #{post_id}'

# Using different types
@app.route('/product/<int:product_id>')
def product(product_id):
    return f'Product ID: {product_id}'

@app.route('/price/<float:amount>')
def price(amount):
    return f'Price: ${amount:.2f}'

# Blog example with year and slug
@app.route('/blog/<int:year>/<slug>')
def blog_post(year, slug):
    return f'Blog post from {year}: {slug}'

if __name__ == '__main__':
    app.run(debug=True)

