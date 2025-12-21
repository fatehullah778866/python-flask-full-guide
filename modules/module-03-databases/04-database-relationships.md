# Lesson 3.4: Database Relationships - Connecting Tables! 🔗

## What are Relationships? 🤔

**Relationships** connect tables together, like connecting puzzle pieces!

### Real-World Example:

Think of a blog:
- **Users** write **Posts**
- **Posts** have **Comments**
- **Users** write **Comments**

These are **relationships** - tables connected to each other!

## Types of Relationships 🔗

### 1. One-to-Many (Most Common)

**One user** can have **many posts**

```
User (One)  ──→  Posts (Many)
  John      ──→  Post 1
            ──→  Post 2
            ──→  Post 3
```

**Example**: One author writes many blog posts

### 2. Many-to-Many

**Many users** can like **many posts**

```
Users  ←──→  Posts
John   ←──→  Post 1
Sarah  ←──→  Post 1
John   ←──→  Post 2
```

**Example**: Many users can like many posts

### 3. One-to-One (Less Common)

**One user** has **one profile**

```
User  ──→  Profile
John  ──→  John's Profile
```

**Example**: One user has one profile picture

## One-to-Many Relationship 👥→📝

### Example: Users and Posts

One user can write many posts.

### Step 1: Create Models

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship: One user has many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key: Links to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'
```

### Breaking It Down:

**In User model:**
- **`posts = db.relationship(...)`** = Creates relationship to Post
- **`backref='author'`** = Creates `post.author` to get the user
- **`lazy=True`** = Loads posts when accessed

**In Post model:**
- **`user_id = db.Column(...)`** = Foreign key (link to User)
- **`db.ForeignKey('user.id')`** = Points to User's id column

### Step 2: Using the Relationship

```python
# Create a user
user = User(name="John", email="john@email.com")
db.session.add(user)
db.session.commit()

# Create posts for this user
post1 = Post(title="My First Post", content="Hello world!", user_id=user.id)
post2 = Post(title="My Second Post", content="Another post!", user_id=user.id)

db.session.add_all([post1, post2])
db.session.commit()

# Get all posts by a user
user = User.query.get(1)
print(f"{user.name} has {len(user.posts)} posts:")
for post in user.posts:
    print(f"  - {post.title}")

# Get the author of a post
post = Post.query.get(1)
print(f"Post '{post.title}' was written by {post.author.name}")
```

## Understanding Foreign Keys 🔑

### What is a Foreign Key?

A **foreign key** is a column that points to another table's primary key.

```
User Table:
  id (Primary Key)
  name
  email

Post Table:
  id (Primary Key)
  title
  content
  user_id (Foreign Key → points to User.id)
```

**`user_id` in Post table points to `id` in User table!**

## Many-to-Many Relationship 👥↔️📝

### Example: Users and Liked Posts

Many users can like many posts.

### Step 1: Create Association Table

```python
# Association table (connects Users and Posts)
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)
```

### Step 2: Create Models with Relationship

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Many-to-many relationship
    liked_posts = db.relationship('Post', secondary=likes, lazy='subquery',
                                backref=db.backref('liked_by', lazy=True))
    
    def __repr__(self):
        return f'<User {self.name}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'
```

### Step 3: Using Many-to-Many

```python
# Create users
user1 = User(name="John", email="john@email.com")
user2 = User(name="Sarah", email="sarah@email.com")
db.session.add_all([user1, user2])
db.session.commit()

# Create posts
post1 = Post(title="Post 1", content="Content 1")
post2 = Post(title="Post 2", content="Content 2")
db.session.add_all([post1, post2])
db.session.commit()

# User1 likes both posts
user1.liked_posts.append(post1)
user1.liked_posts.append(post2)

# User2 likes post1
user2.liked_posts.append(post1)

db.session.commit()

# Get all posts liked by user1
print(f"{user1.name} likes:")
for post in user1.liked_posts:
    print(f"  - {post.title}")

# Get all users who liked post1
print(f"Post '{post1.title}' is liked by:")
for user in post1.liked_by:
    print(f"  - {user.name}")
```

## Complete Blog Example 🎯

Let's build a complete blog with Users, Posts, and Comments:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "blog.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # One-to-many: One user has many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # One-to-many: One user has many comments
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # One-to-many: One post has many comments
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to Post
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.text[:50]}>'

# Create tables
with app.app_context():
    db.create_all()

# Route to create sample data
@app.route('/setup')
def setup():
    # Create users
    user1 = User(name="John", email="john@email.com")
    user2 = User(name="Sarah", email="sarah@email.com")
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Create posts
    post1 = Post(title="My First Post", content="This is my first blog post!", user_id=user1.id)
    post2 = Post(title="Python Tips", content="Here are some Python tips...", user_id=user2.id)
    db.session.add_all([post1, post2])
    db.session.commit()
    
    # Create comments
    comment1 = Comment(text="Great post!", post_id=post1.id, user_id=user2.id)
    comment2 = Comment(text="Thanks!", post_id=post1.id, user_id=user1.id)
    db.session.add_all([comment1, comment2])
    db.session.commit()
    
    return "Sample data created!"

# Route to show all posts with authors
@app.route('/posts')
def show_posts():
    posts = Post.query.all()
    result = []
    for post in posts:
        result.append(f"<h3>{post.title}</h3>")
        result.append(f"<p>By: {post.author.name}</p>")
        result.append(f"<p>{post.content}</p>")
        result.append(f"<p>Comments: {len(post.comments)}</p>")
        result.append("<hr>")
    return '<br>'.join(result)

# Route to show post with comments
@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return "Post not found!"
    
    result = []
    result.append(f"<h2>{post.title}</h2>")
    result.append(f"<p>By: {post.author.name}</p>")
    result.append(f"<p>{post.content}</p>")
    result.append("<h3>Comments:</h3>")
    
    for comment in post.comments:
        result.append(f"<p><strong>{comment.commenter.name}:</strong> {comment.text}</p>")
    
    return '<br>'.join(result)

if __name__ == '__main__':
    app.run(debug=True)
```

## Understanding Cascade Delete 🗑️

When you delete a parent, what happens to children?

```python
# Cascade delete: When post is deleted, delete all comments
comments = db.relationship('Comment', backref='post', lazy=True, 
                          cascade='all, delete-orphan')
```

**Options:**
- **`cascade='all'`** = Delete children when parent is deleted
- **`cascade='all, delete-orphan'`** = Delete children and orphans
- **No cascade** = Children remain (orphaned)

## Querying with Relationships 🔍

### Get Posts by User

```python
user = User.query.get(1)
posts = user.posts  # Gets all posts by this user
```

### Get Comments on a Post

```python
post = Post.query.get(1)
comments = post.comments  # Gets all comments on this post
```

### Get Author of a Post

```python
post = Post.query.get(1)
author = post.author  # Gets the user who wrote this post
```

### Complex Queries

```python
# Get all posts with their authors
posts = Post.query.join(User).all()
for post in posts:
    print(f"{post.title} by {post.author.name}")

# Get all comments with their authors and posts
comments = Comment.query.join(User).join(Post).all()
for comment in comments:
    print(f"{comment.commenter.name} commented on '{comment.post.title}': {comment.text}")
```

## Practice Exercise 🏋️

Create a library system:

1. **Book Model** (title, author_name)
2. **Member Model** (name, email)
3. **Borrowing Model** (book_id, member_id, borrowed_date)

**Relationships:**
- One book can be borrowed by many members (over time)
- One member can borrow many books

**Try it yourself!**

## Common Mistakes 🔧

### Mistake 1: Wrong Foreign Key Name
```python
# ❌ Wrong table name
user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# ✅ Correct (use lowercase class name)
user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

### Mistake 2: Forgetting to Add to Relationship
```python
# ❌ Just setting foreign key
post.user_id = user.id

# ✅ Also add to relationship
user.posts.append(post)
```

### Mistake 3: Not Committing
```python
user.posts.append(post)
# ❌ Missing commit!
db.session.commit()  # ✅ Must commit!
```

## What You Learned! 📚

✅ What relationships are and why we need them  
✅ One-to-many relationships  
✅ Many-to-many relationships  
✅ Foreign keys  
✅ How to use relationships in queries  
✅ Cascade delete  

## Key Concepts 💡

1. **Relationship** = Connection between tables
2. **Foreign Key** = Column that points to another table
3. **One-to-Many** = One parent, many children
4. **Many-to-Many** = Many-to-many connection (needs association table)
5. **backref** = Creates reverse relationship
6. **Cascade** = What happens when parent is deleted

## What's Next? 🚀

You now know how to connect tables! Next, we'll learn about **advanced database operations** - pagination, complex queries, and optimization!

---

**Fantastic! You can now build complex database structures! 🎉**

