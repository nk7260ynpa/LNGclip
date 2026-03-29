"""頻道元資料抓取服務（使用 yt-dlp）。"""

import logging
from typing import Optional

import yt_dlp

logger = logging.getLogger(__name__)


def fetch_channel_metadata(channel_url: str) -> Optional[dict]:
    """從 YouTube 頻道 URL 抓取元資料。

    Args:
        channel_url: YouTube 頻道網址。

    Returns:
        包含 channel_name、subscriber_count、video_count 的字典，
        抓取失敗時回傳 None。
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "playlist_items": "0",
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

        return {
            "channel_name": info.get("channel") or info.get("uploader"),
            "subscriber_count": info.get("channel_follower_count"),
            "video_count": info.get("playlist_count"),
        }
    except Exception:
        logger.warning("元資料抓取失敗：%s", channel_url, exc_info=True)
        return None
