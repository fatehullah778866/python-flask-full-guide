# Gunicorn Configuration File
# Use with: gunicorn -c gunicorn_config.py app:app

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
# Formula: (2 × CPU cores) + 1
workers = 4
worker_class = "sync"  # Use "gevent" for async
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Process naming
proc_name = "flask-app"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_redirect = False

# SSL (uncomment if using SSL)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Preload app (faster startup)
preload_app = True

# Max requests per worker (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 50

