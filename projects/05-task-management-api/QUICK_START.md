# Quick Start Guide 🚀

## Get Your API Running in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask flask-sqlalchemy
```

**That's it! All dependencies installed!**

### Step 2: Run Your API

Navigate to the project folder:
```bash
cd projects/05-task-management-api
```

Run the API:
```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

**The database (tasks.db) will be created automatically!**

### Step 3: Test Your API

Open a new terminal and test the API using curl or Python!

## Testing with curl

### 1. Get All Tasks (GET)
```bash
curl http://localhost:5000/api/tasks
```

### 2. Create a Task (POST)
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Buy groceries\", \"description\": \"Milk, bread, eggs\"}"
```

### 3. Get Single Task (GET)
```bash
curl http://localhost:5000/api/tasks/1
```

### 4. Update a Task (PUT)
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"completed\": true}"
```

### 5. Delete a Task (DELETE)
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Testing with Python

Create a file `test_api.py`:

```python
import requests

# Base URL
BASE_URL = 'http://localhost:5000/api'

# 1. Get all tasks
print("GET All Tasks:")
response = requests.get(f'{BASE_URL}/tasks')
print(response.json())
print()

# 2. Create a task
print("CREATE Task:")
response = requests.post(f'{BASE_URL}/tasks', json={
    'title': 'Learn Flask',
    'description': 'Complete Flask tutorial',
    'completed': False
})
print(response.json())
print()

# 3. Get single task
print("GET Single Task:")
response = requests.get(f'{BASE_URL}/tasks/1')
print(response.json())
print()

# 4. Update task
print("UPDATE Task:")
response = requests.put(f'{BASE_URL}/tasks/1', json={
    'completed': True
})
print(response.json())
print()

# 5. Delete task
print("DELETE Task:")
response = requests.delete(f'{BASE_URL}/tasks/1')
print(response.json())
```

Run it:
```bash
pip install requests
python test_api.py
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| GET | `/api/tasks/<id>` | Get single task |
| POST | `/api/tasks` | Create new task |
| PUT | `/api/tasks/<id>` | Update task |
| DELETE | `/api/tasks/<id>` | Delete task |
| GET | `/api/health` | Health check |

## Example JSON Request/Response

### Create Task Request:
```json
{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false
}
```

### Response:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "completed": false,
  "date_created": "2024-01-01T12:00:00"
}
```

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how everything works
2. **Test all endpoints** - Try each HTTP method
3. **Use Postman** - Visual API testing tool
4. **Build a frontend** - Create a web app that uses this API

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install flask flask-sqlalchemy` again

### "Port already in use"
**Solution:** Close other Flask apps or change port:
```python
app.run(debug=True, port=5001)
```

### "No JSON data"
**Solution:** Make sure to include `Content-Type: application/json` header in POST/PUT requests

---

**Have fun with your API! 🎉**

