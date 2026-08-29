FROM python:3.11-slim

# Install system dependencies: Tesseract with multiple language packs, Poppler
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tam \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    tesseract-ocr-tel \
    tesseract-ocr-ben \
    tesseract-ocr-kan \
    tesseract-ocr-mal \
    tesseract-ocr-guj \
    tesseract-ocr-pan \
    tesseract-ocr-mar \
    tesseract-ocr-ara \
    tesseract-ocr-spa \
    tesseract-ocr-fra \
    tesseract-ocr-deu \
    tesseract-ocr-ita \
    tesseract-ocr-rus \
    tesseract-ocr-chi-sim \
    tesseract-ocr-jpn \
    tesseract-ocr-kor \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mega.py==1.0.8 --no-deps

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Expose port (Render uses PORT environment variable)
EXPOSE 8080

# Make start script executable
RUN chmod +x /app/start.sh

# Run the application with Gunicorn via start script
CMD ["/bin/bash", "/app/start.sh"]
