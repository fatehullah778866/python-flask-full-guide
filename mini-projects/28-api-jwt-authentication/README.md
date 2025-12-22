# Project 28: API with Authentication (JWT) 🔐

Welcome to Project 28! This app demonstrates JWT authentication for RESTful APIs!

## What is This Project? 🤔

**API with JWT Authentication** = A secure RESTful API using JWT tokens!

**Think of it like:**
- **API** = Web service
- **JWT** = Security token
- **Authentication** = Verify identity

**JWT = Secure way to authenticate API requests!**

## What You'll Learn 📚

✅ JWT (JSON Web Token)
✅ API authentication
✅ Access tokens
✅ Refresh tokens
✅ Protected endpoints
✅ Token expiration

## What This App Does 🎯

1. **User Registration** - Register via API
2. **User Login** - Login and get JWT tokens
3. **Token Refresh** - Get new access tokens
4. **Protected Endpoints** - Access resources with tokens
5. **Resource Management** - Create and view resources

**Features:**
- 🔐 JWT authentication
- 🎫 Access tokens (1 hour)
- 🔄 Refresh tokens (30 days)
- 🛡️ Protected endpoints
- 📚 API documentation
- 🧪 Test script included

## Step-by-Step Explanation 📖

### Step 1: JWT Setup
```python
from flask_jwt_extended import JWTManager, create_access_token
jwt = JWTManager(app)
```
**What this does:**
- Initializes JWT manager
- Enables token creation
- Sets up authentication

**Simple explanation:**
- JWT = Token system
- Manager = Handles tokens!

### Step 2: Create Tokens
```python
access_token = create_access_token(identity=user.id)
refresh_token = create_refresh_token(identity=user.id)
```
**What this does:**
- Creates access token
- Creates refresh token
- Encodes user ID

**Simple explanation:**
- Create = Make token
- Identity = User ID!

### Step 3: Protect Endpoints
```python
@jwt_required()
def get_resources():
    user_id = get_jwt_identity()
```
**What this does:**
- Requires valid token
- Gets user from token
- Protects endpoint

**Simple explanation:**
- Protect = Require token
- Identity = Get user!

## Key Concepts 🎓

### 1. JWT (JSON Web Token)

**What is JWT?**
- Secure token format
- Contains user information
- Signed with secret key

**Structure:**
- Header = Token type
- Payload = User data
- Signature = Verification

### 2. Access Tokens

**What are access tokens?**
- Short-lived tokens
- Used for API requests
- Expire quickly (1 hour)

**How it works:**
- Client sends token in header
- Server verifies token
- Grants access if valid

### 3. Refresh Tokens

**What are refresh tokens?**
- Long-lived tokens
- Used to get new access tokens
- Expire slowly (30 days)

**How it works:**
- Client sends refresh token
- Server creates new access token
- Client uses new token

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Test the API
```bash
python test_api.py
```

### Step 4: View Documentation
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Register a user via API
2. Login to get tokens
3. Use access token for protected endpoints
4. Refresh token when access token expires!

## Files in This Project 📁

```
28-api-jwt-authentication/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── test_api.py         # Test script
├── templates/           # HTML templates
│   └── api_docs.html   # API documentation
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test API endpoints
2. ✅ Understand JWT tokens
3. ✅ Learn about token expiration
4. ✅ You've completed 28 projects! 🎉

---

**Congratulations! You've completed 28 projects! 🎉**

