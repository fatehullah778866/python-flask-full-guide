# Personal Portfolio Website
# This is your main Flask application file

from flask import Flask, render_template

# Create Flask app
# __name__ tells Flask where to find files
app = Flask(__name__)

# Home page route
# When someone visits http://localhost:5000/, this function runs
@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

# About page route
# When someone visits http://localhost:5000/about, this function runs
@app.route('/about')
def about():
    # Render the about.html template
    return render_template('about.html')

# Projects page route
# When someone visits http://localhost:5000/projects, this function runs
@app.route('/projects')
def projects():
    # Render the projects.html template
    return render_template('projects.html')

# Contact page route
# When someone visits http://localhost:5000/contact, this function runs
@app.route('/contact')
def contact():
    # Render the contact.html template
    return render_template('contact.html')

# This runs the app when you execute this file
if __name__ == '__main__':
    # debug=True means you'll see errors in the browser
    # This is helpful when learning!
    app.run(debug=True)

