# Project 7: URL Shortener (Simple) 🔗

Welcome to Project 7! This app shortens long URLs using session storage!

## What is This Project? 🤔

**URL Shortener** = An app that makes long URLs short!

**Think of it like:**
- **Long URL** = https://www.example.com/very/long/complicated/url
- **Short URL** = http://127.0.0.1:5000/abc123
- **Same destination** = Both go to the same place!

**Short = Easy to share and remember!**

## What You'll Learn 📚

✅ Session storage with dictionaries
✅ String manipulation
✅ Random code generation
✅ URL validation
✅ Redirect functionality
✅ Dictionary operations
✅ Duplicate checking

## What This App Does 🎯

1. **Enter Long URL** - User enters a long URL
2. **Generate Short Code** - App creates random short code
3. **Store Mapping** - Saves short code → long URL
4. **Redirect** - Clicking short URL goes to original

**Features:**
- 🔗 Shorten any URL
- 📋 Copy short URL
- 🔄 Redirect to original
- 💾 Session-based storage

## Step-by-Step Explanation 📖

### Step 1: Generate Short Code
```python
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
```
**What this does:**
- Creates random string
- Uses letters and digits
- Returns short code

**Simple explanation:**
- Random code = Like a random password
- Used to identify the URL!

### Step 2: Shorten URL
```python
short_code = generate_short_code()
urls[short_code] = long_url
```
**What this does:**
- Generates code
- Stores mapping
- Saves to session

**Simple explanation:**
- Create code → Link to URL → Save it!

### Step 3: Redirect
```python
@app.route('/<short_code>')
def redirect_to_url(short_code):
    return redirect(urls[short_code])
```
**What this does:**
- Gets short code from URL
- Looks up original URL
- Redirects to it

**Simple explanation:**
- Visit short URL → Find original → Go there!

## Key Concepts 🎓

### 1. Dictionary Storage

**What is a dictionary?**
- Key-value pairs
- Like a phone book
- Key = Short code
- Value = Long URL

**Example:**
```python
urls = {
    'abc123': 'https://example.com',
    'xyz789': 'https://google.com'
}
```

### 2. Random Code Generation

**How it works:**
- Pick random characters
- Combine into string
- Use as identifier

**Simple explanation:**
- Random = Unpredictable
- Code = Identifier for URL!

### 3. URL Validation

**What we do:**
- Check if URL has http://
- Add it if missing
- Make URL valid

**Simple explanation:**
- Validate = Make sure it's correct
- Add protocol if needed!

## How to Run 🚀

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Enter long URL
2. Click "Shorten URL"
3. Copy short URL
4. Click short URL to test redirect!

## Files in This Project 📁

```
07-url-shortener/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # URL shortener form
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try shortening different URLs
2. ✅ Test the redirect functionality
3. ✅ Move to Project 8: Password Generator

---

**Ready for the next project? Try Project 8: Password Generator!**

