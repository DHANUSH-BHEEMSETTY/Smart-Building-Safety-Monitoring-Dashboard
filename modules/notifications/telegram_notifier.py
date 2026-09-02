import os
import time
import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load environment variables from project root .env
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

# In-memory alert timestamps for 60-second rate-limiting: {(alert_type, location): timestamp}
_alert_history = {}
RATE_LIMIT_SECONDS = 60


def get_telegram_credentials():
    """
    Loads and validates Telegram credentials from .env.
    Raises ValueError with a clear actionable message if missing or empty.
    Never prints or logs the secret credentials.
    """
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not token.strip() or token.strip() == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("TELEGRAM_BOT_TOKEN not found — check your .env file at the project root.")

    if not chat_id or not chat_id.strip() or chat_id.strip() == "YOUR_CHAT_ID_HERE":
        raise ValueError("TELEGRAM_CHAT_ID not found — check your .env file at the project root.")

    return token.strip(), chat_id.strip()


def send_telegram_alert(alert_type: str, location: str, details: str = None, confidence: float = None, force: bool = False):
    """
    Sends a structured Telegram security alert with a 60-second duplicate suppression window.
    
    Parameters:
      - alert_type: "fire", "weapon_detected", "suspicious_activity"
      - location: camera/zone identifier (e.g., "102", "Zone A")
      - details: optional descriptive string
      - confidence: optional model confidence score
      - force: if True, bypasses the 60-second rate limiter (for standalone tests)
      
    Returns: (success: bool, status_message: str)
    """
    now = time.time()
    key = (alert_type.lower().strip(), str(location).strip())

    # 60-second rate limit check
    if not force and key in _alert_history:
        elapsed = now - _alert_history[key]
        if elapsed < RATE_LIMIT_SECONDS:
            remaining = int(RATE_LIMIT_SECONDS - elapsed)
            msg = f"Rate limited: alert for [{alert_type}] at [{location}] was sent {int(elapsed)}s ago. Next alert allowed in {remaining}s."
            print(f"[Telegram RateLimit] {msg}")
            return False, msg

    token, chat_id = get_telegram_credentials()
    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")

    # Format structured message
    alert_lower = alert_type.lower().strip()
    if alert_lower == "fire":
        header = "🚨 *EMERGENCY FIRE & SMOKE ALERT* 🚨"
        msg_lines = [
            header,
            f"📍 *Location:* Room/Corridor {location}",
            f"⏱ *Timestamp:* `{current_time_str}`",
        ]
        if confidence is not None:
            msg_lines.append(f"📊 *Detection Confidence:* `{confidence:.2f}`")
        msg_lines.append("⚠️ *Status:* Confirmed sustained hazard — Automated dynamic evacuation route initiated.")
        if details:
            msg_lines.append(f"📝 *Details:* {details}")

    elif alert_lower in ("weapon_detected", "weapon"):
        header = "🚨 *LETHAL THREAT: WEAPON DETECTED* 🚨"
        msg_lines = [
            header,
            f"📍 *Location:* Zone {location}",
            f"⏱ *Timestamp:* `{current_time_str}`",
            f"⚠️ *Threat Identified:* {details if details else 'Visual weapon detection confirmed.'}",
            "👮‍♂️ *Protocol:* Immediate security dispatch triggered."
        ]

    elif alert_lower in ("suspicious_activity", "suspicious"):
        header = "⚠️ *SECURITY ALERT: SUSPICIOUS ACTIVITY* ⚠️"
        msg_lines = [
            header,
            f"📍 *Location:* Zone {location}",
            f"⏱ *Timestamp:* `{current_time_str}`",
            f"🔍 *Infraction Reason:* {details if details else 'After-hours restricted zone entry.'}",
            "👮‍♂️ *Protocol:* Incident logged and security notified."
        ]

    else:
        header = f"🚨 *SECURITY EVENT: {alert_type.upper()}* 🚨"
        msg_lines = [
            header,
            f"📍 *Location:* {location}",
            f"⏱ *Timestamp:* `{current_time_str}`",
            f"📝 *Details:* {details if details else 'Security alert triggered.'}"
        ]

    message = "\n".join(msg_lines)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        _alert_history[key] = now
        print(f"[Telegram] Notification sent successfully for [{alert_type}] at [{location}].")
        return True, "Notification sent successfully."
    except requests.exceptions.RequestException as e:
        err_msg = f"Telegram API error: {e}"
        print(f"[Telegram Error] {err_msg}")
        return False, err_msg


def notify_security(alert_type: str, details: str, location: str = "102"):
    """
    Backwards-compatible wrapper matching the legacy notify_security signature.
    """
    success, _ = send_telegram_alert(alert_type=alert_type, location=location, details=details)
    return success


def reset_rate_limits():
    """Clears the 60-second rate limiter cache."""
    _alert_history.clear()
