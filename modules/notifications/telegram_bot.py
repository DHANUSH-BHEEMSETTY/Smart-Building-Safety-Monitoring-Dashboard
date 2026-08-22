import os
import requests

# Set your Telegram Bot Token and Chat ID as environment variables or update them here for testing
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def notify_security(alert_type, details):
    """
    Sends an alert message to a phone via Telegram.
    """
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("Warning: Telegram Bot Token or Chat ID is not configured. Message not sent.")
        return False
        
    message = f"🚨 *{alert_type.upper()}* 🚨\n{details}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[{alert_type}] Notification sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram notification: {e}")
        return False
