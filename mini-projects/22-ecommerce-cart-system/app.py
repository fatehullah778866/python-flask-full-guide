# E-commerce Cart System App
# This app allows users to add products to a shopping cart!

# Step 1: Import Flask and Session Tools
# What is this? We're importing Flask and session tools
# Think of it like: "Get Flask tools and shopping cart tools"
from flask import Flask, render_template, request, redirect, url_for, session, flash
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - redirect = Function to redirect to another page
# - url_for = Function to generate URLs
# - session = Object for storing data between requests (our shopping cart!)
# - flash = Function to show messages to users
# - We'll use session to store the shopping cart!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Secret Key
# What is this? Setting up secret key for sessions
# Think of it like: "Set a secret password for security"
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions to work
# - In production, use a long, random string!
# - Sessions need this to securely store data

# Step 4: Define Product Catalog
# What is this? Creating a list of products to sell
# Think of it like: "Create a catalog of items in the store"
PRODUCTS = [
    {
        'id': 1,
        # Explanation:
        # - 'id' = Unique identifier for the product
        # - 1 = Product ID number
        # - Each product needs a unique ID
        
        'name': 'Laptop',
        # Explanation:
        # - 'name' = Product name
        # - 'Laptop' = The name of the product
        # - What the product is called
        
        'price': 999.99,
        # Explanation:
        # - 'price' = Product price
        # - 999.99 = Price in dollars (decimal number)
        # - How much the product costs
        
        'description': 'High-performance laptop for work and gaming',
        # Explanation:
        # - 'description' = Product description
        # - Text describing what the product is
        # - Tells customers about the product
        
        'image': '💻'
        # Explanation:
        # - 'image' = Product image (emoji for simplicity)
        # - '💻' = Laptop emoji
        # - In a real app, this would be an image URL
    },
    {
        'id': 2,
        'name': 'Smartphone',
        'price': 699.99,
        'description': 'Latest smartphone with amazing camera',
        'image': '📱'
    },
    {
        'id': 3,
        'name': 'Headphones',
        'price': 149.99,
        'description': 'Wireless noise-canceling headphones',
        'image': '🎧'
    },
    {
        'id': 4,
        'name': 'Tablet',
        'price': 449.99,
        'description': '10-inch tablet perfect for reading and browsing',
        'image': '📱'
    },
    {
        'id': 5,
        'name': 'Smart Watch',
        'price': 299.99,
        'description': 'Fitness tracker and smartwatch in one',
        'image': '⌚'
    },
    {
        'id': 6,
        'name': 'Keyboard',
        'price': 79.99,
        'description': 'Mechanical keyboard for typing enthusiasts',
        'image': '⌨️'
    }
]
# Explanation:
# - PRODUCTS = List of product dictionaries
# - Each dictionary = One product
# - Contains: id, name, price, description, image
# - This is our product catalog (what we're selling!)

# Step 5: Helper Function to Get Product by ID
# What is this? Function to find a product by its ID
# Think of it like: "Find a product in the catalog by its number"
def get_product(product_id):
    """
    Get a product by its ID
    
    Parameters:
    - product_id: The ID of the product to find
    
    Returns:
    - Product dictionary if found, None otherwise
    """
    # Step 6: Loop Through Products
    # What is this? Searching through all products
    for product in PRODUCTS:
        # Explanation:
        # - for product in PRODUCTS = Loop through each product
        # - product = Current product dictionary
        # - Loops through all products in catalog
        
        if product['id'] == product_id:
            # Explanation:
            # - if product['id'] == product_id = If this product's ID matches
            # - product['id'] = ID of current product
            # - product_id = ID we're looking for
            # - Only proceed if IDs match
            
            return product
            # Explanation:
            # - return product = Returns the product dictionary
            # - We found the product!
            # - Exit function and return the product
    
    # Step 7: Return None if Not Found
    # What is this? Product doesn't exist
    return None
    # Explanation:
    # - return None = Returns None (nothing)
    # - Product with that ID doesn't exist
    # - This happens if product_id is invalid

# Step 8: Helper Function to Initialize Cart
# What is this? Making sure cart exists in session
# Think of it like: "Create an empty shopping cart if one doesn't exist"
def init_cart():
    """
    Initialize the shopping cart in session if it doesn't exist
    """
    if 'cart' not in session:
        # Explanation:
        # - if 'cart' not in session = If cart doesn't exist in session
        # - session = Flask session object (stores data between requests)
        # - Only proceed if cart doesn't exist
        
        session['cart'] = {}
        # Explanation:
        # - session['cart'] = {} = Creates empty dictionary for cart
        # - {} = Empty dictionary
        # - Format: {product_id: quantity}
        # - Example: {1: 2, 3: 1} = 2 of product 1, 1 of product 3
        # - This is our shopping cart!


def cart_key(product_id):
    """
    Normalize a product ID for use as a session dict key.
    """
    return str(product_id)

# Step 9: Helper Function to Get Cart Total
# What is this? Calculating total price of items in cart
# Think of it like: "Add up all the prices in the shopping cart"
def get_cart_total():
    """
    Calculate the total price of all items in the cart
    
    Returns:
    - Total price as a float
    """
    # Step 10: Initialize Total
    # What is this? Starting with zero
    total = 0.0
    # Explanation:
    # - total = 0.0 = Starting total is zero
    # - We'll add prices to this
    # - 0.0 = Decimal number (float)
    
    # Step 11: Initialize Cart
    # What is this? Making sure cart exists
    init_cart()
    # Explanation:
    # - init_cart() = Our helper function
    # - Creates cart if it doesn't exist
    # - Ensures we have a cart to work with
    
    # Step 12: Loop Through Cart Items
    # What is this? Going through each item in the cart
    for stored_product_id, quantity in session['cart'].items():
        # Explanation:
        # - for product_id, quantity in session['cart'].items() = Loop through cart
        # - .items() = Gets key-value pairs from dictionary
        # - product_id = Product ID (key)
        # - quantity = How many of this product (value)
        # - Example: {1: 2, 3: 1} → product_id=1, quantity=2 then product_id=3, quantity=1
        
        # Step 13: Get Product Information
        # What is this? Finding the product details
        product = get_product(int(stored_product_id))
        # Explanation:
        # - get_product(product_id) = Our helper function
        # - product = Product dictionary (or None if not found)
        # - Gets product information (name, price, etc.)
        
        # Step 14: Calculate Item Total
        # What is this? Price of this item times quantity
        if product:
            # Explanation:
            # - if product = If product was found
            # - Only proceed if product exists
            
            total += product['price'] * quantity
            # Explanation:
            # - product['price'] = Price of one item
            # - quantity = How many of this item
            # - * = Multiply
            # - total += = Add to total (same as total = total + ...)
            # - Example: $10 * 3 = $30 added to total
            # - This calculates: price per item × quantity = total for this item
    
    # Step 15: Return Total
    # What is this? Returning the calculated total
    return total
    # Explanation:
    # - return total = Returns the total price
    # - This is the sum of all items in the cart
    # - Example: $999.99 + $149.99 = $1149.98

# Step 16: Create Home Route (GET)
# What is this? The main page that shows all products
# Think of it like: "When someone visits the home page, show the product catalog"
@app.route('/')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/' = The home page (like www.example.com/)
# - When someone visits '/', Flask will run the function below

def index():
    """
    This function runs when someone visits the home page
    It shows all products from the catalog
    """
    # Step 17: Initialize Cart
    # What is this? Making sure cart exists
    init_cart()
    # Explanation:
    # - init_cart() = Our helper function
    # - Creates cart if it doesn't exist
    # - Ensures we have a cart ready
    
    # Step 18: Get Cart Item Count
    # What is this? Counting how many items are in the cart
    cart_count = sum(session['cart'].values())
    # Explanation:
    # - session['cart'].values() = Gets all quantities from cart
    # - .values() = Gets all values from dictionary (the quantities)
    # - sum() = Adds all quantities together
    # - cart_count = Total number of items in cart
    # - Example: {1: 2, 3: 1} → sum([2, 1]) = 3 items total
    
    # Step 19: Render Template with Products
    # What is this? Showing the HTML page with products
    return render_template('index.html', products=PRODUCTS, cart_count=cart_count)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - products=PRODUCTS = Passes product catalog to template
    # - cart_count=cart_count = Passes cart item count to template
    # - In the template, we can use products to display them

# Step 20: Create Add to Cart Route (POST)
# What is this? Handles adding a product to the cart
# Think of it like: "When user clicks 'Add to Cart', add the product"
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/add-to-cart/<int:product_id>' = Dynamic route with product ID
# - <int:product_id> = Captures product ID from URL (must be integer)
# - methods=['POST'] = Only accepts POST requests (form submission)
# - Example: /add-to-cart/1 → product_id = 1

def add_to_cart(product_id):
    """
    This function runs when a user adds a product to the cart
    It adds the product to the session cart
    """
    # Step 21: Initialize Cart
    # What is this? Making sure cart exists
    init_cart()
    # Explanation:
    # - init_cart() = Our helper function
    # - Creates cart if it doesn't exist
    
    # Step 22: Get Product
    # What is this? Finding the product being added
    product = get_product(product_id)
    # Explanation:
    # - get_product(product_id) = Our helper function
    # - product = Product dictionary (or None if not found)
    
    # Step 23: Check if Product Exists
    # What is this? Making sure product is valid
    if not product:
        # Explanation:
        # - if not product = If product doesn't exist
        # - Product ID is invalid
        
        flash('Product not found!', 'error')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Product not found!' = Error message
        # - 'error' = Message category
        
        return redirect(url_for('index'))
        # Explanation:
        # - redirect = Sends user to another page
        # - url_for('index') = Generates URL for 'index' route
        # - User is sent back to home page
    
    # Step 24: Get Quantity from Form
    # What is this? Getting how many items to add
    quantity = int(request.form.get('quantity', 1))
    # Explanation:
    # - request.form.get('quantity', 1) = Gets value of input named 'quantity'
    # - If 'quantity' doesn't exist, returns 1 (default)
    # - int() = Converts to integer
    # - quantity = How many items to add
    # - Example: User selects 3 → quantity = 3
    
    # Step 25: Add Product to Cart
    # What is this? Adding the product to the shopping cart
    cart = session['cart']
    cart_item_key = cart_key(product_id)
    if cart_item_key in cart:
        # Explanation:
        # - if product_id in session['cart'] = If product already in cart
        # - Check if this product is already in the cart
        # - Only proceed if product is already in cart
        
        cart[cart_item_key] += quantity
        # Explanation:
        # - session['cart'][product_id] = Current quantity of this product
        # - += quantity = Add to existing quantity
        # - Same as: session['cart'][product_id] = session['cart'][product_id] + quantity
        # - Example: Had 2, adding 1 → now have 3
    else:
        # Explanation:
        # - else = If product is NOT in cart
        # - This is the first time adding this product
        
        cart[cart_item_key] = quantity
        # Explanation:
        # - session['cart'][product_id] = quantity = Sets quantity
        # - Adds new product to cart with specified quantity
        # - Example: Adding product 1 with quantity 2 → cart[1] = 2
    
    # Step 26: Mark Session as Modified
    # What is this? Telling Flask that session changed
    session.modified = True
    # Explanation:
    # - session.modified = True = Marks session as changed
    # - Flask needs this to save changes to mutable objects (like dictionaries)
    # - Without this, Flask might not notice the change!
    
    # Step 27: Show Success Message
    # What is this? Telling user the item was added
    flash(f'{product["name"]} added to cart!', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - f'{product["name"]} added to cart!' = Success message with product name
    # - 'success' = Message category
    # - Example: "Laptop added to cart!"
    
    # Step 28: Redirect to Home Page
    # What is this? Sending user back to product catalog
    return redirect(url_for('index'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('index') = Generates URL for 'index' route
    # - User is sent back to home page
    # - They'll see the success message and updated cart count!

# Step 29: Create Cart Route (GET)
# What is this? The page that shows the shopping cart
# Think of it like: "When someone visits /cart, show their shopping cart"
@app.route('/cart')
# Explanation:
# - @app.route = Decorator that creates a route
# - '/cart' = The cart page URL
# - When someone visits '/cart', Flask will run the function below

def cart():
    """
    This function runs when someone visits the cart page
    It shows all items in the shopping cart
    """
    # Step 30: Initialize Cart
    # What is this? Making sure cart exists
    init_cart()
    # Explanation:
    # - init_cart() = Our helper function
    # - Creates cart if it doesn't exist
    
    # Step 31: Build Cart Items List
    # What is this? Creating a list of cart items with product details
    cart_items = []
    # Explanation:
    # - cart_items = Empty list to store cart items
    # - [] = Empty list
    # - We'll add items to this list
    
    # Step 32: Loop Through Cart Items
    # What is this? Going through each item in the cart
    for stored_product_id, quantity in session['cart'].items():
        # Explanation:
        # - for product_id, quantity in session['cart'].items() = Loop through cart
        # - .items() = Gets key-value pairs from dictionary
        # - product_id = Product ID (key)
        # - quantity = How many of this product (value)

        # Step 33: Get Product Information
        # What is this? Finding the product details
        product = get_product(int(stored_product_id))
        # Explanation:
        # - get_product(product_id) = Our helper function
        # - product = Product dictionary (or None if not found)
        
        # Step 34: Add Item to Cart Items List
        # What is this? Adding item with all its information
        if product:
            # Explanation:
            # - if product = If product was found
            # - Only proceed if product exists
            
            cart_items.append({
                # Explanation:
                # - cart_items.append() = Adds item to list
                # - Dictionary = Item information
                
                'product': product,
                # Explanation:
                # - 'product' = Product dictionary (name, price, etc.)
                # - product = The product information
                
                'quantity': quantity,
                # Explanation:
                # - 'quantity' = How many of this product
                # - quantity = The quantity from cart
                
                'subtotal': product['price'] * quantity
                # Explanation:
                # - 'subtotal' = Total price for this item
                # - product['price'] = Price of one item
                # - quantity = How many items
                # - * = Multiply
                # - Example: $10 * 3 = $30 subtotal
            })
            # Explanation:
            # - This adds a dictionary with product info, quantity, and subtotal
            # - Example: {'product': {...}, 'quantity': 2, 'subtotal': 1999.98}
    
    # Step 35: Calculate Cart Total
    # What is this? Getting the total price of all items
    cart_total = get_cart_total()
    # Explanation:
    # - get_cart_total() = Our helper function
    # - cart_total = Total price of all items in cart
    # - Example: $1149.98
    
    # Step 36: Render Template with Cart
    # What is this? Showing the HTML page with cart items
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'cart.html' = The template file to display
    # - cart_items=cart_items = Passes cart items list to template
    # - cart_total=cart_total = Passes total price to template
    # - In the template, we can use these to display the cart!

# Step 37: Create Update Cart Route (POST)
# What is this? Handles updating quantity of items in cart
# Think of it like: "When user changes quantity, update the cart"
@app.route('/update-cart/<int:product_id>', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/update-cart/<int:product_id>' = Dynamic route with product ID
# - <int:product_id> = Captures product ID from URL
# - methods=['POST'] = Only accepts POST requests

def update_cart(product_id):
    """
    This function runs when a user updates the quantity of an item in the cart
    It updates the quantity or removes the item
    """
    # Step 38: Initialize Cart
    # What is this? Making sure cart exists
    init_cart()
    # Explanation:
    # - init_cart() = Our helper function
    # - Creates cart if it doesn't exist
    
    # Step 39: Get New Quantity from Form
    # What is this? Getting the updated quantity
    new_quantity = int(request.form.get('quantity', 0))
    # Explanation:
    # - request.form.get('quantity', 0) = Gets value of input named 'quantity'
    # - If 'quantity' doesn't exist, returns 0 (default)
    # - int() = Converts to integer
    # - new_quantity = The new quantity user wants
    # - Example: User changes to 5 → new_quantity = 5
    
    # Step 40: Update or Remove Item
    # What is this? Updating quantity or removing item
    cart = session['cart']
    cart_item_key = cart_key(product_id)
    if new_quantity > 0:
        # Explanation:
        # - if new_quantity > 0 = If quantity is greater than 0
        # - User wants to keep the item (just change quantity)
        
        cart[cart_item_key] = new_quantity
        # Explanation:
        # - session['cart'][product_id] = new_quantity = Sets new quantity
        # - Updates the quantity for this product
        # - Example: Had 3, changed to 5 → now have 5
    else:
        # Explanation:
        # - else = If quantity is 0 or less
        # - User wants to remove the item
        
        del cart[cart_item_key]
        # Explanation:
        # - del session['cart'][product_id] = Removes item from cart
        # - Deletes this product from the cart dictionary
        # - Item is no longer in cart
    
    # Step 41: Mark Session as Modified
    # What is this? Telling Flask that session changed
    session.modified = True
    # Explanation:
    # - session.modified = True = Marks session as changed
    # - Flask needs this to save changes
    
    # Step 42: Show Success Message
    # What is this? Telling user the cart was updated
    flash('Cart updated!', 'success')
    # Explanation:
    # - flash() = Shows temporary message
    # - 'Cart updated!' = Success message
    # - 'success' = Message category
    
    # Step 43: Redirect to Cart Page
    # What is this? Sending user back to cart page
    return redirect(url_for('cart'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('cart') = Generates URL for 'cart' route
    # - User is sent back to cart page
    # - They'll see the updated cart!

# Step 44: Create Remove from Cart Route (POST)
# What is this? Handles removing an item from the cart
# Think of it like: "When user clicks 'Remove', delete the item"
@app.route('/remove-from-cart/<int:product_id>', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/remove-from-cart/<int:product_id>' = Dynamic route with product ID
# - <int:product_id> = Captures product ID from URL
# - methods=['POST'] = Only accepts POST requests

def remove_from_cart(product_id):
    """
    This function runs when a user removes an item from the cart
    It removes the product from the session cart
    """
    # Step 45: Initialize Cart
    # What is this? Making sure cart exists
    init_cart()
    # Explanation:
    # - init_cart() = Our helper function
    # - Creates cart if it doesn't exist
    cart = session['cart']
    cart_item_key = cart_key(product_id)
    
    # Step 46: Remove Item from Cart
    # What is this? Deleting the product from cart
    if cart_item_key in cart:
        # Explanation:
        # - if product_id in session['cart'] = If product is in cart
        # - Check if this product exists in cart
        # - Only proceed if product is in cart
        
        del cart[cart_item_key]
        # Explanation:
        # - del session['cart'][product_id] = Removes item from cart
        # - Deletes this product from the cart dictionary
        # - Item is no longer in cart
        
        # Step 47: Mark Session as Modified
        # What is this? Telling Flask that session changed
        session.modified = True
        # Explanation:
        # - session.modified = True = Marks session as changed
        # - Flask needs this to save changes
        
        # Step 48: Show Success Message
        # What is this? Telling user the item was removed
        flash('Item removed from cart!', 'success')
        # Explanation:
        # - flash() = Shows temporary message
        # - 'Item removed from cart!' = Success message
        # - 'success' = Message category
    
    # Step 49: Redirect to Cart Page
    # What is this? Sending user back to cart page
    return redirect(url_for('cart'))
    # Explanation:
    # - redirect = Sends user to another page
    # - url_for('cart') = Generates URL for 'cart' route
    # - User is sent back to cart page
    # - They'll see the updated cart (without the removed item)!

# Step 50: Run the Application
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

