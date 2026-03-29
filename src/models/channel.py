"""Channel 資料模型。"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class Channel(Base):
    """YouTube 頻道資料表。"""

    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String(24), unique=True, nullable=False)
    channel_url = Column(String, nullable=False)

    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")
