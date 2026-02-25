import asyncio
import logging
import os
from typing import List

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from yt_dlp.utils import DownloadError

from downloader import download_audio_mp3
from search_engine import search_youtube


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Chao ban! Dung lenh /search <ten bai hat> de tim nhac."
    )


def _build_results_keyboard(results: List[dict]) -> InlineKeyboardMarkup:
    buttons = []
    for item in results:
        title = item.get("title") or ""
        video_id = item.get("id") or ""
        duration = item.get("duration") or ""
        label = title if not duration else f"{title} ({duration})"
        buttons.append([InlineKeyboardButton(label, callback_data=f"dl:{video_id}")])
    return InlineKeyboardMarkup(buttons)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Hay nhap tu khoa. Vi du: /search Imagine Dragons")
        return
    query = " ".join(context.args)
    results = await asyncio.to_thread(search_youtube, query, 5)
    if not results:
        await update.message.reply_text("Khong tim thay ket qua phu hop.")
        return
    keyboard = _build_results_keyboard(results)
    await update.message.reply_text("Chon bai hat:", reply_markup=keyboard)


async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return
    await query.answer()
    if not query.data or not query.data.startswith("dl:"):
        return
    video_id = query.data.split(":", 1)[1]
    url = f"https://www.youtube.com/watch?v={video_id}"

    await query.edit_message_text("Dang xu ly am thanh... 🎧")
    try:
        mp3_path, title, temp_dir = await download_audio_mp3(url)
        with open(mp3_path, "rb") as audio_file:
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=audio_file,
                title=title,
            )
    except ValueError:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Video qua dai. Vui long chon bai duoi 10 phut.",
        )
    except DownloadError:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Khong tai duoc am thanh. Video co the bi chan hoac gioi han tuoi.",
        )
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Da xay ra loi khi xu ly yeu cau.",
        )
    finally:
        if "temp_dir" in locals():
            try:
                import shutil

                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                logger.warning("Failed to cleanup temp dir: %s", temp_dir)


def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Check your .env file.")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CallbackQueryHandler(handle_download))

    application.run_polling()


if __name__ == "__main__":
    main()
