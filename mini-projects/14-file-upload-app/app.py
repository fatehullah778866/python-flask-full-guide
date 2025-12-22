# File Upload App
# This app allows users to upload files!

# Step 1: Import Flask and File Tools
# What is this? We're importing Flask and file handling tools
# Think of it like: "Get Flask tools and file tools"
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data and files
# - flash = Function to show messages to users
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - send_from_directory = Function to serve files
# - os = Module for working with file paths
# - secure_filename = Function to make filenames safe
# - We'll use these to handle file uploads!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure File Upload Settings
# What is this? Setting up where to store uploaded files
# Think of it like: "Tell Flask where to save uploaded files"
UPLOAD_FOLDER = 'uploads'
# Explanation:
# - UPLOAD_FOLDER = Variable to hold folder name
# - 'uploads' = Name of folder to store uploaded files
# - This folder will contain all uploaded files
# - We'll create this folder if it doesn't exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Explanation:
# - app.config = Flask configuration dictionary
# - 'UPLOAD_FOLDER' = Setting name for upload folder
# - UPLOAD_FOLDER = The folder path
# - Flask will use this to know where to save files

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Explanation:
# - 'MAX_CONTENT_LENGTH' = Maximum file size allowed
# - 16 * 1024 * 1024 = 16 megabytes (16 MB)
# - 1024 = 1 kilobyte (KB)
# - 1024 * 1024 = 1 megabyte (MB)
# - 16 * 1024 * 1024 = 16 MB
# - This limits file size to prevent huge uploads
# - You can change this to allow larger or smaller files

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
# Explanation:
# - ALLOWED_EXTENSIONS = Set of allowed file extensions
# - {'txt', 'pdf', 'png', ...} = Set of allowed extensions
# - Set = Collection of unique items (no duplicates)
# - Only files with these extensions can be uploaded
# - This is a security measure to prevent dangerous files
# - Example: 'document.pdf' is allowed, 'script.exe' is not

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions and flash messages
# - Required for flash messages to work
# - In production, use a long, random, secret key

# Step 4: Create Uploads Directory
# What is this? Making sure the uploads folder exists
# Think of it like: "Create the folder if it doesn't exist"
if not os.path.exists(UPLOAD_FOLDER):
    # Explanation:
    # - if not os.path.exists(UPLOAD_FOLDER) = If uploads folder doesn't exist
    # - os.path.exists() = Checks if path exists
    # - Only create folder if it doesn't exist
    
    os.makedirs(UPLOAD_FOLDER)
    # Explanation:
    # - os.makedirs() = Creates directory (folder)
    # - UPLOAD_FOLDER = Folder to create
    # - This creates the 'uploads' folder
    # - If folder already exists, does nothing

# Step 5: Check Allowed File Extension Function
# What is this? Function to check if file extension is allowed
# Think of it like: "Is this file type allowed?"
def allowed_file(filename):
    """
    Check if file has an allowed extension
    
    Parameters:
    - filename: Name of the file
    
    Returns:
    - True if extension is allowed, False otherwise
    """
    # Step 6: Get File Extension
    # What is this? Extracting the file extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    # Explanation:
    # - '.' in filename = Checks if filename contains a dot (has extension)
    # - filename.rsplit('.', 1) = Splits filename from right, max 1 split
    # - [1] = Gets the part after the dot (the extension)
    # - .lower() = Converts to lowercase (PDF = pdf)
    # - in ALLOWED_EXTENSIONS = Checks if extension is in allowed set
    # - Returns True if extension is allowed, False otherwise
    # - Example: 'document.pdf' → extension = 'pdf' → True (pdf is allowed)
    # - Example: 'script.exe' → extension = 'exe' → False (exe is not allowed)

# Step 7: Create Home Route (GET)
# What is this? The main page that shows the file upload form
# Think of it like: "When someone visits the home page, show the form"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows the file upload form and list of uploaded files
    """
    # Step 8: Get List of Uploaded Files
    # What is this? Getting all files in the uploads folder
    uploaded_files = []
    # Explanation:
    # - uploaded_files = Empty list to store file names
    # - We'll add file names to this list
    
    if os.path.exists(UPLOAD_FOLDER):
        # Explanation:
        # - if os.path.exists(UPLOAD_FOLDER) = If uploads folder exists
        # - Safety check before listing files
        
        uploaded_files = os.listdir(UPLOAD_FOLDER)
        # Explanation:
        # - os.listdir() = Lists all files in directory
        # - UPLOAD_FOLDER = Directory to list
        # - uploaded_files = List of all file names in uploads folder
        # - Example: ['document.pdf', 'image.jpg', 'file.txt']
    
    # Step 9: Render Template with Files
    # What is this? Showing the HTML page with files list
    return render_template('index.html', files=uploaded_files)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - files=uploaded_files = Passes the files list to the template
    # - The first 'files' = Variable name in the template
    # - The second uploaded_files = The actual files list from Python
    # - In the template, we can use files to display them

# Step 10: Create Upload Route (POST)
# What is this? Handles file upload
# Think of it like: "When user uploads file, save it"
@app.route('/upload', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/upload' = The URL for uploading files
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/upload', Flask will run the function below

def upload_file():
    """
    This function runs when a file is uploaded
    It validates and saves the uploaded file
    """
    # Step 11: Check if File was Uploaded
    # What is this? Checking if user actually uploaded a file
    if 'file' not in request.files:
        # Explanation:
        # - 'file' not in request.files = If no file was uploaded
        # - request.files = Dictionary of uploaded files
        # - 'file' = Name of the file input in the form
        # - If no file uploaded, show error
        
        flash('No file selected!', 'error')
        # Explanation:
        # - flash() = Function to show temporary message
        # - 'No file selected!' = Error message
        # - 'error' = Message category
        
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route
        # - User is sent back to form
    
    # Step 12: Get Uploaded File
    # What is this? Getting the file from the form
    file = request.files['file']
    # Explanation:
    # - request.files['file'] = Gets the uploaded file
    # - 'file' = Name of the file input in the form
    # - file = File object (not the actual file content yet)
    # - This is like getting the file from the form
    
    # Step 13: Check if Filename is Empty
    # What is this? Checking if user selected a file
    if file.filename == '':
        # Explanation:
        # - file.filename = Name of the uploaded file
        # - '' = Empty string (no file selected)
        # - If filename is empty, no file was selected
        
        flash('No file selected!', 'error')
        # Explanation:
        # - Shows error message
        
        return redirect(url_for('index'))
        # Explanation:
        # - Sends user back to form
    
    # Step 14: Validate File Extension
    # What is this? Checking if file type is allowed
    if file and allowed_file(file.filename):
        # Explanation:
        # - if file = If file exists
        # - allowed_file(file.filename) = Checks if extension is allowed
        # - Only proceed if file exists AND extension is allowed
        
        # Step 15: Secure the Filename
        # What is this? Making the filename safe
        filename = secure_filename(file.filename)
        # Explanation:
        # - secure_filename() = Function to make filename safe
        # - file.filename = Original filename
        # - secure_filename() = Removes dangerous characters
        # - Example: 'my file.pdf' → 'my_file.pdf'
        # - Example: '../../hack.txt' → 'hack.txt' (removes path traversal)
        # - This prevents security issues!
        # - filename = Safe version of filename
        
        # Step 16: Save File
        # What is this? Saving the file to disk
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Explanation:
        # - os.path.join() = Joins path parts correctly
        # - app.config['UPLOAD_FOLDER'] = Upload folder path ('uploads')
        # - filename = Safe filename
        # - file_path = Full path to save file
        # - Example: 'uploads/document.pdf'
        # - This creates the full file path
        
        file.save(file_path)
        # Explanation:
        # - file.save() = Saves the file to disk
        # - file_path = Where to save the file
        # - This actually writes the file to the uploads folder
        # - The file is now permanently saved!
        
        # Step 17: Show Success Message
        # What is this? Telling user the file was uploaded
        flash(f'File "{filename}" uploaded successfully!', 'success')
        # Explanation:
        # - flash() = Shows temporary message
        # - f'File "{filename}" uploaded successfully!' = Success message
        # - {filename} = Name of uploaded file
        # - 'success' = Message category
        
    else:
        # Explanation:
        # - else = If file extension is not allowed
        
        # Step 18: Show Error Message
        # What is this? Telling user the file type is not allowed
        flash('File type not allowed! Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS), 'error')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'File type not allowed!' = Error message
        # - ', '.join(ALLOWED_EXTENSIONS) = Joins allowed extensions with commas
        # - Example: 'txt, pdf, png, jpg'
        # - Shows user which file types are allowed
        # - 'error' = Message category
    
    # Step 19: Redirect to Home Page
    # What is this? Sending user back to home page
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is sent back to upload form
    # - They'll see the success or error message

# Step 20: Create Download Route
# What is this? Route to download uploaded files
# Think of it like: "When someone visits /download/filename, send them the file"
@app.route('/download/<filename>')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/download/<filename>' = Dynamic route with filename
# - <filename> = Captures filename from URL
# - Example: /download/document.pdf → filename = 'document.pdf'

def download_file(filename):
    """
    This function runs when someone wants to download a file
    It sends the file to the user's browser
    """
    # Step 21: Send File
    # What is this? Sending the file to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # Explanation:
    # - send_from_directory() = Function to send file from directory
    # - app.config['UPLOAD_FOLDER'] = Directory where files are stored
    # - filename = Name of file to send
    # - This sends the file to the user's browser
    # - Browser will download or display the file
    # - Example: PDFs might open in browser, images display, etc.

# Step 22: Run the Application
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

