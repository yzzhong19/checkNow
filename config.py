import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080/')
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
    PUSHOVER_TOKEN = os.getenv('PUSHOVER_TOKEN')
    
    # Validation
    @classmethod
    def validate(cls):
        missing = []
        if not cls.GOOGLE_CLIENT_ID: missing.append('GOOGLE_CLIENT_ID')
        if not cls.GOOGLE_CLIENT_SECRET: missing.append('GOOGLE_CLIENT_SECRET')
        if not cls.GEMINI_API_KEY: missing.append('GEMINI_API_KEY')
        if not cls.PUSHOVER_USER_KEY: missing.append('PUSHOVER_USER_KEY')
        if not cls.PUSHOVER_TOKEN: missing.append('PUSHOVER_TOKEN')
        
        if missing:
            print(f"WARNING: Missing environment variables: {', '.join(missing)}")
            return False
        return True

config = Config()
