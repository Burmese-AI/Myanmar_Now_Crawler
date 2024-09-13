#!/usr/bin/env bash
# exit on error
set -o errexit

#Chrome
STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

#requirements
echo "Installing Python requirements..."
pip install -r requirements.txt


# Create Gunicorn configuration file
echo "Creating Gunicorn configuration file..."
cat << EOF > gunicorn_config.py
# Gunicorn configuration file
import multiprocessing
import os

# Bind to the port provided by Render
port = os.environ.get("PORT", 10000)
bind = f"0.0.0.0:{port}"

# Reduce the number of workers
workers = multiprocessing.cpu_count() + 1

# Use gevent worker class
worker_class = "gevent"

# Increase the timeout
timeout = 300  # 5 minutes

# Enable access logging
accesslog = "-"

# Set log level
loglevel = "info"

# Don't preload the application
preload_app = False

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Restart workers when code changes (development only)
reload = False

# Daemonize the Gunicorn process (don't use this on Render)
daemon = False

# Set a maximum request line size to prevent large requests
limit_request_line = 4094

# Set the maximum number of simultaneous clients
worker_connections = 1000

# Set a lower keepalive timeout
keepalive = 5

# Graceful timeout
graceful_timeout = 30

EOF

echo "Gunicorn configuration file created."

# Make sure the script is executable
chmod +x $HOME/project/src/render.sh

echo "Render build script completed."

