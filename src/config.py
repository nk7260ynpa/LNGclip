"""應用程式設定管理。"""

import os

# 資料庫連線
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://lngclip:lngclip@localhost:5432/lngclip",
)

# RSS 同步排程
SYNC_SCHEDULE_HOUR = int(os.getenv("SYNC_SCHEDULE_HOUR", "6"))
SYNC_SCHEDULE_MINUTE = int(os.getenv("SYNC_SCHEDULE_MINUTE", "0"))

# 日誌
LOG_DIR = os.getenv("LOG_DIR", "logs")
