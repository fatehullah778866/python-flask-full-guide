# Deploying to Heroku 🟣

## What is Heroku?

**Heroku** = Popular platform for deploying web apps

Think of it like:
- **Heroku** = A hotel for your website
- **Very popular** = Many people use it
- **Easy to use** = Simple deployment
- **Free tier** = Can try for free!

**Heroku = Easy deployment platform!**

## Step-by-Step Guide

### Step 1: Install Heroku CLI

1. Go to: https://devcenter.heroku.com/articles/heroku-cli
2. Download and install Heroku CLI
3. Open terminal and verify:
   ```bash
   heroku --version
   ```

### Step 2: Login to Heroku

```bash
heroku login
```

This opens a browser - login with your Heroku account (create one if needed!)

### Step 3: Create Heroku App

```bash
heroku create my-flask-app
```

**This creates an app on Heroku!**

### Step 4: Create Procfile

**Create a file called `Procfile` (no extension!):**
```
web: gunicorn app:app
```

**Procfile = Tells Heroku how to run your app!**

### Step 5: Set Environment Variables

```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
```

**Environment Variables = Secret settings!**

### Step 6: Deploy

```bash
git add .
git commit -m "Ready for deployment"
git push heroku main
```

**That's it! Your app is live!**

### Step 7: Open Your App

```bash
heroku open
```

**Or visit the URL shown in terminal!**

## Your App URL

After deployment, you'll get a URL like:
```
https://my-flask-app.herokuapp.com
```

**Share this URL with everyone!**

## Updating Your App

When you make changes:

```bash
git add .
git commit -m "Update app"
git push heroku main
```

**Heroku automatically updates!**

## View Logs

```bash
heroku logs --tail
```

**See what's happening!**

## Common Commands

```bash
# View app info
heroku info

# View environment variables
heroku config

# Open app in browser
heroku open

# View logs
heroku logs --tail

# Restart app
heroku restart
```

## Troubleshooting

### "No Procfile found"
**Solution:** Create `Procfile` with: `web: gunicorn app:app`

### "Application error"
**Solution:** Check logs: `heroku logs --tail`

### "Build failed"
**Solution:** Check `requirements.txt` is correct

---

**Heroku = Easy deployment! 🎉**

