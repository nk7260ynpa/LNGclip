"""頻道相關的 Pydantic schemas。"""

from pydantic import BaseModel


class ChannelCreate(BaseModel):
    """新增頻道的請求 schema。"""

    url: str


class ChannelResponse(BaseModel):
    """頻道回應 schema。"""

    id: int
    channel_id: str
    channel_url: str

    model_config = {"from_attributes": True}
