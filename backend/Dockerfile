# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (เฉพาะที่จำเป็นสำหรับ PyMuPDF)
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]