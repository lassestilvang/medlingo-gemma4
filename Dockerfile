# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a start script to handle Ollama and the App
RUN echo '#!/bin/bash\n\
ollama serve > ollama.log 2>&1 &\n\
sleep 5\n\
ollama pull gemma4:e4b\n\
python app.py\n\
' > start.sh && chmod +x start.sh

# Expose port
EXPOSE 8000

# Run the start script
CMD ["./start.sh"]
