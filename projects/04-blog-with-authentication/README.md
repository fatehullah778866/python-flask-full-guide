# Project 4: Blog with Authentication 🔐

Welcome to Project 4! We're going to add user authentication to our blog so only logged-in users can create and edit posts!

## What is Authentication? 🤔

**Authentication** = Making sure only the right people can access things

Think of it like:
- **Authentication** = A lock on your door
- **Password** = The key to unlock
- **Only you** = Can open the door with your key!

**Authentication = Protecting your blog so only you can edit it!**

## What We'll Build 🎯

We'll add to our blog:
1. **User Registration** - People can create accounts
2. **User Login** - People can sign in
3. **Password Protection** - Passwords are encrypted (safe!)
4. **Protected Routes** - Only logged-in users can create/edit posts
5. **User Sessions** - Stay logged in
6. **Logout** - Sign out when done

**Complete authentication system!**

## What You'll Learn 📚

- ✅ How to create user accounts
- ✅ How to hash passwords securely
- ✅ How to handle user login
- ✅ How to manage sessions
- ✅ How to protect routes
- ✅ How to check if user is logged in

## Step-by-Step Guide 📋

Follow these steps in order:

1. **Setup** - Add authentication to blog
2. **User Model** - Create user database model
3. **Registration** - Let users create accounts
4. **Login** - Let users sign in
5. **Password Hashing** - Secure passwords
6. **Session Management** - Keep users logged in
7. **Protect Routes** - Only logged-in users can post

## Files We'll Create 📁

```
04-blog-with-authentication/
├── app.py              # Main Flask app with auth
├── requirements.txt    # Dependencies
├── README.md          # This file
├── PROJECT_GUIDE.md   # Complete guide
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # List all posts
│   ├── post.html      # View single post
│   ├── create.html    # Create post (protected)
│   ├── edit.html      # Edit post (protected)
│   ├── register.html  # User registration
│   └── login.html     # User login
├── static/            # CSS
│   └── style.css      # Stylesheet
└── blog.db            # SQLite database
```

## How to Run 🚀

1. **Install Dependencies:**
   ```bash
   pip install flask flask-sqlalchemy werkzeug
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Next Steps 🎯

Read `PROJECT_GUIDE.md` for detailed step-by-step instructions!

---

**Let's secure your blog! 🔒**

