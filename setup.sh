#!/bin/bash

echo "Setting up Ursula Voice Implementation..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Generate SSH key if it doesn't exist
if [ ! -f ~/.ssh/ursula_github ]; then
    echo "Generating SSH key..."
    mkdir -p ~/.ssh
    ssh-keygen -t ed25519 -f ~/.ssh/ursula_github -N "" -C "ursula-api"
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/ursula_github
    echo "Your SSH public key (add to GitHub):"
    cat ~/.ssh/ursula_github.pub
fi

# Initialize database
echo "Setting up database..."
rm -f ursula.db
sqlite3 ursula.db < ursula-db-schema.sql
python3 populate_ursula_db.py

# Set up git config if not already set
if [ -z "$(git config --global user.email)" ]; then
    echo "Setting up git configuration..."
    read -p "Enter git user.email: " git_email
    read -p "Enter git user.name: " git_name
    git config --global user.email "$git_email"
    git config --global user.name "$git_name"
fi

# Start the server
echo "Starting Ursula API server..."
uvicorn ursula_api:app --host 0.0.0.0 --port 8080 --reload 