# Simple Calculator App
# This app performs basic mathematical operations using forms!

# Step 1: Import Flask and request
# What is this? We're importing Flask and request object
# Think of it like: "Get Flask tools and the request handler"
from flask import Flask, render_template, request
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data from user
# - request = Like a mailbox that holds user input

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create Home Route (GET method)
# What is this? The main page that shows the calculator form
# Think of it like: "When someone visits the home page, show the calculator"
@app.route('/', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - methods=['GET'] = Only accepts GET requests (default, but explicit)
# - GET = Request to get/view a page (not submit data)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows the calculator form
    """
    # Step 4: Render the Calculator Template
    # What is this? We're showing the calculator HTML page
    # Think of it like: "Show the calculator form"
    return render_template('calculator.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'calculator.html' = The template file to display
    # - Flask looks for templates in the 'templates' folder
    # - This will show a calculator form with input fields

# Step 4: Create Calculate Route (POST method)
# What is this? Handles form submission and performs calculation
# Think of it like: "When user submits the form, calculate and show result"
@app.route('/calculate', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/calculate' = The URL for form submission
# - methods=['POST'] = Only accepts POST requests
# - POST = Request to submit/send data (form submission)
# - When form is submitted, Flask will run the function below

def calculate():
    """
    This function runs when the form is submitted
    It gets the numbers and operation from the form
    Performs the calculation and shows the result
    """
    # Step 5: Get Form Data
    # What is this? We're getting the data the user entered in the form
    # Think of it like: "Get the numbers and operation from the form"
    num1 = request.form.get('num1')
    # Explanation:
    # - request.form = Dictionary containing form data
    # - .get('num1') = Gets the value of input field named 'num1'
    # - num1 = First number from the form (as string)
    # - Form data comes as strings, so we need to convert to float
    
    num2 = request.form.get('num2')
    # Explanation:
    # - Gets the second number from the form
    # - num2 = Second number from the form (as string)
    
    operation = request.form.get('operation')
    # Explanation:
    # - Gets the operation (add, subtract, multiply, divide)
    # - operation = The mathematical operation to perform
    # - This comes from a dropdown/select field in the form
    
    # Step 6: Validate Input
    # What is this? We're checking if the user entered valid data
    # Think of it like: "Make sure the user entered numbers"
    if not num1 or not num2:
        # Explanation:
        # - Checks if num1 or num2 is empty/None
        # - If either is missing, show an error
        # - This prevents errors when user doesn't enter numbers
        
        error = "Please enter both numbers!"
        # Explanation:
        # - error = Error message to show
        # - This will be passed to the template
        
        return render_template('calculator.html', error=error)
        # Explanation:
        # - Shows calculator form again
        # - error=error = Passes error message to template
        # - Template can display the error
    
    # Step 7: Convert to Numbers
    # What is this? Converting string input to numbers for calculation
    # Think of it like: "Convert text to numbers so we can do math"
    try:
        # Explanation:
        # - try = Attempt to do something
        # - If it fails, catch the error (except block)
        # - This handles cases where user enters non-numeric text
        
        num1 = float(num1)
        # Explanation:
        # - float() = Converts string to decimal number
        # - Example: "5.5" → 5.5
        # - If conversion fails, raises ValueError
        
        num2 = float(num2)
        # Explanation:
        # - Converts second number to float
        # - Example: "10" → 10.0
        
    except ValueError:
        # Explanation:
        # - except = If an error occurs
        # - ValueError = Error when conversion fails (not a number)
        # - Example: User enters "abc" instead of a number
        
        error = "Please enter valid numbers!"
        # Explanation:
        # - Error message for invalid input
        
        return render_template('calculator.html', error=error)
        # Explanation:
        # - Shows calculator form again with error message
    
    # Step 8: Perform Calculation
    # What is this? Doing the actual math based on the operation
    # Think of it like: "Do the calculation the user requested"
    result = None
    # Explanation:
    # - result = Variable to store the answer
    # - None = No value yet (will be set based on operation)
    
    if operation == 'add':
        # Explanation:
        # - if = Conditional statement
        # - Checks if operation is 'add'
        # - == = Comparison (is equal to)
        
        result = num1 + num2
        # Explanation:
        # - Addition: num1 + num2
        # - Example: 5 + 3 = 8
        # - Stores result in result variable
        
    elif operation == 'subtract':
        # Explanation:
        # - elif = Else if (another condition)
        # - Checks if operation is 'subtract'
        
        result = num1 - num2
        # Explanation:
        # - Subtraction: num1 - num2
        # - Example: 10 - 3 = 7
        
    elif operation == 'multiply':
        # Explanation:
        # - Another condition check
        
        result = num1 * num2
        # Explanation:
        # - Multiplication: num1 * num2
        # - Example: 4 * 5 = 20
        # - * = Multiplication operator
        
    elif operation == 'divide':
        # Explanation:
        # - Checks if operation is 'divide'
        
        if num2 == 0:
            # Explanation:
            # - Special check for division by zero
            # - Can't divide by zero (mathematical error)
            # - == 0 = Checks if num2 is zero
            
            error = "Cannot divide by zero!"
            # Explanation:
            # - Error message for division by zero
            
            return render_template('calculator.html', error=error)
            # Explanation:
            # - Shows calculator form with error message
            
        result = num1 / num2
        # Explanation:
        # - Division: num1 / num2
        # - Example: 10 / 2 = 5.0
        # - / = Division operator
        # - Only runs if num2 is not zero
        
    else:
        # Explanation:
        # - else = If none of the above conditions are true
        # - Handles invalid operation selection
        
        error = "Please select a valid operation!"
        # Explanation:
        # - Error message for invalid operation
        
        return render_template('calculator.html', error=error)
        # Explanation:
        # - Shows calculator form with error message
    
    # Step 9: Render Result
    # What is this? Showing the calculation result to the user
    # Think of it like: "Show the answer on the calculator"
    return render_template('calculator.html', 
                         result=result, 
                         num1=num1, 
                         num2=num2, 
                         operation=operation)
    # Explanation:
    # - render_template = Shows the calculator template
    # - result=result = Passes the answer to template
    # - num1=num1 = Passes first number (to show in form)
    # - num2=num2 = Passes second number (to show in form)
    # - operation=operation = Passes operation (to show in form)
    # - Template can display the result and keep form values

# Step 10: Run the Application
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

