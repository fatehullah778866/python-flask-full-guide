# URL Shortener App (Simple)
# This app shortens long URLs using session storage!

# Step 1: Import Flask and string/random modules
# What is this? We're importing Flask and modules for generating short codes
# Think of it like: "Get Flask tools and random string generator"
from flask import Flask, render_template, request, redirect, url_for, session, flash
import string
import random
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - session = Object for storing data between requests
# - flash = Function to show messages to users
# - string = Module with string constants (letters, digits)
# - random = Module for generating random values
# - We'll use these to create short codes!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Set Secret Key for Sessions
# What is this? A secret key needed for session security
# Think of it like: "A password to protect session data"
app.secret_key = 'your-secret-key-change-this-in-production'
# Explanation:
# - secret_key = Required for sessions to work
# - Sessions need encryption, and this key is used for that
# - In production, use a random, secure key
# - This is like a password that protects your session data

# Step 4: Initialize URLs Dictionary in Session
# What is this? Helper function to set up URLs storage
# Think of it like: "Make sure we have a place to store URLs"
def init_urls():
    """
    Initialize URLs dictionary in session if it doesn't exist
    This ensures we always have a URLs dictionary to work with
    """
    if 'urls' not in session:
        # Explanation:
        # - 'urls' not in session = Check if 'urls' key doesn't exist
        # - session = Dictionary-like object for storing data
        # - If URLs dictionary doesn't exist, create it
        
        session['urls'] = {}
        # Explanation:
        # - session['urls'] = Create 'urls' key in session
        # - {} = Empty dictionary to store URL mappings
        # - This dictionary will hold: {short_code: long_url}
        # - Example: {'abc123': 'https://www.example.com/very/long/url'}

# Step 5: Generate Short Code Function
# What is this? Function to create a random short code
# Think of it like: "Create a random short string to represent the URL"
def generate_short_code(length=6):
    """
    Generate a random short code for URL shortening
    
    Parameters:
    - length: Length of the short code (default: 6 characters)
    
    Returns:
    - Random string of letters and digits
    """
    # Step 6: Define Characters to Use
    # What is this? Characters we'll use to create the short code
    characters = string.ascii_letters + string.digits
    # Explanation:
    # - string.ascii_letters = All letters (a-z, A-Z)
    # - string.digits = All digits (0-9)
    # - + = Concatenation (combines them)
    # - characters = String containing all letters and digits
    # - Example: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    # Step 7: Generate Random Code
    # What is this? Creating a random string of specified length
    short_code = ''.join(random.choice(characters) for _ in range(length))
    # Explanation:
    # - random.choice(characters) = Picks random character from characters string
    # - for _ in range(length) = Repeats 'length' times (e.g., 6 times)
    # - _ = Variable name (we don't use it, just need the loop)
    # - ''.join() = Joins all characters into one string
    # - short_code = Random string like "aB3xY9"
    # - Example: If length=6, might generate "kL9mN2"
    
    return short_code
    # Explanation:
    # - Returns the generated short code
    # - This will be used as the key in our URLs dictionary

# Step 8: Create Home Route (GET)
# What is this? The main page that shows the URL shortener form
# Think of it like: "When someone visits the home page, show the form"
@app.route('/', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - methods=['GET'] = Only accepts GET requests (viewing page)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows the URL shortener form and list of shortened URLs
    """
    # Step 9: Initialize URLs
    # What is this? Make sure URLs dictionary exists
    init_urls()
    # Explanation:
    # - Calls our helper function
    # - Ensures session['urls'] exists
    # - If it doesn't exist, creates empty dictionary
    
    # Step 10: Get URLs from Session
    # What is this? Getting all URL mappings from session storage
    urls = session.get('urls', {})
    # Explanation:
    # - session.get('urls', {}) = Get 'urls' from session
    # - If 'urls' doesn't exist, return empty dictionary {}
    # - urls = Dictionary containing {short_code: long_url}
    # - Example: {'abc123': 'https://example.com', 'xyz789': 'https://google.com'}
    
    # Step 11: Render Template with URLs
    # What is this? Showing the HTML page with URLs
    return render_template('index.html', urls=urls)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - urls=urls = Passes the URLs dictionary to the template
    # - The first 'urls' = Variable name in the template
    # - The second urls = The actual URLs dictionary from Python
    # - In the template, we can use urls to display them

# Step 12: Create Shorten Route (POST)
# What is this? Handles form submission to shorten a URL
# Think of it like: "When user submits form to shorten URL, do this"
@app.route('/shorten', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/shorten' = The URL for shortening URLs
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/shorten', Flask will run the function below

def shorten_url():
    """
    This function runs when a URL is submitted to be shortened
    It generates a short code and stores the mapping
    """
    # Step 13: Initialize URLs
    # What is this? Make sure URLs dictionary exists
    init_urls()
    # Explanation:
    # - Ensures session['urls'] exists before we use it
    
    # Step 14: Get Long URL from Form
    # What is this? Getting the long URL the user entered
    long_url = request.form.get('url', '').strip()
    # Explanation:
    # - request.form.get('url', '') = Gets value of input named 'url'
    # - If 'url' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - long_url = Variable to hold the original URL
    # - Example: User enters "  https://example.com  " → becomes "https://example.com"
    
    # Step 15: Validate URL
    # What is this? Checking if user actually entered a URL
    if not long_url:
        # Explanation:
        # - if not long_url = If long_url is empty
        # - Empty strings are "falsy" in Python
        # - Only proceed if user entered something
        
        flash('Please enter a URL!', 'error')
        # Explanation:
        # - flash() = Function to show temporary message to user
        # - 'Please enter a URL!' = The message text
        # - 'error' = Message category (for styling)
        # - This message will appear on the page
        
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route (home page)
        # - User is sent back to home page to try again
    
    # Step 16: Add Protocol if Missing
    # What is this? Making sure URL has http:// or https://
    # Think of it like: "If URL doesn't start with http, add it"
    if not long_url.startswith(('http://', 'https://')):
        # Explanation:
        # - long_url.startswith() = Checks if URL starts with something
        # - ('http://', 'https://') = Tuple of prefixes to check
        # - If URL doesn't start with http:// or https://, add it
        # - This ensures the URL is valid and clickable
        
        long_url = 'http://' + long_url
        # Explanation:
        # - Adds 'http://' to the beginning of the URL
        # - Example: "example.com" → "http://example.com"
        # - This makes the URL valid and accessible
    
    # Step 17: Generate Short Code
    # What is this? Creating a unique short code for this URL
    short_code = generate_short_code()
    # Explanation:
    # - Calls our generate_short_code() function
    # - Creates a random 6-character code
    # - short_code = Random string like "aB3xY9"
    # - This will be used as the key in our URLs dictionary
    
    # Step 18: Check for Duplicates (Simple Check)
    # What is this? Making sure short code is unique
    # Think of it like: "If this code already exists, generate a new one"
    urls = session.get('urls', {})
    # Explanation:
    # - Gets current URLs dictionary from session
    
    while short_code in urls:
        # Explanation:
        # - while = Loop that continues while condition is true
        # - short_code in urls = Checks if short_code already exists as a key
        # - If it exists, generate a new one
        # - This prevents collisions (two URLs with same short code)
        
        short_code = generate_short_code()
        # Explanation:
        # - Generates a new short code
        # - Loop continues until we get a unique code
    
    # Step 19: Store URL Mapping
    # What is this? Saving the short code and long URL in session
    urls[short_code] = long_url
    # Explanation:
    # - urls = Dictionary from session
    # - [short_code] = Key (the short code)
    # - long_url = Value (the original URL)
    # - This creates the mapping: short_code → long_url
    # - Example: urls['aB3xY9'] = 'https://example.com'
    
    # Step 20: Save to Session
    # What is this? Making sure session changes are saved
    session['urls'] = urls
    # Explanation:
    # - Updates session with modified URLs dictionary
    # - session['urls'] = The URLs dictionary in session
    # - urls = Our modified dictionary
    # - This saves the changes
    
    session.modified = True
    # Explanation:
    # - Forces Flask to save the session
    # - Important for persistence
    # - Ensures changes are saved
    
    # Step 21: Show Success Message
    # What is this? Telling user the URL was shortened successfully
    flash(f'URL shortened successfully! Short code: {short_code}', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - f'...' = f-string (formatted string)
    # - {short_code} = Inserts short code into message
    # - 'success' = Message category (for styling)
    # - Example: "URL shortened successfully! Short code: aB3xY9"
    
    # Step 22: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - After shortening, user is sent back to home page
    # - Home page will now show the new shortened URL

# Step 23: Create Redirect Route
# What is this? Handles clicking on short URL and redirects to original
# Think of it like: "When someone visits /abc123, redirect to the original URL"
@app.route('/<short_code>')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/<short_code>' = Dynamic route that captures short code
# - <short_code> = Variable that captures part of URL
# - Example: /abc123 → short_code = "abc123"
# - When someone visits '/abc123', Flask will run the function below

def redirect_to_url(short_code):
    """
    This function runs when someone visits a short URL
    It looks up the original URL and redirects to it
    """
    # Step 24: Initialize URLs
    # What is this? Make sure URLs dictionary exists
    init_urls()
    # Explanation:
    # - Ensures session['urls'] exists
    
    # Step 25: Get URLs from Session
    # What is this? Getting all URL mappings
    urls = session.get('urls', {})
    # Explanation:
    # - Gets URLs dictionary from session
    # - urls = Dictionary containing {short_code: long_url}
    
    # Step 26: Look Up Original URL
    # What is this? Finding the original URL for this short code
    if short_code in urls:
        # Explanation:
        # - if short_code in urls = Checks if short_code exists as a key
        # - Only proceed if short code exists
        
        original_url = urls[short_code]
        # Explanation:
        # - urls[short_code] = Gets the value (original URL) for this key
        # - original_url = The long URL that was shortened
        # - Example: If short_code = 'abc123' and urls['abc123'] = 'https://example.com'
        # - Then original_url = 'https://example.com'
        
        # Step 27: Redirect to Original URL
        # What is this? Sending user to the original URL
        return redirect(original_url)
        # Explanation:
        # - redirect() = Function to redirect to another URL
        # - original_url = The long URL to redirect to
        # - User's browser will go to the original URL
        # - This is how URL shortening works!
        
    else:
        # Explanation:
        # - else = If short code doesn't exist
        # - Handle the error case
        
        flash(f'Short code "{short_code}" not found!', 'error')
        # Explanation:
        # - Shows error message
        # - f'...' = f-string with short_code
        # - 'error' = Message category
        
        return redirect(url_for('index'))
        # Explanation:
        # - Redirects to home page
        # - User sees error message

# Step 28: Run the Application
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

