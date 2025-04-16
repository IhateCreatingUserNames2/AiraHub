#!/bin/bash

# AIRA Hub WebUI Startup Script

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if AIRA_HUB_URL is set
if [ -z "$AIRA_HUB_URL" ]; then
    echo "Warning: AIRA_HUB_URL environment variable is not set."
    echo "Using default: https://aira-fl8f.onrender.com"
    export AIRA_HUB_URL="https://aira-fl8f.onrender.com"
fi

# Check if SECRET_KEY is set
if [ -z "$SECRET_KEY" ]; then
    echo "Warning: SECRET_KEY environment variable is not set."
    echo "Generating a random secret key..."
    export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
fi

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment 'venv' not found."
    echo "Running without virtual environment. Make sure all dependencies are installed."
fi

# Get port from environment or use default
PORT=${PORT:-5000}

echo "Starting AIRA Hub WebUI on port $PORT..."
echo "Hub URL: $AIRA_HUB_URL"

# Run in development mode if DEBUG is set
if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
    echo "Running in debug mode..."
    FLASK_APP=app.py FLASK_ENV=development flask run --host=0.0.0.0 --port=$PORT
else
    # Run with gunicorn in production
    if command -v gunicorn &> /dev/null; then
        echo "Running with gunicorn..."
        gunicorn --bind 0.0.0.0:$PORT app:app
    else
        echo "Gunicorn not found. Running with Flask's development server..."
        FLASK_APP=app.py flask run --host=0.0.0.0 --port=$PORT
    fi
fi