"""資料模型套件。"""

from src.models.base import Base, engine, get_db
from src.models.channel import Channel
from src.models.video import Video


def init_db():
    """建立所有資料表。"""
    Base.metadata.create_all(bind=engine)
