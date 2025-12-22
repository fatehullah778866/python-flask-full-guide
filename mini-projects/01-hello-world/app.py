# Hello World Flask App
# This is the simplest Flask application you can build!

# Step 1: Import Flask
# What is this? We're telling Python to use the Flask library
# Think of it like: "Hey Python, I want to use Flask tools!"
from flask import Flask

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application (we can call it anything)
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create a Route
# What is a route? A route is like a web page address
# Think of it like: "When someone visits the home page, show them this"
@app.route('/')
# Explanation:
# - @app.route = This is a "decorator" (special Python feature)
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def hello_world():
    """
    This function runs when someone visits the home page
    It returns the text "Hello, World!"
    """
    # Step 4: Return a Message
    # What is return? It sends something back to the user's browser
    # Think of it like: "Show this text on the webpage"
    return 'Hello, World!'
    # Explanation:
    # - return = Send this back to the user
    # - 'Hello, World!' = The text that will appear on the webpage
    # - This is what the user will see in their browser!

# Step 5: Run the Application
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

