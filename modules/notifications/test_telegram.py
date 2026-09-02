import sys
import os

# Set stdout encoding for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add capstone root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.notifications.telegram_notifier import send_telegram_alert, get_telegram_credentials

def main():
    print("==================================================")
    print("🛡️  Telegram Notification Setup Verification")
    print("==================================================")
    
    # 1. Check Credentials in .env
    print("\n[Step 1] Checking .env configuration...")
    try:
        token, chat_id = get_telegram_credentials()
        print("✅ .env file successfully located and parsed.")
        print(f"✅ TELEGRAM_BOT_TOKEN: Present (length: {len(token)} characters)")
        print(f"✅ TELEGRAM_CHAT_ID:   Present (length: {len(chat_id)} characters)")
    except Exception as e:
        print(f"\n❌ Credential Verification Failed: {e}")
        print("\nPlease create a '.env' file at the project root with the following format:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather")
        print("TELEGRAM_CHAT_ID=your_chat_id")
        sys.exit(1)
        
    # 2. Dispatch Test Alert
    print("\n[Step 2] Sending verification test alert to Telegram...")
    try:
        success, message = send_telegram_alert(
            alert_type="SYSTEM TEST",
            location="Zone 102 - Security Server Room",
            details="AegisAI security monitoring pipeline is online and connected.",
            force=True  # Bypass 60s rate limit for test
        )
        if success:
            print("\n🎉 SUCCESS! Test message sent to your Telegram channel/chat.")
            print("👉 Please check your Telegram app to confirm receipt.")
        else:
            print(f"\n❌ Dispatch Failed: {message}")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during Telegram transmission: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
