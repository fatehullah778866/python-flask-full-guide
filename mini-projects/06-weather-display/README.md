# Project 6: Weather Display App 🌤️

Welcome to Project 6! This app displays weather information for any city using an API!

## What is This Project? 🤔

**Weather Display App** = An app that shows weather for any city!

**Think of it like:**
- **Weather Website** = Shows weather online
- **API** = Gets weather data from service
- **Our App** = Displays it beautifully!

**API = Application Programming Interface (way to get data from other services)!**

## What You'll Learn 📚

✅ API integration
✅ HTTP requests (GET requests)
✅ JSON data handling
✅ Environment variables
✅ Error handling for APIs
✅ requests library
✅ External API usage
✅ Data parsing and formatting

## What This App Does 🎯

1. **Enter City Name** - User enters a city name
2. **Fetch Weather** - App gets weather from OpenWeatherMap API
3. **Display Weather** - Shows temperature, humidity, wind, etc.
4. **Error Handling** - Shows helpful error messages

**Features:**
- 🌡️ Temperature (Celsius)
- 💧 Humidity percentage
- 💨 Wind speed (km/h)
- 📊 Atmospheric pressure
- 🌤️ Weather description
- 🖼️ Weather icons

## Step-by-Step Explanation 📖

### Step 1: Import Flask and requests
```python
from flask import Flask, render_template, request, flash
import requests
```
**What this does:**
- Gets Flask (for web app)
- Gets requests (for API calls)
- Gets flash (for messages)

**Simple explanation:**
- `requests` = Tool to talk to other websites/APIs
- Like sending a letter and getting a reply!

### Step 2: Set Up API Configuration
```python
API_KEY = os.environ.get('WEATHER_API_KEY', 'your-api-key-here')
API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
```
**What this does:**
- Gets API key from environment variable
- Sets API URL
- API key = Password to access weather API

**Simple explanation:**
- API key = Password
- API URL = Address to get weather from!

### Step 3: Home Route
```python
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
```
**What this does:**
- Shows form to enter city name
- User can input city and submit

**Simple explanation:**
- When someone visits `/`, show the form!

### Step 4: Weather Route
```python
@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    response = requests.get(API_BASE_URL, params=params)
    data = response.json()
```
**What this does:**
- Gets city from form
- Sends request to API
- Gets weather data
- Displays it

**Simple explanation:**
- Get city → Ask API for weather → Get data → Show it!

## Key Concepts 🎓

### 1. APIs (Application Programming Interface)

**What is an API?**
- Way for apps to communicate
- Provides data/services
- Like a menu at a restaurant

**Example:**
- Weather API = Provides weather data
- We send request = "What's weather in London?"
- API sends response = Weather data

**Simple explanation:**
- API = Service that gives you data
- You ask, it answers!

### 2. HTTP Requests

**What are HTTP requests?**
- Way to communicate over internet
- GET = Get data (read)
- POST = Send data (create/update)

**requests.get():**
```python
response = requests.get(url, params=params)
```
- Sends GET request
- Gets response
- Returns response object

**Simple explanation:**
- HTTP request = Asking for something
- GET = "Give me data"

### 3. JSON Data

**What is JSON?**
- JavaScript Object Notation
- Data format (like dictionary)
- Easy for computers to read

**Example:**
```json
{
    "name": "London",
    "temp": 22.5,
    "humidity": 65
}
```

**Parsing JSON:**
```python
data = response.json()
```
- Converts JSON to Python dictionary
- Can access like: `data['name']`

**Simple explanation:**
- JSON = Data format
- Like a dictionary in Python!

### 4. Environment Variables

**What are they?**
- Variables stored in system
- Not in code (more secure)
- Good for API keys

**Getting them:**
```python
API_KEY = os.environ.get('WEATHER_API_KEY')
```
- Gets value from environment
- Returns None if not found

**Simple explanation:**
- Environment variable = Secret stored outside code
- More secure than hardcoding!

### 5. Error Handling

**Why needed?**
- APIs can fail
- Network errors
- Invalid responses

**Try/Except:**
```python
try:
    response = requests.get(url)
except RequestException:
    flash('Error connecting to API')
```
- Tries to get data
- If fails, shows error
- Prevents app crash

**Simple explanation:**
- Try = Attempt
- Except = If it fails, do this
- Prevents crashes!

## How to Run 🚀

### Step 1: Get API Key

1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get your API key
4. Set environment variable:
   ```bash
   # Windows:
   set WEATHER_API_KEY=your-api-key-here
   
   # Mac/Linux:
   export WEATHER_API_KEY=your-api-key-here
   ```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
Visit: `http://127.0.0.1:5000`

**What you'll see:**
- Form to enter city name
- Enter city (e.g., "London")
- Click "Get Weather"
- See weather information!

## Understanding the Flow 🔄

### Complete Flow:

1. **User enters city name**
   - Fills form and submits
   - POST request to `/weather`

2. **Flask gets city name**
   - Extracts from form
   - Validates input

3. **Flask sends API request**
   - Uses requests library
   - Sends city name and API key
   - Waits for response

4. **API responds**
   - Sends weather data (JSON)
   - Contains temperature, humidity, etc.

5. **Flask parses response**
   - Converts JSON to dictionary
   - Extracts needed information
   - Formats for display

6. **Flask displays weather**
   - Shows in template
   - Beautiful card design
   - All weather details

**Simple explanation:**
- Enter city → Ask API → Get data → Parse → Display!

## Files in This Project 📁

```
06-weather-display/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies (Flask, requests)
├── templates/           # HTML templates
│   └── index.html      # Weather form and display
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Key Differences from Previous Projects 🆚

### Project 1-5:
- No external data
- All data from user or hardcoded

### Project 6 (Weather Display):
- **API integration** (external data source)
- **HTTP requests** (talking to other services)
- **JSON parsing** (handling API responses)
- **Environment variables** (secure API keys)
- **Error handling** (network/API errors)

**Progress = You're integrating with external services!**

## Common Questions ❓

### Q: What is an API key?
**A:** Password to access the API. Get it from OpenWeatherMap (free tier available).

### Q: Why use environment variables?
**A:** More secure! Don't put API keys in code. Store them in environment.

### Q: What if API is down?
**A:** Error handling shows user-friendly message. App doesn't crash!

### Q: Can I use other weather APIs?
**A:** Yes! Just change the API_BASE_URL and adjust response parsing.

### Q: Is the API free?
**A:** OpenWeatherMap has a free tier (limited requests per day).

## Practice Exercises 💪

### Exercise 1: Add 5-Day Forecast
Get and display 5-day weather forecast.

### Exercise 2: Add Weather Icons
Display weather icons based on conditions.

### Exercise 3: Add Unit Toggle
Let users switch between Celsius and Fahrenheit.

### Exercise 4: Add Recent Cities
Remember recently searched cities.

## Next Steps 🎯

After completing this project:

1. ✅ Get your API key from OpenWeatherMap
2. ✅ Try different cities
3. ✅ Experiment with API responses
4. ✅ Move to Project 7: URL Shortener

## Congratulations! 🎉

You've learned:
- ✅ API integration
- ✅ HTTP requests
- ✅ JSON handling
- ✅ Environment variables
- ✅ Error handling
- ✅ External services

**You're building apps that use real-world data!** 🚀

---

**Ready for the next project? Try Project 7: URL Shortener!**

