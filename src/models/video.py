"""Video 資料模型。"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class Video(Base):
    """YouTube 影片資料表。"""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    video_id = Column(String(32), unique=True, nullable=False)
    title = Column(String, nullable=False)
    thumbnail = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    channel = relationship("Channel", back_populates="videos")
