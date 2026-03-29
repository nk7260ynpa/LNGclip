"""頻道 API。"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.channel import Channel
from src.schemas.channel import ChannelCreate, ChannelResponse
from src.services.url_parser import parse_channel_id

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/channels", response_model=list[ChannelResponse])
def list_channels(db: Session = Depends(get_db)):
    """取得所有頻道列表。"""
    channels = db.query(Channel).order_by(Channel.id).all()
    return channels


@router.post("/channels", response_model=ChannelResponse, status_code=201)
def create_channel(data: ChannelCreate, db: Session = Depends(get_db)):
    """新增頻道（從 URL 解析 channel_id）。"""
    try:
        channel_id = parse_channel_id(data.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing = db.query(Channel).filter(
        Channel.channel_id == channel_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="此頻道已存在")

    channel = Channel(
        channel_id=channel_id,
        channel_url=data.url.strip(),
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)
    logger.info("新增頻道：%s", channel.channel_id)

    return channel


@router.delete("/channels/{channel_db_id}", status_code=204)
def delete_channel(channel_db_id: int, db: Session = Depends(get_db)):
    """刪除頻道及其所有影片。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    logger.info("刪除頻道：%s", channel.channel_id)
    db.delete(channel)
    db.commit()
