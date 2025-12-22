# Project 11: Blog (Simple with Database) 📝

Welcome to Project 11! This app creates a simple blog with database storage!

## What is This Project? 🤔

**Simple Blog** = An app that stores blog posts in a database!

**Think of it like:**
- **Blog** = Website where you write posts
- **Database** = Permanent storage for posts
- **CRUD** = Create, Read, Update, Delete operations

**Database = Permanent storage that persists!**

## What You'll Learn 📚

✅ Database integration (SQLite)
✅ SQLAlchemy ORM
✅ Database models
✅ CRUD operations
✅ Database queries
✅ Form handling
✅ Data persistence

## What This App Does 🎯

1. **Create Posts** - Write and save blog posts
2. **View Posts** - See all posts on home page
3. **Read Post** - View individual posts
4. **Database Storage** - Posts saved permanently

**Features:**
- 📝 Create blog posts
- 📋 View all posts
- 📖 Read individual posts
- 💾 Database storage (SQLite)
- 📅 Automatic timestamps

## Step-by-Step Explanation 📖

### Step 1: Database Setup
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
```
**What this does:**
- Configures database location
- Creates database object
- Sets up SQLite database

**Simple explanation:**
- Database = File to store data
- SQLite = Simple file-based database!

### Step 2: Create Model
```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
```
**What this does:**
- Defines post structure
- Creates database table
- Sets up columns

**Simple explanation:**
- Model = Template for data
- Columns = Fields in database!

### Step 3: Create Post
```python
new_post = Post(title=title, content=content)
db.session.add(new_post)
db.session.commit()
```
**What this does:**
- Creates post object
- Adds to database
- Saves permanently

**Simple explanation:**
- Create = Make new post
- Add = Stage for saving
- Commit = Save permanently!

## Key Concepts 🎓

### 1. Databases

**What is a database?**
- Permanent storage for data
- Organized in tables
- Like a digital filing cabinet

**SQLite:**
- File-based database
- No server needed
- Perfect for learning

### 2. SQLAlchemy ORM

**What is ORM?**
- Object-Relational Mapping
- Works with Python objects
- Converts to database operations

**Simple explanation:**
- ORM = Python objects → Database
- Easy to use!

### 3. Database Models

**What are models?**
- Python classes
- Represent database tables
- Define structure

**Example:**
```python
class Post(db.Model):
    title = db.Column(db.String(200))
```

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Click "Create New Post"
2. Fill in title and content
3. Submit form
4. View posts on home page!

## Files in This Project 📁

```
11-blog-simple-database/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Home page (all posts)
│   ├── post.html       # Single post view
│   └── create.html    # Create post form
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try creating multiple posts
2. ✅ View individual posts
3. ✅ Move to Project 12: User Registration System

---

**Ready for the next project? Try Project 12: User Registration System!**

