# Use a Python image
FROM python:3.11.4-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (from project root)
COPY requirements_deploy.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_deploy.txt

# Copy app files
COPY app/ .

# Expose port
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]