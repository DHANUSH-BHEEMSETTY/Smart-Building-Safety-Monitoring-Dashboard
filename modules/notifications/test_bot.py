from telegram_bot import notify_security

def main():
    print("Sending test notification to Telegram...")
    
    # NOTE: You MUST configure your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID 
    # in telegram_bot.py (or as environment variables) before running this script!
    
    alert_type = "TEST ALERT"
    details = "fire detected in Room 101"
    
    success = notify_security(alert_type, details)
    
    if success:
        print("Success! Check your Telegram app for the message.")
    else:
        print("\nFailed to send message.")
        print("Please ensure you have replaced 'YOUR_BOT_TOKEN_HERE' and 'YOUR_CHAT_ID_HERE'")
        print("in telegram_bot.py with your actual bot credentials from @BotFather and @userinfobot.")

if __name__ == "__main__":
    main()
