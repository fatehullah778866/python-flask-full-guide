# Weather Display App
# This app displays weather information for any city using an API!

# Step 1: Import Flask and requests
# What is this? We're importing Flask and requests library
# Think of it like: "Get Flask tools and HTTP request tool"
from flask import Flask, render_template, request, flash
import requests
import os
# Explanation:
# - Flask = The main Flask class
# - render_template = Function to display HTML templates
# - request = Object that contains form data
# - flash = Function to show messages to users
# - requests = Library for making HTTP requests (getting data from APIs)
# - os = Library for accessing environment variables
# - requests = Like a messenger that goes to other websites and gets data!

# Step 2: Create the Flask Application
# What is this? We're creating our web application
# Think of it like: "Create a new website called 'app'"
app = Flask(__name__)
# Explanation:
# - 'app' = The name of our Flask application
# - Flask(__name__) = Creates a new Flask app
# - __name__ = Tells Flask where to find files (current folder)

# Step 3: Set Secret Key for Flash Messages
# What is this? A secret key needed for flash messages
# Think of it like: "A password to protect flash messages"
app.secret_key = 'your-secret-key-change-this-in-production'
# Explanation:
# - secret_key = Required for flash messages to work
# - Flash messages = Temporary messages shown to users
# - In production, use a random, secure key
# - This is like a password that protects your messages

# Step 4: Set Up API Configuration
# What is this? Configuration for the weather API
# Think of it like: "Settings for getting weather data"
API_KEY = os.environ.get('WEATHER_API_KEY', 'your-api-key-here')
# Explanation:
# - API_KEY = Variable to store the API key
# - os.environ.get() = Gets value from environment variable
# - 'WEATHER_API_KEY' = Name of environment variable
# - 'your-api-key-here' = Default value if not found
# - API key = Password to access the weather API
# - We'll use OpenWeatherMap API (free tier available)

API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
# Explanation:
# - API_BASE_URL = The base URL for weather API
# - This is where we'll send requests to get weather data
# - OpenWeatherMap = Free weather API service
# - /data/2.5/weather = Endpoint for current weather

# Step 5: Create Home Route (GET)
# What is this? The main page that shows the weather form
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
    It shows the form to enter a city name
    """
    # Step 6: Render the Weather Form Template
    # What is this? We're showing the HTML page with the form
    return render_template('index.html')
    # Explanation:
    # - render_template = Function that displays HTML templates
    # - 'index.html' = The template file to display
    # - Flask looks for templates in the 'templates' folder
    # - This will show a form where users can enter a city name

# Step 7: Create Weather Route (POST)
# What is this? Handles form submission and gets weather data
# Think of it like: "When user submits form, get weather and show it"
@app.route('/weather', methods=['POST'])
# Explanation:
# - @app.route = Decorator that creates a route
# - '/weather' = The URL for getting weather
# - methods=['POST'] = Only accepts POST requests (form submission)
# - When form is submitted to '/weather', Flask will run the function below

def get_weather():
    """
    This function runs when the form is submitted
    It gets the city name, fetches weather data from API, and displays it
    """
    # Step 8: Get City Name from Form
    # What is this? We're getting the city name the user entered
    city = request.form.get('city', '').strip()
    # Explanation:
    # - request.form.get('city', '') = Gets value of input named 'city'
    # - If 'city' doesn't exist, returns empty string ''
    # - .strip() = Removes whitespace from beginning and end
    # - city = Variable to hold the city name
    # - Example: User enters "  New York  " → becomes "New York"
    
    # Step 9: Validate City Name
    # What is this? Checking if user actually entered a city name
    if not city:
        # Explanation:
        # - if not city = If city is empty
        # - Empty strings are "falsy" in Python
        # - Only proceed if user entered something
        
        flash('Please enter a city name!', 'error')
        # Explanation:
        # - flash() = Function to show temporary message to user
        # - 'Please enter a city name!' = The message text
        # - 'error' = Message category (for styling)
        # - This message will appear on the page
        
        return render_template('index.html')
        # Explanation:
        # - Shows the form again
        # - User will see the error message
        # - They can try again
    
    # Step 10: Prepare API Request Parameters
    # What is this? Setting up the data to send to the API
    params = {
        'q': city,
        # Explanation:
        # - 'q' = Query parameter (city name)
        # - city = The city name from the form
        # - API expects city name in 'q' parameter
        
        'appid': API_KEY,
        # Explanation:
        # - 'appid' = API key parameter
        # - API_KEY = Our API key (password for API)
        # - API requires this to authenticate our request
        
        'units': 'metric'
        # Explanation:
        # - 'units' = Temperature units
        # - 'metric' = Celsius (not Fahrenheit)
        # - You can use 'imperial' for Fahrenheit
    }
    # Explanation:
    # - params = Dictionary of parameters
    # - These will be sent to the API
    # - Like filling out a form to request weather data
    
    # Step 11: Make API Request
    # What is this? Sending request to weather API to get data
    # Think of it like: "Ask the weather API for information about this city"
    try:
        # Explanation:
        # - try = Attempt to do something
        # - If it fails, catch the error (except block)
        # - This handles network errors, API errors, etc.
        
        response = requests.get(API_BASE_URL, params=params, timeout=10)
        # Explanation:
        # - requests.get() = Function to make GET HTTP request
        # - API_BASE_URL = Where to send the request
        # - params=params = Parameters to send (city, API key, units)
        # - timeout=10 = Wait maximum 10 seconds for response
        # - response = Object containing the API's response
        # - This is like sending a letter and waiting for a reply!
        
        # Step 12: Check Response Status
        # What is this? Checking if the API request was successful
        if response.status_code == 200:
            # Explanation:
            # - response.status_code = HTTP status code
            # - 200 = Success (OK)
            # - Other codes: 404 (Not Found), 401 (Unauthorized), etc.
            # - Only proceed if request was successful
            
            # Step 13: Parse JSON Response
            # What is this? Converting API response to Python dictionary
            data = response.json()
            # Explanation:
            # - response.json() = Converts JSON to Python dictionary
            # - JSON = JavaScript Object Notation (data format)
            # - Dictionary = Python data structure (key-value pairs)
            # - data = Dictionary containing weather information
            # - Now we can access weather data like: data['temperature']
            
            # Step 14: Extract Weather Information
            # What is this? Getting specific weather data from the response
            weather_info = {
                # Explanation:
                # - weather_info = Dictionary to store formatted weather data
                # - We'll extract and format the data for display
                
                'city': data['name'],
                # Explanation:
                # - 'city' = City name
                # - data['name'] = City name from API response
                # - Example: "New York"
                
                'country': data['sys']['country'],
                # Explanation:
                # - 'country' = Country code
                # - data['sys']['country'] = Nested dictionary access
                # - data['sys'] = Gets 'sys' dictionary
                # - ['country'] = Gets 'country' from that dictionary
                # - Example: "US"
                
                'temperature': round(data['main']['temp']),
                # Explanation:
                # - 'temperature' = Temperature in Celsius
                # - data['main']['temp'] = Temperature from API
                # - round() = Rounds to nearest whole number
                # - Example: 22.5 → 23
                
                'feels_like': round(data['main']['feels_like']),
                # Explanation:
                # - 'feels_like' = "Feels like" temperature
                # - data['main']['feels_like'] = Perceived temperature
                # - round() = Rounds to whole number
                # - Example: 20.3 → 20
                
                'description': data['weather'][0]['description'].title(),
                # Explanation:
                # - 'description' = Weather description
                # - data['weather'] = List of weather conditions
                # - [0] = First item in the list
                # - ['description'] = Description text
                # - .title() = Capitalizes first letter of each word
                # - Example: "clear sky" → "Clear Sky"
                
                'humidity': data['main']['humidity'],
                # Explanation:
                # - 'humidity' = Humidity percentage
                # - data['main']['humidity'] = Humidity value
                # - Example: 65 (means 65%)
                
                'wind_speed': round(data['wind']['speed'] * 3.6),
                # Explanation:
                # - 'wind_speed' = Wind speed in km/h
                # - data['wind']['speed'] = Wind speed from API (m/s)
                # - * 3.6 = Converts m/s to km/h
                # - round() = Rounds to whole number
                # - Example: 5.5 m/s → 20 km/h
                
                'pressure': data['main']['pressure'],
                # Explanation:
                # - 'pressure' = Atmospheric pressure
                # - data['main']['pressure'] = Pressure in hPa
                # - Example: 1013
                
                'icon': data['weather'][0]['icon']
                # Explanation:
                # - 'icon' = Weather icon code
                # - data['weather'][0]['icon'] = Icon code from API
                # - Example: "01d" (clear sky, day)
                # - We can use this to show weather icons
            }
            
            # Step 15: Render Template with Weather Data
            # What is this? Showing the weather information to the user
            return render_template('index.html', weather=weather_info, city=city)
            # Explanation:
            # - render_template = Function that displays HTML templates
            # - 'index.html' = The template file to display
            # - weather=weather_info = Passes weather data to template
            # - city=city = Passes city name to template
            # - Template can display the weather information
            
        elif response.status_code == 404:
            # Explanation:
            # - elif = Else if (another condition)
            # - 404 = Not Found
            # - City not found in API database
            
            flash(f'City "{city}" not found. Please check the spelling and try again.', 'error')
            # Explanation:
            # - flash() = Show error message
            # - f'...' = f-string (formatted string)
            # - {city} = Inserts city name into message
            # - 'error' = Message category
            
            return render_template('index.html')
            # Explanation:
            # - Shows form again with error message
            
        elif response.status_code == 401:
            # Explanation:
            # - 401 = Unauthorized
            # - Invalid API key
            
            flash('Invalid API key. Please check your API configuration.', 'error')
            # Explanation:
            # - Shows error about API key
            
            return render_template('index.html')
            # Explanation:
            # - Shows form again
            
        else:
            # Explanation:
            # - else = If none of the above conditions are true
            # - Other error status codes
            
            flash(f'Error: Unable to fetch weather data. Status code: {response.status_code}', 'error')
            # Explanation:
            # - Shows generic error message
            # - Includes status code for debugging
            
            return render_template('index.html')
            # Explanation:
            # - Shows form again
            
    except requests.exceptions.RequestException as e:
        # Explanation:
        # - except = If an error occurs
        # - requests.exceptions.RequestException = Error from requests library
        # - as e = Stores error in variable 'e'
        # - This catches network errors, timeout errors, etc.
        
        flash(f'Error connecting to weather service: {str(e)}', 'error')
        # Explanation:
        # - Shows error message
        # - str(e) = Converts error to string
        # - User sees what went wrong
        
        return render_template('index.html')
        # Explanation:
        # - Shows form again with error message
        
    except KeyError as e:
        # Explanation:
        # - KeyError = Error when dictionary key doesn't exist
        # - This happens if API response structure is unexpected
        
        flash('Error: Unexpected response from weather service.', 'error')
        # Explanation:
        # - Shows error message
        
        return render_template('index.html')
        # Explanation:
        # - Shows form again

# Step 16: Run the Application
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

