FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and trained model
COPY app.py .
COPY train.py .
COPY model/ ./model/
COPY templates/ ./templates/
COPY tests/ ./tests/

# Expose web application port
EXPOSE 5000

# Healthcheck instruction for container orchestration & monitoring
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Launch the Flask application
CMD ["python", "app.py"]

