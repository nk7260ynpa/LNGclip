"""APScheduler 排程服務。"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from src.config import SYNC_SCHEDULE_HOUR, SYNC_SCHEDULE_MINUTE

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def _scheduled_sync():
    """排程觸發的同步任務。"""
    from src.models.base import SessionLocal
    from src.services.rss_sync import sync_all_channels

    logger.info("排程同步任務開始執行")
    db = SessionLocal()
    try:
        sync_all_channels(db)
    except Exception:
        logger.exception("排程同步任務執行失敗")
    finally:
        db.close()


def start_scheduler():
    """啟動排程器。"""
    scheduler.add_job(
        _scheduled_sync,
        "cron",
        hour=SYNC_SCHEDULE_HOUR,
        minute=SYNC_SCHEDULE_MINUTE,
        id="daily_sync",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "排程器已啟動，每日 %02d:%02d 執行同步",
        SYNC_SCHEDULE_HOUR,
        SYNC_SCHEDULE_MINUTE,
    )


def shutdown_scheduler():
    """關閉排程器。"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("排程器已關閉")
