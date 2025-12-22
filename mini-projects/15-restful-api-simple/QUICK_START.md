# Quick Start Guide 🚀

Get your RESTful API running in 3 steps!

## Step 1: Install Flask 📦

```bash
pip install -r requirements.txt
```

## Step 2: Run the App ▶️

```bash
python app.py
```

## Step 3: Test the API 🌐

Visit: `http://127.0.0.1:5000`

**Test with curl:**

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

**PUT update item:**
```bash
curl -X PUT http://127.0.0.1:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'
```

**DELETE item:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/items/1
```

---

**That's it! You've built a RESTful API! 🎉**

