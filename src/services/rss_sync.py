"""RSS Feed 同步服務。"""

import logging
import time
from datetime import datetime

import feedparser
from sqlalchemy.orm import Session

from src.models.channel import Channel
from src.models.video import Video

logger = logging.getLogger(__name__)

RSS_URL_TEMPLATE = (
    "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
)


def fetch_rss_feed(channel_id: str) -> list[dict]:
    """抓取 YouTube 頻道的 RSS Feed 並解析影片資料。

    Args:
        channel_id: YouTube 頻道 ID。

    Returns:
        影片資料列表，每筆包含 video_id、title、thumbnail、published_at。
    """
    url = RSS_URL_TEMPLATE.format(channel_id=channel_id)
    feed = feedparser.parse(url)

    if feed.bozo and not feed.entries:
        logger.error("RSS 抓取失敗：%s（%s）", channel_id, feed.bozo_exception)
        return []

    videos = []
    for entry in feed.entries:
        video_id = entry.get("yt_videoid", "")
        if not video_id:
            continue

        published = entry.get("published_parsed")
        published_at = (
            datetime(*published[:6]) if published else None
        )

        thumbnail = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"

        videos.append({
            "video_id": video_id,
            "title": entry.get("title", ""),
            "thumbnail": thumbnail,
            "published_at": published_at,
        })

    return videos


def sync_channel_videos(channel: Channel, db: Session) -> int:
    """同步單一頻道的影片。

    Args:
        channel: 頻道 model 實例。
        db: 資料庫 session。

    Returns:
        新增的影片數量。
    """
    logger.info("開始同步頻道：%s（%s）", channel.channel_name, channel.channel_id)

    feed_videos = fetch_rss_feed(channel.channel_id)
    if not feed_videos:
        logger.info("頻道 %s 無影片資料", channel.channel_name)
        return 0

    existing_ids = {
        v.video_id
        for v in db.query(Video.video_id)
        .filter(Video.channel_id == channel.id)
        .all()
    }

    new_count = 0
    for video_data in feed_videos:
        if video_data["video_id"] in existing_ids:
            continue

        video = Video(
            channel_id=channel.id,
            video_id=video_data["video_id"],
            title=video_data["title"],
            thumbnail=video_data["thumbnail"],
            published_at=video_data["published_at"],
        )
        db.add(video)
        new_count += 1

    if new_count > 0:
        db.commit()

    logger.info(
        "頻道 %s 同步完成，新增 %d 部影片", channel.channel_name, new_count
    )
    return new_count


def sync_all_channels(db: Session) -> dict:
    """同步所有啟用頻道的影片。

    Args:
        db: 資料庫 session。

    Returns:
        同步結果摘要。
    """
    start_time = time.time()

    channels = (
        db.query(Channel).filter(Channel.is_active.is_(True)).all()
    )

    logger.info("開始同步所有頻道，共 %d 個", len(channels))

    total_new = 0
    results = []
    for channel in channels:
        new_count = sync_channel_videos(channel, db)
        total_new += new_count
        results.append({
            "channel_name": channel.channel_name,
            "new_videos": new_count,
        })

    elapsed = round(time.time() - start_time, 2)
    logger.info(
        "全部同步完成：%d 個頻道，新增 %d 部影片，耗時 %s 秒",
        len(channels),
        total_new,
        elapsed,
    )

    return {
        "channels_processed": len(channels),
        "total_new_videos": total_new,
        "elapsed_seconds": elapsed,
        "details": results,
    }
