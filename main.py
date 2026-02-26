import asyncio
import logging
import os
from typing import List, Optional, Set

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from yt_dlp.utils import DownloadError

from downloader import download_audio_mp3, download_tiktok_video
from search_engine import search_youtube


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

_ALLOWED_USER_IDS: Optional[Set[int]] = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await _reject_if_not_allowed(update):
        return
    await update.message.reply_text(
        "Chao ban! Dung lenh /search <ten bai hat> de tim nhac.\n"
        "Dung lenh /help de xem huong dan chi tiet."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await _reject_if_not_allowed(update):
        return
    help_text = """
📖 *HƯỚNG DẪN SỬ DỤNG BOT NHẠC & VIDEO*

🎵 *Các lệnh có sẵn:*

/start - Khởi động bot
/help - Hiển thị menu trợ giúp này
/search <tên bài hát> - Tìm kiếm và tải nhạc từ YouTube
/dowtiktok <URL> - Tải video từ TikTok

📝 *Cách sử dụng:*

*🎧 Tải nhạc YouTube:*
1️⃣ Gõ lệnh /search kèm tên bài hát
   • Ví dụ: `/search Imagine Dragons Believer`
2️⃣ Bot sẽ trả về 5 kết quả phù hợp nhất
3️⃣ Chọn bài hát bạn muốn tải
4️⃣ Chờ bot xử lý và gửi file MP3 cho bạn

*🎬 Tải video TikTok:*
1️⃣ Copy link video TikTok (link đầy đủ hoặc rút gọn)
2️⃣ Gõ lệnh /dowtiktok kèm link
   • Ví dụ: `/dowtiktok https://www.tiktok.com/@user/video/123456`
   • Hoặc: `/dowtiktok https://vm.tiktok.com/xyz123`
3️⃣ Chờ bot tải và gửi video cho bạn

⚠️ *Giới hạn:*
• Nhạc YouTube: < 30 phút → MP3
• Video TikTok: < 10 phút → Video gốc
• Video riêng tư, bị chặn, hoặc giới hạn độ tuổi không tải được

💡 *Mẹo:* 
• Gõ tên bài hát cụ thể kèm tên ca sĩ để kết quả chính xác hơn
• Với TikTok, cả link đầy đủ và link rút gọn đều được hỗ trợ
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def dowtiktok_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await _reject_if_not_allowed(update):
        return
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text(
            "Hay nhap URL video TikTok.\n"
            "Vi du: /dowtiktok https://www.tiktok.com/@user/video/123456"
        )
        return
    
    url = context.args[0]
    # Support both full and shortened TikTok URLs
    if "tiktok.com" not in url and "vm.tiktok.com" not in url:
        await update.message.reply_text("URL khong hop le. Vui long nhap link TikTok.")
        return
    
    msg = await update.message.reply_text("Dang tai video TikTok... 🎬")
    
    try:
        video_path, title, temp_dir = await download_tiktok_video(url)
        with open(video_path, "rb") as video_file:
            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=video_file,
                caption=title,
            )
        await msg.delete()
    except ValueError:
        await msg.edit_text("Video qua dai. Vui long chon video duoi 10 phut.")
    except DownloadError:
        await msg.edit_text(
            "Khong tai duoc video. Video co the bi chan hoac rieng tu."
        )
    except Exception as exc:
        logger.exception("Unexpected error downloading TikTok: %s", exc)
        await msg.edit_text("Da xay ra loi khi tai video.")
    finally:
        if "temp_dir" in locals():
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                logger.warning("Failed to cleanup temp dir: %s", temp_dir)


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
    if await _reject_if_not_allowed(update):
        return
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
    if await _reject_if_not_allowed(update):
        return
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
            text="Video qua dai. Vui long chon bai duoi 30 phut.",
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

    allowed_ids_raw = os.getenv("ALLOWED_TELEGRAM_IDS", "")
    allowed_ids = _parse_allowed_ids(allowed_ids_raw)
    global _ALLOWED_USER_IDS
    _ALLOWED_USER_IDS = allowed_ids if allowed_ids else None

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("dowtiktok", dowtiktok_command))
    application.add_handler(CallbackQueryHandler(handle_download))

    application.run_polling()


def _parse_allowed_ids(value: str) -> Set[int]:
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


async def _reject_if_not_allowed(update: Update) -> bool:
    if not _ALLOWED_USER_IDS:
        return False
    user = update.effective_user
    if not user or user.id not in _ALLOWED_USER_IDS:
        message = "Ban khong co quyen su dung bot."
        if update.message:
            await update.message.reply_text(message)
        elif update.callback_query:
            await update.callback_query.answer(text=message, show_alert=True)
        return True
    return False


if __name__ == "__main__":
    main()
