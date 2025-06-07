#!/bin/bash

# Exit immediately on any error
set -e

# Configurable variables
SERVICE_NAME="carrie_ai_sow.service"
VENV_DIR="env"
DEPLOY_ENV_FILE=".env"

echo "🚀 Starting deployment..."

# Load environment variables if .env exists
if [ -f "$DEPLOY_ENV_FILE" ]; then
  echo "📦 Loading environment from $DEPLOY_ENV_FILE..."
  set -o allexport
  source "$DEPLOY_ENV_FILE"
  set +o allexport
fi

# Git hard reset based on environment
if [ "$DEPLOY_ENV" = "production" ]; then
  echo "🧹 Cleaning working directory for production..."
  git reset --hard HEAD
else
  echo "⚠️ Skipping hard reset in non-production environment: $DEPLOY_ENV"
fi

# Pull latest code
echo "📥 Pulling latest changes from Git..."
git pull origin main

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating virtual environment in $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "⚙️ Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Export for subprocesses (e.g., systemd services)
export VIRTUAL_ENV="$PWD/$VENV_DIR"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
echo "📦 Installing dependencies..."
chmod +x install.sh
./install.sh

# Reload systemd daemon to pick up any changes in service files
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

# Restart service
echo "🔄 Restarting systemd service: $SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

# Show service status
sudo systemctl status "$SERVICE_NAME" --no-pager

echo "✅ Deployment complete!"
