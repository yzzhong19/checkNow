from services.pushover_service import pushover_service
import time

print("--- Testing Priority 2 (Emergency) Notification ---")
print("This should bypass smooth/silent modes and repeat every 60s.")

try:
    pushover_service.send_notification(
        title="🚨 TEST: URGENT EMERGENCY",
        message="This is a test of the Priority 2 Emergency system. Please acknowledge receipt.",
        priority=2,
        url="https://www.google.com"
    )
    print("✅ Notification Sent! Check your phone immediately.")
except Exception as e:
    print(f"❌ Failed: {e}")
