# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=0

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (minimal set for python-psycopg2 / postgres connection if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Perform database upgrades and start the application using Gunicorn
CMD ["sh", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:5000 run:app"]
