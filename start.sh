#!/bin/bash

# Step 1: Check if virtual environment exists and activate it
if [ ! -d "venv" ]; then
    echo "Virtual environment not found! Please create a virtual environment first."
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Step 2: Check and install missing dependencies (if necessary)
if [ ! -f "requirements.txt" ]; then
    echo "No requirements.txt found! Please create a requirements file."
    exit 1
fi

# Install dependencies if they're missing
pip install -r requirements.txt

# Step 3: Run the Flask app
echo "Starting the Flask application..."
python app.py
