# Quick Start Guide 🚀

Get your Simple Calculator running in 3 steps!

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
3. You'll see a calculator form!

**How to use:**
1. Enter the first number
2. Select an operation (add, subtract, multiply, or divide)
3. Enter the second number
4. Click "Calculate"
5. See the result!

**That's it!** You've successfully run your Simple Calculator! 🎉

## Try These Calculations! 🧮

- **Addition:** 5 + 3 = 8
- **Subtraction:** 10 - 4 = 6
- **Multiplication:** 6 × 7 = 42
- **Division:** 20 ÷ 4 = 5

## Troubleshooting 🔧

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install Flask first:
```bash
pip install flask
```

### Problem: "Template not found"
**Solution:** Make sure you have a `templates/` folder with:
- `calculator.html`

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

### Problem: "Cannot divide by zero"
**Solution:** This is expected! The app prevents division by zero. Try a different number.

### Problem: "Please enter valid numbers"
**Solution:** Make sure you enter actual numbers, not text. The app validates input.

## What's Next? 🎯

1. ✅ Try different calculations
2. ✅ Read `EXPLANATION.md` for detailed explanations
3. ✅ Experiment with the code
4. ✅ Add more operations (power, modulo, etc.)
5. ✅ Move to Project 4: Random Quote Generator

---

**Congratulations! You've built an interactive calculator! 🎉**

