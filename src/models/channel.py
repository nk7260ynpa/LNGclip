"""Channel 資料模型。"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from src.models.base import Base


class Channel(Base):
    """YouTube 頻道資料表。"""

    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_name = Column(String, nullable=False)
    channel_id = Column(String(24), unique=True, nullable=False)
    channel_url = Column(String)
    description = Column(Text)
    thumbnail = Column(String)
    streamer = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")
