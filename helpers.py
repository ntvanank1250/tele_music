"""Helper functions and utilities for the bot."""

import logging
import shutil
from functools import wraps
from typing import Callable, Optional, Set

from telegram import Update
from telegram.ext import ContextTypes

from constants import MSG_UNAUTHORIZED


logger = logging.getLogger(__name__)

# Global state for allowed user IDs
_ALLOWED_USER_IDS: Optional[Set[int]] = None


def set_allowed_user_ids(user_ids: Optional[Set[int]]) -> None:
    """Set the allowed user IDs for permission checking."""
    global _ALLOWED_USER_IDS
    _ALLOWED_USER_IDS = user_ids


def is_tiktok_url(url: str) -> bool:
    """Check if URL is a valid TikTok URL."""
    return "tiktok.com" in url or "vm.tiktok.com" in url


def parse_allowed_ids(value: str) -> Set[int]:
    """Parse comma-separated user IDs from string."""
    ids: Set[int] = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            ids.add(int(item))
        except ValueError:
            logger.warning("Invalid Telegram user id: %s", item)
    return ids


async def check_permission(update: Update) -> bool:
    """
    Check if user has permission to use the bot.
    
    Returns:
        True if user is NOT allowed (should reject), False if allowed.
    """
    if not _ALLOWED_USER_IDS:
        return False
    
    user = update.effective_user
    if not user or user.id not in _ALLOWED_USER_IDS:
        if update.message:
            await update.message.reply_text(MSG_UNAUTHORIZED)
        elif update.callback_query:
            await update.callback_query.answer(text=MSG_UNAUTHORIZED, show_alert=True)
        return True
    return False


def require_permission(func: Callable) -> Callable:
    """Decorator to check user permission before executing command."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await check_permission(update):
            return
        return await func(update, context)
    return wrapper


def cleanup_temp_dir(temp_dir: str) -> None:
    """Safely remove temporary directory."""
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as exc:
        logger.warning("Failed to cleanup temp dir %s: %s", temp_dir, exc)


def filter_valid_tiktok_urls(urls: list[str]) -> tuple[list[str], list[str]]:
    """
    Filter and separate valid TikTok URLs from invalid ones.
    
    Returns:
        Tuple of (valid_urls, invalid_urls)
    """
    urls = [url.strip() for url in urls if url.strip()]
    valid_urls = [url for url in urls if is_tiktok_url(url)]
    invalid_urls = [url for url in urls if url not in valid_urls]
    return valid_urls, invalid_urls
