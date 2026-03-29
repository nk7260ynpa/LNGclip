"""影片查詢 API。"""

import logging
import time
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.channel import Channel
from src.models.video import Video
from src.schemas.video import VideoResponse
from src.services.video_fetch import fetch_channel_videos

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/videos")
def list_videos(
    page: int = Query(1, ge=1),
    per_page: int = Query(9, ge=1, le=50),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """取得所有影片（跨頻道），依發佈時間倒序，支援分頁與標題搜尋。"""
    query = db.query(Video)

    if search:
        query = query.filter(Video.title.ilike(f"%{search}%"))

    total = query.with_entities(func.count(Video.id)).scalar()
    total_pages = max(1, -(-total // per_page))

    videos = (
        query
        .order_by(Video.published_at.desc().nullslast(), Video.id.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "videos": [VideoResponse.model_validate(v).model_dump() for v in videos],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }


@router.post("/crawl")
def crawl_all(db: Session = Depends(get_db)):
    """手動觸發所有頻道的影片爬蟲。"""
    start_time = time.time()
    channels = db.query(Channel).all()
    logger.info("手動爬蟲開始，共 %d 個頻道", len(channels))

    total_new = 0
    results = []
    for channel in channels:
        new_count = fetch_channel_videos(channel, db, limit=15)
        total_new += new_count
        results.append({
            "channel_id": channel.channel_id,
            "new_videos": new_count,
        })
        time.sleep(2)

    elapsed = round(time.time() - start_time, 2)
    logger.info(
        "手動爬蟲完成：%d 個頻道，新增 %d 部影片，耗時 %s 秒",
        len(channels), total_new, elapsed,
    )

    return {
        "channels_processed": len(channels),
        "total_new_videos": total_new,
        "elapsed_seconds": elapsed,
        "details": results,
    }
