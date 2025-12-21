# Quick Start Guide 🚀

## Get Your Tests Running in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask flask-sqlalchemy pytest pytest-flask
```

**That's it! All dependencies installed!**

### Step 2: Run Tests

Navigate to the project folder:
```bash
cd projects/07-tested-applications
```

Run all tests:
```bash
pytest
```

**You should see:**
```
tests/test_models.py::test_create_post PASSED
tests/test_routes.py::test_index_route PASSED
...
======================== X passed in Y.Ys ========================
```

### Step 3: Run the App (Optional)

Run the application:
```bash
python app.py
```

Open in browser:
```
http://localhost:5000
```

## Understanding Test Output

### All Tests Pass:
```
======================== 10 passed in 0.5s ========================
```
**✅ All tests passed! Your code works!**

### Some Tests Fail:
```
tests/test_routes.py::test_create_post FAILED
...
FAILED tests/test_routes.py::test_create_post - AssertionError
```
**❌ Some tests failed. Check the error message!**

## Running Specific Tests

### Run One Test File:
```bash
pytest tests/test_models.py
```

### Run One Specific Test:
```bash
pytest tests/test_models.py::test_create_post
```

### Run with Verbose Output:
```bash
pytest -v
```

### Run with More Details:
```bash
pytest -vv
```

## Test Files

- **test_models.py** - Tests database models
- **test_routes.py** - Tests API routes
- **test_helper_functions.py** - Tests helper functions

## What Tests Check

✅ **Models** - Can create, read, update, delete posts
✅ **Routes** - All API endpoints work
✅ **Error Handling** - Errors are handled correctly
✅ **Data Validation** - Invalid data is rejected

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn how testing works
2. **Write more tests** - Add tests for edge cases
3. **Run tests regularly** - Test after making changes
4. **Fix failing tests** - Make sure all tests pass

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytest'"
**Solution:** Run `pip install pytest pytest-flask` again

### "ImportError: cannot import name 'app'"
**Solution:** Make sure you're running tests from the project directory

### Tests fail
**Solution:** Read the error message - it tells you what's wrong!

---

**Have fun testing! 🧪**

