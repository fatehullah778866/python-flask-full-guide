# Quick Start Guide 🚀

Get your Personal Greeting App running in 3 steps!

## Step 1: Install Flask 📦

Open your terminal/command prompt and run:

```bash
pip install flask
```

**Or use requirements.txt:**
```bash
pip install -r requirements.txt
```

**What this does:**
- Installs Flask library
- Makes Flask available to use

**Expected output:**
```
Successfully installed flask-3.0.0
```

## Step 2: Run the App ▶️

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

## Step 3: Open in Browser 🌐

### Option 1: Use the Form

1. Open your web browser
2. Go to: `http://127.0.0.1:5000`
3. You'll see a form to enter your name
4. Enter your name and click "Get Greeting!"
5. You'll see: **Hello, [Your Name]!**

### Option 2: Direct URL

1. Open your web browser
2. Go to: `http://127.0.0.1:5000/hello/YourName`
3. Replace "YourName" with your actual name
4. Example: `http://127.0.0.1:5000/hello/John`
5. You'll see: **Hello, John!**

**That's it!** You've successfully run your Personal Greeting App! 🎉

## Try Different Names! 🎯

Try these URLs:
- `http://127.0.0.1:5000/hello/John`
- `http://127.0.0.1:5000/hello/Sarah`
- `http://127.0.0.1:5000/hello/Bob`
- `http://127.0.0.1:5000/hello/YourName`

**Each one shows a personalized greeting!**

## Troubleshooting 🔧

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask first:
```bash
pip install flask
```

### Problem: "Template not found"
**Solution:** Make sure you have a `templates/` folder with:
- `index.html`
- `greeting.html`

### Problem: "Static file not found"
**Solution:** Make sure you have a `static/` folder with:
- `style.css`

### Problem: "Address already in use"
**Solution:** Another Flask app is running. Either:
- Stop the other app (Ctrl+C)
- Or change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Problem: Name doesn't appear in greeting
**Solution:** 
- Check the route has `<name>` parameter
- Check function has `name` parameter
- Check template uses `{{ name }}`

## What's Next? 🎯

1. ✅ Try different names in the URL
2. ✅ Read `EXPLANATION.md` for detailed explanations
3. ✅ Experiment with the code
4. ✅ Move to Project 3: Simple Calculator

---

**Congratulations! You've built a dynamic Flask app! 🎉**

