# Project 24: Task Management with Teams 📋

Welcome to Project 24! This app allows users to create teams, assign tasks, and collaborate!

## What is This Project? 🤔

**Task Management with Teams** = An app for team collaboration!

**Think of it like:**
- **Teams** = Groups of users
- **Tasks** = Work items
- **Assignment** = Who does what

**Teams = Groups working together!**

## What You'll Learn 📚

✅ Many-to-many relationships
✅ Team management
✅ Task assignment
✅ Status tracking
✅ Due dates
✅ Team collaboration

## What This App Does 🎯

1. **Create Teams** - Form teams
2. **Add Members** - Add users to teams
3. **Create Tasks** - Create tasks in teams
4. **Assign Tasks** - Assign tasks to team members
5. **Update Tasks** - Change status, priority, due date
6. **Track Progress** - See task status

**Features:**
- 👥 Team creation
- 👤 Team members
- 📋 Task management
- ✅ Status tracking
- 📅 Due dates
- 🎯 Priority levels

## Step-by-Step Explanation 📖

### Step 1: Many-to-Many Relationship
```python
team_members = db.Table('team_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'))
)
```
**What this does:**
- Creates association table
- Links users to teams
- Enables many-to-many relationship

**Simple explanation:**
- Association = Connection table
- Many-to-many = Multiple connections!

### Step 2: Add Team Member
```python
team.members.append(user)
db.session.commit()
```
**What this does:**
- Adds user to team
- Updates relationship
- Saves to database

**Simple explanation:**
- Append = Add
- Commit = Save!

### Step 3: Task Assignment
```python
task = Task(
    assignee_id=user_id,
    team_id=team_id
)
```
**What this does:**
- Creates task
- Assigns to user
- Links to team

**Simple explanation:**
- Create = Make new
- Assign = Give to user!

## Key Concepts 🎓

### 1. Many-to-Many Relationships

**What is it?**
- Multiple connections
- Association table
- Users ↔ Teams

**In this app:**
- User can be in many teams
- Team can have many users
- Association table links them

### 2. Task Management

**How it works:**
- Tasks belong to teams
- Tasks assigned to users
- Status tracking
- Priority levels

### 3. Team Collaboration

**How it works:**
- Create teams
- Add members
- Create tasks
- Assign tasks
- Track progress

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
2. Create teams
3. Add team members
4. Create tasks
5. Assign tasks
6. Update task status!

## Files in This Project 📁

```
24-task-management-teams/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Dashboard
│   ├── team_detail.html # Team detail page
│   ├── create_team.html # Create team form
│   ├── login.html      # Login page
│   └── register.html   # Registration page
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test team creation
2. ✅ Test task assignment
3. ✅ Understand many-to-many relationships
4. ✅ You've completed 24 projects! 🎉

---

**Congratulations! You've completed 24 projects! 🎉**

