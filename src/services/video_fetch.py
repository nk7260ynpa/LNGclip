"""頻道影片抓取服務（使用 yt-dlp）。"""

import logging
from datetime import datetime

import yt_dlp
from sqlalchemy.orm import Session

from src.models.channel import Channel
from src.models.video import Video

logger = logging.getLogger(__name__)


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
        "extract_flat": True,
        "playlistend": limit,
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
        .filter(Video.channel_id == channel.id)
        .all()
    }

    new_count = 0
    for entry in entries:
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

        thumbnail = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"

        video = Video(
            channel_id=channel.id,
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
