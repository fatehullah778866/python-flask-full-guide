# Quick Start Guide 🚀

Get your Weather Display App running in 4 steps!

## Step 1: Get API Key 🔑

1. Go to https://openweathermap.org/api
2. Click "Sign Up" (free account)
3. Verify your email
4. Go to "API Keys" section
5. Copy your API key

**Note:** Free tier allows 60 requests/minute and 1,000,000 requests/month

## Step 2: Set Environment Variable 📝

**Windows (Command Prompt):**
```bash
set WEATHER_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:WEATHER_API_KEY="your-api-key-here"
```

**Mac/Linux:**
```bash
export WEATHER_API_KEY=your-api-key-here
```

**What this does:**
- Stores API key in environment
- App reads it from there
- More secure than hardcoding!

## Step 3: Install Dependencies 📦

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

**What this does:**
- Installs Flask
- Installs requests library
- Makes everything available

**Expected output:**
```
Successfully installed Flask-3.0.0 requests-2.31.0
```

## Step 4: Run the App ▶️

In the same terminal, run:

```bash
python app.py
```

**What you'll see:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
Press CTRL+C to quit
```

**What this means:**
- Your Flask app is running!
- It's available at `http://127.0.0.1:5000`
- Debug mode is on (shows errors)

## Step 5: Open in Browser 🌐

1. Open your web browser
2. Go to: `http://127.0.0.1:5000`
3. You'll see the weather form!

**How to use:**
1. Enter a city name (e.g., "London", "New York", "Tokyo")
2. Click "🔍 Get Weather" button
3. See the weather information!

**That's it!** You've successfully run your Weather Display App! 🎉

## Try These Cities! 🌍

- **London** - United Kingdom
- **New York** - United States
- **Tokyo** - Japan
- **Paris** - France
- **Sydney** - Australia

## Troubleshooting 🔧

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "ModuleNotFoundError: No module named 'requests'"
**Solution:** Install requests:
```bash
pip install requests
```

### Problem: "Invalid API key"
**Solution:** 
- Check you set the environment variable correctly
- Make sure API key is correct
- Verify API key in OpenWeatherMap dashboard

### Problem: "City not found"
**Solution:**
- Check spelling of city name
- Try full city name (e.g., "New York" not "NY")
- Some cities might not be in database

### Problem: "Error connecting to weather service"
**Solution:**
- Check internet connection
- API might be temporarily down
- Try again in a few minutes

### Problem: Environment variable not working
**Solution:**
- Make sure you set it in the same terminal
- Restart terminal after setting
- Or set it directly in code (for testing only):
```python
API_KEY = 'your-api-key-here'  # For testing only!
```

## What's Next? 🎯

1. ✅ Try different cities
2. ✅ Read `EXPLANATION.md` for detailed explanations
3. ✅ Experiment with API responses
4. ✅ Add more features (forecast, icons, etc.)
5. ✅ Move to Project 7: URL Shortener

---

**Congratulations! You've built an app that uses real-world data! 🎉**

