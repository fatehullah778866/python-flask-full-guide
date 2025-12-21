# Your First Flask Application
# This is the simplest Flask app possible!

# Step 1: Import Flask
# This brings Flask into our program so we can use it
from flask import Flask

# Step 2: Create a Flask application
# Think of this as creating a new website
app = Flask(__name__)

# Step 3: Create a route (a page on your website)
# @app.route('/') means "when someone visits the homepage"
@app.route('/')
def hello():
    # This function returns what the user will see
    return 'Hello World!'

# Step 4: Run the application
# This starts your website so people can visit it
if __name__ == '__main__':
    # debug=True means it will show errors and auto-reload when you make changes
    app.run(debug=True)

