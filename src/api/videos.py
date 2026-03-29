"""影片查詢 API。"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import get_db
from src.models.video import Video
from src.schemas.video import VideoResponse

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
