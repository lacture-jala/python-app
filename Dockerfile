# Use a specific, stable Python base image with a known tag (avoid 'latest')
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app  

# Upgrade pip, install system dependencies, and update OS packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt . 

# Upgrade pip inside container and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
