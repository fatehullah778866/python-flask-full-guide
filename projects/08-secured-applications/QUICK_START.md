# Quick Start Guide 🚀

## Get Your Secured Application Running in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask flask-sqlalchemy flask-wtf werkzeug wtforms
```

**That's it! All dependencies installed!**

### Step 2: Run Your Application

Navigate to the project folder:
```bash
cd projects/08-secured-applications
```

Run the app:
```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

**The database (blog.db) will be created automatically!**

### Step 3: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

**Your secured application is live! 🎉**

## What You Can Do

1. **Register** - Create account with secure password hashing
2. **Login** - Sign in with secure password checking
3. **Create Posts** - All input is validated and sanitized
4. **View Security Features** - See all security measures in action

## Security Features to Test

### 1. Password Hashing
- Register a new account
- Check the database - password is hashed, not plain text!

### 2. CSRF Protection
- Try to submit a form without CSRF token - it will be rejected!

### 3. Input Validation
- Try to register with weak password - validation will reject it
- Try to register with invalid email - validation will reject it

### 4. XSS Prevention
- Create a post with HTML/JavaScript - it will be escaped safely

### 5. SQL Injection Prevention
- SQLAlchemy automatically prevents SQL injection

## Understanding Security

### Check Password Hashing:
1. Register a user
2. Check `blog.db` file
3. See that password is hashed (not plain text!)

### Test CSRF Protection:
1. Try to submit form without CSRF token
2. You'll get a CSRF error
3. This prevents fake requests!

### Test Input Validation:
1. Try weak password (less than 8 chars)
2. Try invalid email (no @ symbol)
3. Validation will reject them!

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how security works
2. **Test security features** - Try to break the app (safely!)
3. **Apply to your projects** - Add security to your apps
4. **Learn more** - Advanced security topics

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask_wtf'"
**Solution:** Run `pip install flask-wtf` again

### "CSRF token missing"
**Solution:** Make sure `{{ form.hidden_tag() }}` is in your forms

### "Port already in use"
**Solution:** Close other Flask apps or change port:
```python
app.run(debug=True, port=5001)
```

---

**Have fun with your secured application! 🔒**

