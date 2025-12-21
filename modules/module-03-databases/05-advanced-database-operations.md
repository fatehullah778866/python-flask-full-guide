# Lesson 3.5: Advanced Database Operations - Power User Skills! ⚡

## What We'll Learn 🎯

Now that you know the basics, let's learn advanced techniques:
- Pagination (showing data in pages)
- Complex queries
- Aggregations (counting, summing)
- Database optimization
- Transactions

## Pagination 📄

### What is Pagination?

Instead of showing 1000 posts at once, show 10 per page!

**Like**: Google search results - you see page 1, then click "Next" for page 2.

### Basic Pagination

```python
from flask import request

@app.route('/posts')
def show_posts():
    # Get page number from URL (default: page 1)
    page = request.args.get('page', 1, type=int)
    
    # Get 10 posts per page
    posts = Post.query.paginate(page=page, per_page=10, error_out=False)
    
    result = []
    for post in posts.items:
        result.append(f"<h3>{post.title}</h3>")
        result.append(f"<p>{post.content[:100]}...</p>")
    
    # Add pagination links
    if posts.has_prev:
        result.append(f'<a href="/posts?page={posts.prev_num}">Previous</a> ')
    if posts.has_next:
        result.append(f'<a href="/posts?page={posts.next_num}">Next</a>')
    
    return '<br>'.join(result)
```

### Understanding Pagination:

- **`paginate(page=1, per_page=10)`** = Get page 1, 10 items per page
- **`posts.items`** = List of posts on this page
- **`posts.has_prev`** = True if there's a previous page
- **`posts.has_next`** = True if there's a next page
- **`posts.prev_num`** = Previous page number
- **`posts.next_num`** = Next page number
- **`posts.pages`** = Total number of pages

## Complex Queries 🔍

### Joining Tables

```python
# Get all posts with their authors
posts = Post.query.join(User).all()
for post in posts:
    print(f"{post.title} by {post.author.name}")

# Get posts with filters
posts = Post.query.join(User).filter(User.name == "John").all()
```

### Subqueries

```python
from sqlalchemy import func

# Get users who have written more than 5 posts
subquery = db.session.query(Post.user_id).group_by(Post.user_id).having(func.count(Post.id) > 5).subquery()
users = User.query.filter(User.id.in_(subquery)).all()
```

### Ordering and Grouping

```python
# Order by created date (newest first)
posts = Post.query.order_by(Post.created_at.desc()).all()

# Group by user and count posts
from sqlalchemy import func
result = db.session.query(User.name, func.count(Post.id)).join(Post).group_by(User.id).all()
for name, count in result:
    print(f"{name} has {count} posts")
```

## Aggregations (Counting, Summing) 📊

### Count Records

```python
# Count all users
user_count = User.query.count()

# Count posts by a user
user = User.query.get(1)
post_count = Post.query.filter_by(user_id=user.id).count()

# Or using relationship
post_count = len(user.posts)
```

### Sum and Average

```python
from sqlalchemy import func

# Sum of all ages
total_age = db.session.query(func.sum(User.age)).scalar()

# Average age
avg_age = db.session.query(func.avg(User.age)).scalar()

# Count posts per user
post_counts = db.session.query(User.name, func.count(Post.id)).join(Post).group_by(User.id).all()
```

### Min and Max

```python
from sqlalchemy import func

# Oldest user
oldest = db.session.query(func.max(User.age)).scalar()

# Youngest user
youngest = db.session.query(func.min(User.age)).scalar()

# Most recent post
recent_post = Post.query.order_by(Post.created_at.desc()).first()
```

## Filtering with Multiple Conditions 🔧

### AND Conditions

```python
# Multiple conditions (AND)
posts = Post.query.filter(
    Post.created_at > datetime(2024, 1, 1),
    Post.title.contains('Python')
).all()
```

### OR Conditions

```python
from sqlalchemy import or_

# OR conditions
users = User.query.filter(
    or_(User.name == "John", User.email.contains("@gmail.com"))
).all()
```

### NOT Conditions

```python
from sqlalchemy import not_

# NOT conditions
users = User.query.filter(not_(User.age < 18)).all()
```

## Searching 🔎

### Simple Search

```python
@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # Search in post titles and content
    posts = Post.query.filter(
        or_(
            Post.title.contains(query),
            Post.content.contains(query)
        )
    ).all()
    
    return f"Found {len(posts)} posts matching '{query}'"
```

### Case-Insensitive Search

```python
from sqlalchemy import func

# Case-insensitive search
posts = Post.query.filter(
    func.lower(Post.title).contains(query.lower())
).all()
```

## Database Indexes ⚡

### What are Indexes?

Indexes make searches faster (like an index in a book).

### Adding Indexes

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Indexed!
    name = db.Column(db.String(100), index=True)  # Indexed!
```

**Indexes make queries faster but use more storage space.**

## Transactions 🔄

### What are Transactions?

A transaction is a group of operations that must all succeed or all fail.

### Example: Transfer Money

```python
try:
    # Start transaction
    user1 = User.query.get(1)
    user2 = User.query.get(2)
    
    # Transfer points
    user1.points -= 100
    user2.points += 100
    
    # Save both or neither
    db.session.commit()
    return "Transfer successful!"
except:
    # If anything fails, undo everything
    db.session.rollback()
    return "Transfer failed!"
```

## Bulk Operations 📦

### Bulk Insert

```python
# Add many users at once
users = [
    User(name="User1", email="user1@email.com"),
    User(name="User2", email="user2@email.com"),
    User(name="User3", email="user3@email.com"),
]

db.session.bulk_save_objects(users)
db.session.commit()
```

### Bulk Update

```python
# Update all users at once
User.query.filter(User.age < 18).update({User.age: 18})
db.session.commit()
```

## Raw SQL Queries (When Needed) 🔤

Sometimes you need raw SQL:

```python
# Execute raw SQL
result = db.session.execute("SELECT * FROM users WHERE age > 25")
users = result.fetchall()

# With parameters (safer)
result = db.session.execute(
    "SELECT * FROM users WHERE age > :age",
    {"age": 25}
)
users = result.fetchall()
```

**Use ORM when possible, raw SQL only when necessary!**

## Database Optimization Tips ⚡

### 1. Use Indexes for Frequently Searched Columns

```python
email = db.Column(db.String(100), index=True)  # Faster email searches
```

### 2. Limit Results

```python
# Don't load all records
posts = Post.query.limit(10).all()  # Only 10 posts
```

### 3. Use Eager Loading (Avoid N+1 Problem)

```python
from sqlalchemy.orm import joinedload

# Load posts with authors in one query
posts = Post.query.options(joinedload(Post.author)).all()
```

### 4. Select Only Needed Columns

```python
# Only get names, not all columns
names = db.session.query(User.name).all()
```

## Complete Advanced Example 🎯

```python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "blog.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

# Paginated posts
@app.route('/posts')
def show_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    
    result = [f"<h2>Posts (Page {page} of {posts.pages})</h2>"]
    for post in posts.items:
        result.append(f"<h3>{post.title}</h3>")
        result.append(f"<p>By: {post.author.name}</p>")
        result.append(f"<p>{post.content[:100]}...</p>")
        result.append("<hr>")
    
    # Pagination links
    nav = []
    if posts.has_prev:
        nav.append(f'<a href="/posts?page={posts.prev_num}">Previous</a>')
    if posts.has_next:
        nav.append(f'<a href="/posts?page={posts.next_num}">Next</a>')
    result.append(' | '.join(nav))
    
    return '<br>'.join(result)

# Search
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return "Please provide a search query (?q=your+search)"
    
    posts = Post.query.filter(
        or_(
            Post.title.contains(query),
            Post.content.contains(query)
        )
    ).all()
    
    result = [f"<h2>Search Results for '{query}'</h2>"]
    result.append(f"<p>Found {len(posts)} posts</p>")
    for post in posts:
        result.append(f"<h3>{post.title}</h3>")
        result.append(f"<p>By: {post.author.name}</p>")
    
    return '<br>'.join(result)

# Statistics
@app.route('/stats')
def stats():
    total_users = User.query.count()
    total_posts = Post.query.count()
    avg_posts = db.session.query(func.avg(
        db.session.query(func.count(Post.id))
        .filter(Post.user_id == User.id)
        .scalar_subquery()
    )).scalar() or 0
    
    result = []
    result.append("<h2>Blog Statistics</h2>")
    result.append(f"<p>Total Users: {total_users}</p>")
    result.append(f"<p>Total Posts: {total_posts}</p>")
    result.append(f"<p>Average Posts per User: {avg_posts:.2f}</p>")
    
    return '<br>'.join(result)

if __name__ == '__main__':
    app.run(debug=True)
```

## Common Mistakes 🔧

### Mistake 1: Loading Too Much Data
```python
# ❌ Loads all posts (could be thousands!)
posts = Post.query.all()

# ✅ Use pagination
posts = Post.query.paginate(page=1, per_page=10)
```

### Mistake 2: N+1 Query Problem
```python
# ❌ Makes many database queries
posts = Post.query.all()
for post in posts:
    print(post.author.name)  # One query per post!

# ✅ Use eager loading
posts = Post.query.options(joinedload(Post.author)).all()
```

### Mistake 3: Not Using Indexes
```python
# ❌ No index - slow searches
email = db.Column(db.String(100))

# ✅ With index - fast searches
email = db.Column(db.String(100), index=True)
```

## What You Learned! 📚

✅ How to paginate results  
✅ Complex queries with joins  
✅ Aggregations (count, sum, avg)  
✅ Database indexes  
✅ Transactions  
✅ Bulk operations  
✅ Optimization techniques  

## Key Concepts 💡

1. **Pagination** = Showing data in pages
2. **Aggregation** = Counting, summing, averaging
3. **Index** = Makes searches faster
4. **Transaction** = All-or-nothing operations
5. **Eager Loading** = Load related data efficiently
6. **Optimization** = Making queries faster

## What's Next? 🚀

Congratulations! You've mastered databases! You now know:
- ✅ How databases work
- ✅ How to create models
- ✅ How to query data
- ✅ How to create relationships
- ✅ Advanced operations

**Next Module**: User Authentication - Learn how to securely handle user logins and registration!

---

**Incredible! You're a database master now! 🎉**

