import asyncio
import logging
import os
from typing import List

from dotenv import load_dotenv
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from yt_dlp.utils import DownloadError

from constants import (
    BOT_COMMANDS,
    MAX_TIKTOK_DURATION,
    MAX_YOUTUBE_DURATION,
    MSG_COLLECTING_SYSTEM_INFO,
    MSG_DOWNLOAD_AUDIO_FAILED,
    MSG_DOWNLOAD_FAILED,
    MSG_DOWNLOADING_TIKTOK,
    MSG_FB_CONFIG_MISSING,
    MSG_HELP,
    MSG_INVALID_TIKTOK_URL,
    MSG_NO_SEARCH_RESULTS,
    MSG_NO_VALID_TIKTOK_URL,
    MSG_PROCESSING_AUDIO,
    MSG_SEARCH_USAGE,
    MSG_SELECT_SONG,
    MSG_SYSTEM_INFO_ERROR,
    MSG_TIKTOK_USAGE,
    MSG_UNEXPECTED_ERROR,
    MSG_UPFB_COMPLETE,
    MSG_UPFB_FAILED_DOWNLOAD,
    MSG_UPFB_FAILED_LONG,
    MSG_UPFB_FAILED_UPLOAD,
    MSG_UPFB_INVALID_LINKS,
    MSG_UPFB_PROCESSING,
    MSG_UPFB_SUCCESS,
    MSG_UPFB_USAGE,
    MSG_VIDEO_TOO_LONG_TIKTOK,
    MSG_VIDEO_TOO_LONG_YOUTUBE,
    MSG_WELCOME,
)
from downloader import download_audio_mp3, download_tiktok_video
from facebook_uploader import upload_video_to_facebook
from helpers import (
    cleanup_temp_dir,
    filter_valid_tiktok_urls,
    is_tiktok_url,
    parse_allowed_ids,
    require_permission,
    set_allowed_user_ids,
)
from search_engine import search_youtube
from system_info import get_system_info


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@require_permission
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(MSG_WELCOME)


@require_permission
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await update.message.reply_text(MSG_HELP)


@require_permission
async def sys_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /sys command - Display system information."""
    if not update.message:
        return
    
    msg = await update.message.reply_text(MSG_COLLECTING_SYSTEM_INFO)
    
    try:
        system_info = await get_system_info()
        await msg.edit_text(system_info, parse_mode="Markdown")
    except Exception as exc:
        logger.exception("Error getting system info: %s", exc)
        await msg.edit_text(MSG_SYSTEM_INFO_ERROR)


@require_permission
async def dowtiktok_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /dowtiktok command - Download TikTok video."""
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text(MSG_TIKTOK_USAGE)
        return
    
    url = context.args[0]
    if not is_tiktok_url(url):
        await update.message.reply_text(MSG_INVALID_TIKTOK_URL)
        return
    
    msg = await update.message.reply_text(MSG_DOWNLOADING_TIKTOK)
    temp_dir = None
    
    try:
        video_path, title, temp_dir = await download_tiktok_video(url, MAX_TIKTOK_DURATION)
        with open(video_path, "rb") as video_file:
            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=video_file,
                caption=title,
            )
        await msg.delete()
    except ValueError:
        await msg.edit_text(MSG_VIDEO_TOO_LONG_TIKTOK)
    except DownloadError:
        await msg.edit_text(MSG_DOWNLOAD_FAILED)
    except Exception as exc:
        logger.exception("Unexpected error downloading TikTok: %s", exc)
        await msg.edit_text(MSG_UNEXPECTED_ERROR)
    finally:
        if temp_dir:
            cleanup_temp_dir(temp_dir)


@require_permission
async def upfb_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /upfb command - Upload TikTok videos to Facebook Page."""
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text(MSG_UPFB_USAGE)
        return

    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")
    if not page_id or not access_token:
        await update.message.reply_text(MSG_FB_CONFIG_MISSING)
        return

    valid_urls, invalid_urls = filter_valid_tiktok_urls(context.args)
    if not valid_urls:
        await update.message.reply_text(MSG_NO_VALID_TIKTOK_URL)
        return

    msg = await update.message.reply_text(
        MSG_UPFB_PROCESSING.format(0, len(valid_urls))
    )

    results = []
    for idx, url in enumerate(valid_urls, start=1):
        await msg.edit_text(MSG_UPFB_PROCESSING.format(idx, len(valid_urls)))
        temp_dir = None
        
        try:
            video_path, title, temp_dir = await download_tiktok_video(url, MAX_TIKTOK_DURATION)
            await asyncio.to_thread(
                upload_video_to_facebook,
                video_path,
                title,
                page_id,
                access_token,
            )
            results.append(f"{idx}. {MSG_UPFB_SUCCESS.format(title)}")
        except ValueError:
            results.append(f"{idx}. {MSG_UPFB_FAILED_LONG}")
        except DownloadError:
            results.append(f"{idx}. {MSG_UPFB_FAILED_DOWNLOAD}")
        except Exception as exc:
            logger.exception("Unexpected error uploading to Facebook: %s", exc)
            results.append(f"{idx}. {MSG_UPFB_FAILED_UPLOAD}")
        finally:
            if temp_dir:
                cleanup_temp_dir(temp_dir)

    if invalid_urls:
        results.append(MSG_UPFB_INVALID_LINKS.format(", ".join(invalid_urls)))

    await msg.edit_text(MSG_UPFB_COMPLETE + "\n".join(results))


def _build_results_keyboard(results: List[dict]) -> InlineKeyboardMarkup:
    buttons = []
    for item in results:
        title = item.get("title") or ""
        video_id = item.get("id") or ""
        duration = item.get("duration") or ""
        label = title if not duration else f"{title} ({duration})"
        buttons.append([InlineKeyboardButton(label, callback_data=f"dl:{video_id}")])
    return InlineKeyboardMarkup(buttons)


@require_permission
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /search command - Search YouTube videos."""
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text(MSG_SEARCH_USAGE)
        return
    
    query = " ".join(context.args)
    results = await asyncio.to_thread(search_youtube, query, 5)
    if not results:
        await update.message.reply_text(MSG_NO_SEARCH_RESULTS)
        return
    
    keyboard = _build_results_keyboard(results)
    await update.message.reply_text(MSG_SELECT_SONG, reply_markup=keyboard)


@require_permission
async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback query for downloading YouTube audio."""
    query = update.callback_query
    if not query:
        return
    await query.answer()
    if not query.data or not query.data.startswith("dl:"):
        return
    
    video_id = query.data.split(":", 1)[1]
    url = f"https://www.youtube.com/watch?v={video_id}"

    await query.edit_message_text(MSG_PROCESSING_AUDIO)
    temp_dir = None
    
    try:
        mp3_path, title, temp_dir = await download_audio_mp3(url, MAX_YOUTUBE_DURATION)
        with open(mp3_path, "rb") as audio_file:
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=audio_file,
                title=title,
            )
    except ValueError:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=MSG_VIDEO_TOO_LONG_YOUTUBE,
        )
    except DownloadError:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=MSG_DOWNLOAD_AUDIO_FAILED,
        )
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=MSG_UNEXPECTED_ERROR,
        )
    finally:
        if temp_dir:
            cleanup_temp_dir(temp_dir)


async def post_init(application: Application) -> None:
    """Set bot commands menu after initialization."""
    try:
        commands = [BotCommand(cmd, desc) for cmd, desc in BOT_COMMANDS]
        await application.bot.set_my_commands(commands)
        logger.info("Bot commands menu has been set successfully")
    except Exception as exc:
        logger.warning("Failed to set bot commands menu: %s", exc)


def main() -> None:
    """Main function to start the bot."""
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Check your .env file.")

    # Setup allowed user IDs
    allowed_ids_raw = os.getenv("ALLOWED_TELEGRAM_IDS", "")
    allowed_ids = parse_allowed_ids(allowed_ids_raw)
    set_allowed_user_ids(allowed_ids if allowed_ids else None)

    # Build application
    application = Application.builder().token(token).post_init(post_init).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("dowtiktok", dowtiktok_command))
    application.add_handler(CommandHandler("upfb", upfb_command))
    application.add_handler(CommandHandler("sys", sys_command))
    application.add_handler(CallbackQueryHandler(handle_download))

    # Start polling
    application.run_polling()


if __name__ == "__main__":
    main()
