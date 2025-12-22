# Project 25: Notification System 🔔

Welcome to Project 25! This app allows users to receive and manage notifications!

## What is This Project? 🤔

**Notification System** = An app for managing user notifications!

**Think of it like:**
- **Notifications** = Messages/alerts
- **Read/Unread** = Status tracking
- **Real-time** = Live updates

**Notifications = Alerts and messages for users!**

## What You'll Learn 📚

✅ Notification management
✅ Read/unread tracking
✅ Notification types
✅ Real-time updates (polling)
✅ API endpoints
✅ Event tracking

## What This App Does 🎯

1. **Create Notifications** - Generate notifications
2. **View Notifications** - See all notifications
3. **Mark as Read** - Mark notifications as read
4. **Mark All as Read** - Mark all notifications as read
5. **Real-time Count** - Live notification count updates
6. **Notification Types** - Different types (info, success, warning, error)

**Features:**
- 🔔 Notification creation
- 📋 Notification list
- ✅ Mark as read/unread
- 🔄 Real-time count updates
- 🎨 Notification types
- 📊 Unread count badge

## Step-by-Step Explanation 📖

### Step 1: Notification Model
```python
class Notification(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
```
**What this does:**
- Defines notification structure
- Links to user
- Tracks read status

**Simple explanation:**
- Model = Template
- Read = Status!

### Step 2: Mark as Read
```python
notification.is_read = True
db.session.commit()
```
**What this does:**
- Updates read status
- Saves to database
- Changes notification state

**Simple explanation:**
- Update = Change
- Commit = Save!

### Step 3: Real-time Updates
```python
setInterval(updateNotificationCount, 5000);
```
**What this does:**
- Polls server every 5 seconds
- Updates notification count
- Creates real-time feel

**Simple explanation:**
- Poll = Check regularly
- Update = Refresh count!

## Key Concepts 🎓

### 1. Notification Management

**What are notifications?**
- User messages/alerts
- Read/unread status
- Different types

**Notification Structure:**
- Title
- Message
- Type
- Read status
- Timestamp

### 2. Real-time Updates

**How it works:**
- JavaScript polling
- Fetches count from API
- Updates UI automatically
- No page refresh needed

### 3. API Endpoints

**What are API endpoints?**
- URLs that return JSON
- Used by JavaScript
- Enable real-time updates

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
2. Create test notifications
3. View notifications
4. Mark as read
5. See real-time count updates!

## Files in This Project 📁

```
25-notification-system/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Dashboard
│   ├── notifications.html # Notifications list
│   ├── login.html      # Login page
│   └── register.html   # Registration page
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test notification creation
2. ✅ Test mark as read
3. ✅ Understand real-time updates
4. ✅ Move to Project 26: Analytics Dashboard

---

**Ready for the next project? Try Project 26: Analytics Dashboard!**

