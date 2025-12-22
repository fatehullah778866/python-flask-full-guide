# Image Gallery App
# This app displays images in a gallery format!

# Step 1: Import Flask and File Tools
# What is this? We're importing Flask and file handling tools
# Think of it like: "Get Flask tools and file tools"
from flask import Flask, render_template, send_from_directory
import os
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - send_from_directory = Function to serve files (images)
# - os = Module for working with file paths
# - We'll use these to display images in a gallery!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Image Directory
# What is this? Setting up where images are stored
# Think of it like: "Tell Flask where to find images"
IMAGE_FOLDER = 'static/images'
# Explanation:
# - IMAGE_FOLDER = Variable to hold folder name
# - 'static/images' = Path to images folder
# - static = Flask's static files folder
# - images = Subfolder for images
# - This is where we'll store our images

# Step 4: Create Images Directory
# What is this? Making sure the images folder exists
# Think of it like: "Create the folder if it doesn't exist"
if not os.path.exists(IMAGE_FOLDER):
    # Explanation:
    # - if not os.path.exists(IMAGE_FOLDER) = If images folder doesn't exist
    # - os.path.exists() = Checks if path exists
    # - Only create folder if it doesn't exist
    
    os.makedirs(IMAGE_FOLDER)
    # Explanation:
    # - os.makedirs() = Creates directory (folder)
    # - IMAGE_FOLDER = Folder to create
    # - This creates the 'static/images' folder
    # - If folder already exists, does nothing

# Step 5: Get Allowed Image Extensions
# What is this? Defining which image file types are allowed
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# Explanation:
# - ALLOWED_EXTENSIONS = Set of allowed image extensions
# - {'png', 'jpg', 'jpeg', 'gif', 'webp'} = Set of extensions
# - Set = Collection of unique items (no duplicates)
# - Only files with these extensions are considered images
# - Example: 'image.jpg' is allowed, 'document.pdf' is not

# Step 6: Get Images Function
# What is this? Function to get list of all images
# Think of it like: "Find all image files in the images folder"
def get_images():
    """
    Get list of all images in the images folder
    
    Returns:
    - List of image filenames
    """
    # Step 7: Initialize Images List
    # What is this? Creating a list to store image filenames
    images = []
    # Explanation:
    # - images = Empty list to store image filenames
    # - [] = Empty list
    # - We'll add image filenames to this list
    
    # Step 8: Check if Images Folder Exists
    # What is this? Safety check before listing files
    if os.path.exists(IMAGE_FOLDER):
        # Explanation:
        # - if os.path.exists(IMAGE_FOLDER) = If images folder exists
        # - Only proceed if folder exists
        
        # Step 9: Loop Through Files in Folder
        # What is this? Checking each file in the images folder
        for filename in os.listdir(IMAGE_FOLDER):
            # Explanation:
            # - for filename in os.listdir(IMAGE_FOLDER) = Loop through files
            # - os.listdir() = Lists all files in directory
            # - IMAGE_FOLDER = Directory to list
            # - filename = Current filename
            # - Loops through all files in the images folder
            
            # Step 10: Check if File is an Image
            # What is this? Making sure the file is actually an image
            if '.' in filename:
                # Explanation:
                # - if '.' in filename = If filename has an extension
                # - Files need extensions to check type
                # - Only proceed if file has extension
                
                extension = filename.rsplit('.', 1)[1].lower()
                # Explanation:
                # - filename.rsplit('.', 1) = Splits filename from right, max 1 split
                # - [1] = Gets the part after the dot (the extension)
                # - .lower() = Converts to lowercase
                # - extension = File extension (e.g., 'jpg', 'png')
                # - Example: 'image.jpg' → extension = 'jpg'
                
                if extension in ALLOWED_EXTENSIONS:
                    # Explanation:
                    # - if extension in ALLOWED_EXTENSIONS = If extension is allowed
                    # - Checks if extension is in our allowed set
                    # - Only proceed if it's an image file
                    
                    images.append(filename)
                    # Explanation:
                    # - images.append(filename) = Adds filename to images list
                    # - .append() = Method to add item to list
                    # - This image is added to our gallery!
    
    # Step 11: Sort Images
    # What is this? Sorting images alphabetically
    images.sort()
    # Explanation:
    # - images.sort() = Sorts list alphabetically
    # - Modifies the list in place
    # - Images will be displayed in alphabetical order
    # - Example: ['a.jpg', 'b.jpg', 'c.jpg'] instead of random order
    
    # Step 12: Return Images List
    # What is this? Returning the list of image filenames
    return images
    # Explanation:
    # - return images = Returns the list of image filenames
    # - images = List of all image filenames
    # - This is what we'll display in the gallery!

# Step 13: Create Home Route (GET)
# What is this? The main page that shows the image gallery
# Think of it like: "When someone visits the home page, show all images"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows the image gallery
    """
    # Step 14: Get All Images
    # What is this? Getting list of all images
    images = get_images()
    # Explanation:
    # - get_images() = Our function to get all images
    # - images = List of image filenames
    # - Example: ['image1.jpg', 'image2.png', 'image3.gif']
    
    # Step 15: Render Template with Images
    # What is this? Showing the HTML page with the gallery
    return render_template('index.html', images=images)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - images=images = Passes the images list to the template
    # - The first 'images' = Variable name in the template
    # - The second images = The actual images list from Python
    # - In the template, we can use images to display them in a gallery!

# Step 16: Create Image Serving Route
# What is this? Route to serve individual images
# Think of it like: "When someone wants to see an image, send it to them"
@app.route('/images/<filename>')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/images/<filename>' = Dynamic route with filename
# - <filename> = Captures filename from URL
# - Example: /images/photo.jpg → filename = 'photo.jpg'
# - This route serves the actual image files

def serve_image(filename):
    """
    This function runs when someone requests an image
    It sends the image file to the browser
    """
    # Step 17: Send Image File
    # What is this? Sending the image file to the browser
    return send_from_directory(IMAGE_FOLDER, filename)
    # Explanation:
    # - send_from_directory() = Function to send file from directory
    # - IMAGE_FOLDER = Directory where images are stored
    # - filename = Name of image file to send
    # - This sends the image file to the browser
    # - Browser will display the image
    # - Example: /images/photo.jpg sends photo.jpg from static/images/

# Step 18: Run the Application
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
    # - Note: Add some images to static/images/ folder to see them in the gallery!

