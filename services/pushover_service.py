import requests
from config import config

class PushoverService:
    def __init__(self):
        self.user_key = config.PUSHOVER_USER_KEY
        self.token = config.PUSHOVER_TOKEN
        self.url = "https://api.pushover.net/1/messages.json"

    def send_notification(self, title, message, priority=0, url=None):
        if not self.user_key or not self.token:
            print("Pushover credentials missing. Skipping notification.")
            print(f"[Would have sent] {title}: {message}")
            return

        payload = {
            "token": self.token,
            "user": self.user_key,
            "title": title,
            "message": message,
            "priority": priority,
        }
        
        if url:
            payload["url"] = url
            payload["url_title"] = "View Email"
            
        if priority > 0:
            payload["sound"] = "critical"
            
        if priority == 2:
            payload["retry"] = 60  # Retry every 60 seconds
            payload["expire"] = 3600 # Stop retrying after 1 hour

        try:
            response = requests.post(self.url, data=payload)
            response.raise_for_status()
            print(f"Notification sent: {title}")
        except Exception as e:
            print(f"Failed to send Pushover notification: {e}")

pushover_service = PushoverService()
