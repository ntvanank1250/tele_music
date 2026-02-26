import asyncio
import os
import shutil
import tempfile
from typing import Tuple

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


DEFAULT_MAX_DURATION_SECONDS = 60 * 60


def _build_ydl_opts(output_dir: str) -> dict:
    return {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }


def _fetch_info(url: str) -> dict:
    with YoutubeDL({"quiet": True}) as ydl:
        return ydl.extract_info(url, download=False)


def _download_audio(url: str, output_dir: str) -> Tuple[str, str]:
    opts = _build_ydl_opts(output_dir)
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        mp3_path = f"{base}.mp3"
        title = info.get("title") or "audio"
        return mp3_path, title


async def download_audio_mp3(url: str, max_duration_seconds: int = 30 * 60) -> Tuple[str, str, str]:
    """Download YouTube audio as MP3. Default max duration is 30 minutes."""
    temp_dir = tempfile.mkdtemp(prefix="tele_music_")
    try:
        info = await asyncio.to_thread(_fetch_info, url)
        duration = info.get("duration") or 0
        if duration and duration > max_duration_seconds:
            raise ValueError("Video too long")
        mp3_path, title = await asyncio.to_thread(_download_audio, url, temp_dir)
        return mp3_path, title, temp_dir
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def _build_tiktok_opts(output_dir: str) -> dict:
    return {
        "format": "best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": True,
    }


def _download_tiktok(url: str, output_dir: str) -> Tuple[str, str]:
    opts = _build_tiktok_opts(output_dir)
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get("title") or "tiktok_video"
        return filename, title


async def download_tiktok_video(url: str, max_duration_seconds: int = 10 * 60) -> Tuple[str, str, str]:
    """Download TikTok video. Default max duration is 10 minutes."""
    temp_dir = tempfile.mkdtemp(prefix="tiktok_")
    try:
        info = await asyncio.to_thread(_fetch_info, url)
        duration = info.get("duration") or 0
        if duration and duration > max_duration_seconds:
            raise ValueError("Video too long")
        video_path, title = await asyncio.to_thread(_download_tiktok, url, temp_dir)
        return video_path, title, temp_dir
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise
