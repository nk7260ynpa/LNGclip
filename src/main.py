"""LNGclip FastAPI 應用程式入口。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logging_config import setup_logging
from src.models import init_db
from src.services.scheduler import start_scheduler, shutdown_scheduler
from src.api.channels import router as channels_router
from src.api.videos import router as videos_router
from src.api.sync import router as sync_router

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理。"""
    logger.info("LNGclip 後端服務啟動中...")
    init_db()
    logger.info("資料庫初始化完成")
    start_scheduler()
    logger.info("排程器已啟動")
    yield
    shutdown_scheduler()
    logger.info("LNGclip 後端服務已關閉")


app = FastAPI(
    title="LNGclip API",
    description="LNG 精華影片頻道管理平台",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(channels_router, prefix="/api")
app.include_router(videos_router, prefix="/api")
app.include_router(sync_router, prefix="/api")


@app.get("/api/health")
def health_check():
    """健康檢查端點。"""
    return {"status": "ok"}
