"""
telegram_bot.py — Legacy compatibility module redirecting to telegram_notifier.py
"""
from .telegram_notifier import (
    get_telegram_credentials,
    send_telegram_alert,
    notify_security,
    reset_rate_limits,
    RATE_LIMIT_SECONDS
)

__all__ = [
    "get_telegram_credentials",
    "send_telegram_alert",
    "notify_security",
    "reset_rate_limits",
    "RATE_LIMIT_SECONDS"
]
