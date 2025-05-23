#!/bin/bash

# Exit on any error
set -e

# Install Python dependencies
if [ -f "requirements.txt" ]; then
  echo "📄 Installing Python packages from requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "❌ requirements.txt not found!"
  exit 1
fi

# Install pandoc
echo "📦 Installing pandoc..."
if command -v apt-get &> /dev/null; then
  sudo apt-get update
  sudo apt-get install -y pandoc
else
  echo "❌ Unsupported OS. Please install pandoc manually: https://pandoc.org/installing.html"
  exit 1
fi

echo "✅ Installation complete!"
