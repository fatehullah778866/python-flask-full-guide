# Quick Start Guide 🚀

## Get Your Authenticated Blog Running in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask flask-sqlalchemy werkzeug
```

**That's it! All dependencies installed!**

### Step 2: Run Your Blog

Navigate to the project folder:
```bash
cd projects/04-blog-with-authentication
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

**Your authenticated blog is live! 🎉**

## What You Can Do

1. **Register** - Create a new account
2. **Login** - Sign in to your account
3. **Create Posts** - Only logged-in users can create posts
4. **Edit Posts** - Only you can edit your own posts
5. **Delete Posts** - Only you can delete your own posts
6. **Logout** - Sign out when done

## Testing Your Blog

1. **Register a new account:**
   - Click "Register"
   - Fill in username, email, and password
   - Click "Register"
   - You should see a success message!

2. **Login:**
   - Click "Login"
   - Enter your username and password
   - Click "Login"
   - You should see "Hello, [username]!" in the nav

3. **Create a post:**
   - Click "New Post" (only visible when logged in)
   - Fill in title and content
   - Click "Create Post"
   - Your post appears on the home page!

4. **Edit your post:**
   - Click "Edit" on your post
   - Make changes
   - Click "Update Post"

5. **Try to edit someone else's post:**
   - You'll get an error message!
   - Only post owners can edit their posts

6. **Logout:**
   - Click "Logout"
   - You're signed out!

## Security Features

- ✅ **Password Hashing** - Passwords are encrypted
- ✅ **Session Management** - Stay logged in
- ✅ **Protected Routes** - Only logged-in users can post
- ✅ **Ownership Check** - Only you can edit/delete your posts

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how everything works
2. **Create multiple accounts** - Test with different users
3. **Test security** - Try accessing protected pages without login
4. **Customize** - Add more features

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install flask flask-sqlalchemy werkzeug` again

### "Port already in use"
**Solution:** Close other Flask apps or change port:
```python
app.run(debug=True, port=5001)
```

### Can't create posts
**Solution:** Make sure you're logged in! Only logged-in users can create posts.

### Can't edit/delete posts
**Solution:** You can only edit/delete your own posts. Make sure you're logged in as the post owner.

---

**Have fun with your secure blog! 🔒**

