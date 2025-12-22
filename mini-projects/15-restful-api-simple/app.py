# RESTful API (Simple) App
# This app creates a simple RESTful API for managing items!

# Step 1: Import Flask and JSON Tools
# What is this? We're importing Flask and JSON tools
# Think of it like: "Get Flask tools and JSON tools"
from flask import Flask, jsonify, request
# Explanation:
# - Flask = The main Flask class
# - jsonify = Function to create JSON responses
# - request = Object that contains request data
# - We'll use jsonify to send JSON data (API format)
# - JSON = JavaScript Object Notation (data format for APIs)

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Create In-Memory Data Storage
# What is this? Creating a list to store items (like a simple database)
# Think of it like: "Create a list to store our items"
items = []
# Explanation:
# - items = Empty list to store items
# - [] = Empty list
# - We'll store items here (like a simple database)
# - In a real app, you'd use a database, but this is simpler for learning!
# - Each item will be a dictionary with id, name, and description

# Step 4: Initialize with Sample Data
# What is this? Adding some sample items to start with
# Think of it like: "Add some example items so we have data to work with"
items = [
    {'id': 1, 'name': 'Item 1', 'description': 'This is the first item'},
    {'id': 2, 'name': 'Item 2', 'description': 'This is the second item'},
    {'id': 3, 'name': 'Item 3', 'description': 'This is the third item'}
]
# Explanation:
# - items = List of dictionaries
# - Each dictionary = One item with id, name, description
# - id = Unique identifier (1, 2, 3, ...)
# - name = Item name
# - description = Item description
# - This gives us some data to work with!

# Step 5: Helper Function to Get Next ID
# What is this? Function to generate the next unique ID
# Think of it like: "Find the next available ID number"
def get_next_id():
    """
    Get the next available ID for a new item
    
    Returns:
    - Next ID number (integer)
    """
    if not items:
        # Explanation:
        # - if not items = If items list is empty
        # - Empty lists are "falsy" in Python
        # - If no items, start with ID 1
        
        return 1
        # Explanation:
        # - Returns 1 as the first ID
        # - First item gets ID 1
    
    # Step 6: Find Maximum ID
    # What is this? Finding the highest ID currently used
    max_id = max(item['id'] for item in items)
    # Explanation:
    # - max() = Function to find maximum value
    # - item['id'] for item in items = Gets all IDs from items
    # - This is a list comprehension (gets all IDs)
    # - max_id = Highest ID number
    # - Example: If items have IDs [1, 2, 3], max_id = 3
    
    return max_id + 1
    # Explanation:
    # - Returns max_id + 1
    # - Next item gets ID that's one more than the highest
    # - Example: If max_id = 3, returns 4

# Step 7: Create GET All Items Route
# What is this? API endpoint to get all items
# Think of it like: "When someone asks for all items, give them the list"
@app.route('/api/items', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/items' = The URL for getting all items
# - methods=['GET'] = Only accepts GET requests (reading data)
# - GET = HTTP method for reading/retrieving data
# - This is a RESTful API endpoint!

def get_items():
    """
    Get all items
    
    Returns:
    - JSON response with all items
    """
    # Step 8: Return JSON Response
    # What is this? Sending all items as JSON
    return jsonify({'items': items, 'count': len(items)})
    # Explanation:
    # - jsonify() = Function to create JSON response
    # - {'items': items, 'count': len(items)} = Dictionary to convert to JSON
    # - 'items' = Key, items = List of all items
    # - 'count' = Key, len(items) = Number of items
    # - Returns JSON like: {"items": [...], "count": 3}
    # - JSON = Data format that APIs use
    # - This sends all items to the client!

# Step 8: Create GET Single Item Route
# What is this? API endpoint to get one specific item
# Think of it like: "When someone asks for item #5, give them that item"
@app.route('/api/items/<int:item_id>', methods=['GET'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/items/<int:item_id>' = Dynamic route with item ID
# - <int:item_id> = Captures item ID from URL (must be integer)
# - Example: /api/items/1 → item_id = 1
# - methods=['GET'] = Only accepts GET requests

def get_item(item_id):
    """
    Get a single item by ID
    
    Parameters:
    - item_id: ID of the item to get
    
    Returns:
    - JSON response with the item, or 404 if not found
    """
    # Step 9: Find Item by ID
    # What is this? Looking for the item with this ID
    item = next((item for item in items if item['id'] == item_id), None)
    # Explanation:
    # - next() = Gets first item from iterator, or default if not found
    # - (item for item in items if item['id'] == item_id) = Generator expression
    # - Loops through items, finds one where id matches item_id
    # - None = Default value if not found
    # - item = The found item, or None if not found
    # - This is like searching for an item by ID
    
    # Step 10: Check if Item Found
    # What is this? Checking if the item exists
    if item:
        # Explanation:
        # - if item = If item was found (not None)
        # - Only proceed if item exists
        
        return jsonify(item)
        # Explanation:
        # - jsonify(item) = Converts item dictionary to JSON
        # - Returns JSON like: {"id": 1, "name": "Item 1", "description": "..."}
        # - This sends the item to the client!
    else:
        # Explanation:
        # - else = If item was not found (None)
        # - Item doesn't exist
        
        return jsonify({'error': 'Item not found'}), 404
        # Explanation:
        # - jsonify({'error': 'Item not found'}) = Error message as JSON
        # - 404 = HTTP status code (Not Found)
        # - Status codes tell client what happened
        # - 404 = Resource not found
        # - This tells the client the item doesn't exist!

# Step 11: Create POST Create Item Route
# What is this? API endpoint to create a new item
# Think of it like: "When someone sends data to create an item, add it"
@app.route('/api/items', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/items' = The URL for creating items
# - methods=['POST'] = Only accepts POST requests (creating data)
# - POST = HTTP method for creating new data
# - Same URL as GET, but different method!

def create_item():
    """
    Create a new item
    
    Returns:
    - JSON response with the created item, or 400 if invalid
    """
    # Step 12: Get JSON Data from Request
    # What is this? Getting the data sent by the client
    data = request.get_json()
    # Explanation:
    # - request.get_json() = Gets JSON data from request body
    # - request = Flask request object
    # - .get_json() = Parses JSON data
    # - data = Dictionary with the data sent by client
    # - Example: {"name": "New Item", "description": "Description"}
    # - Client sends JSON, we parse it to Python dictionary
    
    # Step 13: Validate Data
    # What is this? Checking if required fields are present
    if not data or 'name' not in data:
        # Explanation:
        # - if not data = If no data was sent
        # - 'name' not in data = If 'name' field is missing
        # - Only proceed if data exists and has 'name' field
        
        return jsonify({'error': 'Name is required'}), 400
        # Explanation:
        # - jsonify({'error': 'Name is required'}) = Error message as JSON
        # - 400 = HTTP status code (Bad Request)
        # - 400 = Client sent invalid data
        # - This tells the client what's wrong!
    
    # Step 14: Create New Item
    # What is this? Creating a new item dictionary
    new_item = {
        'id': get_next_id(),
        # Explanation:
        # - 'id' = Unique identifier
        # - get_next_id() = Gets next available ID
        # - Automatically assigns ID
        
        'name': data.get('name', ''),
        # Explanation:
        # - 'name' = Item name
        # - data.get('name', '') = Gets 'name' from data, or '' if not found
        # - Gets name from the JSON data sent by client
        
        'description': data.get('description', '')
        # Explanation:
        # - 'description' = Item description
        # - data.get('description', '') = Gets 'description' from data, or '' if not found
        # - Description is optional (can be empty)
    }
    # Explanation:
    # - new_item = Dictionary with id, name, description
    # - This is the new item to add
    
    # Step 15: Add Item to List
    # What is this? Adding the new item to our items list
    items.append(new_item)
    # Explanation:
    # - items.append(new_item) = Adds new item to end of list
    # - .append() = Method to add item to list
    # - Now the item is stored in our list!
    
    # Step 16: Return Created Item
    # What is this? Sending the created item back to client
    return jsonify(new_item), 201
    # Explanation:
    # - jsonify(new_item) = Converts item to JSON
    # - 201 = HTTP status code (Created)
    # - 201 = Successfully created new resource
    # - This tells the client the item was created and returns it!

# Step 17: Create PUT Update Item Route
# What is this? API endpoint to update an existing item
# Think of it like: "When someone wants to change item #5, update it"
@app.route('/api/items/<int:item_id>', methods=['PUT'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/items/<int:item_id>' = Dynamic route with item ID
# - <int:item_id> = Captures item ID from URL
# - methods=['PUT'] = Only accepts PUT requests (updating data)
# - PUT = HTTP method for updating/replacing data

def update_item(item_id):
    """
    Update an existing item
    
    Parameters:
    - item_id: ID of the item to update
    
    Returns:
    - JSON response with the updated item, or 404 if not found
    """
    # Step 18: Find Item by ID
    # What is this? Looking for the item to update
    item = next((item for item in items if item['id'] == item_id), None)
    # Explanation:
    # - Same as before: finds item by ID
    # - item = The found item, or None if not found
    
    # Step 19: Check if Item Found
    # What is this? Checking if the item exists
    if not item:
        # Explanation:
        # - if not item = If item was not found (None)
        # - Can't update what doesn't exist!
        
        return jsonify({'error': 'Item not found'}), 404
        # Explanation:
        # - Returns 404 error if item doesn't exist
        # - 404 = Not Found
    
    # Step 20: Get JSON Data from Request
    # What is this? Getting the updated data from client
    data = request.get_json()
    # Explanation:
    # - request.get_json() = Gets JSON data from request body
    # - data = Dictionary with updated data
    # - Client sends what fields to update
    
    # Step 21: Update Item Fields
    # What is this? Updating the item with new data
    if 'name' in data:
        # Explanation:
        # - if 'name' in data = If 'name' field was sent
        # - Only update if field is present
        
        item['name'] = data['name']
        # Explanation:
        # - item['name'] = Updates the name field
        # - data['name'] = New name from request
        # - This changes the item's name
    
    if 'description' in data:
        # Explanation:
        # - if 'description' in data = If 'description' field was sent
        
        item['description'] = data['description']
        # Explanation:
        # - item['description'] = Updates the description field
        # - data['description'] = New description from request
        # - This changes the item's description
    
    # Step 22: Return Updated Item
    # What is this? Sending the updated item back to client
    return jsonify(item)
    # Explanation:
    # - jsonify(item) = Converts updated item to JSON
    # - Returns the updated item
    # - Client can see what was changed!

# Step 23: Create DELETE Item Route
# What is this? API endpoint to delete an item
# Think of it like: "When someone wants to delete item #5, remove it"
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/api/items/<int:item_id>' = Dynamic route with item ID
# - <int:item_id> = Captures item ID from URL
# - methods=['DELETE'] = Only accepts DELETE requests (deleting data)
# - DELETE = HTTP method for deleting data

def delete_item(item_id):
    """
    Delete an item by ID
    
    Parameters:
    - item_id: ID of the item to delete
    
    Returns:
    - JSON response with success message, or 404 if not found
    """
    # Step 24: Find Item by ID
    # What is this? Looking for the item to delete
    item = next((item for item in items if item['id'] == item_id), None)
    # Explanation:
    # - Same as before: finds item by ID
    # - item = The found item, or None if not found
    
    # Step 25: Check if Item Found
    # What is this? Checking if the item exists
    if not item:
        # Explanation:
        # - if not item = If item was not found
        # - Can't delete what doesn't exist!
        
        return jsonify({'error': 'Item not found'}), 404
        # Explanation:
        # - Returns 404 error if item doesn't exist
    
    # Step 26: Remove Item from List
    # What is this? Deleting the item from our list
    items.remove(item)
    # Explanation:
    # - items.remove(item) = Removes item from list
    # - .remove() = Method to remove item from list
    # - The item is now deleted!
    
    # Step 27: Return Success Message
    # What is this? Telling client the item was deleted
    return jsonify({'message': 'Item deleted successfully'})
    # Explanation:
    # - jsonify({'message': 'Item deleted successfully'}) = Success message as JSON
    # - Returns confirmation that item was deleted
    # - Client knows the deletion was successful!

# Step 28: Create Home Route (GET)
# What is this? Simple home page with API documentation
# Think of it like: "When someone visits the home page, show API info"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page

def home():
    """
    Home page with API documentation
    """
    # Step 29: Return API Information
    # What is this? Showing API endpoints and how to use them
    return {
        'message': 'Welcome to the RESTful API!',
        'endpoints': {
            'GET /api/items': 'Get all items',
            'GET /api/items/<id>': 'Get single item',
            'POST /api/items': 'Create new item',
            'PUT /api/items/<id>': 'Update item',
            'DELETE /api/items/<id>': 'Delete item'
        }
    }
    # Explanation:
    # - Returns dictionary with API information
    # - Flask automatically converts to JSON
    # - Shows all available endpoints
    # - Helps users understand how to use the API!

# Step 30: Run the Application
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
    # - You can then visit that address in your browser or use API tools!

