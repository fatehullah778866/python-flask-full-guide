# Caching System App
# This app demonstrates caching to improve performance!

# Step 1: Import Flask and Caching Tools
# What is this? We're importing Flask and caching tools
# Think of it like: "Get Flask tools and caching tools"
from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
import time
import random
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains request data
# - jsonify = Function to return JSON responses
# - Cache = Flask-Caching extension for caching
# - time = Module for time-related functions
# - random = Module for random number generation
# - We'll use caching to store frequently accessed data!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Configure Caching
# What is this? Setting up caching system
# Think of it like: "Tell Flask how to cache data"
app.config['CACHE_TYPE'] = 'SimpleCache'
# Explanation:
# - app.config = Flask configuration dictionary
# - 'CACHE_TYPE' = Type of cache to use
# - 'SimpleCache' = In-memory cache (simple, no Redis needed)
# - This stores data in Python's memory
# - For production, use 'RedisCache' with Redis server

app.config['CACHE_DEFAULT_TIMEOUT'] = 300
# Explanation:
# - 'CACHE_DEFAULT_TIMEOUT' = Default time before cache expires
# - 300 = 300 seconds (5 minutes)
# - After 5 minutes, cached data is removed
# - This prevents stale data

app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
# Explanation:
# - 'SECRET_KEY' = Secret key for Flask sessions
# - Required for sessions to work

# Step 4: Initialize Cache
# What is this? Creating the cache object
# Think of it like: "Create a cache manager"
cache = Cache(app)
# Explanation:
# - Cache(app) = Creates cache object connected to Flask app
# - cache = Our cache manager
# - This enables caching functionality!

# Step 5: Simulate Expensive Operation
# What is this? Function that takes time to complete
# Think of it like: "A slow operation we want to cache"
def expensive_operation(data_key):
    """
    Simulates an expensive operation (like database query or API call)
    This function takes time to complete, so we'll cache its result
    
    Args:
    - data_key: Key to identify the data
    
    Returns:
    - Dictionary with result and timestamp
    """
    # Step 6: Simulate Processing Time
    # What is this? Making the function take time
    time.sleep(2)
    # Explanation:
    # - time.sleep(2) = Pause execution for 2 seconds
    # - This simulates a slow operation
    # - In real apps, this could be a database query or API call
    # - We want to cache this result so we don't have to wait every time!
    
    # Step 7: Generate Result
    # What is this? Creating the result data
    result = {
        'data': f'Result for {data_key}',
        'value': random.randint(1, 1000),
        'timestamp': time.time(),
        'processed_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    # Explanation:
    # - result = Dictionary with result data
    # - 'data' = Some text data
    # - 'value' = Random number (simulates data)
    # - 'timestamp' = Current time as Unix timestamp
    # - 'processed_at' = Formatted date/time string
    # - This is what we'll cache!
    
    return result
    # Explanation:
    # - return result = Returns the result dictionary
    # - This function takes 2 seconds to complete
    # - We'll cache this result so next time it's instant!

# Step 8: Create Cached Route (GET)
# What is this? Route that uses caching
@app.route('/')
def index():
    """
    This function runs when someone visits the home page
    It shows caching information and controls
    """
    # Step 9: Get Cache Statistics
    # What is this? Getting information about the cache
    cache_stats = {
        'type': app.config.get('CACHE_TYPE', 'Unknown'),
        'timeout': app.config.get('CACHE_DEFAULT_TIMEOUT', 0)
    }
    # Explanation:
    # - cache_stats = Dictionary with cache information
    # - 'type' = Type of cache being used
    # - 'timeout' = Default timeout in seconds
    # - This shows users what caching system is active
    
    return render_template('index.html', cache_stats=cache_stats)
    # Explanation:
    # - render_template = Displays HTML template
    # - 'index.html' = The template file to display
    # - cache_stats=cache_stats = Passes cache stats to template

# Step 9: Create Get Data Route (GET) - Without Cache
# What is this? Route that doesn't use caching (slow)
@app.route('/api/data/<key>')
def get_data_no_cache(key):
    """
    This function gets data without caching
    It's slow because it always runs the expensive operation
    """
    # Step 10: Run Expensive Operation
    # What is this? Running the slow operation
    start_time = time.time()
    # Explanation:
    # - time.time() = Gets current time in seconds
    # - start_time = Time when we started
    # - We'll use this to measure how long it takes
    
    result = expensive_operation(key)
    # Explanation:
    # - expensive_operation(key) = Runs the slow function
    # - This takes 2 seconds!
    # - result = The result dictionary
    
    elapsed_time = time.time() - start_time
    # Explanation:
    # - time.time() = Current time
    # - start_time = Time when we started
    # - elapsed_time = How long it took (in seconds)
    # - This will be about 2 seconds
    
    result['elapsed_time'] = elapsed_time
    result['cached'] = False
    # Explanation:
    # - 'elapsed_time' = How long it took
    # - 'cached' = False (not from cache)
    # - This shows it was slow
    
    return jsonify(result)
    # Explanation:
    # - jsonify() = Returns JSON response
    # - result = The result dictionary
    # - Client receives the data (slow!)

# Step 10: Create Get Data Route (GET) - With Cache
# What is this? Route that uses caching (fast!)
@app.route('/api/data-cached/<key>')
@cache.cached(timeout=60)
# Explanation:
# - @cache.cached(timeout=60) = Decorator that caches the result
# - timeout=60 = Cache expires after 60 seconds
# - If same request comes within 60 seconds, returns cached result
# - This makes the route much faster!

def get_data_cached(key):
    """
    This function gets data with caching
    It's fast because it uses cached results when available
    """
    # Step 11: Run Expensive Operation (Only if Not Cached)
    # What is this? Running the slow operation only if needed
    start_time = time.time()
    # Explanation:
    # - time.time() = Gets current time in seconds
    # - start_time = Time when we started
    
    result = expensive_operation(key)
    # Explanation:
    # - expensive_operation(key) = Runs the slow function
    # - BUT: If this was called recently, cache returns old result instantly!
    # - First call: Takes 2 seconds
    # - Next calls (within 60 seconds): Instant!
    
    elapsed_time = time.time() - start_time
    # Explanation:
    # - elapsed_time = How long it took
    # - First call: ~2 seconds
    # - Cached calls: ~0.001 seconds (very fast!)
    
    result['elapsed_time'] = elapsed_time
    result['cached'] = elapsed_time < 0.1
    # Explanation:
    # - 'elapsed_time' = How long it took
    # - 'cached' = True if very fast (< 0.1 seconds)
    # - This indicates if result came from cache
    
    return jsonify(result)
    # Explanation:
    # - jsonify() = Returns JSON response
    # - result = The result dictionary
    # - Client receives the data (fast if cached!)

# Step 11: Create Clear Cache Route (POST)
# What is this? Route to clear the cache
@app.route('/api/clear-cache', methods=['POST'])
def clear_cache():
    """
    This function clears all cached data
    Useful when data changes and cache needs to be refreshed
    """
    # Step 12: Clear All Cache
    # What is this? Removing all cached data
    cache.clear()
    # Explanation:
    # - cache.clear() = Removes all cached data
    # - This forces fresh data on next request
    # - Useful when data is updated
    
    return jsonify({
        'message': 'Cache cleared successfully',
        'timestamp': time.time()
    })
    # Explanation:
    # - jsonify() = Returns JSON response
    # - 'message' = Success message
    # - 'timestamp' = When cache was cleared
    # - Client knows cache is now empty

# Step 12: Create Clear Specific Cache Route (POST)
# What is this? Route to clear cache for specific key
@app.route('/api/clear-cache/<key>', methods=['POST'])
def clear_cache_key(key):
    """
    This function clears cache for a specific key
    More targeted than clearing all cache
    """
    # Step 13: Clear Specific Cache Entry
    # What is this? Removing cached data for one key
    cache.delete(key)
    # Explanation:
    # - cache.delete(key) = Removes cached data for this key
    # - Other cached data remains
    # - More efficient than clearing everything
    
    return jsonify({
        'message': f'Cache cleared for key: {key}',
        'timestamp': time.time()
    })
    # Explanation:
    # - jsonify() = Returns JSON response
    # - 'message' = Success message with key name
    # - 'timestamp' = When cache was cleared

# Step 13: Create Cache Statistics Route (GET)
# What is this? Route to get cache statistics
@app.route('/api/cache-stats')
def cache_stats():
    """
    This function returns cache statistics
    Shows how caching is performing
    """
    # Step 14: Get Cache Information
    # What is this? Getting information about cache
    stats = {
        'cache_type': app.config.get('CACHE_TYPE', 'Unknown'),
        'default_timeout': app.config.get('CACHE_DEFAULT_TIMEOUT', 0),
        'timestamp': time.time()
    }
    # Explanation:
    # - stats = Dictionary with cache information
    # - 'cache_type' = Type of cache (SimpleCache, RedisCache, etc.)
    # - 'default_timeout' = Default expiration time
    # - 'timestamp' = Current time
    
    return jsonify(stats)
    # Explanation:
    # - jsonify() = Returns JSON response
    # - stats = Cache statistics
    # - Client can see cache configuration

# Step 14: Run the Application
# What is this? This starts the web server
if __name__ == '__main__':
    app.run(debug=True)
    # Explanation:
    # - app.run() = Start the Flask web server
    # - debug=True = Show errors in the browser (helpful for learning!)

