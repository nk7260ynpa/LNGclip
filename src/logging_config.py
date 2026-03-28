"""日誌設定模組。"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.config import LOG_DIR


def setup_logging() -> logging.Logger:
    """設定日誌系統，輸出至 console 與檔案。

    Returns:
        根 logger 實例。
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("lngclip")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler（每日輪替）
    file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, "lngclip.log"),
        when="midnight",
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 設定其他模組的 logger 也使用此設定
    logging.getLogger("src").setLevel(logging.INFO)
    for handler in logger.handlers:
        logging.getLogger("src").addHandler(handler)

    return logger
