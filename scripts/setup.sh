#!/bin/bash
echo "Setting up BRO-AI development environment..."

cd "$(dirname "$0")/.."

# Check Python version
python3 --version 2>&1 || { echo "Python 3.11+ required"; exit 1; }

# Create virtual environment
cd core
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../apps/desktop
npm install

# Create data directory
mkdir -p ../../data

echo "Setup complete! Run ./scripts/dev.sh to start development."
