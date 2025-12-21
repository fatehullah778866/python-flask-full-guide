# Lesson 7.4: Test Coverage - Making Sure You Test Everything! 📊

## What is Test Coverage? 🎯

**Test Coverage** = How much of your code is tested

Think of it like:
- **Code** = A book
- **Tests** = Reading the book
- **Coverage** = How much of the book you've read

**Coverage = Percentage of code that's tested!**

## Why Measure Coverage? ✨

### The Problem:

- ❌ You write tests
- ❌ But did you test everything?
- ❌ Some code might not be tested
- ❌ Bugs hide in untested code!

### The Solution: Coverage

- ✅ Shows what's tested
- ✅ Shows what's NOT tested
- ✅ Helps you write better tests
- ✅ Gives confidence

**Coverage = Knowing what you've tested!**

## Installing Coverage Tools 📦

```bash
pip install pytest-cov coverage
```

**That's it!** Coverage tools are now installed.

## Measuring Coverage 📊

### Run Tests with Coverage:

```bash
pytest --cov=app --cov-report=html
```

**This shows:**
- How much code is tested
- Which lines are tested
- Which lines are NOT tested

### Coverage Report:

```
Name           Stmts   Miss  Cover
-----------------------------------
app.py            50     10    80%
routes.py         30      5    83%
models.py         20      0   100%
-----------------------------------
TOTAL            100     15    85%
```

**This means:**
- **85% coverage** = 85% of code is tested
- **15 lines** = Not tested (might have bugs!)

## Understanding Coverage Percentages 📈

### 0% Coverage:

```
❌ No tests at all!
❌ Don't know if code works
❌ Very risky!
```

### 50% Coverage:

```
⚠️ Half the code is tested
⚠️ Half might have bugs
⚠️ Not great, but better than nothing
```

### 80% Coverage:

```
✅ Most code is tested
✅ Good coverage
✅ Most bugs will be caught
```

### 100% Coverage:

```
🎉 All code is tested!
🎉 Very confident
🎉 But hard to achieve
```

**Aim for 80%+ coverage!**

## Viewing Coverage Report 📄

### HTML Report:

```bash
pytest --cov=app --cov-report=html
```

**This creates:**
- `htmlcov/index.html` - Coverage report
- Open in browser to see detailed report
- Shows which lines are covered (green) and not covered (red)

### Terminal Report:

```bash
pytest --cov=app --cov-report=term
```

**Shows coverage in terminal:**
```
app.py                   50     10    80%
routes.py                30      5    83%
```

## Coverage Example 🎯

### Code to Test:

```python
# calculator.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
```

### Tests (Incomplete):

```python
# test_calculator.py
from calculator import add, divide

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5
```

### Coverage Report:

```
Name              Stmts   Miss  Cover
-----------------------------------
calculator.py        10      4    60%
-----------------------------------
```

**What's missing?**
- ❌ `subtract()` - Not tested
- ❌ `multiply()` - Not tested
- ❌ `divide()` error case - Not tested

### Complete Tests:

```python
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    try:
        divide(10, 0)
        assert False
    except ValueError:
        assert True
```

**Now coverage is 100%!**

## Coverage Configuration ⚙️

### Create .coveragerc File:

```ini
[run]
source = .
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

**This:**
- Tells coverage what to measure
- Excludes test files
- Excludes virtual environment

## Writing Effective Tests ✍️

### Test All Paths:

```python
def process_age(age):
    if age < 0:
        return "Invalid"
    elif age < 18:
        return "Minor"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"

# Good tests - cover all paths
def test_negative_age():
    assert process_age(-1) == "Invalid"

def test_minor():
    assert process_age(10) == "Minor"

def test_adult():
    assert process_age(30) == "Adult"

def test_senior():
    assert process_age(70) == "Senior"
```

### Test Edge Cases:

```python
def test_edge_cases():
    assert process_age(0) == "Minor"      # Edge case
    assert process_age(17) == "Minor"     # Edge case
    assert process_age(18) == "Adult"     # Edge case
    assert process_age(64) == "Adult"      # Edge case
    assert process_age(65) == "Senior"     # Edge case
```

## Coverage Best Practices ✨

### 1. Aim for 80%+ Coverage

```
✅ 80-90% = Good coverage
✅ 90-100% = Excellent coverage
⚠️ Below 80% = Need more tests
```

### 2. Focus on Important Code

```
✅ Test business logic
✅ Test user-facing features
✅ Test error handling
⚠️ Don't worry about simple getters/setters
```

### 3. Test Edge Cases

```python
# ✅ Test edge cases
def test_empty_list():
    assert process_list([]) == []

def test_single_item():
    assert process_list([1]) == [1]

def test_large_list():
    assert process_list([1] * 1000) == [1] * 1000
```

### 4. Don't Obsess Over 100%

```
✅ 100% is great, but hard
✅ 80-90% is usually enough
⚠️ Some code is hard to test
⚠️ Focus on important code
```

## Continuous Integration (CI) Basics 🔄

### What is CI?

**CI** = Continuous Integration

**Automatically:**
- Run tests when you push code
- Check coverage
- Report if tests fail

### Example: GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=app
```

**This runs tests automatically!**

## Complete Coverage Example 🎯

```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')
    
    if operation == 'add':
        return jsonify({"result": a + b})
    elif operation == 'subtract':
        return jsonify({"result": a - b})
    elif operation == 'multiply':
        return jsonify({"result": a * b})
    elif operation == 'divide':
        if b == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        return jsonify({"result": a / b})
    else:
        return jsonify({"error": "Invalid operation"}), 400

# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_add(client):
    response = client.post('/api/calculate',
                          json={'operation': 'add', 'a': 5, 'b': 3})
    assert response.status_code == 200
    assert response.get_json()['result'] == 8

def test_subtract(client):
    response = client.post('/api/calculate',
                          json={'operation': 'subtract', 'a': 5, 'b': 3})
    assert response.status_code == 200
    assert response.get_json()['result'] == 2

def test_multiply(client):
    response = client.post('/api/calculate',
                          json={'operation': 'multiply', 'a': 5, 'b': 3})
    assert response.status_code == 200
    assert response.get_json()['result'] == 15

def test_divide(client):
    response = client.post('/api/calculate',
                          json={'operation': 'divide', 'a': 10, 'b': 2})
    assert response.status_code == 200
    assert response.get_json()['result'] == 5

def test_divide_by_zero(client):
    response = client.post('/api/calculate',
                          json={'operation': 'divide', 'a': 10, 'b': 0})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_invalid_operation(client):
    response = client.post('/api/calculate',
                          json={'operation': 'invalid', 'a': 5, 'b': 3})
    assert response.status_code == 400
    assert 'error' in response.get_json()
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=html
```

## What You Learned! 📚

✅ What test coverage is  
✅ Why measure coverage  
✅ How to install coverage tools  
✅ How to measure coverage  
✅ How to view coverage reports  
✅ How to write effective tests  
✅ Coverage best practices  
✅ CI basics  

## Key Concepts 💡

1. **Coverage** = How much code is tested
2. **Coverage Percentage** = % of code tested
3. **Coverage Report** = Shows what's tested/not tested
4. **80%+ Coverage** = Good coverage goal
5. **CI** = Automatic testing
6. **Edge Cases** = Special situations to test

## What's Next? 🚀

Congratulations! You've completed Module 7! You now know:
- ✅ Why testing is important
- ✅ How to write unit tests
- ✅ How to write integration tests
- ✅ How to measure coverage

**Next Module**: Security - Learn how to protect your Flask applications!

---

**Amazing! You're now a testing expert! 🎉**

