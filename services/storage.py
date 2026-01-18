import json
import os
import time

STORAGE_FILE = "storage.json"

class StorageService:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, 'r') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading storage: {e}")
                self.data = {}
        else:
            self.data = {}

    def save(self):
        try:
            with open(STORAGE_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving storage: {e}")

    def get_last_checked(self) -> float:
        self.load() # reload to get latest
        return self.data.get('last_checked', 0.0)

    def set_last_checked(self, timestamp: float):
        self.data['last_checked'] = timestamp
        self.save()

storage = StorageService()
