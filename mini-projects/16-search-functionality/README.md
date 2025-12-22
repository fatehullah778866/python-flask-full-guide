# Project 16: Search Functionality 🔍

Welcome to Project 16! This app demonstrates search functionality with filtering!

## What is This Project? 🤔

**Search Functionality** = An app that searches through data!

**Think of it like:**
- **Search** = Finding items
- **Query** = What you're looking for
- **Filter** = Narrowing down results

**Search = Finding what you need!**

## What You'll Learn 📚

✅ Search algorithms
✅ String matching
✅ Case-insensitive search
✅ Category filtering
✅ Query parameters
✅ Results display

## What This App Does 🎯

1. **Search by Query** - Search in titles and descriptions
2. **Filter by Category** - Narrow results by category
3. **Display Results** - Show matching items
4. **Case-Insensitive** - Search works regardless of case

**Features:**
- 🔍 Text search
- 📂 Category filtering
- 🔤 Case-insensitive matching
- 📊 Results display
- 🔗 URL query parameters

## Step-by-Step Explanation 📖

### Step 1: Search Function
```python
def search_items(query, category_filter=None):
    results = []
    query_lower = query.lower()
    for item in sample_data:
        if query_lower in item['title'].lower():
            results.append(item)
    return results
```
**What this does:**
- Converts query to lowercase
- Checks each item
- Adds matches to results

**Simple explanation:**
- Search = Find matches
- Lowercase = Case-insensitive!

### Step 2: Get Query Parameters
```python
query = request.args.get('q', '').strip()
category_filter = request.args.get('category', '').strip()
```
**What this does:**
- Gets search query from URL
- Gets category filter from URL
- Strips whitespace

**Simple explanation:**
- URL params = Data in URL
- GET = Read from URL!

### Step 3: Display Results
```python
return render_template('index.html', results=results, query=query)
```
**What this does:**
- Passes results to template
- Shows search form
- Displays matching items

**Simple explanation:**
- Results = Matching items
- Display = Show to user!

## Key Concepts 🎓

### 1. Search Algorithms

**What is searching?**
- Finding items that match
- String matching
- Pattern matching

**Simple Search:**
- Check if query in text
- Case-insensitive
- Partial matching

### 2. Query Parameters

**What are they?**
- Data in URL
- After ? symbol
- Key=value pairs

**Example:**
```
/?q=python&category=Programming
```
- q=python = Search query
- category=Programming = Category filter

### 3. String Matching

**in operator:**
```python
if 'python' in 'Python Programming':
    # Match found!
```
- Checks if substring in string
- Case-sensitive by default
- Use .lower() for case-insensitive

### 4. Filtering

**What is filtering?**
- Narrowing down results
- By category
- By other criteria

**Process:**
1. Get filter value
2. Check each item
3. Include if matches

## How to Run 🚀

### Step 1: Install Flask
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
1. Enter search term
2. Optionally select category
3. Click "Search"
4. View results!

## Files in This Project 📁

```
16-search-functionality/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Search form and results
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try different search queries
2. ✅ Test category filtering
3. ✅ Understand search algorithms
4. ✅ You've completed 16 projects! 🎉

---

**Congratulations! You've completed 16 projects! 🎉**

