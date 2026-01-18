# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (none strictly required for current deps, but good practice)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables will be passed via file
# Tokens and storage will be mounted via volume

# Command to run the application using unbuffered output (so logs appear immediately)
CMD ["python", "-u", "main.py"]
