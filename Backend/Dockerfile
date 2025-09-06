FROM python:3.10.15-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . /app

# Expose FastAPI default port
EXPOSE 8000

# Use Gunicorn + Uvicorn for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--threads", "4", \
     "--timeout", "120"]
