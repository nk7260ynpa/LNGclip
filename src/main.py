"""LNGclip FastAPI 應用程式入口。"""

from contextlib import asynccontextmanager

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.logging_config import setup_logging
from src.models import init_db
from src.api.channels import router as channels_router
from src.api.videos import router as videos_router

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理。"""
    logger.info("LNGclip 後端服務啟動中...")
    init_db()
    logger.info("資料庫初始化完成")
    yield
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

images_dir = os.getenv("IMAGES_DIR", "images")
os.makedirs(images_dir, exist_ok=True)
app.mount("/api/images", StaticFiles(directory=images_dir), name="images")


@app.get("/api/health")
def health_check():
    """健康檢查端點。"""
    return {"status": "ok"}
