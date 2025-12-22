# Multi-language Support App
# This app supports multiple languages using Flask-Babel!

# Step 1: Import Flask and Babel Tools
# What is this? We're importing Flask and internationalization tools
# Think of it like: "Get Flask tools and translation tools"
from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, gettext as _, ngettext, format_date, format_datetime
from datetime import datetime
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains request data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - session = Object for storing data between requests
# - Babel = Flask extension for internationalization (i18n)
# - gettext = Function to translate text (singular)
# - ngettext = Function to translate text (plural)
# - format_date = Function to format dates according to locale
# - format_datetime = Function to format dates/times according to locale
# - datetime = Module for working with dates and times
# - We'll use Babel to support multiple languages!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Babel
# What is this? Setting up language support
# Think of it like: "Tell Flask which languages to support"
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'BABEL_DEFAULT_LOCALE' = Default language setting
# - 'en' = English (default language)
# - If user doesn't select a language, use English

app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es', 'fr', 'de']
# Explanation:
# - 'BABEL_SUPPORTED_LOCALES' = List of supported languages
# - ['en', 'es', 'fr', 'de'] = English, Spanish, French, German
# - These are the languages our app supports
# - Users can switch between these languages

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions to work

# Step 4: Initialize Babel
# What is this? Creating the Babel object
# Think of it like: "Create a translation manager"
babel = Babel(app)
# Explanation:
# - Babel(app) = Creates Babel object connected to Flask app
# - babel = Our translation manager
# - This enables multi-language support!

# Step 5: Function to Get User's Preferred Language
# What is this? Function to determine which language to use
# Think of it like: "Figure out what language the user wants"
@babel.localeselector
# Explanation:
# - @babel.localeselector = Decorator for language selection
# - Babel calls this function to determine which language to use
# - This function runs automatically when Flask needs to know the language

def get_locale():
    """
    Get the user's preferred language
    
    Returns:
    - Language code (e.g., 'en', 'es', 'fr', 'de')
    """
    # Step 6: Check Session for Language Preference
    # What is this? Checking if user selected a language
    if 'language' in session:
        # Explanation:
        # - if 'language' in session = If language is stored in session
        # - session = Flask session object
        # - User may have selected a language previously
        # - Only proceed if language exists in session
        
        return session['language']
        # Explanation:
        # - return session['language'] = Returns stored language
        # - Example: 'es' for Spanish, 'fr' for French
        # - This uses the user's selected language
    
    # Step 7: Check Request Accept-Language Header
    # What is this? Getting language from browser settings
    language = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    # Explanation:
    # - request.accept_languages = Browser's preferred languages
    # - .best_match() = Finds best match from supported languages
    # - app.config['BABEL_SUPPORTED_LOCALES'] = Our supported languages
    # - language = Best matching language (or None)
    # - Example: Browser prefers Spanish → language = 'es'
    
    if language:
        # Explanation:
        # - if language = If a matching language was found
        # - Only proceed if language exists
        
        return language
        # Explanation:
        # - return language = Returns the matched language
        # - Uses browser's preferred language
    
    # Step 8: Return Default Language
    # What is this? Using default language if nothing else found
    return app.config['BABEL_DEFAULT_LOCALE']
    # Explanation:
    # - return app.config['BABEL_DEFAULT_LOCALE'] = Returns default language
    # - 'en' = English (default)
    # - This is used if no language preference is found

# Step 9: Create Home Route (GET)
# What is this? The main page
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows content in the user's selected language
    """
    # Step 10: Get Current Date/Time
    # What is this? Getting current date and time for formatting demo
    current_datetime = datetime.utcnow()
    # Explanation:
    # - datetime.utcnow() = Gets current date and time
    # - current_datetime = Current date/time object
    # - We'll format this according to the selected language
    
    # Step 11: Render Template
    # What is this? Showing the HTML page
    return render_template('index.html', current_datetime=current_datetime, _=_)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = The template file to display
    # - current_datetime=current_datetime = Passes date/time to template
    # - _=_ = Passes translation function to template
    # - Template will use translation functions to display text in correct language

# Step 12: Create Set Language Route (POST)
# What is this? Handles language selection
@app.route('/set-language', methods=['POST'])
def set_language():
    """
    This function handles language selection
    It saves the selected language in the session
    """
    # Step 13: Get Selected Language from Form
    # What is this? Getting the language the user selected
    language = request.form.get('language', 'en')
    # Explanation:
    # - request.form.get('language', 'en') = Gets value of input/select named 'language'
    # - If 'language' doesn't exist, returns 'en' (default)
    # - language = Selected language code
    # - Example: User selects Spanish → language = 'es'
    
    # Step 14: Validate Language
    # What is this? Making sure the language is supported
    if language in app.config['BABEL_SUPPORTED_LOCALES']:
        # Explanation:
        # - if language in app.config['BABEL_SUPPORTED_LOCALES'] = If language is supported
        # - Checks if language is in our supported list
        # - Only proceed if language is valid
        
        session['language'] = language
        # Explanation:
        # - session['language'] = language = Stores language in session
        # - This saves the user's language preference
        # - Session persists across requests
        # - Next time user visits, their language will be remembered
    
    # Step 15: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is sent back to home page
    # - Page will now display in the selected language!

# Step 16: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

