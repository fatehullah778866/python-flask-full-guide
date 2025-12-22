# Word Counter App
# This app counts words, characters, sentences, and paragraphs in text!

# Step 1: Import Flask
# What is this? We're importing Flask
# Think of it like: "Get Flask tools"
from flask import Flask, render_template, request
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - We'll use request to get the text from the form

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Count Words Function
# What is this? Function to count words in text
# Think of it like: "Count how many words are in the text"
def count_words(text):
    """
    Count the number of words in text
    
    Parameters:
    - text: The text to count words in
    
    Returns:
    - Number of words (integer)
    """
    # Step 4: Split Text into Words
    # What is this? Breaking text into individual words
    words = text.split()
    # Explanation:
    # - text.split() = Splits text by whitespace (spaces, tabs, newlines)
    # - Returns list of words
    # - words = List of all words
    # - Example: "Hello world" → ['Hello', 'world']
    # - Example: "The quick brown" → ['The', 'quick', 'brown']
    
    # Step 5: Filter Out Empty Strings
    # What is this? Removing empty strings from the list
    words = [word for word in words if word.strip()]
    # Explanation:
    # - [word for word in words if word.strip()] = List comprehension
    # - Loops through words list
    # - word.strip() = Removes whitespace from word
    # - if word.strip() = Only include if word is not empty after stripping
    # - This removes empty strings that might occur from multiple spaces
    # - words = List of non-empty words
    
    return len(words)
    # Explanation:
    # - len(words) = Number of items in words list
    # - Returns the word count
    # - Example: ['Hello', 'world'] → 2 words

# Step 4: Count Characters Function
# What is this? Function to count characters in text
# Think of it like: "Count how many characters are in the text"
def count_characters(text, include_spaces=True):
    """
    Count the number of characters in text
    
    Parameters:
    - text: The text to count characters in
    - include_spaces: Whether to include spaces in count (default: True)
    
    Returns:
    - Number of characters (integer)
    """
    if include_spaces:
        # Explanation:
        # - if include_spaces = If we should count spaces
        # - Default is True (count spaces)
        
        return len(text)
        # Explanation:
        # - len(text) = Length of text string
        # - Includes all characters including spaces
        # - Example: "Hello world" → 11 characters (includes space)
    else:
        # Explanation:
        # - else = If we should NOT count spaces
        
        return len(text.replace(' ', ''))
        # Explanation:
        # - text.replace(' ', '') = Replaces all spaces with empty string
        # - Removes all spaces from text
        # - len() = Counts characters in text without spaces
        # - Example: "Hello world" → 10 characters (no space)

# Step 5: Count Sentences Function
# What is this? Function to count sentences in text
# Think of it like: "Count how many sentences are in the text"
def count_sentences(text):
    """
    Count the number of sentences in text
    
    Parameters:
    - text: The text to count sentences in
    
    Returns:
    - Number of sentences (integer)
    """
    # Step 6: Count Sentence Endings
    # What is this? Finding sentence-ending punctuation
    sentence_endings = ['.', '!', '?']
    # Explanation:
    # - sentence_endings = List of punctuation that ends sentences
    # - . = Period
    # - ! = Exclamation mark
    # - ? = Question mark
    # - These typically mark the end of sentences
    
    count = 0
    # Explanation:
    # - count = Counter variable
    # - Starts at 0
    # - We'll increment it for each sentence found
    
    for char in text:
        # Explanation:
        # - for char in text = Loop through each character in text
        # - char = Current character
        # - Loops through text character by character
        
        if char in sentence_endings:
            # Explanation:
            # - if char in sentence_endings = If character is a sentence ending
            # - Checks if current character is '.', '!', or '?'
            
            count += 1
            # Explanation:
            # - count += 1 = Increment count by 1
            # - Same as count = count + 1
            # - Found a sentence ending, so add 1 to count
    
    return count if count > 0 else 1
    # Explanation:
    # - count if count > 0 else 1 = Ternary operator
    # - If count > 0, return count
    # - If count is 0 (no sentence endings), return 1 (at least one sentence)
    # - This handles cases where text has no punctuation

# Step 6: Count Paragraphs Function
# What is this? Function to count paragraphs in text
# Think of it like: "Count how many paragraphs are in the text"
def count_paragraphs(text):
    """
    Count the number of paragraphs in text
    
    Parameters:
    - text: The text to count paragraphs in
    
    Returns:
    - Number of paragraphs (integer)
    """
    # Step 7: Split by Double Newlines
    # What is this? Finding paragraph breaks
    paragraphs = text.split('\n\n')
    # Explanation:
    # - text.split('\n\n') = Splits text by double newlines
    # - '\n\n' = Two newline characters (paragraph break)
    # - paragraphs = List of paragraphs
    # - Example: "Para 1\n\nPara 2" → ['Para 1', 'Para 2']
    
    # Step 8: Filter Out Empty Paragraphs
    # What is this? Removing empty paragraphs
    paragraphs = [para for para in paragraphs if para.strip()]
    # Explanation:
    # - List comprehension to filter paragraphs
    # - para.strip() = Removes whitespace
    # - if para.strip() = Only include non-empty paragraphs
    # - Removes empty paragraphs from count
    
    return len(paragraphs) if paragraphs else 1
    # Explanation:
    # - len(paragraphs) = Number of paragraphs
    # - if paragraphs else 1 = If no paragraphs, return 1
    # - At least one paragraph exists if text is not empty

# Step 7: Create Home Route (GET)
# What is this? The main page that shows the word counter form
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
    It shows the word counter form
    """
    # Step 8: Render Template
    # What is this? Showing the HTML page with the form
    return render_template('index.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - Flask looks for templates in the 'templates' folder
    # - This will show a form where users can enter text

# Step 8: Create Count Route (POST)
# What is this? Handles form submission to count text
# Think of it like: "When user submits form, count the text and show results"
@app.route('/count', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/count' = The URL for counting text
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/count', Flask will run the function below

def count():
    """
    This function runs when the form is submitted
    It counts words, characters, sentences, and paragraphs
    """
    # Step 9: Get Text from Form
    # What is this? Getting the text the user entered
    text = request.form.get('text', '').strip()
    # Explanation:
    # - request.form.get('text', '') = Gets value of textarea named 'text'
    # - If 'text' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - text = Variable to hold the user's text
    # - Example: User enters "Hello world" → text = "Hello world"
    
    # Step 10: Initialize Statistics Dictionary
    # What is this? Creating dictionary to store all counts
    stats = {}
    # Explanation:
    # - stats = Empty dictionary
    # - We'll store all statistics here
    # - Will contain: words, characters, sentences, paragraphs
    
    # Step 11: Count Words
    # What is this? Counting words in the text
    if text:
        # Explanation:
        # - if text = If text is not empty
        # - Only count if user entered something
        
        stats['words'] = count_words(text)
        # Explanation:
        # - Calls our count_words() function
        # - stats['words'] = Stores word count in dictionary
        # - Example: "Hello world" → stats['words'] = 2
        
        stats['characters_with_spaces'] = count_characters(text, include_spaces=True)
        # Explanation:
        # - Calls count_characters() with include_spaces=True
        # - stats['characters_with_spaces'] = Character count including spaces
        # - Example: "Hello world" → 11 characters (includes space)
        
        stats['characters_without_spaces'] = count_characters(text, include_spaces=False)
        # Explanation:
        # - Calls count_characters() with include_spaces=False
        # - stats['characters_without_spaces'] = Character count excluding spaces
        # - Example: "Hello world" → 10 characters (no space)
        
        stats['sentences'] = count_sentences(text)
        # Explanation:
        # - Calls our count_sentences() function
        # - stats['sentences'] = Number of sentences
        # - Example: "Hello. World!" → 2 sentences
        
        stats['paragraphs'] = count_paragraphs(text)
        # Explanation:
        # - Calls our count_paragraphs() function
        # - stats['paragraphs'] = Number of paragraphs
        # - Example: "Para 1\n\nPara 2" → 2 paragraphs
        
        stats['text'] = text
        # Explanation:
        # - Stores original text in stats
        # - So we can display it in the template
        # - Keeps the text after form submission
    else:
        # Explanation:
        # - else = If text is empty
        
        stats = None
        # Explanation:
        # - stats = None (no statistics)
        # - Will show message to enter text
    
    # Step 12: Render Template with Statistics
    # What is this? Showing the results to the user
    return render_template('index.html', stats=stats)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - stats=stats = Passes statistics dictionary to template
    # - The first 'stats' = Variable name in the template
    # - The second stats = The actual statistics dictionary from Python
    # - In the template, we can use stats to display results

# Step 13: Run the Application
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

