# Project 15: RESTful API (Simple) 🚀

Welcome to Project 15! This app creates a simple RESTful API for managing items!

## What is This Project? 🤔

**RESTful API** = An API that follows REST principles!

**Think of it like:**
- **API** = Interface for applications to communicate
- **REST** = Architectural style for APIs
- **Endpoints** = URLs that perform actions

**RESTful = Following REST principles!**

## What You'll Learn 📚

✅ REST principles
✅ HTTP methods (GET, POST, PUT, DELETE)
✅ JSON responses
✅ API endpoints
✅ Request handling
✅ Status codes

## What This App Does 🎯

1. **GET All Items** - Retrieve all items
2. **GET Single Item** - Retrieve one item by ID
3. **POST Create Item** - Create new item
4. **PUT Update Item** - Update existing item
5. **DELETE Item** - Delete item

**Features:**
- 🔍 GET requests (read data)
- ➕ POST requests (create data)
- ✏️ PUT requests (update data)
- 🗑️ DELETE requests (delete data)
- 📊 JSON responses
- ✅ HTTP status codes

## Step-by-Step Explanation 📖

### Step 1: GET All Items
```python
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items, 'count': len(items)})
```
**What this does:**
- Returns all items as JSON
- Includes count of items
- GET method for reading

**Simple explanation:**
- GET = Read data
- JSON = Data format!

### Step 2: POST Create Item
```python
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {'id': get_next_id(), 'name': data['name']}
    items.append(new_item)
    return jsonify(new_item), 201
```
**What this does:**
- Gets JSON data from request
- Creates new item
- Returns created item with 201 status

**Simple explanation:**
- POST = Create data
- 201 = Created status!

### Step 3: PUT Update Item
```python
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item['name'] = data['name']
    return jsonify(item)
```
**What this does:**
- Finds item by ID
- Updates item fields
- Returns updated item

**Simple explanation:**
- PUT = Update data
- Modify = Change item!

### Step 4: DELETE Item
```python
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items.remove(item)
    return jsonify({'message': 'Item deleted'})
```
**What this does:**
- Finds item by ID
- Removes from list
- Returns success message

**Simple explanation:**
- DELETE = Remove data
- Remove = Delete item!

## Key Concepts 🎓

### 1. REST Principles

**What is REST?**
- Representational State Transfer
- Architectural style
- Uses HTTP methods

**REST Methods:**
- GET = Read
- POST = Create
- PUT = Update
- DELETE = Delete

### 2. JSON Responses

**What is JSON?**
- JavaScript Object Notation
- Data format
- Easy to parse

**jsonify():**
```python
jsonify({'key': 'value'})
```
- Converts Python dict to JSON
- Sets proper headers
- Returns JSON response

### 3. HTTP Status Codes

**Common Codes:**
- 200 = OK (success)
- 201 = Created (success)
- 400 = Bad Request (client error)
- 404 = Not Found (client error)
- 500 = Server Error (server error)

## How to Run 🚀

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Test the API
Use curl, Postman, or browser:

**GET all items:**
```bash
curl http://127.0.0.1:5000/api/items
```

**GET single item:**
```bash
curl http://127.0.0.1:5000/api/items/1
```

**POST create item:**
```bash
curl -X POST http://127.0.0.1:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "New Item", "description": "Description"}'
```

## Files in This Project 📁

```
15-restful-api-simple/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # API documentation
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test all API endpoints
2. ✅ Understand REST principles
3. ✅ Move to Project 16: Search Functionality

---

**Ready for the next project? Try Project 16: Search Functionality!**

