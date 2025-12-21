# Quick Start Guide 🚀

## Get Your Portfolio Website Running in 3 Steps!

### Step 1: Install Flask

Open your terminal and run:
```bash
pip install flask
```

**That's it! Flask is installed!**

### Step 2: Run Your Website

Navigate to the project folder:
```bash
cd projects/01-personal-portfolio
```

Run the app:
```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

**Your portfolio website is live! 🎉**

## What You'll See

- **Home Page** - Welcome message and your skills
- **About Page** - Information about you
- **Projects Page** - Your projects
- **Contact Page** - How to reach you

## Next Steps

1. **Customize** - Edit the HTML files to add your information
2. **Change Colors** - Edit `static/style.css` to change the design
3. **Add Images** - Put images in `static/images/` folder
4. **Read PROJECT_GUIDE.md** - Learn how everything works!

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install flask` again

### "Port already in use"
**Solution:** Close other Flask apps or change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Page not loading
**Solution:** Make sure you're running `python app.py` from the project folder

---

**Have fun building your portfolio! 🎨**

