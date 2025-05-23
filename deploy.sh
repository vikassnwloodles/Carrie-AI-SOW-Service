#!/bin/bash

# Exit immediately on any error
set -e

# Configurable variables
SERVICE_NAME="carrie_ai_sow.service"

echo "🚀 Starting deployment..."

# Pull latest code from GitHub
echo "📥 Pulling latest changes from Git..."
git reset --hard HEAD  # Optional: discard local changes
git pull origin main   # Replace 'main' with your branch name if different

# Install dependencies
echo "📦 Installing dependencies..."
chmod +x install.sh
./install.sh

# Restart systemd service
echo "🔄 Restarting service: $SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

# Optional: Check status
sudo systemctl status "$SERVICE_NAME" --no-pager

echo "✅ Deployment complete!"
