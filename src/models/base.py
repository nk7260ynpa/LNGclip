"""SQLAlchemy Base 宣告。"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """所有 model 的基礎類別。"""


def get_db():
    """取得資料庫 session。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
