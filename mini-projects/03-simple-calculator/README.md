# Project 3: Simple Calculator 🧮

Welcome to Project 3! This app performs basic mathematical operations using forms!

## What is This Project? 🤔

**Simple Calculator** = A web-based calculator that performs basic math!

**Think of it like:**
- **Real Calculator** = Physical device with buttons
- **Web Calculator** = Same thing, but in your browser!
- **Forms** = How users enter numbers and operations

**Forms = Way for users to input data!**

## What You'll Learn 📚

✅ HTML forms (input fields, dropdowns)
✅ GET vs POST methods
✅ Form handling in Flask
✅ Request object (getting form data)
✅ Input validation
✅ Error handling
✅ Basic calculations
✅ Conditional logic

## What This App Does 🎯

1. **Shows Calculator Form** - User enters two numbers and selects operation
2. **Performs Calculation** - Adds, subtracts, multiplies, or divides
3. **Displays Result** - Shows the answer
4. **Handles Errors** - Shows error messages for invalid input

**Operations:**
- ➕ Addition (+)
- ➖ Subtraction (-)
- ✖️ Multiplication (×)
- ➗ Division (÷)

## Step-by-Step Explanation 📖

### Step 1: Import Flask and request
```python
from flask import Flask, render_template, request
```
**What this does:**
- Gets Flask (for web app)
- Gets render_template (for HTML)
- Gets request (for form data)

**Simple explanation:**
- `request` = Gets data from forms
- Like a mailbox that holds user input!

### Step 2: Create the App
```python
app = Flask(__name__)
```
**What this does:**
- Creates Flask application
- Same as previous projects!

### Step 3: Home Route (GET)
```python
@app.route('/', methods=['GET'])
def index():
    return render_template('calculator.html')
```
**What this does:**
- Shows calculator form
- `methods=['GET']` = Only accepts GET requests
- GET = Request to view a page

**Simple explanation:**
- When someone visits `/`, show the calculator form

### Step 4: Calculate Route (POST)
```python
@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = request.form.get('num1')
    num2 = request.form.get('num2')
    operation = request.form.get('operation')
```
**What this does:**
- Handles form submission
- `methods=['POST']` = Only accepts POST requests
- POST = Request to submit data
- Gets form data using `request.form.get()`

**Simple explanation:**
- When form is submitted, get the numbers and operation
- `request.form` = Dictionary with form data

### Step 5: Validate and Calculate
```python
if operation == 'add':
    result = num1 + num2
elif operation == 'subtract':
    result = num1 - num2
# ... etc
```
**What this does:**
- Checks which operation was selected
- Performs the calculation
- Stores result

**Simple explanation:**
- If user selected "add", add the numbers
- If user selected "subtract", subtract them
- And so on!

## Key Concepts 🎓

### 1. HTML Forms

**What is a form?**
- Way for users to enter data
- Contains input fields, dropdowns, buttons
- Can submit data to server

**Example:**
```html
<form action="/calculate" method="POST">
    <input name="num1" type="number">
    <button type="submit">Calculate</button>
</form>
```

**Simple explanation:**
- Form = Input area
- User enters data
- Submits to server

### 2. GET vs POST Methods

**GET Method:**
- Data appears in URL
- Example: `/page?name=John`
- Used for viewing pages
- Limited data size

**POST Method:**
- Data is hidden
- Sent in request body
- Used for form submissions
- Can send large data

**When to use:**
- GET = Viewing pages, searching
- POST = Submitting forms, creating data

**Simple explanation:**
- GET = "Show me this page"
- POST = "Save this data"

### 3. Request Object

**What is request?**
- Flask object that contains request data
- `request.form` = Form data (POST)
- `request.args` = URL parameters (GET)

**Example:**
```python
num1 = request.form.get('num1')
```
- Gets value of input named 'num1'
- Returns None if not found

**Simple explanation:**
- `request` = Mailbox with user data
- `request.form.get()` = Get specific item

### 4. Input Validation

**What is validation?**
- Checking if input is correct
- Prevents errors
- Shows helpful messages

**Example:**
```python
if not num1 or not num2:
    error = "Please enter both numbers!"
    return render_template('calculator.html', error=error)
```

**Simple explanation:**
- Check if user entered data
- If not, show error message

### 5. Error Handling

**What is error handling?**
- Dealing with errors gracefully
- Using try/except blocks
- Showing user-friendly messages

**Example:**
```python
try:
    num1 = float(num1)
except ValueError:
    error = "Please enter valid numbers!"
```

**Simple explanation:**
- Try to convert to number
- If it fails, show error
- Prevents app from crashing

## How to Run 🚀

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**What you'll see:**
- Calculator form
- Enter two numbers
- Select operation
- Click "Calculate"
- See the result!

## Understanding the Flow 🔄

### Complete Flow:

1. **User visits home page** (`/`)
   - Sees calculator form
   - GET request

2. **User enters data and submits**
   - Fills in numbers
   - Selects operation
   - Clicks "Calculate"
   - POST request to `/calculate`

3. **Flask receives POST request**
   - Gets form data from `request.form`
   - Extracts numbers and operation

4. **Flask validates input**
   - Checks if numbers are valid
   - Checks if operation is selected
   - Handles errors

5. **Flask performs calculation**
   - Does the math
   - Stores result

6. **Flask renders result**
   - Shows calculator form again
   - Displays result
   - Keeps form values

7. **User sees result**
   - Answer appears on screen!

**Simple explanation:**
- User enters → Form submits → Flask gets data → Validates → Calculates → Shows result!

## Files in This Project 📁

```
03-simple-calculator/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── calculator.html # Calculator form and result display
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Key Differences from Previous Projects 🆚

### Project 1 (Hello World):
- Static route
- Returns simple text
- No user input

### Project 2 (Personal Greeting):
- Dynamic route
- URL parameters
- Templates

### Project 3 (Simple Calculator):
- **Forms** (user input)
- **POST method** (form submission)
- **Request object** (getting form data)
- **Validation** (checking input)
- **Error handling** (dealing with errors)

**Progress = You're learning form handling!**

## Common Questions ❓

### Q: What is the difference between GET and POST?
**A:** 
- GET = Data in URL (for viewing)
- POST = Data hidden (for submitting)
- Use POST for forms!

### Q: How does Flask get form data?
**A:** Using `request.form.get('field_name')` - gets value of input field

### Q: What if user enters text instead of number?
**A:** We use try/except to catch the error and show a message

### Q: Why do we validate input?
**A:** To prevent errors and show helpful messages to users

### Q: Can I add more operations?
**A:** Yes! Add more elif conditions in the calculate function

## Practice Exercises 💪

### Exercise 1: Add Power Operation
Add a "power" operation that raises num1 to the power of num2.

### Exercise 2: Add Modulo Operation
Add a "modulo" operation that finds the remainder.

### Exercise 3: Add Clear Button
Add a button to clear the form and start over.

### Exercise 4: Add History
Keep track of previous calculations and display them.

## Next Steps 🎯

After completing this project:

1. ✅ Try different calculations
2. ✅ Add more operations
3. ✅ Experiment with validation
4. ✅ Move to Project 4: Random Quote Generator

## Congratulations! 🎉

You've learned:
- ✅ HTML forms
- ✅ GET vs POST methods
- ✅ Form handling
- ✅ Request object
- ✅ Input validation
- ✅ Error handling
- ✅ Basic calculations

**You're building interactive web apps!** 🚀

---

**Ready for the next project? Try Project 4: Random Quote Generator!**

