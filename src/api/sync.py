"""手動同步 API。"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.channel import Channel
from src.services.rss_sync import sync_channel_videos, sync_all_channels

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/channels/{channel_db_id}/sync")
def sync_single_channel(channel_db_id: int, db: Session = Depends(get_db)):
    """手動觸發單一頻道的影片同步。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    new_count = sync_channel_videos(channel, db)
    logger.info("手動同步頻道 %s，新增 %d 部影片", channel.channel_name, new_count)
    return {"channel_name": channel.channel_name, "new_videos": new_count}


@router.post("/sync")
def sync_all(db: Session = Depends(get_db)):
    """手動觸發所有啟用頻道的影片同步。"""
    result = sync_all_channels(db)
    return result
