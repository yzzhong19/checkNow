import time
import schedule
import datetime
import logging
import sys
import traceback
from config import config
from services.gmail_service import gmail_service
from services.llm_service import llm_service
from services.pushover_service import pushover_service
from services.storage import storage

# Configure Logging
# Writes to both console and app.log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def check_emails():
    logging.info("--- Starting Email Check ---")
    
    try:
        # 1. Determine time range
        last_checked = storage.get_last_checked()
        if last_checked == 0:
            # First run: check last 1 hour
            last_checked = time.time() - 3600
            storage.set_last_checked(time.time())

        # 2. Fetch Messages
        try:
            messages = gmail_service.list_messages(last_checked)
        except Exception as e:
            logging.error(f"Failed to fetch messages: {e}")
            pushover_service.send_notification("⚠️ CheckNow Error", f"Gmail API Error: {e}", priority=1)
            return

        logging.info(f"Found {len(messages)} new messages.")

        # Update timestamp
        storage.set_last_checked(time.time())

        # 3. Process each message
        for msg in messages:
            try:
                logging.info(f"Classifying: {msg['subject'][:50]}...")
                classification = llm_service.classify_email(msg)
                
                is_important = classification.get('important', False)
                is_urgent = classification.get('urgent', False)
                score = classification.get('score', 0)
                reasoning = classification.get('reasoning', '')

                logging.info(f"Result: Important={is_important}, Urgent={is_urgent}, Score={score}")

                if is_important or is_urgent or score >= 0.8:
                    # Priority 2: Emergency (Verified Working!)
                    # Priority 1: High
                    # Priority 0: Normal
                    priority = 2 if is_urgent else 0
                    title = f"📧 {'URGENT ' if is_urgent else ''}Important Email: {msg['sender']}"
                    body = f"{msg['subject']}\n\nReason: {reasoning}"
                    url = f"https://mail.google.com/mail/u/0/#inbox/{msg['id']}"
                    
                    pushover_service.send_notification(title, body, priority, url)
                    logging.info(f"Notification sent for message {msg['id']}")
                    
            except Exception as e:
                logging.error(f"Error processing message {msg['id']}: {e}")
            
            # Rate Limit Protection: Wait 2 seconds between LLM calls
            time.sleep(2)

        logging.info("--- Check Complete ---")
        
    except Exception as e:
        # Catch unexpected crashes in the main logic
        logging.critical(f"Critical error in check_emails: {e}\n{traceback.format_exc()}")
        pushover_service.send_notification("🚨 CheckNow CRASH", f"Critical Error: {e}", priority=1)

def send_heartbeat():
    logging.info("❤️ Keeping alive...")
    # Optional: Send a silent notification every day?
    # pushover_service.send_notification("CheckNow Heartbeat", "I'm still running!", priority=-1)

def main():
    logging.info("Gmail Alerter (Python) Started.")
    
    # Check config
    if not config.validate():
        logging.critical("Exiting due to missing configuration.")
        return

    # Authenticate on startup
    if not gmail_service.authenticate():
        logging.critical("Authentication failed. Please check logs.")
        pushover_service.send_notification("🚨 CheckNow Auth Failed", "Could not authenticate with Gmail.", priority=1)
        return
    
    # Run once immediately
    check_emails()

    # Schedule hourly
    schedule.every().hour.do(check_emails)
    
    # Schedule heartbeat (optional, just logging for now)
    schedule.every().day.at("09:00").do(send_heartbeat)

    logging.info("Scheduler running. Press Ctrl+C to exit.")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping...")
            break
        except Exception as e:
            logging.critical(f"Scheduler Crashed: {e}")
            pushover_service.send_notification("🚨 CheckNow Scheduler Crash", f"Error: {e}", priority=1)
            time.sleep(60) # Wait before retrying

if __name__ == "__main__":
    main()
