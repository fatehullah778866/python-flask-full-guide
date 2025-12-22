# Getting Started with Mini Projects 🚀

Welcome! This guide will help you get started with building mini Flask projects.

## What You Need 📋

### Prerequisites

Before starting, make sure you have:

✅ **Python 3.7+** installed
✅ **Basic Flask knowledge** (from the main course)
✅ **Code editor** (VS Code, PyCharm, etc.)
✅ **Terminal/Command Prompt** access
✅ **Internet connection** (for some projects)

### Required Knowledge

You should know:
- How to create Flask apps
- Basic routing
- Templates and Jinja2
- Forms (basic)
- Database basics (for intermediate/advanced)

**Don't worry if you're new!** Start with beginner projects!

## Setting Up Your Environment 🛠️

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Flask

```bash
pip install flask
```

### Step 3: Create Project Folder

```bash
mkdir my-mini-project
cd my-mini-project
```

## Project Workflow 🔄

### For Each Project:

1. **Read the Plan**
   - Understand what to build
   - Note required concepts
   - Check difficulty level

2. **Set Up Project**
   - Create folder
   - Set up virtual environment
   - Install dependencies

3. **Plan Your Code**
   - List features needed
   - Plan file structure
   - Think about routes

4. **Start Building**
   - Create `app.py`
   - Add routes one by one
   - Test as you go

5. **Add Templates**
   - Create HTML templates
   - Style with CSS
   - Make it look good!

6. **Test Everything**
   - Test all features
   - Fix any bugs
   - Improve if needed

7. **Document**
   - Add README
   - Comment your code
   - Note what you learned

## Project Structure Template 📁

Use this structure for most projects:

```
project-name/
├── app.py                 # Main Flask application
├── models.py              # Database models (if needed)
├── requirements.txt       # Dependencies
├── README.md              # Project description
├── templates/             # HTML templates
│   ├── base.html         # Base template (optional)
│   └── index.html        # Main template
├── static/                # Static files
│   ├── style.css         # Stylesheet
│   └── script.js         # JavaScript (if needed)
└── .gitignore            # Git ignore file
```

## Common Dependencies 📦

### Basic Projects:
```txt
Flask==3.0.0
```

### With Database:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
```

### With Forms:
```txt
Flask==3.0.0
Flask-WTF==1.2.1
WTForms==3.1.1
```

### With Authentication:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
```

## Quick Start Template 🎯

Here's a basic template to start any project:

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Project</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Welcome!</h1>
</body>
</html>
```

**static/style.css:**
```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
```

## Tips for Success 💡

### 1. Start Small
- Build basic version first
- Add features gradually
- Don't try to do everything at once

### 2. Test Frequently
- Test after each feature
- Fix bugs immediately
- Make sure everything works

### 3. Read Documentation
- Flask official docs
- Library documentation
- Stack Overflow for help

### 4. Experiment
- Try different approaches
- Add your own features
- Make it your own!

### 5. Don't Give Up
- Projects get easier with practice
- Each project teaches something new
- You're learning and improving!

## Common Issues & Solutions 🔧

### Issue: Module not found
**Solution:** Make sure virtual environment is activated and dependencies are installed

### Issue: Port already in use
**Solution:** Change port: `app.run(port=5001)` or stop other Flask apps

### Issue: Template not found
**Solution:** Check `templates/` folder exists and file names match

### Issue: Static files not loading
**Solution:** Check `static/` folder exists and use `url_for('static', ...)`

### Issue: Database errors
**Solution:** Make sure database file has write permissions and models are correct

## Learning Path 🎓

### Recommended Order:

1. **Beginner (1-5)**
   - Start here if you're new
   - Build confidence
   - Learn basics

2. **Beginner (6-10)**
   - Slightly more complex
   - Introduce new concepts
   - Build on basics

3. **Intermediate (11-15)**
   - Add database
   - More features
   - Real applications

4. **Intermediate (16-20)**
   - Complex features
   - Multiple models
   - Advanced concepts

5. **Advanced (21-30)**
   - Real-world applications
   - Complex systems
   - Professional features

## Tracking Progress 📊

Keep track of completed projects:

- [ ] Project 1: Hello World
- [ ] Project 2: Personal Greeting
- [ ] Project 3: Simple Calculator
- ... (and so on)

## Resources 📚

### Documentation:
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Flask-WTF: https://flask-wtf.readthedocs.io/

### Learning:
- Flask Tutorial: Official Flask tutorial
- Practice: Build projects regularly
- Community: Join Flask communities

## Next Steps 🚀

1. **Choose a project** from PROJECT_PLAN.md
2. **Read the plan** carefully
3. **Set up your environment**
4. **Start coding!**
5. **Have fun learning!**

---

**You're ready to start building! Pick a project and begin! 🎉**

