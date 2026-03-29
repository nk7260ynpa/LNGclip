"""影片相關的 Pydantic schemas。"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VideoResponse(BaseModel):
    """影片回應 schema。"""

    id: int
    channel_id: str
    video_id: str
    title: str
    thumbnail: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
