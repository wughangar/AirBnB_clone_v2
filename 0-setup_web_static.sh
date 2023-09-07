#!/usr/bin/env bash
# Bash script that sets up webservers for deployment of web_static

# Check if nginx is installed else install
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
    sudo service nginx start
fi

# Create the necessary folders and files if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<!DOCTYPE html>
<html>
  <head>
   <title>Test page for nginx</title>
  </head>
  <body>
   <h1>My Cat's name is Loki.</h1>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link and delete it if it exists
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update nginx configurations using an alias
echo "server {
    listen 80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

}" | sudo tee /etc/nginx/sites-available/default

# Test nginx configurations
sudo nginx -t

# Restart nginx to apply changes
sudo service nginx restart

# Exit the script successfully
exit 0
