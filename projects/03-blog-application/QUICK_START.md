# Quick Start Guide 🚀

## Get Your Blog Running in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask flask-sqlalchemy
```

**That's it! All dependencies installed!**

### Step 2: Run Your Blog

Navigate to the project folder:
```bash
cd projects/03-blog-application
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

**Your blog is live! 🎉**

## What You Can Do

1. **View Posts** - See all blog posts on the home page
2. **Create Post** - Click "Create New Post" to add a post
3. **Read Post** - Click on any post title to read it
4. **Edit Post** - Click "Edit" to modify a post
5. **Delete Post** - Click "Delete" to remove a post

## Testing Your Blog

1. **Create your first post:**
   - Click "Create New Post"
   - Fill in title, author, and content
   - Click "Create Post"
   - You should see it on the home page!

2. **View the post:**
   - Click on the post title
   - See the full content

3. **Edit the post:**
   - Click "Edit"
   - Change something
   - Click "Update Post"

4. **Delete the post:**
   - Click "Delete"
   - Confirm deletion
   - Post is removed!

## Database File

- **blog.db** - SQLite database file (created automatically)
- **Location** - In the project folder
- **Contains** - All your blog posts

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how everything works
2. **Add more posts** - Create multiple blog posts
3. **Customize** - Change styling and add features
4. **Deploy** - Put it online!

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install flask flask-sqlalchemy` again

### "Port already in use"
**Solution:** Close other Flask apps or change port:
```python
app.run(debug=True, port=5001)
```

### Database not created
**Solution:** Make sure you run `python app.py` from the project folder. The database is created automatically.

### Posts not showing
**Solution:** Make sure you've created at least one post. The database starts empty.

---

**Have fun blogging! 📝**

