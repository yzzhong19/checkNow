#!/bin/bash
echo "🚀 Installing CheckNow (Beta)..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

# Create Directory
mkdir -p ~/checknow
cd ~/checknow

# Create Config (Token and Storage) if missing
touch token.json storage.json

# Prompt for Keys if .env missing
if [ ! -f .env ]; then
    echo "🔑 Configuration Setup:"
    read -p "Enter Gemini API Key: " gemini_key
    read -p "Enter Pushover User Key: " pushover_user
    # Default CheckNow App Token
    pushover_token="anuvriiayu3u9ehq6j814gwskjb398"
    
    echo "GEMINI_API_KEY=$gemini_key" > .env
    echo "PUSHOVER_USER_KEY=$pushover_user" >> .env
    echo "PUSHOVER_TOKEN=$pushover_token" >> .env
fi

# Run the Beta Image (which has GOOGLE_CLIENT_ID hardcoded inside)
echo "⬇️ Pulling latest version..."
docker pull yzzhong/checknow:beta

echo "✅ Launching... (Click the link below to login)"
docker run -it --rm \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/token.json:/app/token.json \
  -v $(pwd)/storage.json:/app/storage.json \
  -p 8080:8080 \
  yzzhong/checknow:beta python main.py
