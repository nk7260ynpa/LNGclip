"""定期爬蟲腳本：檢查各頻道是否有新影片並寫入 DB。"""

import logging
import time

from src.models.base import SessionLocal
from src.models.channel import Channel
from src.services.video_fetch import fetch_channel_videos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("crawler")

FETCH_LIMIT = 15
DELAY_SECONDS = 2


def run():
    """執行爬蟲：遍歷所有頻道，抓取最新影片。"""
    start_time = time.time()
    db = SessionLocal()

    try:
        channels = db.query(Channel).all()
        logger.info("開始爬蟲，共 %d 個頻道", len(channels))

        total_new = 0
        for channel in channels:
            new_count = fetch_channel_videos(channel, db, limit=FETCH_LIMIT)
            total_new += new_count
            if new_count > 0:
                logger.info(
                    "頻道 %s 新增 %d 部影片", channel.channel_id, new_count
                )
            time.sleep(DELAY_SECONDS)

        elapsed = round(time.time() - start_time, 2)
        logger.info(
            "爬蟲完成：%d 個頻道，新增 %d 部影片，耗時 %s 秒",
            len(channels),
            total_new,
            elapsed,
        )
    except Exception:
        logger.exception("爬蟲執行失敗")
    finally:
        db.close()


if __name__ == "__main__":
    run()
