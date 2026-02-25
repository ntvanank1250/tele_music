import re
from typing import List, Dict, Any

from youtubesearchpython import VideosSearch


_DURATION_RE = re.compile(r"^(?:(\d+):)?(\d+):(\d+)$")


def _duration_to_seconds(duration: str) -> int:
    match = _DURATION_RE.match(duration.strip())
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def search_youtube(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    results = VideosSearch(query, limit=limit).result().get("result", [])
    items: List[Dict[str, Any]] = []
    for item in results:
        duration = item.get("duration") or ""
        items.append(
            {
                "title": item.get("title") or "",
                "id": item.get("id") or "",
                "url": item.get("link") or "",
                "duration": duration,
                "duration_seconds": _duration_to_seconds(duration),
                "channel": (item.get("channel") or {}).get("name") or "",
            }
        )
    return items
