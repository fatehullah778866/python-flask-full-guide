# Pagination System App
# This app demonstrates pagination (splitting data into pages)!

# Step 1: Import Flask and Math Tools
# What is this? We're importing Flask and math tools
# Think of it like: "Get Flask tools and math tools"
from flask import Flask, render_template, request, url_for
import math
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains request data (like page number)
# - url_for = Function to generate URLs
# - math = Module for mathematical operations
# - We'll use math.ceil() to calculate total pages
# - math.ceil() = Rounds up to nearest whole number

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create Sample Data
# What is this? Creating a list of items to paginate
# Think of it like: "Create a list of items to split into pages"
sample_data = []
# Explanation:
# - sample_data = Empty list to start
# - We'll fill it with sample items

# Step 4: Generate Sample Items
# What is this? Creating many items for pagination demonstration
# Think of it like: "Create lots of items so we can split them into pages"
for i in range(1, 101):
    # Explanation:
    # - for i in range(1, 101) = Loop from 1 to 100
    # - range(1, 101) = Creates sequence: 1, 2, 3, ..., 100
    # - i = Current number in loop
    # - We'll create 100 items (good for pagination demo!)
    
    sample_data.append({
        'id': i,
        # Explanation:
        # - 'id' = Unique identifier
        # - i = Current loop number (1, 2, 3, ..., 100)
        # - Each item gets a unique ID
        
        'title': f'Item {i}',
        # Explanation:
        # - 'title' = Item title
        # - f'Item {i}' = Formatted string with item number
        # - Example: "Item 1", "Item 2", "Item 3", ...
        
        'description': f'This is the description for item number {i}'
        # Explanation:
        # - 'description' = Item description
        # - f'This is the description for item number {i}' = Formatted string
        # - Example: "This is the description for item number 1"
    })
    # Explanation:
    # - sample_data.append() = Adds item to list
    # - After loop, we have 100 items in the list!

# Step 5: Pagination Helper Function
# What is this? Function to calculate pagination information
# Think of it like: "Calculate which items to show on which page"
def paginate(items, page=1, per_page=10):
    """
    Paginate a list of items
    
    Parameters:
    - items: List of items to paginate
    - page: Current page number (default: 1)
    - per_page: Items per page (default: 10)
    
    Returns:
    - Dictionary with pagination info and items for current page
    """
    # Step 6: Calculate Total Pages
    # What is this? Figuring out how many pages we need
    total_items = len(items)
    # Explanation:
    # - len(items) = Number of items in list
    # - total_items = Total number of items
    # - Example: If 100 items, total_items = 100
    
    total_pages = math.ceil(total_items / per_page)
    # Explanation:
    # - math.ceil() = Rounds up to nearest whole number
    # - total_items / per_page = Items divided by items per page
    # - total_pages = Number of pages needed
    # - Example: 100 items / 10 per page = 10 pages
    # - Example: 95 items / 10 per page = 9.5 → 10 pages (rounded up)
    # - math.ceil(9.5) = 10
    
    # Step 7: Validate Page Number
    # What is this? Making sure page number is valid
    if page < 1:
        # Explanation:
        # - if page < 1 = If page number is less than 1
        # - Page numbers start at 1, not 0
        # - Only proceed if page is valid
        
        page = 1
        # Explanation:
        # - Sets page to 1 (first page)
        # - Prevents invalid page numbers
    
    if page > total_pages and total_pages > 0:
        # Explanation:
        # - if page > total_pages = If page number is too high
        # - and total_pages > 0 = And there are pages
        # - Can't go to page 11 if only 10 pages exist
        
        page = total_pages
        # Explanation:
        # - Sets page to last page
        # - Prevents going beyond available pages
    
    # Step 8: Calculate Start and End Index
    # What is this? Figuring out which items to show on this page
    start_index = (page - 1) * per_page
    # Explanation:
    # - (page - 1) = Page number minus 1 (because we start at 0, not 1)
    # - * per_page = Multiply by items per page
    # - start_index = Index where current page starts
    # - Example: Page 1, 10 per page → (1-1) * 10 = 0 (start at index 0)
    # - Example: Page 2, 10 per page → (2-1) * 10 = 10 (start at index 10)
    # - Example: Page 3, 10 per page → (3-1) * 10 = 20 (start at index 20)
    
    end_index = start_index + per_page
    # Explanation:
    # - start_index + per_page = Start index plus items per page
    # - end_index = Index where current page ends (not inclusive)
    # - Example: Page 1 → start=0, end=10 (items 0-9, which is 10 items)
    # - Example: Page 2 → start=10, end=20 (items 10-19, which is 10 items)
    # - Note: end_index is not inclusive (we use it in slicing)
    
    # Step 9: Get Items for Current Page
    # What is this? Extracting the items that belong on this page
    page_items = items[start_index:end_index]
    # Explanation:
    # - items[start_index:end_index] = Slicing the list
    # - Gets items from start_index to end_index (not including end_index)
    # - page_items = List of items for current page
    # - Example: items[0:10] = First 10 items (indices 0-9)
    # - Example: items[10:20] = Next 10 items (indices 10-19)
    
    # Step 10: Return Pagination Info
    # What is this? Returning all pagination information
    return {
        'items': page_items,
        # Explanation:
        # - 'items' = Items for current page
        # - page_items = List of items to display
        
        'page': page,
        # Explanation:
        # - 'page' = Current page number
        # - Used to show "Page X of Y"
        
        'per_page': per_page,
        # Explanation:
        # - 'per_page' = Items per page
        # - Used in calculations
        
        'total_items': total_items,
        # Explanation:
        # - 'total_items' = Total number of items
        # - Used to show "Showing X of Y items"
        
        'total_pages': total_pages,
        # Explanation:
        # - 'total_pages' = Total number of pages
        # - Used to show "Page X of Y"
        
        'has_prev': page > 1,
        # Explanation:
        # - 'has_prev' = Whether there's a previous page
        # - page > 1 = True if not on first page
        # - Used to show/hide "Previous" button
        
        'has_next': page < total_pages,
        # Explanation:
        # - 'has_next' = Whether there's a next page
        # - page < total_pages = True if not on last page
        # - Used to show/hide "Next" button
        
        'prev_page': page - 1 if page > 1 else None,
        # Explanation:
        # - 'prev_page' = Previous page number
        # - page - 1 = Previous page number
        # - if page > 1 else None = Only if not on first page
        # - Used for "Previous" button link
        
        'next_page': page + 1 if page < total_pages else None
        # Explanation:
        # - 'next_page' = Next page number
        # - page + 1 = Next page number
        # - if page < total_pages else None = Only if not on last page
        # - Used for "Next" button link
    }
    # Explanation:
    # - Returns dictionary with all pagination information
    # - Template can use this to display items and pagination controls

# Step 11: Create Home Route (GET)
# What is this? The main page that shows paginated items
# Think of it like: "When someone visits the home page, show items on page 1"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows paginated items
    """
    # Step 12: Get Page Number from URL
    # What is this? Getting which page the user wants to see
    page = request.args.get('page', 1, type=int)
    # Explanation:
    # - request.args.get('page', 1, type=int) = Gets 'page' parameter from URL
    # - request.args = Dictionary of URL query parameters
    # - 'page' = Parameter name
    # - 1 = Default value if 'page' doesn't exist (first page)
    # - type=int = Converts to integer
    # - page = Current page number
    # - Example: /?page=1 → page = 1
    # - Example: /?page=5 → page = 5
    # - Example: / (no page) → page = 1 (default)
    
    # Step 13: Get Items Per Page from URL
    # What is this? Getting how many items per page user wants
    per_page = request.args.get('per_page', 10, type=int)
    # Explanation:
    # - request.args.get('per_page', 10, type=int) = Gets 'per_page' parameter
    # - 'per_page' = Parameter name
    # - 10 = Default value (10 items per page)
    # - type=int = Converts to integer
    # - per_page = Items per page
    # - Example: /?per_page=20 → per_page = 20
    # - Example: / (no per_page) → per_page = 10 (default)
    
    # Step 14: Validate Per Page
    # What is this? Making sure per_page is reasonable
    if per_page < 1:
        # Explanation:
        # - if per_page < 1 = If per_page is less than 1
        # - Can't show 0 or negative items per page!
        
        per_page = 10
        # Explanation:
        # - Sets per_page to 10 (default)
        # - Prevents invalid values
    
    if per_page > 50:
        # Explanation:
        # - if per_page > 50 = If per_page is more than 50
        # - Too many items per page might be slow
        
        per_page = 50
        # Explanation:
        # - Sets per_page to 50 (maximum)
        # - Prevents too many items per page
    
    # Step 15: Get Paginated Data
    # What is this? Getting items for current page and pagination info
    pagination = paginate(sample_data, page=page, per_page=per_page)
    # Explanation:
    # - paginate() = Our pagination helper function
    # - sample_data = All items to paginate
    # - page=page = Current page number
    # - per_page=per_page = Items per page
    # - pagination = Dictionary with pagination info and items
    
    # Step 16: Render Template with Pagination
    # What is this? Showing the HTML page with paginated items
    return render_template('index.html', pagination=pagination)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - pagination=pagination = Passes pagination dictionary to template
    # - The first 'pagination' = Variable name in the template
    # - The second pagination = The actual pagination dictionary from Python
    # - In the template, we can use pagination.items, pagination.page, etc.

# Step 17: Run the Application
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

