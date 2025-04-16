# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copy project files
COPY . /app/

# Expose port
EXPOSE 5000

# Set default environment variables
ENV AIRA_HUB_URL=https://aira-fl8f.onrender.com \
    PORT=5000

# Create a non-root user and switch to it
RUN useradd -m airauser && \
    chown -R airauser:airauser /app
USER airauser

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT app:app