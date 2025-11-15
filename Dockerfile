# Use official lightweight Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (optional but useful)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose FastAPI default port (in case you run uvicorn)
EXPOSE 8000

# Default command (can be overridden in docker-compose or Jenkins)
CMD ["python", "app/main.py"]
