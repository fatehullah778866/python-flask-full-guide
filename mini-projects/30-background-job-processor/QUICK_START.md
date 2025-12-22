# Quick Start Guide 🚀

Get your Background Job Processor running in 5 steps!

## Step 1: Install Dependencies 📦

```bash
pip install -r requirements.txt
```

## Step 2: Install Redis 🔴

**Mac:**
```bash
brew install redis
```

**Windows:**
Download from https://redis.io/download

**Linux:**
```bash
sudo apt-get install redis-server
```

## Step 3: Start Redis ▶️

```bash
redis-server
```

**Keep this terminal open!**

## Step 4: Start Celery Worker ⚙️

**Open a new terminal:**
```bash
cd path/to/project
celery -A app.celery worker --loglevel=info
```

**Keep this terminal open!**

## Step 5: Run Flask App 🚀

**Open another new terminal:**
```bash
cd path/to/project
python app.py
```

## Step 6: Open in Browser 🌐

Visit: `http://127.0.0.1:5000`

**How to use:**
1. Submit a long-running task (e.g., 10 seconds)
2. Get task ID immediately
3. Check task status page
4. See progress in real-time!
5. App stays responsive while task runs!

---

**That's it! You've built a background job processor! 🎉**

