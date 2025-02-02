#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize and optimize database
python3 optimize_ursula_db.py

# Start the API server
python3 ursula_api.py 