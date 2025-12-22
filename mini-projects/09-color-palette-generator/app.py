# Color Palette Generator App
# This app generates random color palettes with hex codes!

# Step 1: Import Flask and random module
# What is this? We're importing Flask and random module
# Think of it like: "Get Flask tools and random number generator"
from flask import Flask, render_template
import random
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - random = Module for generating random numbers
# - We'll use random to generate color values!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Generate Random Color Function
# What is this? Function to create a random color
# Think of it like: "Create a random color in hex format"
def generate_random_color():
    """
    Generate a random color in hexadecimal format
    
    Returns:
    - Hex color code (e.g., '#FF5733')
    """
    # Step 4: Generate Random RGB Values
    # What is this? Creating random values for red, green, and blue
    # Think of it like: "Pick random amounts of red, green, and blue"
    r = random.randint(0, 255)
    # Explanation:
    # - random.randint(0, 255) = Random integer between 0 and 255
    # - r = Red component (0 = no red, 255 = full red)
    # - RGB colors use values from 0 to 255
    # - Example: r = 255 (full red)
    
    g = random.randint(0, 255)
    # Explanation:
    # - g = Green component (0 = no green, 255 = full green)
    # - Example: g = 87 (some green)
    
    b = random.randint(0, 255)
    # Explanation:
    # - b = Blue component (0 = no blue, 255 = full blue)
    # - Example: b = 51 (some blue)
    
    # Step 5: Convert to Hexadecimal
    # What is this? Converting RGB values to hex format
    # Think of it like: "Convert numbers to hex color code"
    hex_color = f'#{r:02X}{g:02X}{b:02X}'
    # Explanation:
    # - f'...' = f-string (formatted string)
    # - # = Hex color code prefix
    # - {r:02X} = Formats r as 2-digit uppercase hex
    # - :02X = Format specifier (2 digits, uppercase hex)
    # - 02 = Minimum 2 digits (pads with 0 if needed)
    # - X = Uppercase hexadecimal
    # - Example: r=255, g=87, b=51 → '#FF5733'
    # - Hex = Base 16 number system (0-9, A-F)
    
    return hex_color
    # Explanation:
    # - Returns the hex color code
    # - Example: '#FF5733', '#A1B2C3', '#000000'

# Step 6: Generate Color Palette Function
# What is this? Function to create a palette of colors
# Think of it like: "Create a collection of 5 random colors"
def generate_palette(num_colors=5):
    """
    Generate a palette of random colors
    
    Parameters:
    - num_colors: Number of colors in palette (default: 5)
    
    Returns:
    - List of hex color codes
    """
    # Step 7: Generate Multiple Colors
    # What is this? Creating a list of random colors
    palette = []
    # Explanation:
    # - palette = Empty list to store colors
    # - [] = Empty list
    # - We'll add colors to this list
    
    for _ in range(num_colors):
        # Explanation:
        # - for _ in range(num_colors) = Loop num_colors times
        # - _ = Variable name (we don't use it, just need the loop)
        # - range(num_colors) = Creates sequence 0, 1, 2, ..., num_colors-1
        # - If num_colors=5, loops 5 times
        
        color = generate_random_color()
        # Explanation:
        # - Calls our generate_random_color() function
        # - Gets one random hex color
        # - color = Hex color code like '#FF5733'
        
        palette.append(color)
        # Explanation:
        # - .append() = Adds item to end of list
        # - palette.append(color) = Adds color to palette list
        # - After loop, palette has num_colors colors
    
    return palette
    # Explanation:
    # - Returns the list of colors
    # - Example: ['#FF5733', '#A1B2C3', '#000000', '#FFFFFF', '#123ABC']

# Step 8: Create Home Route (GET)
# What is this? The main page that shows a color palette
# Think of it like: "When someone visits the home page, show a random palette"
@app.route('/', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - methods=['GET'] = Only accepts GET requests (viewing page)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It generates a random color palette and shows it
    """
    # Step 9: Generate Color Palette
    # What is this? Creating a random palette of colors
    palette = generate_palette(5)
    # Explanation:
    # - generate_palette(5) = Creates palette with 5 colors
    # - palette = List of 5 hex color codes
    # - Example: ['#FF5733', '#A1B2C3', '#000000', '#FFFFFF', '#123ABC']
    # - Each time page loads, might get different colors!
    
    # Step 10: Render Template with Palette
    # What is this? Showing the HTML page with the color palette
    return render_template('index.html', palette=palette)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - palette=palette = Passes the color palette to the template
    # - The first 'palette' = Variable name in the template
    # - The second palette = The actual palette list from Python
    # - In the template, we can use palette to display colors

# Step 11: Create New Palette Route (GET)
# What is this? Route to generate a new random palette
# Think of it like: "When user clicks button, generate new palette"
@app.route('/new-palette')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/new-palette' = The URL for getting a new palette
# - When someone visits '/new-palette', Flask will run the function below

def new_palette():
    """
    This function runs when someone visits /new-palette
    It generates a new random color palette
    """
    # Step 12: Generate New Palette
    # What is this? Creating a different random palette
    palette = generate_palette(5)
    # Explanation:
    # - Generates new random palette
    # - Might be same colors or different (random!)
    
    # Step 13: Render Template with New Palette
    # What is this? Showing the page with new palette
    return render_template('index.html', palette=palette)
    # Explanation:
    # - Shows the same template
    # - But with a (possibly) different color palette
    # - User sees new random colors

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

