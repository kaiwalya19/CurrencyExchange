# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/

# Install dependencies while pinning redis to avoid issues
RUN pip install --no-cache-dir -r requirements.txt 

# Copy project files into the container
COPY . /app/

# Expose the application port
EXPOSE 8000

# Default command for the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
