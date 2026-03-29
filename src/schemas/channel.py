"""頻道相關的 Pydantic schemas。"""

from typing import Optional

from pydantic import BaseModel


class ChannelCreate(BaseModel):
    """新增頻道的請求 schema。"""

    url: str


class ChannelResponse(BaseModel):
    """頻道回應 schema。"""

    id: int
    channel_id: str
    channel_url: str
    channel_name: Optional[str] = None
    subscriber_count: Optional[int] = None
    video_count: Optional[int] = None

    model_config = {"from_attributes": True}
