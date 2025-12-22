# Random Quote Generator App
# This app displays random inspirational quotes!

# Step 1: Import Flask and random module
# What is this? We're importing Flask and Python's random module
# Think of it like: "Get Flask tools and random number generator"
from flask import Flask, render_template
import random
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - random = Python module for generating random numbers/choices
# - random = Like rolling dice or picking from a hat randomly

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create List of Quotes
# What is this? A collection of inspirational quotes
# Think of it like: "A box full of quotes to pick from"
quotes = [
    # Explanation:
    # - quotes = Variable name for our list
    # - [] = Square brackets create a list
    # - List = Collection of items in order
    # - We'll store all our quotes here
    
    "The only way to do great work is to love what you do. - Steve Jobs",
    # Explanation:
    # - This is a string (text) in the list
    # - Each quote is a separate item
    # - Quotes are separated by commas
    
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    # Explanation:
    # - Another quote string
    # - Each quote has the quote text and author
    
    "Life is what happens to you while you're busy making other plans. - John Lennon",
    # Explanation:
    # - More quotes in the list
    # - We can have as many as we want!
    
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    
    "It is during our darkest moments that we must focus to see the light. - Aristotle",
    
    "The only impossible journey is the one you never begin. - Tony Robbins",
    
    "In the middle of difficulty lies opportunity. - Albert Einstein",
    
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    
    "You miss 100% of the shots you don't take. - Wayne Gretzky",
    
    "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
    
    "Go confidently in the direction of your dreams. Live the life you have imagined. - Henry David Thoreau",
    
    "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
    
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    
    "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
    
    "If you can dream it, you can do it. - Walt Disney",
    
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    
    "The purpose of our lives is to be happy. - Dalai Lama",
    
    "Get busy living or get busy dying. - Stephen King"
]
# Explanation:
# - This closes the list with ]
# - We now have 20 quotes in our list
# - Each quote can be accessed by its position (index)
# - Index starts at 0 (first quote is quotes[0])

# Step 4: Create Home Route
# What is this? The main page that shows a random quote
# Think of it like: "When someone visits the home page, show a random quote"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It picks a random quote and shows it
    """
    # Step 5: Select Random Quote
    # What is this? We're picking one quote randomly from our list
    # Think of it like: "Reach into the hat and pick one quote"
    random_quote = random.choice(quotes)
    # Explanation:
    # - random.choice() = Function that picks random item from list
    # - quotes = Our list of quotes
    # - random.choice(quotes) = Picks one random quote
    # - random_quote = Variable to store the selected quote
    # - Each time this runs, it might pick a different quote!
    
    # Step 6: Render Template with Quote
    # What is this? We're showing the HTML page with the random quote
    # Think of it like: "Show the page and tell it which quote to display"
    return render_template('index.html', quote=random_quote)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - quote=random_quote = Passes the random quote to the template
    # - The first 'quote' = Variable name in the template
    # - random_quote = The actual quote value from Python
    # - In the template, we can use {{ quote }} to display it

# Step 7: Create Route for New Quote (Optional)
# What is this? A route that gets a new random quote
# Think of it like: "When user clicks 'New Quote', get another random one"
@app.route('/new-quote')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/new-quote' = The URL for getting a new quote
# - When someone visits '/new-quote', Flask will run the function below

def new_quote():
    """
    This function runs when someone visits /new-quote
    It picks a new random quote and shows it
    """
    # Step 8: Select New Random Quote
    # What is this? Picking a different random quote
    # Think of it like: "Pick another quote from the hat"
    random_quote = random.choice(quotes)
    # Explanation:
    # - Same as before, picks a random quote
    # - This might be the same quote or a different one
    # - That's the nature of randomness!
    
    # Step 9: Render Template with New Quote
    # What is this? Showing the page with the new quote
    return render_template('index.html', quote=random_quote)
    # Explanation:
    # - Shows the same template
    # - But with a (possibly) different quote
    # - User sees a new random quote

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

