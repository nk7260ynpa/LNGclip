"""影片查詢 API。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.channel import Channel
from src.models.video import Video
from src.schemas.video import VideoResponse

router = APIRouter()


@router.get(
    "/channels/{channel_db_id}/videos", response_model=list[VideoResponse]
)
def list_channel_videos(
    channel_db_id: int, db: Session = Depends(get_db)
):
    """取得指定頻道的影片列表，依發佈時間倒序排列。"""
    channel = db.query(Channel).filter(Channel.id == channel_db_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="頻道不存在")

    videos = (
        db.query(Video)
        .filter(Video.channel_id == channel_db_id)
        .order_by(Video.published_at.desc())
        .all()
    )
    return videos
