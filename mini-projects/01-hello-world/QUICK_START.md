# Quick Start Guide 🚀

Get your Hello World Flask app running in 3 steps!

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

1. Open your web browser
2. Go to: `http://127.0.0.1:5000`
3. You should see: **Hello, World!**

**That's it!** You've successfully run your first Flask app! 🎉

## Troubleshooting 🔧

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask first:
```bash
pip install flask
```

### Problem: "python: command not found"
**Solution:** Try:
```bash
python3 app.py
```
Or make sure Python is installed.

### Problem: "Address already in use"
**Solution:** Another Flask app is running. Either:
- Stop the other app (Ctrl+C)
- Or change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Problem: Nothing happens when I visit the URL
**Solution:** 
- Make sure the app is running (you should see the running message)
- Check you're visiting `http://127.0.0.1:5000` (not `https://`)
- Try `http://localhost:5000` instead

## What's Next? 🎯

1. ✅ Try changing the message in `app.py`
2. ✅ Read `EXPLANATION.md` for detailed explanations
3. ✅ Move to Project 2: Personal Greeting App

---

**Congratulations! You've built your first Flask app! 🎉**

