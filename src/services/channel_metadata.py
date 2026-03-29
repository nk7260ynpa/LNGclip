"""頻道元資料抓取服務（使用 yt-dlp）。"""

import logging
from typing import Optional

import yt_dlp

logger = logging.getLogger(__name__)

_YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": True,
}


def _count_tab(channel_url: str, tab: str) -> int:
    """計算頻道特定分頁的影片數量。"""
    try:
        with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
            info = ydl.extract_info(f"{channel_url}/{tab}", download=False)
        count = info.get("playlist_count")
        if count is not None:
            return count
        entries = info.get("entries")
        if entries is not None:
            return len(list(entries))
    except Exception:
        pass
    return 0


def fetch_channel_metadata(channel_url: str) -> Optional[dict]:
    """從 YouTube 頻道 URL 抓取元資料。

    Args:
        channel_url: YouTube 頻道網址。

    Returns:
        包含 channel_name、subscriber_count、video_count 的字典，
        抓取失敗時回傳 None。
    """
    try:
        with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
            info = ydl.extract_info(
                f"{channel_url}/videos", download=False
            )

        channel_name = info.get("channel") or info.get("uploader")
        subscriber_count = info.get("channel_follower_count")

        # 影片數 = videos + shorts
        videos_count = info.get("playlist_count")
        if videos_count is None:
            entries = info.get("entries")
            videos_count = len(list(entries)) if entries else 0

        shorts_count = _count_tab(channel_url, "shorts")

        return {
            "channel_name": channel_name,
            "subscriber_count": subscriber_count,
            "video_count": videos_count + shorts_count,
        }
    except Exception:
        logger.warning("元資料抓取失敗：%s", channel_url, exc_info=True)
        return None
