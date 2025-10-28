# Use a lightweight, secure Python base image
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Copy dependencies list first (this allows for better Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/

# The command that will be run when the container starts
CMD ["python", "src/main.py"]
