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
echo "Starting Ollama..." \n\
ollama serve > ollama.log 2>&1 &\n\
\n\
echo "Waiting for Ollama to be ready..." \n\
until curl -s http://localhost:11434/api/tags > /dev/null; do \n\
  sleep 2 \n\
done \n\
\n\
echo "Pulling model $GEMMA_MODEL..." \n\
ollama pull ${GEMMA_MODEL:-gemma4:e2b} \n\
\n\
echo "Starting FastAPI..." \n\
python app.py \n\
' > start.sh && chmod +x start.sh

# Expose port
EXPOSE 8000

# Run the start script
CMD ["./start.sh"]
