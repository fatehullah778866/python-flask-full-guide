# Quick Start Guide 🚀

## Get Your App Ready for Deployment in 3 Steps!

### Step 1: Install Dependencies

Open your terminal and run:
```bash
pip install flask gunicorn
```

**That's it! All dependencies installed!**

### Step 2: Test Locally

Run the app:
```bash
python app.py
```

**Or with Gunicorn (production mode):**
```bash
gunicorn app:app
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Choose Deployment Platform

Pick one:
- **Heroku** - Most popular (see `deployment-guides/heroku.md`)
- **Railway** - Modern and easy (see `deployment-guides/railway.md`)
- **Render** - Simple with free tier (see `deployment-guides/render.md`)

## Files Needed for Deployment

### 1. requirements.txt
Lists all packages your app needs

### 2. Procfile (for Heroku)
Tells Heroku how to run your app:
```
web: gunicorn app:app
```

### 3. runtime.txt (optional)
Specifies Python version:
```
python-3.11.0
```

### 4. .gitignore
Keeps secrets out of Git

## Deployment Checklist ✅

Before deploying:

- [ ] Debug mode is OFF
- [ ] Environment variables are set
- [ ] requirements.txt is up to date
- [ ] Procfile exists (for Heroku)
- [ ] .gitignore is configured
- [ ] App runs locally with Gunicorn

## Testing Locally with Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn app:app

# With options
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

**Gunicorn = Production server!**

## Environment Variables

Set these on your deployment platform:

- `SECRET_KEY` - Strong random key
- `DEBUG` - `False` for production
- `PORT` - Platform sets this automatically

## Next Steps

1. **Read PROJECT_GUIDE.md** - Learn about deployment
2. **Choose platform** - Pick Heroku, Railway, or Render
3. **Follow guide** - Use platform-specific guide
4. **Deploy!** - Put your app online!

## Troubleshooting

### "No module named 'gunicorn'"
**Solution:** Run `pip install gunicorn`

### "Procfile not found" (Heroku)
**Solution:** Create `Procfile` with: `web: gunicorn app:app`

### "Application error" (after deployment)
**Solution:** Check logs on your platform

---

**Ready to deploy? Choose a platform and follow its guide! 🚀**

