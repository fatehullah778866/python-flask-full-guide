# Quick Start Guide 🚀

Get your JWT API running in 3 steps!

## Step 1: Install Dependencies 📦

```bash
pip install -r requirements.txt
```

## Step 2: Run the App ▶️

```bash
python app.py
```

## Step 3: Test the API 🧪

### Option 1: Use Test Script
```bash
python test_api.py
```

### Option 2: Use curl
```bash
# Register
curl -X POST http://127.0.0.1:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Get Resources (use access_token from login)
curl -X GET http://127.0.0.1:5000/api/resources \
  -H "Authorization: Bearer <access_token>"
```

### Option 3: View Documentation
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Register a user via API
2. Login to get access_token and refresh_token
3. Use access_token in Authorization header for protected endpoints
4. Use refresh_token to get new access_token when it expires!

---

**That's it! You've built a JWT-authenticated API! 🎉**

