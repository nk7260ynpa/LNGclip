"""頻道相關的 Pydantic schemas。"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChannelCreate(BaseModel):
    """新增頻道的請求 schema。"""

    channel_id: str
    channel_name: str
    streamer: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class ChannelUpdate(BaseModel):
    """更新頻道的請求 schema。"""

    channel_name: Optional[str] = None
    streamer: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    is_active: Optional[bool] = None


class ChannelResponse(BaseModel):
    """頻道回應 schema。"""

    id: int
    channel_name: str
    channel_id: str
    channel_url: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    streamer: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    video_count: int = 0

    model_config = {"from_attributes": True}
