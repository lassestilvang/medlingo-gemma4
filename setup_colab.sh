#!/bin/bash
# MedLingo Colab Setup Script

echo "🚀 Starting MedLingo Setup..."

# 1. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet

# 2. Install Ollama
echo "🦙 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# 3. Start Ollama in the background
echo "⚡ Starting Ollama server..."
ollama serve > ollama.log 2>&1 &
sleep 5

# 4. Pull Gemma 4
echo "📥 Pulling Gemma 4 model (this may take a few minutes)..."
ollama pull gemma4:e4b

# 5. Install Localtunnel for public access
echo "🌐 Installing Localtunnel..."
npm install -g localtunnel --quiet

echo "✅ Setup complete! You can now run the app."
