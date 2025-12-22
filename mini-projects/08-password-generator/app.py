# Password Generator App
# This app generates secure random passwords with customizable options!

# Step 1: Import Flask and string/random modules
# What is this? We're importing Flask and modules for generating passwords
# Think of it like: "Get Flask tools and password generator tools"
from flask import Flask, render_template, request
import string
import random
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - string = Module with string constants (letters, digits, punctuation)
# - random = Module for generating random values
# - We'll use these to generate secure passwords!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Generate Password Function
# What is this? Function to create a random password
# Think of it like: "Create a random secure password based on user options"
def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                     include_digits=True, include_special=False):
    """
    Generate a random password based on specified criteria
    
    Parameters:
    - length: Length of password (default: 12)
    - include_uppercase: Include uppercase letters (A-Z)
    - include_lowercase: Include lowercase letters (a-z)
    - include_digits: Include digits (0-9)
    - include_special: Include special characters (!@#$%^&*)
    
    Returns:
    - Random password string
    """
    # Step 4: Build Character Set
    # What is this? Creating a string of characters to use in password
    characters = ''
    # Explanation:
    # - characters = Empty string to start
    # - We'll add different character types based on options
    # - This will be the pool of characters to pick from
    
    if include_uppercase:
        # Explanation:
        # - if include_uppercase = If user wants uppercase letters
        # - Only add if option is enabled
        
        characters += string.ascii_uppercase
        # Explanation:
        # - string.ascii_uppercase = All uppercase letters (A-Z)
        # - += = Adds to the characters string
        # - Example: characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if include_lowercase:
        # Explanation:
        # - if include_lowercase = If user wants lowercase letters
        
        characters += string.ascii_lowercase
        # Explanation:
        # - string.ascii_lowercase = All lowercase letters (a-z)
        # - Adds to characters string
        # - Example: characters = "ABCD...XYZabcdef...xyz"
    
    if include_digits:
        # Explanation:
        # - if include_digits = If user wants numbers
        
        characters += string.digits
        # Explanation:
        # - string.digits = All digits (0-9)
        # - Adds to characters string
        # - Example: characters = "...0123456789"
    
    if include_special:
        # Explanation:
        # - if include_special = If user wants special characters
        
        characters += string.punctuation
        # Explanation:
        # - string.punctuation = Special characters (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
        # - Adds to characters string
        # - Example: characters = "...!@#$%^&*()"
    
    # Step 5: Validate Character Set
    # What is this? Making sure we have at least one character type
    if not characters:
        # Explanation:
        # - if not characters = If characters string is empty
        # - This happens if user unchecks all options
        # - We need at least one character type!
        
        return "Error: Please select at least one character type!"
        # Explanation:
        # - Returns error message
        # - User will see this if they uncheck everything
    
    # Step 6: Generate Password
    # What is this? Creating the random password
    password = ''.join(random.choice(characters) for _ in range(length))
    # Explanation:
    # - random.choice(characters) = Picks random character from characters string
    # - for _ in range(length) = Repeats 'length' times (e.g., 12 times)
    # - _ = Variable name (we don't use it, just need the loop)
    # - ''.join() = Joins all characters into one string
    # - password = Random string of specified length
    # - Example: If length=12, might generate "aB3xY9mK2pL8"
    
    return password
    # Explanation:
    # - Returns the generated password
    # - This will be displayed to the user

# Step 7: Create Home Route (GET)
# What is this? The main page that shows the password generator form
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
    It shows the password generator form
    """
    # Step 8: Render Template
    # What is this? Showing the HTML page with the form
    return render_template('index.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - Flask looks for templates in the 'templates' folder
    # - This will show a form where users can configure password options

# Step 9: Create Generate Route (POST)
# What is this? Handles form submission to generate password
# Think of it like: "When user submits form, generate password and show it"
@app.route('/generate', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/generate' = The URL for generating passwords
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/generate', Flask will run the function below

def generate():
    """
    This function runs when the form is submitted
    It gets the options from the form and generates a password
    """
    # Step 10: Get Form Data
    # What is this? Getting the password options the user selected
    length = int(request.form.get('length', 12))
    # Explanation:
    # - request.form.get('length', 12) = Gets value of input named 'length'
    # - If 'length' doesn't exist, returns 12 (default)
    # - int() = Converts string to integer
    # - length = Password length (e.g., 12, 16, 20)
    
    include_uppercase = 'uppercase' in request.form
    # Explanation:
    # - 'uppercase' in request.form = Checks if checkbox named 'uppercase' was checked
    # - If checkbox is checked, returns True
    # - If not checked, returns False
    # - include_uppercase = Boolean (True or False)
    
    include_lowercase = 'lowercase' in request.form
    # Explanation:
    # - Checks if 'lowercase' checkbox was checked
    # - include_lowercase = Boolean
    
    include_digits = 'digits' in request.form
    # Explanation:
    # - Checks if 'digits' checkbox was checked
    # - include_digits = Boolean
    
    include_special = 'special' in request.form
    # Explanation:
    # - Checks if 'special' checkbox was checked
    # - include_special = Boolean
    
    # Step 11: Validate Length
    # What is this? Making sure password length is reasonable
    if length < 4:
        # Explanation:
        # - if length < 4 = If length is less than 4
        # - Very short passwords are not secure
        # - We'll set a minimum
        
        length = 4
        # Explanation:
        # - Sets minimum length to 4
        # - Ensures password is at least somewhat secure
    
    if length > 100:
        # Explanation:
        # - if length > 100 = If length is more than 100
        # - Very long passwords might be impractical
        # - We'll set a maximum
        
        length = 100
        # Explanation:
        # - Sets maximum length to 100
        # - Prevents extremely long passwords
    
    # Step 12: Generate Password
    # What is this? Creating the password with user's options
    password = generate_password(
        length=length,
        include_uppercase=include_uppercase,
        include_lowercase=include_lowercase,
        include_digits=include_digits,
        include_special=include_special
    )
    # Explanation:
    # - Calls our generate_password() function
    # - Passes all the options from the form
    # - password = Generated password string
    # - Example: "aB3xY9mK2pL8" or "Error: Please select..."
    
    # Step 13: Render Template with Password
    # What is this? Showing the password to the user
    return render_template('index.html', 
                         password=password,
                         length=length,
                         include_uppercase=include_uppercase,
                         include_lowercase=include_lowercase,
                         include_digits=include_digits,
                         include_special=include_special)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - password=password = Passes generated password to template
    # - Also passes all options to keep form values
    # - Template can display the password and show form with selected options

# Step 14: Run the Application
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

