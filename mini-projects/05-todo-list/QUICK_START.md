# Quick Start Guide 🚀

Get your Simple To-Do List running in 3 steps!

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
3. You'll see the to-do list interface!

**How to use:**
1. **Add Task:** Enter task in input field, click "Add Task"
2. **Mark Complete:** Click "✅ Mark Complete" button
3. **Mark Incomplete:** Click "⏪ Mark Incomplete" button
4. **Delete Task:** Click "🗑️ Delete" button (with confirmation)

**That's it!** You've successfully run your To-Do List app! 🎉

## Try These Features! ✨

- **Add Tasks** - Enter multiple tasks
- **Mark Complete** - Toggle task completion
- **Delete Tasks** - Remove tasks you don't need
- **Session Persistence** - Refresh page (tasks stay!)
- **Responsive Design** - Works on mobile devices

## Important Notes 📝

### Session Storage
- Tasks are stored in session
- They persist during browser session
- **Lost when you close the browser** (this is normal!)
- To persist forever, you'd need a database (we'll learn that later)

### Secret Key
- The app uses a simple secret key
- In production, use a secure, random key
- Never commit secret keys to version control

## Troubleshooting 🔧

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask first:
```bash
pip install flask
```

### Problem: "Template not found"
**Solution:** Make sure you have a `templates/` folder with:
- `index.html`

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

### Problem: Tasks disappear after closing browser
**Solution:** This is normal! Sessions are temporary. To persist forever, use a database.

### Problem: Tasks not saving
**Solution:** Make sure `session.modified = True` is set after modifying tasks.

## What's Next? 🎯

1. ✅ Try adding, completing, and deleting tasks
2. ✅ Refresh the page (tasks should stay!)
3. ✅ Read `EXPLANATION.md` for detailed explanations
4. ✅ Experiment with the code
5. ✅ Add more features (edit, due dates, priorities)
6. ✅ Move to Project 6: Weather Display App

---

**Congratulations! You've built a functional to-do list! 🎉**

