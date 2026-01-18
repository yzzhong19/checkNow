import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import config
from services.storage import storage
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None

    def authenticate(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            try:
                self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            except Exception:
                self.creds = None

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception:
                    self.creds = None

            if not self.creds:
                # We need to construct a client config dictionary manually 
                # because we are reading from env vars, not a file.
                client_config = {
                    "installed": {
                        "client_id": config.GOOGLE_CLIENT_ID,
                        "client_secret": config.GOOGLE_CLIENT_SECRET,
                        "project_id": "checknow-app", # dummy value usually ok
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": ["http://localhost:8080/"]
                    }
                }
                
                try:
                    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                    self.creds = flow.run_local_server(port=8080)
                except Exception as e:
                    print(f"Authentication failed: {e}")
                    return False

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            self.service = build("gmail", "v1", credentials=self.creds)
            return True
        except Exception as e:
            print(f"Failed to build service: {e}")
            return False

    def list_messages(self, after_timestamp: float):
        if not self.service:
            if not self.authenticate():
                return []

        # Convert to seconds
        after_seconds = int(after_timestamp)
        query = f"after:{after_seconds}"
        print(f"Searching email with query: {query}")

        try:
            results = self.service.users().messages().list(userId="me", q=query).execute()
            messages = results.get("messages", [])
            
            detailed_messages = []
            for msg in messages:
                msg_id = msg['id']
                try:
                    # Get full details
                    details = self.service.users().messages().get(userId="me", id=msg_id).execute()
                    
                    payload = details.get('payload', {})
                    headers = payload.get('headers', [])
                    
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown)')
                    date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                    snippet = details.get('snippet', '')
                    
                    detailed_messages.append({
                        'id': msg_id,
                        'subject': subject,
                        'sender': sender,
                        'date': date_str,
                        'snippet': snippet
                    })
                except Exception as e:
                    print(f"Error fetching details for message {msg_id}: {e}")
            
            return detailed_messages

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

gmail_service = GmailService()
