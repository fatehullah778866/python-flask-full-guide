# Search Functionality App
# This app demonstrates search functionality with filtering!

# Step 1: Import Flask
# What is this? We're importing Flask
# Think of it like: "Get Flask tools"
from flask import Flask, render_template, request
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data and query parameters
# - We'll use request to get search queries

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create Sample Data
# What is this? Creating a list of items to search through
# Think of it like: "Create a list of items to search"
sample_data = [
    {'id': 1, 'title': 'Python Programming', 'category': 'Programming', 'description': 'Learn Python programming language'},
    {'id': 2, 'title': 'Web Development', 'category': 'Web', 'description': 'Build websites with HTML, CSS, and JavaScript'},
    {'id': 3, 'title': 'Data Science', 'category': 'Science', 'description': 'Analyze data with Python and machine learning'},
    {'id': 4, 'title': 'Flask Framework', 'category': 'Programming', 'description': 'Build web applications with Flask'},
    {'id': 5, 'title': 'JavaScript Basics', 'category': 'Programming', 'description': 'Learn JavaScript for web development'},
    {'id': 6, 'title': 'Database Design', 'category': 'Database', 'description': 'Design and manage databases'},
    {'id': 7, 'title': 'API Development', 'category': 'Web', 'description': 'Create RESTful APIs'},
    {'id': 8, 'title': 'Machine Learning', 'category': 'Science', 'description': 'Introduction to machine learning algorithms'},
    {'id': 9, 'title': 'SQL Queries', 'category': 'Database', 'description': 'Learn SQL for database queries'},
    {'id': 10, 'title': 'React Framework', 'category': 'Web', 'description': 'Build user interfaces with React'}
]
# Explanation:
# - sample_data = List of dictionaries
# - Each dictionary = One item with id, title, category, description
# - id = Unique identifier
# - title = Item title
# - category = Item category
# - description = Item description
# - This is our "database" to search through
# - In a real app, this would come from a database!

# Step 4: Search Function
# What is this? Function to search through the data
# Think of it like: "Find items that match the search query"
def search_items(query, category_filter=None):
    """
    Search items by query and optional category filter
    
    Parameters:
    - query: Search query string
    - category_filter: Optional category to filter by
    
    Returns:
    - List of matching items
    """
    # Step 5: Initialize Results List
    # What is this? Creating a list to store search results
    results = []
    # Explanation:
    # - results = Empty list to store matching items
    # - [] = Empty list
    # - We'll add matching items to this list
    
    # Step 6: Normalize Search Query
    # What is this? Making search case-insensitive
    query_lower = query.lower() if query else ''
    # Explanation:
    # - query.lower() = Converts query to lowercase
    # - if query = Only convert if query exists
    # - '' = Empty string if no query
    # - query_lower = Lowercase version of query
    # - This makes search case-insensitive (Python = python)
    # - Example: "Python" → "python"
    
    # Step 7: Loop Through All Items
    # What is this? Checking each item to see if it matches
    for item in sample_data:
        # Explanation:
        # - for item in sample_data = Loop through each item
        # - item = Current item being checked
        # - Loops through all items in sample_data
        
        # Step 8: Check Category Filter
        # What is this? Filtering by category if specified
        if category_filter and item['category'].lower() != category_filter.lower():
            # Explanation:
            # - if category_filter = If a category filter was specified
            # - item['category'].lower() = Item's category in lowercase
            # - category_filter.lower() = Filter category in lowercase
            # - != = Not equal operator
            # - If categories don't match, skip this item
            # - Only proceed if category matches (or no filter)
            
            continue
            # Explanation:
            # - continue = Skip to next item in loop
            # - Don't check this item further
            # - Move to next item
        
        # Step 9: Check if Query Matches
        # What is this? Checking if search query matches item
        if query_lower:
            # Explanation:
            # - if query_lower = If there's a search query
            # - Only search if query exists
            
            # Step 10: Check Title Match
            # What is this? Checking if query is in title
            title_match = query_lower in item['title'].lower()
            # Explanation:
            # - query_lower in item['title'].lower() = Checks if query is in title
            # - .lower() = Converts to lowercase for case-insensitive search
            # - in = Checks if string contains substring
            # - title_match = True if query found in title, False otherwise
            # - Example: query="python", title="Python Programming" → True
            
            # Step 11: Check Description Match
            # What is this? Checking if query is in description
            description_match = query_lower in item['description'].lower()
            # Explanation:
            # - query_lower in item['description'].lower() = Checks if query is in description
            # - .lower() = Converts to lowercase
            # - description_match = True if query found in description, False otherwise
            # - Example: query="web", description="Build websites" → True
            
            # Step 12: Check if Item Matches
            # What is this? Item matches if query is in title OR description
            if title_match or description_match:
                # Explanation:
                # - if title_match or description_match = If query found in title OR description
                # - or = Logical OR operator
                # - Item matches if query is anywhere in title or description
                # - Only proceed if item matches
                
                results.append(item)
                # Explanation:
                # - results.append(item) = Adds item to results list
                # - .append() = Method to add item to list
                # - This item matches the search!
        else:
            # Explanation:
            # - else = If there's no search query
            # - Show all items (if no query, show everything)
            
            results.append(item)
            # Explanation:
            # - results.append(item) = Adds item to results list
            # - If no query, include all items (or filtered by category)
    
    # Step 13: Return Results
    # What is this? Returning the list of matching items
    return results
    # Explanation:
    # - return results = Returns the list of matching items
    # - results = List of items that match the search
    # - This is what we'll display to the user!

# Step 14: Create Home Route (GET)
# What is this? The main page that shows the search form
# Think of it like: "When someone visits the home page, show the search form"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows the search form and search results
    """
    # Step 15: Get Search Query from URL
    # What is this? Getting the search query from URL parameters
    query = request.args.get('q', '').strip()
    # Explanation:
    # - request.args.get('q', '') = Gets 'q' parameter from URL
    # - request.args = Dictionary of URL query parameters
    # - 'q' = Parameter name (query)
    # - '' = Default value if 'q' doesn't exist
    # - .strip() = Removes whitespace
    # - query = Search query string
    # - Example: /?q=python → query = "python"
    # - Example: /?q=web%20development → query = "web development"
    
    # Step 16: Get Category Filter from URL
    # What is this? Getting the category filter from URL parameters
    category_filter = request.args.get('category', '').strip()
    # Explanation:
    # - request.args.get('category', '') = Gets 'category' parameter from URL
    # - 'category' = Parameter name
    # - '' = Default value if 'category' doesn't exist
    # - .strip() = Removes whitespace
    # - category_filter = Category to filter by
    # - Example: /?category=Programming → category_filter = "Programming"
    # - If empty, no category filter
    
    # Step 17: Get All Unique Categories
    # What is this? Getting list of all categories for the filter dropdown
    categories = sorted(set(item['category'] for item in sample_data))
    # Explanation:
    # - item['category'] for item in sample_data = Gets all categories (list comprehension)
    # - set() = Converts to set (removes duplicates)
    # - sorted() = Sorts categories alphabetically
    # - categories = List of unique categories
    # - Example: ['Database', 'Programming', 'Science', 'Web']
    # - This is for the category filter dropdown
    
    # Step 18: Perform Search
    # What is this? Searching for items that match the query
    results = search_items(query, category_filter if category_filter else None)
    # Explanation:
    # - search_items() = Our search function
    # - query = Search query string
    # - category_filter if category_filter else None = Category filter or None
    # - results = List of matching items
    # - If no query and no filter, returns all items
    
    # Step 19: Render Template with Results
    # What is this? Showing the HTML page with search results
    return render_template('index.html', 
                         results=results, 
                         query=query, 
                         category_filter=category_filter,
                         categories=categories)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - results=results = Passes search results to template
    # - query=query = Passes search query to template (to show in input)
    # - category_filter=category_filter = Passes category filter to template
    # - categories=categories = Passes categories list to template (for dropdown)
    # - In the template, we can use these to display search form and results!

# Step 20: Run the Application
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

