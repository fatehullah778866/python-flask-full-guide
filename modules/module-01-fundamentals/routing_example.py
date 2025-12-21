# Routing Example - Multiple Pages
# This shows how to create different pages (routes) in Flask

from flask import Flask

app = Flask(__name__)

# Homepage - the main page of your website
@app.route('/')
def home():
    return 'Welcome to my website!'

# About page
@app.route('/about')
def about():
    return 'Learn about us!'

# Services page
@app.route('/services')
def services():
    return 'Our services'

# Contact page
@app.route('/contact')
def contact():
    return 'Contact us!'

# You can have multiple routes point to the same function
@app.route('/home')
@app.route('/index')
def home_alternatives():
    return 'Welcome to my website!'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

