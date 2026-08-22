# Security Notifications via Telegram

This module is designed to send critical security alerts (such as fire detection, weapons, or unauthorized access) directly to a mobile device via the Telegram Bot API. It is completely free, lightning fast, and has no restrictions on recipient numbers.

## Setup Instructions

To receive messages, you need to configure a Bot Token and your personal Chat ID.

### 1. Create a Bot and Get the API Token
1. Open the Telegram app on your phone or desktop.
2. Search for the **@BotFather** user (it will have a blue verification tick).
3. Send the command `/newbot` and follow the prompts to name your bot and choose a username.
4. Once completed, BotFather will give you a **Bot Token** (e.g., `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
5. Paste this token into `telegram_bot.py` as `TELEGRAM_BOT_TOKEN`, or export it as an environment variable in your terminal.

### 2. Get Your Chat ID
1. Search for your newly created bot on Telegram using its username and click **Start** to initiate a conversation. You must do this so the bot has permission to message you.
2. Next, search for **@userinfobot** or **@get_id_bot** and start a chat with them.
3. The bot will instantly reply with your `chat_id` (a series of numbers, e.g., `987654321`).
4. Paste this ID into `telegram_bot.py` as `TELEGRAM_CHAT_ID`, or export it as an environment variable in your terminal.

### 3. Test the Setup
Run the `test_bot.py` script to confirm that the bot is correctly configured and can reach your phone!

```bash
python test_bot.py
```
If successful, you will instantly receive a test message on your phone.
