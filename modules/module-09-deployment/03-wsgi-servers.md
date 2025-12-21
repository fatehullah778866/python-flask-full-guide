# Lesson 9.3: WSGI Servers - Running Your App in Production! 🚀

## What is WSGI? 🤔

**WSGI** = Web Server Gateway Interface

Think of it like:
- **Your Flask App** = A chef
- **WSGI Server** = The restaurant
- **Web Server** = The waiter
- **User** = The customer

**WSGI = How your app talks to the web server!**

## Why Do We Need WSGI Servers? 🎯

### The Problem with Flask's Built-in Server:

```python
# Development server (NOT for production!)
app.run(debug=True)
```

**Problems:**
- ❌ Only one person can use it
- ❌ Very slow
- ❌ Not secure
- ❌ Crashes easily

**Development server = Only for testing!**

### The Solution: WSGI Server

**WSGI Server:**
- ✅ Handles many users
- ✅ Fast and efficient
- ✅ Secure
- ✅ Stable

**WSGI Server = Production-ready!**

## Understanding WSGI 🔌

### How WSGI Works:

```
User Request
    ↓
Web Server (Nginx/Apache)
    ↓
WSGI Server (Gunicorn/uWSGI)
    ↓
Flask Application
    ↓
Response
```

**WSGI = Bridge between web server and Flask!**

### WSGI Interface:

```python
def application(environ, start_response):
    """WSGI application"""
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    return [b'Hello World!']
```

**Flask automatically implements WSGI!**

## Gunicorn - The Popular Choice 🦄

### What is Gunicorn?

**Gunicorn** = Green Unicorn (popular WSGI server)

Think of it like:
- **Gunicorn** = Strong worker
- **Handles** = Many requests at once
- **Popular** = Everyone uses it!

**Gunicorn = Most popular WSGI server!**

### Installing Gunicorn:

```bash
pip install gunicorn
```

### Running with Gunicorn:

```bash
# Basic command
gunicorn app:app

# With options
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

**That's it! Your app is running!**

### Gunicorn Options:

- **`--workers`** = Number of worker processes
- **`--bind`** = Host and port
- **`--timeout`** = Request timeout
- **`--access-logfile`** = Access log file
- **`--error-logfile`** = Error log file

### Example Gunicorn Command:

```bash
gunicorn \
  --workers 4 \
  --bind 0.0.0.0:5000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

## Gunicorn Configuration File 📝

### Creating config.py:

**Create `gunicorn_config.py`:**
```python
# Gunicorn configuration file

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "my-flask-app"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_redirect = False

# SSL (if needed)
# keyfile = None
# certfile = None
```

### Using Config File:

```bash
gunicorn -c gunicorn_config.py app:app
```

**Much easier to manage!**

## uWSGI - Another Option 🐍

### What is uWSGI?

**uWSGI** = Another WSGI server

**Pros:**
- ✅ Very fast
- ✅ Many features
- ✅ Good for large apps

**Cons:**
- ❌ More complex
- ❌ Harder to configure

**uWSGI = Powerful but complex!**

### Installing uWSGI:

```bash
pip install uwsgi
```

### Running with uWSGI:

```bash
uwsgi --http :5000 --wsgi-file app.py --callable app
```

### uWSGI Configuration File:

**Create `uwsgi.ini`:**
```ini
[uwsgi]
module = app:app
http = :5000
processes = 4
threads = 2
master = true
vacuum = true
die-on-term = true
```

**Run:**
```bash
uwsgi --ini uwsgi.ini
```

## Choosing Workers 👷

### What are Workers?

**Workers** = Processes that handle requests

Think of it like:
- **Workers** = Employees
- **More workers** = Handle more customers
- **Too many** = Waste resources

**Workers = Handle requests!**

### How Many Workers?

**Rule of thumb:**
```
Workers = (2 × CPU cores) + 1
```

**Examples:**
- 1 CPU core → 3 workers
- 2 CPU cores → 5 workers
- 4 CPU cores → 9 workers

### Worker Types:

#### 1. Sync Workers (Default)
```python
worker_class = "sync"
```
- Simple
- One request per worker
- Good for most apps

#### 2. Gevent Workers (Async)
```python
worker_class = "gevent"
```
- Handles many requests
- Good for I/O-heavy apps
- Need to install: `pip install gevent`

#### 3. Eventlet Workers (Async)
```python
worker_class = "eventlet"
```
- Similar to gevent
- Need to install: `pip install eventlet`

## Nginx as Reverse Proxy 🔄

### What is a Reverse Proxy?

**Reverse Proxy** = Server in front of your app

Think of it like:
- **Nginx** = Receptionist
- **Gunicorn** = The actual worker
- **User** = Talks to receptionist first

**Reverse Proxy = Handles requests before your app!**

### Why Use Nginx?

- ✅ Serves static files (fast!)
- ✅ Handles SSL/HTTPS
- ✅ Load balancing
- ✅ Better security

**Nginx = Professional setup!**

### Nginx Configuration:

**Create `/etc/nginx/sites-available/myapp`:**
```nginx
server {
    listen 80;
    server_name example.com;

    # Static files
    location /static {
        alias /path/to/app/static;
        expires 30d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

## Complete Production Setup 🎯

### Step 1: Install Gunicorn

```bash
pip install gunicorn
```

### Step 2: Create Gunicorn Config

**`gunicorn_config.py`:**
```python
bind = "127.0.0.1:5000"
workers = 4
timeout = 120
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
```

### Step 3: Run Gunicorn

```bash
gunicorn -c gunicorn_config.py app:app
```

### Step 4: Set Up Systemd Service (Linux)

**Create `/etc/systemd/system/myapp.service`:**
```ini
[Unit]
Description=My Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl start myapp
sudo systemctl enable myapp  # Start on boot
```

### Step 5: Configure Nginx

**As shown above!**

## Testing Your Setup 🧪

### Test Gunicorn:

```bash
# Start Gunicorn
gunicorn app:app

# Test in another terminal
curl http://localhost:5000
```

### Test Nginx:

```bash
# Test configuration
sudo nginx -t

# Reload
sudo systemctl reload nginx

# Test
curl http://localhost
```

## Monitoring and Logging 📊

### Access Logs:

**Gunicorn access logs show:**
- Who visited
- What pages
- When they visited

### Error Logs:

**Gunicorn error logs show:**
- Errors
- Warnings
- Debug info

### Viewing Logs:

```bash
# Gunicorn logs
tail -f /var/log/gunicorn/access.log
tail -f /var/log/gunicorn/error.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## Performance Tuning ⚡

### Gunicorn Tuning:

```python
# For CPU-bound apps
workers = (2 × CPU cores) + 1
worker_class = "sync"

# For I/O-bound apps
workers = 4
worker_class = "gevent"
worker_connections = 1000
```

### Nginx Tuning:

```nginx
# Increase connections
worker_connections 1024;

# Enable gzip
gzip on;
gzip_types text/plain text/css application/json;
```

## Common Issues and Solutions 🔧

### Issue 1: App Not Starting

**Problem:** Gunicorn can't find app
**Solution:** Check path and app name
```bash
gunicorn app:app  # app.py, app variable
```

### Issue 2: Too Many Workers

**Problem:** Server runs out of memory
**Solution:** Reduce workers
```python
workers = 2  # Instead of 4
```

### Issue 3: Timeout Errors

**Problem:** Requests take too long
**Solution:** Increase timeout
```python
timeout = 300  # 5 minutes
```

## What You Learned! 📚

✅ What WSGI is  
✅ Why we need WSGI servers  
✅ How WSGI works  
✅ Gunicorn setup and configuration  
✅ uWSGI basics  
✅ Choosing workers  
✅ Nginx as reverse proxy  
✅ Complete production setup  
✅ Monitoring and logging  
✅ Performance tuning  

## Key Concepts 💡

1. **WSGI** = Interface between web server and app
2. **Gunicorn** = Popular WSGI server
3. **Workers** = Processes handling requests
4. **Nginx** = Reverse proxy server
5. **Systemd** = Service manager
6. **Logging** = Track what happens

## What's Next? 🚀

Congratulations! You've completed Module 9! You now know:
- ✅ How to prepare for deployment
- ✅ Different deployment options
- ✅ How to use WSGI servers

**Next Module**: Advanced Topics - Learn even more about Flask!

---

**Amazing! Your apps are production-ready! 🎉**

