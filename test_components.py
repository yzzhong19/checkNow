import sys
import time
import argparse
from config import config
from services.gmail_service import gmail_service
from services.llm_service import llm_service
from services.pushover_service import pushover_service

def test_pushover():
    print("\n[TEST] Pushover Notification")
    print("--------------------------------")
    try:
        pushover_service.send_notification(
            title="Test Notification",
            message="This is a test from the Gmail Alerter App.",
            priority=0
        )
        print("✅ Notification sent successfully! Check your device.")
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")

def test_llm():
    print("\n[TEST] LLM Classification")
    print("--------------------------------")
    
    mock_email = {
        "subject": "Urgent: Invoice Overdue",
        "sender": "billing@example.com",
        "snippet": "Your payment of $500 is overdue by 3 days. Please pay immediately to avoid service interruption.",
        "date": "2023-10-27T10:00:00Z"
    }
    
    print(f"Sending mock email to LLM:\nSubject: {mock_email['subject']}\nSnippet: {mock_email['snippet'][:50]}...")
    
    try:
        result = llm_service.classify_email(mock_email)
        print(f"\n✅ Result: {result}")
        
        if result.get('important') or result.get('urgent'):
             print("   (Correctly identified as important/urgent)")
        else:
             print("   (Classified as normal)")
             
    except Exception as e:
        print(f"❌ LLM Test Failed: {e}")

def test_gmail():
    print("\n[TEST] Gmail API")
    print("--------------------------------")
    
    try:
        if not gmail_service.authenticate():
            print("❌ Authentication failed. Cannot proceed.")
            return

        print("✅ Authenticated successfully.")
        
        # Check messages from last 24 hours
        one_day_ago = time.time() - (24 * 3600)
        print(f"Fetching messages since unix timestamp: {one_day_ago}")
        
        messages = gmail_service.list_messages(one_day_ago)
        
        if messages:
            print(f"✅ Found {len(messages)} messages.")
            print("First message details:")
            print(f"  Subject: {messages[0]['subject']}")
            print(f"  From:    {messages[0]['sender']}")
        else:
            print("✅ API call successful, but no new messages found (this is normal if inbox is quiet).")
            
    except Exception as e:
         print(f"❌ Gmail Test Failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Test Gmail Alerter Components")
    parser.add_argument('component', choices=['pushover', 'llm', 'gmail', 'all'], help='Component to test')
    
    args = parser.parse_args()
    
    # Check config validity first
    if not config.validate():
        print("❌ Configuration invalid. Please check .env file.")
        return

    if args.component == 'pushover' or args.component == 'all':
        test_pushover()
    
    if args.component == 'llm' or args.component == 'all':
        test_llm()
        
    if args.component == 'gmail' or args.component == 'all':
        test_gmail()

if __name__ == "__main__":
    main()
