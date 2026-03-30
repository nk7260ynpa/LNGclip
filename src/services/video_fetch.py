"""頻道影片抓取服務（使用 yt-dlp）。"""

import logging
import os
import urllib.request
from datetime import datetime

import yt_dlp
from sqlalchemy.orm import Session

from src.models.channel import Channel
from src.models.video import Video

logger = logging.getLogger(__name__)

IMAGES_DIR = os.getenv("IMAGES_DIR", "images")


def _download_thumbnail(video_id: str) -> str:
    """下載影片縮圖到本地 images/ 目錄。

    Args:
        video_id: YouTube 影片 ID。

    Returns:
        本地路徑（成功）或 YouTube CDN URL（失敗時 fallback）。
    """
    cdn_url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
    local_path = os.path.join(IMAGES_DIR, f"{video_id}.jpg")

    if os.path.exists(local_path):
        return f"/api/images/{video_id}.jpg"

    try:
        os.makedirs(IMAGES_DIR, exist_ok=True)
        urllib.request.urlretrieve(cdn_url, local_path)
        return f"/api/images/{video_id}.jpg"
    except Exception:
        logger.warning("縮圖下載失敗：%s", video_id)
        return cdn_url


def fetch_channel_videos(channel: Channel, db: Session, limit: int = 30) -> int:
    """抓取頻道最新影片並寫入 DB。

    Args:
        channel: 頻道 model 實例。
        db: 資料庫 session。
        limit: 最多抓取的影片數量。

    Returns:
        新增的影片數量。
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "playlistend": limit,
        "extract_flat": False,
        "ignoreerrors": True,
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(
                f"{channel.channel_url}/videos", download=False
            )
    except Exception:
        logger.warning("影片列表抓取失敗：%s", channel.channel_id, exc_info=True)
        return 0

    entries = info.get("entries")
    if not entries:
        logger.info("頻道 %s 無影片資料", channel.channel_id)
        return 0

    existing_ids = {
        v.video_id
        for v in db.query(Video.video_id)
        .filter(Video.channel_id == channel.channel_id)
        .all()
    }

    new_count = 0
    for entry in entries:
        if entry is None:
            continue
        video_id = entry.get("id", "")
        if not video_id or video_id in existing_ids:
            continue

        upload_date = entry.get("upload_date")
        published_at = None
        if upload_date:
            try:
                published_at = datetime.strptime(upload_date, "%Y%m%d")
            except ValueError:
                pass

        thumbnail = _download_thumbnail(video_id)

        video = Video(
            channel_id=channel.channel_id,
            video_id=video_id,
            title=entry.get("title", ""),
            thumbnail=thumbnail,
            published_at=published_at,
        )
        db.add(video)
        new_count += 1

    if new_count > 0:
        db.commit()

    logger.info(
        "頻道 %s 影片抓取完成，新增 %d 部", channel.channel_id, new_count
    )
    return new_count
