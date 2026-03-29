"""頻道 API。"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.channel import Channel
from src.schemas.channel import ChannelCreate, ChannelResponse
from src.services.url_parser import parse_channel_id, normalize_channel_url
from src.services.channel_metadata import fetch_channel_metadata
from src.services.video_fetch import fetch_channel_videos

logger = logging.getLogger(__name__)

router = APIRouter()


def _update_metadata(channel: Channel, db: Session) -> None:
    """抓取並更新頻道元資料。"""
    metadata = fetch_channel_metadata(channel.channel_url)
    if metadata:
        channel.channel_name = metadata["channel_name"]
        channel.subscriber_count = metadata["subscriber_count"]
        channel.video_count = metadata["video_count"]
        db.commit()
        db.refresh(channel)
        logger.info(
            "元資料更新成功：%s（%s）",
            channel.channel_name,
            channel.channel_id,
        )
    else:
        logger.warning("元資料抓取失敗：%s", channel.channel_id)


@router.get("/channels", response_model=list[ChannelResponse])
def list_channels(db: Session = Depends(get_db)):
    """取得所有頻道列表。"""
    channels = db.query(Channel).order_by(Channel.id).all()
    return channels


@router.post("/channels", response_model=ChannelResponse, status_code=201)
def create_channel(data: ChannelCreate, db: Session = Depends(get_db)):
    """新增頻道（從 URL 解析 channel_id，自動抓取元資料）。"""
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
        channel_url=normalize_channel_url(data.url, channel_id),
    )
    db.add(channel)
    db.commit()
    db.refresh(channel)
    logger.info("新增頻道：%s", channel.channel_id)

    _update_metadata(channel, db)
    fetch_channel_videos(channel, db)

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


@router.post(
    "/channels/{channel_db_id}/fetch-metadata",
    response_model=ChannelResponse,
)
def fetch_metadata(channel_db_id: int, db: Session = Depends(get_db)):
    """手動觸發單一頻道的元資料抓取。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    _update_metadata(channel, db)
    return channel


@router.post("/channels/backfill")
def backfill_channels(db: Session = Depends(get_db)):
    """批次補足所有缺失元資料的頻道。"""
    channels = (
        db.query(Channel).filter(Channel.channel_name.is_(None)).all()
    )
    logger.info("開始 backfill，共 %d 個頻道缺失元資料", len(channels))

    results = []
    for channel in channels:
        _update_metadata(channel, db)
        results.append({
            "channel_id": channel.channel_id,
            "channel_name": channel.channel_name,
            "success": channel.channel_name is not None,
        })

    success_count = sum(1 for r in results if r["success"])
    logger.info("Backfill 完成：%d/%d 成功", success_count, len(channels))

    return {
        "total": len(channels),
        "success": success_count,
        "details": results,
    }
