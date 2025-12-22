# Project 20: Voting/Polling System 🗳️

Welcome to Project 20! This app allows users to vote on polls!

## What is This Project? 🤔

**Voting/Polling System** = An app for creating polls and voting!

**Think of it like:**
- **Poll** = Question with options
- **Vote** = User's choice
- **Results** = Vote counts and percentages

**Voting = Making choices and seeing results!**

## What You'll Learn 📚

✅ Poll creation
✅ Voting functionality
✅ Vote counting
✅ Duplicate vote prevention
✅ Results display
✅ Database relationships
✅ IP tracking

## What This App Does 🎯

1. **Create Polls** - Users can create polls
2. **Vote on Polls** - Users can vote
3. **View Results** - See vote counts and percentages
4. **Prevent Duplicates** - One vote per user per poll

**Features:**
- 🗳️ Create polls
- ✅ Vote on polls
- 📊 View results
- 🔒 Duplicate vote prevention
- 📈 Vote percentages
- 💾 Database storage

## Step-by-Step Explanation 📖

### Step 1: Create Poll Model
```python
class Poll(db.Model):
    question = db.Column(db.String(200))
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    votes_option1 = db.Column(db.Integer, default=0)
    votes_option2 = db.Column(db.Integer, default=0)
```
**What this does:**
- Defines poll structure
- Stores question and options
- Tracks vote counts

**Simple explanation:**
- Poll = Question with options
- Votes = Count of votes!

### Step 2: Create Vote Model
```python
class Vote(db.Model):
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'))
    voter_ip = db.Column(db.String(50))
    option = db.Column(db.Integer)
```
**What this does:**
- Defines vote structure
- Links to poll
- Tracks who voted

**Simple explanation:**
- Vote = User's choice
- Links = Connects to poll!

### Step 3: Vote Processing
```python
if option == 1:
    poll.votes_option1 += 1
else:
    poll.votes_option2 += 1
```
**What this does:**
- Increments vote count
- Updates poll
- Saves to database

**Simple explanation:**
- Increment = Add one
- Update = Change count!

## Key Concepts 🎓

### 1. Database Relationships

**What are relationships?**
- Links between tables
- Foreign keys
- One-to-many

**Vote → Poll:**
- Vote has poll_id
- Links to Poll table
- Many votes per poll

### 2. Duplicate Prevention

**How to prevent:**
- Track voter IP
- Check if already voted
- Unique constraint
- One vote per IP per poll

### 3. Vote Counting

**How it works:**
- Increment vote count
- Update poll
- Calculate percentages
- Display results

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
1. View existing polls
2. Vote on polls
3. Create new polls
4. See results!

## Files in This Project 📁

```
20-voting-polling-system/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Polls list and voting
│   └── create_poll.html # Create poll form
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try creating polls
2. ✅ Test voting functionality
3. ✅ Understand duplicate prevention
4. ✅ You've completed 20 projects! 🎉

---

**Congratulations! You've completed 20 projects! 🎉**

