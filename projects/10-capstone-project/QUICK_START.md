# Quick Start Guide 🚀

Get your Capstone Project running in minutes!

## Step 1: Install Dependencies 📦

```bash
pip install -r requirements.txt
```

**What this does:**
- Installs Flask and all needed packages
- Like getting all ingredients before cooking!

## Step 2: Run the Application ▶️

```bash
python run.py
```

**What this does:**
- Starts the Flask development server
- Creates the database automatically
- Opens at `http://127.0.0.1:5000`

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

## Step 3: Open in Browser 🌐

Visit: `http://127.0.0.1:5000`

**What you'll see:**
- Home page with features
- Navigation menu
- Welcome message

## Step 4: Create an Account 👤

1. Click **"Register"** in navigation
2. Fill in:
   - Username (at least 3 characters)
   - Email (valid email address)
   - Password (at least 8 characters)
3. Click **"Register"**

**What happens:**
- Account is created
- Password is securely hashed
- You're redirected to login

## Step 5: Login 🔐

1. Enter your username and password
2. Click **"Login"**

**What happens:**
- Session is created
- You're logged in
- Navigation shows your username

## Step 6: Create Your First Post 📝

1. Click **"New Post"** in navigation
2. Fill in:
   - Title (what your post is about)
   - Content (the actual post)
3. Click **"Save Post"**

**What happens:**
- Post is saved to database
- You can view, edit, or delete it

## Step 7: Explore Features 🎯

**Try these:**
- View all posts: `/posts/`
- View your profile: Click your username
- Edit a post: Click "Edit" on your posts
- Delete a post: Click "Delete" on your posts
- View About page: `/about`

## Step 8: Test the API 🌐

**Health Check:**
```bash
curl http://127.0.0.1:5000/api/health
```

**Get All Posts:**
```bash
curl http://127.0.0.1:5000/api/posts
```

**Create Post (after login):**
```bash
curl -X POST http://127.0.0.1:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "API Post", "content": "Created via API"}'
```

## Step 9: Run Tests 🧪

```bash
pytest
```

**What this does:**
- Runs all test files
- Checks if everything works
- Shows test results

## Troubleshooting 🔧

**Problem: Module not found**
- Solution: Make sure you installed requirements.txt

**Problem: Database error**
- Solution: Delete `capstone.db` and run again

**Problem: Port already in use**
- Solution: Change port in `run.py` or stop other Flask apps

## Next Steps 📚

1. **Read PROJECT_GUIDE.md** - Learn how everything works
2. **Explore the code** - See how it's structured
3. **Modify features** - Add your own ideas!
4. **Deploy it** - Put it online!

---

**You're ready to go! 🎉**

