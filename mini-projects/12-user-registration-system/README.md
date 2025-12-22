# Project 12: User Registration System 👤

Welcome to Project 12! This app allows users to register and login!

## What is This Project? 🤔

**User Registration System** = An app for user accounts!

**Think of it like:**
- **Registration** = Creating an account
- **Login** = Accessing your account
- **Authentication** = Verifying who you are

**System = Complete user management!**

## What You'll Learn 📚

✅ User registration
✅ Password hashing
✅ User authentication
✅ Session management
✅ Database for users
✅ Form validation
✅ Security practices

## What This App Does 🎯

1. **Register** - Create new user account
2. **Login** - Access existing account
3. **Logout** - End session
4. **Session Management** - Track logged-in users

**Features:**
- 👤 User registration
- 🔐 Secure password hashing
- ✅ Form validation
- 🔒 Session management
- 💾 Database storage

## Step-by-Step Explanation 📖

### Step 1: Password Hashing
```python
password_hash = generate_password_hash(password)
```
**What this does:**
- Converts password to hash
- One-way encryption
- Secure storage

**Simple explanation:**
- Hash = Encrypted password
- Can't get original back
- Secure!

### Step 2: User Registration
```python
new_user = User(username=username, email=email, password_hash=password_hash)
db.session.add(new_user)
db.session.commit()
```
**What this does:**
- Creates user object
- Saves to database
- Stores hashed password

**Simple explanation:**
- Register = Create account
- Save = Store in database!

### Step 3: User Login
```python
if check_password_hash(user.password_hash, password):
    session['user_id'] = user.id
```
**What this does:**
- Verifies password
- Creates session
- Logs user in

**Simple explanation:**
- Check = Verify password
- Session = Logged in state!

## Key Concepts 🎓

### 1. Password Hashing

**What is hashing?**
- One-way encryption
- Can't reverse it
- Secure storage

**Werkzeug:**
- Flask's security tools
- generate_password_hash()
- check_password_hash()

### 2. Session Management

**What are sessions?**
- Data stored between requests
- Tracks logged-in users
- Temporary storage

**Simple explanation:**
- Session = Logged in state
- Persists until logout!

### 3. Authentication

**What is authentication?**
- Verifying user identity
- Checking credentials
- Granting access

**Process:**
1. User enters credentials
2. Check against database
3. Create session if valid

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
1. Click "Register"
2. Fill in username, email, password
3. Click "Login"
4. Access your account!

## Files in This Project 📁

```
12-user-registration-system/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   └── login.html      # Login form
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try registering multiple users
2. ✅ Test login and logout
3. ✅ Understand password security
4. ✅ You've completed 12 projects! 🎉

---

**Congratulations! You've completed 12 projects! 🎉**

