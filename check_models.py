import requests
import os
from config import config

def list_models():
    api_key = config.GEMINI_API_KEY
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print("Available Models:")
        for model in data.get('models', []):
            if 'generateContent' in model['supportedGenerationMethods']:
                print(f"- {model['name']}")
                
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
