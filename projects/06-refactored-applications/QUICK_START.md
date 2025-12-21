# Quick Start Guide 🚀

## Get Your Refactored Application Running in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask flask-sqlalchemy werkzeug
```

**That's it! All dependencies installed!**

### Step 2: Run Your Application

Navigate to the project folder:
```bash
cd projects/06-refactored-applications
```

Run the app:
```bash
python run.py
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

**Your refactored application is live! 🎉**

## What You Can Do

1. **View Home** - See the main page
2. **View About** - Learn about refactoring
3. **View Posts** - See all blog posts
4. **Create Posts** - Add new posts
5. **Register/Login** - Create account and login
6. **Test Error Pages** - Visit a non-existent page (404)

## Project Structure

```
app/
├── __init__.py      # Application factory
├── models.py        # Database models
├── config.py        # Configuration
├── main/            # Main blueprint (home, about)
├── posts/           # Posts blueprint (blog posts)
└── auth/            # Auth blueprint (login, register)
```

## Key Features

- ✅ **Application Factory** - Better app creation
- ✅ **Blueprints** - Organized code modules
- ✅ **Configuration** - Separate settings
- ✅ **Error Handling** - Custom error pages
- ✅ **Professional Structure** - Clean organization

## Understanding the Structure

### Application Factory (`app/__init__.py`)
- Creates the Flask app
- Registers blueprints
- Sets up error handlers

### Blueprints
- **main** - Home and about pages
- **posts** - Blog post management
- **auth** - User authentication

### Configuration (`app/config.py`)
- Development settings
- Production settings
- Environment variables

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how everything works
2. **Explore the code** - See how blueprints work
3. **Add features** - Create new blueprints
4. **Refactor your projects** - Apply these patterns

## Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
**Solution:** Make sure you're running from the project root directory

### "Port already in use"
**Solution:** Close other Flask apps or change port in `run.py`:
```python
app.run(debug=True, port=5001)
```

### Import errors
**Solution:** Make sure all `__init__.py` files exist in blueprint folders

---

**Have fun with your refactored application! 🔧**

