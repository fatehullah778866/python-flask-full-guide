# Flask-Caching Example
# Demonstrates caching with Flask-Caching

from flask import Flask, render_template_string
from flask_caching import Cache
import time

app = Flask(__name__)

# Configure cache
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes

# Create cache
cache = Cache(app)

# Expensive function (simulated)
@cache.memoize(timeout=300)
def expensive_calculation(n):
    """Expensive calculation - cached"""
    time.sleep(2)  # Simulate slow operation
    return sum(range(n))

@app.route('/')
def home():
    return '''
    <h1>Caching Example</h1>
    <ul>
        <li><a href="/slow">Slow Route (cached)</a></li>
        <li><a href="/fast">Fast Route</a></li>
        <li><a href="/clear">Clear Cache</a></li>
    </ul>
    '''

@app.route('/slow')
@cache.cached(timeout=300)
def slow_route():
    """This route is cached - first call slow, next calls fast"""
    result = expensive_calculation(1000000)
    return f'''
    <h2>Slow Route (Cached)</h2>
    <p>Result: {result}</p>
    <p>First call takes 2 seconds, next calls are instant!</p>
    <a href="/">Back</a>
    '''

@app.route('/fast')
def fast_route():
    """This route is not cached"""
    return '''
    <h2>Fast Route</h2>
    <p>This route is always fast (no expensive operations)</p>
    <a href="/">Back</a>
    '''

@app.route('/clear')
def clear_cache():
    """Clear all cache"""
    cache.clear()
    return '''
    <h2>Cache Cleared!</h2>
    <p>All cached data has been cleared.</p>
    <a href="/">Back</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)

