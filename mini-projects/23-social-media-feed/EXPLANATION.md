# Complete Explanation: Social Media Feed 📚

## What is a Social Media Feed? 📱

**Social Media Feed** = Personalized content from followed users

**Think of it like:**
- **Feed** = Stream of posts
- **Followed** = Users you subscribe to
- **Personalized** = Content just for you

**Why use feeds?**
- See relevant content
- Follow interests
- Stay connected
- Personalized experience

## Understanding Database Relationships 🔗

### User → Post Relationship

**What is it?**
- One user can create many posts
- One-to-many relationship
- Foreign key in Post table

**Structure:**
```python
class User(db.Model):
    posts = db.relationship('Post', backref='author')

class Post(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
```

**Simple explanation:**
- User = One
- Posts = Many
- Link = Foreign key!

### Follow Relationship

**What is it?**
- Users can follow other users
- Many-to-many relationship
- Follow table links users

**Structure:**
```python
class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))
```

**Simple explanation:**
- Follower = User who follows
- Followed = User being followed
- Link = Follow table!

### Like Relationship

**What is it?**
- Users can like posts
- Many-to-many relationship
- Like table links users and posts

**Structure:**
```python
class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
```

**Simple explanation:**
- User = One
- Posts = Many (can like many)
- Link = Like table!

## Understanding Feed Generation 📊

### Feed Algorithm

**How it works:**
1. Get followed user IDs
2. Add current user ID (see own posts)
3. Filter posts by author ID
4. Sort by date (newest first)
5. Display in feed

**Code:**
```python
followed_ids = [follow.followed_id for follow in current_user.following]
followed_ids.append(current_user.id)
posts = Post.query.filter(Post.author_id.in_(followed_ids)).order_by(Post.date_created.desc()).all()
```

**Simple explanation:**
- Get = Find followed users
- Filter = Get their posts
- Sort = Newest first!

## Understanding Follow System 👥

### Follow/Unfollow Logic

**How it works:**
1. Check if already following
2. If following, unfollow (delete)
3. If not following, follow (create)
4. Save to database

**Code:**
```python
existing_follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
if existing_follow:
    db.session.delete(existing_follow)  # Unfollow
else:
    db.session.add(Follow(...))  # Follow
```

**Simple explanation:**
- Check = See if following
- Toggle = Switch follow/unfollow!

## Understanding Like System ❤️

### Like/Unlike Logic

**How it works:**
1. Check if already liked
2. If liked, unlike (delete)
3. If not liked, like (create)
4. Save to database

**Code:**
```python
existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
if existing_like:
    db.session.delete(existing_like)  # Unlike
else:
    db.session.add(Like(...))  # Like
```

**Simple explanation:**
- Check = See if liked
- Toggle = Switch like/unlike!

## Key Concepts Summary 📝

### 1. Database Relationships
- One-to-many (User → Posts)
- Many-to-many (User ↔ User via Follow)
- Many-to-many (User ↔ Post via Like)

### 2. Feed Generation
- Get followed users
- Filter posts
- Sort by date
- Display feed

### 3. Follow System
- Follow table
- Unique constraint
- Toggle follow/unfollow

### 4. Like System
- Like table
- Unique constraint
- Toggle like/unlike

---

**Next: Try Project 24: Task Management with Teams!**

