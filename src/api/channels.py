"""頻道 CRUD API。"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.channel import Channel
from src.models.video import Video
from src.schemas.channel import ChannelCreate, ChannelResponse, ChannelUpdate
from src.services.rss_sync import sync_channel_videos

logger = logging.getLogger(__name__)

router = APIRouter()


def _channel_to_response(channel: Channel, db: Session) -> dict:
    """將 Channel model 轉換為回應字典（含 video_count）。"""
    video_count = db.query(func.count(Video.id)).filter(
        Video.channel_id == channel.id
    ).scalar()
    return {
        **{c.name: getattr(channel, c.name) for c in channel.__table__.columns},
        "video_count": video_count,
    }


@router.get("/channels", response_model=list[ChannelResponse])
def list_channels(active_only: bool = False, db: Session = Depends(get_db)):
    """取得頻道列表。"""
    query = db.query(Channel)
    if active_only:
        query = query.filter(Channel.is_active.is_(True))
    channels = query.order_by(Channel.channel_name).all()
    return [_channel_to_response(ch, db) for ch in channels]


@router.get("/channels/{channel_db_id}", response_model=ChannelResponse)
def get_channel(channel_db_id: int, db: Session = Depends(get_db)):
    """取得單一頻道。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")
    return _channel_to_response(channel, db)


@router.post("/channels", response_model=ChannelResponse, status_code=201)
def create_channel(data: ChannelCreate, db: Session = Depends(get_db)):
    """新增頻道。"""
    existing = db.query(Channel).filter(
        Channel.channel_id == data.channel_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="此頻道已存在")

    channel = Channel(
        channel_name=data.channel_name,
        channel_id=data.channel_id,
        channel_url=f"https://www.youtube.com/channel/{data.channel_id}",
        description=data.description,
        thumbnail=data.thumbnail,
        streamer=data.streamer,
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)
    logger.info("新增頻道：%s（%s）", channel.channel_name, channel.channel_id)

    sync_channel_videos(channel, db)

    return _channel_to_response(channel, db)


@router.put("/channels/{channel_db_id}", response_model=ChannelResponse)
def update_channel(
    channel_db_id: int, data: ChannelUpdate, db: Session = Depends(get_db)
):
    """更新頻道。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(channel, key, value)

    db.commit()
    db.refresh(channel)
    logger.info("更新頻道：%s", channel.channel_name)
    return _channel_to_response(channel, db)


@router.delete("/channels/{channel_db_id}", status_code=204)
def delete_channel(channel_db_id: int, db: Session = Depends(get_db)):
    """刪除頻道及其所有影片。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    logger.info("刪除頻道：%s（%s）", channel.channel_name, channel.channel_id)
    db.delete(channel)
    db.commit()


@router.patch("/channels/{channel_db_id}/toggle", response_model=ChannelResponse)
def toggle_channel(channel_db_id: int, db: Session = Depends(get_db)):
    """切換頻道啟用狀態。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    channel.is_active = not channel.is_active
    db.commit()
    db.refresh(channel)

    status = "啟用" if channel.is_active else "停用"
    logger.info("頻道 %s 已%s", channel.channel_name, status)

    if channel.is_active:
        sync_channel_videos(channel, db)

    return _channel_to_response(channel, db)
