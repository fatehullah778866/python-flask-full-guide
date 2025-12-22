# Project 23: Social Media Feed 📱

Welcome to Project 23! This app allows users to create posts, follow users, and see a personalized feed!

## What is This Project? 🤔

**Social Media Feed** = An app for social networking!

**Think of it like:**
- **Posts** = User messages/updates
- **Follow** = Subscribe to users
- **Feed** = Personalized content

**Feed = Posts from users you follow!**

## What You'll Learn 📚

✅ Complex database relationships
✅ Follow/unfollow system
✅ Feed generation algorithms
✅ Like system
✅ User authentication
✅ Personalized content

## What This App Does 🎯

1. **User Registration/Login** - Create account and login
2. **Create Posts** - Share updates
3. **Follow Users** - Subscribe to other users
4. **Personalized Feed** - See posts from followed users
5. **Like Posts** - Like/unlike posts

**Features:**
- 👤 User profiles
- 📝 Post creation
- 👥 Follow/unfollow
- 📱 Personalized feed
- ❤️ Like system
- 🔐 User authentication

## Step-by-Step Explanation 📖

### Step 1: Database Relationships
```python
class User(db.Model):
    posts = db.relationship('Post', backref='author')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id')
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id')
```
**What this does:**
- Creates relationships between models
- Links users to posts, follows, followers
- Enables complex queries

**Simple explanation:**
- Relationships = Connections
- Links = Connect tables!

### Step 2: Feed Generation
```python
followed_ids = [follow.followed_id for follow in current_user.following]
posts = Post.query.filter(Post.author_id.in_(followed_ids)).all()
```
**What this does:**
- Gets IDs of followed users
- Filters posts by followed users
- Creates personalized feed

**Simple explanation:**
- Followed = Users you follow
- Filter = Get their posts!

### Step 3: Like System
```python
existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
if existing_like:
    db.session.delete(existing_like)  # Unlike
else:
    db.session.add(Like(...))  # Like
```
**What this does:**
- Checks if already liked
- Toggles like/unlike
- Updates database

**Simple explanation:**
- Check = See if liked
- Toggle = Switch like/unlike!

## Key Concepts 🎓

### 1. Database Relationships

**What are relationships?**
- Links between tables
- Foreign keys
- One-to-many, many-to-many

**In this app:**
- User → Posts (one-to-many)
- User → Follows (many-to-many)
- User → Likes (many-to-many)

### 2. Feed Algorithm

**How it works:**
- Get followed user IDs
- Filter posts by author
- Sort by date (newest first)
- Display in feed

### 3. Follow System

**How it works:**
- Follow table links users
- follower_id → followed_id
- Unique constraint prevents duplicates

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
1. Register/Login
2. Create posts
3. Follow other users
4. See personalized feed
5. Like posts!

## Files in This Project 📁

```
23-social-media-feed/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Feed page
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   └── users.html      # Users list page
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test follow/unfollow
2. ✅ Test feed generation
3. ✅ Understand relationships
4. ✅ Move to Project 24: Task Management with Teams

---

**Ready for the next project? Try Project 24: Task Management with Teams!**

