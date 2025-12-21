# Lesson 1.2: Setting Up Flask - Getting Ready to Build! 🛠️

## What We're Going to Do 📋

Before we can build websites with Flask, we need to:
1. Make sure Python is installed
2. Create a special folder (called a "virtual environment")
3. Install Flask in that folder

Think of it like setting up a workspace before you start building!

## Step 1: Check if Python is Installed 🐍

Python is the programming language Flask uses. Let's check if you have it!

### How to Check:

1. Open your terminal/command prompt
2. Type this and press Enter:
   ```bash
   python --version
   ```

### What You Should See:

If Python is installed, you'll see something like:
```
Python 3.10.5
```
or
```
Python 3.11.2
```

**Any version 3.8 or higher is good!**

### If Python is NOT Installed:

Don't worry! Go to https://www.python.org/downloads/ and download Python. Make sure to check "Add Python to PATH" when installing!

## Step 2: Understanding Virtual Environments 🏠

### What is a Virtual Environment?

Imagine you're working on multiple art projects:
- Project 1 needs red paint
- Project 2 needs blue paint
- Project 3 needs both!

If you mix all your paints together, it becomes a mess! 🎨

A **virtual environment** is like having separate paint boxes for each project. Each project has its own tools and doesn't interfere with others!

### Why Do We Need This?

- **Isolation**: Your Flask project won't mess with other Python projects
- **Organization**: Everything Flask needs is in one place
- **Cleanliness**: Keeps your computer organized

## Step 3: Create Your Project Folder 📁

Let's create a special folder for our Flask learning!

### On Windows (PowerShell):
```bash
# Navigate to your desktop or where you want to work
cd Desktop

# Create a new folder
mkdir my-first-flask-app
cd my-first-flask-app
```

### What Just Happened?
- `mkdir` = "make directory" (create a folder)
- `cd` = "change directory" (go into a folder)
- We created a folder called `my-first-flask-app` and went into it!

## Step 4: Create a Virtual Environment 🏗️

Now let's create our special workspace (virtual environment):

```bash
python -m venv venv
```

### Breaking This Down:
- `python` = We're using Python
- `-m venv` = "Make a virtual environment"
- `venv` = The name of our virtual environment (you can call it anything, but "venv" is common)

### What Happened?
Python created a folder called `venv` with all the tools we need!

## Step 5: Activate the Virtual Environment 🚀

Now we need to "turn on" our virtual environment. It's like turning on the lights in your workspace!

### On Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```

### On Windows (Command Prompt):
```bash
venv\Scripts\activate.bat
```

### On Mac/Linux:
```bash
source venv/bin/activate
```

### How Do You Know It Worked?

You'll see `(venv)` at the beginning of your command line:
```
(venv) C:\Users\dell\Desktop\my-first-flask-app>
```

This means your virtual environment is ACTIVE! 🎉

### To Deactivate (Turn Off):
When you're done working, you can turn it off:
```bash
deactivate
```

## Step 6: Install Flask 📦

Now let's install Flask! It's like downloading the tools you need.

```bash
pip install flask
```

### What is `pip`?
`pip` is like an app store for Python tools. It downloads and installs things for you!

### What Just Happened?
- `pip` = Python's package installer
- `install` = Download and set up
- `flask` = The Flask tool we want

### You Should See:
```
Collecting flask
  Downloading flask-3.0.0-py3-none-any.whl
  ...
Successfully installed flask-3.0.0
```

This means Flask is now installed! ✅

## Step 7: Verify Flask is Installed ✅

Let's make sure Flask is ready to use:

```bash
python -c "import flask; print(flask.__version__)"
```

You should see a version number like `3.0.0` or similar!

## Common Problems and Solutions 🔧

### Problem 1: "python is not recognized"
**Solution**: Python isn't in your PATH. Reinstall Python and check "Add Python to PATH"

### Problem 2: "pip is not recognized"
**Solution**: Make sure Python is installed correctly. Try `python -m pip install flask` instead

### Problem 3: "Activate.ps1 cannot be loaded"
**Solution**: Run this in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Your Workspace is Ready! 🎉

Now you have:
- ✅ Python installed
- ✅ A project folder
- ✅ A virtual environment
- ✅ Flask installed

## Quick Reference Card 📝

```bash
# 1. Create folder
mkdir my-first-flask-app
cd my-first-flask-app

# 2. Create virtual environment
python -m venv venv

# 3. Activate it (Windows PowerShell)
venv\Scripts\Activate.ps1

# 4. Install Flask
pip install flask

# 5. Verify installation
python -c "import flask; print(flask.__version__)"
```

## What's Next? 🚀

Now that Flask is installed, let's create our first website! In the next lesson, we'll build a "Hello World" app - the simplest website possible!

---

**Remember**: Every time you want to work on your Flask project:
1. Go to your project folder
2. Activate the virtual environment
3. Start coding!

