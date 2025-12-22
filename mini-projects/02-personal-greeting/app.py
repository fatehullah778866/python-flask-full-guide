# Personal Greeting App
# This app greets users by their name using dynamic routes!

# Step 1: Import Flask
# What is this? We're importing Flask and render_template
# Think of it like: "Get Flask tools and template rendering tool"
from flask import Flask, render_template
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - Templates = HTML files with dynamic content

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create Home Route
# What is this? The main page of our website
# Think of it like: "When someone visits the home page, show them this"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows a form where users can enter their name
    """
    # Step 4: Render the Home Template
    # What is this? We're showing an HTML page
    # Think of it like: "Show the home page template"
    return render_template('index.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - Flask looks for templates in the 'templates' folder
    # - This will show a form where users can enter their name

# Step 5: Create Dynamic Greeting Route
# What is this? A route that changes based on the URL
# Think of it like: "When someone visits /hello/John, greet John"
@app.route('/hello/<name>')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/hello/<name>' = Dynamic route with a parameter
# - <name> = A variable that captures part of the URL
# - Example: /hello/John → name = "John"
# - Example: /hello/Sarah → name = "Sarah"

def greet(name):
    """
    This function runs when someone visits /hello/<name>
    It greets the user by the name in the URL
    
    Parameters:
    - name: The name from the URL (captured automatically)
    """
    # Step 6: Render the Greeting Template with Data
    # What is this? We're showing a template and passing data to it
    # Think of it like: "Show the greeting page and tell it the name"
    return render_template('greeting.html', name=name)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'greeting.html' = The template file to display
    # - name=name = Passing the name variable to the template
    # - The first 'name' = Variable name in the template
    # - The second name = Value from the function parameter
    # - In the template, we can use {{ name }} to display it

# Step 7: Run the Application
# What is this? This starts the web server
# Think of it like: "Turn on the website so people can visit it"
if __name__ == '__main__':
    # Explanation:
    # - if __name__ == '__main__' = Only run this if we run the file directly
    # - This prevents it from running if we import this file elsewhere
    
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)
    # - When you run this, you'll see: "Running on http://127.0.0.1:5000"
    # - You can then visit that address in your browser!

