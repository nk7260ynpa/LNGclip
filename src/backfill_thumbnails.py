"""一次性腳本：下載所有現有影片的縮圖並更新 DB thumbnail 欄位。"""

import logging

from src.models.base import SessionLocal
from src.models.video import Video
from src.services.video_fetch import _download_thumbnail

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("backfill_thumbnails")


def run():
    """下載所有影片縮圖並更新 thumbnail 欄位。"""
    db = SessionLocal()
    try:
        videos = db.query(Video).all()
        logger.info("開始下載縮圖，共 %d 部影片", len(videos))

        updated = 0
        for video in videos:
            local_path = _download_thumbnail(video.video_id)
            if local_path != video.thumbnail:
                video.thumbnail = local_path
                updated += 1

        db.commit()
        logger.info("縮圖下載完成，更新 %d 筆", updated)
    finally:
        db.close()


if __name__ == "__main__":
    run()
