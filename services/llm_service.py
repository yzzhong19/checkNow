import requests
import json
from config import config

class LLMService:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        # Switching to the 'latest' alias which usually points to the current stable Flash model (1.5 or 2.0)
        # This often has better availability on free tiers than specific preview versions.
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.api_key}"

    def classify_email(self, email_data):
        if not self.api_key:
            print("No Gemini API Key provided")
            return {"important": False, "score": 0, "reasoning": "No API Key"}

        prompt = f"""
You are a strict personal filtration assistant. I ONLY want to be notified about emails that have DIRECT PERSONAL CONSEQUENCES if I do not act.

CRITERIA FOR "IMPORTANT":
1. FINANCIAL LOSS: Bills, subscription renewals, unpaid invoices, tax documents.
2. CRITICAL DEADLINES: Medical enrollment, voting registration, flight check-ins, appointment confirmations.
3. SECURITY: Account breaches, login verification codes, password resets.

CRITERIA FOR "IGNORE" (Even if it looks important):
- General company updates (e.g., "We raised $100M", "New Policy Update").
- Investor updates, industry news, or newsletters.
- Marketing masquerading as alerts (e.g., "Last chance to save!").
- Social media notifications (LinkedIn, Twitter, etc).

Email Subject: {email_data['subject']}
Sender: {email_data['sender']}
Snippet: {email_data['snippet']}
Date: {email_data['date']}

Respond with a purely JSON object (no markdown, no backticks).
Format:
{{
  "important": boolean,
  "urgent": boolean,
  "score": number (0.0 to 1.0, where 1.0 is extremely critical),
  "reasoning": "short explanation"
}}
"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        # Retry logic for Rate Limits (429)
        import time
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                
                # Clean up potential markdown
                text = text.replace('```json', '').replace('```', '').strip()
                
                return json.loads(text)
                
            except requests.exceptions.HTTPError as e:
                # If we get a 429 (Too Many Requests), wait and retry
                if e.response.status_code == 429:
                    wait_time = (attempt + 1) * 5  # Wait 5s, 10s, 15s
                    print(f"⚠️ Hit Rate Limit (429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    # Other errors (404, 500) we assume are fatal
                    print(f"LLM Classification HTTP failed: {e}")
                    return {"important": False, "score": 0, "reasoning": f"HTTP Error: {e}"}
                    
            except Exception as e:
                print(f"LLM Classification failed: {e}")
                return {"important": False, "score": 0, "reasoning": f"Error: {e}"}

        # If we exhausted all retries
        return {"important": False, "score": 0, "reasoning": "Failed after max retries (Rate Limit)"}

llm_service = LLMService()
