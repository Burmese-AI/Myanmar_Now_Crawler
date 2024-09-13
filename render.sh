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

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Use gevent worker class for better concurrency
worker_class = "gevent"

# Set timeout to 120 seconds
timeout = 120

# Enable access logging
accesslog = "-"

# Set log level
loglevel = "info"

# Preload the application
preload_app = True

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Restart workers when code changes (development only)
reload = False

# Daemonize the Gunicorn process (don't use this on Render)
daemon = False
EOF

echo "Gunicorn configuration file created."

# Make sure the script is executable
chmod +x $HOME/project/src/render.sh

echo "Render build script completed."

